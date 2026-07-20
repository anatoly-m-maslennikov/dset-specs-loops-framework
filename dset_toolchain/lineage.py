from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .diagnostics import Diagnostic
from .frontmatter import FrontmatterError
from .frontmatter import metadata as frontmatter_metadata
from .layout import discover_layout
from .semantic_types import SEMANTIC_SUBTYPES
from .yaml_subset import YamlSubsetError, load

ID_PATTERN = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)+$")
SESSION_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*:[A-Za-z0-9._:-]+$")
ATOM_PATTERN = re.compile(r"-ATOMIC-RECORD-([0-9]+)$")
INACTIVE_EVENTS = frozenset({"absorbed", "rejected", "retired", "withdrawn"})
RELATION_TYPES = frozenset(
    {
        "child_of",
        "analysis_of",
        "projection_of",
        "implementation_of",
        "check_of",
        "evidence_for",
        "resolution_of",
        "override_of",
        "replacement_of",
        "relates_to",
    }
)
ACYCLIC_RELATION_TYPES = frozenset(
    {"child_of", "override_of", "replacement_of"}
)
PROJECTION_SOURCE_TYPES = frozenset(
    {"specification", "procedure", "plan", "derived_view", "navigation"}
)
SEMANTIC_TYPES = frozenset(SEMANTIC_SUBTYPES)
LAYERS = frozenset({"meta", "gov", "tool", "skill", "ops"})
SCOPE_KINDS = frozenset({"project", "layer", "feature_group", "feature"})
REVERSE_FIELDS = frozenset(
    {
        "parent_to",
        "analysis_by",
        "projection_by",
        "implemented_by",
        "checked_by",
        "evidence_from",
        "resolved_by",
        "overridden_by",
        "replaced_by",
    }
)
IGNORED_PARTS = frozenset(
    {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".uv-cache",
        ".venv",
        "__pycache__",
        "dist",
        "templates",
    }
)


@dataclass(frozen=True)
class ProjectionRange:
    semantic_type: str
    subtype: str | None
    layer: str | None
    scope_kind: str
    scope_id: str
    through: str

    def as_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "semantic_type": self.semantic_type,
            "scope": {"kind": self.scope_kind, "id": self.scope_id},
            "through": self.through,
        }
        if self.subtype is not None:
            data["subtype"] = self.subtype
        if self.layer is not None:
            data["layer"] = self.layer
        return data


@dataclass(frozen=True)
class ArtifactRelation:
    type: str
    target: str | None
    range: ProjectionRange | None
    origin: str

    def as_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"type": self.type, "origin": self.origin}
        if self.target is not None:
            data["target"] = self.target
        if self.range is not None:
            data["range"] = self.range.as_dict()
        return data


@dataclass(frozen=True)
class RelationNode:
    id: str
    artifact_id: str
    path: str
    artifact_type: str | None
    semantic_type: str | None
    subtype: str | None
    layer: str | None
    scope_kind: str | None
    scope_id: str | None
    relations: tuple[ArtifactRelation, ...]

    @property
    def child_of(self) -> tuple[str, ...]:
        return tuple(
            relation.target
            for relation in self.relations
            if relation.type == "child_of" and relation.target is not None
        )


@dataclass(frozen=True)
class _RawNode:
    node: RelationNode
    path: Path


def parse_authored_relations(
    path: Path,
    metadata: dict[str, Any],
    diagnostics: list[Diagnostic],
) -> tuple[ArtifactRelation, ...]:
    """Parse canonical relations and sealed legacy child_of compatibility."""
    _reject_reverse_fields(path, metadata, diagnostics)
    raw_relations = metadata.get("relations")
    raw_legacy = metadata.get("child_of")
    if raw_relations is not None and raw_legacy is not None:
        diagnostics.append(
            _diag(path, "relations and legacy child_of cannot be authored together")
        )
        return ()
    if raw_legacy is not None:
        return _parse_legacy_child_of(path, raw_legacy, diagnostics)
    if raw_relations is None:
        return ()
    if not isinstance(raw_relations, list) or not raw_relations:
        diagnostics.append(_diag(path, "relations must be a non-empty list"))
        return ()
    parsed = [
        relation
        for item in raw_relations
        if (relation := _parse_relation(path, item, diagnostics)) is not None
    ]
    _validate_local_uniqueness(path, parsed, diagnostics)
    return tuple(parsed)


