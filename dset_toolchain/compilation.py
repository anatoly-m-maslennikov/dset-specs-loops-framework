from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from .layout import discover_layout
from .semantic_atoms import collect_semantic_atoms
from .yaml_subset import YamlSubsetError, dump, load

DECISION_FIELDS = ("requirements", "contracts", "stories", "outcomes")
INACTIVE_EVENTS = frozenset({"absorbed", "rejected", "retired", "withdrawn"})
IGNORED_PARTS = frozenset(
    {
        ".git",
        ".cache",
        ".dset",
        ".venv",
        "__pycache__",
        "dist",
        "generated",
        "templates",
    }
)


def build_compilation_index(root: Path) -> dict[str, Any]:
    root = root.resolve()
    sources = _authority_sources(root)
    projections = _projection_paths(root)
    records: list[dict[str, Any]] = []
    missing: list[str] = []
    for identifier, source in sorted(sources.items()):
        owners = [
            (path, _projection_fragments(path, identifier)) for path in projections
        ]
        owners = [(path, fragments) for path, fragments in owners if fragments]
        if not owners:
            missing.append(identifier)
            continue
        records.append(
            {
                "id": identifier,
                "source": {
                    "path": source.relative_to(root).as_posix(),
                    "sha256": _digest(source),
                },
                "projections": [
                    {
                        "path": path.relative_to(root).as_posix(),
                        "sha256": _digest(path),
                        "fragments": fragments,
                    }
                    for path, fragments in owners
                ],
            }
        )
    if missing:
        raise ValueError(
            "active Decision authority lacks an evergreen projection: "
            + ", ".join(missing)
        )
    return {
        "schema_version": "1.0",
        "records": records,
    }


def compilation_path(root: Path) -> Path:
    layout = discover_layout(root.resolve())
    generated = (
        layout.traceability_path.parent
        if layout.layered
        else layout.dset_root / "generated"
    )
    suffix = ".toml" if layout.manifest_path.suffix == ".toml" else ".yaml"
    return layout.structured_file(generated, f"compilation{suffix}")


def rendered_compilation(root: Path) -> str:
    return dump(build_compilation_index(root), compilation_path(root))


def compilation_is_fresh(root: Path) -> bool:
    path = compilation_path(root)
    try:
        rendered = rendered_compilation(root)
    except ValueError:
        return False
    return path.is_file() and path.read_text(encoding="utf-8") == rendered


def write_compilation(root: Path) -> Path:
    path = compilation_path(root)
    content = rendered_compilation(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)
    return path


def active_authority_ids(root: Path) -> set[str]:
    return set(_authority_sources(root.resolve()))


def projected_authority_ids(root: Path) -> set[str]:
    """Return authorities with an explicit evergreen claim fragment."""
    root = root.resolve()
    sources = _authority_sources(root)
    projections = _projection_paths(root)
    return {
        identifier
        for identifier in sources
        if any(_projection_fragments(path, identifier) for path in projections)
    }


def _authority_sources(root: Path) -> dict[str, Path]:
    lifecycle = _lifecycle_status(root)
    sources: dict[str, Path] = {}
    atoms, diagnostics = collect_semantic_atoms(root)
    if diagnostics:
        raise ValueError(diagnostics[0].message)
    for atom in atoms.values():
        if (
            atom.semantic_type == "decision"
            and atom.emission_status == "accepted"
            and lifecycle.get(atom.semantic_id) not in INACTIVE_EVENTS
        ):
            sources[atom.semantic_id] = root / atom.path
    for path in root.rglob("decision-*.md"):
        if _ignored(root, path):
            continue
        text = _read(path)
        match = re.search(r"\*\*Decision ID:\*\*\s*`([^`]+)`", text)
        if not match or "**Status:** accepted" not in text:
            continue
        identifier = match.group(1)
        if lifecycle.get(identifier) not in INACTIVE_EVENTS:
            sources[identifier] = path
    for path in discover_layout(root).structured_named_files(root, "package"):
        if _ignored(root, path) or "specs" not in path.parts:
            continue
        try:
            data = load(path)
        except (OSError, UnicodeError, YamlSubsetError):
            continue
        if not isinstance(data, dict):
            continue
        for field in DECISION_FIELDS:
            values = data.get(field, [])
            if not isinstance(values, list):
                continue
            for identifier in values:
                if (
                    isinstance(identifier, str)
                    and lifecycle.get(identifier) not in INACTIVE_EVENTS
                ):
                    sources.setdefault(identifier, path)
    return sources


def _projection_paths(root: Path) -> list[Path]:
    return [
        path
        for path in sorted(root.rglob("*.md"))
        if not _ignored(root, path)
        and ("specs" in path.parts or "governance" in path.parts)
    ]


def _lifecycle_status(root: Path) -> dict[str, str]:
    layout = discover_layout(root)
    path = layout.structured_file(layout.governance_root, "lifecycle.toml")
    if not path.is_file():
        return {}
    data = load(path)
    events = data.get("events", []) if isinstance(data, dict) else []
    return {
        str(item.get("atom_id")): str(item.get("event"))
        for item in events
        if isinstance(item, dict)
    }


def _ignored(root: Path, path: Path) -> bool:
    relative = path.relative_to(root)
    return any(
        part in IGNORED_PARTS or (part.startswith(".") and part != ".github")
        for part in relative.parts
    )


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""


def _projection_fragments(path: Path, identifier: str) -> list[dict[str, Any]]:
    """Extract only explicit evergreen claim structures, never loose mentions."""
    lines = _read(path).splitlines()
    fragments: list[dict[str, Any]] = []
    escaped = re.escape(identifier)
    heading = re.compile(rf"^(#{{1,6}})\s+`?{escaped}`?(?:\s|$)")
    table = re.compile(rf"^\|\s*`?{escaped}`?\s*\|")
    labeled = re.compile(rf"^\*\*[^*\n]*\b{escaped}\b[^*\n]*:\*\*")
    for index, line in enumerate(lines):
        match = heading.match(line)
        kind: str | None = None
        end = index + 1
        if match:
            kind = "section"
            level = len(match.group(1))
            while end < len(lines):
                next_heading = re.match(r"^(#{1,6})\s+", lines[end])
                if next_heading and len(next_heading.group(1)) <= level:
                    break
                end += 1
        elif table.match(line):
            kind = "table-row"
        elif labeled.match(line):
            kind = "labeled-block"
            while end < len(lines) and lines[end].strip():
                end += 1
        if kind is None:
            continue
        content = "\n".join(lines[index:end]).strip()
        fragments.append(
            {
                "kind": kind,
                "line": index + 1,
                "sha256": hashlib.sha256(content.encode()).hexdigest(),
            }
        )
    return fragments


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
