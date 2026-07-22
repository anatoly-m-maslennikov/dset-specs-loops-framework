"""Provide DSET skill distribution behavior."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import sys
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path, PurePath
from typing import Any

from . import __version__
from .bootstrap import distribution_source
from .skill_catalog import PUBLIC_SKILL_WORKFLOWS, SKILL_INVOCATION_MARKERS
from .skill_context import resolve_skill_context
from .temp_paths import temporary_directory

# SKILL_WORKFLOWS defines skill workflows; this module owns the default.
SKILL_WORKFLOWS = PUBLIC_SKILL_WORKFLOWS
# HOSTS defines hosts; this module owns the default.
HOSTS = {"claude", "codex"}
# RECEIPT_SCHEMA_VERSION defines receipt schema version; this module owns the default.
RECEIPT_SCHEMA_VERSION = "1.1"
# RUNTIME_PACKAGE_SCHEMA_VERSION defines runtime package schema version; this module owns the default.
RUNTIME_PACKAGE_SCHEMA_VERSION = "2.0"
# RECEIPT_FIELDS defines receipt fields; this module owns the default.
RECEIPT_FIELDS = {
    "schema_version",
    "host",
    "host_version",
    "skill_id",
    "workflow_id",
    "installed_digest",
    "installation_manifest_digest",
    "repository_identity",
    "host_session_id",
    "discovered",
    "loaded",
    "invoked",
    "local_rules_resolved",
    "handoff_observed",
    "stop_boundary_observed",
}
# MAX_RECEIPT_BYTES bounds max receipt bytes in bytes; this module owns the limit.
MAX_RECEIPT_BYTES = 16 * 1024
# _DSET_CODE_COMMAND validates dset code command; this module owns the accepted syntax.
_DSET_CODE_COMMAND = re.compile(r"`dset(?=\s)")


class SkillDistributionError(ValueError):
    pass


@dataclass(frozen=True)
class InstallAction:
    host: str
    skill_id: str
    source: str
    destination: str
    source_digest: str
    installed_digest: str | None
    status: str
    runtime_destination: str
    launcher_command: str


@dataclass(frozen=True)
class InstallationProof:
    host: str
    skill_id: str
    destination: str
    digest: str
    copied_folder: bool
    discoverable: bool
    invocation_contract: bool


@dataclass(frozen=True)
class RuntimeInstallAction:
    host: str
    source: str
    destination: str
    source_digest: str
    installed_digest: str | None
    status: str
    wrapper_source: str
    skills_destination: str
    expected_manifest_digest: str


@dataclass(frozen=True)
class RuntimeInstallationProof:
    host: str
    destination: str
    digest: str
    copied_package: bool
    manifest_current: bool
    portable_launcher: str


def default_destination(
    host: str,
    *,
    environment: Mapping[str, str] | None = None,
    home: Path | None = None,
) -> Path:
    _require_host(host)
    base = Path.home() if home is None else home
    if host == "codex":
        return base / ".agents" / "skills"
    values = os.environ if environment is None else environment
    configured = values.get("CLAUDE_CONFIG_DIR")
    if configured:
        return Path(configured).expanduser() / "skills"
    return base / ".claude" / "skills"


def default_package_destination(
    host: str,
    *,
    environment: Mapping[str, str] | None = None,
    home: Path | None = None,
) -> Path:
    _require_host(host)
    values = os.environ if environment is None else environment
    variable = "CODEX_HOME" if host == "codex" else "CLAUDE_CONFIG_DIR"
    configured = values.get(variable)
    if configured:
        return Path(configured).expanduser() / "packages" / "dset"
    base = Path.home() if home is None else home
    return base / (".codex" if host == "codex" else ".claude") / "packages" / "dset"


def plan_runtime_install(
    source: Path,
    host: str,
    destination: Path | None = None,
    *,
    wrapper_source: Path | None = None,
    skills_destination: Path | None = None,
) -> RuntimeInstallAction:
    _require_host(host)
    source_root = _distribution_root(source)
    destination_root = (
        default_package_destination(host) if destination is None else destination
    )
    wrapper_root = _skills_root(
        source_root if wrapper_source is None else wrapper_source
    )
    skills_root = (
        _skills_destination_for_runtime(host, destination_root)
        if skills_destination is None
        else skills_destination
    )
    with temporary_directory(prefix="dset-runtime-plan-") as raw:
        rendered = Path(raw) / "dset"
        _render_runtime_package(
            source_root,
            host,
            rendered,
            runtime_destination=destination_root,
            wrapper_source=wrapper_root,
            skills_destination=skills_root,
        )
        source_digest = tree_digest(rendered)
        expected_manifest_digest = _file_digest(rendered / "manifest.json")
    installed_digest = (
        tree_digest(destination_root) if destination_root.is_dir() else None
    )
    if destination_root.exists() and not destination_root.is_dir():
        status = "conflict"
    elif installed_digest is None:
        status = "create"
    elif installed_digest == source_digest:
        status = "current"
    else:
        status = "conflict"
    return RuntimeInstallAction(
        host=host,
        source=str(source_root),
        destination=str(destination_root),
        source_digest=source_digest,
        installed_digest=installed_digest,
        status=status,
        wrapper_source=str(wrapper_root),
        skills_destination=str(skills_root),
        expected_manifest_digest=expected_manifest_digest,
    )


def apply_runtime_install(
    action: RuntimeInstallAction,
) -> RuntimeInstallationProof:
    _require_host(action.host)
    source = Path(action.source)
    destination = Path(action.destination)
    if action.status == "conflict":
        raise SkillDistributionError(
            f"runtime destination differs for {action.host}: {destination}"
        )
    _validate_runtime_source(action)
    if destination.exists():
        if not destination.is_dir() or tree_digest(destination) != action.source_digest:
            raise SkillDistributionError(
                f"runtime destination changed after planning: {destination}"
            )
        return verify_runtime_installation(
            action.host,
            destination,
            expected_manifest_digest=action.expected_manifest_digest,
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging_parent = Path(
        tempfile.mkdtemp(prefix=".dset-runtime-", dir=destination.parent)
    )
    staged = staging_parent / "dset"
    try:
        _render_runtime_package(
            source,
            action.host,
            staged,
            runtime_destination=destination,
            wrapper_source=Path(action.wrapper_source),
            skills_destination=Path(action.skills_destination),
        )
        if tree_digest(staged) != action.source_digest:
            raise SkillDistributionError("runtime source changed after planning")
        staged.replace(destination)
    finally:
        shutil.rmtree(staging_parent, ignore_errors=True)
    return verify_runtime_installation(
        action.host,
        destination,
        expected_manifest_digest=action.expected_manifest_digest,
    )


def verify_runtime_installation(
    host: str,
    destination: Path,
    *,
    expected_manifest_digest: str | None = None,
) -> RuntimeInstallationProof:
    _require_host(host)
    if destination.is_symlink() or not destination.is_dir():
        raise SkillDistributionError(f"runtime package is missing: {destination}")
    manifest, manifest_digest = _load_installation_manifest(host, destination)
    if (
        expected_manifest_digest is not None
        and manifest_digest != expected_manifest_digest
    ):
        raise SkillDistributionError("runtime manifest differs from install preview")
    installation = _manifest_mapping(manifest, "installation")
    expected_destination = str(destination.resolve())
    if installation.get("runtime_destination") != expected_destination:
        raise SkillDistributionError("runtime manifest destination mismatch")
    runtime = _manifest_mapping(manifest, "runtime_payload")
    expected_files = _manifest_file_digests(runtime)
    actual_files = _file_digests(destination, excluded={"manifest.json"})
    if actual_files != expected_files:
        raise SkillDistributionError("runtime payload differs from expected manifest")
    if runtime.get("sha256") != _digest_file_map(actual_files):
        raise SkillDistributionError("runtime payload digest mismatch")
    if manifest.get("source_digest") != _runtime_source_digest(destination):
        raise SkillDistributionError("runtime source identity mismatch")
    return RuntimeInstallationProof(
        host=host,
        destination=str(destination),
        digest=tree_digest(destination),
        copied_package=True,
        manifest_current=True,
        portable_launcher="dset.py",
    )


def plan_install(
    source: Path,
    host: str,
    destination: Path | None = None,
    package_destination: Path | None = None,
) -> list[InstallAction]:
    _require_host(host)
    skills_root = _skills_root(source)
    _validate_source_surface(skills_root)
    destination_root = default_destination(host) if destination is None else destination
    runtime_destination = (
        default_package_destination(host)
        if package_destination is None and destination is None
        else (
            destination_root.parent / "packages" / "dset"
            if package_destination is None
            else package_destination
        )
    )
    launcher_command = _launcher_command(runtime_destination)
    actions: list[InstallAction] = []
    for skill_id in sorted(SKILL_WORKFLOWS):
        source_skill = skills_root / skill_id
        _validate_skill_shape(source_skill, host)
        target = destination_root / skill_id
        source_digest = _rendered_skill_digest(source_skill, host, launcher_command)
        installed_digest = tree_digest(target) if target.is_dir() else None
        if target.exists() and not target.is_dir():
            status = "conflict"
        elif installed_digest is None:
            status = "create"
        elif installed_digest == source_digest:
            status = "current"
        else:
            status = "conflict"
        actions.append(
            InstallAction(
                host=host,
                skill_id=skill_id,
                source=str(source_skill),
                destination=str(target),
                source_digest=source_digest,
                installed_digest=installed_digest,
                status=status,
                runtime_destination=str(runtime_destination),
                launcher_command=launcher_command,
            )
        )
    return actions


def apply_install(actions: Sequence[InstallAction]) -> list[InstallationProof]:
    if not actions:
        return []
    hosts = {action.host for action in actions}
    destination_roots = {Path(action.destination).parent for action in actions}
    skill_ids = {action.skill_id for action in actions}
    if (
        len(hosts) != 1
        or len(destination_roots) != 1
        or skill_ids != set(SKILL_WORKFLOWS)
    ):
        raise SkillDistributionError("install plan is incomplete or mixed")
    for action in actions:
        source = Path(action.source)
        destination = Path(action.destination)
        _validate_skill_shape(source, action.host)
        if action.launcher_command != _launcher_command(
            Path(action.runtime_destination)
        ):
            raise SkillDistributionError(
                f"runtime launcher changed after planning: {action.skill_id}"
            )
        if (
            source.name != action.skill_id
            or _rendered_skill_digest(source, action.host, action.launcher_command)
            != action.source_digest
        ):
            raise SkillDistributionError(
                f"source changed after planning: {action.skill_id}"
            )
        if action.status == "conflict":
            raise SkillDistributionError(
                "destination differs for "
                f"{action.host}/{action.skill_id}: {destination}"
            )
        if destination.exists() and (
            not destination.is_dir() or tree_digest(destination) != action.source_digest
        ):
            raise SkillDistributionError(
                f"destination changed after planning: {destination}"
            )
    for action in actions:
        source = Path(action.source)
        destination = Path(action.destination)
        if destination.exists():
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        staging_parent = Path(
            tempfile.mkdtemp(prefix=f".{action.skill_id}-", dir=destination.parent)
        )
        staged = staging_parent / action.skill_id
        try:
            _render_skill_package(
                source,
                staged,
                action.host,
                action.launcher_command,
            )
            if tree_digest(staged) != action.source_digest:
                raise SkillDistributionError(
                    f"copied skill digest mismatch: {action.skill_id}"
                )
            staged.replace(destination)
        finally:
            shutil.rmtree(staging_parent, ignore_errors=True)
    first = actions[0]
    destination_root = Path(first.destination).parent
    proofs: list[InstallationProof] = []
    expected = {action.skill_id: action.source_digest for action in actions}
    for skill_id in sorted(SKILL_WORKFLOWS):
        skill = destination_root / skill_id
        digest = tree_digest(skill)
        if digest != expected[skill_id]:
            raise SkillDistributionError(
                f"installed skill differs from install preview: {skill_id}"
            )
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        proofs.append(
            InstallationProof(
                host=first.host,
                skill_id=skill_id,
                destination=str(skill),
                digest=digest,
                copied_folder=True,
                discoverable=True,
                invocation_contract=(SKILL_INVOCATION_MARKERS[skill_id] in text),
            )
        )
    return proofs


def verify_installation(
    host: str,
    destination: Path,
    package_destination: Path | None = None,
    *,
    expected_manifest_digest: str | None = None,
) -> list[InstallationProof]:
    _require_host(host)
    runtime_destination = (
        _package_destination_for_skills(host, destination)
        if package_destination is None
        else package_destination
    )
    verify_runtime_installation(
        host,
        runtime_destination,
        expected_manifest_digest=expected_manifest_digest,
    )
    manifest, manifest_digest = _load_installation_manifest(host, runtime_destination)
    if (
        expected_manifest_digest is not None
        and manifest_digest != expected_manifest_digest
    ):
        raise SkillDistributionError("skill manifest differs from install preview")
    installation = _manifest_mapping(manifest, "installation")
    if installation.get("skills_destination") != str(destination.resolve()):
        raise SkillDistributionError("skill manifest destination mismatch")
    wrappers = _manifest_mapping(manifest, "wrappers")
    if set(wrappers) != set(SKILL_WORKFLOWS):
        raise SkillDistributionError("skill manifest catalog mismatch")
    actual_catalog = {
        path.name
        for path in destination.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    if actual_catalog != set(SKILL_WORKFLOWS):
        raise SkillDistributionError("installed skill catalog differs from manifest")
    proofs: list[InstallationProof] = []
    for skill_id, _workflow in sorted(SKILL_WORKFLOWS.items()):
        skill = destination / skill_id
        _validate_skill_shape(skill, host)
        if skill.is_symlink():
            raise SkillDistributionError(f"installed skill is a symlink: {skill}")
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        digest = tree_digest(skill)
        if wrappers.get(skill_id) != digest:
            raise SkillDistributionError(
                f"installed skill differs from expected manifest: {skill_id}"
            )
        proofs.append(
            InstallationProof(
                host=host,
                skill_id=skill_id,
                destination=str(skill),
                digest=digest,
                copied_folder=True,
                discoverable=True,
                invocation_contract=(SKILL_INVOCATION_MARKERS[skill_id] in text),
            )
        )
    return proofs


def invocation_receipt_template(
    host: str,
    skill_id: str,
    destination: Path,
    package_destination: Path | None = None,
) -> dict[str, object]:
    runtime_destination = (
        _package_destination_for_skills(host, destination)
        if package_destination is None
        else package_destination
    )
    verify_runtime_installation(host, runtime_destination)
    proof = _proof_for_skill(
        verify_installation(host, destination, runtime_destination), skill_id
    )
    return {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "host": host,
        "host_version": "",
        "skill_id": skill_id,
        "workflow_id": SKILL_WORKFLOWS[skill_id],
        "installed_digest": proof.digest,
        "installation_manifest_digest": _file_digest(
            runtime_destination / "manifest.json"
        ),
        "repository_identity": "",
        "host_session_id": "",
        "discovered": False,
        "loaded": False,
        "invoked": False,
        "local_rules_resolved": False,
        "handoff_observed": False,
        "stop_boundary_observed": False,
    }


def verify_invocation_receipt(
    receipt: Mapping[str, object],
    host: str,
    destination: Path,
    package_destination: Path | None = None,
) -> dict[str, object]:
    try:
        serialized = json.dumps(receipt, separators=(",", ":")).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise SkillDistributionError(
            "invocation receipt is not JSON-compatible"
        ) from error
    if len(serialized) > MAX_RECEIPT_BYTES:
        raise SkillDistributionError("invocation receipt exceeds the size limit")
    if set(receipt) != RECEIPT_FIELDS:
        raise SkillDistributionError(
            "invocation receipt fields do not match the schema"
        )
    if receipt.get("schema_version") != RECEIPT_SCHEMA_VERSION:
        raise SkillDistributionError("unsupported invocation receipt schema")
    if receipt.get("host") != host:
        raise SkillDistributionError("invocation receipt host mismatch")
    raw_skill = receipt.get("skill_id")
    if not isinstance(raw_skill, str) or raw_skill not in SKILL_WORKFLOWS:
        raise SkillDistributionError("invocation receipt skill is invalid")
    if receipt.get("workflow_id") != SKILL_WORKFLOWS[raw_skill]:
        raise SkillDistributionError("invocation receipt workflow mismatch")
    runtime_destination = (
        _package_destination_for_skills(host, destination)
        if package_destination is None
        else package_destination
    )
    manifest_digest = _file_digest(runtime_destination / "manifest.json")
    if receipt.get("installation_manifest_digest") != manifest_digest:
        raise SkillDistributionError("invocation receipt manifest is stale")
    verify_runtime_installation(
        host,
        runtime_destination,
        expected_manifest_digest=manifest_digest,
    )
    proof = _proof_for_skill(
        verify_installation(
            host,
            destination,
            runtime_destination,
            expected_manifest_digest=manifest_digest,
        ),
        raw_skill,
    )
    if receipt.get("installed_digest") != proof.digest:
        raise SkillDistributionError("invocation receipt digest is stale")
    for field in ("host_version", "repository_identity", "host_session_id"):
        value = receipt.get(field)
        if not isinstance(value, str) or not value.strip() or len(value) > 256:
            raise SkillDistributionError(
                f"invocation receipt field is invalid: {field}"
            )
    for field in (
        "discovered",
        "loaded",
        "invoked",
        "local_rules_resolved",
        "handoff_observed",
        "stop_boundary_observed",
    ):
        if receipt.get(field) is not True:
            raise SkillDistributionError(
                f"invocation receipt proof is missing: {field}"
            )
    return {
        "status": "verified",
        "host": host,
        "skill_id": raw_skill,
        "workflow_id": SKILL_WORKFLOWS[raw_skill],
        "installed_digest": proof.digest,
        "installation_manifest_digest": manifest_digest,
        "repository_identity": receipt["repository_identity"],
        "host_session_id": receipt["host_session_id"],
    }


def tree_digest(root: Path) -> str:
    if root.is_symlink():
        raise SkillDistributionError(f"symlinks are not portable skill input: {root}")
    if not root.is_dir():
        raise SkillDistributionError(f"skill folder is missing: {root}")
    digest = hashlib.sha256()
    files: list[Path] = []
    for path in root.rglob("*"):
        relative_parts = path.relative_to(root).parts
        if "__pycache__" in relative_parts or path.suffix in {".pyc", ".pyo"}:
            continue
        if path.is_symlink():
            raise SkillDistributionError(
                f"symlinks are not portable skill input: {path}"
            )
        if path.is_file():
            files.append(path)
    for path in sorted(files, key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        content = path.read_bytes()
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def _file_digest(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise SkillDistributionError(f"installation file is missing: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _file_digests(
    root: Path,
    *,
    excluded: set[str] | None = None,
) -> dict[str, str]:
    if root.is_symlink() or not root.is_dir():
        raise SkillDistributionError(f"installation folder is missing: {root}")
    ignored = excluded or set()
    files: dict[str, str] = {}
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        relative_parts = path.relative_to(root).parts
        if (
            relative in ignored
            or "__pycache__" in relative_parts
            or path.suffix in {".pyc", ".pyo"}
        ):
            continue
        if path.is_symlink():
            raise SkillDistributionError(
                f"symlinks are not portable installation input: {path}"
            )
        if path.is_file():
            files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(sorted(files.items()))


def _digest_file_map(files: Mapping[str, str]) -> str:
    encoded = json.dumps(
        dict(sorted(files.items())),
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _canonical_manifest(manifest: Mapping[str, object]) -> bytes:
    return (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _load_installation_manifest(
    host: str,
    runtime_destination: Path,
) -> tuple[dict[str, object], str]:
    path = runtime_destination / "manifest.json"
    if path.is_symlink() or not path.is_file():
        raise SkillDistributionError(f"runtime manifest is missing: {path}")
    raw = path.read_bytes()
    try:
        decoded = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SkillDistributionError(f"runtime manifest is invalid: {path}") from error
    if not isinstance(decoded, dict) or raw != _canonical_manifest(decoded):
        raise SkillDistributionError("runtime manifest is not canonical")
    manifest = dict(decoded)
    required = {
        "schema_version",
        "package",
        "version",
        "host",
        "entrypoint",
        "source_digest",
        "installation",
        "runtime_payload",
        "wrappers",
    }
    if set(manifest) != required:
        raise SkillDistributionError("runtime manifest fields do not match schema")
    expected = {
        "schema_version": RUNTIME_PACKAGE_SCHEMA_VERSION,
        "package": "dset",
        "version": __version__,
        "host": host,
        "entrypoint": "dset.py",
    }
    if any(manifest.get(key) != value for key, value in expected.items()):
        raise SkillDistributionError("runtime manifest identity is stale")
    if not _is_sha256(manifest.get("source_digest")):
        raise SkillDistributionError("runtime manifest source digest is invalid")
    installation = _manifest_mapping(manifest, "installation")
    if set(installation) != {"runtime_destination", "skills_destination"} or not all(
        isinstance(installation.get(key), str) and installation.get(key)
        for key in ("runtime_destination", "skills_destination")
    ):
        raise SkillDistributionError("runtime manifest destinations are invalid")
    runtime = _manifest_mapping(manifest, "runtime_payload")
    if set(runtime) != {"sha256", "files"} or not _is_sha256(runtime.get("sha256")):
        raise SkillDistributionError("runtime payload manifest is invalid")
    _manifest_file_digests(runtime)
    wrappers = _manifest_mapping(manifest, "wrappers")
    if set(wrappers) != set(SKILL_WORKFLOWS) or not all(
        _is_sha256(value) for value in wrappers.values()
    ):
        raise SkillDistributionError("wrapper manifest is invalid")
    return manifest, hashlib.sha256(raw).hexdigest()


def _manifest_mapping(manifest: Mapping[str, object], key: str) -> dict[str, object]:
    value = manifest.get(key)
    if not isinstance(value, dict):
        raise SkillDistributionError(f"runtime manifest field is invalid: {key}")
    return dict(value)


def _manifest_file_digests(runtime: Mapping[str, object]) -> dict[str, str]:
    raw = runtime.get("files")
    if not isinstance(raw, dict):
        raise SkillDistributionError("runtime payload file manifest is invalid")
    files: dict[str, str] = {}
    for relative, digest in raw.items():
        if (
            not isinstance(relative, str)
            or not relative
            or Path(relative).is_absolute()
            or "\\" in relative
            or any(part in {"", ".", ".."} for part in Path(relative).parts)
            or not _is_sha256(digest)
        ):
            raise SkillDistributionError("runtime payload file identity is invalid")
        files[relative] = str(digest)
    return dict(sorted(files.items()))


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _skills_destination_for_runtime(host: str, destination: Path) -> Path:
    if destination.resolve() == default_package_destination(host).resolve():
        return default_destination(host)
    return destination.parent.parent / "skills"


def _package_destination_for_skills(host: str, destination: Path) -> Path:
    if destination.resolve() == default_destination(host).resolve():
        return default_package_destination(host)
    return destination.parent / "packages" / "dset"


def _skills_root(source: Path) -> Path:
    candidate = source / "skills"
    return candidate if candidate.is_dir() else source


def _distribution_root(source: Path) -> Path:
    candidate = source.resolve()
    if (candidate / "dset_toolchain" / "__init__.py").is_file():
        return candidate
    if candidate.name == "skills":
        sibling = candidate.parent
        if (sibling / "dset_toolchain" / "__init__.py").is_file():
            return sibling
    raise SkillDistributionError(
        f"DSET runtime source is missing beside the skills catalog: {source}"
    )


def _runtime_source_digest(source: Path) -> str:
    package = source / "dset_toolchain"
    digest = hashlib.sha256()
    files = sorted(
        (
            path
            for path in package.iterdir()
            if path.is_file()
            and (path.suffix == ".py" or path.name == "bootstrap_bundle.json")
        ),
        key=lambda item: item.name,
    )
    if not files:
        raise SkillDistributionError(f"DSET runtime source is empty: {package}")
    for path in files:
        relative = path.relative_to(source).as_posix().encode("utf-8")
        content = path.read_bytes()
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def _launcher_command(
    runtime_destination: PurePath,
    *,
    platform_name: str | None = None,
    executable: str | None = None,
) -> str:
    launcher = runtime_destination / "dset.py"
    interpreter = sys.executable if executable is None else executable
    platform = os.name if platform_name is None else platform_name
    if platform == "nt":
        return "& " + " ".join(
            _powershell_literal(argument) for argument in (interpreter, str(launcher))
        )
    if platform == "posix":
        return shlex.join([interpreter, str(launcher)])
    raise SkillDistributionError(f"unsupported launcher platform: {platform}")


def _powershell_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _rendered_skill_digest(source: Path, host: str, launcher_command: str) -> str:
    with temporary_directory(prefix="dset-skill-render-") as raw:
        rendered = Path(raw) / source.name
        _render_skill_package(source, rendered, host, launcher_command)
        return tree_digest(rendered)


def _render_skill_package(
    source: Path,
    destination: Path,
    host: str,
    launcher_command: str,
) -> None:
    _validate_skill_shape(source, host)
    shutil.copytree(source, destination, copy_function=shutil.copy2)
    skill_file = destination / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    if text.count("`dset skills context") != 1:
        raise SkillDistributionError(
            f"skill context launcher is not uniquely renderable: {source.name}"
        )
    command_count = len(_DSET_CODE_COMMAND.findall(text))
    if command_count == 0:
        raise SkillDistributionError(
            f"skill has no renderable DSET commands: {source.name}"
        )
    text = _DSET_CODE_COMMAND.sub(lambda _match: f"`{launcher_command}", text)
    if _DSET_CODE_COMMAND.search(text):
        raise SkillDistributionError(
            f"skill retains an ambient DSET command: {source.name}"
        )
    skill_file.write_text(text, encoding="utf-8")


def _render_runtime_package(
    source: Path,
    host: str,
    destination: Path,
    *,
    runtime_destination: Path,
    wrapper_source: Path,
    skills_destination: Path,
) -> None:
    _require_host(host)
    source_root = _distribution_root(source)
    package_source = source_root / "dset_toolchain"
    destination.mkdir(parents=True)
    shutil.copytree(
        package_source,
        destination / "dset_toolchain",
        copy_function=shutil.copy2,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )
    launcher = (
        "from dset_toolchain.cli import main\n\n"
        'if __name__ == "__main__":\n'
        "    raise SystemExit(main())\n"
    )
    (destination / "dset.py").write_text(launcher, encoding="utf-8")
    (destination / "dset").write_text(
        "#!/usr/bin/env python3\n" + launcher,
        encoding="utf-8",
    )
    (destination / "dset").chmod(0o755)
    (destination / "dset.cmd").write_text(
        '@echo off\r\npy -3 "%~dp0dset.py" %*\r\n',
        encoding="utf-8",
    )
    runtime_files = _file_digests(destination)
    wrappers = {
        skill_id: _rendered_skill_digest(
            wrapper_source / skill_id,
            host,
            _launcher_command(runtime_destination),
        )
        for skill_id in sorted(SKILL_WORKFLOWS)
    }
    manifest: dict[str, object] = {
        "schema_version": RUNTIME_PACKAGE_SCHEMA_VERSION,
        "package": "dset",
        "version": __version__,
        "host": host,
        "entrypoint": "dset.py",
        "source_digest": _runtime_source_digest(source_root),
        "installation": {
            "runtime_destination": str(runtime_destination.resolve()),
            "skills_destination": str(skills_destination.resolve()),
        },
        "runtime_payload": {
            "sha256": _digest_file_map(runtime_files),
            "files": runtime_files,
        },
        "wrappers": wrappers,
    }
    (destination / "manifest.json").write_bytes(_canonical_manifest(manifest))


def _validate_runtime_source(action: RuntimeInstallAction) -> None:
    with temporary_directory(prefix="dset-runtime-validate-") as raw:
        rendered = Path(raw) / "dset"
        _render_runtime_package(
            Path(action.source),
            action.host,
            rendered,
            runtime_destination=Path(action.destination),
            wrapper_source=Path(action.wrapper_source),
            skills_destination=Path(action.skills_destination),
        )
        if tree_digest(rendered) != action.source_digest:
            raise SkillDistributionError("runtime source changed after planning")
        if _file_digest(rendered / "manifest.json") != action.expected_manifest_digest:
            raise SkillDistributionError("runtime manifest changed after planning")


def _expected_manifest(action: RuntimeInstallAction) -> dict[str, object]:
    with temporary_directory(prefix="dset-runtime-manifest-") as raw:
        rendered = Path(raw) / "dset"
        _render_runtime_package(
            Path(action.source),
            action.host,
            rendered,
            runtime_destination=Path(action.destination),
            wrapper_source=Path(action.wrapper_source),
            skills_destination=Path(action.skills_destination),
        )
        manifest, digest = _load_installation_manifest(action.host, rendered)
        if digest != action.expected_manifest_digest:
            raise SkillDistributionError("runtime manifest changed after planning")
        return manifest


def _validate_source_surface(skills_root: Path) -> None:
    if not skills_root.is_dir():
        raise SkillDistributionError(f"skills source is missing: {skills_root}")
    actual = {
        path.parent.name for path in skills_root.glob("*/SKILL.md") if path.is_file()
    }
    expected = set(SKILL_WORKFLOWS)
    if actual != expected:
        raise SkillDistributionError(
            "source must contain exactly the public DSET skill catalog: "
            f"expected={sorted(expected)}, actual={sorted(actual)}"
        )


def _validate_skill_shape(skill: Path, host: str) -> None:
    _require_host(host)
    skill_file = skill / "SKILL.md"
    if not skill_file.is_file():
        raise SkillDistributionError(f"SKILL.md is missing: {skill_file}")
    text = skill_file.read_text(encoding="utf-8")
    name = skill.name
    if f"\nname: {name}\n" not in text or "\ndescription: " not in text:
        raise SkillDistributionError(f"skill frontmatter is invalid: {skill_file}")
    marker = SKILL_INVOCATION_MARKERS.get(name)
    if marker is None or marker not in text:
        raise SkillDistributionError(f"skill invocation contract is invalid: {name}")
    if host == "codex":
        metadata = skill / "agents" / "openai.yaml"
        if not metadata.is_file():
            raise SkillDistributionError(f"Codex metadata is missing: {metadata}")
        if f"Use ${name}" not in metadata.read_text(encoding="utf-8"):
            raise SkillDistributionError(f"Codex default prompt is invalid: {name}")


def _proof_for_skill(
    proofs: Sequence[InstallationProof], skill_id: str
) -> InstallationProof:
    if skill_id not in SKILL_WORKFLOWS:
        raise SkillDistributionError(f"unknown public skill: {skill_id}")
    return next(proof for proof in proofs if proof.skill_id == skill_id)


def _require_host(host: str) -> None:
    if host not in HOSTS:
        raise SkillDistributionError(f"unsupported skill host: {host}")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install and verify DSET skills")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("install", "verify", "receipt-template", "verify-invocation"):
        item = subparsers.add_parser(command)
        item.add_argument("--host", choices=sorted(HOSTS), required=True)
        item.add_argument("--destination", type=Path)
        if command in {
            "install",
            "verify",
            "receipt-template",
            "verify-invocation",
        }:
            item.add_argument("--package-destination", type=Path)
        if command == "install":
            item.add_argument("--source", type=Path)
            item.add_argument("--apply", action="store_true")
        if command in {"receipt-template", "verify-invocation"}:
            item.add_argument("--skill", choices=sorted(SKILL_WORKFLOWS), required=True)
        if command == "verify-invocation":
            item.add_argument("--receipt", type=Path, required=True)
    context = subparsers.add_parser("context")
    context.add_argument("--skill", choices=sorted(SKILL_WORKFLOWS), required=True)
    context.add_argument("--target", type=Path, required=True)
    context.add_argument("--objective", default="Resolve the governed DSET context")
    context.add_argument("--session-id")
    context.add_argument("--llm-session-id", action="append", default=[])
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "context":
            context_result = resolve_skill_context(
                Path(arguments.target),
                skill_id=str(arguments.skill),
                objective=str(arguments.objective),
                session_id=arguments.session_id,
                llm_session_ids=arguments.llm_session_id,
            )
            print(json.dumps(context_result, indent=2, sort_keys=True))
            return 0
        host = str(arguments.host)
        destination = (
            default_destination(host)
            if arguments.destination is None
            else Path(arguments.destination)
        )
        requested_package_destination = getattr(arguments, "package_destination", None)
        package_destination = (
            default_package_destination(host)
            if requested_package_destination is None and arguments.destination is None
            else (
                destination.parent / "packages" / "dset"
                if requested_package_destination is None
                else Path(requested_package_destination)
            )
        )
        result: Any
        actions: list[InstallAction] = []
        runtime_action: RuntimeInstallAction | None = None
        if arguments.command == "install":
            source = Path(arguments.source) if arguments.source is not None else None
            if source is not None:
                actions = plan_install(
                    source,
                    host,
                    destination,
                    package_destination,
                )
                runtime_action = plan_runtime_install(
                    source,
                    host,
                    package_destination,
                    wrapper_source=source,
                    skills_destination=destination,
                )
                result = _execute_install(
                    actions, runtime_action, apply=arguments.apply
                )
            else:
                with distribution_source() as (selected_source, _identity):
                    actions = plan_install(
                        selected_source,
                        host,
                        destination,
                        package_destination,
                    )
                    runtime_action = plan_runtime_install(
                        Path(__file__).resolve().parents[1],
                        host,
                        package_destination,
                        wrapper_source=selected_source,
                        skills_destination=destination,
                    )
                    result = _execute_install(
                        actions, runtime_action, apply=arguments.apply
                    )
        elif arguments.command == "verify":
            result = {
                "proofs": [
                    asdict(item)
                    for item in verify_installation(
                        host, destination, package_destination
                    )
                ],
                "runtime_proof": asdict(
                    verify_runtime_installation(host, package_destination)
                ),
            }
        elif arguments.command == "receipt-template":
            result = invocation_receipt_template(
                host,
                str(arguments.skill),
                destination,
                package_destination,
            )
        else:
            receipt_path = Path(arguments.receipt)
            if receipt_path.stat().st_size > MAX_RECEIPT_BYTES:
                raise SkillDistributionError(
                    "invocation receipt exceeds the size limit"
                )
            raw = json.loads(receipt_path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                raise SkillDistributionError("invocation receipt must be a JSON object")
            if raw.get("skill_id") != arguments.skill:
                raise SkillDistributionError("receipt and --skill do not match")
            result = verify_invocation_receipt(
                raw,
                host,
                destination,
                package_destination,
            )
    except (OSError, json.JSONDecodeError, SkillDistributionError) as error:
        print(json.dumps({"status": "error", "message": str(error)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    if arguments.command == "install" and not arguments.apply:
        has_conflict = any(item.status == "conflict" for item in actions)
        if runtime_action is not None and runtime_action.status == "conflict":
            has_conflict = True
        return 2 if has_conflict else 0
    return 0


def _execute_install(
    actions: Sequence[InstallAction],
    runtime_action: RuntimeInstallAction,
    *,
    apply: bool,
) -> dict[str, object]:
    expected_manifest = _expected_manifest(runtime_action)
    manifest_wrappers = _manifest_mapping(expected_manifest, "wrappers")
    action_wrappers = {action.skill_id: action.source_digest for action in actions}
    if manifest_wrappers != action_wrappers:
        raise SkillDistributionError(
            "skill and runtime plans have different wrapper identities"
        )
    installation = _manifest_mapping(expected_manifest, "installation")
    destinations = {
        str(Path(action.destination).parent.resolve()) for action in actions
    }
    if destinations != {installation.get("skills_destination")}:
        raise SkillDistributionError(
            "skill and runtime plans have different destinations"
        )
    if apply:
        if any(action.status == "conflict" for action in actions):
            raise SkillDistributionError("skill destination conflict blocks install")
        if runtime_action.status == "conflict":
            raise SkillDistributionError("runtime destination conflict blocks install")
        _validate_runtime_source(runtime_action)
        initially_absent = {
            Path(action.destination): action.source_digest
            for action in actions
            if not Path(action.destination).exists()
        }
        runtime_path = Path(runtime_action.destination)
        if not runtime_path.exists():
            initially_absent[runtime_path] = runtime_action.source_digest
        initially_absent_parents = {
            destination.parent
            for destination in initially_absent
            if not destination.parent.exists()
        }
        try:
            apply_install(actions)
            runtime_proof = apply_runtime_install(runtime_action)
            proofs = verify_installation(
                runtime_action.host,
                Path(next(iter(actions)).destination).parent,
                Path(runtime_action.destination),
                expected_manifest_digest=runtime_action.expected_manifest_digest,
            )
        except Exception as error:
            rollback_failures = _rollback_created_install(
                initially_absent, initially_absent_parents
            )
            if rollback_failures:
                raise SkillDistributionError(
                    "install failed and rollback was incomplete: "
                    + ", ".join(rollback_failures)
                ) from error
            raise
        return {
            "applied": True,
            "proofs": [asdict(item) for item in proofs],
            "runtime_proof": asdict(runtime_proof),
            "expected_manifest": expected_manifest,
            "expected_manifest_digest": runtime_action.expected_manifest_digest,
        }
    return {
        "applied": False,
        "actions": [asdict(item) for item in actions],
        "runtime_action": asdict(runtime_action),
        "expected_manifest": expected_manifest,
        "expected_manifest_digest": runtime_action.expected_manifest_digest,
    }


def _rollback_created_install(
    created: Mapping[Path, str], created_parents: set[Path]
) -> list[str]:
    failures: list[str] = []
    for destination, expected_digest in reversed(tuple(created.items())):
        if not destination.exists():
            continue
        try:
            if not destination.is_dir() or tree_digest(destination) != expected_digest:
                failures.append(str(destination))
                continue
            shutil.rmtree(destination)
        except OSError:
            failures.append(str(destination))
    ordered_parents = sorted(
        created_parents, key=lambda item: len(item.parts), reverse=True
    )
    for parent in ordered_parents:
        try:
            parent.rmdir()
        except FileNotFoundError:
            continue
        except OSError:
            if parent.is_dir() and not any(parent.iterdir()):
                failures.append(str(parent))
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
