from __future__ import annotations

from pathlib import Path
from typing import Any

from .layout import discover_layout
from .yaml_subset import load

VALID_PROFILES = {"small", "standard", "large", "defect", "adoption"}


def required_artifacts(root: Path, profile: str) -> tuple[set[str], set[str]]:
    data = load(discover_layout(root).find_template("profiles.yaml"))
    profiles: dict[str, dict[str, Any]] = data["profiles"]
    documents: set[str] = set()
    directories: set[str] = set()
    files: set[str] = set()
    seen: set[str] = set()

    def collect(name: str) -> None:
        if name in seen:
            raise ValueError(f"cyclic profile inheritance: {name}")
        seen.add(name)
        current = profiles[name]
        parent = current.get("extends")
        if parent:
            collect(parent)
        documents.update(current.get("documents", []))
        directories.update(current.get("directories", []))
        files.update(current.get("files", []))

    collect(profile)
    return documents | files | {"change.yaml"}, directories
