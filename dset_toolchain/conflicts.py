from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .artifact_emission import assess_artifact_candidate
from .semantic_atoms import collect_semantic_atoms, effective_priority, seal_atom
from .settings import load_project_settings
from .yaml_subset import dump

ROLES = frozenset(
    {
        "atomic_authority",
        "evergreen_projection",
        "external_authority",
        "implementation",
        "qa",
        "evidence",
        "verification",
        "readiness",
        "derived_view",
    }
)
ASSURANCE_ROLES = frozenset({"qa", "evidence", "verification", "readiness"})
AUTHORITY_ROLES = frozenset({"atomic_authority", "external_authority"})


@dataclass(frozen=True)
class ConflictParty:
    id: str
    role: str
    priority: str
    priority_source: str
    immutable: bool
    external: bool


def resolve_conflict(root: Path, candidate: dict[str, Any]) -> dict[str, Any]:
    """Classify a candidate conflict before consulting priority."""
    root = root.resolve()
    settings, issues = load_project_settings(root)
    if issues:
        raise ValueError(issues[0])
    left = _party(root, candidate.get("left"), settings.default_priority)
    right = _party(root, candidate.get("right"), settings.default_priority)
    if left.id == right.id:
        raise ValueError("conflict parties must be different artifacts")
    relation = candidate.get("relation", "none")
    if relation not in {"none", "source_projection", "absorption"}:
        raise ValueError(f"unknown conflict relation: {relation}")
    context = _context(candidate.get("context"))
    base = {
        "schema_version": "1.0",
        "left": _party_dict(left),
        "right": _party_dict(right),
        "context": context,
        "profile": "core-v1@0.3",
        "input_sha256": _input_digest(candidate),
        "resolution_basis_sha256": _resolution_basis_digest(
            left,
            right,
            context,
            relation,
            candidate.get("selectable"),
            candidate.get("precedence"),
            settings.priority_scale,
        ),
        "conflict_atom_required": False,
        "selected_id": None,
        "resolution_event_required": False,
        "stale_when": "Either party, priority source, relation, or context changes.",
    }
    if relation == "absorption":
        winner = _required_party_id(candidate.get("relation_winner"), left, right)
        return _result(
            base,
            conflict_class="absorption",
            disposition="absorbing_atom_governs",
            selected_id=winner,
        )
    if relation == "source_projection":
        source = _role_party("atomic_authority", left, right)
        projection = _role_party("evergreen_projection", left, right)
        if source is None or projection is None:
            raise ValueError(
                "source_projection requires atomic_authority and evergreen_projection"
            )
        return _result(
            base,
            conflict_class="source_projection_drift",
            disposition="recompile_projection",
            selected_id=source.id,
        )
    if not all(context.values()):
        return _result(
            base,
            conflict_class="not_a_conflict",
            disposition="no_conflict",
        )
    roles = {left.role, right.role}
    if roles & AUTHORITY_ROLES and roles & ASSURANCE_ROLES:
        return _result(
            base,
            conflict_class="assurance_change",
            disposition="update_assurance_and_relying_gate",
        )
    if not roles & AUTHORITY_ROLES and roles & ASSURANCE_ROLES:
        return _result(
            base,
            conflict_class="assurance_change",
            disposition="update_assurance_and_relying_gate",
        )
    if "implementation" in roles and roles & AUTHORITY_ROLES:
        return _result(
            base,
            conflict_class="implementation_nonconformance",
            disposition="route_problem_defect",
        )
    if "implementation" in roles:
        return _result(
            base,
            conflict_class="implementation_ownership",
            disposition="follow_owner_or_stop",
        )
    if roles == {"evidence"}:
        return _result(
            base,
            conflict_class="evidence_adjudication",
            disposition="apply_proof_plan_or_stop",
        )
    if "derived_view" in roles:
        return _result(
            base,
            conflict_class="generated_staleness",
            disposition="refresh_derived_view",
        )
    if "evergreen_projection" in roles and not roles & AUTHORITY_ROLES:
        return _result(
            base,
            conflict_class="projection_ownership",
            disposition="route_source_conflict_or_recompile",
        )
    if "evergreen_projection" in roles:
        return _result(
            base,
            conflict_class="projection_ownership",
            disposition="declare_source_projection_relation_or_stop",
        )
    if left.external and left.immutable and not right.immutable:
        return _result(
            base,
            conflict_class="immutable_external_authority",
            disposition="external_authority_governs",
            selected_id=left.id,
        )
    if right.external and right.immutable and not left.immutable:
        return _result(
            base,
            conflict_class="immutable_external_authority",
            disposition="external_authority_governs",
            selected_id=right.id,
        )
    base["conflict_atom_required"] = True
    if left.immutable and right.immutable:
        return _result(
            base,
            conflict_class="unsatisfiable_immutable_authority",
            disposition="stop_for_external_resolution",
        )
    if candidate.get("selectable") is not True:
        return _result(
            base,
            conflict_class="nonselectable_authority",
            disposition="stop_for_decision",
        )
    precedence = candidate.get("precedence")
    if precedence is not None:
        precedence_winner = _required_party_id(precedence, left, right)
        base["resolution_event_required"] = True
        return _result(
            base,
            conflict_class="selectable_policy",
            disposition="selected_by_precedence",
            selected_id=precedence_winner,
        )
    priority_winner = _priority_winner(left, right, settings.priority_scale)
    if priority_winner is None:
        return _result(
            base,
            conflict_class="selectable_policy",
            disposition="stop_on_equal_unknown_or_incomparable_priority",
        )
    base["resolution_event_required"] = True
    return _result(
        base,
        conflict_class="selectable_policy",
        disposition="selected_by_priority",
        selected_id=priority_winner.id,
    )


