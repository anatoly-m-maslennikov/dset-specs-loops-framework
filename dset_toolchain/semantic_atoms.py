from __future__ import annotations

import hashlib
import re
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .diagnostics import Diagnostic
from .layout import discover_layout
from .legacy_authority import validate_legacy_authority_ledger
from .semantic_types import SEMANTIC_ID_KINDS, SEMANTIC_SUBTYPES
from .settings import load_project_settings
from .yaml_subset import YamlSubsetError, dump, load, loads

ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")
SESSION_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*:[A-Za-z0-9._:-]+$")
EVENTS = frozenset(
    {
        "accepted",
        "answered",
        "absorbed",
        "confirmed",
        "priority_changed",
        "reopened",
        "rejected",
        "resolved",
        "retired",
        "withdrawn",
    }
)
TERMINAL_STATES = frozenset({"absorbed", "rejected", "retired", "withdrawn"})
REOPENABLE_STATES = frozenset({"answered", "confirmed", "resolved"})


@dataclass(frozen=True)
class SemanticAtom:
    semantic_id: str
    carrier_id: str
    path: str
    semantic_type: str
    subtype: str | None
    emission_status: str
    priority: str
    llm_session_ids: tuple[str, ...]
    child_of: tuple[str, ...]
    sha256: str


def collect_semantic_atoms(
    root: Path,
) -> tuple[dict[str, SemanticAtom], list[Diagnostic]]:
    root = root.resolve()
    atoms: dict[str, SemanticAtom] = {}
    diagnostics: list[Diagnostic] = []
    settings, _ = load_project_settings(root)
    allowed_priorities = {*settings.priority_scale, "unknown"}
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if _ignored(relative) or "templates" in relative.parts:
            continue
        metadata = _frontmatter(path)
        if metadata is None or metadata.get("artifact_type") != "atomic_record":
            continue
        atom, issues = _parse_atom(root, path, metadata, allowed_priorities)
        diagnostics.extend(issues)
        if atom is None:
            continue
        previous = atoms.get(atom.semantic_id)
        if previous is not None:
            diagnostics.append(
                Diagnostic(
                    "DSET-E159",
                    path,
                    f"duplicate semantic atom ID: {atom.semantic_id}",
                )
            )
            continue
        atoms[atom.semantic_id] = atom
    return atoms, diagnostics


def validate_semantic_atoms(root: Path) -> list[Diagnostic]:
    atoms, diagnostics = collect_semantic_atoms(root)
    diagnostics.extend(
        _validate_lifecycle(
            root,
            _known_semantic_ids(root, atoms),
            {identifier: atom.emission_status for identifier, atom in atoms.items()},
        )
    )
    diagnostics.extend(_validate_ledger(root, atoms))
    diagnostics.extend(validate_legacy_authority_ledger(root))
    return sorted(set(diagnostics))


def seal_atom(root: Path, path: Path) -> Path:
    root = root.resolve()
    path = path.resolve()
    try:
        path.relative_to(root)
    except ValueError as error:
        raise ValueError("atom carrier must be inside the repository") from error
    metadata = _frontmatter(path)
    settings, issues = load_project_settings(root)
    if issues:
        raise ValueError("project settings must pass before sealing an atom")
    if metadata is None:
        raise ValueError("atom carrier requires YAML frontmatter")
    atom, diagnostics = _parse_atom(
        root, path, metadata, {*settings.priority_scale, "unknown"}
    )
    if diagnostics or atom is None:
        message = diagnostics[0].message if diagnostics else "invalid atom"
        raise ValueError(message)
    from .artifact_emission import assess_artifact_candidate

    candidate = {
        "authority": metadata.get("authority"),
        "claim": metadata.get("claim"),
        "type": metadata.get("type"),
        "subtype": metadata.get("subtype"),
        "scope": metadata.get("scope"),
        "llm_session_ids": metadata.get("llm_session_ids"),
        "material_links": metadata.get("child_of", []),
        "priority": metadata.get("priority"),
        "acceptance": metadata.get("status"),
        "promotion": metadata.get("promotion"),
    }
    for field in (
        "boundary",
        "lineage",
        "conflict_state",
        "verification_obligation",
        "unknowns",
    ):
        if field in metadata:
            candidate[field] = metadata[field]
    assessment = assess_artifact_candidate(root, candidate)
    if assessment["emission_allowed"] is not True:
        first = assessment["diagnostics"][0]
        raise ValueError(f"artifact emission is blocked: {first['message']}")
    ledger_path = _ledger_path(root)
    data = _load_or_empty(ledger_path, "records")
    records = data["records"]
    assert isinstance(records, list)
    if any(
        isinstance(item, dict) and item.get("semantic_id") == atom.semantic_id
        for item in records
    ):
        raise FileExistsError(f"atom is already sealed: {atom.semantic_id}")
    records.append(_ledger_record(atom))
    records.sort(key=lambda item: str(item.get("semantic_id", "")))
    _atomic_dump(ledger_path, data)
    return ledger_path


