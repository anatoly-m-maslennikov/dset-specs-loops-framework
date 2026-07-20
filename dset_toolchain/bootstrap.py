from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
from collections.abc import Iterator, Sequence
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from datetime import date
from importlib import resources
from pathlib import Path
from typing import Any, cast

from .governance import materialize_governance
from .layout import LAYERS, discover_layout
from .legacy_authority import write_legacy_authority_ledger
from .traceability import write_traceability
from .validation import validate_repository
from .yaml_subset import dump

_KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_PROJECT_KEY = re.compile(r"^[A-Z][A-Z0-9]*$")


class InitializationError(ValueError):
    """The rootless bootstrap transaction is invalid or unsafe."""


@dataclass(frozen=True)
class WorkArea:
    identifier: str
    path: str


@dataclass(frozen=True)
class InitializationResult:
    target: Path
    source: str
    profile: str
    paths: tuple[str, ...]
    executed: bool

    def as_dict(self) -> dict[str, object]:
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
        tempfile.TemporaryDirectory(
            prefix="dset-init-", ignore_cleanup_errors=True
        ) as raw,
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
    identifier, separator, path = raw.partition("=")
    if not separator or not identifier or not path:
        raise InitializationError("work area must use ID=repository/relative/path")
    return WorkArea(identifier, path)


def bundled_source_digest() -> str:
    data = _load_bundle()
    return str(data["sha256"])


@contextmanager
def distribution_source(source_root: Path | None = None) -> Iterator[tuple[Path, str]]:
    """Yield an explicit framework root or the verified packaged source bundle."""

    if source_root is not None:
        source = source_root.resolve()
        manifest = source / "dset" / "scopes" / "meta" / "dset.yaml"
        if not manifest.is_file():
            raise InitializationError(f"source is not a schema 1.2 DSET root: {source}")
        yield source, f"path:{source.as_posix()}"
        return
    with tempfile.TemporaryDirectory(prefix="dset-source-") as raw:
        source = Path(raw)
        bundle = _load_bundle()
        files = cast(dict[str, str], bundle["files"])
        for relative, content in files.items():
            destination = source / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
        yield source, f"bundled:{bundle['sha256']}"


def _load_bundle() -> dict[str, Any]:
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
        candidate = Path(item.path)
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
    source_layout = discover_layout(source)
    for layer in LAYERS:
        layer_root = stage / "dset" / "scopes" / layer
        layer_root.mkdir(parents=True)
        (layer_root / "changes" / "archive").mkdir(parents=True)
        for folder in ("schemas", "templates"):
            origin = source / "dset" / "scopes" / layer / folder
            if origin.is_dir():
                shutil.copytree(origin, layer_root / folder)

    manifest = {
        "schema_version": "1.2",
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
            "runbook": "dset/scopes/ops/supportability/README.md",
        },
        "release": {
            "status": "not-applicable",
            "reason": (
                "bootstrap default; configure a protected publication path explicitly"
            ),
        },
        "work_items": {"registry": "dset/scopes/gov/intake.yaml"},
        "structure": {"layout": "layered-v1"},
        "work_areas": [
            {"id": item.identifier, "path": item.path} for item in work_areas
        ],
        "packages": [{"id": package_id, "status": "active", "layers": ["meta"]}],
        "profiles": {
            "runtime_risk": "non-production",
            "durability_topology": "files",
            "enforcement": "none",
            "artifact": None,
            "repository_governance": profile,
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
    }
    manifest_path = stage / "dset" / "scopes" / "meta" / "dset.yaml"
    manifest_path.write_text(dump(manifest, manifest_path), encoding="utf-8")
    shutil.copyfile(
        source_layout.find_template("dset_settings.toml"),
        stage / "dset_settings.toml",
    )
    _materialize_package(
        source_layout,
        stage,
        project_key,
        package_id,
        project_name,
    )
    gov = stage / "dset" / "scopes" / "gov"
    shutil.copyfile(
        source_layout.find_template("artifact-types.yaml"),
        gov / "artifact-types.yaml",
    )
    shutil.copyfile(source_layout.find_template("intake.yaml"), gov / "intake.yaml")
    provenance_path = gov / "provenance.yaml"
    provenance_path.write_text(
        dump(
            {
                "schema_version": 1.0,
                "project_license": project_license,
                "sources": [],
            },
            provenance_path,
        ),
        encoding="utf-8",
    )
    skill = stage / "dset" / "scopes" / "skill"
    shutil.copyfile(source_layout.find_template("budget.yaml"), skill / "budget.yaml")
    ops = stage / "dset" / "scopes" / "ops"
    supportability = ops / "supportability"
    supportability.mkdir()
    supportability_state = (
        "Active hosted automation was detected during bootstrap. Supportability "
        "is applicable; complete the production runbook before release."
        if hosted_automation
        else "Bootstrap default: not applicable. Reclassify before release."
    )
    (supportability / "README.md").write_text(
        f"# Supportability\n\n{supportability_state}\n",
        encoding="utf-8",
    )
    history = ops / "history"
    history.mkdir()
    history_path = history / "pull-requests.yaml"
    history_path.write_text(
        dump(
            {
                "schema_version": 1.0,
                "repository": repository,
                "authoritative_source": "github",
                "observed_on": date.today().isoformat(),
                "pull_requests": [],
            },
            history_path,
        ),
        encoding="utf-8",
    )
    (stage / ".dset").mkdir()
    (stage / ".dset" / ".gitignore").write_text(
        "runs/\nsessions/\n",
        encoding="utf-8",
    )
    (stage / "dset" / "README.md").write_text(
        "# DSET project control\n\n"
        "Repository-local governance, accepted truth, Changes, and proof.\n",
        encoding="utf-8",
    )
    materialize_governance(source, stage, profile, install_wrappers=True)
    write_legacy_authority_ledger(stage)
    write_traceability(stage)


def _materialize_package(
    source_layout: Any,
    stage: Path,
    project_key: str,
    package_id: str,
    project_name: str,
) -> None:
    destination = stage / "dset" / "scopes" / "meta" / "specs" / "packages" / package_id
    destination.mkdir(parents=True)
    replacements = {
        "{{project_key}}": project_key,
        "{{package_id}}": package_id,
        "{{title}}": project_name,
        "{{id_layer}}": "-META",
        "{{layer}}": "meta",
    }
    names = (
        "README.md",
        "domain.md",
        "spec.md",
        "contracts.md",
        "stories.md",
        "outcomes.md",
        "test-plan.md",
        "eval-plan.md",
    )
    for name in names:
        content = source_layout.find_template(Path("package") / name).read_text(
            encoding="utf-8"
        )
        for old, new in replacements.items():
            content = content.replace(old, new)
        (destination / name).write_text(content, encoding="utf-8")
    manifest = source_layout.find_template("package/layered/package.yaml").read_text(
        encoding="utf-8"
    )
    for old, new in replacements.items():
        manifest = manifest.replace(old, new)
    (destination / "package.yaml").write_text(manifest, encoding="utf-8")


def _commit_stage(stage: Path, target: Path, paths: Sequence[str]) -> None:
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
    if not root.is_dir():
        return
    for path in sorted(
        (item for item in root.rglob("*") if item.is_dir()),
        key=lambda item: len(item.parts),
        reverse=True,
    ):
        with suppress(OSError):
            path.rmdir()
