"""Provide DSET traceability behavior."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .layout import discover_layout
from .lineage import build_relation_index
from .semantic_atoms import build_semantic_atom_index
from .semantic_types import build_semantic_classification_index
from .yaml_subset import dump, load


def build_traceability(root: Path) -> dict[str, Any]:
    """Build traceability using the declared repository contract."""
    root = root.resolve()
    layout = discover_layout(root)
    history = load(layout.history_path)
    changes = [_change_entry(layout, path) for path in _change_paths(layout)]
    changes = [item for item in changes if item is not None]
    changes.sort(key=lambda item: item["id"])
    return {
        "schema_version": "1.3" if layout.layered else 1.1,
        "repository": history["repository"],
        "changes": changes,
        "semantic_classifications": build_semantic_classification_index(root),
        "semantic_atoms": build_semantic_atom_index(root),
        "relations": build_relation_index(root),
    }


def _change_paths(layout: Any) -> list[Path]:
    """Enumerate active and archived Change directories once."""
    candidates: list[Path] = []
    for change_root in layout.active_change_roots:
        if change_root.is_dir():
            candidates.extend(
                path
                for path in change_root.iterdir()
                if path.is_dir() and path.name != "archive"
            )
    for archive in layout.archive_change_roots:
        if archive.is_dir():
            candidates.extend(path for path in archive.iterdir() if path.is_dir())
    return sorted(candidates, key=lambda item: item.name)


def _change_entry(layout: Any, path: Path) -> dict[str, Any] | None:
    """Render one Change manifest and its evidence inventory."""
    manifest = layout.structured_file(path, "change.yaml")
    if not manifest.is_file():
        return None
    data = load(manifest)
    pr = data.get("pull_request", {})
    entry = {
        "id": data["id"],
        "status": data["status"],
        "packages": sorted(data.get("packages", [])),
        "requirements": sorted(data.get("requirements", [])),
        "tests": sorted(data.get("tests", [])),
        "evals": sorted(data.get("evals", [])),
        "intake": sorted(data.get("intake", [])),
        "decisions": sorted(data.get("decisions", data.get("adrs", []))),
        "contracts": sorted(data.get("contracts", [])),
        "stories": sorted(data.get("stories", [])),
        "outcomes": sorted(data.get("outcomes", [])),
        "pull_request": pr.get("url", "pending"),
        "evidence": _evidence_names(path / "proofs"),
    }
    if layout.layered:
        entry.update(_layered_change_fields(data))
    return entry


def _evidence_names(root: Path) -> list[str]:
    """List non-hub proof carrier names under one Change."""
    if not root.is_dir():
        return []
    return [
        item.name
        for item in sorted(root.rglob("*"))
        if item.is_file() and item.name != "README.md"
    ]


def _layered_change_fields(data: dict[str, Any]) -> dict[str, Any]:
    """Render the fields present only in layered Change manifests."""
    target = data.get("target")
    rendered_target = _render_target(target) if isinstance(target, dict) else target
    dependencies = sorted(
        data.get("dependencies", []),
        key=lambda item: (
            str(item.get("change_id", "")) if isinstance(item, dict) else ""
        ),
    )
    return {
        "slug": data.get("slug"),
        "primary_layer": data.get("primary_layer"),
        "affected_layers": sorted(data.get("affected_layers", [])),
        "target": rendered_target,
        "workspace": data.get("workspace"),
        "dependencies": dependencies,
    }


def _render_target(target: dict[str, Any]) -> dict[str, Any]:
    """Normalize the work-area list of a layered Change target."""
    work_areas = target.get("work_areas")
    if isinstance(work_areas, list) and all(
        isinstance(item, str) for item in work_areas
    ):
        work_areas = sorted(work_areas)
    return {"repository": target.get("repository"), "work_areas": work_areas}


def rendered_traceability(root: Path) -> str:
    """Handle traceability using the declared repository contract."""
    path = discover_layout(root).traceability_path
    return dump(build_traceability(root), path)


def trace_is_fresh(root: Path) -> bool:
    """Handle is fresh using the declared repository contract."""
    path = discover_layout(root).traceability_path
    return path.is_file() and path.read_text(encoding="utf-8") == rendered_traceability(
        root
    )


def write_traceability(root: Path) -> Path:
    """Write traceability using the declared repository contract."""
    path = discover_layout(root).traceability_path
    content = rendered_traceability(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)
    return path
