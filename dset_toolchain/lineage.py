from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .diagnostics import Diagnostic
from .yaml_subset import YamlSubsetError, loads

ID_PATTERN = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)+$")
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
class LineageNode:
    id: str
    artifact_id: str
    path: str
    child_of: tuple[str, ...]


@dataclass(frozen=True)
class _RawNode:
    id: str
    artifact_id: str
    path: Path
    child_of: tuple[str, ...]


def collect_artifact_lineage(
    root: Path,
) -> tuple[dict[str, LineageNode], list[Diagnostic]]:
    """Collect and validate authored child-owned artifact lineage."""
    root = root.resolve()
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
        if "parent_to" in metadata:
            diagnostics.append(
                Diagnostic(
                    "DSET-E158",
                    path,
                    "parent_to is derived and must not be authored",
                )
            )
        raw_parents = metadata.get("child_of")
        artifact_id = metadata.get("artifact_id")
        if artifact_id is None:
            if raw_parents is not None or "parent_to" in metadata:
                diagnostics.append(
                    Diagnostic(
                        "DSET-E158",
                        path,
                        "artifact lineage requires artifact_id",
                    )
                )
            continue
        if not isinstance(artifact_id, str) or not ID_PATTERN.fullmatch(artifact_id):
            continue

        semantic_id = metadata.get("semantic_id")
        node_id = artifact_id
        if (
            metadata.get("artifact_type") == "atomic_record"
            and isinstance(semantic_id, str)
            and ID_PATTERN.fullmatch(semantic_id)
        ):
            node_id = semantic_id

        parents = _validate_parent_list(path, raw_parents, diagnostics)
        raw_nodes.append(_RawNode(node_id, artifact_id, path, parents))
        for alias in {artifact_id, node_id}:
            previous = aliases.get(alias)
            if previous is not None and alias_paths[alias] != path:
                diagnostics.append(
                    Diagnostic(
                        "DSET-E158",
                        path,
                        f"duplicate lineage ID: {alias}",
                    )
                )
            else:
                aliases[alias] = node_id
                alias_paths[alias] = path

    nodes: dict[str, LineageNode] = {}
    for raw in raw_nodes:
        canonical_parents: list[str] = []
        for parent in raw.child_of:
            canonical = aliases.get(parent)
            if canonical is None:
                diagnostics.append(
                    Diagnostic(
                        "DSET-E158",
                        raw.path,
                        f"unresolved child_of ID: {parent}",
                    )
                )
                continue
            if canonical == raw.id:
                diagnostics.append(
                    Diagnostic(
                        "DSET-E158",
                        raw.path,
                        f"artifact cannot be child_of itself: {parent}",
                    )
                )
                continue
            canonical_parents.append(canonical)
        nodes[raw.id] = LineageNode(
            id=raw.id,
            artifact_id=raw.artifact_id,
            path=raw.path.relative_to(root).as_posix(),
            child_of=tuple(canonical_parents),
        )

    diagnostics.extend(_cycle_diagnostics(root, nodes))
    return nodes, sorted(set(diagnostics))


def derived_parent_to(nodes: dict[str, LineageNode]) -> dict[str, tuple[str, ...]]:
    reverse: dict[str, list[str]] = {identifier: [] for identifier in nodes}
    for child, node in nodes.items():
        for parent in node.child_of:
            if parent in reverse:
                reverse[parent].append(child)
    return {
        identifier: tuple(sorted(children)) for identifier, children in reverse.items()
    }


def transitive_ancestors(
    nodes: dict[str, LineageNode], identifier: str
) -> tuple[str, ...]:
    found: set[str] = set()
    pending = list(nodes.get(identifier, LineageNode("", "", "", ())).child_of)
    while pending:
        parent = pending.pop()
        if parent in found:
            continue
        found.add(parent)
        if parent in nodes:
            pending.extend(nodes[parent].child_of)
    return tuple(sorted(found))


def build_lineage_index(root: Path) -> list[dict[str, Any]]:
    nodes, _ = collect_artifact_lineage(root)
    reverse = derived_parent_to(nodes)
    return [
        {
            "id": node.id,
            "artifact_id": node.artifact_id,
            "path": node.path,
            "child_of": list(node.child_of),
            "parent_to": list(reverse[node.id]),
        }
        for node in sorted(nodes.values(), key=lambda item: item.id)
    ]


def validate_artifact_lineage(root: Path) -> list[Diagnostic]:
    _, diagnostics = collect_artifact_lineage(root)
    return diagnostics


def _frontmatter(path: Path) -> dict[str, Any] | None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return None
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = lines.index("---", 1)
        data = loads("\n".join(lines[1:end]))
    except (ValueError, YamlSubsetError):
        return None
    return data if isinstance(data, dict) else None


def _validate_parent_list(
    path: Path,
    value: object,
    diagnostics: list[Diagnostic],
) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or not value:
        diagnostics.append(
            Diagnostic(
                "DSET-E158",
                path,
                "child_of must be a non-empty list of canonical IDs",
            )
        )
        return ()
    parents: list[str] = []
    for parent in value:
        if not isinstance(parent, str) or not ID_PATTERN.fullmatch(parent):
            diagnostics.append(
                Diagnostic(
                    "DSET-E158",
                    path,
                    f"invalid child_of ID: {parent}",
                )
            )
            continue
        parents.append(parent)
    if len(set(parents)) != len(parents):
        diagnostics.append(Diagnostic("DSET-E158", path, "child_of IDs must be unique"))
    return tuple(dict.fromkeys(parents))


def _cycle_diagnostics(root: Path, nodes: dict[str, LineageNode]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    state: dict[str, int] = {}
    reported: set[str] = set()

    def visit(identifier: str, stack: list[str]) -> None:
        marker = state.get(identifier, 0)
        if marker == 2:
            return
        if marker == 1:
            start = stack.index(identifier)
            cycle = stack[start:]
            key = " -> ".join([*cycle, identifier])
            if key not in reported:
                reported.add(key)
                diagnostics.append(
                    Diagnostic(
                        "DSET-E158",
                        root / nodes[identifier].path,
                        f"artifact lineage cycle: {key}",
                    )
                )
            return
        state[identifier] = 1
        stack.append(identifier)
        for parent in nodes[identifier].child_of:
            if parent in nodes:
                visit(parent, stack)
        stack.pop()
        state[identifier] = 2

    for identifier in sorted(nodes):
        visit(identifier, [])
    return diagnostics
