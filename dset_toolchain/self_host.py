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
from .yaml_subset import load


def run_self_host(
    root: Path,
    work_root: Path,
    *,
    released_ref: str | None = None,
    candidate_command: list[str] | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    work_root = work_root.resolve()
    version_path = discover_layout(root).version_path
    if not version_path.is_file():
        raise DsetCommandError(
            "DSET-E140", version_path, "self-host version contract is missing"
        )
    version = project_section(root, "version_registry")
    released = version.get("released_validator", {})
    reference = released_ref or str(released.get("commit", ""))
    extracted = work_root / "released-validator"
    adopter = work_root / "temporary-adopter"
    _extract_released(root, reference, extracted)
    released_status = "pass"
    released_diagnostic: str | None = None
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
        released_status = "bootstrap-transition"
        released_diagnostic = error.message[:2000]
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
    adopter_registry = project_section(adopter, "governance_registry")
    workflow_ids = tuple(
        str(item["workflow"])
        for item in adopter_registry.get("wrappers", [])
        if isinstance(item, dict) and isinstance(item.get("workflow"), str)
    )
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
        wrapper_path = adopter / str(resolved["wrapper"]["path"])
        wrapper_before[workflow_id] = _sha256(wrapper_path)
    resolved = resolved_workflows["domain-clarification"]
    rule = next(
        item for item in resolved["rules"] if item["id"] == "DSET-RULE-DOMAIN-SPEC"
    )
    rule_path = adopter / str(rule["path"])
    rule_path.write_text(
        rule_path.read_text(encoding="utf-8")
        + "\n<!-- bounded self-host customization -->\n",
        encoding="utf-8",
    )
    if "DSET-E139" not in {item.code for item in validate_governance(adopter)}:
        raise DsetCommandError(
            "DSET-E141", rule_path, "local customization was not detected"
        )
    refresh_customization(adopter)
    _run_validator(
        [sys.executable, "-m", "dset_toolchain", "check", str(adopter)],
        root,
        "DSET-E141",
        "customized temporary adopter did not validate",
    )
    customized_workflows: dict[str, dict[str, Any]] = {}
    wrappers_unchanged = True
    for workflow_id in workflow_ids:
        customized, diagnostics = resolve_workflow(adopter, workflow_id)
        if diagnostics or customized is None:
            raise DsetCommandError(
                "DSET-E141",
                rule_path,
                f"customized workflow did not resolve: {workflow_id}",
            )
        customized_workflows[workflow_id] = customized
        wrapper_path = adopter / str(customized["wrapper"]["path"])
        wrappers_unchanged = (
            wrappers_unchanged and _sha256(wrapper_path) == wrapper_before[workflow_id]
        )
    return {
        "released_validator": released_status,
        "released_validator_diagnostic": released_diagnostic,
        "candidate_repository": "pass",
        "temporary_adopter": "pass",
        "customization": customized_workflows["domain-clarification"]["customization"],
        "workflows_resolved": list(workflow_ids),
        "wrappers_unchanged": wrappers_unchanged,
        "wrapper_unchanged": wrappers_unchanged,
        "recursion_stopped": not discover_layout(adopter).version_path.exists(),
        "released_ref": reference,
        "adopter": adopter.as_posix(),
    }


def _extract_released(root: Path, reference: str, destination: Path) -> None:
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
