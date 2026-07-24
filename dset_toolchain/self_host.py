"""Provide DSET self host behavior."""

from __future__ import annotations

import hashlib
import io
import os
import subprocess
import sys
import tarfile
from pathlib import Path
from typing import Any

from .adopter import create_adopter
from .errors import DsetCommandError
from .governance import refresh_customization, resolve_workflow, validate_governance
from .layout import discover_layout
from .project_data import project_section


def run_self_host(
    root: Path,
    work_root: Path,
    *,
    released_ref: str | None = None,
    candidate_command: list[str] | None = None,
) -> dict[str, Any]:
    """Run the bounded released, candidate, adopter, and customization proof."""
    root = root.resolve()
    work_root = work_root.resolve()
    released = _released_contract(root)
    reference = released_ref or str(released.get("commit", ""))
    adopter = work_root / "temporary-adopter"
    released_status, released_diagnostic = _validate_released(
        root, work_root, reference, released
    )
    _validate_candidate_and_adopter(root, adopter, candidate_command)
    adopter_registry = project_section(adopter, "governance_registry")
    workflow_ids = tuple(
        str(item["workflow"])
        for item in adopter_registry.get("wrappers", [])
        if isinstance(item, dict) and isinstance(item.get("workflow"), str)
    )
    resolved, wrapper_before = _resolve_workflows(adopter, workflow_ids)
    rule_path = _customize_adopter(root, adopter, resolved["domain-clarification"])
    customized, wrappers_unchanged = _resolve_customized(
        adopter, workflow_ids, wrapper_before, rule_path
    )
    return {
        "released_validator": released_status,
        "released_validator_diagnostic": released_diagnostic,
        "candidate_repository": "pass",
        "temporary_adopter": "pass",
        "customization": customized["domain-clarification"]["customization"],
        "workflows_resolved": list(workflow_ids),
        "wrappers_unchanged": wrappers_unchanged,
        "wrapper_unchanged": wrappers_unchanged,
        "recursion_stopped": not discover_layout(adopter).version_path.exists(),
        "released_ref": reference,
        "adopter": adopter.as_posix(),
    }


def _released_contract(root: Path) -> dict[str, Any]:
    """Load the released-validator contract after checking its carrier."""
    version_path = discover_layout(root).version_path
    if not version_path.is_file():
        raise DsetCommandError(
            "DSET-E140", version_path, "self-host version contract is missing"
        )
    version = project_section(root, "version_registry")
    released = version.get("released_validator", {})
    return released if isinstance(released, dict) else {}


def _validate_released(
    root: Path, work_root: Path, reference: str, released: dict[str, Any]
) -> tuple[str, str | None]:
    """Run the released validator and classify an allowed bootstrap transition."""
    extracted = work_root / "released-validator"
    _extract_released(root, reference, extracted)
    try:
        _run_validator(
            [sys.executable, "-m", "dset_toolchain", "check", str(root)],
            extracted,
            "DSET-E140",
            "released validator rejected the candidate repository",
        )
    except DsetCommandError as error:
        if released.get("assurance") != "bootstrap-transition":
            raise
        return "bootstrap-transition", error.message[:2000]
    return "pass", None


def _validate_candidate_and_adopter(
    root: Path, adopter: Path, candidate_command: list[str] | None
) -> None:
    """Validate the candidate repository and a freshly initialized adopter."""
    command = candidate_command or [
        sys.executable,
        "-m",
        "dset_toolchain",
        "check",
        str(root),
    ]
    _run_validator(
        command,
        root,
        "DSET-E141",
        "candidate validator rejected the framework repository",
    )
    create_adopter(root, adopter)
    _run_validator(
        [sys.executable, "-m", "dset_toolchain", "check", str(adopter)],
        root,
        "DSET-E141",
        "candidate validator rejected the temporary adopter",
    )


