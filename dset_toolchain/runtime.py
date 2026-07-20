from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import tempfile
import uuid
from collections.abc import Mapping, Sequence
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .lifecycle import advance_closure, initial_closure
from .skill_catalog import PUBLIC_SKILL_MODES, PUBLIC_SKILL_WORKFLOWS
from .yaml_subset import load

RUN_SCHEMA_VERSION = "1.2"
CHECKPOINT_SCHEMA_VERSION = "1.3"
MAX_RECORD_BYTES = 64 * 1024
MAX_RUN_AGE = timedelta(days=30)
MAX_RUN_COUNT = 200
MAX_RUN_BYTES = 20 * 1024 * 1024

_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_LLM_SESSION_ID = re.compile(r"^[a-z][a-z0-9_-]*:[A-Za-z0-9._:-]+$")
_STABLE_CODE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+){1,5}$")
_PUBLIC_ENTRYPOINTS = frozenset(PUBLIC_SKILL_WORKFLOWS)
_INVOCATION_SOURCES = {
    "operator",
    "public-skill",
    "chained-skill",
    "governed-model",
    "delegated-run",
}
_RUN_STATUSES = {"succeeded", "failed", "stopped", "interrupted"}
_SESSION_STATUSES = {"active", "paused", "completed", "stopped"}
_NEXT_MODES = {
    "initialize",
    "repair-governance",
    "decompose",
    "diagnose",
    "clarify",
    "landscape",
    "prototype",
    "decisions",
    "plan-proof",
    "plan-implementation",
    "implement",
    "verify",
    "triage-work",
    "release",
    "complete",
}
_NEXT_AUTHORIZATIONS = {
    "none",
    "repository-write",
    "external-write",
    "publication",
}
_AUTHORIZATION_CLASSES = {
    "read-only",
    "repository-write",
    "external-write",
    "publication",
    "unknown",
}
_AUTHORIZATION_STATES = {"granted", "not-granted", "consumed", "unknown"}
_PARAMETER_NAMES = {
    "operation",
    "change_profile",
    "budget_profile",
    "applicability",
    "authorization",
    "scope_kind",
    "source_kind",
    "target_kind",
    "result_class",
    "risk_class",
}
_CATEGORY_VALUES = {
    "none",
    "small",
    "standard",
    "large",
    "defect",
    "adoption",
    "low",
    "medium",
    "high",
    "applicable",
    "not-applicable",
    "read-only",
    "write-authorized",
    "automatic",
    "manual",
    "local",
    "hosted",
    "success",
    "failure",
    "stopped",
    "unknown",
}


class RuntimeStateError(ValueError):
    """The requested runtime transition is invalid or unsafe."""


class AmbiguousSessionError(RuntimeStateError):
    """More than one active checkpoint matches an implicit resume."""


class RunFinishedError(RuntimeStateError):
    """A terminal invocation cannot be finalized again."""


@dataclass(frozen=True)
class _Storage:
    root: Path
    runs: Path
    sessions: Path


@dataclass
class RuntimeInvocation:
    """In-process handle for one DSET invocation.

    The public dictionaries are copies of the schema-shaped state returned to
    callers. Persistence is deliberately best-effort: a valid writable DSET
    repository receives local evidence, while an absent or unwritable root
    receives the same terminal record with ``persistence: unavailable``.
    """

    run: dict[str, Any]
    checkpoint: dict[str, Any]
    storage: _Storage | None
    running_path: Path | None
    finished: bool = False

    @property
    def session_id(self) -> str:
        return str(self.run["session_id"])

    @property
    def run_id(self) -> str:
        return str(self.run["run_id"])