def conflict_result_is_fresh(
    root: Path, candidate: dict[str, Any], recorded: dict[str, Any]
) -> bool:
    """Return whether a recorded disposition still matches current inputs."""
    current = resolve_conflict(root, candidate)
    return all(
        recorded.get(field) == current.get(field)
        for field in (
            "input_sha256",
            "resolution_basis_sha256",
            "conflict_class",
            "disposition",
            "selected_id",
            "conflict_atom_required",
            "resolution_event_required",
        )
    )


def emit_conflict_atom(
    root: Path,
    path: Path,
    candidate: dict[str, Any],
) -> tuple[Path, dict[str, Any]]:
    """Emit and seal one first-class Conflict atom after strictness assessment."""
    root = root.resolve()
    path = path.resolve()
    try:
        path.relative_to(root)
    except ValueError as error:
        raise ValueError("conflict atom must be inside the repository") from error
    if path.exists():
        raise FileExistsError(f"conflict atom already exists: {path}")

    result = resolve_conflict(root, candidate)
    if result["conflict_atom_required"] is not True:
        raise ValueError("classified incompatibility does not require a Conflict atom")
    raw_atom = candidate.get("conflict_atom")
    if not isinstance(raw_atom, dict):
        raise ValueError("conflict candidate requires conflict_atom metadata")
    atom = dict(raw_atom)
    atom["type"] = "question"
    atom["subtype"] = "conflict"
    parents = [str(result["left"]["id"]), str(result["right"]["id"])]
    if atom.get("material_links") != parents:
        raise ValueError("conflict_atom material_links must equal the two party IDs")
    if atom.get("lineage", parents) != parents:
        raise ValueError("conflict_atom lineage must equal the two party IDs")
    atom["lineage"] = parents
    assessment = assess_artifact_candidate(root, atom)
    if assessment["emission_allowed"] is not True:
        questions = assessment.get("questions", [])
        detail = "; ".join(str(item) for item in questions)
        raise ValueError(
            f"conflict atom emission is blocked: {detail or 'invalid candidate'}"
        )

    frontmatter: dict[str, Any] = {
        "artifact_type": "atomic_record",
        "artifact_id": _required_text(atom, "artifact_id"),
        "type": "question",
        "subtype": "conflict",
        "semantic_id": _required_text(atom, "semantic_id"),
        "status": _required_text(atom, "acceptance"),
        "priority": _required_text(atom, "priority"),
        "authority": _required_text(atom, "authority"),
        "claim": _required_text(atom, "claim"),
        "scope": atom.get("scope"),
        "promotion": atom.get("promotion"),
        "relations": [
            {"type": "relates_to", "target": parent} for parent in parents
        ],
        "llm_session_ids": atom.get("llm_session_ids"),
    }
    for field in (
        "boundary",
        "lineage",
        "conflict_state",
        "verification_obligation",
        "unknowns",
    ):
        if field in atom:
            frontmatter[field] = atom[field]
    rationale = atom.get("rationale")
    if rationale is not None:
        frontmatter["rationale"] = rationale
    claim = _required_text(atom, "claim")
    body = _conflict_body(claim, result)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(f"---\n{dump(frontmatter)}---\n\n{body}", encoding="utf-8")
    temporary.replace(path)
    try:
        seal_atom(root, path)
    except Exception:
        path.unlink(missing_ok=True)
        raise
    return path, result


