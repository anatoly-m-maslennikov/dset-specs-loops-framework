from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .errors import DsetCommandError
from .governance import resolve_workflow
from .runtime import (
    finish_run,
    load_invocation,
    resume_checkpoint,
    start_run,
    update_checkpoint,
)


def start_runtime(
    root: Path,
    *,
    public_entrypoint: str,
    workflow_id: str,
    objective: str,
    mode_id: str | None = None,
    session_id: str | None = None,
    llm_session_ids: Sequence[str] = (),
) -> dict[str, object]:
    resolved, diagnostics = resolve_workflow(root, workflow_id)
    if diagnostics:
        diagnostic = diagnostics[0]
        raise DsetCommandError(diagnostic.code, diagnostic.path, diagnostic.message)
    assert resolved is not None
    profile = resolved["profile"]
    profile_version = resolved["profile_version"]
    customization = resolved["customization"]
    identity = f"{profile}:{profile_version}:{customization}"
    invocation = start_run(
        root,
        public_entrypoint=public_entrypoint,
        objective=objective,
        workflow_id=workflow_id,
        mode_id=mode_id,
        session_id=session_id,
        llm_session_ids=llm_session_ids,
        invocation_source="public-skill",
        ruleset_identity=identity,
        next_mode=mode_id or "complete",
        next_reason_code="DSET-RUNTIME-HOST-BRIDGE",
    )
    return {
        "run": invocation.run,
        "checkpoint": invocation.checkpoint,
        "resolved": resolved,
    }


def read_runtime(
    root: Path,
    *,
    session_id: str | None = None,
) -> dict[str, Any] | None:
    return resume_checkpoint(root, session_id=session_id)


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
    session_status: str | None = None,
    usage: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    invocation = load_invocation(root, run_id)
    return finish_run(
        invocation,
        status=status,
        outputs=outputs,
        diagnostics=diagnostics,
        next_signals=next_signals,
        session_status=session_status,
        usage=usage,
    )
