"""Provide DSET project data behavior."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .layout import RepositoryLayout, discover_layout
from .structured_data import dump as dump_structured
from .structured_data import load
from .toml_codec import dumps as dump_toml


def project_section(root: Path, name: str) -> dict[str, Any]:
    """Read a project registry from settings or its pre-1.4 carrier."""

    layout = discover_layout(root)
    current = layout.recursive or layout.separated
    separate_catalog = (
        name == "artifact_catalog"
        and layout.artifact_type_registry_path != layout.settings_path
    )
    path = (
        layout.artifact_type_registry_path
        if separate_catalog
        else layout.settings_path
        if current
        else _legacy_path(layout, name)
    )
    data = load(path)
    if not isinstance(data, dict):
        raise ValueError(f"project carrier must be a mapping: {path}")
    if current and not separate_catalog:
        value = data.get(name)
        if not isinstance(value, dict):
            raise ValueError(f"settings section is missing or invalid: {name}")
        return value
    return data


def write_project_section(root: Path, name: str, value: dict[str, Any]) -> Path:
    """Replace one registry without discarding documented settings comments."""

    layout = discover_layout(root)
    if (
        name == "artifact_catalog"
        and layout.artifact_type_registry_path != layout.settings_path
    ):
        path = layout.artifact_type_registry_path
        path.write_text(dump_toml(value), encoding="utf-8")
        return path
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


def _legacy_path(layout: RepositoryLayout, name: str) -> Path:
    """Handle path using the declared repository contract."""
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
    """Handle bounds using the declared repository contract."""
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
