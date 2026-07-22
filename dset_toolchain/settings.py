from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .toml_codec import TomlCodecError
from .toml_codec import load as load_toml

SETTINGS_FILENAME = "dset_settings.toml"
SETTINGS_DIRECTORY = ".dset"
LEGACY_SETTINGS_FILENAME = "dset.toml"
SETTINGS_SCHEMA_VERSION = "1.3"
PREVIOUS_SETTINGS_SCHEMA_VERSION = "1.2"
LEGACY_SETTINGS_SCHEMA_VERSION = "1.0"
SUPPORTED_SETTINGS_SCHEMA_VERSIONS = frozenset(
    {
        LEGACY_SETTINGS_SCHEMA_VERSION,
        "1.1",
        PREVIOUS_SETTINGS_SCHEMA_VERSION,
        SETTINGS_SCHEMA_VERSION,
    }
)
ARTIFACT_CREATION_STRICTNESS = frozenset({"medium", "high"})
IMPLEMENTATION_MODES = frozenset({"lazy", "strict"})
CHANGE_WORKSPACE_MODES = frozenset({"integration-branch", "branch-worktree"})
DELEGATION_BUDGET_PROFILES = frozenset({"low", "medium", "high"})
DEFAULT_PRIORITY_SCALE = ("critical", "high", "medium", "low", "deferred")


@dataclass(frozen=True)
class ProjectSettings:
    """Validated settings normalized across all supported read contracts."""

    schema_version: str = SETTINGS_SCHEMA_VERSION
    artifact_subtype_in_names: bool = False
    artifact_creation_strictness: str = "medium"
    implementation_mode: str = "lazy"
    change_workspace_mode: str = "integration-branch"
    delegation_budget_profile: str = "medium"
    priority_scale: tuple[str, ...] = DEFAULT_PRIORITY_SCALE
    default_priority: str = "medium"


def selected_settings_path(root: Path) -> Path:
    """Return the selected settings carrier or the canonical missing path."""

    canonical = root / SETTINGS_DIRECTORY / SETTINGS_FILENAME
    interim = root / "dset" / SETTINGS_FILENAME
    previous = root / SETTINGS_FILENAME
    legacy = root / LEGACY_SETTINGS_FILENAME
    if canonical.is_file():
        return canonical
    if interim.is_file():
        return interim
    if previous.is_file():
        return previous
    if legacy.is_file():
        return legacy
    return canonical


def load_project_settings(root: Path) -> tuple[ProjectSettings, tuple[str, ...]]:
    """Read canonical settings with explicit legacy-name compatibility.

    New writers use ``.dset/dset_settings.toml`` and schema 1.3. This reader
    accepts the uncommitted schema-1.3 preview path plus retired root filenames
    and 1.0-1.2 field contracts only so an adopter can plan a deliberate
    migration; it never emits them. Competing names fail closed instead of
    selecting by precedence.
    """

    canonical = root / SETTINGS_DIRECTORY / SETTINGS_FILENAME
    interim_path = root / "dset" / SETTINGS_FILENAME
    previous_path = root / SETTINGS_FILENAME
    legacy_path = root / LEGACY_SETTINGS_FILENAME
    existing = [
        path
        for path in (canonical, interim_path, previous_path, legacy_path)
        if path.is_file()
    ]
    if len(existing) > 1:
        return (
            ProjectSettings(),
            (
                "DSET settings carriers cannot coexist: "
                + ", ".join(path.relative_to(root).as_posix() for path in existing),
            ),
        )
    path = selected_settings_path(root)
    if not path.is_file():
        return ProjectSettings(), ()
    try:
        raw = load_toml(path)
    except (OSError, UnicodeError, TomlCodecError) as error:
        return ProjectSettings(), (f"cannot read settings: {error}",)

    issues: list[str] = []
    schema_version = _string(raw.get("schema_version"), "schema_version", issues)
    if schema_version not in SUPPORTED_SETTINGS_SCHEMA_VERSIONS:
        issues.append("settings schema_version must be 1.0, 1.1, 1.2, or 1.3")

    legacy = schema_version == LEGACY_SETTINGS_SCHEMA_VERSION
    _validate_known_keys(raw, schema_version, issues)
    artifacts_name = "optional_capabilities" if legacy else "artifacts"
    artifacts = _table(raw.get(artifacts_name), artifacts_name, issues)
    subtype_key = "artifact_subtype_in_names" if legacy else "subtype_in_names"
    strictness_key = "artifact_creation_strictness" if legacy else "creation_strictness"

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
        issues.append(f"{artifacts_name}.{strictness_key} must be medium or high")
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

    change_workspace_mode = "integration-branch"
    delegation_budget_profile = "medium"
    if schema_version in {PREVIOUS_SETTINGS_SCHEMA_VERSION, SETTINGS_SCHEMA_VERSION}:
        changes = _table(raw.get("changes"), "changes", issues)
        change_workspace_mode = _string(
            changes.get("default_workspace", "integration-branch"),
            "changes.default_workspace",
            issues,
        )
        if change_workspace_mode not in CHANGE_WORKSPACE_MODES:
            issues.append(
                "changes.default_workspace must be integration-branch or "
                "branch-worktree"
            )
            change_workspace_mode = "integration-branch"

        delegation = _table(raw.get("delegation"), "delegation", issues)
        delegation_budget_profile = _string(
            delegation.get("budget_profile", "medium"),
            "delegation.budget_profile",
            issues,
        )
        if delegation_budget_profile not in DELEGATION_BUDGET_PROFILES:
            issues.append("delegation.budget_profile must be low, medium, or high")
            delegation_budget_profile = "medium"

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
            change_workspace_mode=change_workspace_mode,
            delegation_budget_profile=delegation_budget_profile,
            priority_scale=priority_scale,
            default_priority=default_priority,
        ),
        tuple(issues),
    )


