"""Collect and validate semantic classifications from repository carriers."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from .diagnostics import Diagnostic
from .frontmatter import FrontmatterError
from .frontmatter import metadata as frontmatter_metadata
from .identity import iter_control_files, logical_part
from .layout import discover_layout
from .legacy_authority import legacy_shared_package_paths
from .semantic_type_model import (
    FIELD_CLASSIFICATION,
    LEGACY_INTAKE_CLASSIFICATION,
    SEMANTIC_ID_KINDS,
    SEMANTIC_SUBTYPES,
    classify_semantic_id,
    normalize_semantic_classification,
    semantic_id_kind,
)
from .structured_data import StructuredDataError, load

# DECISION_ID_RE extracts legacy Decision IDs from Markdown carriers.
DECISION_ID_RE: Final[re.Pattern[str]] = re.compile(
    r"-\s*\*\*Decision ID:\*\*\s*`([^`]+)`"
)
# STATUS_RE extracts legacy Decision status labels.
STATUS_RE: Final[re.Pattern[str]] = re.compile(r"-\s*\*\*Status:\*\*\s*([^\n]+)")
# IGNORED_PARTS excludes generated, dependency, and template trees.
IGNORED_PARTS: Final[frozenset[str]] = frozenset(
    {
        ".git",
        ".cache",
        ".venv",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "__pycache__",
        "dist",
        "templates",
    }
)


@dataclass
class _Classification:
    """Aggregate every carrier that asserts one semantic identity."""

    semantic_id: str
    semantic_type: str
    subtype: str | None
    carriers: set[str]
    origins: set[str]
    statuses: set[str]
    modern: bool


def build_semantic_classification_index(root: Path) -> list[dict[str, Any]]:
    """Build a deterministic semantic classification index."""
    root = root.resolve()
    records, diagnostics = _collect(root)
    if diagnostics:
        raise ValueError(diagnostics[0].message)
    rows = [_index_row(root, record) for record in records.values()]
    return sorted(rows, key=lambda item: str(item["id"]))


def validate_semantic_classifications(root: Path) -> list[Diagnostic]:
    """Validate classifications without materializing an index."""
    _, diagnostics = _collect(root.resolve())
    return sorted(set(diagnostics))


def _index_row(
    root: Path,
    record: _Classification,
) -> dict[str, Any]:
    """Render one aggregate as a stable index row."""
    carriers = sorted(
        Path(carrier).relative_to(root).as_posix() for carrier in record.carriers
    )
    return {
        "id": record.semantic_id,
        "type": record.semantic_type,
        "subtype": record.subtype or "none",
        "historical_carrier": not record.modern,
        "origins": sorted(record.origins),
        "carriers": carriers,
        "carrier_statuses": sorted(record.statuses),
        "archived": any("archive" in Path(carrier).parts for carrier in carriers),
    }


def _collect(
    root: Path,
) -> tuple[dict[str, _Classification], list[Diagnostic]]:
    """Collect current and compatibility carriers into one identity map."""
    records: dict[str, _Classification] = {}
    diagnostics: list[Diagnostic] = []
    layout = discover_layout(root)
    _collect_markdown(root, layout.separated, records, diagnostics)
    if not layout.separated:
        _collect_packages(root, records, diagnostics)
    _collect_legacy_packages(root, records, diagnostics)
    _collect_intake(root, layout.recursive or layout.separated, records, diagnostics)
    return records, diagnostics


def _collect_markdown(
    root: Path,
    separated: bool,
    records: dict[str, _Classification],
    diagnostics: list[Diagnostic],
) -> None:
    """Collect atomic and legacy Decision Markdown carriers."""
    paths = (
        iter_control_files(root, "*.md") if separated else sorted(root.rglob("*.md"))
    )
    for path in paths:
        if _ignored(root, path):
            continue
        metadata = _frontmatter(path)
        if metadata and metadata.get("artifact_type") == "atomic_record":
            _collect_atom(path, metadata, records, diagnostics)
        else:
            _collect_legacy_decision(path, records, diagnostics)


def _collect_atom(
    path: Path,
    metadata: dict[str, Any],
    records: dict[str, _Classification],
    diagnostics: list[Diagnostic],
) -> None:
    """Register one modern atomic carrier when its identity is complete."""
    identifier = metadata.get("semantic_id")
    semantic_type = metadata.get("type")
    subtype = _normalized_subtype(metadata.get("subtype"))
    if not isinstance(identifier, str) or not isinstance(semantic_type, str):
        return
    classification = normalize_semantic_classification(semantic_type, subtype)
    _register(
        records,
        diagnostics,
        path,
        identifier,
        classification,
        origin="modern_atom",
        status=str(metadata.get("status", "unknown")),
        modern=(
            classification == (semantic_type, subtype)
            and SEMANTIC_ID_KINDS.get(classification) == semantic_id_kind(identifier)
        ),
    )


def _collect_legacy_decision(
    path: Path,
    records: dict[str, _Classification],
    diagnostics: list[Diagnostic],
) -> None:
    """Register a historical Decision document when its canonical ID is present."""
    if not (
        path.name.startswith("decision-")
        or (
            any(logical_part(part) == "decision" for part in path.parts)
            and path.name.startswith("DSET-DECISION-")
        )
    ):
        return
    text = path.read_text(encoding="utf-8")
    match = DECISION_ID_RE.search(text)
    if match is None:
        return
    status = STATUS_RE.search(text)
    _register(
        records,
        diagnostics,
        path,
        match.group(1),
        ("decision", None),
        origin="legacy_decision",
        status=status.group(1).strip() if status else "unknown",
        modern=False,
    )


def _collect_packages(
    root: Path,
    records: dict[str, _Classification],
    diagnostics: list[Diagnostic],
) -> None:
    """Collect package claims from pre-separated project storage."""
    layout = discover_layout(root)
    sources: list[tuple[Path, dict[str, Any]]] = []
    for path in layout.structured_named_files(root, "package"):
        data = _safe_load(path, diagnostics)
        if isinstance(data, dict):
            sources.append((path, data))
    for path, data in sources:
        if not _ignored(root, path):
            _collect_package_fields(path, data, "package", records, diagnostics)


def _collect_legacy_packages(
    root: Path,
    records: dict[str, _Classification],
    diagnostics: list[Diagnostic],
) -> None:
    """Collect sealed compatibility claims from historical package carriers."""
    for path in legacy_shared_package_paths(root):
        data = _safe_load(path, diagnostics)
        if isinstance(data, dict):
            _collect_package_fields(path, data, "legacy_package", records, diagnostics)


def _collect_package_fields(
    path: Path,
    data: dict[str, Any],
    origin: str,
    records: dict[str, _Classification],
    diagnostics: list[Diagnostic],
) -> None:
    """Register the classified list fields of one package carrier."""
    for field, classification in FIELD_CLASSIFICATION.items():
        values = data.get(field, [])
        if not isinstance(values, list):
            continue
        for identifier in values:
            if isinstance(identifier, str):
                _register(
                    records,
                    diagnostics,
                    path,
                    identifier,
                    classification,
                    origin=f"{origin}:{field}",
                    status="historical" if origin == "legacy_package" else "defined",
                    modern=False,
                )


def _collect_intake(
    root: Path,
    embedded: bool,
    records: dict[str, _Classification],
    diagnostics: list[Diagnostic],
) -> None:
    """Collect legacy intake rows only for layouts that still own an intake file."""
    try:
        path = discover_layout(root).intake_path
    except ValueError:
        path = root / "dset/intake.yaml"
    data = _safe_load(path, diagnostics) if path.is_file() and not embedded else None
    items = data.get("items", []) if isinstance(data, dict) else []
    if not isinstance(items, list):
        return
    for item in items:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            _collect_intake_item(path, item, records, diagnostics)


def _collect_intake_item(
    path: Path,
    item: dict[str, Any],
    records: dict[str, _Classification],
    diagnostics: list[Diagnostic],
) -> None:
    """Translate and register one compatibility intake row."""
    raw_type = item.get("type")
    subtype = _normalized_subtype(item.get("subtype"))
    if raw_type in SEMANTIC_SUBTYPES:
        classification = normalize_semantic_classification(str(raw_type), subtype)
    else:
        classification = LEGACY_INTAKE_CLASSIFICATION.get(str(raw_type))
    if classification is None:
        diagnostics.append(
            Diagnostic(
                "DSET-E166", path, f"intake semantic type is not recognized: {raw_type}"
            )
        )
        return
    _register(
        records,
        diagnostics,
        path,
        str(item["id"]),
        classification,
        origin="intake_compatibility",
        status=str(item.get("status", "unknown")),
        modern=False,
    )


def _register(
    records: dict[str, _Classification],
    diagnostics: list[Diagnostic],
    path: Path,
    identifier: str,
    classification: tuple[str, str | None],
    *,
    origin: str,
    status: str,
    modern: bool,
) -> None:
    """Validate and merge one semantic assertion."""
    if not _valid_classification(classification):
        diagnostics.append(
            Diagnostic("DSET-E166", path, f"invalid flat classification: {identifier}")
        )
        return
    if classify_semantic_id(identifier) != classification:
        diagnostics.append(
            Diagnostic(
                "DSET-E166",
                path,
                f"semantic ID kind disagrees with carrier classification: {identifier}",
            )
        )
        return
    existing = records.get(identifier)
    if existing is None:
        records[identifier] = _new_record(
            path, identifier, classification, origin, status, modern
        )
        return
    _merge_record(existing, path, classification, origin, status, modern, diagnostics)


def _valid_classification(classification: tuple[str, str | None]) -> bool:
    """Return whether one Type and direct subtype belong to the flat model."""
    semantic_type, subtype = classification
    return semantic_type in SEMANTIC_SUBTYPES and (
        subtype is None or subtype in SEMANTIC_SUBTYPES[semantic_type]
    )


def _new_record(
    path: Path,
    identifier: str,
    classification: tuple[str, str | None],
    origin: str,
    status: str,
    modern: bool,
) -> _Classification:
    """Create the first aggregate for one semantic identity."""
    semantic_type, subtype = classification
    return _Classification(
        identifier,
        semantic_type,
        subtype,
        {path.as_posix()},
        {origin},
        {status},
        modern,
    )


def _merge_record(
    record: _Classification,
    path: Path,
    classification: tuple[str, str | None],
    origin: str,
    status: str,
    modern: bool,
    diagnostics: list[Diagnostic],
) -> None:
    """Merge a compatible carrier or report conflicting classification."""
    if (record.semantic_type, record.subtype) != classification:
        diagnostics.append(
            Diagnostic(
                "DSET-E166",
                path,
                f"semantic carriers disagree on Type/subtype: {record.semantic_id}",
            )
        )
        return
    record.carriers.add(path.as_posix())
    record.origins.add(origin)
    record.statuses.add(status)
    record.modern = record.modern or modern


def _ignored(root: Path, path: Path) -> bool:
    """Return whether a carrier belongs to generated or dependency storage."""
    relative = path.relative_to(root)
    return (
        relative.parts[:1] == (".dset_runtime",)
        or relative.parts[:2] == (".dset", "runtime")
        or any(logical_part(part) in IGNORED_PARTS for part in relative.parts)
    )


def _normalized_subtype(value: object) -> str | None:
    """Normalize absent subtype markers to the empty direct subtype."""
    return None if value is None or value == "none" else str(value)


def _frontmatter(path: Path) -> dict[str, Any] | None:
    """Read TOML or compatibility frontmatter without aborting collection."""
    try:
        data = frontmatter_metadata(path)
    except (OSError, UnicodeError, FrontmatterError):
        return None
    return data if isinstance(data, dict) else None


def _safe_load(path: Path, diagnostics: list[Diagnostic]) -> Any:
    """Load a structured carrier and convert parser failures to diagnostics."""
    try:
        return load(path)
    except (OSError, UnicodeError, StructuredDataError) as error:
        diagnostics.append(
            Diagnostic("DSET-E166", path, f"cannot classify carrier: {error}")
        )
        return None
