"""Provide DSET settings behavior."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .artifact_routing import (
    CONTENT_ROLES,
    GOVERNANCE_ORIGINS,
    RELATION_SHAPES,
    REVISION_MODES,
)
from .toml_codec import TomlCodecError
from .toml_codec import load as load_toml

# SETTINGS_FILENAME defines settings filename; this module owns the default.
SETTINGS_FILENAME = "dset_settings.toml"
# SETTINGS_DIRECTORY defines settings directory; this module owns the default.
SETTINGS_DIRECTORY = ".dset"
# LEGACY_SETTINGS_FILENAME defines the retired settings filename.
LEGACY_SETTINGS_FILENAME = "dset.toml"
# SETTINGS_SCHEMA_VERSION defines settings schema version; this module owns the default.
SETTINGS_SCHEMA_VERSION = "1.5"
# PREVIOUS_SETTINGS_SCHEMA_VERSION defines the previous settings schema.
PREVIOUS_SETTINGS_SCHEMA_VERSION = "1.4"
# HIDDEN_SETTINGS_SCHEMA_VERSION defines the first hidden-layout schema.
HIDDEN_SETTINGS_SCHEMA_VERSION = "1.3"
# LEGACY_SETTINGS_SCHEMA_VERSION defines the oldest readable schema.
LEGACY_SETTINGS_SCHEMA_VERSION = "1.0"
# SUPPORTED_SETTINGS_SCHEMA_VERSIONS defines every readable schema.
SUPPORTED_SETTINGS_SCHEMA_VERSIONS = frozenset(
    {
        LEGACY_SETTINGS_SCHEMA_VERSION,
        "1.1",
        "1.2",
        HIDDEN_SETTINGS_SCHEMA_VERSION,
        PREVIOUS_SETTINGS_SCHEMA_VERSION,
        SETTINGS_SCHEMA_VERSION,
    }
)
# ARTIFACT_CREATION_STRICTNESS defines artifact creation gates.
ARTIFACT_CREATION_STRICTNESS = frozenset({"medium", "high"})
# IMPLEMENTATION_MODES defines implementation modes; this module owns the default.
IMPLEMENTATION_MODES = frozenset({"lazy", "strict"})
# CHANGE_WORKSPACE_MODES defines change workspace modes; this module owns the default.
CHANGE_WORKSPACE_MODES = frozenset({"integration-branch", "branch-worktree"})
# DELEGATION_BUDGET_PROFILES defines delegation budgets.
DELEGATION_BUDGET_PROFILES = frozenset({"low", "medium", "high"})
# SEMANTIC_COMPILATION_MODES defines compilation timing.
SEMANTIC_COMPILATION_MODES = frozenset({"on_demand", "eager"})
# CONFLICT_RESOLUTION_MODES defines conflict selection modes.
CONFLICT_RESOLUTION_MODES = frozenset({"ask_always", "auto_by_effective_priority"})
# GOVERNANCE_SURFACE_KEYS defines optional governed project surfaces.
GOVERNANCE_SURFACE_KEYS = (
    "evergreen_specification",
    "test_plan",
    "evaluation_plan",
    "implementation_plan",
    "project_overview",
    "architecture_view",
)
# DEFAULT_PRIORITY_SCALE defines default priority scale; this module owns the default.
DEFAULT_PRIORITY_SCALE = ("high", "medium", "low")


@dataclass(frozen=True)
class ProjectSettings:
    """Validated settings normalized across all supported read contracts."""

    schema_version: str = SETTINGS_SCHEMA_VERSION
    artifact_subtype_in_names: bool = False
    artifact_creation_strictness: str = "medium"
    implementation_mode: str = "lazy"
    change_workspace_mode: str = "integration-branch"
    delegation_budget_profile: str = "medium"
    semantic_compilation_mode: str = "on_demand"
    priority_scale: tuple[str, ...] = DEFAULT_PRIORITY_SCALE
    default_priority: str = "medium"
    conflict_resolution_mode: str = "ask_always"
    active_governance_surfaces: tuple[str, ...] = ()
    routing_revision_modes: tuple[str, ...] = REVISION_MODES
    routing_content_roles: tuple[str, ...] = CONTENT_ROLES
    routing_governance_origins: tuple[str, ...] = GOVERNANCE_ORIGINS
    routing_relation_shapes: tuple[str, ...] = RELATION_SHAPES


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

    New writers use ``.dset/dset_settings.toml`` and schema 1.5. This reader
    accepts the earlier hidden layouts plus retired root filenames and
    1.0-1.2 field contracts only so an adopter can plan a deliberate
    migration; it never emits them. Competing names fail closed instead of
    selecting by precedence.
    """

    canonical = root / SETTINGS_DIRECTORY / SETTINGS_FILENAME
    interim_path = root / "dset" / SETTINGS_FILENAME
    previous_path = root / SETTINGS_FILENAME
    legacy_path = root / LEGACY_SETTINGS_FILENAME
    existing = [canonical]
    if not canonical.is_file():
        existing = [
            path
            for path in (interim_path, previous_path, legacy_path)
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
        issues.append("settings schema_version must be 1.0, 1.1, 1.2, 1.3, 1.4, or 1.5")

    legacy = schema_version == LEGACY_SETTINGS_SCHEMA_VERSION
    _validate_known_keys(raw, schema_version, issues)
    artifacts_name = "optional_capabilities" if legacy else "artifacts"
    artifacts = _table(raw.get(artifacts_name), artifacts_name, issues)
    subtype_key = "artifact_subtype_in_names" if legacy else "subtype_in_names"
    strictness_key = "artifact_creation_strictness" if legacy else "creation_strictness"

    include_subtype = False
    if schema_version != SETTINGS_SCHEMA_VERSION:
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
    semantic_compilation_mode = "on_demand"
    if not legacy:
        workflows = _table(raw.get("workflows"), "workflows", issues)
        implement = _table(workflows.get("implement"), "workflows.implement", issues)
        implementation_mode = _string(
            implement.get("mode", "lazy"), "workflows.implement.mode", issues
        )
        if implementation_mode not in IMPLEMENTATION_MODES:
            issues.append("workflows.implement.mode must be lazy or strict")
            implementation_mode = "lazy"
        compilation = _table(raw.get("compilation"), "compilation", issues)
        semantic_compilation_mode = _string(
            compilation.get("mode", "on_demand"), "compilation.mode", issues
        )
        if semantic_compilation_mode not in SEMANTIC_COMPILATION_MODES:
            issues.append("compilation.mode must be on_demand or eager")
            semantic_compilation_mode = "on_demand"

    change_workspace_mode = "integration-branch"
    delegation_budget_profile = "medium"
    if schema_version in {
        "1.2",
        HIDDEN_SETTINGS_SCHEMA_VERSION,
        PREVIOUS_SETTINGS_SCHEMA_VERSION,
        SETTINGS_SCHEMA_VERSION,
    }:
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
        priority.get("scale", DEFAULT_PRIORITY_SCALE),
        legacy,
        schema_version == SETTINGS_SCHEMA_VERSION,
        issues,
    )
    default_priority = _string(
        priority.get("default", "medium"), "priority.default", issues
    )
    if default_priority not in priority_scale:
        issues.append("priority.default must be present in priority.scale")

    conflict_resolution = _table(
        raw.get("conflict_resolution"),
        "conflict_resolution",
        issues,
    )
    conflict_resolution_mode = _string(
        conflict_resolution.get("mode", "ask_always"),
        "conflict_resolution.mode",
        issues,
    )
    if conflict_resolution_mode not in CONFLICT_RESOLUTION_MODES:
        issues.append(
            "conflict_resolution.mode must be ask_always or auto_by_effective_priority"
        )
        conflict_resolution_mode = "ask_always"

    governance_surfaces = _table(
        raw.get("governance_surfaces"),
        "governance_surfaces",
        issues,
    )
    active_governance_surfaces = tuple(
        key
        for key in GOVERNANCE_SURFACE_KEYS
        if _boolean(
            governance_surfaces.get(key, False),
            f"governance_surfaces.{key}",
            issues,
        )
    )

    routing = _table(raw.get("routing"), "routing", issues)
    routing_revision_modes = _route_axis(
        routing.get("revision_modes", REVISION_MODES),
        "routing.revision_modes",
        REVISION_MODES,
        issues,
    )
    routing_content_roles = _route_axis(
        routing.get("content_roles", CONTENT_ROLES),
        "routing.content_roles",
        CONTENT_ROLES,
        issues,
    )
    routing_governance_origins = _route_axis(
        routing.get("governance_origins", GOVERNANCE_ORIGINS),
        "routing.governance_origins",
        GOVERNANCE_ORIGINS,
        issues,
    )
    routing_relation_shapes = _route_axis(
        routing.get("relation_shapes", RELATION_SHAPES),
        "routing.relation_shapes",
        RELATION_SHAPES,
        issues,
    )

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
            semantic_compilation_mode=semantic_compilation_mode,
            priority_scale=priority_scale,
            default_priority=default_priority,
            conflict_resolution_mode=conflict_resolution_mode,
            active_governance_surfaces=active_governance_surfaces,
            routing_revision_modes=routing_revision_modes,
            routing_content_roles=routing_content_roles,
            routing_governance_origins=routing_governance_origins,
            routing_relation_shapes=routing_relation_shapes,
        ),
        tuple(issues),
    )