def collect_artifact_relations(
    root: Path,
) -> tuple[dict[str, RelationNode], list[Diagnostic]]:
    """Collect canonical forward relations from governed Markdown artifacts."""
    root = root.resolve()
    raw_nodes, aliases, diagnostics = _collect_raw_nodes(root)
    inactive = _inactive_semantic_ids(root)
    known = _known_relation_ids(root) | set(aliases)
    nodes = _resolve_nodes(root, raw_nodes, aliases, known, inactive, diagnostics)
    diagnostics.extend(_cycle_diagnostics(root, nodes, inactive))
    diagnostics.extend(_range_diagnostics(root, nodes, inactive))
    diagnostics.extend(_replacement_diagnostics(root, nodes))
    diagnostics.extend(_source_diagnostics(root, nodes))
    return nodes, sorted(set(diagnostics))


def build_relation_index(root: Path) -> list[dict[str, Any]]:
    nodes, diagnostics = collect_artifact_relations(root)
    if diagnostics:
        raise ValueError(diagnostics[0].message)
    rows: list[dict[str, Any]] = []
    for node in nodes.values():
        for relation in node.relations:
            row = {
                "source": node.id,
                "source_kind": "artifact",
                "source_artifact_id": node.artifact_id,
                "source_path": node.path,
                **relation.as_dict(),
                "llm_session_ids": [],
            }
            rows.append(row)
    rows.extend(build_commit_implementation_relations(root))
    return sorted(rows, key=_relation_sort_key)


