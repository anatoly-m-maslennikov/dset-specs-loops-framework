from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .settings import load_project_settings

SEMANTIC_SUBTYPES = {
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

MEDIUM_FIELDS = (
    "authority",
    "claim",
    "type",
    "scope",
    "llm_session_ids",
    "material_links",
    "promotion",
)
HIGH_FIELDS = (
    "boundary",
    "priority",
    "lineage",
    "acceptance",
    "conflict_state",
    "verification_obligation",
)
FIELD_QUESTIONS = {
    "authority": "Who or what authorizes this atomic claim?",
    "claim": "What is the one precise primary claim to preserve?",
    "type": "Which one semantic Type owns this claim?",
    "scope": "What is the narrowest structural scope that owns this claim?",
    "llm_session_ids": "Which explicit LLM session IDs produced this candidate?",
    "material_links": "Which material parent or related artifact IDs apply?",
    "promotion": "What is the immediately broader enabled scope, if any?",
    "boundary": "What exact boundary and exclusions make the claim immutable?",
    "priority": "What effective project priority applies to this artifact?",
    "lineage": "Which immediate parent IDs apply, including an explicit empty list?",
    "acceptance": "What is the explicit acceptance or recording state?",
    "conflict_state": "Is any applicable authority conflict unresolved?",
    "verification_obligation": "What proof obligation applies, including none?",
}
ALLOWED_PROMOTION_STEPS = frozenset(
    {
        ("feature", "feature_group"),
        ("feature", "project"),
        ("feature_group", "project"),
        ("layer", "project"),
    }
)


def assess_artifact_candidate(
    root: Path, candidate: Mapping[str, Any]
) -> dict[str, Any]:
    settings, settings_issues = load_project_settings(root)
    if settings_issues:
        raise ValueError("; ".join(settings_issues))
    strictness = settings.artifact_creation_strictness
    fields = MEDIUM_FIELDS + (HIGH_FIELDS if strictness == "high" else ())
    diagnostics: list[dict[str, str]] = []
    questions: list[str] = []

    for field in fields:
        if not _has_explicit_value(candidate, field):
            diagnostics.append(
                {
                    "code": "DSET-ARTIFACT-MISSING",
                    "field": field,
                    "message": f"material field is not explicit: {field}",
                }
            )
            questions.append(FIELD_QUESTIONS[field])

    diagnostics.extend(_semantic_diagnostics(candidate))
    diagnostics.extend(_shape_diagnostics(candidate))
    unknown_diagnostics, unknown_questions = _unknown_diagnostics(candidate)
    diagnostics.extend(unknown_diagnostics)
    questions.extend(unknown_questions)

    promotion = _assess_promotion(candidate)
    if promotion["status"] == "invalid":
        diagnostics.append(
            {
                "code": "DSET-ARTIFACT-PROMOTION",
                "field": "promotion.parent_scope",
                "message": str(
                    promotion.get("reason", "promotion assessment is invalid")
                ),
            }
        )
    elif promotion["status"] == "proposal-required":
        diagnostics.append(
            {
                "code": "DSET-ARTIFACT-PROMOTION-AUTHORITY",
                "field": "promotion.disposition",
                "message": (
                    "eligible broader-scope promotion needs operator disposition"
                ),
            }
        )
        questions.append(str(promotion["question"]))
    elif promotion["status"] == "promote-before-emission":
        diagnostics.append(
            {
                "code": "DSET-ARTIFACT-PROMOTE-FIRST",
                "field": "scope",
                "message": "rebuild the candidate at the accepted broader scope",
            }
        )

    return {
        "schema_version": "1.0",
        "strictness": strictness,
        "emission_allowed": not diagnostics,
        "diagnostics": diagnostics,
        "questions": _unique(questions),
        "promotion": promotion,
        "writes_performed": False,
    }


def _has_explicit_value(candidate: Mapping[str, Any], field: str) -> bool:
    if field not in candidate:
        return False
    value = candidate[field]
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True


def _semantic_diagnostics(candidate: Mapping[str, Any]) -> list[dict[str, str]]:
    semantic_type = candidate.get("type")
    subtype = candidate.get("subtype")
    if semantic_type not in SEMANTIC_SUBTYPES:
        return [
            {
                "code": "DSET-ARTIFACT-TYPE",
                "field": "type",
                "message": "type must be decision, question, problem, or qa",
            }
        ]
    if subtype is not None and subtype not in SEMANTIC_SUBTYPES[str(semantic_type)]:
        return [
            {
                "code": "DSET-ARTIFACT-SUBTYPE",
                "field": "subtype",
                "message": f"subtype is not valid for {semantic_type}",
            }
        ]
    if semantic_type == "qa" and subtype is None:
        return [
            {
                "code": "DSET-ARTIFACT-SUBTYPE",
                "field": "subtype",
                "message": "qa requires test or evaluation subtype",
            }
        ]
    return []


def _shape_diagnostics(candidate: Mapping[str, Any]) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    for field in ("llm_session_ids", "material_links", "lineage"):
        if field in candidate and not _is_string_sequence(candidate[field]):
            diagnostics.append(
                {
                    "code": "DSET-ARTIFACT-SHAPE",
                    "field": field,
                    "message": f"{field} must be a list of strings",
                }
            )
    scope = candidate.get("scope")
    if scope is not None and not _valid_scope(scope):
        diagnostics.append(
            {
                "code": "DSET-ARTIFACT-SCOPE",
                "field": "scope",
                "message": "scope must contain non-empty kind and id strings",
            }
        )
    if "promotion" in candidate and not isinstance(candidate["promotion"], Mapping):
        diagnostics.append(
            {
                "code": "DSET-ARTIFACT-PROMOTION",
                "field": "promotion",
                "message": "promotion must be an object",
            }
        )
    return diagnostics


def _unknown_diagnostics(
    candidate: Mapping[str, Any],
) -> tuple[list[dict[str, str]], list[str]]:
    raw_unknowns = candidate.get("unknowns", [])
    if not isinstance(raw_unknowns, Sequence) or isinstance(raw_unknowns, str):
        return (
            [
                {
                    "code": "DSET-ARTIFACT-SHAPE",
                    "field": "unknowns",
                    "message": "unknowns must be a list of objects",
                }
            ],
            ["Which candidate details remain unknown, and are they material?"],
        )
    diagnostics: list[dict[str, str]] = []
    questions: list[str] = []
    for index, item in enumerate(raw_unknowns):
        if not isinstance(item, Mapping):
            diagnostics.append(
                {
                    "code": "DSET-ARTIFACT-SHAPE",
                    "field": f"unknowns[{index}]",
                    "message": "unknown entry must be an object",
                }
            )
            continue
        if item.get("material") is not True:
            continue
        field = str(item.get("field", f"unknowns[{index}]"))
        question = str(item.get("question", "")).strip()
        diagnostics.append(
            {
                "code": "DSET-ARTIFACT-AMBIGUOUS",
                "field": field,
                "message": "material ambiguity blocks immutable emission",
            }
        )
        questions.append(question or f"What precise value resolves {field}?")
    return diagnostics, questions


def _assess_promotion(candidate: Mapping[str, Any]) -> dict[str, Any]:
    raw = candidate.get("promotion")
    if not isinstance(raw, Mapping):
        return {"status": "not-assessed", "eligible": False}
    parent = raw.get("parent_scope")
    if parent is None:
        return {
            "status": "not-applicable",
            "eligible": False,
            "reason": "no broader enabled scope",
        }
    scope = candidate.get("scope")
    if not _valid_scope(scope) or not _valid_scope(parent):
        return {"status": "invalid", "eligible": False}
    assert isinstance(scope, Mapping)
    assert isinstance(parent, Mapping)
    current_kind = str(scope["kind"])
    parent_kind = str(parent["kind"])
    if (current_kind, parent_kind) not in ALLOWED_PROMOTION_STEPS:
        return {
            "status": "invalid",
            "eligible": False,
            "reason": "parent_scope is not an allowed immediate broader step",
        }
    affected = raw.get("affected_children")
    eligible = (
        raw.get("applies_unchanged") is True
        and raw.get("local_context_required") is False
        and _is_string_sequence(affected)
        and bool(affected)
    )
    if not eligible:
        return {
            "status": "keep-local",
            "eligible": False,
            "reason": "claim changes across children or requires local context",
        }
    disposition = raw.get("disposition")
    assert isinstance(affected, Sequence) and not isinstance(affected, str)
    affected_children = [str(item) for item in affected]
    proposal = (
        f"Promote the unchanged claim from {scope['kind']}:{scope['id']} to "
        f"{parent['kind']}:{parent['id']} for {', '.join(affected_children)}?"
    )
    if disposition == "keep_local":
        status = "declined"
    elif disposition == "promote":
        status = "promote-before-emission"
    else:
        status = "proposal-required"
    return {
        "status": status,
        "eligible": True,
        "from_scope": dict(scope),
        "to_scope": dict(parent),
        "affected_children": affected_children,
        "question": proposal,
        "automatic": False,
    }


def _valid_scope(value: object) -> bool:
    return (
        isinstance(value, Mapping)
        and isinstance(value.get("kind"), str)
        and bool(str(value["kind"]).strip())
        and isinstance(value.get("id"), str)
        and bool(str(value["id"]).strip())
    )


def _is_string_sequence(value: object) -> bool:
    return (
        isinstance(value, Sequence)
        and not isinstance(value, str)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )


def _unique(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))