def _validate_known_keys(
    raw: dict[str, Any], schema_version: str, issues: list[str]
) -> None:
    """Validate known keys using the declared repository contract."""
    legacy = schema_version == LEGACY_SETTINGS_SCHEMA_VERSION
    current = schema_version in {
        "1.2",
        HIDDEN_SETTINGS_SCHEMA_VERSION,
        PREVIOUS_SETTINGS_SCHEMA_VERSION,
        SETTINGS_SCHEMA_VERSION,
    }
    allowed_top = {
        "schema_version",
        "optional_capabilities" if legacy else "artifacts",
        "priority",
    }
    if not legacy:
        allowed_top.update({"workflows", "compilation"})
    if current:
        allowed_top.update({"changes", "delegation"})
    if schema_version in {PREVIOUS_SETTINGS_SCHEMA_VERSION, SETTINGS_SCHEMA_VERSION}:
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
                "artifact_catalog",
                "artifact_structure",
                "governance_registry",
                "source_provenance",
                "version_registry",
                "package_catalog",
                "conflict_resolution",
                "governance_surfaces",
                "routing",
            }
        )
    _unknown_keys(raw, allowed_top, "settings", issues)

    artifacts_name = "optional_capabilities" if legacy else "artifacts"
    artifacts = raw.get(artifacts_name)
    if isinstance(artifacts, dict):
        artifact_keys = {
            ("artifact_creation_strictness" if legacy else "creation_strictness"),
        }
        if schema_version != SETTINGS_SCHEMA_VERSION:
            artifact_keys.add(
                "artifact_subtype_in_names" if legacy else "subtype_in_names"
            )
        _unknown_keys(
            artifacts,
            artifact_keys,
            artifacts_name,
            issues,
        )
    priority = raw.get("priority")
    if isinstance(priority, dict):
        _unknown_keys(
            priority,
            {"scale", "default", "creation_defaults", "comparison"},
            "priority",
            issues,
        )
        creation_defaults = priority.get("creation_defaults")
        if isinstance(creation_defaults, dict):
            _unknown_keys(
                creation_defaults,
                {
                    "constraint",
                    "contract",
                    "requirement",
                    "decision",
                    "implementation",
                    "other",
                },
                "priority.creation_defaults",
                issues,
            )
        comparison = priority.get("comparison")
        if isinstance(comparison, dict):
            _unknown_keys(
                comparison,
                {
                    "strict_scope_ancestor_steps",
                    "earlier_layer_steps",
                    "bonuses_are_additive",
                    "cap",
                    "layer_order",
                    "peer_features_are_ordered",
                    "unrelated_scopes_receive_bonus",
                },
                "priority.comparison",
                issues,
            )
    workflows = raw.get("workflows")
    if isinstance(workflows, dict):
        _unknown_keys(workflows, {"implement"}, "workflows", issues)
        implement = workflows.get("implement")
        if isinstance(implement, dict):
            _unknown_keys(implement, {"mode"}, "workflows.implement", issues)
    compilation = raw.get("compilation")
    if isinstance(compilation, dict):
        _unknown_keys(
            compilation,
            {"mode", "skill", "runtime_output"},
            "compilation",
            issues,
        )
    changes = raw.get("changes")
    if isinstance(changes, dict):
        _unknown_keys(changes, {"default_workspace"}, "changes", issues)
    delegation = raw.get("delegation")
    if isinstance(delegation, dict):
        _unknown_keys(delegation, {"budget_profile"}, "delegation", issues)
    conflict_resolution = raw.get("conflict_resolution")
    if isinstance(conflict_resolution, dict):
        _unknown_keys(
            conflict_resolution,
            {
                "mode",
                "allowed_modes",
                "automatic_requires_unique_winner",
                "tie_or_same_level",
                "unknown_uncertain_or_incomparable",
                "unsatisfiable_external_obligations",
            },
            "conflict_resolution",
            issues,
        )
    governance_surfaces = raw.get("governance_surfaces")
    if isinstance(governance_surfaces, dict):
        _unknown_keys(
            governance_surfaces,
            set(GOVERNANCE_SURFACE_KEYS),
            "governance_surfaces",
            issues,
        )
    routing = raw.get("routing")
    if isinstance(routing, dict):
        _unknown_keys(
            routing,
            {
                "revision_modes",
                "content_roles",
                "governance_origins",
                "relation_shapes",
            },
            "routing",
            issues,
        )


