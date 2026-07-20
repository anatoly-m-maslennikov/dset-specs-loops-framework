from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .diagnostics import Diagnostic
from .frontmatter import FrontmatterError
from .frontmatter import metadata as frontmatter_metadata
from .layout import discover_layout
from .yaml_subset import YamlSubsetError, load

SEMANTIC_SUBTYPES: dict[str, frozenset[str]] = {
    "decision": frozenset(
        {
            "requirement",
            "constraint",
            "contract",
            "user_story",
            "outcome",
            "scenario",
            "invariant",
        }
    ),
    "question": frozenset({"conflict", "risk", "opportunity"}),
    "problem": frozenset({"defect", "gap", "debt"}),
    "qa": frozenset({"test", "evaluation"}),
}
SEMANTIC_ID_KINDS: dict[tuple[str, str | None], str] = {
    ("decision", None): "DECISION",
    ("decision", "requirement"): "REQUIREMENT",
    ("decision", "constraint"): "CONSTRAINT",
    ("decision", "contract"): "CONTRACT",
    ("decision", "user_story"): "STORY",
    ("decision", "outcome"): "OUTCOME",
    ("decision", "scenario"): "SCENARIO",
    ("decision", "invariant"): "INVARIANT",
    ("question", None): "QUESTION",
    ("question", "conflict"): "CONFLICT",
    ("question", "risk"): "RISK",
    ("question", "opportunity"): "OPPORTUNITY",
    ("problem", None): "PROBLEM",
    ("problem", "defect"): "DEFECT",
    ("problem", "gap"): "GAP",
    ("problem", "debt"): "DEBT",
    ("qa", "test"): "TEST",
    ("qa", "evaluation"): "EVALUATION",
}
KIND_CLASSIFICATION = {
    kind: classification for classification, kind in SEMANTIC_ID_KINDS.items()
}
KIND_CLASSIFICATION["EVAL"] = ("qa", "evaluation")
FIELD_CLASSIFICATION: dict[str, tuple[str, str | None]] = {
    "requirements": ("decision", "requirement"),
    "contracts": ("decision", "contract"),
    "stories": ("decision", "user_story"),
    "outcomes": ("decision", "outcome"),
    "tests": ("qa", "test"),
    "evals": ("qa", "evaluation"),
}
LEGACY_INTAKE_CLASSIFICATION: dict[str, tuple[str, str | None]] = {
    "decision": ("decision", None),
    "requirement": ("decision", "requirement"),
    "constraint": ("decision", "constraint"),
    "contract": ("decision", "contract"),
    "user_story": ("decision", "user_story"),
    "outcome": ("decision", "outcome"),
    "scenario": ("decision", "scenario"),
    "invariant": ("decision", "invariant"),
    "question": ("question", None),
    "conflict": ("question", "conflict"),
    "risk": ("question", "risk"),
    "opportunity": ("question", "opportunity"),
    "problem": ("problem", None),
    "defect": ("problem", "defect"),
    "gap": ("problem", "gap"),
    "debt": ("problem", "debt"),
    "test": ("qa", "test"),
    "evaluation": ("qa", "evaluation"),
}
DECISION_ID_RE = re.compile(r"-\s*\*\*Decision ID:\*\*\s*`([^`]+)`")
STATUS_RE = re.compile(r"-\s*\*\*Status:\*\*\s*([^\n]+)")
IGNORED_PARTS = frozenset(
    {
        ".git",
        ".cache",
        ".dset",
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
    semantic_id: str
    semantic_type: str
    subtype: str | None
    carriers: set[str]
    origins: set[str]
    statuses: set[str]
    modern: bool


def classify_semantic_id(identifier: str) -> tuple[str, str | None] | None:
    """Classify a stable semantic ID without changing its spelling."""
    matches = {
        KIND_CLASSIFICATION[token]
        for token in identifier.split("-")
        if token in KIND_CLASSIFICATION
    }
    if len(matches) != 1:
        return None
    return next(iter(matches))


def build_semantic_classification_index(root: Path) -> list[dict[str, Any]]:
    root = root.resolve()
    records, diagnostics = _collect(root)
    if diagnostics:
        raise ValueError(diagnostics[0].message)
    lifecycle = _lifecycle_events(root.resolve())
    rows: list[dict[str, Any]] = []
    for record in records.values():
        events = [
            str(event["id"])
            for event in lifecycle
            if event.get("atom_id") == record.semantic_id
        ]
        rows.append(
            {
                "id": record.semantic_id,
                "type": record.semantic_type,
                "subtype": record.subtype or "none",
                "compatibility": not record.modern,
                "origins": sorted(record.origins),
                "carriers": sorted(
                    Path(carrier).relative_to(root).as_posix()
                    for carrier in record.carriers
                ),
                "carrier_statuses": sorted(record.statuses),
                "lifecycle_events": events,
            }
        )
    return sorted(rows, key=lambda item: str(item["id"]))


def validate_semantic_classifications(root: Path) -> list[Diagnostic]:
    _, diagnostics = _collect(root.resolve())
    return sorted(set(diagnostics))


def _collect(
    root: Path,
) -> tuple[dict[str, _Classification], list[Diagnostic]]:
    records: dict[str, _Classification] = {}
    diagnostics: list[Diagnostic] = []

    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        metadata = _frontmatter(path)
        if metadata and metadata.get("artifact_type") == "atomic_record":
            identifier = metadata.get("semantic_id")
            semantic_type = metadata.get("type")
            subtype = metadata.get("subtype")
            if isinstance(identifier, str) and isinstance(semantic_type, str):
                _register(
                    records,
                    diagnostics,
                    path,
                    identifier,
                    (semantic_type, str(subtype) if subtype is not None else None),
                    origin="modern_atom",
                    status=str(metadata.get("status", "unknown")),
                    modern=True,
                )
            continue
        if path.name.startswith("decision-"):
            text = path.read_text(encoding="utf-8")
            match = DECISION_ID_RE.search(text)
            if match:
                status_match = STATUS_RE.search(text)
                _register(
                    records,
                    diagnostics,
                    path,
                    match.group(1),
                    ("decision", None),
                    origin="legacy_decision",
                    status=(
                        status_match.group(1).strip() if status_match else "unknown"
                    ),
                    modern=False,
                )

    for path in discover_layout(root).structured_named_files(root, "package"):
        relative = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        data = _safe_load(path, diagnostics)
        if not isinstance(data, dict):
            continue
        for field, package_classification in FIELD_CLASSIFICATION.items():
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
                        package_classification,
                        origin=f"package:{field}",
                        status="defined",
                        modern=False,
                    )

    try:
        intake_path = discover_layout(root).intake_path
    except ValueError:
        intake_path = root / "dset/intake.yaml"
    data = _safe_load(intake_path, diagnostics) if intake_path.is_file() else None
    items = data.get("items", []) if isinstance(data, dict) else []
    if isinstance(items, list):
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                continue
            raw_type = item.get("type")
            raw_subtype = item.get("subtype")
            intake_classification: tuple[str, str | None] | None
            if raw_type in SEMANTIC_SUBTYPES:
                intake_classification = (
                    str(raw_type),
                    str(raw_subtype) if raw_subtype is not None else None,
                )
            else:
                intake_classification = LEGACY_INTAKE_CLASSIFICATION.get(str(raw_type))
            if intake_classification is None:
                diagnostics.append(
                    Diagnostic(
                        "DSET-E166",
                        intake_path,
                        f"intake semantic type is not recognized: {raw_type}",
                    )
                )
                continue
            _register(
                records,
                diagnostics,
                intake_path,
                str(item["id"]),
                intake_classification,
                origin="intake_compatibility",
                status=str(item.get("status", "unknown")),
                modern=False,
            )
    return records, diagnostics


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
    semantic_type, subtype = classification
    if semantic_type not in SEMANTIC_SUBTYPES or (
        subtype is not None and subtype not in SEMANTIC_SUBTYPES[semantic_type]
    ):
        diagnostics.append(
            Diagnostic("DSET-E166", path, f"invalid flat classification: {identifier}")
        )
        return
    by_id = classify_semantic_id(identifier)
    if by_id != classification:
        diagnostics.append(
            Diagnostic(
                "DSET-E166",
                path,
                f"semantic ID kind disagrees with carrier classification: {identifier}",
            )
        )
        return
    relative = path.as_posix()
    existing = records.get(identifier)
    if existing is None:
        records[identifier] = _Classification(
            identifier,
            semantic_type,
            subtype,
            {relative},
            {origin},
            {status},
            modern,
        )
        return
    if (existing.semantic_type, existing.subtype) != classification:
        diagnostics.append(
            Diagnostic(
                "DSET-E166",
                path,
                f"semantic carriers disagree on Type/subtype: {identifier}",
            )
        )
        return
    existing.carriers.add(relative)
    existing.origins.add(origin)
    existing.statuses.add(status)
    existing.modern = existing.modern or modern


def _frontmatter(path: Path) -> dict[str, Any] | None:
    try:
        data = frontmatter_metadata(path)
    except (OSError, UnicodeError, FrontmatterError):
        return None
    return data if isinstance(data, dict) else None


def _safe_load(path: Path, diagnostics: list[Diagnostic]) -> Any:
    try:
        return load(path)
    except (OSError, UnicodeError, YamlSubsetError) as error:
        diagnostics.append(
            Diagnostic("DSET-E166", path, f"cannot classify carrier: {error}")
        )
        return None


def _lifecycle_events(root: Path) -> list[dict[str, Any]]:
    try:
        layout = discover_layout(root)
        path = layout.structured_file(layout.governance_root, "lifecycle.toml")
    except ValueError:
        return []
    try:
        data = load(path)
    except (OSError, UnicodeError, YamlSubsetError):
        return []
    events = data.get("events", []) if isinstance(data, dict) else []
    return [item for item in events if isinstance(item, dict)]
