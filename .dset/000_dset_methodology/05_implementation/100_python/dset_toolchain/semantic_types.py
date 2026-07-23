"""Expose the stable semantic Type API from focused implementation modules."""

from __future__ import annotations

from pathlib import Path

from .semantic_type_index import (
    build_semantic_classification_index,
    validate_semantic_classifications,
)
from .semantic_type_model import (
    KIND_CLASSIFICATION,
    SEMANTIC_ID_KINDS,
    SEMANTIC_SUBTYPES,
    SEMANTIC_TYPE_ID_KINDS,
    classify_semantic_id,
    normalize_semantic_classification,
    semantic_id_kind,
    semantic_id_matches_classification,
    semantic_naming_axis,
)

# __all__ defines the supported compatibility facade for existing callers.
__all__ = [
    "KIND_CLASSIFICATION",
    "SEMANTIC_ID_KINDS",
    "SEMANTIC_SUBTYPES",
    "SEMANTIC_TYPE_ID_KINDS",
    "build_semantic_classification_index",
    "classify_semantic_id",
    "next_semantic_sequence",
    "normalize_semantic_classification",
    "semantic_id_kind",
    "semantic_id_matches_classification",
    "semantic_naming_axis",
    "validate_semantic_classifications",
]


def next_semantic_sequence(
    root: Path,
    semantic_type: str,
    subtype: str | None,
    *,
    include_subtype: bool,
) -> int:
    """Return the next project-wide number for the configured naming axis."""
    numbers = [
        number
        for row in build_semantic_classification_index(root)
        if (number := _matching_number(row, semantic_type, subtype, include_subtype))
        is not None
    ]
    return max(numbers, default=0) + 1


def _matching_number(
    row: dict[str, object],
    semantic_type: str,
    subtype: str | None,
    include_subtype: bool,
) -> int | None:
    """Extract a row sequence when it belongs to the requested naming axis."""
    if row.get("type") != semantic_type:
        return None
    if include_subtype and row.get("subtype") != (subtype or "none"):
        return None
    tail = str(row.get("id", "")).rsplit("-", 1)[-1]
    return int(tail) if tail.isdigit() else None