def _unknown_keys(
    table: dict[str, Any], allowed: set[str], name: str, issues: list[str]
) -> None:
    for key in sorted(set(table) - allowed):
        issues.append(f"{name} has unknown setting: {key}")


def _table(value: object, name: str, issues: list[str]) -> dict[str, Any]:
    """Handle table using the declared repository contract."""
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


def _route_axis(
    value: object,
    name: str,
    canonical: tuple[str, ...],
    issues: list[str],
) -> tuple[str, ...]:
    """Require the complete ordered routing vocabulary for one axis."""
    if not isinstance(value, (list, tuple)) or not all(
        isinstance(item, str) for item in value
    ):
        issues.append(f"{name} must be a TOML array of strings")
        return canonical
    selected = tuple(value)
    if selected != canonical:
        issues.append(f"{name} must be: {', '.join(canonical)}")
        return canonical
    return selected


def _priority_scale(
    value: object,
    legacy: bool,
    current_contract: bool,
    issues: list[str],
) -> tuple[str, ...]:
    """Handle scale using the declared repository contract."""
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
    removed = sorted({"critical", "deferred"}.intersection(selected))
    if removed:
        issues.append("priority.scale contains removed values: " + ", ".join(removed))
        return DEFAULT_PRIORITY_SCALE
    if current_contract and selected != DEFAULT_PRIORITY_SCALE:
        issues.append("priority.scale must be high, medium, low")
        return DEFAULT_PRIORITY_SCALE
    return selected