def append_lifecycle_event(root: Path, event: dict[str, Any]) -> Path:
    root = root.resolve()
    atoms, diagnostics = collect_semantic_atoms(root)
    if diagnostics:
        raise ValueError(diagnostics[0].message)
    known_ids = _known_semantic_ids(root, atoms)
    normalized = _validate_event(root, event, known_ids)
    lifecycle_path = _lifecycle_path(root)
    data = _load_or_empty(lifecycle_path, "events")
    events = data["events"]
    assert isinstance(events, list)
    event_id = normalized["id"]
    if any(isinstance(item, dict) and item.get("id") == event_id for item in events):
        raise FileExistsError(f"lifecycle event already exists: {event_id}")
    events.append(normalized)
    _validate_event_graph(
        events,
        {identifier: atom.emission_status for identifier, atom in atoms.items()},
    )
    _atomic_dump(lifecycle_path, data)
    return lifecycle_path


def effective_priority(root: Path, atom: SemanticAtom) -> tuple[str, str]:
    lifecycle_path = _lifecycle_path(root)
    if lifecycle_path.is_file():
        data = load(lifecycle_path)
        events = data.get("events", []) if isinstance(data, dict) else []
        changes = [
            item
            for item in events
            if isinstance(item, dict)
            and item.get("atom_id") == atom.semantic_id
            and item.get("event") == "priority_changed"
        ]
        if changes:
            latest = changes[-1]
            return str(latest["priority"]), f"lifecycle:{latest['id']}"
    if atom.priority == "unknown":
        return "unknown", f"atom:{atom.semantic_id}"
    return atom.priority, f"atom:{atom.semantic_id}"


def build_semantic_atom_index(root: Path) -> list[dict[str, Any]]:
    """Build current atom/lifecycle/priority/archive lookup for derived views."""
    atoms, diagnostics = collect_semantic_atoms(root)
    if diagnostics:
        raise ValueError(diagnostics[0].message)
    events = _lifecycle_events(root)
    rows: list[dict[str, Any]] = []
    for atom in atoms.values():
        atom_events = [
            event for event in events if event.get("atom_id") == atom.semantic_id
        ]
        priority, priority_source = effective_priority(root, atom)
        absorbed_by = [
            str(event["related"][0])
            for event in atom_events
            if event.get("event") == "absorbed"
            and isinstance(event.get("related"), list)
            and event["related"]
        ]
        rows.append(
            {
                "id": atom.semantic_id,
                "carrier_id": atom.carrier_id,
                "path": atom.path,
                "sha256": atom.sha256,
                "type": atom.semantic_type,
                "subtype": atom.subtype or "none",
                "emission_status": atom.emission_status,
                "current_status": _current_status(atom, atom_events),
                "priority": priority,
                "priority_source": priority_source,
                "child_of": list(atom.child_of),
                "lifecycle_events": [str(event["id"]) for event in atom_events],
                "absorbed_by": absorbed_by,
                "archived": "archive" in Path(atom.path).parts,
            }
        )
    return sorted(rows, key=lambda item: str(item["id"]))


