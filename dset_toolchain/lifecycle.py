from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping
from typing import Any

IMPLEMENT_CRITERIA = (
    "decisions_reconciled",
    "proof_plan_complete",
    "implementation_plan_complete",
    "implementation_authorized",
    "implementation_complete",
)
IMPLEMENT_WORKFLOWS = (
    "decisions",
    "plan-proof",
    "plan-implementation",
    "implement",
)
WORKFLOW_PROGRESS = {
    "decisions": "decisions_reconciled",
    "plan-proof": "proof_plan_complete",
    "plan-implementation": "implementation_plan_complete",
    "implement": "implementation_complete",
}


class LifecycleClosureError(ValueError):
    pass


def initial_closure(public_entrypoint: str, mode_id: str | None) -> dict[str, Any]:
    if public_entrypoint != "dset-implement":
        return {
            "schema_version": "1.0",
            "requested_mode": mode_id,
            "status": "direct",
            "criteria": {},
            "next_workflow": mode_id,
            "reason_code": "DSET-RUNTIME-DIRECT",
            "history": [],
            "visited_states": [],
        }
    closure = {
        "schema_version": "1.0",
        "requested_mode": "implement",
        "status": "active",
        "criteria": {
            "decisions_reconciled": False,
            "proof_plan_complete": None,
            "implementation_plan_complete": None,
            "implementation_authorized": None,
            "implementation_complete": False,
        },
        "next_workflow": "decisions",
        "reason_code": "DSET-RUNTIME-DECISIONS-FIRST",
        "history": [],
        "visited_states": [],
    }
    closure["visited_states"] = [_state_fingerprint(closure)]
    return closure


def advance_closure(
    raw: Mapping[str, Any],
    *,
    workflow_id: str | None = None,
    child_status: str = "succeeded",
    observations: Mapping[str, bool | None] | None = None,
) -> dict[str, Any]:
    closure = _validated_copy(raw)
    if closure["requested_mode"] != "implement":
        raise LifecycleClosureError("direct workflow has no prerequisite closure")
    if closure["status"] in {"completed", "stopped"}:
        raise LifecycleClosureError("closure is terminal")
    expected = closure.get("next_workflow")
    if workflow_id is not None and workflow_id != expected:
        raise LifecycleClosureError(
            f"workflow mismatch: expected {expected}, received {workflow_id}"
        )
    if workflow_id is None and not observations:
        raise LifecycleClosureError("an observation or completed workflow is required")
    if child_status not in {"succeeded", "failed", "stopped", "ambiguous"}:
        raise LifecycleClosureError("invalid child status")
    if workflow_id is not None and child_status != "succeeded":
        closure["status"] = "stopped"
        closure["next_workflow"] = None
        closure["reason_code"] = {
            "failed": "DSET-RUNTIME-CHILD-FAILED",
            "stopped": "DSET-RUNTIME-CHILD-STOPPED",
            "ambiguous": "DSET-RUNTIME-AMBIGUOUS",
        }[child_status]
        closure["history"].append(
            {"workflow_id": workflow_id, "status": child_status, "progress": []}
        )
        return closure

    before = copy.deepcopy(closure["criteria"])
    if observations:
        for key, value in observations.items():
            if key not in IMPLEMENT_CRITERIA:
                raise LifecycleClosureError(f"unknown entry criterion: {key}")
            if value not in {True, False, None}:
                raise LifecycleClosureError(f"invalid criterion value: {key}")
            closure["criteria"][key] = value
    if workflow_id is not None:
        if workflow_id not in IMPLEMENT_WORKFLOWS:
            raise LifecycleClosureError(f"workflow is outside closure: {workflow_id}")
        closure["criteria"][WORKFLOW_PROGRESS[workflow_id]] = True

    progress = [
        key
        for key in IMPLEMENT_CRITERIA
        if before.get(key) != closure["criteria"].get(key)
    ]
    if not progress:
        closure["status"] = "stopped"
        closure["next_workflow"] = None
        closure["reason_code"] = "DSET-RUNTIME-NO-PROGRESS"
    else:
        _select_next(closure)
    if workflow_id is not None:
        closure["history"].append(
            {"workflow_id": workflow_id, "status": child_status, "progress": progress}
        )

    fingerprint = _state_fingerprint(closure)
    if fingerprint in closure["visited_states"]:
        closure["status"] = "stopped"
        closure["next_workflow"] = None
        closure["reason_code"] = "DSET-RUNTIME-REPEATED-STATE"
    else:
        closure["visited_states"].append(fingerprint)
    return closure


def _select_next(closure: dict[str, Any]) -> None:
    criteria = closure["criteria"]
    if criteria["decisions_reconciled"] is not True:
        _set_next(closure, "active", "decisions", "DSET-RUNTIME-DECISIONS-FIRST")
    elif criteria["proof_plan_complete"] is None:
        _set_next(closure, "blocked", None, "DSET-RUNTIME-CRITERIA-UNKNOWN")
    elif criteria["proof_plan_complete"] is False:
        _set_next(closure, "active", "plan-proof", "DSET-RUNTIME-PROOF-PLAN")
    elif criteria["implementation_plan_complete"] is None:
        _set_next(closure, "blocked", None, "DSET-RUNTIME-CRITERIA-UNKNOWN")
    elif criteria["implementation_plan_complete"] is False:
        _set_next(
            closure,
            "active",
            "plan-implementation",
            "DSET-RUNTIME-IMPLEMENTATION-PLAN",
        )
    elif criteria["implementation_authorized"] is not True:
        _set_next(
            closure,
            "authorization-required",
            None,
            "DSET-RUNTIME-AUTHORIZATION-REQUIRED",
        )
    elif criteria["implementation_complete"] is not True:
        _set_next(closure, "ready", "implement", "DSET-RUNTIME-IMPLEMENT")
    else:
        _set_next(closure, "completed", None, "DSET-RUNTIME-COMPLETE")


def _set_next(
    closure: dict[str, Any], status: str, workflow: str | None, reason: str
) -> None:
    closure["status"] = status
    closure["next_workflow"] = workflow
    closure["reason_code"] = reason


def _validated_copy(raw: Mapping[str, Any]) -> dict[str, Any]:
    closure = copy.deepcopy(dict(raw))
    if closure.get("schema_version") != "1.0":
        raise LifecycleClosureError("unsupported closure schema")
    criteria = closure.get("criteria")
    history = closure.get("history")
    visited = closure.get("visited_states")
    if not isinstance(criteria, dict):
        raise LifecycleClosureError("closure criteria are invalid")
    if not isinstance(history, list) or not isinstance(visited, list):
        raise LifecycleClosureError("closure history is invalid")
    return closure


def _state_fingerprint(closure: Mapping[str, Any]) -> str:
    payload = {
        "requested_mode": closure["requested_mode"],
        "criteria": closure["criteria"],
        "status": closure["status"],
        "next_workflow": closure["next_workflow"],
        "reason_code": closure["reason_code"],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"state:{hashlib.sha256(encoded).hexdigest()}"
