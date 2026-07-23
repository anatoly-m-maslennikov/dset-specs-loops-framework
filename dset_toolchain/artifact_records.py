"""Collect and validate routed atomic artifact records."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .artifact_routing import ArtifactRoute, parse_artifact_route, route_issues
from .diagnostics import Diagnostic
from .frontmatter import FrontmatterError
from .frontmatter import metadata as frontmatter_metadata
from .identity import has_logical_part, iter_control_files
from .layout import discover_layout
from .lineage import ArtifactRelation, parse_authored_relations
from .settings import load_project_settings

# ARTIFACT_ID validates stable persisted identities without assigning semantics.
ARTIFACT_ID = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")
# SESSION_ID validates explicit provider/session provenance.
SESSION_ID = re.compile(r"^[a-z][a-z0-9_-]*:[A-Za-z0-9._:-]+$")
# ROUTE_FIELDS identify a carrier that opts into routed governance.
ROUTE_FIELDS = frozenset(
    {
        "revision_mode",
        "content_role",
        "governance_origin",
        "relation_shape",
        "scope_path",
    }
)


@dataclass(frozen=True)
class AtomicArtifactRecord:
    """Represent one routed immutable artifact without a Type taxonomy."""

    semantic_id: str
    carrier_id: str
    path: str
    route: ArtifactRoute
    status: str
    priority: str
    llm_session_ids: tuple[str, ...]
    relations: tuple[ArtifactRelation, ...]
    sha256: str

    def as_index_row(self) -> dict[str, Any]:
        """Render the route-first lookup record used by project tooling."""
        archived = "archive" in Path(self.path).parts
        return {
            "id": self.semantic_id,
            "carrier_id": self.carrier_id,
            "carrier": Path(self.path).name,
            "sha256": self.sha256,
            "route": self.route.as_dict(),
            "status": "archived" if archived else self.status,
            "priority": self.priority,
            "relations": [relation.as_dict() for relation in self.relations],
            "archived": archived,
        }


def collect_atomic_artifact_records(
    root: Path,
) -> tuple[dict[str, AtomicArtifactRecord], list[Diagnostic]]:
    """Collect all project-owned atomic carriers through explicit routes."""
    root = root.resolve()
    settings, settings_issues = load_project_settings(root)
    if settings_issues:
        return {}, [
            Diagnostic("DSET-E169", root / ".dset/dset_settings.toml", issue)
            for issue in settings_issues
        ]
    priorities = {*settings.priority_scale, "unknown"}
    records: dict[str, AtomicArtifactRecord] = {}
    carrier_ids: set[str] = set()
    diagnostics: list[Diagnostic] = []
    for path in iter_control_files(root, "*.md"):
        relative = path.relative_to(root)
        if has_logical_part(relative, {"templates", "methodology"}):
            continue
        metadata = _metadata(path)
        if metadata is None or not _is_atomic_candidate(metadata):
            continue
        record, issues = _parse_record(root, path, metadata, priorities)
        diagnostics.extend(issues)
        if record is None:
            continue
        if record.semantic_id in records:
            diagnostics.append(
                Diagnostic(
                    "DSET-E170",
                    path,
                    f"duplicate atomic semantic identity: {record.semantic_id}",
                )
            )
            continue
        if record.carrier_id in carrier_ids:
            diagnostics.append(
                Diagnostic(
                    "DSET-E170",
                    path,
                    f"duplicate atomic carrier identity: {record.carrier_id}",
                )
            )
            continue
        records[record.semantic_id] = record
        carrier_ids.add(record.carrier_id)
    return records, diagnostics


def validate_atomic_artifact_routes(root: Path) -> list[Diagnostic]:
    """Return route and identity diagnostics for persisted atomic artifacts."""
    _records, diagnostics = collect_atomic_artifact_records(root)
    return sorted(set(diagnostics))


def build_atomic_artifact_route_index(root: Path) -> list[dict[str, Any]]:
    """Build a stable route-first index without semantic Type fields."""
    records, diagnostics = collect_atomic_artifact_records(root)
    if diagnostics:
        raise ValueError(diagnostics[0].message)
    return sorted(
        (record.as_index_row() for record in records.values()),
        key=lambda row: str(row["id"]),
    )


def seal_atom(root: Path, path: Path) -> Path:
    """Validate one newly emitted route-first atom without a separate ledger."""
    root = root.resolve()
    path = path.resolve()
    try:
        path.relative_to(root)
    except ValueError as error:
        raise ValueError("atomic carrier must be inside the repository") from error
    metadata = _metadata(path)
    if metadata is None:
        raise ValueError("atomic carrier requires TOML frontmatter")
    settings, setting_issues = load_project_settings(root)
    if setting_issues:
        raise ValueError("project settings must pass before sealing an atom")
    record, diagnostics = _parse_record(
        root,
        path,
        metadata,
        {*settings.priority_scale, "unknown"},
    )
    if diagnostics or record is None:
        raise ValueError(
            diagnostics[0].message if diagnostics else "invalid atomic carrier"
        )

    from .artifact_emission import assess_artifact_candidate

    candidate = dict(metadata)
    candidate["acceptance"] = metadata.get("status")
    candidate["material_links"] = [
        relation.target
        for relation in record.relations
        if relation.target is not None
    ]
    assessment = assess_artifact_candidate(root, candidate)
    if assessment["emission_allowed"] is not True:
        first = assessment["diagnostics"][0]
        raise ValueError(f"artifact emission is blocked: {first['message']}")
    if not discover_layout(root).separated:
        raise ValueError("route-first atom sealing requires the separated control plane")
    return path


def archive_atom(root: Path, semantic_id: str) -> Path:
    """Move an inactive atom into the adjacent archive without changing bytes."""
    root = root.resolve()
    records, diagnostics = collect_atomic_artifact_records(root)
    if diagnostics:
        raise ValueError(diagnostics[0].message)
    record = records.get(semantic_id)
    if record is None:
        raise ValueError(f"unknown atomic artifact: {semantic_id}")
    source = root / record.path
    if "archive" in source.relative_to(root).parts:
        raise ValueError(f"atomic artifact is already archived: {semantic_id}")
    active_dependants = [
        candidate.semantic_id
        for candidate in records.values()
        if "archive" not in Path(candidate.path).parts
        and any(
            relation.target == semantic_id
            and relation.type in {"child_of", "override_of"}
            for relation in candidate.relations
        )
    ]
    if active_dependants:
        raise ValueError(
            "atomic artifact has active child reliance: "
            + ", ".join(sorted(active_dependants))
        )
    destination = source.parent / "archive" / source.name
    if destination.exists():
        raise FileExistsError(f"archive destination already exists: {source.name}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    source.replace(destination)
    return destination


def _parse_record(
    root: Path,
    path: Path,
    metadata: dict[str, Any],
    priorities: set[str],
) -> tuple[AtomicArtifactRecord | None, list[Diagnostic]]:
    diagnostics = [
        Diagnostic("DSET-E169", path, issue) for issue in route_issues(metadata)
    ]
    semantic_id = metadata.get("semantic_id")
    carrier_id = metadata.get("artifact_id")
    status = metadata.get("status")
    priority = metadata.get("priority")
    sessions = metadata.get("llm_session_ids")
    if metadata.get("revision_mode") != "atomic":
        diagnostics.append(
            Diagnostic("DSET-E169", path, "atomic carrier requires revision_mode atomic")
        )
    if not isinstance(semantic_id, str) or ARTIFACT_ID.fullmatch(semantic_id) is None:
        diagnostics.append(
            Diagnostic("DSET-E170", path, "atomic carrier requires semantic_id")
        )
    if not isinstance(carrier_id, str) or ARTIFACT_ID.fullmatch(carrier_id) is None:
        diagnostics.append(
            Diagnostic("DSET-E170", path, "atomic carrier requires artifact_id")
        )
    if status not in {"proposed", "accepted"}:
        diagnostics.append(
            Diagnostic("DSET-E170", path, "atomic status must be proposed or accepted")
        )
    if priority not in priorities:
        diagnostics.append(
            Diagnostic("DSET-E170", path, "atomic priority is not in project scale")
        )
    if not _valid_sessions(sessions):
        diagnostics.append(
            Diagnostic(
                "DSET-E170",
                path,
                "atomic carrier requires unique provider-prefixed llm_session_ids",
            )
        )
    relations = parse_authored_relations(path, metadata, diagnostics)
    if diagnostics:
        return None, diagnostics
    route = parse_artifact_route(metadata)
    assert isinstance(semantic_id, str)
    assert isinstance(carrier_id, str)
    assert isinstance(status, str)
    assert isinstance(priority, str)
    assert isinstance(sessions, list)
    return (
        AtomicArtifactRecord(
            semantic_id=semantic_id,
            carrier_id=carrier_id,
            path=path.relative_to(root).as_posix(),
            route=route,
            status=status,
            priority=priority,
            llm_session_ids=tuple(str(item) for item in sessions),
            relations=relations,
            sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        ),
        diagnostics,
    )


def _is_atomic_candidate(metadata: dict[str, Any]) -> bool:
    return (
        metadata.get("revision_mode") == "atomic"
        or metadata.get("artifact_type") == "atomic_record"
        or bool(ROUTE_FIELDS.intersection(metadata))
    )


def _metadata(path: Path) -> dict[str, Any] | None:
    try:
        value = frontmatter_metadata(path)
    except (OSError, UnicodeError, FrontmatterError):
        return None
    return value if isinstance(value, dict) else None


def _valid_sessions(value: object) -> bool:
    return (
        isinstance(value, list)
        and len(value) == len(set(str(item) for item in value))
        and all(
            isinstance(item, str) and SESSION_ID.fullmatch(item) for item in value
        )
    )