def _validate_known_keys(
    raw: dict[str, Any], schema_version: str, issues: list[str]
) -> None:
    legacy = schema_version == LEGACY_SETTINGS_SCHEMA_VERSION
    current = schema_version in {
        PREVIOUS_SETTINGS_SCHEMA_VERSION,
        SETTINGS_SCHEMA_VERSION,
    }
    allowed_top = {
        "schema_version",
        "optional_capabilities" if legacy else "artifacts",
        "priority",
    }
    if not legacy:
        allowed_top.add("workflows")
    if current:
        allowed_top.update({"changes", "delegation"})
    if schema_version == SETTINGS_SCHEMA_VERSION:
        allowed_top.update(
            {
                "canonical_command",
                "project",
                "supportability",
                "release",
                "work_items",
                "structure",
                "profiles",
                "change_contract",
                "commit_provenance",
                "verification",
                "work_areas",
                "packages",
            }
        )
    _unknown_keys(raw, allowed_top, "settings", issues)

    artifacts_name = "optional_capabilities" if legacy else "artifacts"
    artifacts = raw.get(artifacts_name)
    if isinstance(artifacts, dict):
        _unknown_keys(
            artifacts,
            {
                "artifact_subtype_in_names" if legacy else "subtype_in_names",
                ("artifact_creation_strictness" if legacy else "creation_strictness"),
            },
            artifacts_name,
            issues,
        )
    priority = raw.get("priority")
    if isinstance(priority, dict):
        _unknown_keys(priority, {"scale", "default"}, "priority", issues)
    workflows = raw.get("workflows")
    if isinstance(workflows, dict):
        _unknown_keys(workflows, {"implement"}, "workflows", issues)
        implement = workflows.get("implement")
        if isinstance(implement, dict):
            _unknown_keys(implement, {"mode"}, "workflows.implement", issues)
    changes = raw.get("changes")
    if isinstance(changes, dict):
        _unknown_keys(changes, {"default_workspace"}, "changes", issues)
    delegation = raw.get("delegation")
    if isinstance(delegation, dict):
        _unknown_keys(delegation, {"budget_profile"}, "delegation", issues)


def _unknown_keys(
    table: dict[str, Any], allowed: set[str], name: str, issues: list[str]
) -> None:
    for key in sorted(set(table) - allowed):
        issues.append(f"{name} has unknown setting: {key}")


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


def _priority_scale(value: object, legacy: bool, issues: list[str]) -> tuple[str, ...]:
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