def archive_atom(root: Path, semantic_id: str) -> Path:
    """Move a fully retired atom byte-for-byte and update canonical lookup."""
    root = root.resolve()
    atoms, diagnostics = collect_semantic_atoms(root)
    if diagnostics:
        raise ValueError(diagnostics[0].message)
    atom = atoms.get(semantic_id)
    if atom is None:
        raise ValueError(f"unknown semantic atom: {semantic_id}")
    source = root / atom.path
    if "archive" in source.relative_to(root).parts:
        raise ValueError(f"semantic atom is already archived: {semantic_id}")
    events = _lifecycle_events(root)
    atom_events = [event for event in events if event.get("atom_id") == semantic_id]
    if _current_status(atom, atom_events) != "retired":
        raise ValueError("semantic atom must be explicitly retired before archival")
    active_dependants = [
        candidate.semantic_id
        for candidate in atoms.values()
        if semantic_id in candidate.child_of
        and _current_status(
            candidate,
            [
                event
                for event in events
                if event.get("atom_id") == candidate.semantic_id
            ],
        )
        not in {"absorbed", "rejected", "retired", "withdrawn"}
    ]
    if active_dependants:
        raise ValueError(
            "semantic atom has active child reliance: "
            + ", ".join(sorted(active_dependants))
        )

    destination = source.parent / "archive" / source.name
    if destination.exists():
        raise FileExistsError(f"atom archive destination exists: {destination}")
    ledger_path = _ledger_path(root)
    ledger = _load_or_empty(ledger_path, "records")
    records = ledger["records"]
    assert isinstance(records, list)
    record = next(
        (
            item
            for item in records
            if isinstance(item, dict) and item.get("semantic_id") == semantic_id
        ),
        None,
    )
    if record is None or record.get("sha256") != atom.sha256:
        raise ValueError("atom archive requires a current digest-bound ledger record")
    updated = dict(record)
    updated["path"] = destination.relative_to(root).as_posix()
    records[records.index(record)] = updated
    temporary = ledger_path.with_suffix(ledger_path.suffix + ".tmp")
    temporary.write_text(dump(ledger), encoding="utf-8")
    destination.parent.mkdir(parents=True, exist_ok=True)
    source.replace(destination)
    try:
        temporary.replace(ledger_path)
    except Exception:
        destination.replace(source)
        temporary.unlink(missing_ok=True)
        raise
    return destination


