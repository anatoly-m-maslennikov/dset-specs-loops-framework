"""Provide DSET runtime bridge behavior."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .errors import DsetCommandError
from .governance import resolve_workflow
from .runtime import (
    advance_session_closure,
    finish_run,
    load_invocation,
    resume_checkpoint,
    start_run,
    update_checkpoint,
)
from .settings import IMPLEMENTATION_MODES, load_project_settings
from .skill_catalog import PUBLIC_SKILL_MODES, PUBLIC_SKILL_WORKFLOWS


def start_runtime(
    root: Path,
    *,
    public_entrypoint: str,
    workflow_id: str,
    objective: str,
    mode_id: str | None = None,
    session_id: str | None = None,
    llm_session_ids: Sequence[str] = (),
    invocation_source: str = "public-skill",
    parent_run_id: str | None = None,
    root_run_id: str | None = None,
    scope: Mapping[str, Any] | None = None,
    parameters: Sequence[Mapping[str, Any]] = (),
    budget: Mapping[str, Any] | None = None,
    authorization_class: str = "read-only",
    authorization_state: str = "not-granted",
    authority_snapshot: Mapping[str, Any] | None = None,
    implementation_mode: str | None = None,
) -> dict[str, object]:
    """Start a governed runtime for one public or chained skill."""
    expected_mode = _validate_public_binding(public_entrypoint, workflow_id, mode_id)
    resolved = _resolved_workflow(root, workflow_id)
    selected_mode = mode_id if mode_id is not None else expected_mode
    selected_implementation_mode = _implementation_mode(
        root, public_entrypoint, implementation_mode
    )
    _require_explicit_resumption(root, session_id, scope)
    invocation = start_run(
        root,
        public_entrypoint=public_entrypoint,
        objective=objective,
        workflow_id=workflow_id,
        mode_id=selected_mode,
        session_id=session_id,
        llm_session_ids=llm_session_ids,
        invocation_source=invocation_source,
        parent_run_id=parent_run_id,
        root_run_id=root_run_id,
        ruleset_identity=_ruleset_identity(resolved),
        scope=scope,
        parameters=parameters,
        budget=budget,
        next_mode=selected_mode or "complete",
        next_reason_code="DSET-RUNTIME-HOST-BRIDGE",
        authorization_class=authorization_class,
        authorization_state=authorization_state,
        authority_snapshot=authority_snapshot,
        implementation_mode=selected_implementation_mode,
    )
    return {
        "run": invocation.run,
        "checkpoint": invocation.checkpoint,
        "resolved": resolved,
    }


def _validate_public_binding(
    entrypoint: str, workflow_id: str, mode_id: str | None
) -> str:
    """Validate the public skill's fixed workflow and default mode."""
    expected = PUBLIC_SKILL_WORKFLOWS.get(entrypoint)
    if expected is None:
        raise ValueError(f"unknown public skill: {entrypoint}")
    if expected != workflow_id:
        raise ValueError(
            "public skill/workflow mismatch: "
            f"{entrypoint} requires {expected}, received {workflow_id}"
        )
    expected_mode = PUBLIC_SKILL_MODES[entrypoint]
    if mode_id is not None and entrypoint != "dset" and mode_id != expected_mode:
        raise ValueError(
            "public skill/mode mismatch: "
            f"{entrypoint} requires {expected_mode}, received {mode_id}"
        )
    return expected_mode


def _resolved_workflow(root: Path, workflow_id: str) -> Mapping[str, Any]:
    """Resolve governance or raise the first deterministic diagnostic."""
    resolved, diagnostics = resolve_workflow(root, workflow_id)
    if diagnostics:
        diagnostic = diagnostics[0]
        raise DsetCommandError(diagnostic.code, diagnostic.path, diagnostic.message)
    assert resolved is not None
    return resolved


def _implementation_mode(root: Path, entrypoint: str, requested: str | None) -> str:
    """Resolve lazy or strict preparation only for implementation runs."""
    if entrypoint != "dset-implement":
        return "lazy"
    settings, issues = load_project_settings(root)
    if issues:
        raise ValueError("; ".join(issues))
    selected = requested if requested is not None else settings.implementation_mode
    if selected not in IMPLEMENTATION_MODES:
        raise ValueError("implementation preparation mode must be lazy or strict")
    return selected


def _require_explicit_resumption(
    root: Path, session_id: str | None, scope: Mapping[str, Any] | None
) -> None:
    """Stop implicit attachment to an already-active session."""
    if session_id is None:
        active = resume_checkpoint(root, scope=scope)
        if active is not None:
            raise ValueError(
                "active DSET session requires explicit session ID: "
                f"{active['session_id']}"
            )


