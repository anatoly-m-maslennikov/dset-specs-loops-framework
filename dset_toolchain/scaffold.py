from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path

from .layout import discover_layout
from .profiles import VALID_PROFILES, required_artifacts
from .settings import load_project_settings
from .yaml_subset import dump, load

TRACE_LAYERS = ("META", "GOV", "TOOL", "SKILL", "OPS")


def create_change(
    root: Path,
    change_id: str,
    package_id: str,
    profile: str,
    title: str | None = None,
    layer: str | None = None,
    stable_id: str | None = None,
    work_areas: Sequence[str] | None = None,
    workspace_mode: str | None = None,
) -> Path:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", change_id):
        raise ValueError("change ID must be lowercase kebab-case")
    if profile not in VALID_PROFILES:
        raise ValueError(f"unknown profile: {profile}")
    layout = discover_layout(root)
    if layout.layered and layer is None:
        raise ValueError("schema 1.2 changes require an owning DSET layer")
    change_target = _change_target(root, work_areas)
    canonical_id = change_id
    if layout.layered:
        canonical_id = stable_id or _next_change_id(root, str(layer))
        expected = (
            rf"{re.escape(_project_key(root))}-CHANGE-{str(layer).upper()}-[0-9]{{3,}}"
        )
        if re.fullmatch(expected, canonical_id) is None:
            raise ValueError("stable Change ID must match its project and owning layer")
    destination = layout.active_change_root(layer) / change_id
    if destination.exists():
        raise FileExistsError(f"change already exists: {destination}")
    files, directories = required_artifacts(root, profile)
    display_title = title or change_id.replace("-", " ").title()
    project_key = _project_key(root)
    id_layer = _id_layer(root, layer)
    replacements = {
        "{{change_id}}": canonical_id,
        "{{change_slug}}": change_id,
        "{{package_id}}": package_id,
        "{{profile}}": profile,
        "{{title}}": display_title,
        "{{project_key}}": project_key,
        "{{id_layer}}": id_layer,
        "{{layer}}": str(layer).lower() if layer is not None else "",
        "{{repository}}": _repository(root),
    }
    destination.mkdir(parents=True)
    try:
        for directory in sorted(directories):
            (destination / directory).mkdir(parents=True, exist_ok=True)
        for relative in sorted(files):
            template_relative = Path("change") / relative
            relative_path = Path(relative)
            if relative_path.stem == "change" and relative_path.suffix in {
                ".toml",
                ".yaml",
                ".yml",
            }:
                template_family = "layered" if layout.layered else "legacy"
                template_relative = Path("change") / template_family / relative_path
            source = layout.find_template(template_relative)
            target = destination / relative
            _copy_template(source, target, replacements)
        if "specs" in directories:
            source = layout.find_template("change/specs/package.md")
            target = destination / "specs" / f"{package_id}.md"
            _copy_template(source, target, replacements)
        if "proofs" in directories:
            source = layout.find_template("change/proofs/README.md")
            target = destination / "proofs" / "README.md"
            _copy_template(source, target, replacements)
        if "proofs/candidate-fit" in directories:
            source = layout.find_template("change/proofs/candidate-fit/README.md")
            target = destination / "proofs" / "candidate-fit" / "README.md"
            _copy_template(source, target, replacements)
        if layout.layered:
            _materialize_layered_manifest(
                root,
                destination,
                canonical_id,
                change_id,
                str(layer),
                change_target,
                workspace_mode,
            )
    except Exception:
        _remove_tree(destination)
        raise
    return destination


def _copy_template(source: Path, target: Path, replacements: dict[str, str]) -> None:
    if not source.is_file():
        raise FileNotFoundError(f"template is missing: {source}")
    if target.suffix == ".toml" and source.suffix in {".toml", ".yaml", ".yml"}:
        data = _replace_values(load(source), replacements)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(dump(data, target), encoding="utf-8")
        return
    text = source.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def _replace_values(value: object, replacements: dict[str, str]) -> object:
    if isinstance(value, dict):
        return {key: _replace_values(item, replacements) for key, item in value.items()}
    if isinstance(value, list):
        return [_replace_values(item, replacements) for item in value]
    if isinstance(value, str):
        for old, new in replacements.items():
            value = value.replace(old, new)
    return value


def _project_key(root: Path) -> str:
    data = load(discover_layout(root).manifest_path)
    project = data.get("project", {}) if isinstance(data, dict) else {}
    key = project.get("key") if isinstance(project, dict) else None
    if not isinstance(key, str) or not re.fullmatch(r"[A-Z][A-Z0-9]*", key):
        raise ValueError("project.key must be an uppercase ID segment")
    return key