def _parse_atom(
    root: Path,
    path: Path,
    data: dict[str, Any],
    allowed_priorities: set[str],
) -> tuple[SemanticAtom | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    semantic_type = data.get("type")
    subtype = data.get("subtype")
    semantic_id = data.get("semantic_id")
    carrier_id = data.get("artifact_id")
    status = data.get("status")
    priority = data.get("priority")
    sessions = data.get("llm_session_ids")
    if semantic_type not in SEMANTIC_SUBTYPES:
        diagnostics.append(_atom_diag(path, "atom requires one of the four Types"))
    elif subtype is not None and subtype not in SEMANTIC_SUBTYPES[semantic_type]:
        diagnostics.append(_atom_diag(path, "atom has an invalid direct subtype"))
    elif semantic_type == "qa" and subtype not in {"test", "evaluation"}:
        diagnostics.append(_atom_diag(path, "QA atom requires test or evaluation"))
    if not isinstance(semantic_id, str) or not ID_PATTERN.fullmatch(semantic_id):
        diagnostics.append(_atom_diag(path, "atom requires a canonical semantic_id"))
    elif semantic_type in SEMANTIC_SUBTYPES:
        expected = SEMANTIC_ID_KINDS.get((semantic_type, subtype))
        segments = semantic_id.split("-")
        if expected is None or expected not in segments:
            diagnostics.append(
                _atom_diag(path, f"semantic_id must use the {expected} kind")
            )
    if not isinstance(carrier_id, str) or not ID_PATTERN.fullmatch(carrier_id):
        diagnostics.append(_atom_diag(path, "atom requires a canonical artifact_id"))
    if status not in {"proposed", "accepted"}:
        diagnostics.append(
            _atom_diag(path, "emission status must be proposed or accepted")
        )
    if priority not in allowed_priorities:
        diagnostics.append(_atom_diag(path, "atom priority is not in project scale"))
    if not _valid_sessions(sessions):
        diagnostics.append(
            _atom_diag(path, "atom requires unique host-prefixed llm_session_ids")
        )
    child_of = data.get("child_of", [])
    if child_of is None:
        child_of = []
    if not isinstance(child_of, list) or not all(
        isinstance(item, str) and ID_PATTERN.fullmatch(item) for item in child_of
    ):
        diagnostics.append(_atom_diag(path, "child_of must contain canonical IDs"))
        child_of = []
    if diagnostics:
        return None, diagnostics
    assert isinstance(semantic_id, str)
    assert isinstance(carrier_id, str)
    assert isinstance(semantic_type, str)
    assert isinstance(status, str)
    assert isinstance(priority, str)
    assert isinstance(sessions, list)
    return (
        SemanticAtom(
            semantic_id=semantic_id,
            carrier_id=carrier_id,
            path=path.relative_to(root).as_posix(),
            semantic_type=semantic_type,
            subtype=str(subtype) if subtype is not None else None,
            emission_status=status,
            priority=priority,
            llm_session_ids=tuple(str(item) for item in sessions),
            child_of=tuple(str(item) for item in child_of),
            sha256=_digest(path),
        ),
        diagnostics,
    )


def _validate_lifecycle(
    root: Path,
    known_ids: set[str],
    initial_statuses: dict[str, str],
) -> list[Diagnostic]:
    path = _lifecycle_path(root)
    if not path.is_file():
        return []
    try:
        data = load(path)
    except (OSError, UnicodeError, YamlSubsetError) as error:
        return [Diagnostic("DSET-E160", path, f"invalid lifecycle registry: {error}")]
    events = data.get("events") if isinstance(data, dict) else None
    if not isinstance(data, dict) or str(data.get("schema_version")) != "1.0":
        return [Diagnostic("DSET-E160", path, "lifecycle schema_version must be 1.0")]
    if not isinstance(events, list):
        return [Diagnostic("DSET-E160", path, "lifecycle events must be a list")]
    diagnostics: list[Diagnostic] = []
    seen: set[str] = set()
    normalized_events: list[dict[str, Any]] = []
    for event in events:
        try:
            normalized = _validate_event(root, event, known_ids)
        except ValueError as error:
            diagnostics.append(Diagnostic("DSET-E160", path, str(error)))
            continue
        normalized_events.append(normalized)
        event_id = str(normalized["id"])
        if event_id in seen:
            diagnostics.append(
                Diagnostic("DSET-E160", path, f"duplicate lifecycle event: {event_id}")
            )
        seen.add(event_id)
    try:
        _validate_event_graph(normalized_events, initial_statuses)
    except ValueError as error:
        diagnostics.append(Diagnostic("DSET-E160", path, str(error)))
    return diagnostics


def _validate_event(root: Path, event: object, known_ids: set[str]) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise ValueError("every lifecycle event must be a mapping")
    event_id = event.get("id")
    atom_id = event.get("atom_id")
    event_kind = event.get("event")
    allowed_fields = {
        "id",
        "atom_id",
        "event",
        "occurred_at",
        "priority",
        "related",
        "llm_session_ids",
        "rationale",
    }
    unknown_fields = sorted(set(event) - allowed_fields)
    if unknown_fields:
        raise ValueError(
            "lifecycle event has unknown fields: " + ", ".join(unknown_fields)
        )
    if not isinstance(event_id, str) or not re.fullmatch(
        r"[A-Z][A-Z0-9]*-LIFECYCLE-EVENT-[0-9]{3,}", event_id
    ):
        raise ValueError("lifecycle event requires a canonical ID")
    if not isinstance(atom_id, str) or atom_id not in known_ids:
        raise ValueError(f"lifecycle event has unresolved atom_id: {atom_id}")
    if event_kind not in EVENTS:
        raise ValueError(f"unknown lifecycle event: {event_kind}")
    occurred_at = event.get("occurred_at")
    try:
        observed = datetime.fromisoformat(str(occurred_at))
    except ValueError as error:
        raise ValueError("lifecycle event requires an ISO timestamp") from error
    if observed.tzinfo is None:
        raise ValueError("lifecycle event timestamp requires a timezone")
    if not _valid_sessions(event.get("llm_session_ids")):
        raise ValueError("lifecycle event requires valid llm_session_ids")
    related = event.get("related", [])
    if not isinstance(related, list) or not all(
        isinstance(item, str) and ID_PATTERN.fullmatch(item) for item in related
    ):
        raise ValueError("lifecycle related IDs must be canonical")
    if event_kind == "absorbed" and (len(related) != 1 or related[0] not in known_ids):
        raise ValueError("absorbed event requires one resolving atom")
    if event_kind == "priority_changed":
        settings, _ = load_project_settings(root)
        if event.get("priority") not in settings.priority_scale:
            raise ValueError("priority_changed requires a project priority value")
    elif "priority" in event:
        raise ValueError("priority is valid only for priority_changed events")
    rationale = event.get("rationale")
    if rationale is not None and (
        not isinstance(rationale, str) or not 1 <= len(rationale) <= 4096
    ):
        raise ValueError("lifecycle rationale must be non-empty and bounded")
    return dict(event)


def _validate_event_graph(
    events: Sequence[object], initial_statuses: dict[str, str] | None = None
) -> None:
    edges: dict[str, str] = {}
    states = dict(initial_statuses or {})
    explicit_acceptance: set[str] = set()
    for event in events:
        if not isinstance(event, dict):
            continue
        atom_id = str(event.get("atom_id"))
        event_kind = str(event.get("event"))
        state = states.get(atom_id, "accepted")
        if event_kind == "absorbed" and atom_id in edges:
            raise ValueError(f"atom has multiple absorption successors: {atom_id}")
        if state in TERMINAL_STATES:
            raise ValueError(
                f"terminal atom {atom_id} cannot transition from {state} "
                f"through {event_kind}"
            )
        if event_kind == "priority_changed":
            continue
        if event_kind == "accepted":
            if state == "proposed" or (
                state == "accepted" and atom_id not in explicit_acceptance
            ):
                states[atom_id] = "accepted"
            else:
                raise ValueError(
                    f"atom {atom_id} cannot transition from {state} through accepted"
                )
            explicit_acceptance.add(atom_id)
            continue
        if event_kind == "reopened":
            if state not in REOPENABLE_STATES:
                raise ValueError(
                    f"atom {atom_id} cannot transition from {state} through reopened"
                )
            states[atom_id] = "reopened"
            continue
        if event_kind in {"answered", "confirmed", "resolved"}:
            if state not in {"accepted", "reopened"}:
                raise ValueError(
                    f"atom {atom_id} cannot transition from {state} "
                    f"through {event_kind}"
                )
            states[atom_id] = event_kind
            continue
        if event_kind in {"rejected", "withdrawn"}:
            if state not in {"proposed", "accepted", "reopened"}:
                raise ValueError(
                    f"atom {atom_id} cannot transition from {state} "
                    f"through {event_kind}"
                )
            states[atom_id] = event_kind
            continue
        if event_kind in {"absorbed", "retired"}:
            if state not in {
                "accepted",
                "answered",
                "confirmed",
                "reopened",
                "resolved",
            }:
                raise ValueError(
                    f"atom {atom_id} cannot transition from {state} "
                    f"through {event_kind}"
                )
            states[atom_id] = event_kind
        if event_kind != "absorbed":
            continue
        related = event.get("related")
        if isinstance(related, list) and len(related) == 1:
            edges[atom_id] = str(related[0])
    for start in edges:
        seen: set[str] = set()
        current = start
        while current in edges:
            if current in seen:
                raise ValueError(f"atom absorption cycle includes {current}")
            seen.add(current)
            current = edges[current]


def _known_semantic_ids(root: Path, atoms: dict[str, SemanticAtom]) -> set[str]:
    identifiers = set(atoms)
    layout = discover_layout(root)
    if layout.intake_path.is_file():
        data = load(layout.intake_path)
        items = data.get("items", []) if isinstance(data, dict) else []
        identifiers.update(
            str(item["id"])
            for item in items
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        )
    for path in sorted(root.rglob("decision-*.md")):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"-\s*\*\*Decision ID:\*\*\s*`([^`]+)`", text)
        if match:
            identifiers.add(match.group(1))
    for path in sorted(root.rglob("package.yaml")):
        try:
            data = load(path)
        except (OSError, UnicodeError, YamlSubsetError):
            continue
        if not isinstance(data, dict):
            continue
        fields = (
            "requirements",
            "tests",
            "evals",
            "contracts",
            "stories",
            "outcomes",
        )
        for field in fields:
            values = data.get(field, [])
            if isinstance(values, list):
                identifiers.update(
                    str(item) for item in values if isinstance(item, str)
                )
    return identifiers


