from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

from .governance import validate_governance
from .layout import discover_layout, has_manifest
from .runtime_bridge import start_runtime
from .semantic_types import build_semantic_classification_index
from .settings import load_project_settings
from .skill_catalog import (
    PUBLIC_SKILL_MODES,
    PUBLIC_SKILL_WORKFLOWS,
)
from .yaml_subset import load

CONTEXT_SCHEMA_VERSION = "1.0"


def resolve_skill_context(
    target: Path,
    *,
    skill_id: str,
    objective: str,
    session_id: str | None = None,
    llm_session_ids: Sequence[str] = (),
) -> dict[str, object]:
    """Resolve one explicit target into its project-owned DSET workflow context."""

    if skill_id not in PUBLIC_SKILL_WORKFLOWS:
        raise ValueError(f"unknown public skill: {skill_id}")
    requested = target.resolve()
    if skill_id == "dset-init":
        return _initialization_context(requested, skill_id)

    root = _find_unique_repository(requested)
    if skill_id == "dset-repair-governance":
        return _repair_context(requested, root, skill_id)

    scope, work_area = _target_scope(root, requested)
    started = start_runtime(
        root,
        public_entrypoint=skill_id,
        workflow_id=PUBLIC_SKILL_WORKFLOWS[skill_id],
        objective=objective,
        mode_id=PUBLIC_SKILL_MODES[skill_id],
        session_id=session_id,
        llm_session_ids=llm_session_ids,
        scope=scope,
    )
    resolved = started["resolved"]
    assert isinstance(resolved, dict)
    checkpoint = started["checkpoint"]
    assert isinstance(checkpoint, dict)
    settings, settings_issues = load_project_settings(root)
    if settings_issues:
        raise ValueError("; ".join(settings_issues))
    semantic_index = build_semantic_classification_index(root)
    return {
        "schema_version": CONTEXT_SCHEMA_VERSION,
        "status": "resolved",
        "target": str(requested),
        "repository_root": str(root),
        "work_area": work_area,
        "skill_id": skill_id,
        "workflow_id": PUBLIC_SKILL_WORKFLOWS[skill_id],
        "mode_id": PUBLIC_SKILL_MODES[skill_id],
        "manifest": discover_layout(root).manifest_path.relative_to(root).as_posix(),
        "governance": discover_layout(root)
        .governance_path.relative_to(root)
        .as_posix(),
        "ruleset_identity": _run_ruleset_identity(started["run"]),
        "artifact_creation_strictness": settings.artifact_creation_strictness,
        "semantic_routing": {
            "types": ["decision", "question", "problem", "qa"],
            "classification_count": len(semantic_index),
            "compatibility_count": sum(
                1 for item in semantic_index if item["compatibility"]
            ),
            "source": discover_layout(root)
            .governance_root.joinpath("governance/work-items.md")
            .relative_to(root)
            .as_posix(),
        },
        "resolved": resolved,
        "run": started["run"],
        "checkpoint": checkpoint,
        "closure": checkpoint["closure"],
    }


def _initialization_context(target: Path, skill_id: str) -> dict[str, object]:
    try:
        root = _find_unique_repository(target)
    except FileNotFoundError:
        return {
            "schema_version": CONTEXT_SCHEMA_VERSION,
            "status": "initialization-required",
            "target": str(target),
            "repository_root": None,
            "work_area": None,
            "skill_id": skill_id,
            "workflow_id": PUBLIC_SKILL_WORKFLOWS[skill_id],
            "mode_id": PUBLIC_SKILL_MODES[skill_id],
            "resolved": None,
            "run": None,
            "checkpoint": None,
        }
    raise ValueError(f"DSET project already exists at: {root}")


def _repair_context(target: Path, root: Path, skill_id: str) -> dict[str, object]:
    diagnostics = validate_governance(root)
    if not diagnostics:
        raise ValueError(f"DSET governance is valid at: {root}")
    return {
        "schema_version": CONTEXT_SCHEMA_VERSION,
        "status": "invalid-governance",
        "target": str(target),
        "repository_root": str(root),
        "work_area": None,
        "skill_id": skill_id,
        "workflow_id": PUBLIC_SKILL_WORKFLOWS[skill_id],
        "mode_id": PUBLIC_SKILL_MODES[skill_id],
        "diagnostics": [item.render(root) for item in diagnostics],
        "resolved": None,
        "run": None,
        "checkpoint": None,
    }


def _find_unique_repository(start: Path) -> Path:
    current = start if start.is_dir() else start.parent
    matches = [
        candidate
        for candidate in (current, *current.parents)
        if has_manifest(candidate)
    ]
    if not matches:
        raise FileNotFoundError(f"DSET project root not found from: {start}")
    if len(matches) > 1:
        raise ValueError(
            "competing DSET project roots: " + ", ".join(str(item) for item in matches)
        )
    return matches[0]


def _target_scope(root: Path, target: Path) -> tuple[dict[str, Any], str | None]:
    manifest = load(discover_layout(root).manifest_path)
    project = manifest.get("project") if isinstance(manifest, dict) else None
    project_id = project.get("id") if isinstance(project, dict) else None
    candidates: list[str] = []
    raw_areas = manifest.get("work_areas", []) if isinstance(manifest, dict) else []
    for raw in raw_areas if isinstance(raw_areas, list) else []:
        if not isinstance(raw, dict):
            continue
        identifier = raw.get("id")
        relative = raw.get("path")
        if not isinstance(identifier, str) or not isinstance(relative, str):
            continue
        area_root = (root / relative).resolve()
        try:
            target.relative_to(area_root)
        except ValueError:
            continue
        candidates.append(identifier)
    if len(candidates) > 1:
        raise ValueError(
            "target belongs to competing Work Areas: " + ", ".join(sorted(candidates))
        )
    work_area = candidates[0] if candidates else None
    return (
        {
            "project": project_id,
            "target": {
                "repository": work_area is None,
                "work_areas": [] if work_area is None else [work_area],
            },
        },
        work_area,
    )


def _run_ruleset_identity(raw: object) -> object:
    if not isinstance(raw, dict):
        raise ValueError("runtime returned an invalid run record")
    return raw.get("ruleset_identity")
