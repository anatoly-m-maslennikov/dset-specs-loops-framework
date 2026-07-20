from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SETTINGS_SCHEMA_VERSION = "1.0"
ARTIFACT_CREATION_STRICTNESS = frozenset({"medium", "high"})


@dataclass(frozen=True)
class ProjectSettings:
    schema_version: str = SETTINGS_SCHEMA_VERSION
    artifact_subtype_in_names: bool = False
    artifact_creation_strictness: str = "medium"


def load_project_settings(root: Path) -> tuple[ProjectSettings, tuple[str, ...]]:
    path = root / "dset.toml"
    if not path.is_file():
        return ProjectSettings(), ()
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        return ProjectSettings(), (f"cannot read settings: {error}",)

    schema_version: str | None = None
    include_subtype: bool | None = None
    strictness = "medium"
    issues: list[str] = []
    section = ""
    for raw in lines:
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            continue
        key, separator, value = line.partition("=")
        if not separator:
            continue
        key = key.strip()
        value = value.strip()
        if not section and key == "schema_version":
            schema_version = value.strip('"')
        if section != "optional_capabilities":
            continue
        if key == "artifact_subtype_in_names":
            if value not in {"true", "false"}:
                issues.append("artifact_subtype_in_names must be true or false")
            else:
                include_subtype = value == "true"
        if key == "artifact_creation_strictness":
            selected = value.strip('"')
            if selected not in ARTIFACT_CREATION_STRICTNESS:
                issues.append(
                    "artifact_creation_strictness must be medium or high"
                )
            else:
                strictness = selected

    if schema_version != SETTINGS_SCHEMA_VERSION:
        issues.append(f"settings schema_version must be {SETTINGS_SCHEMA_VERSION}")
    if include_subtype is None:
        issues.append(
            "optional_capabilities.artifact_subtype_in_names is required"
        )
    return (
        ProjectSettings(
            schema_version=schema_version or SETTINGS_SCHEMA_VERSION,
            artifact_subtype_in_names=bool(include_subtype),
            artifact_creation_strictness=strictness,
        ),
        tuple(issues),
    )
