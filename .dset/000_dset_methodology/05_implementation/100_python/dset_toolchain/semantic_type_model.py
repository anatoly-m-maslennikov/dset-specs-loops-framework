"""Define the canonical semantic Type model and historical carrier vocabulary."""

from __future__ import annotations

from typing import Final


LAYER_KINDS: Final[frozenset[str]] = frozenset(
    {"META", "GOV", "TOOL", "SKILL", "IMPL", "OPS"}
)

# SEMANTIC_SUBTYPES owns every direct subtype admitted by the four Types.
SEMANTIC_SUBTYPES: Final[dict[str, frozenset[str]]] = {
    "decision": frozenset(
        {"requirement", "constraint", "contract", "implementation_decision"}
    ),
    "question": frozenset({"conflict", "risk", "opportunity"}),
    "problem": frozenset({"defect", "gap", "debt"}),
    "qa": frozenset({"test_plan", "evaluation_plan"}),
}
# SEMANTIC_ID_KINDS maps each current classification to its subtype-aware token.
SEMANTIC_ID_KINDS: Final[dict[tuple[str, str | None], str]] = {
    ("decision", None): "DECISION",
    ("decision", "requirement"): "REQUIREMENT",
    ("decision", "constraint"): "CONSTRAINT",
    ("decision", "contract"): "CONTRACT",
    ("decision", "implementation_decision"): "IMPL",
    ("question", None): "QUESTION",
    ("question", "conflict"): "CONFLICT",
    ("question", "risk"): "RISK",
    ("question", "opportunity"): "OPPORTUNITY",
    ("problem", None): "PROBLEM",
    ("problem", "defect"): "DEFECT",
    ("problem", "gap"): "GAP",
    ("problem", "debt"): "DEBT",
    ("qa", "test_plan"): "TEST-PLAN",
    ("qa", "evaluation_plan"): "EVAL-PLAN",
}
# SEMANTIC_TYPE_ID_KINDS maps Types to their type-only filename tokens.
SEMANTIC_TYPE_ID_KINDS: Final[dict[str, str]] = {
    "decision": "DECISION",
    "question": "QUESTION",
    "problem": "PROBLEM",
    "qa": "QA",
}
# KIND_CLASSIFICATION accepts canonical tokens used by current identifiers.
KIND_CLASSIFICATION: Final[dict[str, tuple[str, str | None]]] = {
    **{kind: classification for classification, kind in SEMANTIC_ID_KINDS.items()},
    "STORY": ("decision", "requirement"),
    "OUTCOME": ("decision", "requirement"),
    "SCENARIO": ("decision", "requirement"),
    "INVARIANT": ("decision", "requirement"),
    "QA": ("qa", None),
}
# FIELD_CLASSIFICATION maps historical package fields to semantic claims.
FIELD_CLASSIFICATION: Final[dict[str, tuple[str, str | None]]] = {
    "requirements": ("decision", "requirement"),
    "contracts": ("decision", "contract"),
    "stories": ("decision", "requirement"),
    "outcomes": ("decision", "requirement"),
    "tests": ("qa", "test_plan"),
    "evals": ("qa", "evaluation_plan"),
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
    "test_plan": ("qa", "test_plan"),
    "evaluation_plan": ("qa", "evaluation_plan"),
}


def classify_semantic_id(identifier: str) -> tuple[str, str | None] | None:
    """Classify a stable semantic ID without changing its spelling."""
    kind = semantic_id_kind(identifier)
    return KIND_CLASSIFICATION.get(kind) if kind is not None else None


def semantic_id_kind(identifier: str) -> str | None:
    """Return the semantic kind without confusing IMPL with the IMPL layer."""
    tokens = identifier.split("-")
    if len(tokens) < 3 or not tokens[-1].isdigit():
        return None
    body = tokens[1:-1]
    if len(body) > 1 and body[-1] in LAYER_KINDS:
        body = body[:-1]
    matches: list[str] = []
    for index, token in enumerate(body):
        if index + 1 < len(body):
            compound = "-".join(body[index : index + 2])
            if compound in KIND_CLASSIFICATION:
                matches.append(compound)
        if token in KIND_CLASSIFICATION:
            matches.append(token)
    return matches[0] if len(matches) == 1 else None


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
