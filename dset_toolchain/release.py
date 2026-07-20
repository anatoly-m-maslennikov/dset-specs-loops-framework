from __future__ import annotations

import json
import os
import re
import tempfile
from collections.abc import Mapping
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .frontmatter import FrontmatterError
from .frontmatter import parse as parse_frontmatter
from .layout import RepositoryLayout, discover_layout
from .yaml_subset import dump, load

_SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-rc\.(0|[1-9][0-9]*))?$"
)
RELEASE_CLASSES = {"bootstrap", "small", "normal", "rc", "final", "breaking"}
_FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
_PROJECT_VERSION = re.compile(
    r'(?ms)(^\[project\]\s*$.*?^version\s*=\s*")([^"]+)("\s*$)'
)
_MODULE_VERSION = re.compile(r'(?m)^__version__\s*=\s*"([^"]+)"\s*$')


class ReleaseError(ValueError):
    """A release transaction is incomplete, inconsistent, or unsafe."""


@dataclass(frozen=True, order=True)
class ProductVersion:
    major: int
    minor: int
    patch: int
    rc: int | None = None

    @classmethod
    def parse(cls, raw: str) -> ProductVersion:
        match = _SEMVER.fullmatch(raw)
        if match is None:
            raise ValueError(f"invalid DSET product version: {raw}")
        major, minor, patch, rc = match.groups()
        return cls(int(major), int(minor), int(patch), int(rc) if rc else None)

    @property
    def semver(self) -> str:
        base = f"{self.major}.{self.minor}.{self.patch}"
        return f"{base}-rc.{self.rc}" if self.rc is not None else base

    @property
    def python(self) -> str:
        base = f"{self.major}.{self.minor}.{self.patch}"
        return f"{base}rc{self.rc}" if self.rc is not None else base


def expected_target(
    base: str | None,
    release_class: str,
    *,
    bootstrap_target: str | None = None,
    readiness_passed: bool = False,
) -> ProductVersion:
    if release_class not in RELEASE_CLASSES:
        raise ValueError(f"unknown release class: {release_class}")
    if release_class == "bootstrap":
        if base not in {None, "unversioned"}:
            raise ValueError("bootstrap requires an unversioned base")
        if bootstrap_target is None:
            raise ValueError("bootstrap requires an explicit target")
        target = ProductVersion.parse(bootstrap_target)
        if target.major != 0 or target.rc is not None:
            raise ValueError("bootstrap target must be a stable pre-1.0 version")
        return target
    if base in {None, "unversioned"}:
        raise ValueError(f"{release_class} requires a versioned base")

    current = ProductVersion.parse(base)
    if release_class == "rc":
        if current.rc is not None:
            return ProductVersion(1, 0, 0, current.rc + 1)
        if current.major != 0 or not readiness_passed:
            raise ValueError("the first 1.0 RC requires a passing pre-1.0 base")
        return ProductVersion(1, 0, 0, 1)
    if release_class == "final":
        if current != ProductVersion(1, 0, 0, current.rc) or current.rc is None:
            raise ValueError("final requires a 1.0.0 RC base")
        if not readiness_passed:
            raise ValueError("final requires passing readiness")
        return ProductVersion(1, 0, 0)
    if current.rc is not None:
        raise ValueError("published RCs advance only to a higher RC or final")
    if release_class == "small":
        return ProductVersion(current.major, current.minor, current.patch + 1)
    if release_class == "normal":
        return ProductVersion(current.major, current.minor + 1, 0)
    if release_class == "breaking" and current.major >= 1:
        return ProductVersion(current.major + 1, 0, 0)
    raise ValueError("breaking releases require a stable post-1.0 base")


def validate_coordinated_identity(product: str, python_package: str) -> None:
    version = ProductVersion.parse(product)
    if python_package != version.python:
        raise ValueError(
            "Python package version must be the exact PEP 440 serialization "
            f"of {version.semver}: {version.python}"
        )