def build_commit_implementation_relations(root: Path) -> list[dict[str, Any]]:
    """Derive typed implementation relations from immutable Git trailers."""
    try:
        completed = subprocess.run(
            ["git", "log", "--no-merges", "--format=%H%x1f%B%x1e"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    rows: list[dict[str, Any]] = []
    for record in completed.stdout.split("\x1e"):
        rows.extend(_commit_relations(record))
    return sorted(rows, key=_relation_sort_key)


def validate_artifact_relations(root: Path) -> list[Diagnostic]:
    _, diagnostics = collect_artifact_relations(root)
    return diagnostics


def validate_artifact_lineage(root: Path) -> list[Diagnostic]:
    """Compatibility entrypoint for the renamed typed-relation validator."""
    return validate_artifact_relations(root)


def _collect_raw_nodes(
    root: Path,
) -> tuple[list[_RawNode], dict[str, str], list[Diagnostic]]:
    raw_nodes: list[_RawNode] = []
    aliases: dict[str, str] = {}
    alias_paths: dict[str, Path] = {}
    diagnostics: list[Diagnostic] = []
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        metadata = _frontmatter(path)
        if metadata is None:
            continue
        relations = parse_authored_relations(path, metadata, diagnostics)
        artifact_id = metadata.get("artifact_id")
        if artifact_id is None:
            if relations or any(field in metadata for field in REVERSE_FIELDS):
                diagnostics.append(
                    _diag(path, "artifact relations require artifact_id")
                )
            continue
        if not isinstance(artifact_id, str) or not ID_PATTERN.fullmatch(artifact_id):
            continue
        node = _node_from_metadata(root, path, artifact_id, metadata, relations)
        raw_nodes.append(_RawNode(node, path))
        _register_aliases(node, path, aliases, alias_paths, diagnostics)
    return raw_nodes, aliases, diagnostics


def _node_from_metadata(
    root: Path,
    path: Path,
    artifact_id: str,
    metadata: dict[str, Any],
    relations: tuple[ArtifactRelation, ...],
) -> RelationNode:
    semantic_id = metadata.get("semantic_id")
    node_id = artifact_id
    if (
        metadata.get("artifact_type") == "atomic_record"
        and isinstance(semantic_id, str)
        and ID_PATTERN.fullmatch(semantic_id)
    ):
        node_id = semantic_id
    scope = metadata.get("scope")
    scope_kind = scope.get("kind") if isinstance(scope, dict) else None
    scope_id = scope.get("id") if isinstance(scope, dict) else None
    semantic_type = metadata.get("type")
    subtype = metadata.get("subtype")
    return RelationNode(
        id=node_id,
        artifact_id=artifact_id,
        path=path.relative_to(root).as_posix(),
        artifact_type=_optional_text(metadata.get("artifact_type")),
        semantic_type=_optional_text(semantic_type),
        subtype=_optional_text(subtype),
        layer=_layer_from_id(node_id),
        scope_kind=_optional_text(scope_kind),
        scope_id=_optional_text(scope_id),
        relations=relations,
    )


def _register_aliases(
    node: RelationNode,
    path: Path,
    aliases: dict[str, str],
    alias_paths: dict[str, Path],
    diagnostics: list[Diagnostic],
) -> None:
    for alias in {node.artifact_id, node.id}:
        previous = aliases.get(alias)
        if previous is not None and alias_paths[alias] != path:
            diagnostics.append(_diag(path, f"duplicate relation ID: {alias}"))
            continue
        aliases[alias] = node.id
        alias_paths[alias] = path


def _resolve_nodes(
    root: Path,
    raw_nodes: list[_RawNode],
    aliases: dict[str, str],
    known: set[str],
    inactive: set[str],
    diagnostics: list[Diagnostic],
) -> dict[str, RelationNode]:
    nodes: dict[str, RelationNode] = {}
    for raw in raw_nodes:
        resolved = tuple(
            _resolve_relation(raw, item, aliases, known, inactive, diagnostics)
            for item in raw.node.relations
        )
        nodes[raw.node.id] = RelationNode(
            **{**raw.node.__dict__, "relations": resolved},
        )
    _validate_resolved_uniqueness(root, nodes, diagnostics)
    return nodes


def _resolve_relation(
    raw: _RawNode,
    relation: ArtifactRelation,
    aliases: dict[str, str],
    known: set[str],
    inactive: set[str],
    diagnostics: list[Diagnostic],
) -> ArtifactRelation:
    if relation.target is None:
        return relation
    canonical = aliases.get(relation.target, relation.target)
    unresolved = relation.target not in known
    legacy_inactive = raw.node.id in inactive and relation.origin == "legacy_child_of"
    if unresolved and not legacy_inactive:
        diagnostics.append(
            _diag(raw.path, f"unresolved {relation.type} target: {relation.target}")
        )
    if canonical == raw.node.id and not legacy_inactive:
        diagnostics.append(
            _diag(raw.path, f"artifact cannot be {relation.type} itself: {canonical}")
        )
    return ArtifactRelation(relation.type, canonical, relation.range, relation.origin)


def _parse_relation(
    path: Path,
    value: object,
    diagnostics: list[Diagnostic],
) -> ArtifactRelation | None:
    if not isinstance(value, dict):
        diagnostics.append(_diag(path, "every relation must be a mapping"))
        return None
    relation_type = value.get("type")
    if relation_type not in RELATION_TYPES:
        diagnostics.append(_diag(path, f"unknown relation type: {relation_type}"))
        return None
    allowed = {"type", "target", "range"}
    if set(value) - allowed:
        diagnostics.append(_diag(path, "relation has unknown or inverse fields"))
        return None
    has_target = "target" in value
    has_range = "range" in value
    if has_target == has_range:
        diagnostics.append(_diag(path, "relation requires exactly one target or range"))
        return None
    if has_range:
        if relation_type != "projection_of":
            diagnostics.append(_diag(path, "only projection_of accepts a range"))
            return None
        parsed_range = _parse_range(path, value["range"], diagnostics)
        return (
            ArtifactRelation(str(relation_type), None, parsed_range, "authored")
            if parsed_range is not None
            else None
        )
    target = value.get("target")
    if not isinstance(target, str) or not ID_PATTERN.fullmatch(target):
        diagnostics.append(_diag(path, f"invalid {relation_type} target: {target}"))
        return None
    return ArtifactRelation(str(relation_type), target, None, "authored")


def _parse_range(
    path: Path,
    value: object,
    diagnostics: list[Diagnostic],
) -> ProjectionRange | None:
    if not isinstance(value, dict):
        diagnostics.append(_diag(path, "projection range must be a mapping"))
        return None
    allowed = {"semantic_type", "subtype", "layer", "scope", "through"}
    if set(value) - allowed:
        diagnostics.append(_diag(path, "projection range has unknown fields"))
        return None
    semantic_type = value.get("semantic_type")
    subtype = value.get("subtype")
    layer = value.get("layer")
    scope = value.get("scope")
    through = value.get("through")
    valid = semantic_type in SEMANTIC_TYPES
    valid = valid and _valid_range_subtype(semantic_type, subtype)
    valid = valid and (layer is None or layer in LAYERS)
    if not isinstance(scope, dict):
        diagnostics.append(_diag(path, "invalid projection range selector"))
        return None
    valid = valid and set(scope) == {"kind", "id"}
    valid = valid and scope.get("kind") in SCOPE_KINDS
    scope_id = scope.get("id")
    valid = valid and isinstance(scope_id, str) and bool(scope_id)
    valid = valid and isinstance(through, str) and bool(ATOM_PATTERN.search(through))
    if not valid or not isinstance(scope_id, str):
        diagnostics.append(_diag(path, "invalid projection range selector"))
        return None
    return ProjectionRange(
        semantic_type=str(semantic_type),
        subtype=str(subtype) if subtype is not None else None,
        layer=str(layer) if layer is not None else None,
        scope_kind=str(scope["kind"]),
        scope_id=scope_id,
        through=str(through),
    )


def _parse_legacy_child_of(
    path: Path,
    value: object,
    diagnostics: list[Diagnostic],
) -> tuple[ArtifactRelation, ...]:
    if not isinstance(value, list) or not value:
        diagnostics.append(
            _diag(path, "legacy child_of must be a non-empty list of canonical IDs")
        )
        return ()
    targets: list[str] = []
    for target in value:
        if not isinstance(target, str) or not ID_PATTERN.fullmatch(target):
            diagnostics.append(_diag(path, f"invalid legacy child_of target: {target}"))
            continue
        targets.append(target)
    if len(set(targets)) != len(targets):
        diagnostics.append(_diag(path, "legacy child_of targets must be unique"))
    return tuple(
        ArtifactRelation("child_of", target, None, "legacy_child_of")
        for target in dict.fromkeys(targets)
    )


def _validate_local_uniqueness(
    path: Path,
    relations: list[ArtifactRelation],
    diagnostics: list[Diagnostic],
) -> None:
    keys = [_local_relation_key(item) for item in relations]
    if len(set(keys)) != len(keys):
        diagnostics.append(_diag(path, "relations must be unique"))
    targets = [item.target for item in relations if item.target is not None]
    if len(set(targets)) != len(targets):
        diagnostics.append(
            _diag(path, "one source-target pair must have one primary relation")
        )


def _validate_resolved_uniqueness(
    root: Path,
    nodes: dict[str, RelationNode],
    diagnostics: list[Diagnostic],
) -> None:
    for node in nodes.values():
        targets = [item.target for item in node.relations if item.target is not None]
        if len(set(targets)) != len(targets):
            diagnostics.append(
                _diag(
                    root / node.path,
                    "aliased source-target pair has more than one primary relation",
                )
            )


def _range_diagnostics(
    root: Path,
    nodes: dict[str, RelationNode],
    inactive: set[str],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    by_artifact = {node.artifact_id: node for node in nodes.values()}
    for node in nodes.values():
        for relation in node.relations:
            selector = relation.range
            if selector is None:
                continue
            through = by_artifact.get(selector.through)
            if through is None or through.artifact_type != "atomic_record":
                diagnostics.append(
                    _diag(
                        root / node.path,
                        "projection through must name an atom carrier",
                    )
                )
                continue
            candidates = [
                item
                for item in nodes.values()
                if _range_matches(item, selector) and item.id not in inactive
            ]
            if through not in candidates:
                diagnostics.append(
                    _diag(root / node.path, "projection frontier is outside its range")
                )
                continue
            latest = max(candidates, key=lambda item: _atom_sequence(item.artifact_id))
            if latest.artifact_id != selector.through:
                diagnostics.append(
                    _diag(
                        root / node.path,
                        f"stale projection frontier: latest is {latest.artifact_id}",
                    )
                )
    return diagnostics


def _range_matches(node: RelationNode, selector: ProjectionRange) -> bool:
    if node.artifact_type != "atomic_record":
        return False
    if node.semantic_type != selector.semantic_type:
        return False
    if selector.subtype is not None and (node.subtype or "none") != selector.subtype:
        return False
    if selector.layer is not None and node.layer != selector.layer:
        return False
    return (
        node.scope_kind == selector.scope_kind and node.scope_id == selector.scope_id
    )


def _replacement_diagnostics(
    root: Path,
    nodes: dict[str, RelationNode],
) -> list[Diagnostic]:
    absorbed = _absorption_edges(root)
    diagnostics: list[Diagnostic] = []
    for node in nodes.values():
        for relation in node.relations:
            if relation.type != "replacement_of" or relation.target is None:
                continue
            if absorbed.get(relation.target) != node.id:
                diagnostics.append(
                    _diag(
                        root / node.path,
                        "replacement_of requires matching append-only absorption",
                    )
                )
    return diagnostics


def _source_diagnostics(
    root: Path,
    nodes: dict[str, RelationNode],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for node in nodes.values():
        for relation in node.relations:
            if relation.origin == "legacy_child_of":
                continue
            message = _source_error(node, relation.type)
            if message is not None:
                diagnostics.append(_diag(root / node.path, message))
    return diagnostics


def _source_error(node: RelationNode, relation_type: str) -> str | None:
    if relation_type == "analysis_of" and node.artifact_type != "analysis_report":
        return "analysis_of must originate from an Analysis Report"
    if (
        relation_type == "projection_of"
        and node.artifact_type not in PROJECTION_SOURCE_TYPES
    ):
        return "projection_of must originate from an evergreen artifact"
    if relation_type == "check_of" and not (
        node.semantic_type == "qa" and node.subtype in {"test", "evaluation"}
    ):
        return "check_of must originate from a Test or Evaluation atom"
    if relation_type == "evidence_for" and node.artifact_type != "evidence_record":
        return "evidence_for must originate from an Evidence Record"
    if relation_type == "override_of" and node.semantic_type != "decision":
        return "override_of must originate from Decision authority"
    if relation_type == "replacement_of" and node.artifact_type != "atomic_record":
        return "replacement_of must originate from an atomic artifact"
    if relation_type == "implementation_of" and node.artifact_type != "implementation":
        return "implementation_of must originate from implementation or a commit"
    return None


def _cycle_diagnostics(
    root: Path,
    nodes: dict[str, RelationNode],
    inactive: set[str],
) -> list[Diagnostic]:
    graph: dict[str, list[str]] = {}
    for identifier, node in nodes.items():
        graph[identifier] = [
            str(item.target)
            for item in node.relations
            if item.type in ACYCLIC_RELATION_TYPES and item.target in nodes
        ]
    diagnostics: list[Diagnostic] = []
    state: dict[str, int] = {}
    for identifier in sorted(set(nodes) - inactive):
        _visit_cycle(identifier, [], graph, nodes, inactive, state, diagnostics, root)
    return diagnostics


def _visit_cycle(
    identifier: str,
    stack: list[str],
    graph: dict[str, list[str]],
    nodes: dict[str, RelationNode],
    inactive: set[str],
    state: dict[str, int],
    diagnostics: list[Diagnostic],
    root: Path,
) -> None:
    if state.get(identifier) == 2:
        return
    if state.get(identifier) == 1:
        start = stack.index(identifier)
        cycle = [*stack[start:], identifier]
        diagnostics.append(
            _diag(
                root / nodes[identifier].path,
                "artifact relation cycle: " + " -> ".join(cycle),
            )
        )
        return
    state[identifier] = 1
    stack.append(identifier)
    for target in graph.get(identifier, []):
        if target not in inactive:
            _visit_cycle(
                target,
                stack,
                graph,
                nodes,
                inactive,
                state,
                diagnostics,
                root,
            )
    stack.pop()
    state[identifier] = 2


def _commit_relations(record: str) -> list[dict[str, Any]]:
    record = record.strip()
    if not record or "\x1f" not in record:
        return []
    commit, body = record.split("\x1f", 1)
    implements: set[str] = set()
    sessions: set[str] = set()
    for line in body.splitlines():
        if line.startswith("Implements:"):
            implements.update(re.findall(r"[A-Z0-9]+(?:-[A-Z0-9]+)+", line))
        elif line.startswith("Session:"):
            value = line.partition(":")[2].strip()
            if SESSION_PATTERN.fullmatch(value):
                sessions.add(value)
    return [
        {
            "source": commit,
            "source_kind": "commit",
            "type": "implementation_of",
            "target": target,
            "origin": "commit_trailer",
            "llm_session_ids": sorted(sessions),
        }
        for target in sorted(implements)
    ]


def _relation_sort_key(item: dict[str, Any]) -> tuple[str, str, str]:
    target = item.get("target")
    if target is None:
        target = repr(item.get("range", {}))
    return str(item["source"]), str(item["type"]), str(target)


def _local_relation_key(relation: ArtifactRelation) -> tuple[str, str]:
    locator = relation.target or repr(relation.range)
    return relation.type, locator


def _reject_reverse_fields(
    path: Path,
    metadata: dict[str, Any],
    diagnostics: list[Diagnostic],
) -> None:
    present = sorted(REVERSE_FIELDS & set(metadata))
    if present:
        diagnostics.append(
            _diag(path, "reverse relations must not be authored: " + ", ".join(present))
        )


def _known_relation_ids(root: Path) -> set[str]:
    identifiers: set[str] = set()
    layout = discover_layout(root)
    if layout.intake_path.is_file():
        data = load(layout.intake_path)
        items = data.get("items", []) if isinstance(data, dict) else []
        identifiers.update(
            str(item["id"])
            for item in items
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        )
    for path in sorted(root.rglob("package.yaml")):
        identifiers.update(_package_ids(path))
    return identifiers


def _package_ids(path: Path) -> set[str]:
    try:
        data = load(path)
    except (OSError, UnicodeError, YamlSubsetError):
        return set()
    if not isinstance(data, dict):
        return set()
    identifiers: set[str] = set()
    for value in data.values():
        if isinstance(value, list):
            identifiers.update(
                str(item)
                for item in value
                if isinstance(item, str) and ID_PATTERN.fullmatch(item)
            )
    return identifiers


def _frontmatter(path: Path) -> dict[str, Any] | None:
    try:
        data = frontmatter_metadata(path)
    except (OSError, UnicodeError, FrontmatterError):
        return None
    return data if isinstance(data, dict) else None


def _inactive_semantic_ids(root: Path) -> set[str]:
    current: dict[str, str] = {}
    for event in _lifecycle_events(root):
        atom_id = event.get("atom_id")
        kind = event.get("event")
        if (
            isinstance(atom_id, str)
            and isinstance(kind, str)
            and kind != "priority_changed"
        ):
            current[atom_id] = kind
    return {
        identifier for identifier, kind in current.items() if kind in INACTIVE_EVENTS
    }


def _absorption_edges(root: Path) -> dict[str, str]:
    edges: dict[str, str] = {}
    for event in _lifecycle_events(root):
        related = event.get("related")
        if event.get("event") != "absorbed" or not isinstance(related, list):
            continue
        if len(related) == 1:
            edges[str(event.get("atom_id"))] = str(related[0])
    return edges


def _lifecycle_events(root: Path) -> list[dict[str, Any]]:
    path = discover_layout(root).governance_root / "lifecycle.yaml"
    if not path.is_file():
        return []
    try:
        data = load(path)
    except (OSError, UnicodeError, YamlSubsetError):
        return []
    values = data.get("events", []) if isinstance(data, dict) else []
    return [item for item in values if isinstance(item, dict)]


def _layer_from_id(identifier: str) -> str | None:
    for segment in identifier.split("-"):
        lowered = segment.lower()
        if lowered in LAYERS:
            return lowered
    return None


def _atom_sequence(identifier: str) -> int:
    match = ATOM_PATTERN.search(identifier)
    return int(match.group(1)) if match else -1


def _optional_text(value: object) -> str | None:
    return str(value) if isinstance(value, str) else None


def _valid_range_subtype(semantic_type: object, subtype: object) -> bool:
    if subtype is None:
        return True
    if not isinstance(semantic_type, str) or not isinstance(subtype, str):
        return False
    if subtype == "none":
        return semantic_type != "qa"
    return subtype in SEMANTIC_SUBTYPES.get(semantic_type, frozenset())


def _diag(path: Path, message: str) -> Diagnostic:
    return Diagnostic("DSET-E158", path, message)
