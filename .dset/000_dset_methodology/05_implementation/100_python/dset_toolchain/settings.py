"""Provide DSET settings behavior."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .artifact_routing import (
    CONTENT_ROLES,
    GOVERNANCE_LOCI,
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
SETTINGS_SCHEMA_VERSION = "1.8"
# PREVIOUS_SETTINGS_SCHEMA_VERSION defines the previous settings schema.
PREVIOUS_SETTINGS_SCHEMA_VERSION = "1.7"
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
        "1.4",
        "1.5",
        "1.6",
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
# MAINTAINED_VIEW_REFRESH_MODES defines maintained-view refresh timing.
MAINTAINED_VIEW_REFRESH_MODES = frozenset({"on_demand"})
# CONFLICT_RESOLUTION_MODES defines conflict selection modes.
CONFLICT_RESOLUTION_MODES = frozenset({"ask_always", "auto_by_effective_priority"})
# GOVERNANCE_SURFACE_KEYS defines optional governed project surfaces.
GOVERNANCE_SURFACE_KEYS = (
    "maintained_specification",
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
    maintained_view_refresh_mode: str = "on_demand"
    priority_scale: tuple[str, ...] = DEFAULT_PRIORITY_SCALE
    default_priority: str = "medium"
    conflict_resolution_mode: str = "ask_always"
    active_governance_surfaces: tuple[str, ...] = ()
    enabled_artifact_types: tuple[str, ...] = ()
    enabled_artifact_subtypes: tuple[str, ...] = ()
    routing_revision_modes: tuple[str, ...] = REVISION_MODES
    routing_content_roles: tuple[str, ...] = CONTENT_ROLES
    routing_governance_loci: tuple[str, ...] = GOVERNANCE_LOCI


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

    New writers use ``.dset/dset_settings.toml`` and schema 1.8. Earlier
    schemas and retired root filenames are migration inputs only. Competing
    names fail closed instead of selecting by precedence.
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
        issues.append("settings schema_version must be between 1.0 and 1.8")

    legacy = schema_version == LEGACY_SETTINGS_SCHEMA_VERSION
    _validate_known_keys(raw, schema_version, issues)
    artifacts_name = "optional_capabilities" if legacy else "artifacts"
    artifacts = _table(raw.get(artifacts_name), artifacts_name, issues)
    strictness_key = "artifact_creation_strictness" if legacy else "creation_strictness"

    identity = _table(artifacts.get("identity"), "artifacts.identity", issues)
    if schema_version == SETTINGS_SCHEMA_VERSION:
        include_subtype = _boolean(
            identity.get("subtype_in_names", False),
            "artifacts.identity.subtype_in_names",
            issues,
        )
    else:
        subtype_key = (
            "artifact_subtype_in_names" if legacy else "subtype_in_names"
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
        issues.append(f"{artifacts_name}.{strictness_key} must be medium or high")
        strictness = "medium"

    enabled_artifact_types = _string_axis(
        artifacts.get("enabled_types", []),
        "artifacts.enabled_types",
        issues,
    )
    enabled_artifact_subtypes = _string_axis(
        artifacts.get("enabled_subtypes", []),
        "artifacts.enabled_subtypes",
        issues,
    )

    implementation_mode = "lazy"
    maintained_view_refresh_mode = "on_demand"
    if not legacy:
        workflows = _table(raw.get("workflows"), "workflows", issues)
        implement = _table(workflows.get("implement"), "workflows.implement", issues)
        implementation_mode = _string(
            implement.get("mode", "lazy"), "workflows.implement.mode", issues
        )
        if implementation_mode not in IMPLEMENTATION_MODES:
            issues.append("workflows.implement.mode must be lazy or strict")
            implementation_mode = "lazy"
        view_section_name = (
            "maintained_views"
            if schema_version == SETTINGS_SCHEMA_VERSION
            else "compilation"
        )
        maintained_views = _table(
            raw.get(view_section_name),
            view_section_name,
            issues,
        )
        refresh_key = (
            "refresh_mode"
            if schema_version == SETTINGS_SCHEMA_VERSION
            else "mode"
        )
        maintained_view_refresh_mode = _string(
            maintained_views.get(refresh_key, "on_demand"),
            f"{view_section_name}.{refresh_key}",
            issues,
        )
        if maintained_view_refresh_mode not in MAINTAINED_VIEW_REFRESH_MODES:
            issues.append(
                f"{view_section_name}.{refresh_key} must be on_demand"
            )
            maintained_view_refresh_mode = "on_demand"

    change_workspace_mode = "integration-branch"
    delegation_budget_profile = "medium"
    if schema_version in {
        "1.2",
        HIDDEN_SETTINGS_SCHEMA_VERSION,
        "1.4",
        "1.5",
        "1.6",
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

    routing_name = (
        "artifacts.routing"
        if schema_version == SETTINGS_SCHEMA_VERSION
        else "routing"
    )
    routing = (
        _table(artifacts.get("routing"), routing_name, issues)
        if schema_version == SETTINGS_SCHEMA_VERSION
        else _table(raw.get("routing"), routing_name, issues)
    )
    routing_revision_modes = _route_axis(
        routing.get("revision_modes", REVISION_MODES),
        f"{routing_name}.revision_modes",
        REVISION_MODES,
        issues,
    )
    routing_content_roles = _route_axis(
        routing.get("content_roles", CONTENT_ROLES),
        f"{routing_name}.content_roles",
        CONTENT_ROLES,
        issues,
    )
    routing_governance_loci = _route_axis(
        routing.get("governance_loci", GOVERNANCE_LOCI),
        f"{routing_name}.governance_loci",
        GOVERNANCE_LOCI,
        issues,
    )
    if "internal" not in routing_governance_loci:
        issues.append(f"{routing_name}.governance_loci must include internal")

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
            maintained_view_refresh_mode=maintained_view_refresh_mode,
            priority_scale=priority_scale,
            default_priority=default_priority,
            conflict_resolution_mode=conflict_resolution_mode,
            active_governance_surfaces=active_governance_surfaces,
            enabled_artifact_types=enabled_artifact_types,
            enabled_artifact_subtypes=enabled_artifact_subtypes,
            routing_revision_modes=routing_revision_modes,
            routing_content_roles=routing_content_roles,
            routing_governance_loci=routing_governance_loci,
        ),
        tuple(issues),
    )


def _validate_known_keys(
    raw: dict[str, Any], schema_version: str, issues: list[str]
) -> None:
    """Validate known keys using the declared repository contract."""
    legacy = schema_version == LEGACY_SETTINGS_SCHEMA_VERSION
    current = schema_version == SETTINGS_SCHEMA_VERSION
    allowed_top = {
        "schema_version",
        "optional_capabilities" if legacy else "artifacts",
        "priority",
    }
    if not legacy:
        allowed_top.update(
            {
                "workflows",
                "maintained_views" if current else "compilation",
                "changes",
                "delegation",
            }
        )
    if schema_version in {
        "1.4",
        "1.5",
        "1.6",
        PREVIOUS_SETTINGS_SCHEMA_VERSION,
        SETTINGS_SCHEMA_VERSION,
    }:
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
                "artifact_structure",
                "governance_registry",
                "source_provenance",
                "version_registry",
                "conflict_resolution",
                "governance_surfaces",
            }
        )
    if current:
        allowed_top.update({"paths", "git", "interaction"})
    else:
        allowed_top.update({"artifact_catalog", "package_catalog", "routing"})
    _unknown_keys(raw, allowed_top, "settings", issues)

    artifacts_name = "optional_capabilities" if legacy else "artifacts"
    artifacts = raw.get(artifacts_name)
    if isinstance(artifacts, dict):
        artifact_keys = {
            ("artifact_creation_strictness" if legacy else "creation_strictness"),
        }
        if current:
            artifact_keys.update(
                {"enabled_types", "enabled_subtypes", "identity", "routing"}
            )
        else:
            artifact_keys.add(
                "artifact_subtype_in_names" if legacy else "subtype_in_names"
            )
        _unknown_keys(
            artifacts,
            artifact_keys,
            artifacts_name,
            issues,
        )
        identity = artifacts.get("identity")
        if isinstance(identity, dict):
            _unknown_keys(
                identity,
                {
                    "project_prefix_enabled",
                    "project_prefix",
                    "scope_path_in_ids",
                    "subtype_in_names",
                },
                "artifacts.identity",
                issues,
            )
        artifact_routing = artifacts.get("routing")
        if isinstance(artifact_routing, dict):
            _unknown_keys(
                artifact_routing,
                {"revision_modes", "content_roles", "governance_loci"},
                "artifacts.routing",
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
                    "implementation_decision",
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
        _unknown_keys(
            workflows,
            {"default_mode", "release_mode", "implement"} if current else {"implement"},
            "workflows",
            issues,
        )
        implement = workflows.get("implement")
        if isinstance(implement, dict):
            _unknown_keys(implement, {"mode"}, "workflows.implement", issues)
    maintained_views = raw.get("maintained_views")
    if isinstance(maintained_views, dict):
        _unknown_keys(
            maintained_views,
            {"refresh_mode", "skill"},
            "maintained_views",
            issues,
        )
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
    paths = raw.get("paths")
    if isinstance(paths, dict):
        _unknown_keys(
            paths,
            {"control_root", "journal_root", "runtime_root"},
            "paths",
            issues,
        )
    git = raw.get("git")
    if isinstance(git, dict):
        _unknown_keys(
            git,
            {"required", "initialize_if_missing", "commit_each_governed_change"},
            "git",
            issues,
        )
    interaction = raw.get("interaction")
    if isinstance(interaction, dict):
        _unknown_keys(
            interaction,
            {"reporting_mode"},
            "interaction",
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


def _string_axis(
    value: object,
    name: str,
    issues: list[str],
) -> tuple[str, ...]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item for item in value
    ):
        issues.append(f"{name} must be a list of non-empty strings")
        return ()
    normalized = tuple(str(item) for item in value)
    if len(normalized) != len(set(normalized)):
        issues.append(f"{name} must not contain duplicates")
    return normalized


def _route_axis(
    value: object,
    name: str,
    canonical: tuple[str, ...],
    issues: list[str],
) -> tuple[str, ...]:
    """Require a non-empty ordered subset of one routing vocabulary."""
    if not isinstance(value, (list, tuple)) or not all(
        isinstance(item, str) for item in value
    ):
        issues.append(f"{name} must be a TOML array of strings")
        return canonical
    selected = tuple(value)
    if (
        not selected
        or len(selected) != len(set(selected))
        or any(item not in canonical for item in selected)
        or selected != tuple(item for item in canonical if item in selected)
    ):
        issues.append(
            f"{name} must be an ordered unique subset of: {', '.join(canonical)}"
        )
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