def write_conflict_result(root: Path, path: Path, result: dict[str, Any]) -> Path:
    root = root.resolve()
    path = path.resolve()
    try:
        path.relative_to(root)
    except ValueError as error:
        raise ValueError("conflict output must be inside the repository") from error
    if path.exists():
        raise FileExistsError(f"conflict result already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return path


def _party(root: Path, value: object, default_priority: str) -> ConflictParty:
    if not isinstance(value, dict):
        raise ValueError("each conflict party must be a mapping")
    identifier = value.get("id")
    role = value.get("role")
    if not isinstance(identifier, str) or not identifier:
        raise ValueError("conflict party requires id")
    if role not in ROLES:
        raise ValueError(f"unknown governed artifact role: {role}")
    atoms, diagnostics = collect_semantic_atoms(root)
    if diagnostics:
        raise ValueError(diagnostics[0].message)
    if identifier in atoms:
        priority, source = effective_priority(root, atoms[identifier])
    else:
        priority = value.get("priority", default_priority)
        source = value.get("priority_source", "project:default")
    if not isinstance(priority, str) or not isinstance(source, str) or not source:
        raise ValueError("conflict party requires visible effective priority")
    immutable = value.get("immutable")
    external = value.get("external", False)
    if not isinstance(immutable, bool) or not isinstance(external, bool):
        raise ValueError("immutable and external must be booleans")
    return ConflictParty(identifier, str(role), priority, source, immutable, external)


def _context(value: object) -> dict[str, bool]:
    if not isinstance(value, dict):
        raise ValueError("conflict context must be a mapping")
    result: dict[str, bool] = {}
    for field in ("applicable", "same_scope", "same_concern", "same_effective_time"):
        item = value.get(field)
        if not isinstance(item, bool):
            raise ValueError(f"conflict context requires boolean {field}")
        result[field] = item
    return result


def _priority_winner(
    left: ConflictParty, right: ConflictParty, scale: tuple[str, ...]
) -> ConflictParty | None:
    if left.priority == "unknown" or right.priority == "unknown":
        return None
    try:
        left_rank = scale.index(left.priority)
        right_rank = scale.index(right.priority)
    except ValueError:
        return None
    if left_rank == right_rank:
        return None
    return left if left_rank < right_rank else right


def _required_party_id(value: object, left: ConflictParty, right: ConflictParty) -> str:
    if value not in {left.id, right.id}:
        raise ValueError("winner must identify one conflict party")
    return str(value)


def _role_party(
    role: str, left: ConflictParty, right: ConflictParty
) -> ConflictParty | None:
    if left.role == role:
        return left
    if right.role == role:
        return right
    return None


def _party_dict(party: ConflictParty) -> dict[str, object]:
    return {
        "id": party.id,
        "role": party.role,
        "priority": party.priority,
        "priority_source": party.priority_source,
        "immutable": party.immutable,
        "external": party.external,
    }


def _result(
    base: dict[str, Any],
    *,
    conflict_class: str,
    disposition: str,
    selected_id: str | None = None,
) -> dict[str, Any]:
    base["conflict_class"] = conflict_class
    base["disposition"] = disposition
    base["selected_id"] = selected_id
    return base


def _input_digest(candidate: dict[str, Any]) -> str:
    encoded = json.dumps(candidate, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _resolution_basis_digest(
    left: ConflictParty,
    right: ConflictParty,
    context: dict[str, bool],
    relation: object,
    selectable: object,
    precedence: object,
    priority_scale: tuple[str, ...],
) -> str:
    basis = {
        "left": _party_dict(left),
        "right": _party_dict(right),
        "context": context,
        "relation": relation,
        "selectable": selectable,
        "precedence": precedence,
        "priority_scale": list(priority_scale),
    }
    encoded = json.dumps(basis, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _required_text(candidate: dict[str, Any], field: str) -> str:
    value = candidate.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"conflict_atom requires {field}")
    return value.strip()


def _conflict_body(claim: str, result: dict[str, Any]) -> str:
    return (
        f"# Conflict\n\n{claim}\n\n"
        "## Parties\n\n"
        f"- `{result['left']['id']}`\n"
        f"- `{result['right']['id']}`\n\n"
        "## Initial classification\n\n"
        f"- Class: `{result['conflict_class']}`\n"
        f"- Disposition: `{result['disposition']}`\n"
        f"- Resolution basis: `{result['resolution_basis_sha256']}`\n"
    )
