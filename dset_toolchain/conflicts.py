from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .artifact_emission import assess_artifact_candidate
from .frontmatter import FrontmatterError
from .frontmatter import metadata as frontmatter_metadata
from .frontmatter import render as render_frontmatter
from .layout import discover_layout
from .project_data import project_section
from .semantic_atoms import (
    build_semantic_atom_index,
    collect_semantic_atoms,
    seal_atom,
)
from .settings import load_project_settings
from .toml_codec import loads as load_toml
from .yaml_subset import load as load_structured

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
    applicable: bool
    scope: dict[str, Any] | None
    current_status: str
    semantic_type: str | None
    subtype: str | None
    carrier_id: str | None
    relations: tuple[dict[str, Any], ...]
    absorbed_by: tuple[str, ...]
    evidence: tuple[dict[str, str], ...]


def resolve_conflict(root: Path, candidate: dict[str, Any]) -> dict[str, Any]:
    """Classify a candidate conflict before consulting priority."""
    root = root.resolve()
    unknown_fields = sorted(
        set(candidate)
        - {
            "left",
            "right",
            "context",
            "relation",
            "relation_winner",
            "selectable",
            "precedence",
            "conflict_atom",
        }
    )
    if unknown_fields:
        raise ValueError(
            "conflict candidate has unknown fields: " + ", ".join(unknown_fields)
        )
    settings, issues = load_project_settings(root)
    if issues:
        raise ValueError(issues[0])
    atoms, diagnostics = collect_semantic_atoms(root)
    if diagnostics:
        raise ValueError(diagnostics[0].message)
    atom_index = {str(item["id"]): item for item in build_semantic_atom_index(root)}
    rules, registry_identity = _governance_rules(root)
    left = _party(
        root,
        candidate.get("left"),
        settings.default_priority,
        settings.priority_scale,
        atoms,
        atom_index,
        rules,
        registry_identity,
    )
    right = _party(
        root,
        candidate.get("right"),
        settings.default_priority,
        settings.priority_scale,
        atoms,
        atom_index,
        rules,
        registry_identity,
    )
    if left.id == right.id:
        raise ValueError("conflict parties must be different artifacts")
    relation, relation_winner = _derived_relation(left, right)
    _assert_optional_match(candidate, "relation", relation)
    _assert_optional_match(candidate, "relation_winner", relation_winner)
    context = _context(root, candidate.get("context"), left, right)
    selectable = candidate.get("selectable", False)
    if not isinstance(selectable, bool):
        raise ValueError("conflict selectable assertion must be boolean")
    precedence = _registered_precedence(left.id, right.id, rules)
    _assert_optional_match(candidate, "precedence", precedence)
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
            selectable,
            precedence,
            settings.priority_scale,
        ),
        "conflict_atom_required": False,
        "selected_id": None,
        "resolution_event_required": False,
        "stale_when": "Either party, priority source, relation, or context changes.",
    }
    if relation == "absorption":
        assert relation_winner is not None
        return _result(
            base,
            conflict_class="absorption",
            disposition="absorbing_atom_governs",
            selected_id=relation_winner,
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
    if selectable is not True:
        return _result(
            base,
            conflict_class="nonselectable_authority",
            disposition="stop_for_decision",
        )
    if precedence is not None:
        base["resolution_event_required"] = True
        return _result(
            base,
            conflict_class="selectable_policy",
            disposition="selected_by_precedence",
            selected_id=precedence,
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
    try:
        current = resolve_conflict(root, candidate)
    except ValueError as error:
        message = str(error)
        if message.endswith(" is stale") or "mismatches repository truth" in message:
            return False
        raise
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

    promotion = atom.get("promotion")
    if isinstance(promotion, dict) and promotion.get("parent_scope") is None:
        promotion = {
            key: value for key, value in promotion.items() if key != "parent_scope"
        }
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
        "promotion": promotion,
        "relations": [{"type": "relates_to", "target": parent} for parent in parents],
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
    temporary.write_text(render_frontmatter(frontmatter, f"\n{body}"), encoding="utf-8")
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


def _party(
    root: Path,
    value: object,
    default_priority: str,
    priority_scale: tuple[str, ...],
    atoms: dict[str, Any],
    atom_index: dict[str, dict[str, Any]],
    rules: dict[str, dict[str, Any]],
    registry_identity: dict[str, str] | None,
) -> ConflictParty:
    if not isinstance(value, dict):
        raise ValueError("each conflict party must be a mapping")
    unknown_fields = sorted(
        set(value)
        - {
            "id",
            "source",
            "role",
            "priority",
            "priority_source",
            "immutable",
            "external",
            "scope",
            "current_status",
        }
    )
    if unknown_fields:
        raise ValueError(
            "conflict party has unknown fields: " + ", ".join(unknown_fields)
        )
    identifier = value.get("id")
    if not isinstance(identifier, str) or not identifier:
        raise ValueError("conflict party requires id")
    if identifier in atoms:
        atom = atoms[identifier]
        row = atom_index[identifier]
        path = root / atom.path
        metadata = _read_metadata(path)
        authority = metadata.get("authority")
        external = isinstance(authority, str) and authority.startswith("external:")
        if atom.semantic_type == "decision":
            role = "external_authority" if external else "atomic_authority"
        elif atom.semantic_type == "qa":
            role = "qa"
        else:
            role = "evidence"
        current_status = str(row["current_status"])
        party = ConflictParty(
            id=identifier,
            role=role,
            priority=str(row["priority"]),
            priority_source=str(row["priority_source"]),
            immutable=True,
            external=external,
            applicable=current_status
            not in {"proposed", "absorbed", "rejected", "retired", "withdrawn"},
            scope=_scope(metadata.get("scope")),
            current_status=current_status,
            semantic_type=atom.semantic_type,
            subtype=atom.subtype,
            carrier_id=atom.carrier_id,
            relations=tuple(
                item for item in row["relations"] if isinstance(item, dict)
            ),
            absorbed_by=tuple(str(item) for item in row["absorbed_by"]),
            evidence=tuple(_atom_evidence(root, path, row)),
        )
    elif identifier in rules:
        rule = rules[identifier]
        rule_path = root / str(rule.get("path", ""))
        evidence = [registry_identity] if registry_identity is not None else []
        if rule_path.is_file():
            evidence.append(_derived_identity(root, rule_path))
        applicable = rule.get("applicability") == "applicable"
        party = ConflictParty(
            id=identifier,
            role="atomic_authority",
            priority=default_priority,
            priority_source="project:default",
            immutable=False,
            external=False,
            applicable=applicable,
            scope=None,
            current_status="accepted" if applicable else "withdrawn",
            semantic_type=None,
            subtype=None,
            carrier_id=None,
            relations=(),
            absorbed_by=(),
            evidence=tuple(evidence),
        )
    else:
        source_identity = _asserted_identity(root, value.get("source"), "party source")
        metadata = _read_metadata(root / source_identity["path"])
        resolved_id = metadata.get("artifact_id", metadata.get("id"))
        if resolved_id != identifier:
            raise ValueError("conflict party source does not resolve the party ID")
        role = _metadata_role(metadata)
        priority = metadata.get("priority", default_priority)
        priority_source = (
            f"artifact:{source_identity['path']}"
            if "priority" in metadata
            else "project:default"
        )
        authority = metadata.get("authority")
        external = metadata.get("external", False) is True or (
            isinstance(authority, str) and authority.startswith("external:")
        )
        immutable = metadata.get("immutable", False)
        if not isinstance(immutable, bool):
            raise ValueError("conflict party source immutable fact must be boolean")
        status = metadata.get("current_status", metadata.get("status", "accepted"))
        current_status = str(status)
        party = ConflictParty(
            id=identifier,
            role=role,
            priority=str(priority),
            priority_source=priority_source,
            immutable=immutable,
            external=external,
            applicable=_metadata_applicable(metadata, current_status),
            scope=_scope(metadata.get("scope")),
            current_status=current_status,
            semantic_type=None,
            subtype=None,
            carrier_id=None,
            relations=tuple(_metadata_relations(metadata)),
            absorbed_by=(),
            evidence=(source_identity,),
        )
    if party.priority not in {*priority_scale, "unknown"}:
        raise ValueError("conflict party priority is not in the project scale")
    _validate_party_assertions(value, party)
    return party


def _context(
    root: Path,
    value: object,
    left: ConflictParty,
    right: ConflictParty,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("conflict context must be a mapping")
    unknown_fields = sorted(
        set(value)
        - {
            "applicable",
            "same_scope",
            "same_concern",
            "same_effective_time",
            "evidence",
        }
    )
    if unknown_fields:
        raise ValueError(
            "conflict context has unknown fields: " + ", ".join(unknown_fields)
        )
    evidence = value.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise ValueError("conflict context assertions require evidence")
    identities = [
        _asserted_identity(root, item, "context evidence") for item in evidence
    ]
    result: dict[str, Any] = {}
    derived_applicable = left.applicable and right.applicable
    if value.get("applicable") != derived_applicable:
        raise ValueError("conflict context applicable assertion mismatches repository")
    result["applicable"] = derived_applicable
    if left.scope is not None and right.scope is not None:
        derived_same_scope = left.scope == right.scope
        if value.get("same_scope") != derived_same_scope:
            raise ValueError(
                "conflict context same_scope assertion mismatches repository"
            )
        result["same_scope"] = derived_same_scope
    else:
        same_scope = value.get("same_scope")
        if not isinstance(same_scope, bool):
            raise ValueError("conflict context requires boolean same_scope")
        result["same_scope"] = same_scope
    for field in ("same_concern", "same_effective_time"):
        item = value.get(field)
        if not isinstance(item, bool):
            raise ValueError(f"conflict context requires boolean {field}")
        result[field] = item
    result["evidence"] = identities
    return result


def _governance_rules(
    root: Path,
) -> tuple[dict[str, dict[str, Any]], dict[str, str] | None]:
    path = discover_layout(root).governance_path
    if not path.is_file():
        return {}, None
    data = project_section(root, "governance_registry")
    raw_rules = data.get("rules", [])
    if not isinstance(raw_rules, list):
        raise ValueError("governance registry rules must be a list")
    rules: dict[str, dict[str, Any]] = {}
    for item in raw_rules:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValueError("governance registry rule is invalid")
        identifier = str(item["id"])
        if identifier in rules:
            raise ValueError(f"duplicate governance rule: {identifier}")
        rules[identifier] = item
    return rules, _derived_identity(root, path)


def _read_metadata(path: Path) -> dict[str, Any]:
    try:
        if path.suffix.lower() == ".md":
            value = frontmatter_metadata(path)
        elif path.suffix.lower() == ".json":
            value = json.loads(path.read_text(encoding="utf-8"))
        elif path.suffix.lower() == ".toml":
            value = load_toml(path.read_text(encoding="utf-8"))
        else:
            value = load_structured(path)
    except (OSError, UnicodeError, ValueError, FrontmatterError) as error:
        raise ValueError(
            f"cannot read conflict fact source: {path}: {error}"
        ) from error
    if not isinstance(value, dict):
        raise ValueError(f"conflict fact source must be a mapping: {path}")
    return value


def _derived_identity(root: Path, path: Path) -> dict[str, str]:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(root)
    except ValueError as error:
        raise ValueError(
            "conflict evidence must remain inside the repository"
        ) from error
    if not resolved.is_file():
        raise ValueError(f"conflict evidence does not exist: {relative.as_posix()}")
    return {
        "path": relative.as_posix(),
        "sha256": hashlib.sha256(resolved.read_bytes()).hexdigest(),
    }


def _asserted_identity(root: Path, value: object, label: str) -> dict[str, str]:
    if not isinstance(value, dict) or set(value) != {"path", "sha256"}:
        raise ValueError(f"{label} requires exact path and sha256")
    raw_path = value.get("path")
    raw_digest = value.get("sha256")
    if not isinstance(raw_path, str) or not raw_path or Path(raw_path).is_absolute():
        raise ValueError(f"{label} path must be repository-relative")
    if ".." in Path(raw_path).parts:
        raise ValueError(f"{label} path must not escape the repository")
    if (
        not isinstance(raw_digest, str)
        or len(raw_digest) != 64
        or any(character not in "0123456789abcdef" for character in raw_digest)
    ):
        raise ValueError(f"{label} sha256 is invalid")
    current = _derived_identity(root, root / raw_path)
    if current["sha256"] != raw_digest:
        raise ValueError(f"{label} is stale")
    return current


def _atom_evidence(root: Path, path: Path, row: dict[str, Any]) -> list[dict[str, str]]:
    evidence = [_derived_identity(root, path)]
    if row.get("lifecycle_events"):
        layout = discover_layout(root)
        lifecycle_path = layout.structured_file(
            layout.project_state_root, "lifecycle.toml"
        )
        if lifecycle_path.is_file():
            evidence.append(_derived_identity(root, lifecycle_path))
    return evidence


def _metadata_role(metadata: dict[str, Any]) -> str:
    artifact_type = metadata.get("artifact_type")
    subtype = metadata.get("artifact_subtype")
    mapped = {
        "specification": "evergreen_projection",
        "procedure": "evergreen_projection",
        "plan": "evergreen_projection",
        "implementation": "implementation",
        "evidence_record": "evidence",
        "verification": "verification",
        "analysis_report": "evidence",
        "derived_view": "derived_view",
        "navigation": "derived_view",
    }.get(str(artifact_type))
    if artifact_type == "version" and subtype == "readiness_record":
        mapped = "readiness"
    declared = metadata.get("conflict_role")
    if mapped is not None and declared is not None and declared != mapped:
        raise ValueError("conflict source role contradicts its artifact type")
    role = mapped or declared
    if role not in ROLES:
        raise ValueError("conflict source does not declare a governed role")
    return str(role)


def _metadata_applicable(metadata: dict[str, Any], status: str) -> bool:
    explicit = metadata.get("applicability")
    if isinstance(explicit, bool):
        return explicit
    if isinstance(explicit, str) and explicit in {"applicable", "not_applicable"}:
        return explicit == "applicable"
    return status not in {"proposed", "absorbed", "rejected", "retired", "withdrawn"}


def _scope(value: object) -> dict[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError("conflict party scope must be a mapping")
    return dict(value)


def _metadata_relations(metadata: dict[str, Any]) -> list[dict[str, Any]]:
    raw = metadata.get("relations", [])
    if not isinstance(raw, list) or not all(isinstance(item, dict) for item in raw):
        raise ValueError("conflict source relations must be a list of mappings")
    return [dict(item) for item in raw]


def _validate_party_assertions(asserted: dict[str, Any], party: ConflictParty) -> None:
    derived: dict[str, Any] = {
        "role": party.role,
        "priority": party.priority,
        "priority_source": party.priority_source,
        "immutable": party.immutable,
        "external": party.external,
        "scope": party.scope,
        "current_status": party.current_status,
    }
    for field, expected in derived.items():
        if field in asserted and asserted[field] != expected:
            raise ValueError(
                f"conflict party {field} assertion mismatches repository truth"
            )
    if "source" in asserted and asserted["source"] != party.evidence[0]:
        raise ValueError("conflict party source assertion mismatches repository truth")


def _assert_optional_match(
    candidate: dict[str, Any], field: str, expected: object
) -> None:
    if field in candidate and candidate[field] != expected:
        raise ValueError(f"conflict {field} assertion mismatches repository truth")


def _derived_relation(
    left: ConflictParty, right: ConflictParty
) -> tuple[str, str | None]:
    if right.id in left.absorbed_by:
        return "absorption", right.id
    if left.id in right.absorbed_by:
        return "absorption", left.id
    if left.role == "evergreen_projection" and _projects(left, right):
        return "source_projection", None
    if right.role == "evergreen_projection" and _projects(right, left):
        return "source_projection", None
    return "none", None


def _projects(projection: ConflictParty, source: ConflictParty) -> bool:
    for relation in projection.relations:
        if relation.get("type") != "projection_of":
            continue
        if relation.get("target") == source.id:
            return True
        frontier = relation.get("range")
        if not isinstance(frontier, dict) or source.semantic_type is None:
            continue
        if frontier.get("semantic_type") != source.semantic_type:
            continue
        if frontier.get("subtype") not in {None, source.subtype}:
            continue
        frontier_scope = frontier.get("scope")
        if frontier_scope is not None and frontier_scope != source.scope:
            continue
        layer = frontier.get("layer")
        if isinstance(layer, str) and layer.upper() not in source.id.split("-"):
            continue
        through = frontier.get("through")
        if _carrier_at_or_before(source.carrier_id, through):
            return True
    return False


def _carrier_at_or_before(carrier_id: str | None, through: object) -> bool:
    if not isinstance(carrier_id, str) or not isinstance(through, str):
        return False
    if carrier_id == through:
        return True
    carrier_prefix, separator, carrier_sequence = carrier_id.rpartition("-")
    through_prefix, other_separator, through_sequence = through.rpartition("-")
    return (
        separator == other_separator == "-"
        and carrier_prefix == through_prefix
        and carrier_sequence.isdigit()
        and through_sequence.isdigit()
        and int(carrier_sequence) <= int(through_sequence)
    )


def _registered_precedence(
    left_id: str, right_id: str, rules: dict[str, dict[str, Any]]
) -> str | None:
    left_wins = _precedes(left_id, right_id, rules)
    right_wins = _precedes(right_id, left_id, rules)
    if left_wins and right_wins:
        raise ValueError("registered conflict precedence is cyclic")
    if left_wins:
        return left_id
    if right_wins:
        return right_id
    return None


def _precedes(source: str, target: str, rules: dict[str, dict[str, Any]]) -> bool:
    if source not in rules or target not in rules:
        return False
    pending = [source]
    seen: set[str] = set()
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        seen.add(current)
        raw = rules[current].get("precedence_over", [])
        if not isinstance(raw, list):
            raise ValueError("governance precedence_over must be a list")
        successors = [str(item) for item in raw]
        if target in successors:
            return True
        pending.extend(item for item in successors if item in rules)
    return False


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
        "applicable": party.applicable,
        "scope": party.scope,
        "current_status": party.current_status,
        "semantic_type": party.semantic_type,
        "subtype": party.subtype,
        "carrier_id": party.carrier_id,
        "relations": list(party.relations),
        "absorbed_by": list(party.absorbed_by),
        "evidence": list(party.evidence),
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
    context: dict[str, Any],
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