@dataclass(frozen=True)
class ReleasePlan:
    owner_change: str
    owner_manifest: str
    release_class: str
    base_ref: str
    base_commit: str
    base_version: str
    candidate_commit: str
    target: str
    python_target: str
    tag: str
    publisher: str
    integration_branch: str
    protected_branch: str
    readiness: str
    surfaces: dict[str, str]
    changes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "owner_change": self.owner_change,
            "owner_manifest": self.owner_manifest,
            "release_class": self.release_class,
            "base": {
                "ref": self.base_ref,
                "commit": self.base_commit,
                "version": self.base_version,
            },
            "candidate_commit": self.candidate_commit,
            "target": self.target,
            "python_target": self.python_target,
            "tag": self.tag,
            "publisher": self.publisher,
            "integration_branch": self.integration_branch,
            "protected_branch": self.protected_branch,
            "readiness": self.readiness,
            "surfaces": dict(self.surfaces),
            "changes": list(self.changes),
            "prepared": not self.changes,
        }


@dataclass(frozen=True)
class ReleasePreparation:
    plan: ReleasePlan
    executed: bool
    changed: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        data = self.plan.to_dict()
        data.update({"executed": self.executed, "changed": list(self.changed)})
        return data


def plan_release(root: Path) -> ReleasePlan:
    """Build one deterministic, read-only plan from the committed declaration."""

    root = root.resolve()
    layout = discover_layout(root)
    manifest = _mapping(load(layout.manifest_path), "project manifest")
    project_release = _mapping(manifest.get("release"), "project release config")
    if project_release.get("status") != "applicable":
        raise ReleaseError("release is not applicable to this project")
    integration = _required_string(project_release, "integration_branch")
    protected = _required_string(project_release, "protected_branch")
    publisher = _required_string(project_release, "publisher")
    tag_pattern = _required_string(project_release, "tag_pattern")
    if publisher != "github":
        raise ReleaseError(f"unsupported release publisher: {publisher}")
    if tag_pattern.count("{product_version}") != 1:
        raise ReleaseError(
            "release tag pattern must contain exactly one {product_version} placeholder"
        )

    prepared_version = _current_product_version(layout.version_path)
    owner_path, owner, references = _release_owner(
        layout.active_change_roots,
        layout.archive_change_roots,
        prepared_version,
    )
    owner_id = _required_string(owner, "id")
    declaration = _mapping(owner.get("release"), "release declaration")
    release_class = _required_string(declaration, "class")
    if release_class not in RELEASE_CLASSES:
        raise ReleaseError(f"unknown release class: {release_class}")
    for reference_id, target in references:
        if target != owner_id:
            raise ReleaseError(
                "release owner reference must target "
                f"{owner_id}: {reference_id}/{target}"
            )

    base = _mapping(declaration.get("base"), "release base")
    base_ref = _required_string(base, "ref")
    base_commit = _required_string(base, "commit")
    base_version = _required_string(base, "version")
    candidate_commit = _required_string(declaration, "candidate_commit")
    target = _required_string(declaration, "target")
    readiness_relative = _required_string(declaration, "readiness")
    if base_ref != protected:
        raise ReleaseError(
            f"release base ref must be the protected branch {protected}: {base_ref}"
        )
    if _FULL_SHA.fullmatch(base_commit) is None:
        raise ReleaseError("release base commit must be a full SHA")
    if _FULL_SHA.fullmatch(candidate_commit) is None:
        raise ReleaseError("release candidate commit must be a full SHA")
    readiness = _contained_file(owner_path, readiness_relative, "readiness")
    readiness_passed = _readiness_passed(readiness, candidate_commit)

    try:
        computed = expected_target(
            base_version,
            release_class,
            bootstrap_target=target if release_class == "bootstrap" else None,
            readiness_passed=readiness_passed,
        )
    except ValueError as error:
        raise ReleaseError(str(error)) from error
    if computed.semver != target:
        raise ReleaseError(
            f"declared target does not match {release_class} transition: "
            f"{target} != {computed.semver}"
        )
    tag = tag_pattern.replace("{product_version}", computed.semver)
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", tag) is None:
        raise ReleaseError(f"rendered release tag is not supported safely: {tag}")

    surfaces = _read_version_surfaces(root, layout.version_path)
    changes = tuple(
        sorted(
            {
                _surface_path(root, name)
                for name, value in surfaces.items()
                if value != _surface_target(name, computed)
            }
        )
    )
    return ReleasePlan(
        owner_change=owner_id,
        owner_manifest=RepositoryLayout.structured_file(owner_path, "change.toml")
        .relative_to(root)
        .as_posix(),
        release_class=release_class,
        base_ref=base_ref,
        base_commit=base_commit,
        base_version=base_version,
        candidate_commit=candidate_commit,
        target=computed.semver,
        python_target=computed.python,
        tag=tag,
        publisher=publisher,
        integration_branch=integration,
        protected_branch=protected,
        readiness=readiness.relative_to(root).as_posix(),
        surfaces=surfaces,
        changes=changes,
    )


