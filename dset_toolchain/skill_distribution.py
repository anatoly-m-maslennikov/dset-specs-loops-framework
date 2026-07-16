from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .bootstrap import distribution_source

SKILL_WORKFLOWS = {
    "dset": "lifecycle-orchestration",
    "dset-clarify": "domain-clarification",
    "dset-diagnose": "diagnosis",
    "dset-prototype": "prototyping",
    "dset-release": "release",
}
HOSTS = {"claude", "codex"}
RECEIPT_SCHEMA_VERSION = "1.0"
RECEIPT_FIELDS = {
    "schema_version",
    "host",
    "host_version",
    "skill_id",
    "workflow_id",
    "installed_digest",
    "repository_identity",
    "host_session_id",
    "discovered",
    "loaded",
    "invoked",
    "local_rules_resolved",
    "handoff_observed",
    "stop_boundary_observed",
}
MAX_RECEIPT_BYTES = 16 * 1024


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


@dataclass(frozen=True)
class InstallationProof:
    host: str
    skill_id: str
    destination: str
    digest: str
    copied_folder: bool
    discoverable: bool
    invocation_contract: bool


def default_destination(
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
        return Path(configured).expanduser() / "skills"
    base = Path.home() if home is None else home
    return base / (".codex" if host == "codex" else ".claude") / "skills"


def plan_install(
    source: Path,
    host: str,
    destination: Path | None = None,
) -> list[InstallAction]:
    _require_host(host)
    skills_root = _skills_root(source)
    _validate_source_surface(skills_root)
    destination_root = default_destination(host) if destination is None else destination
    actions: list[InstallAction] = []
    for skill_id in sorted(SKILL_WORKFLOWS):
        source_skill = skills_root / skill_id
        _validate_skill_shape(source_skill, host)
        target = destination_root / skill_id
        source_digest = tree_digest(source_skill)
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
        if (
            source.name != action.skill_id
            or tree_digest(source) != action.source_digest
        ):
            raise SkillDistributionError(
                f"source changed after planning: {action.skill_id}"
            )
        if action.status == "conflict":
            raise SkillDistributionError(
                "destination differs for "
                f"{action.host}/{action.skill_id}: {destination}"
            )
        if destination.exists():
            if (
                not destination.is_dir()
                or tree_digest(destination) != action.source_digest
            ):
                raise SkillDistributionError(
                    f"destination changed after planning: {destination}"
                )
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        staging_parent = Path(
            tempfile.mkdtemp(prefix=f".{action.skill_id}-", dir=destination.parent)
        )
        staged = staging_parent / action.skill_id
        try:
            shutil.copytree(source, staged, copy_function=shutil.copy2)
            if tree_digest(staged) != action.source_digest:
                raise SkillDistributionError(
                    f"copied skill digest mismatch: {action.skill_id}"
                )
            staged.replace(destination)
        finally:
            shutil.rmtree(staging_parent, ignore_errors=True)
    first = actions[0]
    destination_root = Path(first.destination).parent
    return verify_installation(first.host, destination_root)


def verify_installation(host: str, destination: Path) -> list[InstallationProof]:
    _require_host(host)
    proofs: list[InstallationProof] = []
    for skill_id, workflow in sorted(SKILL_WORKFLOWS.items()):
        skill = destination / skill_id
        _validate_skill_shape(skill, host)
        if skill.is_symlink():
            raise SkillDistributionError(f"installed skill is a symlink: {skill}")
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        proofs.append(
            InstallationProof(
                host=host,
                skill_id=skill_id,
                destination=str(skill),
                digest=tree_digest(skill),
                copied_folder=True,
                discoverable=True,
                invocation_contract=(f"rules resolve {workflow} --format json" in text),
            )
        )
    return proofs


def invocation_receipt_template(
    host: str,
    skill_id: str,
    destination: Path,
) -> dict[str, object]:
    proof = _proof_for_skill(verify_installation(host, destination), skill_id)
    return {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "host": host,
        "host_version": "",
        "skill_id": skill_id,
        "workflow_id": SKILL_WORKFLOWS[skill_id],
        "installed_digest": proof.digest,
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
    proof = _proof_for_skill(verify_installation(host, destination), raw_skill)
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


def _skills_root(source: Path) -> Path:
    candidate = source / "skills"
    return candidate if candidate.is_dir() else source


def _validate_source_surface(skills_root: Path) -> None:
    if not skills_root.is_dir():
        raise SkillDistributionError(f"skills source is missing: {skills_root}")
    actual = {
        path.parent.name for path in skills_root.glob("*/SKILL.md") if path.is_file()
    }
    expected = set(SKILL_WORKFLOWS)
    if actual != expected:
        raise SkillDistributionError(
            "source must contain exactly the five public DSET skills: "
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
    workflow = SKILL_WORKFLOWS.get(name)
    if workflow is None or f"rules resolve {workflow} --format json" not in text:
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
        if command == "install":
            item.add_argument("--source", type=Path)
            item.add_argument("--apply", action="store_true")
        if command in {"receipt-template", "verify-invocation"}:
            item.add_argument("--skill", choices=sorted(SKILL_WORKFLOWS), required=True)
        if command == "verify-invocation":
            item.add_argument("--receipt", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    host = str(arguments.host)
    destination = (
        default_destination(host)
        if arguments.destination is None
        else Path(arguments.destination)
    )
    try:
        result: Any
        actions: list[InstallAction] = []
        if arguments.command == "install":
            source = Path(arguments.source) if arguments.source is not None else None
            if source is not None:
                actions = plan_install(source, host, destination)
                result = _execute_install(actions, apply=arguments.apply)
            else:
                with distribution_source() as (selected_source, _identity):
                    actions = plan_install(selected_source, host, destination)
                    result = _execute_install(actions, apply=arguments.apply)
        elif arguments.command == "verify":
            result = {
                "proofs": [
                    asdict(item) for item in verify_installation(host, destination)
                ]
            }
        elif arguments.command == "receipt-template":
            result = invocation_receipt_template(
                host, str(arguments.skill), destination
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
            result = verify_invocation_receipt(raw, host, destination)
    except (OSError, json.JSONDecodeError, SkillDistributionError) as error:
        print(json.dumps({"status": "error", "message": str(error)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    if arguments.command == "install" and not arguments.apply:
        return 2 if any(item.status == "conflict" for item in actions) else 0
    return 0


def _execute_install(
    actions: Sequence[InstallAction], *, apply: bool
) -> dict[str, object]:
    if apply:
        return {
            "applied": True,
            "proofs": [asdict(item) for item in apply_install(actions)],
        }
    return {
        "applied": False,
        "actions": [asdict(item) for item in actions],
    }


if __name__ == "__main__":
    raise SystemExit(main())
