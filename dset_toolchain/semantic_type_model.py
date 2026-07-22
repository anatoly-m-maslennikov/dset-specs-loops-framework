"""Define the canonical semantic Type model and compatibility vocabulary."""

from __future__ import annotations

from typing import Final

# SEMANTIC_SUBTYPES owns every direct subtype admitted by the four Types.
SEMANTIC_SUBTYPES: Final[dict[str, frozenset[str]]] = {
    "decision": frozenset(
        {"requirement", "constraint", "contract", "implementation_decision"}
    ),
    "question": frozenset({"conflict", "risk", "opportunity"}),
    "problem": frozenset({"defect", "gap", "debt"}),
    "qa": frozenset({"test", "evaluation"}),
}
# SEMANTIC_ID_KINDS maps each current classification to its subtype-aware token.
SEMANTIC_ID_KINDS: Final[dict[tuple[str, str | None], str]] = {
    ("decision", None): "DECISION",
    ("decision", "requirement"): "REQ",
    ("decision", "constraint"): "CONSTR",
    ("decision", "contract"): "CONTR",
    ("decision", "implementation_decision"): "IMPDEC",
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
# SEMANTIC_TYPE_ID_KINDS maps Types to their type-only filename tokens.
SEMANTIC_TYPE_ID_KINDS: Final[dict[str, str]] = {
    "decision": "DECISION",
    "question": "QUESTION",
    "problem": "PROBLEM",
    "qa": "QA",
}
# KIND_CLASSIFICATION accepts current tokens and immutable historical aliases.
KIND_CLASSIFICATION: Final[dict[str, tuple[str, str | None]]] = {
    **{kind: classification for classification, kind in SEMANTIC_ID_KINDS.items()},
    "REQUIREMENT": ("decision", "requirement"),
    "CONSTRAINT": ("decision", "constraint"),
    "CONTRACT": ("decision", "contract"),
    "STORY": ("decision", "requirement"),
    "OUTCOME": ("decision", "requirement"),
    "SCENARIO": ("decision", "requirement"),
    "INVARIANT": ("decision", "requirement"),
    "EVAL": ("qa", "evaluation"),
    "QA": ("qa", None),
}
# FIELD_CLASSIFICATION maps compatibility package fields to semantic claims.
FIELD_CLASSIFICATION: Final[dict[str, tuple[str, str | None]]] = {
    "requirements": ("decision", "requirement"),
    "contracts": ("decision", "contract"),
    "stories": ("decision", "requirement"),
    "outcomes": ("decision", "requirement"),
    "tests": ("qa", "test"),
    "evals": ("qa", "evaluation"),
}
# LEGACY_INTAKE_CLASSIFICATION translates historical intake vocabulary.
LEGACY_INTAKE_CLASSIFICATION: Final[dict[str, tuple[str, str | None]]] = {
    "decision": ("decision", None),
    "requirement": ("decision", "requirement"),
    "constraint": ("decision", "constraint"),
    "contract": ("decision", "contract"),
    "implementation_decision": ("decision", "implementation_decision"),
    "user_story": ("decision", "requirement"),
    "outcome": ("decision", "requirement"),
    "scenario": ("decision", "requirement"),
    "invariant": ("decision", "requirement"),
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


def classify_semantic_id(identifier: str) -> tuple[str, str | None] | None:
    """Classify a stable semantic ID without changing its spelling."""
    matches = {
        KIND_CLASSIFICATION[token]
        for token in identifier.split("-")
        if token in KIND_CLASSIFICATION
    }
    return next(iter(matches)) if len(matches) == 1 else None


def semantic_naming_axis(
    semantic_type: str,
    subtype: str | None,
    *,
    include_subtype: bool,
) -> str:
    """Return the project-wide sequence axis selected for a new atom."""
    if include_subtype and subtype is not None:
        return SEMANTIC_ID_KINDS[(semantic_type, subtype)]
    return SEMANTIC_TYPE_ID_KINDS[semantic_type]


def semantic_id_matches_classification(
    identifier: str,
    semantic_type: str,
    subtype: str | None,
) -> bool:
    """Accept either a type-axis or subtype-axis identity for one atom."""
    classification = classify_semantic_id(identifier)
    return classification in {(semantic_type, subtype), (semantic_type, None)}


def normalize_semantic_classification(
    semantic_type: str, subtype: str | None
) -> tuple[str, str | None]:
    """Return the canonical four-Type classification for a carrier."""
    if semantic_type == "requirement":
        if subtype in {"constraint", "contract"}:
            return "decision", subtype
        return "decision", "requirement"
    if semantic_type != "decision" or subtype is None:
        return semantic_type, subtype
    if subtype in SEMANTIC_SUBTYPES["decision"]:
        return semantic_type, subtype
    if subtype in {"user_story", "outcome", "scenario", "invariant"}:
        return "decision", "requirement"
    return semantic_type, subtype
