"""Provide DSET bootstrap behavior."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections.abc import Iterator, Sequence
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from importlib import resources
from pathlib import Path, PurePosixPath
from typing import Any, cast

from .layout import (
    APPLIED_LAYER_DIRECTORIES,
    APPLIED_PROJECT_ROOT,
    APPLIED_VERSIONS_ROOT,
    LAYER_ID_TOKENS,
    LAYERS,
    METHODOLOGY_LAYER_DIRECTORIES,
    METHODOLOGY_ROOT,
    SEPARATED_METHODOLOGY_LAYOUT,
    SEPARATED_SCHEMA_VERSION,
    discover_layout,
    has_manifest,
)
from .project_data import project_section
from .temp_paths import temporary_directory
from .validation import validate_repository
from .structured_data import dump, load

# _KEBAB validates kebab; this module owns the accepted syntax.
_KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# _PROJECT_KEY validates project key; this module owns the accepted syntax.
_PROJECT_KEY = re.compile(r"^[A-Z][A-Z0-9]*$")


class InitializationError(ValueError):
    """The rootless bootstrap transaction is invalid or unsafe."""


@dataclass(frozen=True)
class WorkArea:
    """Represent work area behavior and state."""

    identifier: str
    path: str


@dataclass(frozen=True)
class InitializationResult:
    """Represent initialization result behavior and state."""

    target: Path
    source: str
    profile: str
    paths: tuple[str, ...]
    executed: bool

    def as_dict(self) -> dict[str, object]:
        """Handle dict using the declared repository contract."""
        return {
            "target": self.target.as_posix(),
            "source": self.source,
            "profile": self.profile,
            "paths": list(self.paths),
            "executed": self.executed,
            "next": "run dset rules check, then start a new dset invocation",
        }


def initialize_project(
    target: Path,
    *,
    project_key: str,
    project_id: str,
    project_name: str,
    project_license: str,
    package_id: str = "project",
    repository: str | None = None,
    work_areas: Sequence[WorkArea] = (),
    profile: str = "core-v1",
    source_root: Path | None = None,
    execute: bool = False,
) -> InitializationResult:
    """Preview or execute one bounded rootless initialization transaction."""

    target = target.resolve()
    _validate_inputs(
        project_key,
        project_id,
        project_name,
        project_license,
        package_id,
        work_areas,
    )
    with (
        distribution_source(source_root) as (source, source_identity),
        temporary_directory(prefix="dset-init-") as raw,
    ):
        stage = Path(raw) / "project"
        stage.mkdir()
        _stage_project(
            source,
            stage,
            project_key=project_key,
            project_id=project_id,
            project_name=project_name,
            project_license=project_license,
            package_id=package_id,
            repository=repository or project_id,
            work_areas=work_areas,
            profile=profile,
            hosted_automation=(target / ".github" / "workflows").is_dir(),
        )
        paths = tuple(
            path.relative_to(stage).as_posix()
            for path in sorted(stage.rglob("*"))
            if path.is_file()
        )
        collisions = [relative for relative in paths if (target / relative).exists()]
        if collisions:
            raise FileExistsError(
                "initialization destination exists: " + ", ".join(collisions[:5])
            )
        if execute:
            _commit_stage(stage, target, paths)
            diagnostics = validate_repository(target)
            if diagnostics:
                _rollback_paths(target, paths)
                rendered = "; ".join(item.render(target) for item in diagnostics[:5])
                raise InitializationError(
                    f"initialized project failed validation: {rendered}"
                )
        return InitializationResult(
            target=target,
            source=source_identity,
            profile=profile,
            paths=paths,
            executed=execute,
        )


def parse_work_area(raw: str) -> WorkArea:
    """Parse work area using the declared repository contract."""
    identifier, separator, path = raw.partition("=")
    if not separator or not identifier or not path:
        raise InitializationError("work area must use ID=repository/relative/path")
    return WorkArea(identifier, path)


def bundled_source_digest() -> str:
    """Handle source digest using the declared repository contract."""
    data = _load_bundle()
    return str(data["sha256"])


@contextmanager
def distribution_source(source_root: Path | None = None) -> Iterator[tuple[Path, str]]:
    """Yield an explicit framework root or the verified packaged source bundle."""

    if source_root is not None:
        source = source_root.resolve()
        layout = discover_layout(source)
        if not has_manifest(source) or not (layout.recursive or layout.separated):
            raise InitializationError(
                f"source is not a schema 1.4 or 1.5 DSET root: {source}"
            )
        yield source, f"path:{source.as_posix()}"
        return
    with temporary_directory(prefix="dset-source-") as raw:
        source = Path(raw)
        bundle = _load_bundle()
        files = cast(dict[str, str], bundle["files"])
        for relative, content in files.items():
            destination = source / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
        yield source, f"bundled:{bundle['sha256']}"


def _load_bundle() -> dict[str, Any]:
    """Load bundle using the declared repository contract."""
    path = resources.files("dset_toolchain").joinpath("bootstrap_bundle.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("files"), dict):
        raise InitializationError("bundled bootstrap source is invalid")
    files = cast(dict[str, str], data["files"])
    encoded = json.dumps(
        files, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    digest = hashlib.sha256(encoded).hexdigest()
    if data.get("sha256") != digest:
        raise InitializationError("bundled bootstrap source digest mismatch")
    return cast(dict[str, Any], data)


def _validate_inputs(
    project_key: str,
    project_id: str,
    project_name: str,
    project_license: str,
    package_id: str,
    work_areas: Sequence[WorkArea],
) -> None:
    """Validate inputs using the declared repository contract."""
    if _PROJECT_KEY.fullmatch(project_key) is None:
        raise InitializationError("project key must be an uppercase ID segment")
    for label, value in (("project ID", project_id), ("package ID", package_id)):
        if _KEBAB.fullmatch(value) is None:
            raise InitializationError(f"{label} must be lowercase kebab-case")
    if not project_name.strip():
        raise InitializationError("project name must not be empty")
    if not project_license.strip() or len(project_license) > 128:
        raise InitializationError("project license must contain 1..128 characters")
    identifiers = [item.identifier for item in work_areas]
    paths = [item.path for item in work_areas]
    if len(identifiers) != len(set(identifiers)) or len(paths) != len(set(paths)):
        raise InitializationError("work-area IDs and paths must be unique")
    for item in work_areas:
        if _KEBAB.fullmatch(item.identifier) is None:
            raise InitializationError("work-area IDs must be lowercase kebab-case")
        candidate = PurePosixPath(item.path)
        if (
            candidate.is_absolute()
            or "\\" in item.path
            or any(part in {"", ".", ".."} for part in candidate.parts)
        ):
            raise InitializationError("work-area paths must be repository-relative")


def _stage_project(
    source: Path,
    stage: Path,
    *,
    project_key: str,
    project_id: str,
    project_name: str,
    project_license: str,
    package_id: str,
    repository: str,
    work_areas: Sequence[WorkArea],
    profile: str,
    hosted_automation: bool,
) -> None:
    """Handle project using the declared repository contract."""
    source_layout = discover_layout(source)
    dset_root = stage / ".dset"
    dset_root.mkdir()
    methodology_root = dset_root / METHODOLOGY_ROOT
    methodology_root.mkdir()
    for directory in ("00_project", *METHODOLOGY_LAYER_DIRECTORIES.values()):
        (methodology_root / directory).mkdir()
    for directory in (
        APPLIED_PROJECT_ROOT,
        *APPLIED_LAYER_DIRECTORIES.values(),
        APPLIED_VERSIONS_ROOT,
    ):
        (dset_root / directory).mkdir()
    if source_layout.separated:
        shutil.copytree(
            source_layout.dset_root / METHODOLOGY_ROOT,
            methodology_root,
            dirs_exist_ok=True,
        )
    else:
        raise InitializationError(
            "schema 1.5 separated methodology is required for initialization"
        )

    manifest = {
        "schema_version": SEPARATED_SCHEMA_VERSION,
        "project": {
            "key": project_key,
            "id": project_id,
            "name": project_name,
            "repository_slug": project_id,
            "repository_role": "adopter",
        },
        "supportability": {
            "status": "applicable" if hosted_automation else "not-applicable",
            "reason": (
                "active hosted automation detected during bootstrap; complete "
                "production supportability before release"
                if hosted_automation
                else (
                    "bootstrap default; classify production supportability "
                    "before release"
                )
            ),
            "authority": "local-repository",
            "runbook": "000_dset-ops-supportability-delivery-runbook.md",
        },
        "release": {
            "status": "not-applicable",
            "reason": (
                "bootstrap default; configure a protected publication path explicitly"
            ),
            "integration_branch": "dev",
            "protected_branch": "main",
        },
        "work_items": {
            "atomic_scopes": [
                "project-control",
                *(f"project-{layer}" for layer in LAYERS),
            ]
        },
        "structure": {"layout": SEPARATED_METHODOLOGY_LAYOUT},
        "work_areas": [
            {"id": item.identifier, "path": item.path} for item in work_areas
        ],
        "packages": [{"id": package_id, "status": "active", "layers": ["meta"]}],
        "profiles": {
            "runtime_risk": "non-production",
            "durability_topology": "files",
            "enforcement": "none",
            "repository_governance": profile,
            "implementation": [],
        },
        "change_contract": {
            "change_id_format": "project-type-layer-sequence",
            "change_slug_format": "kebab-case",
            "pull_request_required_before_archive": True,
            "archive_requires_fresh_verification": True,
            "keep_pull_request_draft_until_archive_ready": True,
        },
        "commit_provenance": {"start_commit": "manifest-addition"},
        "verification": {"commands": ["{python} -m dset_toolchain check ."]},
        "canonical_command": "python -m dset_toolchain verify .",
        "artifact_catalog": project_section(source, "artifact_catalog"),
        "artifact_structure": _artifact_structure(project_key),
        "governance_registry": project_section(source, "governance_registry"),
        "source_provenance": {
            "schema_version": 1.0,
            "project_license": project_license,
            "sources": [],
        },
        "version_registry": project_section(source, "version_registry"),
        "package_catalog": {
            "packages": [
                {
                    "schema_version": SEPARATED_SCHEMA_VERSION,
                    "package_id": package_id,
                    "layer": "meta",
                    "requirements": [],
                    "tests": [],
                    "evals": [],
                    "contracts": [],
                    "stories": [],
                    "outcomes": [],
                    "artifacts": _package_artifact_names(project_key),
                }
            ]
        },
    }
    manifest_path = dset_root / "dset_settings.toml"
    _write_combined_settings(
        source_layout.find_template("dset_settings.toml"), manifest_path, manifest
    )
    _materialize_package(
        source_layout,
        stage,
        project_key,
        package_id,
        project_name,
    )
    ops = dset_root / APPLIED_LAYER_DIRECTORIES["ops"]
    supportability = ops / "supportability"
    supportability.mkdir()
    supportability_state = (
        "Active hosted automation was detected during bootstrap. Supportability "
        "is applicable; complete the production runbook before release."
        if hosted_automation
        else "Bootstrap default: not applicable. Reclassify before release."
    )
    (supportability / f"{project_key}-OPS-SUPPORTABILITY.md").write_text(
        f"# Supportability\n\n{supportability_state}\n",
        encoding="utf-8",
    )
    (dset_root / "DSET-CONTROL-HUB.md").write_text(
        "# Project-local DSET control plane\n\n"
        "## Purpose\n\nOwn settings, installed methodology, and applied artifacts.\n\n"
        "## Boundaries\n\nSkills resolve DSET identities only inside this "
        "control root.\n\n"
        "## Start here\n\n"
        "- `dset_settings.toml`\n"
        "- `000_dset-methodology-hub.md`\n"
        f"- `{project_key}-PROJECT-HUB.md`\n",
        encoding="utf-8",
    )
    (dset_root / APPLIED_PROJECT_ROOT / f"{project_key}-PROJECT-HUB.md").write_text(
        "# Applied project-wide DSET artifacts\n\n"
        "## Purpose\n\nOwn project-wide evergreen artifacts and atomic records.\n\n"
        "## Boundaries\n\nLayer-specific truth belongs to its applied layer.\n\n"
        "## Start here\n\nUse the unique applied layer hub names.\n",
        encoding="utf-8",
    )
    (dset_root / APPLIED_VERSIONS_ROOT / f"{project_key}-VERSIONS-HUB.md").write_text(
        "# Version lifecycle\n\n"
        "## Purpose\n\nOwn project-wide Changes and release records.\n\n"
        "## Boundaries\n\nVersion records do not replace Decision authority.\n\n"
        "## Start here\n\nSearch by unique Version identity.\n",
        encoding="utf-8",
    )
    for layer in LAYERS:
        hub = (
            dset_root
            / APPLIED_LAYER_DIRECTORIES[layer]
            / f"{project_key}-{LAYER_ID_TOKENS[layer]}-HUB.md"
        )
        if hub.exists():
            continue
        hub.write_text(
            f"# Applied {LAYER_ID_TOKENS[layer]} artifacts\n\n"
            "## Purpose\n\nOwn project atoms and evergreen artifacts.\n\n"
            "## Boundaries\n\nInstalled methodology remains separate.\n\n"
            "## Start here\n\nSearch by unique artifact or document identity.\n",
            encoding="utf-8",
        )
    _copy_governance_wrappers(source, stage)


def _copy_governance_wrappers(source: Path, stage: Path) -> None:
    """Handle governance wrappers using the declared repository contract."""
    registry = project_section(source, "governance_registry")
    copied: set[Path] = set()
    for item in cast(list[dict[str, Any]], registry.get("wrappers", [])):
        skill = item.get("skill")
        if not isinstance(skill, str) or not skill or Path(skill).name != skill:
            continue
        origin = source / "skills" / skill / "SKILL.md"
        destination = stage / "skills" / skill / "SKILL.md"
        if origin.parent in copied:
            continue
        shutil.copytree(origin.parent, destination.parent)
        copied.add(origin.parent)


def _materialize_package(
    source_layout: Any,
    stage: Path,
    project_key: str,
    package_id: str,
    project_name: str,
) -> None:
    """Handle package using the declared repository contract."""
    destination = stage / ".dset" / APPLIED_LAYER_DIRECTORIES["meta"]
    replacements = {
        "{{project_key}}": project_key,
        "{{package_id}}": package_id,
        "{{title}}": project_name,
        "{{id_layer}}": "-META",
        "{{layer}}": "meta",
    }
    names = {
        "README.md": f"{project_key}-META-HUB.md",
        "domain.md": f"{project_key}-META-specification-domain.md",
        "spec.md": f"{project_key}-META-specification-methodology.md",
        "contracts.md": f"{project_key}-META-specification-contracts.md",
        "stories.md": f"{project_key}-META-specification-user-stories.md",
        "outcomes.md": f"{project_key}-META-specification-outcomes.md",
        "test-plan.md": f"{project_key}-META-plan-tests.md",
        "eval-plan.md": f"{project_key}-META-plan-evaluations.md",
    }
    for source_name, target_name in names.items():
        content = source_layout.find_template(Path("package") / source_name).read_text(
            encoding="utf-8"
        )
        for old, new in replacements.items():
            content = content.replace(old, new)
        for old, new in names.items():
            content = content.replace(f"]({old})", f"]({new})")
        (destination / target_name).write_text(content, encoding="utf-8")
    source = source_layout.find_template("package/layered/package.yaml")
    manifest = _replace_structured_values(load(source), replacements)
    assert isinstance(manifest, dict)
    manifest["artifacts"] = _package_artifact_names(project_key)
    target = destination / "package.toml"
    target.write_text(dump(manifest, target), encoding="utf-8")


def _package_artifact_names(project_key: str) -> dict[str, str]:
    """Handle artifact names using the declared repository contract."""
    return {
        "hub": f"{project_key}-META-HUB.md",
        "domain": f"{project_key}-META-specification-domain.md",
        "spec": f"{project_key}-META-specification-methodology.md",
        "contracts": f"{project_key}-META-specification-contracts.md",
        "stories": f"{project_key}-META-specification-user-stories.md",
        "outcomes": f"{project_key}-META-specification-outcomes.md",
        "test_plan": f"{project_key}-META-plan-tests.md",
        "eval_plan": f"{project_key}-META-plan-evaluations.md",
    }


def _artifact_structure(project_key: str) -> dict[str, Any]:
    """Handle structure using the declared repository contract."""
    areas = [
        {
            "id": "installed-methodology",
            "hub": "000_dset-methodology-hub.md",
            "parent": "framework-control",
            "owner": "methodology",
            "purpose": "Installed project-local DSET methodology",
        },
        {
            "id": "project-control",
            "hub": f"{project_key}-PROJECT-HUB.md",
            "parent": "framework-control",
            "owner": "project",
            "purpose": "Project-wide evergreen truth and atomic records",
        },
    ]
    for layer in LAYERS:
        areas.append(
            {
                "id": f"project-{layer}",
                "hub": f"{project_key}-{LAYER_ID_TOKENS[layer]}-HUB.md",
                "parent": "project-control",
                "owner": layer,
                "purpose": f"Project-owned {LAYER_ID_TOKENS[layer]} truth",
            }
        )
    areas.append(
        {
            "id": "project-versions",
            "hub": f"{project_key}-VERSIONS-HUB.md",
            "parent": "project-control",
            "owner": "ops",
            "purpose": "Version scopes, roadmaps, changes, and release records",
        }
    )
    return {
        "schema_version": 1.0,
        "profile": "documentation-v1",
        "root": {
            "id": "framework-control",
            "hub": "DSET-CONTROL-HUB.md",
            "owner": "framework",
            "purpose": "Repository-local DSET control plane",
        },
        "areas": areas,
    }


def _write_combined_settings(
    template: Path, target: Path, manifest: dict[str, Any]
) -> None:
    """Write combined settings using the declared repository contract."""
    behavior = template.read_text(encoding="utf-8").rstrip()
    project = dict(manifest)
    project.pop("schema_version", None)
    project.pop("canonical_command", None)
    if not project.get("work_areas"):
        project.pop("work_areas", None)
        behavior = behavior.replace(
            'canonical_command = "python -m dset_toolchain verify ."',
            'canonical_command = "python -m dset_toolchain verify ."\nwork_areas = []',
            1,
        )
    rendered = (
        behavior
        + "\n\n# Project identity, topology, and executable boundaries.\n\n"
        + dump(project, target)
    )
    target.write_text(rendered, encoding="utf-8")


def _copy_structured(source: Path, target: Path) -> None:
    """Copy one structured template without mixing its syntax and suffix."""

    target.write_text(dump(load(source), target), encoding="utf-8")


def _replace_structured_values(value: object, replacements: dict[str, str]) -> object:
    """Handle structured values using the declared repository contract."""
    if isinstance(value, dict):
        return {
            key: _replace_structured_values(item, replacements)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_replace_structured_values(item, replacements) for item in value]
    if isinstance(value, str):
        for old, new in replacements.items():
            value = value.replace(old, new)
    return value


def _commit_stage(stage: Path, target: Path, paths: Sequence[str]) -> None:
    """Handle stage using the declared repository contract."""
    created: list[Path] = []
    try:
        target.mkdir(parents=True, exist_ok=True)
        for relative in paths:
            source = stage / relative
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as stream:
                stream.write(source.read_bytes())
            created.append(destination)
    except Exception:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        _remove_empty_directories(target)
        raise


def _rollback_paths(target: Path, paths: Sequence[str]) -> None:
    for relative in reversed(paths):
        (target / relative).unlink(missing_ok=True)
    _remove_empty_directories(target)


def _remove_empty_directories(root: Path) -> None:
    """Handle empty directories using the declared repository contract."""
    if not root.is_dir():
        return
    for path in sorted(
        (item for item in root.rglob("*") if item.is_dir()),
        key=lambda item: len(item.parts),
        reverse=True,
    ):
        with suppress(OSError):
            path.rmdir()