def _validate_ledger(root: Path, atoms: dict[str, SemanticAtom]) -> list[Diagnostic]:
    path = _ledger_path(root)
    if not path.is_file():
        if atoms:
            return [Diagnostic("DSET-E161", path, "semantic atom ledger is missing")]
        return []
    try:
        data = load(path)
    except (OSError, UnicodeError, YamlSubsetError) as error:
        return [Diagnostic("DSET-E161", path, f"invalid atom ledger: {error}")]
    records = data.get("records") if isinstance(data, dict) else None
    if not isinstance(data, dict) or str(data.get("schema_version")) != "1.0":
        return [Diagnostic("DSET-E161", path, "atom ledger schema_version must be 1.0")]
    if not isinstance(records, list):
        return [Diagnostic("DSET-E161", path, "atom ledger records must be a list")]
    diagnostics: list[Diagnostic] = []
    indexed: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict) or not isinstance(
            record.get("semantic_id"), str
        ):
            diagnostics.append(Diagnostic("DSET-E161", path, "invalid ledger record"))
            continue
        identifier = str(record["semantic_id"])
        if identifier in indexed:
            diagnostics.append(
                Diagnostic("DSET-E161", path, f"duplicate ledger atom: {identifier}")
            )
        indexed[identifier] = record
    for identifier, atom in atoms.items():
        record = indexed.get(identifier)
        if record is None:
            diagnostics.append(
                Diagnostic("DSET-E161", root / atom.path, "emitted atom is not sealed")
            )
            continue
        expected = _ledger_record(atom)
        for field in ("carrier_id", "path", "sha256", "type", "subtype"):
            if record.get(field) != expected.get(field):
                diagnostics.append(
                    Diagnostic(
                        "DSET-E161",
                        root / atom.path,
                        f"sealed atom {field} changed: {identifier}",
                    )
                )
    for identifier in sorted(set(indexed) - set(atoms)):
        record_path = indexed[identifier].get("path")
        if not isinstance(record_path, str) or not (root / record_path).is_file():
            diagnostics.append(
                Diagnostic("DSET-E161", path, f"sealed atom is missing: {identifier}")
            )
    return diagnostics