def start_run(
    root: Path | None,
    *,
    public_entrypoint: str,
    objective: str,
    workflow_id: str | None,
    mode_id: str | None = None,
    session_id: str | None = None,
    llm_session_ids: Sequence[str] = (),
    invocation_source: str = "operator",
    parent_run_id: str | None = None,
    root_run_id: str | None = None,
    ruleset_identity: str | None = None,
    scope: Mapping[str, Any] | None = None,
    parameters: Sequence[Mapping[str, Any]] = (),
    budget: Mapping[str, Any] | None = None,
    next_mode: str = "complete",
    next_reason_code: str = "DSET-RUNTIME-START",
    requires_authorization: str = "none",
    authorization_class: str = "read-only",
    authorization_state: str = "not-granted",
    authority_snapshot: Mapping[str, Any] | None = None,
) -> RuntimeInvocation:
    """Start one invocation and its resumable checkpoint.

    ``root`` must already be a DSET repository. This function never creates a
    repository or manifest. If local evidence cannot be persisted, it returns
    an in-memory handle and ``finish_run`` emits a schema-compatible terminal
    record with unavailable persistence.
    """

    _require(public_entrypoint in _PUBLIC_ENTRYPOINTS, "unknown public entrypoint")
    expected_workflow = PUBLIC_SKILL_WORKFLOWS[public_entrypoint]
    _require(
        workflow_id is None or workflow_id == expected_workflow,
        "public entrypoint and workflow do not match",
    )
    expected_mode = PUBLIC_SKILL_MODES[public_entrypoint]
    _require(
        mode_id is None or public_entrypoint == "dset" or mode_id == expected_mode,
        "public entrypoint and mode do not match",
    )
    _require(invocation_source in _INVOCATION_SOURCES, "unknown invocation source")
    _require(0 < len(objective) <= 1024, "objective must contain 1..1024 characters")
    _require(next_mode in _NEXT_MODES, "unknown next mode")
    _require(
        requires_authorization in _NEXT_AUTHORIZATIONS,
        "unknown next authorization",
    )
    _require(
        authorization_class in _AUTHORIZATION_CLASSES,
        "unknown authorization class",
    )
    _require(
        authorization_state in _AUTHORIZATION_STATES,
        "unknown authorization state",
    )
    normalized_llm_ids = _normalize_llm_session_ids(llm_session_ids)
    normalized_scope = _normalize_scope(root, scope)
    normalized_parameters = _normalize_parameters(parameters)
    normalized_budget = _normalize_budget(budget)
    normalized_snapshot = _normalize_authority_snapshot(authority_snapshot)
    for identifier in (
        session_id,
        parent_run_id,
        root_run_id,
        workflow_id,
        mode_id,
        ruleset_identity,
    ):
        _require_nullable_id(identifier)
    _require_id(next_reason_code)

    storage = _storage_for_root(root)
    checkpoint_scope = _checkpoint_scope(normalized_scope)
    resumed: dict[str, Any] | None = None
    if storage is not None:
        if session_id is not None:
            resumed = _load_explicit_checkpoint(storage, session_id)
            if resumed is not None and resumed.get("status") not in {
                "active",
                "paused",
            }:
                raise RuntimeStateError(f"session is not active: {session_id}")
        else:
            resumed = _select_implicit_checkpoint(storage, checkpoint_scope)

    selected_session_id = session_id
    if resumed is not None:
        selected_session_id = str(resumed["session_id"])
    if selected_session_id is None:
        selected_session_id = _new_id("session")
    _require_id(selected_session_id)

    run_id = _new_id("run")
    inherited_root = str(resumed["root_run_id"]) if resumed is not None else None
    inherited_parent = str(resumed["latest_run_id"]) if resumed is not None else None
    selected_root_run = root_run_id or inherited_root or run_id
    selected_parent_run = (
        parent_run_id if parent_run_id is not None else inherited_parent
    )
    _require_id(selected_root_run)
    _require_nullable_id(selected_parent_run)
    checkpoint_relative = (
        f".dset/sessions/{selected_session_id}.json" if storage is not None else None
    )
    started_at = _utc_now()
    run = {
        "schema_version": RUN_SCHEMA_VERSION,
        "session_id": selected_session_id,
        "llm_session_ids": normalized_llm_ids,
        "run_id": run_id,
        "root_run_id": selected_root_run,
        "parent_run_id": selected_parent_run,
        "invocation_source": invocation_source,
        "checkpoint": checkpoint_relative,
        "started_at": started_at,
        "finished_at": None,
        "status": "running",
        "persistence": "persisted" if storage is not None else "unavailable",
        "scope": _run_scope(normalized_scope),
        "skill_id": public_entrypoint,
        "workflow_id": workflow_id,
        "mode_id": mode_id,
        "ruleset_identity": ruleset_identity,
        "parameters": normalized_parameters,
        "outputs": [],
        "diagnostics": [],
        "next_signals": [],
        "budget": normalized_budget,
    }

    sequence = int(resumed.get("sequence", -1)) + 1 if resumed is not None else 0
    completed = copy.deepcopy(resumed.get("completed", [])) if resumed else []
    pending = copy.deepcopy(resumed.get("pending", [])) if resumed else []
    touched = copy.deepcopy(resumed.get("touched_paths", [])) if resumed else []
    closure = (
        copy.deepcopy(resumed["closure"])
        if resumed is not None and isinstance(resumed.get("closure"), dict)
        else initial_closure(public_entrypoint, mode_id)
    )
    active_run_ids = _active_run_ids(resumed)
    active_run_ids.append(run_id)
    checkpoint = {
        "schema_version": CHECKPOINT_SCHEMA_VERSION,
        "session_id": selected_session_id,
        "llm_session_ids": _merge_llm_session_ids(
            resumed.get("llm_session_ids", []) if resumed else [], normalized_llm_ids
        ),
        "sequence": sequence,
        "updated_at": started_at,
        "status": "active",
        "persistence": "persisted" if storage is not None else "unavailable",
        "public_entrypoint": (
            resumed.get("public_entrypoint", public_entrypoint)
            if resumed
            else public_entrypoint
        ),
        "root_run_id": selected_root_run,
        "latest_run_id": run_id,
        "active_run_ids": active_run_ids,
        "scope": checkpoint_scope,
        "objective": objective,
        "ruleset_identity": ruleset_identity,
        "completed": completed,
        "pending": pending,
        "authorization": {
            "class": authorization_class,
            "state": authorization_state,
        },
        "touched_paths": touched,
        "authority_snapshot": normalized_snapshot,
        "closure": closure,
        "next": {
            "mode": next_mode,
            "reason_code": next_reason_code,
            "requires_authorization": requires_authorization,
        },
    }

    running_path: Path | None = None
    if storage is not None:
        candidate = storage.runs / f".{run_id}.running.json"
        try:
            _replace_json(candidate, run)
            _replace_json(storage.sessions / f"{selected_session_id}.json", checkpoint)
            running_path = candidate
        except OSError:
            _safe_unlink(candidate)
            storage = None
            run["persistence"] = "unavailable"
            run["checkpoint"] = None
            checkpoint["persistence"] = "unavailable"
    return RuntimeInvocation(run, checkpoint, storage, running_path)