def check_release(root: Path) -> ReleasePlan:
    """Require every committed release mirror to match its declaration."""

    plan = plan_release(root)
    if plan.changes:
        raise ReleaseError(
            "release is not prepared; mismatched version surfaces: "
            + ", ".join(plan.changes)
        )
    validate_coordinated_identity(plan.target, plan.python_target)
    return plan


def prepare_release(root: Path, *, execute: bool = False) -> ReleasePreparation:
    """Preview or atomically synchronize the declared version surfaces.

    The default is read-only. ``execute=True`` is the explicit repository-write
    boundary. Every file replacement is atomic and a repeated preparation is a
    no-op. Publication is intentionally outside this function.
    """

    root = root.resolve()
    plan = plan_release(root)
    if not execute or not plan.changes:
        return ReleasePreparation(plan, execute, ())
    _require_safe_prepare_inputs(plan)
    layout = discover_layout(root)
    changed: list[str] = []
    version_path = layout.version_path
    if version_path.relative_to(root).as_posix() in plan.changes:
        version_data = _mapping(load(version_path), "version contract")
        framework = _mapping(version_data.get("framework"), "framework version")
        package = _mapping(version_data.get("python_package"), "package version")
        framework["version"] = plan.target
        package["version"] = plan.python_target
        _atomic_replace_text(version_path, dump(version_data, version_path))
        changed.append(version_path.relative_to(root).as_posix())
    pyproject = root / "pyproject.toml"
    if pyproject.relative_to(root).as_posix() in plan.changes:
        text = pyproject.read_text(encoding="utf-8")
        updated, count = _PROJECT_VERSION.subn(
            lambda match: f"{match.group(1)}{plan.python_target}{match.group(3)}",
            text,
            count=1,
        )
        if count != 1:
            raise ReleaseError("pyproject project version is not uniquely writable")
        _atomic_replace_text(pyproject, updated)
        changed.append(pyproject.relative_to(root).as_posix())
    module = root / "dset_toolchain" / "__init__.py"
    if module.relative_to(root).as_posix() in plan.changes:
        text = module.read_text(encoding="utf-8")
        updated, count = _MODULE_VERSION.subn(
            f'__version__ = "{plan.python_target}"', text, count=1
        )
        if count != 1:
            raise ReleaseError("Python module version is not uniquely writable")
        _atomic_replace_text(module, updated)
        changed.append(module.relative_to(root).as_posix())
    prepared = check_release(root)
    return ReleasePreparation(prepared, True, tuple(changed))


def _release_owner(
    active_roots: tuple[Path, ...],
    archive_roots: tuple[Path, ...],
    prepared_version: str,
) -> tuple[Path, dict[str, Any], list[tuple[str, str]]]:
    declarations: list[tuple[Path, dict[str, Any]]] = []
    references: list[tuple[str, str]] = []
    for root in active_roots:
        if not root.is_dir():
            continue
        for path in sorted(root.iterdir()):
            manifest_path = RepositoryLayout.structured_file(path, "change.toml")
            if path.name == "archive" or not manifest_path.is_file():
                continue
            data = _mapping(load(manifest_path), f"Change manifest {manifest_path}")
            release = data.get("release")
            if not isinstance(release, dict):
                continue
            if "class" in release:
                declarations.append((path, data))
            elif isinstance(release.get("owner_change"), str):
                references.append(
                    (str(data.get("id", path.name)), release["owner_change"])
                )
    if not declarations:
        for root in archive_roots:
            if not root.is_dir():
                continue
            for path in sorted(root.iterdir()):
                manifest_path = RepositoryLayout.structured_file(path, "change.toml")
                if not manifest_path.is_file():
                    continue
                data = _mapping(load(manifest_path), f"Change manifest {manifest_path}")
                release = data.get("release")
                if (
                    isinstance(release, dict)
                    and release.get("target") == prepared_version
                    and "class" in release
                ):
                    declarations.append((path, data))
    if len(declarations) != 1:
        raise ReleaseError(
            f"release preparation requires exactly one owner declaration; "
            f"found {len(declarations)}"
        )
    owner_path, owner = declarations[0]
    return owner_path, owner, references