def _ruleset_identity(resolved: Mapping[str, Any]) -> str:
    """Handle identity using the declared repository contract."""
    import hashlib
    import json

    payload = {
        "workflow_id": resolved["workflow_id"],
        "profile": resolved["profile"],
        "profile_version": resolved["profile_version"],
        "customization": resolved["customization"],
        "rules": [
            {
                "id": rule["id"],
                "document": rule["document"],
                "sha256": rule["sha256"],
            }
            for rule in resolved["rules"]
        ],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"ruleset:{hashlib.sha256(encoded).hexdigest()}"


def read_runtime(
    root: Path,
    *,
    session_id: str | None = None,
) -> dict[str, Any] | None:
    """Read runtime using the declared repository contract."""
    return resume_checkpoint(root, session_id=session_id)


def start_child_runtime(
    root: Path,
    *,
    session_id: str,
    workflow_id: str,
    objective: str,
    llm_session_ids: Sequence[str] = (),
) -> dict[str, object]:
    """Start child runtime using the declared repository contract."""
    checkpoint = resume_checkpoint(root, session_id=session_id)
    if checkpoint is None or checkpoint.get("status") not in {"active", "paused"}:
        raise ValueError(f"active session is unavailable: {session_id}")
    closure = checkpoint.get("closure")
    if not isinstance(closure, Mapping):
        raise ValueError("session closure is unavailable")
    if closure.get("next_workflow") != workflow_id:
        raise ValueError(
            "closure workflow mismatch: "
            f"expected {closure.get('next_workflow')}, received {workflow_id}"
        )
    skill_id = _skill_for_workflow(workflow_id)
    scope = checkpoint.get("scope")
    if not isinstance(scope, Mapping):
        raise ValueError("session scope is unavailable")
    return start_runtime(
        root,
        public_entrypoint=skill_id,
        workflow_id=workflow_id,
        objective=objective,
        mode_id=PUBLIC_SKILL_MODES[skill_id],
        session_id=session_id,
        llm_session_ids=llm_session_ids,
        invocation_source="chained-skill",
        root_run_id=str(checkpoint["root_run_id"]),
        scope=scope,
        implementation_mode=(
            str(closure.get("implementation_mode", "lazy"))
            if workflow_id == "implement"
            else None
        ),
    )


def advance_runtime_closure(
    root: Path,
    *,
    session_id: str,
    workflow_id: str | None = None,
    child_status: str = "succeeded",
    observations: Mapping[str, bool | None] | None = None,
) -> dict[str, Any]:
    """Handle runtime closure using the declared repository contract."""
    return advance_session_closure(
        root,
        session_id,
        workflow_id=workflow_id,
        child_status=child_status,
        observations=observations,
    )


def checkpoint_runtime(
    root: Path,
    run_id: str,
    *,
    status: str = "active",
    objective: str | None = None,
    next_mode: str | None = None,
    next_reason_code: str | None = None,
    requires_authorization: str | None = None,
) -> dict[str, Any]:
    """Handle runtime using the declared repository contract."""
    invocation = load_invocation(root, run_id)
    return update_checkpoint(
        invocation,
        status=status,
        objective=objective,
        next_mode=next_mode,
        next_reason_code=next_reason_code,
        requires_authorization=requires_authorization,
    )


def finish_runtime(
    root: Path,
    run_id: str,
    *,
    status: str,
    outputs: Sequence[str] = (),
    diagnostics: Sequence[str] = (),
    next_signals: Sequence[str] = (),
    usage: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Finish a run and close its DSET session terminally."""

    invocation = load_invocation(root, run_id)
    return finish_run(
        invocation,
        status=status,
        outputs=outputs,
        diagnostics=diagnostics,
        next_signals=next_signals,
        session_status="completed" if status == "succeeded" else "stopped",
        usage=usage,
    )


def handoff_runtime(
    root: Path,
    run_id: str,
    *,
    outputs: Sequence[str] = (),
    diagnostics: Sequence[str] = (),
    next_signals: Sequence[str],
    usage: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Finish one successful run while keeping its DSET session active."""

    if not next_signals:
        raise ValueError("active handoff requires at least one next signal")
    invocation = load_invocation(root, run_id)
    return finish_run(
        invocation,
        status="succeeded",
        outputs=outputs,
        diagnostics=diagnostics,
        next_signals=next_signals,
        session_status="active",
        usage=usage,
    )


def _skill_for_workflow(workflow_id: str) -> str:
    """Handle for workflow using the declared repository contract."""
    matches = [
        skill_id
        for skill_id, registered in PUBLIC_SKILL_WORKFLOWS.items()
        if registered == workflow_id
    ]
    if len(matches) != 1:
        raise ValueError(f"workflow has no unique public skill: {workflow_id}")
    return matches[0]