def resume_checkpoint(
    root: Path | None,
    *,
    session_id: str | None = None,
    scope: Mapping[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Read an explicit or uniquely compatible active checkpoint.

    An explicit unknown session returns ``None``. Implicit matching returns
    ``None`` when no checkpoint matches and stops with
    ``AmbiguousSessionError`` when more than one active checkpoint matches.
    This function is read-only and never creates ``.dset``.
    """

    _require_nullable_id(session_id)
    storage = _existing_storage(root)
    if storage is None:
        return None
    if session_id is not None:
        return _load_explicit_checkpoint(storage, session_id)
    normalized_scope = _checkpoint_scope(_normalize_scope(root, scope))
    return _select_implicit_checkpoint(storage, normalized_scope)


def advance_session_closure(
    root: Path,
    session_id: str,
    *,
    workflow_id: str | None = None,
    child_status: str = "succeeded",
    observations: Mapping[str, bool | None] | None = None,
) -> dict[str, Any]:
    """Advance one persisted entry-criteria closure after an authoritative read."""

    _require_id(session_id)
    storage = _existing_storage(root)
    if storage is None:
        raise RuntimeStateError("runtime storage is unavailable")
    path = storage.sessions / f"{session_id}.json"
    checkpoint = _read_checkpoint(path)
    if checkpoint.get("status") not in {"active", "paused"}:
        raise RuntimeStateError(f"session is not active: {session_id}")
    raw_closure = checkpoint.get("closure")
    if not isinstance(raw_closure, Mapping):
        raise RuntimeStateError("session closure is unavailable")
    closure = advance_closure(
        raw_closure,
        workflow_id=workflow_id,
        child_status=child_status,
        observations=observations,
    )
    checkpoint["closure"] = closure
    checkpoint["sequence"] = int(checkpoint["sequence"]) + 1
    checkpoint["updated_at"] = _utc_now()
    checkpoint["next"] = {
        "mode": closure.get("next_workflow") or "complete",
        "reason_code": closure["reason_code"],
        "requires_authorization": (
            "repository-write"
            if closure["status"] == "authorization-required"
            else "none"
        ),
    }
    if closure["status"] == "stopped":
        checkpoint["status"] = "stopped"
    _replace_json(path, checkpoint)
    return copy.deepcopy(checkpoint)


def update_checkpoint(
    invocation: RuntimeInvocation,
    *,
    status: str = "active",
    objective: str | None = None,
    ruleset_identity: str | None = None,
    completed: Sequence[Mapping[str, Any]] | None = None,
    pending: Sequence[Mapping[str, Any]] | None = None,
    touched_paths: Sequence[str] | None = None,
    authorization_class: str | None = None,
    authorization_state: str | None = None,
    authority_snapshot: Mapping[str, Any] | None = None,
    next_mode: str | None = None,
    next_reason_code: str | None = None,
    requires_authorization: str | None = None,
) -> dict[str, Any]:
    """Atomically replace one session checkpoint with its next bounded state."""

    _require(not invocation.finished, "cannot update a finished invocation")
    _require(status in _SESSION_STATUSES, "unknown checkpoint status")
    checkpoint = copy.deepcopy(invocation.checkpoint)
    checkpoint["sequence"] = int(checkpoint["sequence"]) + 1
    checkpoint["updated_at"] = _utc_now()
    checkpoint["status"] = status
    checkpoint["latest_run_id"] = invocation.run_id
    if objective is not None:
        _require(
            0 < len(objective) <= 1024,
            "objective must contain 1..1024 characters",
        )
        checkpoint["objective"] = objective
    if ruleset_identity is not None:
        _require_id(ruleset_identity)
        checkpoint["ruleset_identity"] = ruleset_identity
        invocation.run["ruleset_identity"] = ruleset_identity
    if completed is not None:
        checkpoint["completed"] = _normalize_work_pointers(completed, 64)
    if pending is not None:
        checkpoint["pending"] = _normalize_work_pointers(pending, 32)
    if touched_paths is not None:
        checkpoint["touched_paths"] = _normalize_relative_paths(touched_paths, 64)
    if authorization_class is not None:
        _require(
            authorization_class in _AUTHORIZATION_CLASSES,
            "unknown authorization class",
        )
        checkpoint["authorization"]["class"] = authorization_class
    if authorization_state is not None:
        _require(
            authorization_state in _AUTHORIZATION_STATES,
            "unknown authorization state",
        )
        checkpoint["authorization"]["state"] = authorization_state
    if authority_snapshot is not None:
        checkpoint["authority_snapshot"] = _normalize_authority_snapshot(
            authority_snapshot
        )
    if next_mode is not None:
        _require(next_mode in _NEXT_MODES, "unknown next mode")
        checkpoint["next"]["mode"] = next_mode
    if next_reason_code is not None:
        _require_id(next_reason_code)
        checkpoint["next"]["reason_code"] = next_reason_code
    if requires_authorization is not None:
        _require(
            requires_authorization in _NEXT_AUTHORIZATIONS,
            "unknown next authorization",
        )
        checkpoint["next"]["requires_authorization"] = requires_authorization

    if invocation.storage is not None:
        path = invocation.storage.sessions / f"{invocation.session_id}.json"
        try:
            _replace_json(path, checkpoint)
        except OSError:
            invocation.storage = None
            checkpoint["persistence"] = "unavailable"
            invocation.run["persistence"] = "unavailable"
            invocation.run["checkpoint"] = None
    else:
        checkpoint["persistence"] = "unavailable"
    invocation.checkpoint = checkpoint
    return copy.deepcopy(checkpoint)


def finish_run(
    invocation: RuntimeInvocation,
    *,
    status: str,
    outputs: Sequence[str] = (),
    diagnostics: Sequence[str] = (),
    next_signals: Sequence[str] = (),
    session_status: str | None = None,
    usage: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Finalize one immutable terminal run and its replaceable checkpoint."""

    if invocation.finished:
        raise RunFinishedError("run is already terminal")
    _require(status in _RUN_STATUSES, "unknown terminal run status")
    normalized_outputs = _normalize_relative_paths(outputs, 32)
    normalized_diagnostics = _normalize_diagnostics(diagnostics)
    normalized_signals = _normalize_next_signals(next_signals)
    checkpoint = copy.deepcopy(invocation.checkpoint)
    active_run_ids = _active_run_ids(checkpoint)
    if invocation.run_id not in active_run_ids:
        raise RuntimeStateError(
            f"checkpoint does not own invocation: {invocation.run_id}"
        )
    remaining_run_ids = [
        identifier for identifier in active_run_ids if identifier != invocation.run_id
    ]
    final_session_status = session_status
    if final_session_status is None:
        if remaining_run_ids:
            final_session_status = "active"
        else:
            final_session_status = "completed" if status == "succeeded" else "stopped"
    _require(final_session_status in _SESSION_STATUSES, "unknown checkpoint status")
    if final_session_status in {"completed", "stopped"} and remaining_run_ids:
        raise RuntimeStateError(
            "session cannot become terminal while child or parent runs remain active"
        )
    terminal = copy.deepcopy(invocation.run)
    terminal.update(
        {
            "finished_at": _utc_now(),
            "status": status,
            "outputs": normalized_outputs,
            "diagnostics": normalized_diagnostics,
            "next_signals": normalized_signals,
        }
    )
    if usage is not None:
        terminal["usage"] = _normalize_usage(usage)

    storage = invocation.storage
    if storage is not None:
        name = f"{_utc_basic()}-{invocation.run_id}.json"
        destination = storage.runs / name
        try:
            _publish_new_json(destination, terminal)
            _safe_unlink(invocation.running_path)
        except OSError:
            terminal["persistence"] = "unavailable"
            terminal["checkpoint"] = None
            storage = None
        else:
            with suppress(OSError):
                _prune_runs(storage.runs)
    else:
        terminal["persistence"] = "unavailable"
        terminal["checkpoint"] = None

    invocation.run = terminal
    invocation.storage = storage
    checkpoint["sequence"] = int(checkpoint["sequence"]) + 1
    checkpoint["updated_at"] = str(terminal["finished_at"])
    checkpoint["status"] = final_session_status
    checkpoint["active_run_ids"] = remaining_run_ids
    checkpoint["persistence"] = "persisted" if storage is not None else "unavailable"
    if storage is not None:
        try:
            _replace_json(
                storage.sessions / f"{invocation.session_id}.json", checkpoint
            )
        except OSError:
            checkpoint["persistence"] = "unavailable"
            invocation.storage = None
    invocation.checkpoint = checkpoint
    invocation.finished = True
    _encoded_json(terminal)
    _encoded_json(checkpoint)
    return copy.deepcopy(terminal)


def load_invocation(root: Path, run_id: str) -> RuntimeInvocation:
    """Reload one persisted non-terminal invocation for a host bridge call."""

    _require_id(run_id)
    storage = _existing_storage(root)
    if storage is None:
        raise RuntimeStateError("runtime storage is unavailable")
    running_path = storage.runs / f".{run_id}.running.json"
    run = _read_running_record(running_path)
    if run.get("run_id") != run_id or run.get("status") != "running":
        raise RuntimeStateError(f"invalid running invocation: {run_id}")
    session_id = run.get("session_id")
    _require_id(session_id)
    checkpoint = _read_checkpoint(storage.sessions / f"{session_id}.json")
    if run_id not in _active_run_ids(checkpoint):
        raise RuntimeStateError(f"checkpoint does not own invocation: {run_id}")
    return RuntimeInvocation(run, checkpoint, storage, running_path)


def _storage_for_root(root: Path | None) -> _Storage | None:
    if not _is_dset_root(root):
        return None
    assert root is not None
    resolved = root.resolve()
    runs = resolved / ".dset" / "runs"
    sessions = resolved / ".dset" / "sessions"
    try:
        runs.mkdir(parents=True, exist_ok=True)
        sessions.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None
    return _Storage(resolved, runs, sessions)


def _existing_storage(root: Path | None) -> _Storage | None:
    if not _is_dset_root(root):
        return None
    assert root is not None
    resolved = root.resolve()
    runs = resolved / ".dset" / "runs"
    sessions = resolved / ".dset" / "sessions"
    if not sessions.is_dir():
        return None
    return _Storage(resolved, runs, sessions)


def _is_dset_root(root: Path | None) -> bool:
    if root is None or not root.is_dir():
        return False
    authorities = (
        root / "dset" / "scopes" / "meta" / "dset.yaml",
        root / "dset" / "dset.yaml",
    )
    return sum(path.is_file() for path in authorities) == 1


def _load_explicit_checkpoint(
    storage: _Storage, session_id: str
) -> dict[str, Any] | None:
    path = storage.sessions / f"{session_id}.json"
    if not path.is_file():
        return None
    return _read_checkpoint(path)


def _select_implicit_checkpoint(
    storage: _Storage, scope: Mapping[str, Any]
) -> dict[str, Any] | None:
    matches: list[dict[str, Any]] = []
    for path in sorted(storage.sessions.glob("*.json")):
        checkpoint = _read_checkpoint(path)
        if checkpoint.get("status") not in {"active", "paused"}:
            continue
        candidate_scope = checkpoint.get("scope")
        if isinstance(candidate_scope, dict) and _scopes_compatible(
            candidate_scope, scope
        ):
            matches.append(checkpoint)
    if len(matches) > 1:
        sessions = ", ".join(sorted(str(item["session_id"]) for item in matches))
        raise AmbiguousSessionError(f"multiple compatible sessions: {sessions}")
    return matches[0] if matches else None


def _read_checkpoint(path: Path) -> dict[str, Any]:
    try:
        if path.stat().st_size > MAX_RECORD_BYTES:
            raise RuntimeStateError(f"checkpoint exceeds size limit: {path.name}")
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeStateError(f"invalid checkpoint: {path.name}") from error
    if not isinstance(data, dict) or data.get("schema_version") not in {
        "1.1",
        "1.2",
        CHECKPOINT_SCHEMA_VERSION,
    }:
        raise RuntimeStateError(f"invalid checkpoint: {path.name}")
    if data["schema_version"] in {"1.1", "1.2"}:
        previous_version = str(data["schema_version"])
        data["schema_version"] = CHECKPOINT_SCHEMA_VERSION
        if previous_version == "1.1":
            data["closure"] = initial_closure(
                str(data.get("public_entrypoint", "dset")),
                _checkpoint_mode(data),
            )
        latest = data.get("latest_run_id")
        running_path = path.parent.parent / "runs" / f".{latest}.running.json"
        data["active_run_ids"] = (
            [latest]
            if isinstance(latest, str)
            and data.get("status") in {"active", "paused"}
            and running_path.is_file()
            else []
        )
    return data


def _active_run_ids(checkpoint: Mapping[str, Any] | None) -> list[str]:
    if checkpoint is None:
        return []
    raw = checkpoint.get("active_run_ids", [])
    if not isinstance(raw, list):
        raise RuntimeStateError("checkpoint active_run_ids are invalid")
    values = [str(item) for item in raw]
    if (
        len(values) > 32
        or len(values) != len(set(values))
        or any(not _ID.fullmatch(item) for item in values)
    ):
        raise RuntimeStateError("checkpoint active_run_ids are invalid")
    return values


def _checkpoint_mode(checkpoint: Mapping[str, Any]) -> str | None:
    next_value = checkpoint.get("next")
    if not isinstance(next_value, Mapping):
        return None
    mode = next_value.get("mode")
    return str(mode) if isinstance(mode, str) else None


def _read_running_record(path: Path) -> dict[str, Any]:
    try:
        if path.stat().st_size > MAX_RECORD_BYTES:
            raise RuntimeStateError(f"running record exceeds size limit: {path.name}")
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeStateError(f"invalid running record: {path.name}") from error
    if not isinstance(data, dict) or data.get("schema_version") != RUN_SCHEMA_VERSION:
        raise RuntimeStateError(f"invalid running record: {path.name}")
    return data


def _scopes_compatible(candidate: Mapping[str, Any], wanted: Mapping[str, Any]) -> bool:
    for key in ("repository", "workspace", "project", "package", "change"):
        value = wanted.get(key)
        if value is not None and candidate.get(key) != value:
            return False
    return candidate.get("target") == wanted.get("target")


def _normalize_scope(
    root: Path | None, raw: Mapping[str, Any] | None
) -> dict[str, Any]:
    provided = dict(raw or {})
    repository = provided.get("repository")
    if repository is None and root is not None and root.is_dir():
        repository = _repository_identity(root)
    values = {
        "repository": repository,
        "workspace": provided.get("workspace"),
        "project": provided.get("project"),
        "package": provided.get("package"),
        "change": provided.get("change"),
    }
    for value in values.values():
        if value is not None:
            _require(
                isinstance(value, str)
                and 0 < len(value) <= 128
                and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}", value)
                is not None,
                "invalid scope identifier",
            )
    target = provided.get("target", {"repository": True, "work_areas": []})
    _require(isinstance(target, Mapping), "scope target must be a mapping")
    repository_target = target.get("repository")
    work_areas = target.get("work_areas")
    _require(isinstance(repository_target, bool), "invalid target repository flag")
    _require(isinstance(work_areas, list), "target work_areas must be a list")
    normalized_areas = _normalize_ids(work_areas, 32)
    _require(
        (repository_target and not normalized_areas)
        or (not repository_target and bool(normalized_areas)),
        "target must select the repository or at least one Work Area",
    )
    values["target"] = {
        "repository": repository_target,
        "work_areas": normalized_areas,
    }
    return values


def _repository_identity(root: Path) -> str:
    manifest_path = root / "dset" / "scopes" / "meta" / "dset.yaml"
    try:
        manifest = load(manifest_path)
    except (OSError, UnicodeError, ValueError):
        manifest = {}
    project = manifest.get("project") if isinstance(manifest, dict) else None
    if isinstance(project, dict):
        for key in ("repository_slug", "id"):
            value = project.get(key)
            if isinstance(value, str) and value:
                return value
    name = root.resolve().name
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}", name) is not None:
        return name
    digest = hashlib.sha256(str(root.resolve()).encode("utf-8")).hexdigest()[:16]
    return f"path-{digest}"


