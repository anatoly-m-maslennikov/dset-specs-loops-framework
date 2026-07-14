from __future__ import annotations

import re
from pathlib import Path

from .profiles import VALID_PROFILES, required_artifacts
from .yaml_subset import load

TRACE_LAYERS = ("META", "GOV", "TOOL", "SKILL", "OPS")


def create_change(
    root: Path,
    change_id: str,
    package_id: str,
    profile: str,
    title: str | None = None,
    layer: str | None = None,
) -> Path:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", change_id):
        raise ValueError("change ID must be lowercase kebab-case")
    if profile not in VALID_PROFILES:
        raise ValueError(f"unknown profile: {profile}")
    destination = root / "dset" / "changes" / change_id
    if destination.exists():
        raise FileExistsError(f"change already exists: {destination}")
    files, directories = required_artifacts(root, profile)
    templates = root / "dset" / "templates" / "change"
    display_title = title or change_id.replace("-", " ").title()
    project_key = _project_key(root)
    id_layer = _id_layer(root, layer)
    replacements = {
        "{{change_id}}": change_id,
        "{{package_id}}": package_id,
        "{{profile}}": profile,
        "{{title}}": display_title,
        "{{project_key}}": project_key,
        "{{id_layer}}": id_layer,
        "{{repository}}": _repository(root),
    }
    destination.mkdir(parents=True)
    try:
        for directory in sorted(directories):
            (destination / directory).mkdir(parents=True, exist_ok=True)
        for relative in sorted(files):
            source = templates / relative
            target = destination / relative
            _copy_template(source, target, replacements)
        if "specs" in directories:
            source = templates / "specs" / "package.md"
            target = destination / "specs" / f"{package_id}.md"
            _copy_template(source, target, replacements)
        if "proofs" in directories:
            source = templates / "proofs" / "README.md"
            target = destination / "proofs" / "README.md"
            _copy_template(source, target, replacements)
        if "proofs/candidate-fit" in directories:
            source = templates / "proofs" / "candidate-fit" / "README.md"
            target = destination / "proofs" / "candidate-fit" / "README.md"
            _copy_template(source, target, replacements)
    except Exception:
        _remove_tree(destination)
        raise
    return destination


def _copy_template(source: Path, target: Path, replacements: dict[str, str]) -> None:
    if not source.is_file():
        raise FileNotFoundError(f"template is missing: {source}")
    text = source.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def _project_key(root: Path) -> str:
    data = load(root / "dset" / "dset.yaml")
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
    data = load(root / "dset" / "intake.yaml")
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
    history = load(root / "dset" / "history" / "pull-requests.yaml")
    return str(history["repository"])


def _remove_tree(path: Path) -> None:
    import shutil

    if path.exists():
        shutil.rmtree(path)