def _lifecycle_events(root: Path) -> list[dict[str, Any]]:
    path = _lifecycle_path(root)
    if not path.is_file():
        return []
    data = load(path)
    values = data.get("events", []) if isinstance(data, dict) else []
    return [item for item in values if isinstance(item, dict)]


def _current_status(atom: SemanticAtom, events: list[dict[str, Any]]) -> str:
    status = atom.emission_status
    for event in events:
        kind = event.get("event")
        if kind == "priority_changed":
            continue
        if kind == "accepted":
            status = "accepted"
        elif isinstance(kind, str):
            status = kind
    return status


def _ledger_record(atom: SemanticAtom) -> dict[str, Any]:
    return {
        "semantic_id": atom.semantic_id,
        "carrier_id": atom.carrier_id,
        "path": atom.path,
        "sha256": atom.sha256,
        "type": atom.semantic_type,
        "subtype": atom.subtype if atom.subtype is not None else "none",
    }


def _load_or_empty(path: Path, field: str) -> dict[str, Any]:
    if not path.is_file():
        return {"schema_version": "1.0", field: []}
    data = load(path)
    if not isinstance(data, dict) or str(data.get("schema_version")) != "1.0":
        raise ValueError(f"invalid registry: {path}")
    values = data.get(field)
    if not isinstance(values, list):
        raise ValueError(f"registry field must be a list: {field}")
    return data


def _atomic_dump(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(dump(data), encoding="utf-8")
    temporary.replace(path)


def _frontmatter(path: Path) -> dict[str, Any] | None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return None
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = lines.index("---", 1)
        data = loads("\n".join(lines[1:end]))
    except (ValueError, YamlSubsetError):
        return None
    return data if isinstance(data, dict) else None


def _valid_sessions(value: object) -> bool:
    return (
        isinstance(value, list)
        and len(value) == len(set(str(item) for item in value))
        and all(
            isinstance(item, str) and SESSION_PATTERN.fullmatch(item) for item in value
        )
    )


def _ignored(relative: Path) -> bool:
    ignored = {".git", ".cache", ".venv", "__pycache__", "dist", ".dset"}
    return any(
        part in ignored or (part.startswith(".") and part != ".github")
        for part in relative.parts
    )


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ledger_path(root: Path) -> Path:
    return discover_layout(root).governance_root / "atoms.yaml"


def _lifecycle_path(root: Path) -> Path:
    return discover_layout(root).governance_root / "lifecycle.yaml"


def _atom_diag(path: Path, message: str) -> Diagnostic:
    return Diagnostic("DSET-E159", path, message)