def _id_layer(root: Path, layer: str | None) -> str:
    if layer is None:
        return ""
    normalized = layer.upper()
    if normalized not in TRACE_LAYERS:
        raise ValueError(f"unknown ID layer: {layer}")
    layout = discover_layout(root)
    if layout.layered:
        return f"-{normalized}"
    data = load(layout.intake_path)
    raw_scopes = data.get("scopes", []) if isinstance(data, dict) else []
    registered = {
        item.get("id_segment")
        for item in raw_scopes
        if isinstance(item, dict) and item.get("kind") == "layer"
    }
    if normalized not in registered:
        raise ValueError(f"unregistered ID layer: {normalized}")
    return f"-{normalized}"


def _repository(root: Path) -> str:
    history = load(discover_layout(root).history_path)
    return str(history["repository"])


def _change_target(
    root: Path, work_areas: Sequence[str] | None
) -> dict[str, object] | None:
    layout = discover_layout(root)
    requested = list(work_areas or ())
    if not layout.layered:
        if requested:
            raise ValueError("work-area targets require schema 1.2")
        return None
    if any(
        not isinstance(identifier, str)
        or re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier) is None
        for identifier in requested
    ):
        raise ValueError("work-area targets must be kebab-case IDs")
    if len(requested) != len(set(requested)):
        raise ValueError("work-area targets must be unique")
    manifest = load(layout.manifest_path)
    if not isinstance(manifest, dict):
        raise ValueError("project manifest must be a mapping")
    raw_declared = manifest.get("work_areas", [])
    declared = {
        item.get("id")
        for item in (raw_declared if isinstance(raw_declared, list) else [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    unknown = sorted(set(requested) - declared)
    if unknown:
        raise ValueError(f"undeclared work-area target: {', '.join(unknown)}")
    selected = sorted(requested)
    return {"repository": not selected, "work_areas": selected}


def _next_change_id(root: Path, layer: str) -> str:
    layout = discover_layout(root)
    normalized = layer.upper()
    if normalized not in TRACE_LAYERS:
        raise ValueError(f"unknown ID layer: {layer}")
    prefix = f"{_project_key(root)}-CHANGE-{normalized}-"
    highest = 0
    for change_root in (*layout.active_change_roots, *layout.archive_change_roots):
        if not change_root.is_dir():
            continue
        for directory in change_root.iterdir():
            manifest = layout.structured_file(directory, "change.toml")
            if not directory.is_dir() or not manifest.is_file():
                continue
            data = load(manifest)
            identifier = data.get("id") if isinstance(data, dict) else None
            if isinstance(identifier, str) and identifier.startswith(prefix):
                suffix = identifier.removeprefix(prefix)
                if suffix.isdigit():
                    highest = max(highest, int(suffix))
    return f"{prefix}{highest + 1:03d}"


def _materialize_layered_manifest(
    root: Path,
    destination: Path,
    stable_id: str,
    slug: str,
    layer: str,
    target: dict[str, object] | None,
    workspace_mode: str | None,
) -> None:
    path = discover_layout(root).structured_file(destination, "change.toml")
    data = load(path)
    if not isinstance(data, dict):
        raise ValueError("change template root must be a mapping")
    normalized = layer.lower()
    workspace = _workspace_for_change(root, slug, workspace_mode)
    data.update(
        {
            "schema_version": "1.2",
            "id": stable_id,
            "slug": slug,
            "primary_layer": normalized,
            "affected_layers": [normalized],
            "target": target,
            "workspace": workspace,
            "dependencies": [],
        }
    )
    release = data.get("release")
    if isinstance(release, dict):
        if "policy" in release:
            release["policy"] = "dset/scopes/ops/governance/release.md"
        if "owner_change" in release:
            release["owner_change"] = stable_id
    path.write_text(dump(data, path), encoding="utf-8")


def _workspace_for_change(
    root: Path, slug: str, requested_mode: str | None
) -> dict[str, str]:
    manifest = load(discover_layout(root).manifest_path)
    if not isinstance(manifest, dict):
        raise ValueError("project manifest must be a mapping")
    settings, settings_issues = load_project_settings(root)
    if settings_issues:
        raise ValueError("; ".join(settings_issues))
    mode = requested_mode or settings.change_workspace_mode
    if mode not in {"integration-branch", "branch-worktree"}:
        raise ValueError("workspace mode must be integration-branch or branch-worktree")
    release = manifest.get("release", {})
    integration = (
        release.get("integration_branch") if isinstance(release, dict) else None
    )
    protected = release.get("protected_branch") if isinstance(release, dict) else None
    if not isinstance(integration, str) or not integration:
        integration = "pending"
    if not isinstance(protected, str) or not protected:
        protected = "pending"
    branch = integration if mode == "integration-branch" else f"dset/{slug}"
    base_ref = protected if mode == "integration-branch" else integration
    return {
        "isolation": mode,
        "branch": branch,
        "base_ref": base_ref,
        "base_commit": "pending",
        "head_commit": "pending",
    }


def _remove_tree(path: Path) -> None:
    import shutil

    if path.exists():
        shutil.rmtree(path)
