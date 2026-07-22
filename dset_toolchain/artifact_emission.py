from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .layout import LAYERS, discover_layout
from .lineage import collect_artifact_relations
from .semantic_types import SEMANTIC_SUBTYPES, build_semantic_classification_index
from .settings import load_project_settings
from .yaml_subset import load

SESSION_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*:[A-Za-z0-9._:-]+$")
AUTHORITY_PATTERN = re.compile(r"^(?:operator|repository|external):[A-Za-z0-9._:-]+$")

MEDIUM_FIELDS = (
    "authority",
    "claim",
    "type",
    "scope",
    "llm_session_ids",
    "material_links",
    "priority",
    "acceptance",
    "promotion",
)
HIGH_FIELDS = (
    "boundary",
    "lineage",
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
    diagnostics.extend(_value_diagnostics(root, candidate, settings.priority_scale))
    unknown_diagnostics, unknown_questions = _unknown_diagnostics(candidate)
    diagnostics.extend(unknown_diagnostics)
    questions.extend(unknown_questions)

    scope_model, scope_diagnostics = _repository_scope_model(root)
    diagnostics.extend(scope_diagnostics)
    promotion = _assess_promotion(candidate, scope_model)
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
                "message": (
                    "type must be requirement, decision, question, problem, or qa"
                ),
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


def _value_diagnostics(
    root: Path, candidate: Mapping[str, Any], priorities: Sequence[str]
) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    authority = candidate.get("authority")
    if isinstance(authority, str) and not AUTHORITY_PATTERN.fullmatch(authority):
        diagnostics.append(
            {
                "code": "DSET-ARTIFACT-AUTHORITY",
                "field": "authority",
                "message": (
                    "authority must use operator:, repository:, or external: "
                    "with a stable authority ID"
                ),
            }
        )
    sessions = candidate.get("llm_session_ids")
    if _is_string_sequence(sessions):
        assert isinstance(sessions, Sequence) and not isinstance(sessions, str)
        normalized = [str(item) for item in sessions]
        if len(normalized) != len(set(normalized)) or any(
            not SESSION_PATTERN.fullmatch(item) for item in normalized
        ):
            diagnostics.append(
                {
                    "code": "DSET-ARTIFACT-SESSION",
                    "field": "llm_session_ids",
                    "message": "LLM session IDs must be unique provider:id values",
                }
            )
    priority = candidate.get("priority")
    if isinstance(priority, str) and priority not in {*priorities, "unknown"}:
        diagnostics.append(
            {
                "code": "DSET-ARTIFACT-PRIORITY",
                "field": "priority",
                "message": "priority is not in the repository priority scale",
            }
        )
    acceptance = candidate.get("acceptance")
    if isinstance(acceptance, str) and acceptance not in {"proposed", "accepted"}:
        diagnostics.append(
            {
                "code": "DSET-ARTIFACT-ACCEPTANCE",
                "field": "acceptance",
                "message": "acceptance must be proposed or accepted",
            }
        )
    conflict_state = candidate.get("conflict_state")
    if isinstance(conflict_state, str) and conflict_state not in {
        "clear",
        "unresolved",
    }:
        diagnostics.append(
            {
                "code": "DSET-ARTIFACT-CONFLICT",
                "field": "conflict_state",
                "message": "conflict_state must be clear or unresolved",
            }
        )
    diagnostics.extend(_link_diagnostics(root, candidate))
    return diagnostics


def _link_diagnostics(root: Path, candidate: Mapping[str, Any]) -> list[dict[str, str]]:
    requested: set[str] = set()
    for field in ("material_links", "lineage"):
        value = candidate.get(field)
        if _is_string_sequence(value):
            assert isinstance(value, Sequence) and not isinstance(value, str)
            requested.update(str(item) for item in value)
    if not requested:
        return []
    known: set[str] = set()
    try:
        known.update(
            str(row["id"]) for row in build_semantic_classification_index(root)
        )
        nodes, relation_issues = collect_artifact_relations(root)
        if not relation_issues:
            for node in nodes.values():
                known.update((node.id, node.artifact_id))
    except (OSError, ValueError):
        pass
    missing = sorted(requested - known)
    if not missing:
        return []
    return [
        {
            "code": "DSET-ARTIFACT-LINK",
            "field": "material_links",
            "message": f"linked artifact IDs do not resolve: {', '.join(missing)}",
        }
    ]


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


def _assess_promotion(
    candidate: Mapping[str, Any], scope_model: Mapping[str, Any] | None
) -> dict[str, Any]:
    raw = candidate.get("promotion")
    if not isinstance(raw, Mapping):
        return {"status": "not-assessed", "eligible": False}
    scope = candidate.get("scope")
    if not _valid_scope(scope):
        return {"status": "invalid", "eligible": False}
    assert isinstance(scope, Mapping)
    current_key = (str(scope["kind"]), str(scope["id"]))
    if scope_model is None or current_key not in scope_model["scopes"]:
        return {
            "status": "invalid",
            "eligible": False,
            "reason": "scope is not enabled by the repository manifest",
        }
    parent = raw.get("parent_scope")
    if parent is None:
        if scope_model["parents"].get(current_key) is not None:
            return {
                "status": "invalid",
                "eligible": False,
                "reason": "the enabled local scope requires its immediate parent",
            }
        return {
            "status": "not-applicable",
            "eligible": False,
            "reason": "no broader enabled scope",
        }
    if not _valid_scope(parent):
        return {"status": "invalid", "eligible": False}
    assert isinstance(parent, Mapping)
    current_kind = str(scope["kind"])
    parent_kind = str(parent["kind"])
    parent_key = (parent_kind, str(parent["id"]))
    actual_parent = scope_model["parents"].get(current_key)
    if actual_parent != parent_key:
        return {
            "status": "invalid",
            "eligible": False,
            "reason": "parent_scope is not the manifest-defined immediate parent",
        }
    if (current_kind, parent_kind) not in ALLOWED_PROMOTION_STEPS:
        return {
            "status": "invalid",
            "eligible": False,
            "reason": "parent_scope is not an allowed immediate broader step",
        }
    affected = raw.get("affected_children")
    actual_children = scope_model["children"].get(parent_key, ())
    affected_items: tuple[str, ...] = ()
    if _is_string_sequence(affected):
        assert isinstance(affected, Sequence) and not isinstance(affected, str)
        affected_items = tuple(str(item) for item in affected)
    affected_matches = set(affected_items) == set(actual_children)
    eligible = (
        raw.get("applies_unchanged") is True
        and raw.get("local_context_required") is False
        and affected_matches
        and bool(actual_children)
    )
    if not eligible:
        return {
            "status": "keep-local",
            "eligible": False,
            "reason": "claim changes across children or requires local context",
        }
    disposition = raw.get("disposition")
    affected_children = list(affected_items)
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


def _repository_scope_model(
    root: Path,
) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    try:
        layout = discover_layout(root)
        manifest = load(layout.manifest_path)
    except (OSError, ValueError) as error:
        return None, [
            {
                "code": "DSET-ARTIFACT-REPOSITORY",
                "field": "scope",
                "message": f"repository scope authority is unavailable: {error}",
            }
        ]
    project = manifest.get("project") if isinstance(manifest, Mapping) else None
    project_id = project.get("id") if isinstance(project, Mapping) else None
    if not isinstance(project_id, str) or not project_id.strip():
        return None, [
            {
                "code": "DSET-ARTIFACT-REPOSITORY",
                "field": "scope",
                "message": "project manifest requires project.id",
            }
        ]
    project_key = ("project", project_id)
    scopes: set[tuple[str, str]] = {project_key}
    parents: dict[tuple[str, str], tuple[str, str]] = {}
    children: dict[tuple[str, str], tuple[str, ...]] = {}
    if layout.layered:
        layer_keys = [("layer", layer) for layer in LAYERS]
        scopes.update(layer_keys)
        parents.update({key: project_key for key in layer_keys})
        children[project_key] = LAYERS
    return {
        "scopes": scopes,
        "parents": parents,
        "children": children,
    }, []


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
