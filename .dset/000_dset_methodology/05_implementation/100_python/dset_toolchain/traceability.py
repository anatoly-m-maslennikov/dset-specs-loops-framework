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
    root = root.resolve()
    layout = discover_layout(root)
    history = load(layout.history_path)
    changes: list[dict[str, Any]] = []
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
    for path in sorted(candidates, key=lambda item: item.name):
        manifest = layout.structured_file(path, "change.yaml")
        if not manifest.is_file():
            continue
        data = load(manifest)
        evidence_root = path / "proofs"
        evidence = []
        if evidence_root.is_dir():
            evidence = [
                item.name
                for item in sorted(evidence_root.rglob("*"))
                if item.is_file() and item.name != "README.md"
            ]
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
            "evidence": evidence,
        }
        if layout.layered:
            entry["slug"] = data.get("slug")
            entry["primary_layer"] = data.get("primary_layer")
            entry["affected_layers"] = sorted(data.get("affected_layers", []))
            target = data.get("target")
            if isinstance(target, dict):
                work_areas = target.get("work_areas")
                entry["target"] = {
                    "repository": target.get("repository"),
                    "work_areas": (
                        sorted(work_areas)
                        if isinstance(work_areas, list)
                        and all(isinstance(item, str) for item in work_areas)
                        else work_areas
                    ),
                }
            else:
                entry["target"] = target
            entry["workspace"] = data.get("workspace")
            entry["dependencies"] = sorted(
                data.get("dependencies", []),
                key=lambda item: (
                    str(item.get("change_id", "")) if isinstance(item, dict) else ""
                ),
            )
        changes.append(entry)
    changes.sort(key=lambda item: item["id"])
    return {
        "schema_version": "1.3" if layout.layered else 1.1,
        "repository": history["repository"],
        "changes": changes,
        "semantic_classifications": build_semantic_classification_index(root),
        "semantic_atoms": build_semantic_atom_index(root),
        "relations": build_relation_index(root),
    }


def rendered_traceability(root: Path) -> str:
    path = discover_layout(root).traceability_path
    return dump(build_traceability(root), path)


def trace_is_fresh(root: Path) -> bool:
    path = discover_layout(root).traceability_path
    return path.is_file() and path.read_text(encoding="utf-8") == rendered_traceability(
        root
    )


def write_traceability(root: Path) -> Path:
    path = discover_layout(root).traceability_path
    content = rendered_traceability(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)
    return path