def _run_scope(scope: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "repository": scope["repository"],
        "workspace": scope["workspace"],
        "project": scope["project"],
        "package": scope["package"],
        "change": scope["change"],
        "target": copy.deepcopy(scope["target"]),
    }


def _checkpoint_scope(scope: Mapping[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(dict(scope))


def _normalize_llm_session_ids(values: Sequence[str]) -> list[str]:
    _require(len(values) <= 8, "too many LLM session IDs")
    normalized = list(values)
    _require(len(normalized) == len(set(normalized)), "duplicate LLM session ID")
    for value in normalized:
        _require(
            isinstance(value, str)
            and len(value) <= 160
            and _LLM_SESSION_ID.fullmatch(value) is not None,
            "invalid LLM session ID",
        )
    return normalized


def _merge_llm_session_ids(first: Any, second: Sequence[str]) -> list[str]:
    earlier = first if isinstance(first, list) else []
    return _normalize_llm_session_ids(
        list(dict.fromkeys([*map(str, earlier), *second]))
    )


def _normalize_parameters(values: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    _require(len(values) <= 32, "too many run parameters")
    result: list[dict[str, Any]] = []
    for value in values:
        item = copy.deepcopy(dict(value))
        _require(
            set(item) == {"name", "representation", "value"},
            "invalid run parameter",
        )
        _require(isinstance(item["name"], str), "invalid parameter name")
        _require(
            item["name"] in _PARAMETER_NAMES,
            "invalid parameter name",
        )
        _require(
            item["representation"] in {"category", "sha256", "redacted"},
            "invalid parameter representation",
        )
        if item["representation"] == "category":
            _require(item["value"] in _CATEGORY_VALUES, "invalid category value")
        if item["representation"] == "sha256":
            _require(
                isinstance(item["value"], str)
                and re.fullmatch(r"[0-9a-f]{64}", item["value"]) is not None,
                "invalid parameter digest",
            )
        if item["representation"] == "redacted":
            _require(item["value"] == "[redacted]", "invalid redacted parameter")
        result.append(item)
    return result


def _normalize_budget(raw: Mapping[str, Any] | None) -> dict[str, Any]:
    budget: dict[str, Any] = {
        "profile": "medium",
        "requested_model": None,
        "requested_effort": None,
        "effective_model": None,
        "effective_effort": None,
        "attestation": "unsupported",
        "planned_subagents": 0,
        "actual_subagents": 0,
        "planned_rounds": 0,
        "actual_rounds": 0,
        "deviations": [],
    }
    if raw is not None:
        unknown = set(raw) - set(budget)
        _require(not unknown, f"unknown budget fields: {', '.join(sorted(unknown))}")
        budget.update(copy.deepcopy(dict(raw)))
    _require(budget["profile"] in {"low", "medium", "high"}, "invalid budget profile")
    _require(
        budget["attestation"]
        in {"confirmed", "runtime-default-unverified", "unsupported"},
        "invalid budget attestation",
    )
    for key in (
        "requested_model",
        "requested_effort",
        "effective_model",
        "effective_effort",
    ):
        _require_nullable_id(budget[key])
    limits = {"low": (1, 1), "medium": (3, 2), "high": (6, 3)}
    agent_limit, round_limit = limits[str(budget["profile"])]
    for key in ("planned_subagents", "actual_subagents"):
        _require(
            isinstance(budget[key], int) and 0 <= budget[key] <= agent_limit,
            "budget agent count exceeds profile",
        )
    for key in ("planned_rounds", "actual_rounds"):
        _require(
            isinstance(budget[key], int) and 0 <= budget[key] <= round_limit,
            "budget round count exceeds profile",
        )
    deviations = budget["deviations"]
    _require(
        isinstance(deviations, list) and len(deviations) <= 8, "invalid deviations"
    )
    for deviation in deviations:
        _require_stable_code(deviation)
    return budget


def _normalize_authority_snapshot(raw: Mapping[str, Any] | None) -> dict[str, Any]:
    snapshot: dict[str, Any] = {
        "git_commit": None,
        "working_tree_digest": None,
        "change_manifest": None,
        "proof_ids": [],
        "hosted_refs": [],
    }
    if raw is not None:
        unknown = set(raw) - set(snapshot)
        _require(not unknown, "unknown authority snapshot field")
        snapshot.update(copy.deepcopy(dict(raw)))
    commit = snapshot["git_commit"]
    digest = snapshot["working_tree_digest"]
    _require(
        commit is None
        or (isinstance(commit, str) and re.fullmatch(r"[0-9a-f]{40}", commit)),
        "invalid Git commit",
    )
    _require(
        digest is None
        or (isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest)),
        "invalid working-tree digest",
    )
    manifest = snapshot["change_manifest"]
    if manifest is not None:
        _require_relative_path(manifest)
    _require(isinstance(snapshot["proof_ids"], list), "proof IDs must be a list")
    _require(isinstance(snapshot["hosted_refs"], list), "hosted refs must be a list")
    snapshot["proof_ids"] = _normalize_ids(snapshot["proof_ids"], 32)
    snapshot["hosted_refs"] = _normalize_ids(snapshot["hosted_refs"], 16)
    return snapshot


def _normalize_work_pointers(
    values: Sequence[Mapping[str, Any]], limit: int
) -> list[dict[str, Any]]:
    _require(len(values) <= limit, "too many work pointers")
    result: list[dict[str, Any]] = []
    for value in values:
        item = copy.deepcopy(dict(value))
        _require(set(item) == {"kind", "id", "path"}, "invalid work pointer")
        _require(
            item["kind"] in {"artifact", "workflow", "proof", "diagnostic", "handoff"},
            "invalid work-pointer kind",
        )
        _require_nullable_id(item["id"])
        if item["path"] is not None:
            _require_relative_path(item["path"])
        _require(
            item["id"] is not None or item["path"] is not None, "empty work pointer"
        )
        result.append(item)
    return result


def _normalize_relative_paths(values: Sequence[str], limit: int) -> list[str]:
    _require(len(values) <= limit, "too many paths")
    result = list(values)
    _require(len(result) == len(set(result)), "duplicate path")
    for value in result:
        _require_relative_path(value)
    return result


def _normalize_diagnostics(values: Sequence[str]) -> list[str]:
    _require(len(values) <= 32, "too many diagnostics")
    result = list(values)
    for value in result:
        _require_stable_code(value)
    return result


def _normalize_next_signals(values: Sequence[str]) -> list[str]:
    _require(len(values) <= 16, "too many next signals")
    result = list(values)
    for value in result:
        _require(value in _NEXT_MODES, "unknown next signal")
    return result


def _normalize_usage(raw: Mapping[str, Any]) -> dict[str, Any]:
    allowed = {"input_tokens", "output_tokens", "currency", "cost"}
    _require(not (set(raw) - allowed), "unknown usage field")
    usage = copy.deepcopy(dict(raw))
    for key in ("input_tokens", "output_tokens"):
        if key in usage:
            _require(
                isinstance(usage[key], int) and usage[key] >= 0,
                "invalid token usage",
            )
    if "currency" in usage:
        _require(
            isinstance(usage["currency"], str)
            and re.fullmatch(r"[A-Z]{3}", usage["currency"]),
            "invalid usage currency",
        )
    if "cost" in usage:
        _require(
            isinstance(usage["cost"], (int, float)) and usage["cost"] >= 0,
            "invalid usage cost",
        )
    return usage


def _normalize_ids(values: Sequence[Any], limit: int) -> list[str]:
    _require(len(values) <= limit, "too many identifiers")
    result = [str(value) for value in values]
    _require(len(result) == len(set(result)), "duplicate identifier")
    for value in result:
        _require_id(value)
    return result


def _replace_json(path: Path, data: Mapping[str, Any]) -> None:
    encoded = _encoded_json(data)
    temporary = _write_temporary(path.parent, path.name, encoded)
    try:
        os.replace(temporary, path)
    except Exception:
        _safe_unlink(temporary)
        raise


def _publish_new_json(path: Path, data: Mapping[str, Any]) -> None:
    encoded = _encoded_json(data)
    temporary = _write_temporary(path.parent, path.name, encoded)
    try:
        os.link(temporary, path)
        _safe_unlink(temporary)
    except Exception:
        _safe_unlink(temporary)
        raise


def _write_temporary(parent: Path, name: str, encoded: bytes) -> Path:
    parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw = tempfile.mkstemp(prefix=f".{name}.", suffix=".tmp", dir=parent)
    path = Path(raw)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
    except Exception:
        _safe_unlink(path)
        raise
    return path


def _encoded_json(data: Mapping[str, Any]) -> bytes:
    encoded = (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if len(encoded) > MAX_RECORD_BYTES:
        raise RuntimeStateError(
            f"runtime record exceeds {MAX_RECORD_BYTES} serialized bytes"
        )
    return encoded


def _prune_runs(directory: Path) -> None:
    now = datetime.now(timezone.utc).timestamp()
    candidates = [
        path
        for path in directory.glob("*.json")
        if path.is_file() and not path.name.startswith(".")
    ]
    for path in candidates:
        try:
            if now - path.stat().st_mtime > MAX_RUN_AGE.total_seconds():
                path.unlink()
        except FileNotFoundError:
            continue
    remaining = sorted(
        (
            path
            for path in directory.glob("*.json")
            if path.is_file() and not path.name.startswith(".")
        ),
        key=lambda item: (item.stat().st_mtime, item.name),
    )
    total = sum(path.stat().st_size for path in remaining)
    while len(remaining) > MAX_RUN_COUNT or total > MAX_RUN_BYTES:
        oldest = remaining.pop(0)
        try:
            size = oldest.stat().st_size
            oldest.unlink()
            total -= size
        except FileNotFoundError:
            continue


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex}"


def _utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )


def _utc_basic() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def _require_id(value: Any) -> None:
    _require(isinstance(value, str) and _ID.fullmatch(value) is not None, "invalid ID")


def _require_nullable_id(value: Any) -> None:
    if value is not None:
        _require_id(value)


def _require_stable_code(value: Any) -> None:
    _require(
        isinstance(value, str)
        and len(value) <= 64
        and _STABLE_CODE.fullmatch(value) is not None,
        "invalid stable diagnostic code",
    )


def _require_relative_path(value: Any) -> None:
    _require(isinstance(value, str) and 0 < len(value) <= 512, "invalid relative path")
    path = Path(value)
    _require(
        not path.is_absolute()
        and ".." not in path.parts
        and all(re.fullmatch(r"[A-Za-z0-9._-]+", part) for part in path.parts),
        "invalid relative path",
    )


def _safe_unlink(path: Path | None) -> None:
    if path is None:
        return
    with suppress(FileNotFoundError):
        path.unlink()


def _require(condition: object, message: str) -> None:
    if not condition:
        raise RuntimeStateError(message)