def _current_product_version(version_path: Path) -> str:
    version_data = _mapping(load(version_path), "version contract")
    framework = _mapping(version_data.get("framework"), "framework version")
    return _required_string(framework, "version")


def _readiness_passed(path: Path, candidate_commit: str) -> bool:
    try:
        parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        raise ReleaseError(f"cannot read Readiness Record: {path}") from error
    except FrontmatterError as error:
        raise ReleaseError("Readiness Record frontmatter is invalid") from error
    if parsed is None:
        raise ReleaseError("Readiness Record requires TOML or YAML frontmatter")
    data, _body, _format = parsed
    if (
        not isinstance(data, dict)
        or data.get("artifact_type") != "delivery"
        or data.get("artifact_subtype") != "readiness_record"
    ):
        raise ReleaseError("release readiness must use a Readiness Record")
    if data.get("candidate_sha") != candidate_commit:
        raise ReleaseError(
            "Readiness Record candidate does not match release candidate"
        )
    for field in ("artifact_id", "version_scope_ref", "release_plan_ref"):
        value = data.get(field)
        if not isinstance(value, str) or not value or value == "pending":
            raise ReleaseError(f"Readiness Record field is incomplete: {field}")
    disposition = data.get("disposition")
    if disposition not in {"ready", "blocked"}:
        raise ReleaseError("Readiness Record disposition must be ready or blocked")
    if disposition != "ready":
        raise ReleaseError("Readiness Record blocks this release candidate")
    return True


def _read_version_surfaces(root: Path, version_path: Path) -> dict[str, str]:
    version_data = _mapping(load(version_path), "version contract")
    framework = _mapping(version_data.get("framework"), "framework version")
    package = _mapping(version_data.get("python_package"), "package version")
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")
    project_matches = list(_PROJECT_VERSION.finditer(pyproject))
    if len(project_matches) != 1:
        raise ReleaseError("pyproject must contain one [project] version")
    module_text = (root / "dset_toolchain" / "__init__.py").read_text(encoding="utf-8")
    module_matches = _MODULE_VERSION.findall(module_text)
    if len(module_matches) != 1:
        raise ReleaseError("Python module must contain one __version__")
    return {
        "framework": _required_string(framework, "version"),
        "python_package": _required_string(package, "version"),
        "pyproject": project_matches[0].group(2),
        "module": module_matches[0],
    }


def _surface_target(name: str, target: ProductVersion) -> str:
    return target.semver if name == "framework" else target.python


def _surface_path(root: Path, name: str) -> str:
    if name in {"framework", "python_package"}:
        return discover_layout(root).version_path.relative_to(root).as_posix()
    if name == "pyproject":
        return "pyproject.toml"
    if name == "module":
        return "dset_toolchain/__init__.py"
    raise ReleaseError(f"unknown version surface: {name}")


def _require_safe_prepare_inputs(plan: ReleasePlan) -> None:
    target = ProductVersion.parse(plan.target)
    if plan.base_version == "unversioned":
        allowed_products = {target.semver}
        allowed_python = {target.python}
    else:
        base = ProductVersion.parse(plan.base_version)
        allowed_products = {base.semver, target.semver}
        allowed_python = {base.python, target.python}
    for name, current in plan.surfaces.items():
        allowed = allowed_products if name == "framework" else allowed_python
        if current not in allowed:
            raise ReleaseError(
                f"refusing to overwrite unexpected {name} version: {current}"
            )


def _contained_file(root: Path, raw: str, kind: str) -> Path:
    path = (root / raw).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as error:
        raise ReleaseError(f"{kind} path escapes the release owner") from error
    if not path.is_file():
        raise ReleaseError(f"{kind} artifact is missing: {raw}")
    return path


def _mapping(raw: Any, name: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ReleaseError(f"{name} must be a mapping")
    return raw


def _required_string(data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ReleaseError(f"{key} must be a non-empty string")
    return value


def _atomic_replace_text(path: Path, text: str) -> None:
    descriptor, raw = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(raw)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, path.stat().st_mode)
        os.replace(temporary, path)
    except Exception:
        with suppress(FileNotFoundError):
            temporary.unlink()
        raise


def rendered_plan(plan: ReleasePlan) -> str:
    return json.dumps(plan.to_dict(), indent=2, sort_keys=True)