def _resolve_workflows(
    adopter: Path, workflow_ids: tuple[str, ...]
) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    """Resolve every wrapper workflow and snapshot wrapper digests."""
    resolved_workflows: dict[str, dict[str, Any]] = {}
    wrapper_before: dict[str, str] = {}
    for workflow_id in workflow_ids:
        resolved, diagnostics = resolve_workflow(adopter, workflow_id)
        if diagnostics or resolved is None:
            raise DsetCommandError(
                "DSET-E141",
                discover_layout(adopter).governance_path,
                f"temporary adopter workflow did not resolve: {workflow_id}",
            )
        resolved_workflows[workflow_id] = resolved
        wrapper_before[workflow_id] = _sha256(
            _wrapper_path(adopter, resolved["wrapper"])
        )
    return resolved_workflows, wrapper_before


def _customize_adopter(root: Path, adopter: Path, resolved: dict[str, Any]) -> Path:
    """Apply and validate one bounded project-local governance customization."""
    rule = next(
        item for item in resolved["rules"] if item["id"] == "DSET-RULE-DOMAIN-SPEC"
    )
    path = _rule_path(adopter, rule)
    path.write_text(
        path.read_text(encoding="utf-8")
        + "\n<!-- bounded self-host customization -->\n",
        encoding="utf-8",
    )
    if "DSET-E139" not in {item.code for item in validate_governance(adopter)}:
        raise DsetCommandError(
            "DSET-E141", path, "local customization was not detected"
        )
    refresh_customization(adopter)
    _run_validator(
        [sys.executable, "-m", "dset_toolchain", "check", str(adopter)],
        root,
        "DSET-E141",
        "customized temporary adopter did not validate",
    )
    return path


def _resolve_customized(
    adopter: Path,
    workflow_ids: tuple[str, ...],
    wrapper_before: dict[str, str],
    rule_path: Path,
) -> tuple[dict[str, dict[str, Any]], bool]:
    """Resolve customized workflows and prove thin wrappers stayed unchanged."""
    workflows: dict[str, dict[str, Any]] = {}
    unchanged = True
    for workflow_id in workflow_ids:
        resolved, diagnostics = resolve_workflow(adopter, workflow_id)
        if diagnostics or resolved is None:
            raise DsetCommandError(
                "DSET-E141",
                rule_path,
                f"customized workflow did not resolve: {workflow_id}",
            )
        workflows[workflow_id] = resolved
        unchanged = (
            unchanged
            and _sha256(_wrapper_path(adopter, resolved["wrapper"]))
            == wrapper_before[workflow_id]
        )
    return workflows, unchanged


def _wrapper_path(root: Path, wrapper: Any) -> Path:
    if not isinstance(wrapper, dict) or not isinstance(wrapper.get("skill"), str):
        raise ValueError("resolved workflow has no skill identity")
    return root / "skills" / str(wrapper["skill"]) / "SKILL.md"


def _rule_path(root: Path, rule: dict[str, Any]) -> Path:
    document = rule.get("document")
    if not isinstance(document, str):
        raise ValueError("resolved rule has no document identity")
    from .identity import find_unique_name

    return find_unique_name(root, document)


def _extract_released(root: Path, reference: str, destination: Path) -> None:
    """Handle released using the declared repository contract."""
    result = subprocess.run(
        ["git", "archive", "--format=tar", reference, "dset_toolchain"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise DsetCommandError(
            "DSET-E140",
            discover_layout(root).version_path,
            f"released validator cannot be extracted: {message}",
        )
    destination.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(result.stdout), mode="r:") as archive:
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            try:
                target.relative_to(destination)
            except ValueError as error:
                raise DsetCommandError(
                    "DSET-E140", destination, "released archive escapes destination"
                ) from error
        archive.extractall(destination)


def _run_validator(
    command: list[str],
    cwd: Path,
    code: str,
    failure: str,
) -> int:
    """Run validator using the declared repository contract."""
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(cwd)
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
    except OSError as error:
        raise DsetCommandError(code, cwd, f"{failure}: {error}") from error
    if result.returncode:
        output = result.stdout.strip()
        raise DsetCommandError(code, cwd, f"{failure}: {output}")
    return result.returncode


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
