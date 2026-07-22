from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from .layout import LAYERS, RepositoryLayout, discover_layout
from .toml_codec import dumps as dump_toml
from .yaml_subset import dump as dump_structured
from .yaml_subset import load


def project_section(root: Path, name: str) -> dict[str, Any]:
    """Read a project registry from settings or its pre-1.4 carrier."""

    layout = discover_layout(root)
    current = layout.recursive or layout.separated
    path = layout.settings_path if current else _legacy_path(layout, name)
    data = load(path)
    if not isinstance(data, dict):
        raise ValueError(f"project carrier must be a mapping: {path}")
    if current:
        value = data.get(name)
        if not isinstance(value, dict):
            raise ValueError(f"settings section is missing or invalid: {name}")
        return value
    return data


def write_project_section(root: Path, name: str, value: dict[str, Any]) -> Path:
    """Replace one registry without discarding documented settings comments."""

    layout = discover_layout(root)
    if not (layout.recursive or layout.separated):
        path = _legacy_path(layout, name)
        path.write_text(dump_structured(value, path), encoding="utf-8")
        return path

    path = layout.settings_path
    text = path.read_text(encoding="utf-8")
    rendered = dump_toml({name: value}).strip()
    start, end = _section_bounds(text, name)
    separator = "\n\n" if start > 0 else ""
    replacement = f"{separator}{rendered}\n"
    updated = f"{text[:start].rstrip()}{replacement}{text[end:].lstrip()}"
    path.write_text(updated, encoding="utf-8")
    return path


def lifecycle_event_files(root: Path) -> Iterator[Path]:
    """Yield atomized lifecycle carriers, or the historical aggregate carrier."""

    layout = discover_layout(root)
    if not (layout.recursive or layout.separated):
        path = layout.structured_file(layout.project_state_root, "lifecycle.toml")
        if path.is_file():
            yield path
        return
    roots = (layout.project_root, *(layout.layer_root(layer) for layer in LAYERS))
    for owner in roots:
        lifecycle = owner / "lifecycle"
        if lifecycle.is_dir():
            yield from sorted(lifecycle.glob("*.toml"))


def lifecycle_events(root: Path) -> list[dict[str, Any]]:
    """Load lifecycle events independent of aggregate or atomized storage."""

    layout = discover_layout(root)
    events: list[dict[str, Any]] = []
    for path in lifecycle_event_files(root):
        data = load(path)
        if not isinstance(data, dict):
            raise ValueError(f"lifecycle carrier must be a mapping: {path}")
        if layout.recursive or layout.separated:
            if isinstance(data.get("event"), dict):
                event = dict(data["event"])
            else:
                event = {
                    key: value
                    for key, value in data.items()
                    if key not in {"schema_version", "artifact_type", "artifact_id"}
                }
                event["id"] = str(data.get("artifact_id", event.get("id", "")))
            events.append(event)
            continue
        raw = data.get("events", [])
        if not isinstance(raw, list):
            raise ValueError(f"lifecycle events must be a list: {path}")
        events.extend(dict(item) for item in raw if isinstance(item, dict))
    return sorted(events, key=lambda item: str(item.get("id", "")))


def _legacy_path(layout: RepositoryLayout, name: str) -> Path:
    paths = {
        "artifact_catalog": layout.artifact_type_registry_path,
        "artifact_structure": layout.artifact_registry_path,
        "governance_registry": layout.governance_path,
        "source_provenance": layout.provenance_path,
        "version_registry": layout.version_path,
    }
    try:
        return paths[name]
    except KeyError as error:
        raise ValueError(f"unknown project registry: {name}") from error


def _section_bounds(text: str, name: str) -> tuple[int, int]:
    header = re.compile(r"(?m)^\[([^\[\]\n]+)\]\s*$")
    matches = list(header.finditer(text))
    start_match = next((match for match in matches if match.group(1) == name), None)
    if start_match is None:
        return len(text), len(text)
    end = len(text)
    prefix = f"{name}."
    for match in matches:
        if match.start() <= start_match.start():
            continue
        section = match.group(1)
        if section != name and not section.startswith(prefix):
            end = match.start()
            break
    return start_match.start(), end
