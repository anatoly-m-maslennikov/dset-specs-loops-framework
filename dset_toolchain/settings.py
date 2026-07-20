from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .toml_codec import TomlCodecError
from .toml_codec import load as load_toml

SETTINGS_SCHEMA_VERSION = "1.1"
LEGACY_SETTINGS_SCHEMA_VERSION = "1.0"
SUPPORTED_SETTINGS_SCHEMA_VERSIONS = frozenset(
    {LEGACY_SETTINGS_SCHEMA_VERSION, SETTINGS_SCHEMA_VERSION}
)
ARTIFACT_CREATION_STRICTNESS = frozenset({"medium", "high"})
IMPLEMENTATION_MODES = frozenset({"lazy", "strict"})
DEFAULT_PRIORITY_SCALE = ("critical", "high", "medium", "low", "deferred")


@dataclass(frozen=True)
class ProjectSettings:
    """Validated project settings, normalized across the 1.0 → 1.1 rename."""

    schema_version: str = SETTINGS_SCHEMA_VERSION
    artifact_subtype_in_names: bool = False
    artifact_creation_strictness: str = "medium"
    implementation_mode: str = "lazy"
    priority_scale: tuple[str, ...] = DEFAULT_PRIORITY_SCALE
    default_priority: str = "medium"


def load_project_settings(root: Path) -> tuple[ProjectSettings, tuple[str, ...]]:
    """Read root settings while keeping the 1.0 names read-only compatible.

    New writers must use the documented 1.1 names.  This reader accepts the
    retired 1.0 ``optional_capabilities`` names only so an adopter can plan a
    deliberate migration; it never emits them.
    """

    path = root / "dset.toml"
    if not path.is_file():
        return ProjectSettings(), ()
    try:
        raw = load_toml(path)
    except (OSError, UnicodeError, TomlCodecError) as error:
        return ProjectSettings(), (f"cannot read settings: {error}",)

    issues: list[str] = []
    schema_version = _string(raw.get("schema_version"), "schema_version", issues)
    if schema_version not in SUPPORTED_SETTINGS_SCHEMA_VERSIONS:
        issues.append("settings schema_version must be 1.0 or 1.1")

    legacy = schema_version == LEGACY_SETTINGS_SCHEMA_VERSION
    artifacts_name = "optional_capabilities" if legacy else "artifacts"
    artifacts = _table(raw.get(artifacts_name), artifacts_name, issues)
    subtype_key = "artifact_subtype_in_names" if legacy else "subtype_in_names"
    strictness_key = (
        "artifact_creation_strictness" if legacy else "creation_strictness"
    )

    include_subtype = _boolean(
        artifacts.get(subtype_key, False),
        f"{artifacts_name}.{subtype_key}",
        issues,
    )
    strictness = _string(
        artifacts.get(strictness_key, "medium"),
        f"{artifacts_name}.{strictness_key}",
        issues,
    )
    if strictness not in ARTIFACT_CREATION_STRICTNESS:
        issues.append("artifact_creation_strictness must be medium or high")
        strictness = "medium"

    implementation_mode = "lazy"
    if not legacy:
        workflows = _table(raw.get("workflows"), "workflows", issues)
        implement = _table(workflows.get("implement"), "workflows.implement", issues)
        implementation_mode = _string(
            implement.get("mode", "lazy"), "workflows.implement.mode", issues
        )
        if implementation_mode not in IMPLEMENTATION_MODES:
            issues.append("workflows.implement.mode must be lazy or strict")
            implementation_mode = "lazy"

    priority = _table(raw.get("priority"), "priority", issues)
    priority_scale = _priority_scale(
        priority.get("scale", DEFAULT_PRIORITY_SCALE), legacy, issues
    )
    default_priority = _string(
        priority.get("default", "medium"), "priority.default", issues
    )
    if default_priority not in priority_scale:
        issues.append("priority.default must be present in priority.scale")

    return (
        ProjectSettings(
            schema_version=(
                schema_version
                if schema_version in SUPPORTED_SETTINGS_SCHEMA_VERSIONS
                else SETTINGS_SCHEMA_VERSION
            ),
            artifact_subtype_in_names=include_subtype,
            artifact_creation_strictness=strictness,
            implementation_mode=implementation_mode,
            priority_scale=priority_scale,
            default_priority=default_priority,
        ),
        tuple(issues),
    )


def _table(value: object, name: str, issues: list[str]) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    issues.append(f"{name} must be a TOML table")
    return {}


def _string(value: object, name: str, issues: list[str]) -> str:
    if isinstance(value, str):
        return value
    issues.append(f"{name} must be a string")
    return ""


def _boolean(value: object, name: str, issues: list[str]) -> bool:
    if isinstance(value, bool):
        return value
    issues.append(f"{name} must be true or false")
    return False


def _priority_scale(
    value: object, legacy: bool, issues: list[str]
) -> tuple[str, ...]:
    if legacy and isinstance(value, str):
        selected = tuple(item.strip() for item in value.split(",") if item.strip())
    elif isinstance(value, (list, tuple)) and all(
        isinstance(item, str) for item in value
    ):
        selected = tuple(value)
    else:
        issues.append("priority.scale must be a TOML array of strings")
        return DEFAULT_PRIORITY_SCALE
    if len(selected) < 2 or len(set(selected)) != len(selected):
        issues.append("priority.scale must contain at least two unique values")
        return DEFAULT_PRIORITY_SCALE
    return selected
