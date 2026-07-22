from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote

from . import __version__
from .carrier_transitions import (
    ledger_path as carrier_transition_ledger_path,
)
from .carrier_transitions import (
    load_ledger as load_transition_ledger,
)
from .carrier_transitions import (
    transition_aliases,
    validate_carrier_transition_ledger,
)
from .commit_provenance import validate_commit_provenance
from .compilation import compilation_is_fresh, compilation_path
from .dependencies import validate_dependency_policy
from .diagnostics import Diagnostic
from .evidence import validate_evidence_records
from .frontmatter import FrontmatterError
from .frontmatter import metadata as frontmatter_metadata
from .frontmatter import parse as parse_frontmatter
from .governance import validate_governance
from .health import health_is_fresh, health_path
from .identity import find_unique_name, has_logical_part, logical_part
from .layout import (
    ID_TOKEN_LAYERS,
    LAYER_DIRECTORIES,
    LAYER_ID_TOKENS,
    LAYERS,
    RepositoryLayout,
    discover_layout,
)
from .legacy_authority import legacy_authority_ids
from .lineage import validate_artifact_lineage
from .profiles import VALID_PROFILES, required_artifacts
from .project_data import project_section
from .semantic_atoms import collect_semantic_atoms, validate_semantic_atoms
from .semantic_types import classify_semantic_id, validate_semantic_classifications
from .settings import load_project_settings, selected_settings_path
from .yaml_subset import YamlSubsetError, load

ID_PATTERN = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)+$")
CHANGE_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROJECT_KEY_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*$")
TRACE_LAYERS = tuple(LAYER_ID_TOKENS.values())
TRACE_TYPES = (
    "DECISION",
    "REQUIREMENT",
    "CONSTRAINT",
    "CONTRACT",
    "STORY",
    "OUTCOME",
    "SCENARIO",
    "INVARIANT",
    "QUESTION",
    "CONFLICT",
    "RISK",
    "OPPORTUNITY",
    "PROBLEM",
    "DEFECT",
    "GAP",
    "DEBT",
    "TEST",
    "EVAL",
    "EVALUATION",
    "TASK",
    "CHANGE",
)
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CALLOUT_PATTERN = re.compile(r"^> \[!([^\]]+)\]", re.MULTILINE)
GITHUB_CALLOUTS = {"NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION"}
MARKDOWN_IGNORED_PARTS = frozenset(
    {
        ".cache",
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".uv-cache",
        ".venv",
        "__pycache__",
        "coverage",
        "dist",
        "node_modules",
        "temp",
        "tmp",
    }
)
LLM_SESSION_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*:[A-Za-z0-9._:-]+$")
LLM_SESSION_FIELD_PATTERN = re.compile(
    r"^\s*(?:-\s*)?\*\*LLM session IDs?:\*\*\s*(.*)$",
    re.IGNORECASE,
)
ARTIFACT_CLASSIFICATION_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
ARTIFACT_TYPE_SUBTYPES: dict[str, frozenset[str]] = {
    "atomic_record": frozenset(),
    "analysis_report": frozenset(
        {
            "solution_landscape",
            "root_cause_analysis",
            "proposal",
            "technical_investigation",
            "external_audit_analysis",
        }
    ),
    "specification": frozenset(
        {
            "domain_model",
            "behavior",
            "architecture",
            "design",
            "governance",
        }
    ),
    "procedure": frozenset({"playbook", "runbook"}),
    "plan": frozenset(
        {
            "implementation_plan",
            "test_plan",
            "evaluation_plan",
        }
    ),
    "version": frozenset(
        {
            "roadmap",
            "version_scope",
            "change",
            "release_plan",
            "readiness_record",
            "release_record",
        }
    ),
    "implementation": frozenset(
        {
            "source_code",
            "documentation",
            "configuration",
            "migration",
            "test_implementation",
            "evaluation_implementation",
        }
    ),
    "evidence_record": frozenset(
        {"test_result", "evaluation_result", "review_report", "run_record"}
    ),
    "verification": frozenset(),
    "derived_view": frozenset(
        {"project_overview", "health_dashboard", "traceability_index", "changelog"}
    ),
    "navigation": frozenset({"readme", "hub", "index"}),
}


def validate_repository(root: Path) -> list[Diagnostic]:
    root = root.resolve()
    diagnostics: list[Diagnostic] = []
    settings, settings_issues = load_project_settings(root)
    include_subtype_in_names = settings.artifact_subtype_in_names
    diagnostics.extend(
        _diag("DSET-E157", selected_settings_path(root), issue)
        for issue in settings_issues
    )
    try:
        layout = discover_layout(root)
    except ValueError as error:
        return [_diag("DSET-E001", root / ".dset", str(error))]
    manifest_path = layout.manifest_path
    if not manifest_path.is_file():
        return [_diag("DSET-E001", manifest_path, "project manifest is missing")]
    manifest = _safe_load(manifest_path, diagnostics)
    if manifest:
        diagnostics.extend(_validate_project_manifest(root, manifest_path, manifest))
        diagnostics.extend(_validate_intake_registry(root, manifest))
        diagnostics.extend(
            _validate_artifacts(
                root,
                manifest_path,
                manifest,
                include_subtype_in_names=include_subtype_in_names,
            )
        )
        profiles = manifest.get("profiles", {})
        if isinstance(profiles, dict) and profiles.get("repository_governance"):
            diagnostics.extend(
                validate_governance(root, str(profiles["repository_governance"]))
            )
        diagnostics.extend(_validate_version(root, manifest, layout))
    try:
        schema_paths = tuple(layout.schema_paths())
    except ValueError as error:
        diagnostics.append(_diag("DSET-E118", layout.dset_root, str(error)))
        schema_paths = ()
    diagnostics.extend(_validate_schemas(schema_paths))
    diagnostics.extend(_validate_provenance(root))
    diagnostics.extend(_validate_packages(root, manifest or {}))
    diagnostics.extend(_validate_change_uniqueness(layout))
    for active in layout.active_change_roots:
        if not active.is_dir():
            continue
        for path in sorted(active.iterdir()):
            if path.is_dir() and path.name != "archive":
                diagnostics.extend(validate_change(root, path, archived=False))
    for archive in layout.archive_change_roots:
        if not archive.is_dir():
            continue
        for path in sorted(archive.iterdir()):
            if path.is_dir() and re.match(r"^\d{4}-\d{2}-\d{2}-", path.name):
                diagnostics.extend(validate_change(root, path, archived=True))
    diagnostics.extend(_validate_markdown(root, layout))
    if not layout.separated:
        transition_ledger = layout.migrations_root / "carrier-transitions.toml"
        diagnostics.extend(
            _diag("DSET-E168", transition_ledger, issue)
            for issue in validate_carrier_transition_ledger(root)
        )
    diagnostics.extend(validate_semantic_atoms(root))
    diagnostics.extend(validate_semantic_classifications(root))
    diagnostics.extend(validate_artifact_lineage(root))
    diagnostics.extend(validate_dependency_policy(root))
    diagnostics.extend(validate_commit_provenance(root))
    if health_path(root).is_file() and not health_is_fresh(root):
        diagnostics.append(
            _diag("DSET-E162", health_path(root), "project health is stale")
        )
    if compilation_path(root).is_file() and not compilation_is_fresh(root):
        diagnostics.append(
            _diag(
                "DSET-E164",
                compilation_path(root),
                "active authority compilation is stale or incomplete",
            )
        )
    return sorted(set(diagnostics))


def validate_change(
    root: Path,
    change_dir: Path,
    *,
    archived: bool,
    expected_relative: str | None = None,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    merged = change_dir / "test-eval-plan.md"
    if merged.exists():
        diagnostics.append(
            _diag(
                "DSET-E105",
                merged,
                "tests and evals must remain separate artifacts",
            )
        )
        return diagnostics
    manifest_path = discover_layout(root).structured_file(change_dir, "change.toml")
    if not manifest_path.is_file():
        return [_diag("DSET-E102", manifest_path, "change manifest is missing")]
    data = _safe_load(manifest_path, diagnostics)
    if not data:
        return diagnostics
    layout = discover_layout(root)
    layered = layout.layered
    change_id = str(data.get("id", ""))
    folder_id = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", change_dir.name)
    change_slug = str(data.get("slug", "")) if layered else change_id
    if not CHANGE_PATTERN.fullmatch(change_slug) or change_slug != folder_id:
        diagnostics.append(
            _diag(
                "DSET-E151" if layered else "DSET-E101",
                manifest_path,
                "change slug must be kebab-case and match its directory"
                if layered
                else "change ID must be kebab-case and match its directory",
            )
        )
    profile = str(data.get("profile", ""))
    if profile not in VALID_PROFILES:
        diagnostics.append(
            _diag("DSET-E103", manifest_path, f"unknown change profile: {profile}")
        )
        return diagnostics
    if not layout.slim:
        try:
            files, directories = required_artifacts(root, profile)
        except (KeyError, ValueError, YamlSubsetError) as error:
            diagnostics.append(_diag("DSET-E103", manifest_path, str(error)))
            return diagnostics
        for relative in sorted(files):
            requested = change_dir / relative
            path = (
                layout.structured_file(change_dir, relative)
                if requested.suffix.lower() in {".toml", ".yaml", ".yml"}
                else requested
            )
            if not path.is_file():
                diagnostics.append(
                    _diag("DSET-E104", path, "required artifact is missing")
                )
        for relative in sorted(directories):
            path = change_dir / relative
            if not path.is_dir():
                diagnostics.append(
                    _diag("DSET-E104", path, "required artifact directory is missing")
                )
    if not _is_legacy_change(data) and not _valid_llm_session_ids(
        data.get("llm_session_ids")
    ):
        diagnostics.append(
            _diag(
                "DSET-E155",
                manifest_path,
                "current Change manifests require unique host-prefixed "
                "llm_session_ids; use an empty list for human-only work",
            )
        )
    diagnostics.extend(_validate_atomic_markdown_provenance(change_dir))
    diagnostics.extend(_validate_change_ids(root, change_dir, data))
    if layered:
        diagnostics.extend(_validate_layered_change(layout, change_dir, data))
    status = data.get("status")
    pr = data.get("pull_request", {})
    pr_number = pr.get("number") if isinstance(pr, dict) else None
    if archived and (not isinstance(pr_number, int) or pr_number < 1):
        diagnostics.append(
            _diag(
                "DSET-E107",
                manifest_path,
                "archived changes require a repository-qualified PR",
            )
        )
    if archived and status != "archived":
        diagnostics.append(
            _diag("DSET-E108", manifest_path, "archive status must be archived")
        )
    if not archived and status == "archived":
        diagnostics.append(
            _diag("DSET-E108", manifest_path, "archived change is in active root")
        )
    if archived:
        archive = data.get("archive")
        if not isinstance(archive, dict):
            diagnostics.append(
                _diag("DSET-E108", manifest_path, "archive metadata is missing")
            )
        else:
            expected = None if layout.slim else expected_relative
            if expected is None:
                try:
                    expected = change_dir.relative_to(root).as_posix()
                except ValueError:
                    expected = None
            recorded_archive = archive.get("path")
            relocated_archive = None
            if layout.slim and isinstance(recorded_archive, str):
                relocated_manifest = _transition_current_path(
                    root, f"{recorded_archive}/change.toml"
                )
                if relocated_manifest is not None:
                    relocated_archive = PurePosixPath(
                        relocated_manifest
                    ).parent.as_posix()
            if expected and not (
                recorded_archive == expected or relocated_archive == expected
            ):
                diagnostics.append(
                    _diag(
                        "DSET-E150" if layered else "DSET-E108",
                        manifest_path,
                        "archive path does not match the change directory",
                    )
                )
        if layered:
            workspace = data.get("workspace")
            if not isinstance(workspace, dict) or not all(
                _is_exact_commit(workspace.get(field))
                for field in ("base_commit", "head_commit")
            ):
                diagnostics.append(
                    _diag(
                        "DSET-E152",
                        manifest_path,
                        "archived workspace requires exact base and head commits",
                    )
                )
    return diagnostics


def _validate_project_manifest(
    root: Path, path: Path, data: dict[str, Any]
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    project = data.get("project", {})
    project_key = project.get("key") if isinstance(project, dict) else None
    project_id = project.get("id") if isinstance(project, dict) else None
    repository_slug = (
        project.get("repository_slug") if isinstance(project, dict) else None
    )
    if (
        not isinstance(project_key, str)
        or PROJECT_KEY_PATTERN.fullmatch(project_key) is None
        or not isinstance(project_id, str)
        or not CHANGE_PATTERN.fullmatch(project_id)
        or not isinstance(repository_slug, str)
        or not CHANGE_PATTERN.fullmatch(repository_slug)
    ):
        diagnostics.append(
            _diag("DSET-E115", path, "repository identity is inconsistent")
        )
    packages = data.get("packages", [])
    ids = [item.get("id") for item in packages if isinstance(item, dict)]
    if not ids or len(ids) != len(set(ids)):
        diagnostics.append(
            _diag("DSET-E115", path, "package IDs must be non-empty and unique")
        )
    manifest_schema = str(data.get("schema_version"))
    if manifest_schema in {"1.2", "1.3", "1.4", "1.5"}:
        structure = data.get("structure")
        expected_layouts = {
            "1.2": {"layered-v1"},
            "1.3": {"slim-v1", "numbered-layers-v1"},
            "1.4": {"recursive-framework-v1"},
            "1.5": {"separated-methodology-v1"},
        }[manifest_schema]
        valid_structure = (
            isinstance(structure, dict)
            and set(structure) == {"layout"}
            and structure.get("layout") in expected_layouts
        )
        diagnostics.extend(_validate_work_areas(root, path, data.get("work_areas")))
        valid_packages = isinstance(packages, list) and bool(packages)
        if valid_packages:
            for item in packages:
                layers = item.get("layers") if isinstance(item, dict) else None
                valid_packages = (
                    isinstance(item, dict)
                    and set(item) == {"id", "status", "layers"}
                    and isinstance(item.get("id"), str)
                    and CHANGE_PATTERN.fullmatch(str(item.get("id"))) is not None
                    and item.get("status") in {"active", "retired"}
                    and isinstance(layers, list)
                    and bool(layers)
                    and len(layers) == len(set(layers))
                    and set(layers).issubset(set(LAYERS))
                )
                if not valid_packages:
                    break
        expected_change_contract = {
            "change_id_format": "project-type-layer-sequence",
            "change_slug_format": "kebab-case",
            "pull_request_required_before_archive": True,
            "archive_requires_fresh_verification": True,
            "keep_pull_request_draft_until_archive_ready": True,
        }
        if (
            not valid_structure
            or not valid_packages
            or data.get("change_contract") != expected_change_contract
        ):
            diagnostics.append(
                _diag(
                    "DSET-E143",
                    path,
                    "current schema requires its registered layout and "
                    "package id/status/layers",
                )
            )
    support = data.get("supportability", {})
    workflows = root / ".github" / "workflows"
    if workflows.is_dir() and support.get("status") != "applicable":
        diagnostics.append(
            _diag(
                "DSET-E115",
                path,
                "hosted production automation requires supportability",
            )
        )
    command = str(data.get("canonical_command", ""))
    if "pending" in command.lower() or not command:
        diagnostics.append(
            _diag("DSET-E116", path, "canonical command is not executable")
        )
    work_items = data.get("work_items", {})
    registry = work_items.get("registry") if isinstance(work_items, dict) else None
    if data.get("schema_version") == 1.1 and registry not in {
        "dset/intake.toml",
        "dset/intake.yaml",
    }:
        diagnostics.append(
            _diag("DSET-E115", path, "schema 1.1 requires the central intake path")
        )
    elif isinstance(registry, str) and not (root / registry).is_file():
        diagnostics.append(
            _diag("DSET-E115", root / registry, "work-item registry is missing")
        )
    if manifest_schema in {"1.2", "1.3"}:
        expected_registries = (
            {"00_project/intake.toml"}
            if str(data.get("schema_version")) == "1.3"
            else {
                "dset/scopes/gov/intake.toml",
                "dset/scopes/gov/intake.yaml",
            }
        )
        if registry not in expected_registries:
            diagnostics.append(
                _diag(
                    "DSET-E143",
                    path,
                    "project schema requires its canonical intake path",
                )
            )
        return diagnostics
    if manifest_schema in {"1.4", "1.5"}:
        return diagnostics
    contracts = data.get("contracts")
    if not isinstance(project_key, str):
        return diagnostics
    contract_pattern = _trace_id_pattern(project_key, ("CONTRACT",))
    if not isinstance(contracts, list) or any(
        not isinstance(identifier, str)
        or contract_pattern.fullmatch(identifier) is None
        for identifier in contracts
    ):
        diagnostics.append(
            _diag("DSET-E115", path, "project contract IDs are inconsistent")
        )
    for group, trace_type in (("stories", "STORY"), ("outcomes", "OUTCOME")):
        if group not in data:
            continue
        identifiers = data[group]
        pattern = _trace_id_pattern(project_key, (trace_type,))
        if not isinstance(identifiers, list) or any(
            not isinstance(identifier, str) or pattern.fullmatch(identifier) is None
            for identifier in identifiers
        ):
            diagnostics.append(
                _diag("DSET-E115", path, f"project {group} IDs are inconsistent")
            )
    return diagnostics


def _validate_work_areas(
    root: Path, manifest_path: Path, raw_work_areas: object
) -> list[Diagnostic]:
    valid = isinstance(raw_work_areas, list)
    identifiers: set[str] = set()
    raw_paths: set[str] = set()
    resolved_paths: set[Path] = set()
    for raw_item in raw_work_areas if isinstance(raw_work_areas, list) else []:
        if not isinstance(raw_item, dict) or set(raw_item) != {"id", "path"}:
            valid = False
            continue
        identifier = raw_item.get("id")
        relative = raw_item.get("path")
        if (
            not isinstance(identifier, str)
            or CHANGE_PATTERN.fullmatch(identifier) is None
            or not isinstance(relative, str)
        ):
            valid = False
            continue
        resolved = _safe_repository_directory(root, relative)
        if (
            identifier in identifiers
            or relative in raw_paths
            or resolved is None
            or resolved in resolved_paths
        ):
            valid = False
        identifiers.add(identifier)
        raw_paths.add(relative)
        if resolved is not None:
            resolved_paths.add(resolved)
    if valid:
        return []
    return [
        _diag(
            "DSET-E143",
            manifest_path,
            "work areas require unique kebab-case IDs and safe unique existing "
            "repository-relative directory paths",
        )
    ]


def _safe_repository_directory(root: Path, relative: str) -> Path | None:
    if (
        not relative
        or "\\" in relative
        or re.match(r"^[A-Za-z]:", relative)
        or any(part in {"", ".", ".."} for part in relative.split("/"))
    ):
        return None
    candidate = root.joinpath(*relative.split("/"))
    try:
        resolved = candidate.resolve()
        resolved.relative_to(root.resolve())
    except (OSError, ValueError):
        return None
    return resolved if candidate.is_dir() else None


def _validate_intake_registry(root: Path, manifest: dict[str, Any]) -> list[Diagnostic]:
    work_items = manifest.get("work_items", {})
    relative = work_items.get("registry") if isinstance(work_items, dict) else None
    if not isinstance(relative, str):
        return []
    path = root / relative
    if not path.is_file():
        return []
    diagnostics: list[Diagnostic] = []
    data = _safe_load(path, diagnostics)
    if not data:
        return diagnostics
    project_key = _manifest_project_key(manifest)
    if project_key is None:
        return diagnostics
    layered = str(manifest.get("schema_version")) in {"1.2", "1.3"}
    scopes: dict[str, str]
    if layered:
        scopes = dict(LAYER_ID_TOKENS)
        intake_schema = str(data.get("schema_version"))
        if intake_schema not in {"1.1", "1.2"} or any(
            key in data for key in ("scope_mode", "scopes")
        ):
            diagnostics.append(
                _diag(
                    "DSET-E142",
                    path,
                    "layered intake derives the fixed layers and cannot redefine them",
                )
            )
    else:
        if data.get("scope_mode") != "multi-scope":
            diagnostics.append(
                _diag("DSET-E142", path, "intake must use registered layer scopes")
            )
        raw_scopes = data.get("scopes")
        if not isinstance(raw_scopes, list):
            diagnostics.append(_diag("DSET-E142", path, "scopes must be a list"))
            return diagnostics
        scopes = {}
        seen_segments: set[str] = set()
        for raw_scope in raw_scopes:
            if not isinstance(raw_scope, dict):
                diagnostics.append(
                    _diag("DSET-E142", path, "every scope must be a mapping")
                )
                continue
            scope_id = raw_scope.get("id")
            segment = raw_scope.get("id_segment")
            if (
                not isinstance(scope_id, str)
                or not isinstance(segment, str)
                or segment not in TRACE_LAYERS
                or raw_scope.get("kind") != "layer"
                or scope_id != ID_TOKEN_LAYERS[segment]
                or scope_id in scopes
                or segment in seen_segments
            ):
                diagnostics.append(
                    _diag("DSET-E142", path, f"invalid layer scope: {scope_id}")
                )
                continue
            scopes[scope_id] = segment
            seen_segments.add(segment)
        if seen_segments != set(TRACE_LAYERS):
            diagnostics.append(
                _diag(
                    "DSET-E142",
                    path,
                    "intake must register META, GOV, TOOL, SKILL, IMPL, and OPS "
                    "exactly once",
                )
            )
    raw_items = data.get("items")
    if not isinstance(raw_items, list):
        diagnostics.append(_diag("DSET-E142", path, "items must be a list"))
        return diagnostics
    seen_ids: set[str] = set()
    legacy_intake = str(data.get("schema_version")) == "1.1"
    item_pattern = _trace_id_pattern(
        project_key,
        (
            "PROBLEM",
            "DEFECT",
            "GAP",
            "DEBT",
            "QUESTION",
            "CONFLICT",
            "RISK",
            "OPPORTUNITY",
        ),
    )
    decision_pattern = _trace_id_pattern(
        project_key,
        (
            "DECISION",
            "REQUIREMENT",
            "CONSTRAINT",
            "CONTRACT",
            "STORY",
            "OUTCOME",
            "SCENARIO",
            "INVARIANT",
        ),
    )
    for raw_item in raw_items:
        if not isinstance(raw_item, dict):
            diagnostics.append(
                _diag("DSET-E142", path, "every intake item must be a mapping")
            )
            continue
        identifier = raw_item.get("id")
        match = (
            item_pattern.fullmatch(identifier) if isinstance(identifier, str) else None
        )
        scope_id = raw_item.get("scope")
        scope_segment = scopes.get(scope_id) if isinstance(scope_id, str) else None
        item_type = raw_item.get("type")
        item_subtype = raw_item.get("subtype")
        identity_classification = (
            classify_semantic_id(identifier) if isinstance(identifier, str) else None
        )
        declared_classification = (
            (str(item_type), str(item_subtype) if item_subtype is not None else None)
            if isinstance(item_type, str)
            else None
        )
        classification_matches = match is not None and (
            (
                legacy_intake
                and match.group("type").lower() == item_type
                and item_subtype is None
            )
            or (
                not legacy_intake
                and identity_classification == declared_classification
                and item_type in {"question", "problem"}
            )
        )
        if (
            match is None
            or identifier in seen_ids
            or not isinstance(item_type, str)
            or not classification_matches
            or scope_segment is None
            or (
                match.group("layer") is not None
                and match.group("layer") != scope_segment
            )
        ):
            diagnostics.append(
                _diag("DSET-E142", path, f"invalid intake identity: {identifier}")
            )
        elif isinstance(identifier, str):
            seen_ids.add(identifier)
        if not _valid_llm_session_ids(raw_item.get("llm_session_ids")):
            diagnostics.append(
                _diag(
                    "DSET-E155",
                    path,
                    f"intake item {identifier} requires unique host-prefixed "
                    "llm_session_ids; use an empty list for human-only work",
                )
            )
        decision = raw_item.get("decision")
        owner_change = raw_item.get("owner_change")
        if layered and owner_change not in (None, "pending"):
            owner_match = (
                _trace_id_pattern(project_key, ("CHANGE",)).fullmatch(owner_change)
                if isinstance(owner_change, str)
                else None
            )
            if owner_match is None or owner_match.group("layer") is None:
                diagnostics.append(
                    _diag(
                        "DSET-E142",
                        path,
                        f"invalid owner Change identity: {owner_change}",
                    )
                )
        if decision in (None, "pending"):
            continue
        decision_match = (
            decision_pattern.fullmatch(decision) if isinstance(decision, str) else None
        )
        if (
            decision_match is None
            or scope_segment is None
            or (
                decision_match.group("layer") is not None
                and decision_match.group("layer") != scope_segment
            )
        ):
            diagnostics.append(
                _diag("DSET-E142", path, f"invalid Decision identity: {decision}")
            )
    return diagnostics


def _valid_llm_session_ids(value: object) -> bool:
    if not isinstance(value, list):
        return False
    if any(
        not isinstance(identifier, str)
        or LLM_SESSION_ID_PATTERN.fullmatch(identifier) is None
        for identifier in value
    ):
        return False
    return len(value) == len(set(value))


def _markdown_has_session_provenance(path: Path) -> bool:
    try:
        metadata = frontmatter_metadata(path)
    except (OSError, UnicodeError, FrontmatterError):
        metadata = None
    if metadata is not None and "llm_session_ids" in metadata:
        return _valid_llm_session_ids(metadata["llm_session_ids"])

    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        match = LLM_SESSION_FIELD_PATTERN.fullmatch(line)
        if match is None:
            continue
        block = [match.group(1)]
        for following in lines[index + 1 :]:
            if following.startswith("##"):
                break
            if following and not following.startswith((" ", "-", "`")):
                break
            block.append(following)
        value = "\n".join(block)
        if re.search(r"\bnone\b", value, flags=re.IGNORECASE):
            return True
        return any(
            LLM_SESSION_ID_PATTERN.fullmatch(candidate) is not None
            for candidate in re.findall(r"`([^`]+)`", value)
        )
    return False


def _validate_atomic_markdown_provenance(change_dir: Path) -> list[Diagnostic]:
    paths = list(change_dir.glob("decision-*.md"))
    proofs = change_dir / "proofs"
    if proofs.is_dir():
        paths.extend(path for path in proofs.glob("*.md") if path.name != "README.md")
    return [
        _diag(
            "DSET-E155",
            path,
            "Decision and promoted proof records require an LLM session IDs "
            "field with host-prefixed IDs or explicit none",
        )
        for path in sorted(paths)
        if not _markdown_has_session_provenance(path)
    ]


def _validate_version(
    root: Path, manifest: dict[str, Any], layout: RepositoryLayout
) -> list[Diagnostic]:
    project = manifest.get("project", {})
    role = project.get("repository_role") if isinstance(project, dict) else None
    path = layout.version_path
    if role != "framework-source-and-adopter" and not path.exists():
        return []
    diagnostics: list[Diagnostic] = []
    if layout.recursive or layout.separated:
        try:
            data = project_section(root, "version_registry")
        except (OSError, ValueError, YamlSubsetError) as error:
            diagnostics.append(_diag("DSET-E124", path, str(error)))
            data = None
    else:
        data = _safe_load(path, diagnostics)
    if not data:
        return diagnostics or [_diag("DSET-E124", path, "version contract is missing")]
    framework = data.get("framework", {})
    package = data.get("python_package", {})
    schemas = data.get("schemas", {})
    released = data.get("released_validator", {})
    product_version = framework.get("version") if isinstance(framework, dict) else None
    if (
        not isinstance(framework, dict)
        or not isinstance(product_version, str)
        or _python_release_version(product_version) != __version__
        or framework.get("versioning") != "coordinated-product-package"
    ):
        diagnostics.append(
            _diag("DSET-E124", path, "framework version contract is inconsistent")
        )
    if (
        not isinstance(package, dict)
        or package.get("version") != __version__
        or package.get("versioning") != "coordinated-product-package"
    ):
        diagnostics.append(
            _diag("DSET-E124", path, "Python package version contract is inconsistent")
        )
    if (
        not isinstance(schemas, dict)
        or schemas.get("version") != "1.2"
        or schemas.get("versioning") != "independent"
    ):
        diagnostics.append(
            _diag("DSET-E124", path, "schema version contract is inconsistent")
        )
    commit = released.get("commit") if isinstance(released, dict) else None
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        diagnostics.append(
            _diag("DSET-E124", path, "released validator commit must be a full SHA")
        )
    if data.get("schema_version") != "1.2" or released.get("assurance") not in {
        "published-release",
        "bootstrap-transition",
    }:
        diagnostics.append(
            _diag("DSET-E124", path, "validator assurance contract is inconsistent")
        )
    return diagnostics


def _python_release_version(product_version: str) -> str:
    return product_version.replace("-rc.", "rc")


def _validate_packages(root: Path, manifest: dict[str, Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    layout = discover_layout(root)
    if layout.layered:
        return _validate_layered_packages(root, layout, manifest)
    project_key = _manifest_project_key(manifest)
    if project_key is None:
        return diagnostics
    group_types = {
        "requirements": "REQUIREMENT",
        "tests": "TEST",
        "evals": "EVAL",
        "contracts": "CONTRACT",
        "stories": "STORY",
        "outcomes": "OUTCOME",
    }
    for package in manifest.get("packages", []):
        if not isinstance(package, dict):
            continue
        base = layout.resolve_dset_path(str(package.get("path", "")))
        package_manifest = layout.structured_file(base, "package.toml")
        if not package_manifest.is_file():
            diagnostics.append(
                _diag("DSET-E117", package_manifest, "package manifest is missing")
            )
            continue
        data = _safe_load(package_manifest, diagnostics)
        if not data:
            continue
        if data.get("id") != package.get("id"):
            diagnostics.append(
                _diag("DSET-E117", package_manifest, "package ID mismatch")
            )
        artifacts = data.get("artifacts", {})
        if not isinstance(artifacts, dict):
            diagnostics.append(
                _diag("DSET-E117", package_manifest, "artifacts must be a mapping")
            )
            continue
        for relative in artifacts.values():
            path = base / str(relative)
            if not path.is_file():
                diagnostics.append(
                    _diag("DSET-E117", path, "package artifact is missing")
                )
        owner_paths = {
            "requirements": [base / str(artifacts.get("spec", "spec.md"))],
            "tests": [base / str(artifacts.get("test_plan", "test-plan.md"))],
            "evals": [base / str(artifacts.get("eval_plan", "eval-plan.md"))],
            "contracts": [base / str(artifacts.get("contracts", "contracts.md"))],
            "stories": [base / str(artifacts.get("stories", "stories.md"))],
            "outcomes": [base / str(artifacts.get("outcomes", "outcomes.md"))],
        }
        for group, trace_type in group_types.items():
            if group in {"stories", "outcomes"} and group not in data:
                continue
            identifiers = data.get(group)
            if not isinstance(identifiers, list):
                diagnostics.append(
                    _diag("DSET-E117", package_manifest, f"{group} must be a list")
                )
                continue
            pattern = _trace_id_pattern(
                project_key,
                ("EVAL", "EVALUATION") if trace_type == "EVAL" else (trace_type,),
            )
            content = "\n".join(
                path.read_text(encoding="utf-8")
                for path in owner_paths[group]
                if path.is_file()
            )
            for identifier in identifiers:
                if (
                    not isinstance(identifier, str)
                    or pattern.fullmatch(identifier) is None
                ):
                    diagnostics.append(
                        _diag(
                            "DSET-E117",
                            package_manifest,
                            f"invalid {group} ID: {identifier}",
                        )
                    )
                elif identifier not in content:
                    diagnostics.append(
                        _diag(
                            "DSET-E117",
                            package_manifest,
                            f"{identifier} is not present in its owning artifact",
                        )
                    )
                elif group in {"stories", "outcomes"}:
                    missing = _missing_semantic_fields(
                        owner_paths[group], identifier, trace_type
                    )
                    if missing:
                        diagnostics.append(
                            _diag(
                                "DSET-E117",
                                package_manifest,
                                f"{identifier} is missing fields: {', '.join(missing)}",
                            )
                        )
    return diagnostics


def _validate_layered_packages(
    root: Path, layout: RepositoryLayout, manifest: dict[str, Any]
) -> list[Diagnostic]:
    if layout.separated:
        return _validate_catalog_packages(root, layout, manifest)
    diagnostics: list[Diagnostic] = []
    project_key = _manifest_project_key(manifest)
    if project_key is None:
        return diagnostics
    declared: dict[str, set[str]] = {}
    for item in manifest.get("packages", []):
        if not isinstance(item, dict):
            continue
        package_id = item.get("id")
        layers = item.get("layers")
        if isinstance(package_id, str) and isinstance(layers, list):
            declared[package_id] = {layer for layer in layers if isinstance(layer, str)}
    expected = {
        (package_id, layer)
        for package_id, layers in declared.items()
        for layer in layers
    }
    found: set[tuple[str, str]] = set()
    owners: dict[str, Path] = {}
    group_types = {
        "requirements": "REQUIREMENT",
        "tests": "TEST",
        "evals": "EVAL",
        "contracts": "CONTRACT",
        "stories": "STORY",
        "outcomes": "OUTCOME",
    }
    artifact_names = (
        {
            "hub": "navigation-methodology.md",
            "domain": "specification-domain.md",
            "spec": "specification-methodology.md",
            "contracts": "specification-contracts.md",
            "stories": "specification-user-stories.md",
            "outcomes": "specification-outcomes.md",
            "test_plan": "plan-tests.md",
            "eval_plan": "plan-evaluations.md",
        }
        if layout.slim
        else {
            "hub": "README.md",
            "domain": "domain.md",
            "spec": "spec.md",
            "contracts": "contracts.md",
            "stories": "stories.md",
            "outcomes": "outcomes.md",
            "test_plan": "test-plan.md",
            "eval_plan": "eval-plan.md",
        }
    )
    owner_artifact = {
        "requirements": "spec",
        "tests": "test_plan",
        "evals": "eval_plan",
        "contracts": "contracts",
        "stories": "stories",
        "outcomes": "outcomes",
    }
    for path in layout.package_fragments():
        data = _safe_load(path, diagnostics)
        if not data:
            continue
        try:
            relative = path.relative_to(layout.scopes_root)
        except ValueError:
            diagnostics.append(
                _diag("DSET-E145", path, "package fragment is outside layer roots")
            )
            continue
        directory_layer = relative.parts[0]
        physical_layer = next(
            (
                layer
                for layer, directory in LAYER_DIRECTORIES.items()
                if directory == directory_layer
            ),
            directory_layer,
        )
        physical_package = (
            str(data.get("package_id")) if layout.slim else path.parent.name
        )
        package_id = data.get("package_id")
        layer = data.get("layer")
        identity = (str(package_id), str(layer))
        if (
            data.get("schema_version") != "1.2"
            or package_id != physical_package
            or layer != physical_layer
            or identity not in expected
        ):
            diagnostics.append(
                _diag(
                    "DSET-E145",
                    path,
                    "package fragment identity must match its derived path",
                )
            )
        else:
            found.add(identity)
        artifacts = data.get("artifacts")
        if not isinstance(artifacts, dict) or artifacts != artifact_names:
            diagnostics.append(
                _diag("DSET-E144", path, "package fragment artifacts are malformed")
            )
            artifacts = {}
        for name, filename in artifact_names.items():
            artifact = path.parent / filename
            if artifacts.get(name) == filename and not artifact.is_file():
                diagnostics.append(
                    _diag("DSET-E144", artifact, "package fragment artifact is missing")
                )
        for group, trace_type in group_types.items():
            identifiers = data.get(group)
            if not isinstance(identifiers, list) or len(identifiers) != len(
                set(
                    identifier
                    for identifier in identifiers
                    if isinstance(identifier, str)
                )
            ):
                diagnostics.append(
                    _diag("DSET-E144", path, f"{group} must be a unique list")
                )
                continue
            pattern = _trace_id_pattern(
                project_key,
                ("EVAL", "EVALUATION") if trace_type == "EVAL" else (trace_type,),
            )
            owner = path.parent / artifact_names[owner_artifact[group]]
            content = owner.read_text(encoding="utf-8") if owner.is_file() else ""
            for identifier in identifiers:
                match = (
                    pattern.fullmatch(identifier)
                    if isinstance(identifier, str)
                    else None
                )
                if match is None:
                    diagnostics.append(
                        _diag("DSET-E144", path, f"invalid {group} ID: {identifier}")
                    )
                    continue
                identifier_layer = match.group("layer")
                owns_id = (
                    physical_layer == "meta" and identifier_layer in {None, "META"}
                ) or identifier_layer == LAYER_ID_TOKENS[physical_layer]
                if not owns_id:
                    diagnostics.append(
                        _diag(
                            "DSET-E146",
                            path,
                            f"{identifier} is not owned by layer {physical_layer}",
                        )
                    )
                previous = owners.get(identifier)
                if previous is not None and previous != path:
                    diagnostics.append(
                        _diag(
                            "DSET-E147",
                            path,
                            f"{identifier} is also owned by "
                            f"{previous.relative_to(root)}",
                        )
                    )
                else:
                    owners[identifier] = path
                if identifier not in content:
                    diagnostics.append(
                        _diag(
                            "DSET-E144",
                            path,
                            f"{identifier} is not present in its owning artifact",
                        )
                    )
                elif group in {"stories", "outcomes"}:
                    missing = _missing_semantic_fields([owner], identifier, trace_type)
                    if missing:
                        diagnostics.append(
                            _diag(
                                "DSET-E144",
                                path,
                                f"{identifier} is missing fields: {', '.join(missing)}",
                            )
                        )
    for package_id, layer in sorted(expected - found):
        missing_path = layout.structured_file(
            layout.layer_root(layer) / "specs/packages" / package_id,
            "package.toml",
        )
        diagnostics.append(
            _diag("DSET-E144", missing_path, "declared package fragment is missing")
        )
    return diagnostics


def _validate_catalog_packages(
    root: Path, layout: RepositoryLayout, manifest: dict[str, Any]
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    declared = {
        (str(item.get("id")), str(layer))
        for item in manifest.get("packages", [])
        if isinstance(item, dict) and isinstance(item.get("layers"), list)
        for layer in item["layers"]
        if isinstance(layer, str)
    }
    catalog = project_section(root, "package_catalog")
    packages = catalog.get("packages", [])
    if not isinstance(packages, list):
        return [_diag("DSET-E144", layout.settings_path, "packages must be a list")]
    found: set[tuple[str, str]] = set()
    for package in packages:
        if not isinstance(package, dict):
            diagnostics.append(
                _diag("DSET-E144", layout.settings_path, "package must be a table")
            )
            continue
        identity = (str(package.get("package_id")), str(package.get("layer")))
        if identity not in declared or identity in found:
            diagnostics.append(
                _diag(
                    "DSET-E145",
                    layout.settings_path,
                    f"package identity is undeclared or duplicated: {identity}",
                )
            )
        found.add(identity)
        artifacts = package.get("artifacts")
        if not isinstance(artifacts, dict):
            diagnostics.append(
                _diag(
                    "DSET-E144",
                    layout.settings_path,
                    f"package artifacts are missing: {identity}",
                )
            )
            continue
        for role, carrier in artifacts.items():
            if not isinstance(carrier, str):
                diagnostics.append(
                    _diag(
                        "DSET-E144",
                        layout.settings_path,
                        f"package carrier name is invalid: {identity}/{role}",
                    )
                )
                continue
            try:
                find_unique_name(root, carrier)
            except (FileNotFoundError, ValueError):
                diagnostics.append(
                    _diag(
                        "DSET-E144",
                        layout.settings_path,
                        f"package carrier is missing or ambiguous: {carrier}",
                    )
                )
    for identity in sorted(declared - found):
        diagnostics.append(
            _diag(
                "DSET-E144",
                layout.settings_path,
                f"declared package layer is missing: {identity}",
            )
        )
    return diagnostics


def _validate_artifacts(
    root: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
    *,
    include_subtype_in_names: bool,
) -> list[Diagnostic]:
    profiles = manifest.get("profiles", {})
    if not isinstance(profiles, dict):
        return [_diag("DSET-E120", manifest_path, "profiles must be a mapping")]
    profile = profiles.get("artifact")
    if profile is None:
        return []
    if profile != "documentation-v1":
        return [
            _diag(
                "DSET-E120",
                manifest_path,
                f"unsupported artifact profile: {profile}",
            )
        ]
    layout = discover_layout(root)
    registry_path = layout.artifact_registry_path
    if not registry_path.is_file():
        return [
            _diag(
                "DSET-E120",
                registry_path,
                "documentation-v1 requires an artifact registry",
            )
        ]
    diagnostics: list[Diagnostic] = []
    try:
        registry = project_section(root, "artifact_structure")
    except (OSError, ValueError, YamlSubsetError) as error:
        diagnostics.append(_diag("DSET-E120", registry_path, str(error)))
        registry = {}
    if not registry:
        return diagnostics
    if registry.get("profile") != profile:
        diagnostics.append(
            _diag(
                "DSET-E120",
                registry_path,
                "artifact registry profile does not match project profile",
            )
        )
        return diagnostics
    diagnostics.extend(validate_artifact_registry(root, registry_path, registry))
    type_registry_path = layout.artifact_type_registry_path
    if not type_registry_path.is_file():
        diagnostics.append(
            _diag(
                "DSET-E156",
                type_registry_path,
                "documentation-v1 requires an artifact-type registry",
            )
        )
        return diagnostics
    try:
        type_registry = project_section(root, "artifact_catalog")
    except (OSError, ValueError, YamlSubsetError) as error:
        diagnostics.append(_diag("DSET-E156", type_registry_path, str(error)))
        type_registry = {}
    if type_registry:
        project = manifest.get("project", {})
        project_key = project.get("key") if isinstance(project, dict) else None
        diagnostics.extend(
            validate_artifact_type_registry(
                root,
                type_registry_path,
                type_registry,
                project_key=str(project_key) if project_key else None,
                include_subtype_in_names=include_subtype_in_names,
                separated=layout.separated,
            )
        )
    return diagnostics


def validate_artifact_type_registry(
    root: Path,
    registry_path: Path,
    data: dict[str, Any],
    *,
    project_key: str | None = None,
    include_subtype_in_names: bool = False,
    separated: bool = False,
) -> list[Diagnostic]:
    """Validate the documentation-v1 artifact-role vocabulary and path rules."""
    diagnostics: list[Diagnostic] = []
    if str(data.get("schema_version")) != "1.0":
        diagnostics.append(
            _diag("DSET-E156", registry_path, "schema_version must be 1.0")
        )
    if data.get("profile") != "documentation-v1":
        diagnostics.append(
            _diag("DSET-E156", registry_path, "profile must be documentation-v1")
        )
    diagnostics.extend(_validate_artifact_classification(registry_path, data))
    types, type_diagnostics = _artifact_type_catalog(registry_path, data)
    diagnostics.extend(type_diagnostics)
    exclusions, exclusion_diagnostics = _artifact_exclusions(registry_path, data)
    diagnostics.extend(exclusion_diagnostics)
    if separated:
        diagnostics.extend(
            validate_evidence_records(
                root.resolve(),
                _active_applied_files(root.resolve()),
                frozenset(),
                allow_unversioned_legacy=True,
            )
        )
        return diagnostics
    legacy_evidence, compatibility_diagnostics = _legacy_evidence_paths(
        registry_path, data
    )
    diagnostics.extend(compatibility_diagnostics)
    markdown_texts = _retention_markdown_texts(root.resolve())
    legacy_structured, structured_diagnostics = _legacy_structured_entries(
        root, registry_path, data, types, markdown_texts
    )
    diagnostics.extend(structured_diagnostics)
    diagnostics.extend(
        _validate_artifact_path_rules(
            root,
            registry_path,
            data,
            types,
            exclusions,
            legacy_evidence,
            legacy_structured,
            project_key=project_key,
            include_subtype_in_names=include_subtype_in_names,
        )
    )
    diagnostics.extend(
        validate_evidence_records(
            root.resolve(), _project_visible_files(root.resolve()), legacy_evidence
        )
    )
    if _within_root(root.resolve(), registry_path.resolve()):
        diagnostics.extend(
            _validate_legacy_structured_links(
                root.resolve(),
                registry_path,
                legacy_structured,
                legacy_evidence,
                markdown_texts,
            )
        )
    return diagnostics


def _validate_artifact_classification(
    registry_path: Path, data: dict[str, Any]
) -> list[Diagnostic]:
    expected = {
        "unclassified": "error",
        "multiple_matches": "error",
        "direct_metadata_fields": {
            "type": "artifact_type",
            "subtype": "artifact_subtype",
        },
    }
    if data.get("classification") != expected:
        return [
            _diag(
                "DSET-E156",
                registry_path,
                "classification policy and direct metadata fields are invalid",
            )
        ]
    return []


def _artifact_type_catalog(
    registry_path: Path, data: dict[str, Any]
) -> tuple[dict[str, frozenset[str]], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    raw_types = data.get("artifact_types")
    if not isinstance(raw_types, list) or not raw_types:
        return {}, [
            _diag(
                "DSET-E156",
                registry_path,
                "artifact_types must be a non-empty list",
            )
        ]
    catalog: dict[str, frozenset[str]] = {}
    questions: set[str] = set()
    for entry in raw_types:
        if not isinstance(entry, dict):
            diagnostics.append(
                _diag(
                    "DSET-E156", registry_path, "every artifact type must be a mapping"
                )
            )
            continue
        identifier = entry.get("id")
        if (
            not isinstance(identifier, str)
            or ARTIFACT_CLASSIFICATION_PATTERN.fullmatch(identifier) is None
        ):
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"invalid artifact type ID: {identifier}",
                )
            )
            continue
        if identifier in catalog:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"duplicate artifact type ID: {identifier}",
                )
            )
            continue
        question = entry.get("primary_question")
        if not isinstance(question, str) or not question.strip():
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"{identifier} requires a primary_question",
                )
            )
        elif question in questions:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"duplicate primary_question: {question}",
                )
            )
        else:
            questions.add(question)
        if not isinstance(entry.get("allow_empty_subtype"), bool):
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"{identifier} allow_empty_subtype must be boolean",
                )
            )
        raw_subtypes = entry.get("subtypes")
        if not isinstance(raw_subtypes, list):
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"{identifier} subtypes must be a flat list",
                )
            )
            catalog[identifier] = frozenset()
            continue
        subtypes: set[str] = set()
        for subtype in raw_subtypes:
            if (
                not isinstance(subtype, str)
                or ARTIFACT_CLASSIFICATION_PATTERN.fullmatch(subtype) is None
            ):
                diagnostics.append(
                    _diag(
                        "DSET-E156",
                        registry_path,
                        f"{identifier} contains an invalid or nested subtype",
                    )
                )
            elif subtype in subtypes:
                diagnostics.append(
                    _diag(
                        "DSET-E156",
                        registry_path,
                        f"{identifier} contains duplicate subtype: {subtype}",
                    )
                )
            else:
                subtypes.add(subtype)
        catalog[identifier] = frozenset(subtypes)
    if set(catalog) != set(ARTIFACT_TYPE_SUBTYPES):
        diagnostics.append(
            _diag(
                "DSET-E156",
                registry_path,
                "artifact_types must contain the eleven canonical types exactly",
            )
        )
    for identifier, expected in ARTIFACT_TYPE_SUBTYPES.items():
        if identifier in catalog and catalog[identifier] != expected:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"{identifier} direct subtype set does not match the profile",
                )
            )
    return catalog, diagnostics


def _artifact_exclusions(
    registry_path: Path, data: dict[str, Any]
) -> tuple[list[tuple[str, str]], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    raw_exclusions = data.get("exclusions")
    if not isinstance(raw_exclusions, list) or not raw_exclusions:
        return [], [
            _diag(
                "DSET-E156",
                registry_path,
                "exclusions must be a non-empty explicit registry",
            )
        ]
    exclusions: list[tuple[str, str]] = []
    seen: set[str] = set()
    for item in raw_exclusions:
        if not isinstance(item, dict) or set(item) != {"pattern", "rationale"}:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    "every exclusion requires exactly pattern and rationale",
                )
            )
            continue
        pattern = item.get("pattern")
        rationale = item.get("rationale")
        if not isinstance(pattern, str) or not pattern.strip():
            diagnostics.append(
                _diag("DSET-E156", registry_path, "exclusion pattern is missing")
            )
            continue
        if pattern in seen:
            diagnostics.append(
                _diag("DSET-E156", registry_path, f"duplicate exclusion: {pattern}")
            )
        seen.add(pattern)
        if not isinstance(rationale, str) or not rationale.strip():
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"exclusion {pattern} requires a rationale",
                )
            )
            continue
        exclusions.append((pattern, rationale))
    return exclusions, diagnostics


def _legacy_evidence_paths(
    registry_path: Path, data: dict[str, Any]
) -> tuple[frozenset[str], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    raw_paths = data.get("legacy_evidence_paths")
    if not isinstance(raw_paths, list):
        return frozenset(), [
            _diag(
                "DSET-E156",
                registry_path,
                "legacy_evidence_paths must be an explicit finite list",
            )
        ]
    paths: set[str] = set()
    for item in raw_paths:
        if (
            not isinstance(item, str)
            or not item.endswith(".md")
            or not any(segment in item for segment in ("/proofs/", "/evidence/"))
            or item.startswith("/")
            or any(token in item for token in ("*", "?", "[", "]"))
        ):
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"invalid legacy evidence path: {item}",
                )
            )
            continue
        if item in paths:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"duplicate legacy evidence path: {item}",
                )
            )
        paths.add(item)
    return frozenset(paths), diagnostics


def _legacy_structured_entries(
    root: Path,
    registry_path: Path,
    data: dict[str, Any],
    catalog: dict[str, frozenset[str]],
    markdown_texts: dict[Path, str],
) -> tuple[dict[str, dict[str, Any]], list[Diagnostic]]:
    """Validate the exact registry of byte-stable structured snapshots."""

    diagnostics: list[Diagnostic] = []
    raw_entries = data.get("legacy_structured")
    if not isinstance(raw_entries, list):
        return {}, [
            _diag(
                "DSET-E156",
                registry_path,
                "legacy_structured must be an explicit finite list",
            )
        ]
    entries: dict[str, dict[str, Any]] = {}
    owners: set[str] = set()
    enforce_repository_state = _within_root(root.resolve(), registry_path.resolve())
    ledger = _legacy_authority_records(root) if enforce_repository_state else []
    for item in raw_entries:
        if not isinstance(item, dict):
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    "every legacy_structured entry must be a mapping",
                )
            )
            continue
        allowed = {
            "path",
            "sha256",
            "current_owner",
            "current_path",
            "current_sha256",
            "transition_id",
            "artifact_type",
            "artifact_subtype",
            "retained_for",
        }
        required = allowed - {
            "artifact_subtype",
            "current_path",
            "current_sha256",
            "transition_id",
        }
        if not required.issubset(item) or set(item) - allowed:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    "legacy_structured entry has missing or unknown fields",
                )
            )
            continue
        raw_path = item.get("path")
        raw_owner = item.get("current_owner")
        if not _exact_registry_path(raw_path, suffixes={".yaml", ".yml"}):
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"invalid or wildcard legacy_structured path: {raw_path}",
                )
            )
            continue
        if not _exact_registry_path(raw_owner, suffixes={".toml"}):
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"invalid or wildcard current_owner path: {raw_owner}",
                )
            )
            continue
        assert isinstance(raw_path, str) and isinstance(raw_owner, str)
        if raw_path in entries:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"duplicate legacy_structured path: {raw_path}",
                )
            )
        if raw_owner in owners:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"duplicate legacy_structured current_owner: {raw_owner}",
                )
            )
        entries[raw_path] = item
        owners.add(raw_owner)

        artifact_type = item.get("artifact_type")
        subtype = item.get("artifact_subtype")
        if not isinstance(artifact_type, str) or artifact_type not in catalog:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"legacy_structured uses unknown artifact type: {artifact_type}",
                )
            )
        elif subtype is not None and (
            not isinstance(subtype, str) or subtype not in catalog[artifact_type]
        ):
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"legacy_structured {raw_path} has a subtype/type mismatch",
                )
            )

        if not enforce_repository_state:
            continue
        source = (root / raw_path).resolve()
        owner = (root / raw_owner).resolve()
        raw_current = item.get("current_path")
        current_digest = item.get("current_sha256")
        transition_id = item.get("transition_id")
        transitioned = all(
            isinstance(value, str)
            for value in (raw_current, current_digest, transition_id)
        )
        if (
            any(
                value is not None
                for value in (raw_current, current_digest, transition_id)
            )
            and not transitioned
        ):
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"legacy transition seal is incomplete: {raw_path}",
                )
            )
        invalid_source = (
            not _within_root(root, source)
            or not source.is_file()
            or source.is_symlink()
        )
        if invalid_source and not transitioned:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"legacy snapshot is missing: {raw_path}",
                )
            )
        elif not invalid_source:
            expected = item.get("sha256")
            actual = hashlib.sha256(source.read_bytes()).hexdigest()
            if (
                not isinstance(expected, str)
                or re.fullmatch(r"[0-9a-f]{64}", expected) is None
                or actual != expected
            ):
                diagnostics.append(
                    _diag(
                        "DSET-E156",
                        registry_path,
                        f"legacy snapshot digest changed: {raw_path}",
                    )
                )
        if transitioned:
            assert isinstance(raw_current, str)
            assert isinstance(current_digest, str)
            current = (root / raw_current).resolve()
            if (
                not _within_root(root, current)
                or not current.is_file()
                or current.is_symlink()
                or hashlib.sha256(current.read_bytes()).hexdigest() != current_digest
            ):
                diagnostics.append(
                    _diag(
                        "DSET-E156",
                        registry_path,
                        "legacy transition carrier is missing or changed: "
                        f"{raw_current}",
                    )
                )
        if not _within_root(root, owner) or not owner.is_file() or owner.is_symlink():
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"legacy snapshot current owner is missing: {raw_owner}",
                )
            )
        diagnostics.extend(
            _validate_retention_identities(
                root,
                registry_path,
                raw_path,
                item.get("retained_for"),
                ledger,
                current_path=item.get("current_path"),
                transition_id=item.get("transition_id"),
                markdown_texts=markdown_texts,
            )
        )

    if not enforce_repository_state:
        return entries, diagnostics
    for path in _project_visible_files(root):
        if path.suffix.lower() not in {".yaml", ".yml"}:
            continue
        relative = path.relative_to(root).as_posix()
        if path.with_suffix(".toml").is_file() and relative not in entries:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"unregistered YAML/TOML pair: {relative}",
                )
            )
    return entries, diagnostics


def _exact_registry_path(raw: object, *, suffixes: set[str]) -> bool:
    if not isinstance(raw, str) or not raw or raw.startswith("/") or "\\" in raw:
        return False
    if any(token in raw for token in ("*", "?", "[", "]")):
        return False
    path = PurePosixPath(raw)
    return path.suffix in suffixes and all(
        part not in {"", ".", ".."} for part in path.parts
    )


def _within_root(root: Path, path: Path) -> bool:
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _legacy_authority_records(root: Path) -> list[dict[str, Any]]:
    layout = discover_layout(root)
    path = layout.structured_file(layout.project_state_root, "legacy-authority.toml")
    if not path.is_file():
        return []
    try:
        data = load(path)
    except (OSError, ValueError, YamlSubsetError):
        return []
    records = data.get("records") if isinstance(data, dict) else None
    return (
        [item for item in records if isinstance(item, dict)]
        if isinstance(records, list)
        else []
    )


def _validate_retention_identities(
    root: Path,
    registry_path: Path,
    snapshot: str,
    raw_identities: object,
    ledger: list[dict[str, Any]],
    *,
    current_path: object = None,
    transition_id: object = None,
    markdown_texts: dict[Path, str] | None = None,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if markdown_texts is None:
        markdown_texts = _retention_markdown_texts(root.resolve())
    if not isinstance(raw_identities, list) or not raw_identities:
        return [
            _diag(
                "DSET-E156",
                registry_path,
                f"legacy_structured {snapshot} requires retained_for identities",
            )
        ]
    seen: set[tuple[str, str]] = set()
    snapshot_path = (root / snapshot).resolve()
    transition_target = _registered_transition_target(
        root, snapshot, current_path, transition_id
    )
    if (
        current_path is not None or transition_id is not None
    ) and transition_target is None:
        diagnostics.append(
            _diag(
                "DSET-E156",
                registry_path,
                f"legacy_structured {snapshot} transition is not registered",
            )
        )
    for identity in raw_identities:
        if not isinstance(identity, dict):
            diagnostics.append(
                _diag("DSET-E156", registry_path, "retained_for must be a mapping")
            )
            continue
        identity_keys = set(identity) - {"reason"}
        if (
            identity_keys not in ({"semantic_id"}, {"carrier_path"})
            or not isinstance(identity.get("reason"), str)
            or not str(identity["reason"]).strip()
        ):
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    "retained_for requires reason and exactly one of "
                    "semantic_id or carrier_path",
                )
            )
            continue
        key = next(iter(identity_keys))
        value = identity.get(key)
        if not isinstance(value, str) or not value:
            diagnostics.append(
                _diag("DSET-E156", registry_path, f"retained_for {key} is invalid")
            )
            continue
        marker = (key, value)
        if marker in seen:
            diagnostics.append(
                _diag("DSET-E156", registry_path, f"duplicate retained_for: {value}")
            )
        seen.add(marker)
        if key == "semantic_id":
            carriers = _semantic_retention_carriers(
                root, ledger, value, snapshot, markdown_texts
            )
            if not carriers:
                diagnostics.append(
                    _diag(
                        "DSET-E156",
                        registry_path,
                        "retained_for semantic ID does not select or link "
                        f"{snapshot}: {value}",
                    )
                )
        else:
            if not _exact_registry_path(value, suffixes={".md"}):
                diagnostics.append(
                    _diag(
                        "DSET-E156",
                        registry_path,
                        f"retained_for carrier_path is invalid: {value}",
                    )
                )
                continue
            carrier = (root / value).resolve()
            if (
                not _within_root(root, carrier)
                or not carrier.is_file()
                or not (
                    "/proofs/" in f"/{value}"
                    or discover_layout(root).slim
                    and "/evidence/" in f"/{value}"
                )
                or not (
                    _carrier_references_path(
                        root, carrier, snapshot_path, markdown_texts.get(carrier)
                    )
                    or transition_target is not None
                    and _carrier_references_path(
                        root,
                        carrier,
                        transition_target,
                        markdown_texts.get(carrier),
                    )
                )
            ):
                diagnostics.append(
                    _diag(
                        "DSET-E156",
                        registry_path,
                        f"historical carrier does not link {snapshot}: {value}",
                    )
                )
    return diagnostics


def _registered_transition_target(
    root: Path,
    original_path: str,
    current_path: object,
    transition_id: object,
) -> Path | None:
    if not isinstance(current_path, str) or not isinstance(transition_id, str):
        return None
    try:
        data = load_transition_ledger(root)
    except (OSError, UnicodeError, ValueError):
        return None
    transitions = data.get("transitions")
    if not isinstance(transitions, list):
        return None
    matches = [
        item
        for item in transitions
        if isinstance(item, dict)
        and item.get("id") == transition_id
        and item.get("original_path") == original_path
    ]
    if len(matches) != 1:
        return None
    initial_path = matches[0].get("current_path")
    if not isinstance(initial_path, str):
        return None
    resolved_path = initial_path
    visited = {original_path}
    while resolved_path != current_path:
        if resolved_path in visited:
            return None
        visited.add(resolved_path)
        relocation_targets = {
            str(item["current_path"])
            for item in transitions
            if isinstance(item, dict)
            and item.get("kind") == "carrier_relocation"
            and item.get("original_path") == resolved_path
            and isinstance(item.get("current_path"), str)
        }
        if len(relocation_targets) != 1:
            return None
        resolved_path = next(iter(relocation_targets))
    target = (root / current_path).resolve()
    return target if _within_root(root, target) and target.is_file() else None


def _transition_current_path(root: Path, original_path: str) -> str | None:
    """Return one registered relocation target for an original carrier path."""

    try:
        data = load_transition_ledger(root)
    except (OSError, UnicodeError, ValueError):
        return None
    matches = {
        str(item["current_path"])
        for item in data.get("transitions", [])
        if isinstance(item, dict)
        and item.get("kind") == "carrier_relocation"
        and item.get("original_path") == original_path
        and isinstance(item.get("current_path"), str)
    }
    return next(iter(matches)) if len(matches) == 1 else None


def _semantic_retention_carriers(
    root: Path,
    ledger: list[dict[str, Any]],
    semantic_id: str,
    snapshot: str,
    markdown_texts: dict[Path, str],
) -> set[Path]:
    carriers: set[Path] = set()
    snapshot_path = (root / snapshot).resolve()
    for record in ledger:
        if record.get("semantic_id") != semantic_id:
            continue
        fragments = record.get("fragments")
        if not isinstance(fragments, list):
            continue
        for fragment in fragments:
            raw = fragment.get("path") if isinstance(fragment, dict) else None
            if not isinstance(raw, str):
                continue
            carrier = (root / raw).resolve()
            links_snapshot = (
                carrier.is_file()
                and carrier.suffix == ".md"
                and _carrier_references_path(
                    root, carrier, snapshot_path, markdown_texts.get(carrier)
                )
            )
            if raw == snapshot or links_snapshot:
                carriers.add(carrier)
    for carrier, text in markdown_texts.items():
        if semantic_id not in text:
            continue
        if _carrier_references_path(root, carrier, snapshot_path, text):
            carriers.add(carrier.resolve())
    return carriers


def _carrier_references_path(
    root: Path, carrier: Path, target: Path, text: str | None = None
) -> bool:
    root = root.resolve()
    carrier = carrier.resolve()
    target = target.resolve()
    local_targets = _local_link_targets(carrier)
    if target in local_targets:
        return True
    if text is None:
        text = carrier.read_text(encoding="utf-8")
    for raw_target in LINK_PATTERN.findall(text):
        link = raw_target.strip().strip("<>").split("#", 1)[0]
        if link and (carrier.parent / unquote(link)).resolve() == target:
            return True
    relative = target.relative_to(root).as_posix()
    if relative in text:
        return True
    aliases, reverse = _transition_indexes(root)
    canonical_target = aliases.get(target, target)
    if any(
        aliases.get(candidate, candidate) == canonical_target
        for candidate in local_targets
    ):
        return True
    carrier_locations = {carrier, *reverse.get(carrier, frozenset())}
    for carrier_location in carrier_locations:
        for raw_target in LINK_PATTERN.findall(text):
            link = raw_target.strip().strip("<>").split("#", 1)[0]
            if (
                link
                and aliases.get(
                    (carrier_location.parent / unquote(link)).resolve(),
                    (carrier_location.parent / unquote(link)).resolve(),
                )
                == canonical_target
            ):
                return True
    return False


_TRANSITION_INDEX_CACHE: dict[
    tuple[str, int, int], tuple[dict[Path, Path], dict[Path, frozenset[Path]]]
] = {}


def _transition_indexes(
    root: Path,
) -> tuple[dict[Path, Path], dict[Path, frozenset[Path]]]:
    """Index relocation aliases once per ledger revision."""

    root = root.resolve()
    ledger = carrier_transition_ledger_path(root)
    try:
        stat = ledger.stat()
        revision = (str(root), stat.st_mtime_ns, stat.st_size)
    except OSError:
        revision = (str(root), -1, -1)
    cached = _TRANSITION_INDEX_CACHE.get(revision)
    if cached is not None:
        return cached
    aliases = transition_aliases(root)
    reverse_mutable: dict[Path, set[Path]] = {}
    for original, current in aliases.items():
        reverse_mutable.setdefault(current, set()).add(original)
    reverse = {
        current: frozenset(originals) for current, originals in reverse_mutable.items()
    }
    cached = (aliases, reverse)
    _TRANSITION_INDEX_CACHE.clear()
    _TRANSITION_INDEX_CACHE[revision] = cached
    return cached


def _validate_legacy_structured_links(
    root: Path,
    registry_path: Path,
    entries: dict[str, dict[str, Any]],
    legacy_evidence: frozenset[str],
    markdown_texts: dict[Path, str],
) -> list[Diagnostic]:
    """Keep mutable references current and immutable references explicitly bound."""

    diagnostics: list[Diagnostic] = []
    registered = {(root / relative).resolve(): relative for relative in entries}
    ledger = _legacy_authority_records(root)
    immutable: set[Path] = {(root / relative).resolve() for relative in legacy_evidence}
    for path in markdown_texts:
        relative = path.relative_to(root).as_posix()
        if "/proofs/" in f"/{relative}":
            immutable.add(path.resolve())
    for record in ledger:
        fragments = record.get("fragments")
        if not isinstance(fragments, list):
            continue
        for fragment in fragments:
            if (
                not isinstance(fragment, dict)
                or fragment.get("selector") != "whole-carrier"
            ):
                continue
            raw = fragment.get("path")
            if isinstance(raw, str):
                immutable.add((root / raw).resolve())
    atoms = discover_layout(root).structured_file(
        discover_layout(root).project_state_root, "atoms.toml"
    )
    if atoms.is_file():
        try:
            atom_data = load(atoms)
        except (OSError, ValueError, YamlSubsetError):
            atom_data = {}
        records = atom_data.get("records") if isinstance(atom_data, dict) else None
        if isinstance(records, list):
            for record in records:
                raw = record.get("path") if isinstance(record, dict) else None
                if isinstance(raw, str):
                    immutable.add((root / raw).resolve())

    allowed: dict[Path, set[Path]] = {path: set() for path in registered}
    for relative, entry in entries.items():
        snapshot = (root / relative).resolve()
        identities = entry.get("retained_for")
        if not isinstance(identities, list):
            continue
        for identity in identities:
            if not isinstance(identity, dict):
                continue
            raw_path = identity.get("carrier_path")
            if isinstance(raw_path, str):
                allowed[snapshot].add((root / raw_path).resolve())
            semantic_id = identity.get("semantic_id")
            if isinstance(semantic_id, str):
                allowed[snapshot].update(
                    _semantic_retention_carriers(
                        root, ledger, semantic_id, relative, markdown_texts
                    )
                )

    for carrier, _text in markdown_texts.items():
        targets = _local_link_targets(carrier)
        is_immutable = carrier.resolve() in immutable
        for target in targets:
            registered_relative = registered.get(target)
            if registered_relative is not None:
                if not is_immutable:
                    diagnostics.append(
                        _diag(
                            "DSET-E156",
                            carrier,
                            "mutable carrier links registered legacy snapshot: "
                            f"{registered_relative}",
                        )
                    )
                elif carrier.resolve() not in allowed[target]:
                    diagnostics.append(
                        _diag(
                            "DSET-E156",
                            carrier,
                            "immutable legacy link is not declared by retained_for: "
                            f"{registered_relative}",
                        )
                    )
                continue
            if (
                is_immutable
                and target.suffix.lower() in {".yaml", ".yml"}
                and (
                    _within_root(root / ".dset", target)
                    or _within_root(root / "dset", target)
                )
            ):
                diagnostics.append(
                    _diag(
                        "DSET-E156",
                        carrier,
                        "immutable carrier links an unregistered legacy "
                        f"structured path: {target.relative_to(root).as_posix()}",
                    )
                )
    return diagnostics


def _retention_markdown_texts(root: Path) -> dict[Path, str]:
    """Read each project-visible Markdown carrier once per registry check."""

    texts: dict[Path, str] = {}
    for path in _markdown_paths(root):
        try:
            texts[path.resolve()] = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
    return texts


def _validate_artifact_path_rules(
    root: Path,
    registry_path: Path,
    data: dict[str, Any],
    catalog: dict[str, frozenset[str]],
    exclusions: list[tuple[str, str]],
    legacy_evidence: frozenset[str],
    legacy_structured: dict[str, dict[str, Any]],
    *,
    project_key: str | None,
    include_subtype_in_names: bool,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    raw_rules = data.get("path_rules")
    if not isinstance(raw_rules, list) or not raw_rules:
        return [
            _diag("DSET-E156", registry_path, "path_rules must be a non-empty list")
        ]
    rules: list[tuple[str, str, str | None]] = []
    seen_patterns: set[str] = set()
    for rule in raw_rules:
        if not isinstance(rule, dict):
            diagnostics.append(
                _diag("DSET-E156", registry_path, "every path rule must be a mapping")
            )
            continue
        pattern = rule.get("pattern")
        artifact_type = rule.get("artifact_type")
        artifact_subtype = rule.get("artifact_subtype")
        if not isinstance(pattern, str) or not pattern.strip():
            diagnostics.append(
                _diag("DSET-E156", registry_path, "path rule pattern is missing")
            )
            continue
        if pattern in seen_patterns:
            diagnostics.append(
                _diag("DSET-E156", registry_path, f"duplicate path rule: {pattern}")
            )
        seen_patterns.add(pattern)
        if not isinstance(artifact_type, str) or artifact_type not in catalog:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    registry_path,
                    f"path rule uses unknown artifact type: {artifact_type}",
                )
            )
            continue
        if artifact_subtype is not None:
            if not isinstance(artifact_subtype, str):
                diagnostics.append(
                    _diag(
                        "DSET-E156",
                        registry_path,
                        f"path rule {pattern} has a nested or invalid subtype",
                    )
                )
                continue
            if artifact_subtype not in catalog[artifact_type]:
                diagnostics.append(
                    _diag(
                        "DSET-E156",
                        registry_path,
                        f"path rule {pattern} has a subtype/type mismatch",
                    )
                )
                continue
        rules.append((pattern, artifact_type, artifact_subtype))
    diagnostics.extend(
        _validate_current_artifact_classifications(
            root,
            registry_path,
            rules,
            catalog,
            exclusions,
            legacy_evidence,
            legacy_structured,
            project_key=project_key,
            include_subtype_in_names=include_subtype_in_names,
        )
    )
    return diagnostics


def _validate_current_artifact_classifications(
    root: Path,
    registry_path: Path,
    rules: list[tuple[str, str, str | None]],
    catalog: dict[str, frozenset[str]],
    exclusions: list[tuple[str, str]],
    legacy_evidence: frozenset[str],
    legacy_structured: dict[str, dict[str, Any]],
    *,
    project_key: str | None,
    include_subtype_in_names: bool,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for path in _project_visible_files(root):
        relative = path.relative_to(root).as_posix()
        matched_rules = [
            rule for rule in rules if _path_rule_matches(relative, rule[0])
        ]
        matched_exclusions = [
            pattern
            for pattern, _rationale in exclusions
            if _path_rule_matches(relative, pattern)
        ]
        matches = [rule[0] for rule in matched_rules]
        if len(matches) > 1:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    path,
                    "artifact path matches multiple rules: " + ", ".join(matches),
                )
            )
        direct = _direct_artifact_classification(path)
        is_legacy_evidence = relative in legacy_evidence
        historical = legacy_structured.get(relative)
        transitioned = [
            entry
            for entry in legacy_structured.values()
            if entry.get("current_path") == relative
        ]
        if len(matched_exclusions) > 1:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    path,
                    "artifact path matches multiple exclusions: "
                    + ", ".join(matched_exclusions),
                )
            )
        if matched_exclusions and (
            direct is not None or matched_rules or is_legacy_evidence or historical
        ):
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    path,
                    "governed carrier cannot be both classified and excluded",
                )
            )
        if (
            direct is None
            and not matched_rules
            and not is_legacy_evidence
            and historical is None
            and not transitioned
            and not matched_exclusions
        ):
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    path,
                    "governed carrier has no artifact classification or exclusion",
                )
            )
            continue
        if is_legacy_evidence and direct is not None and direct[0] != "evidence_record":
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    path,
                    "legacy evidence path has a conflicting direct classification",
                )
            )
        if historical is not None and len(matched_rules) == 1:
            _, rule_type, rule_subtype = matched_rules[0]
            historical_classification = (
                historical.get("artifact_type"),
                historical.get("artifact_subtype"),
            )
            if historical_classification[0] != rule_type or (
                rule_subtype is not None
                and historical_classification[1] != rule_subtype
            ):
                diagnostics.append(
                    _diag(
                        "DSET-E156",
                        path,
                        "legacy_structured classification conflicts with its path rule",
                    )
                )
        owner_entries = [
            entry
            for entry in legacy_structured.values()
            if entry.get("current_owner") == relative
        ]
        if owner_entries and len(matched_rules) == 1:
            _, rule_type, rule_subtype = matched_rules[0]
            owner = owner_entries[0]
            owner_classification = (
                owner.get("artifact_type"),
                owner.get("artifact_subtype"),
            )
            if owner_classification[0] != rule_type or (
                rule_subtype is not None and owner_classification[1] != rule_subtype
            ):
                diagnostics.append(
                    _diag(
                        "DSET-E156",
                        path,
                        "current_owner classification conflicts with its path rule",
                    )
                )
        if direct is None:
            continue
        artifact_type, artifact_subtype, artifact_id = direct
        if artifact_type not in catalog:
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    path,
                    f"direct metadata uses unknown artifact type: {artifact_type}",
                )
            )
            continue
        if (
            artifact_subtype is not None
            and artifact_subtype not in catalog[artifact_type]
        ):
            diagnostics.append(
                _diag(
                    "DSET-E156",
                    path,
                    "direct metadata has a subtype/type mismatch",
                )
            )
        if len(matched_rules) == 1:
            _, rule_type, rule_subtype = matched_rules[0]
            if artifact_type != rule_type or (
                rule_subtype is not None and artifact_subtype != rule_subtype
            ):
                diagnostics.append(
                    _diag(
                        "DSET-E156",
                        path,
                        "direct metadata conflicts with its path rule",
                    )
                )
        if (
            project_key is not None
            and artifact_id is not None
            and "templates" not in path.relative_to(root).parts
        ):
            diagnostics.extend(
                _validate_artifact_name(
                    path,
                    artifact_id,
                    project_key,
                    artifact_type,
                    artifact_subtype,
                    include_subtype_in_names=include_subtype_in_names,
                )
            )
    return diagnostics


def _direct_artifact_classification(
    path: Path,
) -> tuple[str, str | None, str | None] | None:
    if path.suffix.lower() != ".md":
        return None
    try:
        metadata = frontmatter_metadata(path)
    except (OSError, UnicodeError, FrontmatterError):
        return None
    if not isinstance(metadata, dict):
        return None
    artifact_type = metadata.get("artifact_type")
    artifact_subtype = metadata.get("artifact_subtype")
    artifact_id = metadata.get("artifact_id")
    semantic_id = metadata.get("semantic_id")
    if artifact_type is None and artifact_subtype is None:
        return None
    return (
        str(artifact_type),
        str(artifact_subtype) if artifact_subtype is not None else None,
        (
            str(semantic_id)
            if artifact_type == "atomic_record" and isinstance(semantic_id, str)
            else str(artifact_id)
            if artifact_id is not None
            else None
        ),
    )


def _validate_artifact_name(
    path: Path,
    artifact_id: str,
    project_key: str,
    artifact_type: str,
    artifact_subtype: str | None,
    *,
    include_subtype_in_names: bool,
) -> list[Diagnostic]:
    type_token = artifact_type.replace("_", "-").upper()
    if artifact_type == "atomic_record":
        semantic = re.match(
            rf"^{re.escape(project_key)}-([A-Z][A-Z0-9-]*?)-(?:[A-Z]+-)?\d+$",
            artifact_id,
        )
        if semantic is not None:
            type_token = semantic.group(1).split("-")[0]
    tokens = [project_key, type_token]
    if include_subtype_in_names and artifact_subtype is not None:
        tokens.append(artifact_subtype.replace("_", "-").upper())
    prefix = "-".join(tokens) + "-"
    layered_prefix = re.compile(
        rf"^{re.escape(prefix)}(?:(?:{'|'.join(TRACE_LAYERS)})-)?"
        rf"(?P<number>\d+)$"
    )
    if layered_prefix.fullmatch(artifact_id) is not None and path.stem.startswith(
        f"{artifact_id}-"
    ):
        return []
    return [
        _diag(
            "DSET-E157",
            path,
            f"artifact ID and filename must use the configured naming prefix: {prefix}",
        )
    ]


def _path_rule_matches(relative_path: str, pattern: str) -> bool:
    if "/" not in pattern:
        return PurePosixPath(relative_path).match(pattern)
    path = PurePosixPath(relative_path)
    return path.match(pattern) or (
        pattern.startswith("**/") and path.match(pattern.removeprefix("**/"))
    )


def validate_artifact_registry(
    root: Path, registry_path: Path, data: dict[str, Any]
) -> list[Diagnostic]:
    """Validate the documentation-v1 authority and hub graph."""
    root = root.resolve()
    diagnostics: list[Diagnostic] = []
    root_entry = data.get("root")
    raw_areas = data.get("areas")
    if not isinstance(root_entry, dict):
        return [_diag("DSET-E121", registry_path, "root must be a mapping")]
    if not isinstance(raw_areas, list) or not raw_areas:
        return [_diag("DSET-E121", registry_path, "areas must be a non-empty list")]
    areas = [item for item in raw_areas if isinstance(item, dict)]
    if len(areas) != len(raw_areas):
        diagnostics.append(
            _diag("DSET-E121", registry_path, "every area must be a mapping")
        )
    entries = [root_entry, *areas]
    diagnostics.extend(_validate_artifact_entries(root, registry_path, entries))
    diagnostics.extend(_validate_artifact_parents(registry_path, root_entry, areas))
    diagnostics.extend(_validate_artifact_hubs(root, registry_path, root_entry, areas))
    return diagnostics


def _validate_artifact_entries(
    root: Path, registry_path: Path, entries: list[dict[str, Any]]
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    seen_ids: set[str] = set()
    seen_roots: set[Path] = set()
    seen_hubs: set[Path] = set()
    for entry in entries:
        for field in ("id", "hub", "owner", "purpose"):
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                diagnostics.append(
                    _diag(
                        "DSET-E121",
                        registry_path,
                        f"artifact {field} must be a non-empty string",
                    )
                )
        identifier = entry.get("id")
        if not isinstance(identifier, str) or not CHANGE_PATTERN.fullmatch(identifier):
            diagnostics.append(
                _diag("DSET-E121", registry_path, f"invalid artifact ID: {identifier}")
            )
        elif identifier in seen_ids:
            diagnostics.append(
                _diag(
                    "DSET-E121", registry_path, f"duplicate artifact ID: {identifier}"
                )
            )
        else:
            seen_ids.add(identifier)
        hub = _artifact_carrier(root, entry.get("hub"))
        area_root = hub.parent if hub is not None else None
        if area_root is None:
            diagnostics.append(
                _diag(
                    "DSET-E121",
                    registry_path,
                    f"artifact hub is missing or ambiguous: {entry.get('hub')}",
                )
            )
        elif area_root in seen_roots:
            diagnostics.append(
                _diag(
                    "DSET-E121",
                    registry_path,
                    f"duplicate artifact area: {entry.get('hub')}",
                )
            )
        else:
            seen_roots.add(area_root)
            if not area_root.is_dir():
                diagnostics.append(
                    _diag("DSET-E121", area_root, "artifact root does not exist")
                )
        if hub is None:
            diagnostics.append(
                _diag(
                    "DSET-E121",
                    registry_path,
                    f"invalid artifact hub: {entry.get('hub')}",
                )
            )
        elif hub in seen_hubs:
            diagnostics.append(
                _diag(
                    "DSET-E121",
                    registry_path,
                    f"duplicate artifact hub: {entry.get('hub')}",
                )
            )
        else:
            seen_hubs.add(hub)
            if not hub.is_file():
                diagnostics.append(_diag("DSET-E121", hub, "artifact hub is missing"))
        if area_root is not None and hub is not None:
            try:
                hub.relative_to(area_root)
            except ValueError:
                diagnostics.append(
                    _diag(
                        "DSET-E121", registry_path, "artifact hub is outside its root"
                    )
                )
    return diagnostics


def _validate_artifact_parents(
    registry_path: Path,
    root_entry: dict[str, Any],
    areas: list[dict[str, Any]],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    root_id = root_entry.get("id")
    if not isinstance(root_id, str):
        return diagnostics
    by_id = {
        item["id"]: item
        for item in [root_entry, *areas]
        if isinstance(item.get("id"), str)
    }
    for area in areas:
        identifier = area.get("id")
        parent = area.get("parent")
        if not isinstance(identifier, str):
            continue
        if not isinstance(parent, str) or parent not in by_id:
            diagnostics.append(
                _diag(
                    "DSET-E122",
                    registry_path,
                    f"artifact {identifier} has an unresolved parent: {parent}",
                )
            )
            continue
        current = identifier
        visited: set[str] = set()
        while current != root_id:
            if current in visited:
                diagnostics.append(
                    _diag(
                        "DSET-E122",
                        registry_path,
                        f"artifact parent cycle includes: {identifier}",
                    )
                )
                break
            visited.add(current)
            node = by_id.get(current)
            next_parent = node.get("parent") if node is not None else None
            if not isinstance(next_parent, str) or next_parent not in by_id:
                diagnostics.append(
                    _diag(
                        "DSET-E122",
                        registry_path,
                        f"artifact parent chain does not reach root: {identifier}",
                    )
                )
                break
            current = next_parent
    return diagnostics


def _validate_artifact_hubs(
    root: Path,
    registry_path: Path,
    root_entry: dict[str, Any],
    areas: list[dict[str, Any]],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    root_id = root_entry.get("id")
    atoms, _ = collect_semantic_atoms(root)
    atomic_names = {(atom.semantic_id, Path(atom.path).name) for atom in atoms.values()}
    for entry in [root_entry, *areas]:
        hub = _artifact_carrier(root, entry.get("hub"))
        if hub is None or not hub.is_file():
            continue
        hub_text = hub.read_text(encoding="utf-8")
        headings = _level_two_headings(hub_text)
        required = {"purpose", "boundaries"}
        if not required.issubset(headings):
            diagnostics.append(
                _diag("DSET-E123", hub, "hub requires Purpose and Boundaries sections")
            )
        navigation = {"start here", "navigation"}
        if entry is root_entry:
            navigation.add("repository areas")
        if headings.isdisjoint(navigation):
            diagnostics.append(
                _diag("DSET-E123", hub, "hub requires a navigation section")
            )
        named_atoms = sorted(
            semantic_id
            for semantic_id, carrier_name in atomic_names
            if semantic_id in hub_text or carrier_name in hub_text
        )
        if named_atoms:
            diagnostics.append(
                _diag(
                    "DSET-E123",
                    hub,
                    "hub must link atomic-artifact folders, not individual "
                    f"atoms: {', '.join(named_atoms)}",
                )
            )
        runtime_descendants = sorted(
            set(
                re.findall(
                    r"\.dset_runtime/[^\s`\)\]\}>]+",
                    hub_text,
                )
            )
        )
        if runtime_descendants:
            diagnostics.append(
                _diag(
                    "DSET-E123",
                    hub,
                    "hub must not include .dset_runtime descendants: "
                    + ", ".join(runtime_descendants),
                )
            )
    root_hub = _artifact_carrier(root, root_entry.get("hub"))
    if root_hub is None or not root_hub.is_file() or not isinstance(root_id, str):
        return diagnostics
    root_text = root_hub.read_text(encoding="utf-8")
    for area in areas:
        if area.get("parent") != root_id:
            continue
        hub_name = area.get("hub")
        if isinstance(hub_name, str) and hub_name not in root_text:
            diagnostics.append(
                _diag(
                    "DSET-E123",
                    root_hub,
                    f"root hub does not link top-level area: {area.get('id')}",
                )
            )
    return diagnostics


def _artifact_path(root: Path, raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw or Path(raw).is_absolute():
        return None
    path = (root / unquote(raw)).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return None
    return path


def _artifact_carrier(root: Path, raw: Any) -> Path | None:
    if not isinstance(raw, str):
        return None
    try:
        return find_unique_name(root, raw)
    except (FileNotFoundError, ValueError):
        return None


def _level_two_headings(text: str) -> set[str]:
    rendered = _without_code(text)
    return {
        match.strip().lower()
        for match in re.findall(r"^##\s+(.+?)\s*$", rendered, flags=re.MULTILINE)
    }


def _local_link_targets(path: Path) -> set[Path]:
    text = _without_code(path.read_text(encoding="utf-8"))
    targets: set[Path] = set()
    for raw_target in LINK_PATTERN.findall(text):
        target = raw_target.strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        target = target.split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if "{{" in target:
            continue
        targets.add((path.parent / unquote(target)).resolve())
    return targets


def _validate_change_ids(
    root: Path, change_dir: Path, data: dict[str, Any]
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    manifest_path = discover_layout(root).structured_file(change_dir, "change.toml")
    layout = discover_layout(root)
    if layout.slim:
        return _validate_slim_change_ids(root, manifest_path, data, layout)
    legacy = _is_legacy_change(data)
    manifest = _safe_load(discover_layout(root).manifest_path, diagnostics) or {}
    project_key = _manifest_project_key(manifest)
    if project_key is None:
        diagnostics.append(
            _diag("DSET-E106", manifest_path, "project.key is unavailable")
        )
        return diagnostics
    atomic_records = list(change_dir.glob("*-ATOMIC-RECORD-*.md"))
    groups: dict[str, list[Path]] = {
        "requirements": [
            *list((change_dir / "specs").glob("*.md")),
            *atomic_records,
        ],
        "tests": [change_dir / "test-plan.md", *atomic_records],
        "evals": [change_dir / "eval-plan.md", *atomic_records],
    }
    group_types = {
        "requirements": "REQUIREMENT",
        "tests": "TEST",
        "evals": "EVAL",
    }
    if legacy:
        if "adrs" not in data or "decisions" in data:
            diagnostics.append(
                _diag(
                    "DSET-E106",
                    manifest_path,
                    "schema 1.0 requires adrs and forbids decisions",
                )
            )
        groups["adrs"] = list(change_dir.glob("*adr*.md"))
    else:
        if "decisions" not in data or "adrs" in data:
            diagnostics.append(
                _diag(
                    "DSET-E106",
                    manifest_path,
                    "schema 1.1 requires decisions and forbids adrs",
                )
            )
        groups["decisions"] = [
            *change_dir.glob("*decision*.md"),
            *change_dir.glob("*adr*.md"),
            *atomic_records,
        ]
        group_types["decisions"] = "DECISION"
        if "contracts" not in data:
            diagnostics.append(
                _diag("DSET-E106", manifest_path, "schema 1.1 requires contracts")
            )
        groups["contracts"] = [
            *list((change_dir / "specs").glob("*.md")),
            change_dir / "design.md",
            change_dir / "solution-landscape.md",
        ]
        group_types["contracts"] = "CONTRACT"
        for group, trace_type, artifact in (
            ("stories", "STORY", "stories.md"),
            ("outcomes", "OUTCOME", "outcomes.md"),
        ):
            if group not in data:
                continue
            groups[group] = [
                change_dir / artifact,
                *list((change_dir / "specs").glob("*.md")),
            ]
            group_types[group] = trace_type
    for group, paths in groups.items():
        ids = data.get(group, [])
        if not isinstance(ids, list):
            diagnostics.append(
                _diag("DSET-E106", manifest_path, f"{group} must be a list")
            )
            continue
        pattern = (
            ID_PATTERN
            if legacy
            else _trace_id_pattern(
                project_key,
                (
                    ("EVAL", "EVALUATION")
                    if group_types[group] == "EVAL"
                    else (group_types[group],)
                ),
            )
        )
        content = "\n".join(
            path.read_text(encoding="utf-8") for path in paths if path.is_file()
        )
        for identifier in ids:
            if not isinstance(identifier, str) or pattern.fullmatch(identifier) is None:
                diagnostics.append(
                    _diag(
                        "DSET-E106",
                        manifest_path,
                        f"invalid ID: {identifier}",
                    )
                )
            elif identifier not in content:
                diagnostics.append(
                    _diag(
                        "DSET-E106",
                        manifest_path,
                        f"{identifier} is not present in its owning artifact",
                    )
                )
            elif group in {"stories", "outcomes"}:
                missing = _missing_semantic_fields(
                    paths, identifier, group_types[group]
                )
                if missing:
                    diagnostics.append(
                        _diag(
                            "DSET-E106",
                            manifest_path,
                            f"{identifier} is missing fields: {', '.join(missing)}",
                        )
                    )
        if group == "evals" and not ids:
            eval_plan = change_dir / "eval-plan.md"
            if (
                eval_plan.is_file()
                and "not applicable"
                not in eval_plan.read_text(encoding="utf-8").lower()
            ):
                diagnostics.append(
                    _diag(
                        "DSET-E106",
                        eval_plan,
                        "empty eval IDs require an explicit not-applicable reason",
                    )
                )
    if not data.get("requirements") or not data.get("tests"):
        diagnostics.append(
            _diag(
                "DSET-E106",
                manifest_path,
                "requirements and tests cannot be empty",
            )
        )
    intake_ids = data.get("intake", [])
    if not isinstance(intake_ids, list):
        diagnostics.append(_diag("DSET-E106", manifest_path, "intake must be a list"))
    else:
        registry_path = discover_layout(root).intake_path
        if not intake_ids and not registry_path.is_file():
            return diagnostics
        registry = _safe_load(registry_path, diagnostics) or {}
        registered = {
            item.get("id")
            for item in registry.get("items", [])
            if isinstance(item, dict)
        }
        for identifier in intake_ids:
            if identifier not in registered:
                diagnostics.append(
                    _diag(
                        "DSET-E106",
                        manifest_path,
                        f"unregistered intake ID: {identifier}",
                    )
                )
    return diagnostics


def _validate_slim_change_ids(
    root: Path,
    manifest_path: Path,
    data: dict[str, Any],
    layout: RepositoryLayout,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    project = _safe_load(layout.manifest_path, diagnostics) or {}
    project_key = _manifest_project_key(project)
    if project_key is None:
        return [_diag("DSET-E106", manifest_path, "project.key is unavailable")]
    atoms, _ = collect_semantic_atoms(root)
    known = set(atoms) | legacy_authority_ids(root) | _defined_semantic_ids(root)
    for package in layout.package_fragments():
        payload = _safe_load(package, diagnostics) or {}
        for group in (
            "requirements",
            "tests",
            "evals",
            "contracts",
            "stories",
            "outcomes",
        ):
            values = payload.get(group)
            if isinstance(values, list):
                known.update(item for item in values if isinstance(item, str))
    groups = {
        "requirements": ("REQUIREMENT",),
        "tests": ("TEST",),
        "evals": ("EVAL", "EVALUATION"),
        "decisions": ("DECISION",),
        "contracts": ("CONTRACT",),
        "stories": ("STORY",),
        "outcomes": ("OUTCOME",),
    }
    for group, kinds in groups.items():
        values = data.get(group)
        if not isinstance(values, list):
            diagnostics.append(
                _diag("DSET-E106", manifest_path, f"{group} must be a list")
            )
            continue
        pattern = _trace_id_pattern(project_key, kinds)
        for identifier in values:
            if not isinstance(identifier, str) or pattern.fullmatch(identifier) is None:
                diagnostics.append(
                    _diag("DSET-E106", manifest_path, f"invalid ID: {identifier}")
                )
            elif identifier not in known:
                diagnostics.append(
                    _diag(
                        "DSET-E106", manifest_path, f"unknown governed ID: {identifier}"
                    )
                )
    if not data.get("requirements") or not data.get("tests"):
        diagnostics.append(
            _diag("DSET-E106", manifest_path, "requirements and tests cannot be empty")
        )
    intake = data.get("intake")
    if not isinstance(intake, list):
        diagnostics.append(_diag("DSET-E106", manifest_path, "intake must be a list"))
    else:
        registry = _safe_load(layout.intake_path, diagnostics) or {}
        registered = {
            item.get("id")
            for item in registry.get("items", [])
            if isinstance(item, dict)
        }
        for identifier in intake:
            if identifier not in registered:
                diagnostics.append(
                    _diag(
                        "DSET-E106",
                        manifest_path,
                        f"unregistered intake ID: {identifier}",
                    )
                )
    return diagnostics


def _defined_semantic_ids(root: Path) -> set[str]:
    """Collect IDs from definition headings and first-column plan rows."""

    identifiers: set[str] = set()
    id_pattern = re.compile(
        r"[A-Z][A-Z0-9]*-(?:" + "|".join(TRACE_TYPES) + r")"
        r"(?:-(?:" + "|".join(TRACE_LAYERS) + r"))?-\d{3,}"
    )
    for path in _markdown_paths(root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith("#") or re.match(
                r"^\|\s*(?:`|\*\*)?[A-Z][A-Z0-9]*-", stripped
            ):
                identifiers.update(id_pattern.findall(line))
    return identifiers


def _validate_layered_change(
    layout: RepositoryLayout, change_dir: Path, data: dict[str, Any]
) -> list[Diagnostic]:
    path = layout.structured_file(change_dir, "change.toml")
    diagnostics: list[Diagnostic] = []
    project = _safe_load(layout.manifest_path, diagnostics) or {}
    diagnostics.extend(_validate_change_target(path, data.get("target"), project))
    primary = data.get("primary_layer")
    affected = data.get("affected_layers")
    try:
        physical = layout.change_layer(change_dir)
    except ValueError:
        physical = None
    layer_names = set(LAYERS)
    if (
        data.get("schema_version") != "1.2"
        or not isinstance(primary, str)
        or primary not in layer_names
        or not isinstance(affected, list)
        or not affected
        or any(
            not isinstance(layer, str) or layer not in layer_names for layer in affected
        )
        or len(affected) != len(set(affected))
        or primary not in affected
        or physical != primary
    ):
        diagnostics.append(
            _diag(
                "DSET-E148",
                path,
                "change ownership must match primary and affected layers",
            )
        )
        return diagnostics
    for group in ("contracts", "stories", "outcomes"):
        if not isinstance(data.get(group), list):
            diagnostics.append(
                _diag("DSET-E148", path, f"schema 1.2 requires {group} as a list")
            )
    project_key = _manifest_project_key(project)
    if project_key is None:
        return diagnostics
    change_id = data.get("id")
    change_match = (
        _trace_id_pattern(project_key, ("CHANGE",)).fullmatch(change_id)
        if isinstance(change_id, str)
        else None
    )
    if (
        change_match is None
        or change_match.group("layer") is None
        or ID_TOKEN_LAYERS.get(str(change_match.group("layer"))) != primary
    ):
        diagnostics.append(
            _diag(
                "DSET-E151",
                path,
                "Change ID must be project-CHANGE-layer-sequence and match owner",
            )
        )
    diagnostics.extend(_validate_workspace(path, data, archived=False))
    diagnostics.extend(_validate_change_dependencies(path, data, project_key))
    release = data.get("release")
    if isinstance(release, dict):
        policy = release.get("policy")
        owner = release.get("owner_change")
        expected_policy = (
            ".dset/000_dset_methodology/06_ops/procedure-release.md"
            if layout.slim
            else "dset/scopes/ops/governance/release.md"
        )
        if policy is not None and policy != expected_policy:
            diagnostics.append(
                _diag("DSET-E153", path, "schema 1.2 release policy path is invalid")
            )
        if owner is not None:
            owner_match = (
                _trace_id_pattern(project_key, ("CHANGE",)).fullmatch(owner)
                if isinstance(owner, str)
                else None
            )
            if owner_match is None or owner_match.group("layer") is None:
                diagnostics.append(
                    _diag("DSET-E153", path, "release owner_change must be stable")
                )
    pattern = _trace_id_pattern(project_key, TRACE_TYPES)
    for group in (
        "requirements",
        "tests",
        "evals",
        "intake",
        "decisions",
        "contracts",
        "stories",
        "outcomes",
    ):
        identifiers = data.get(group, [])
        if not isinstance(identifiers, list):
            continue
        for identifier in identifiers:
            match = (
                pattern.fullmatch(identifier) if isinstance(identifier, str) else None
            )
            if match is None:
                continue
            id_layer = match.group("layer")
            owner = id_layer.lower() if id_layer is not None else "meta"
            if owner not in affected:
                diagnostics.append(
                    _diag(
                        "DSET-E148",
                        path,
                        f"{identifier} is outside affected_layers",
                    )
                )
    return diagnostics


def _validate_change_target(
    path: Path, raw_target: object, project: dict[str, Any]
) -> list[Diagnostic]:
    raw_declared = project.get("work_areas", [])
    declared = {
        item.get("id")
        for item in (raw_declared if isinstance(raw_declared, list) else [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    valid = isinstance(raw_target, dict) and set(raw_target) == {
        "repository",
        "work_areas",
    }
    repository = raw_target.get("repository") if isinstance(raw_target, dict) else None
    work_areas = raw_target.get("work_areas") if isinstance(raw_target, dict) else None
    valid = (
        valid
        and isinstance(repository, bool)
        and isinstance(work_areas, list)
        and len(work_areas)
        == len({item for item in work_areas if isinstance(item, str)})
        and all(
            isinstance(item, str)
            and CHANGE_PATTERN.fullmatch(item) is not None
            and item in declared
            for item in work_areas
        )
        and ((repository and not work_areas) or (not repository and bool(work_areas)))
    )
    if valid:
        return []
    return [
        _diag(
            "DSET-E148",
            path,
            "change target must select the repository or one or more declared "
            "work-area IDs",
        )
    ]


def _validate_change_uniqueness(layout: RepositoryLayout) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not layout.layered:
        return diagnostics
    owners: dict[str, Path] = {}
    branches: dict[str, Path] = {}
    pull_requests: dict[tuple[str, int], Path] = {}
    roots = (*layout.active_change_roots, *layout.archive_change_roots)
    for root in roots:
        if not root.is_dir():
            continue
        archived_root = root in layout.archive_change_roots
        for change in sorted(root.iterdir()):
            manifest = layout.structured_file(change, "change.toml")
            if not change.is_dir() or not manifest.is_file():
                continue
            try:
                data = load(manifest)
            except (OSError, ValueError, YamlSubsetError):
                continue
            identifier = data.get("id") if isinstance(data, dict) else None
            if not isinstance(identifier, str):
                continue
            previous = owners.get(identifier)
            if previous is not None:
                diagnostics.append(
                    _diag(
                        "DSET-E149",
                        manifest,
                        f"change ID is also owned by {previous}",
                    )
                )
            else:
                owners[identifier] = manifest
            workspace = data.get("workspace") if isinstance(data, dict) else None
            isolation = (
                workspace.get("isolation") if isinstance(workspace, dict) else None
            )
            branch = workspace.get("branch") if isinstance(workspace, dict) else None
            if (
                not archived_root
                and isolation == "branch-worktree"
                and isinstance(branch, str)
                and branch != "pending"
            ):
                previous = branches.get(branch)
                if previous is not None:
                    diagnostics.append(
                        _diag(
                            "DSET-E154",
                            manifest,
                            f"workspace branch is also owned by {previous}",
                        )
                    )
                else:
                    branches[branch] = manifest
            pr = data.get("pull_request") if isinstance(data, dict) else None
            repository = pr.get("repository") if isinstance(pr, dict) else None
            number = pr.get("number") if isinstance(pr, dict) else None
            if (
                isolation == "branch-worktree"
                and isinstance(repository, str)
                and isinstance(number, int)
            ):
                pr_key = (repository, number)
                previous = pull_requests.get(pr_key)
                if previous is not None:
                    diagnostics.append(
                        _diag(
                            "DSET-E154",
                            manifest,
                            f"pull request is also owned by {previous}",
                        )
                    )
                else:
                    pull_requests[pr_key] = manifest
    return diagnostics


def _validate_workspace(
    path: Path, data: dict[str, Any], *, archived: bool
) -> list[Diagnostic]:
    workspace = data.get("workspace")
    if not isinstance(workspace, dict):
        return [_diag("DSET-E152", path, "workspace metadata is required")]
    required = {"isolation", "branch", "base_ref", "base_commit", "head_commit"}
    valid = (
        set(workspace) == required
        and workspace.get("isolation") in {"integration-branch", "branch-worktree"}
        and isinstance(workspace.get("branch"), str)
        and bool(str(workspace.get("branch")).strip())
        and isinstance(workspace.get("base_ref"), str)
        and bool(str(workspace.get("base_ref")).strip())
        and all(
            _is_exact_commit(workspace.get(field))
            or (not archived and workspace.get(field) == "pending")
            for field in ("base_commit", "head_commit")
        )
    )
    if not valid:
        return [_diag("DSET-E152", path, "workspace metadata is inconsistent")]
    release = data.get("release")
    candidate = release.get("candidate_commit") if isinstance(release, dict) else None
    head = workspace.get("head_commit")
    if (
        data.get("status") in {"verified", "archive-ready", "archived"}
        and _is_exact_commit(candidate)
        and candidate != head
    ):
        return [
            _diag(
                "DSET-E152",
                path,
                "workspace head_commit must match the release candidate commit",
            )
        ]
    return []


def _validate_change_dependencies(
    path: Path, data: dict[str, Any], project_key: str
) -> list[Diagnostic]:
    dependencies = data.get("dependencies")
    if not isinstance(dependencies, list):
        return [_diag("DSET-E153", path, "dependencies must be a list")]
    diagnostics: list[Diagnostic] = []
    seen: set[str] = set()
    change_pattern = _trace_id_pattern(project_key, ("CHANGE",))
    trace_pattern = _trace_id_pattern(project_key, TRACE_TYPES)
    own_id = data.get("id")
    required = {
        "change_id",
        "pull_request",
        "required_commit",
        "consumes",
        "claim",
        "use",
        "evidence",
        "checked_at",
        "reopen_when",
        "status",
    }
    statuses = {"planned", "available", "integrated", "blocked", "stale"}
    for dependency in dependencies:
        if not isinstance(dependency, dict) or set(dependency) != required:
            diagnostics.append(
                _diag("DSET-E153", path, "dependency record shape is inconsistent")
            )
            continue
        dependency_id = dependency.get("change_id")
        identifier_match = (
            change_pattern.fullmatch(dependency_id)
            if isinstance(dependency_id, str)
            else None
        )
        consumes = dependency.get("consumes")
        status = dependency.get("status")
        pr = dependency.get("pull_request")
        exact_status = status in {"available", "integrated"}
        valid_pr = _valid_pull_request(pr, exact=exact_status)
        valid = (
            identifier_match is not None
            and identifier_match.group("layer") is not None
            and dependency_id != own_id
            and dependency_id not in seen
            and status in statuses
            and valid_pr
            and (
                _is_exact_commit(dependency.get("required_commit"))
                or (not exact_status and dependency.get("required_commit") == "pending")
            )
            and isinstance(consumes, list)
            and bool(consumes)
            and len(consumes) == len(set(consumes))
            and all(
                isinstance(identifier, str)
                and trace_pattern.fullmatch(identifier) is not None
                for identifier in consumes
            )
            and all(
                isinstance(dependency.get(field), str)
                and bool(str(dependency.get(field)).strip())
                for field in ("claim", "use", "evidence", "reopen_when")
            )
            and _is_iso_date(dependency.get("checked_at"))
        )
        if not valid:
            diagnostics.append(
                _diag("DSET-E153", path, f"invalid dependency: {dependency_id}")
            )
        elif isinstance(dependency_id, str):
            seen.add(dependency_id)
    return diagnostics


def _valid_pull_request(raw: Any, *, exact: bool) -> bool:
    if not isinstance(raw, dict) or set(raw) != {"repository", "number", "url"}:
        return False
    repository = raw.get("repository")
    number = raw.get("number")
    url = raw.get("url")
    if (
        not isinstance(repository, str)
        or re.fullmatch(r"[^/]+/[^/]+", repository) is None
    ):
        return False
    if exact:
        return (
            isinstance(number, int)
            and number >= 1
            and isinstance(url, str)
            and url.startswith("https://")
            and url != "pending"
        )
    return (
        ((isinstance(number, int) and number >= 1) or number == "pending")
        and isinstance(url, str)
        and bool(url)
    )


def _is_exact_commit(raw: Any) -> bool:
    return isinstance(raw, str) and re.fullmatch(r"[0-9a-f]{40}", raw) is not None


def _is_iso_date(raw: Any) -> bool:
    if not isinstance(raw, str):
        return False
    try:
        return date.fromisoformat(raw).isoformat() == raw
    except ValueError:
        return False


def _validate_schemas(schema_paths: tuple[Path, ...]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for path in schema_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            diagnostics.append(_diag("DSET-E118", path, str(error)))
    return diagnostics


def _validate_provenance(root: Path) -> list[Diagnostic]:
    layout = discover_layout(root)
    path = layout.provenance_path
    diagnostics: list[Diagnostic] = []
    try:
        data = project_section(root, "source_provenance")
    except (OSError, ValueError, YamlSubsetError) as error:
        diagnostics.append(_diag("DSET-E112", path, str(error)))
        data = {}
    if not data:
        return diagnostics or [_diag("DSET-E112", path, "provenance is missing")]
    for source in data.get("sources", []):
        if not isinstance(source, dict):
            continue
        revision = str(source.get("revision", ""))
        license_name = str(source.get("license_file", ""))
        if not license_name or Path(license_name).name != license_name:
            diagnostics.append(
                _diag(
                    "DSET-E112",
                    layout.legal_files_root,
                    "license_file must be a globally unique carrier name",
                )
            )
            continue
        license_path = layout.legal_files_root / license_name
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            diagnostics.append(
                _diag("DSET-E112", path, "source revision must be a full commit SHA")
            )
        if not license_path.is_file():
            diagnostics.append(
                _diag("DSET-E112", license_path, "retained license is missing")
            )
    return diagnostics


def _validate_markdown(root: Path, layout: RepositoryLayout) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    aliases = transition_aliases(root)
    reverse_aliases = {
        current.resolve(): original.resolve() for original, current in aliases.items()
    }
    relocated_carriers = {path.resolve() for path in aliases.values()}
    for path in _markdown_paths(root):
        relative_parts = path.relative_to(root).parts
        if any(
            logical_part(part) in MARKDOWN_IGNORED_PARTS for part in relative_parts
        ) or (
            layout.separated
            and has_logical_part(Path(*relative_parts), {"legacy", "archive"})
        ):
            continue
        text = path.read_text(encoding="utf-8")
        try:
            parsed = parse_frontmatter(text)
        except FrontmatterError:
            parsed = None
        rendered = _without_code(parsed[1] if parsed is not None else text)
        legacy_atom = layout.separated and (
            (
                parsed is not None
                and isinstance(parsed[0].get("artifact_id"), str)
                and "schema_version" not in parsed[0]
            )
            or (
                parsed is None
                and re.search(
                    r"^\s*-\s+\*\*(?:Decision|Requirement|Question|Problem|"
                    r"Test|Eval(?:uation)?) ID:\*\*",
                    rendered,
                    flags=re.MULTILINE,
                )
                is not None
            )
        )
        if "[[" in rendered or "![[" in rendered:
            diagnostics.append(
                _diag("DSET-E114", path, "Obsidian wiki links are not portable")
            )
        for callout in CALLOUT_PATTERN.findall(rendered):
            if callout.upper() not in GITHUB_CALLOUTS:
                diagnostics.append(
                    _diag(
                        "DSET-E114",
                        path,
                        f"unsupported GitHub alert type: {callout}",
                    )
                )
        details_open = len(re.findall(r"<details(?:\s[^>]*)?>", rendered))
        if details_open != rendered.count("</details>"):
            diagnostics.append(_diag("DSET-E114", path, "unbalanced details element"))
        for raw_target in LINK_PATTERN.findall(rendered):
            target = raw_target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            target = target.split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if "{{" in target:
                continue
            if legacy_atom:
                continue
            resolved = (path.parent / unquote(target)).resolve()
            original_carrier = reverse_aliases.get(path.resolve())
            historical = (
                (original_carrier.parent / unquote(target)).resolve()
                if original_carrier is not None
                else None
            )
            relocated = aliases.get(historical, historical) if historical else None
            if (
                not resolved.exists()
                and not aliases.get(resolved, resolved).exists()
                and (relocated is None or not relocated.exists())
                and path.resolve() not in relocated_carriers
            ):
                diagnostics.append(
                    _diag(
                        "DSET-E113",
                        path,
                        f"local link target does not exist: {raw_target}",
                    )
                )
    return diagnostics


def _markdown_paths(root: Path) -> list[Path]:
    """Return project-visible Markdown, honoring Git ignores when available."""

    return [path for path in _project_visible_files(root) if path.suffix == ".md"]


def _project_visible_files(root: Path) -> list[Path]:
    """Return tracked and unignored files, with a non-Git filesystem fallback."""

    try:
        result = subprocess.run(
            [
                "git",
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
            ],
            cwd=root,
            check=False,
            capture_output=True,
        )
    except OSError:
        result = None
    if result is not None and result.returncode == 0:
        visible: list[Path] = []
        for item in result.stdout.split(b"\0"):
            if not item:
                continue
            relative = Path(item.decode("utf-8"))
            path = root / relative
            if relative.parts[:1] == (".dset_runtime",) or relative.parts[:2] == (
                ".dset",
                "runtime",
            ):
                continue
            if path.is_file() or path.is_symlink():
                visible.append(path)
        return sorted(visible)
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.relative_to(root).parts[:1] != (".dset_runtime",)
        and path.relative_to(root).parts[:2] != (".dset", "runtime")
        and not any(
            logical_part(part) in MARKDOWN_IGNORED_PARTS
            for part in path.relative_to(root).parts
        )
        and not any(part.endswith(".egg-info") for part in path.relative_to(root).parts)
        and path.name != ".DS_Store"
    )


def _active_applied_files(root: Path) -> list[Path]:
    """Return only current project-owned carriers for schema 1.5 checks."""

    layout = discover_layout(root)
    owners = (
        layout.project_root,
        *(layout.layer_root(layer) for layer in LAYERS),
        layout.versions_root,
    )
    visible: list[Path] = []
    for owner in owners:
        if not owner.is_dir():
            continue
        for path in owner.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(owner)
            if has_logical_part(relative, {"legacy", "archive", "templates"}):
                continue
            visible.append(path)
    return sorted(visible)


def _without_code(text: str) -> str:
    without_fences = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return re.sub(r"`[^`]*`", "", without_fences)


def _manifest_project_key(manifest: dict[str, Any]) -> str | None:
    project = manifest.get("project")
    key = project.get("key") if isinstance(project, dict) else None
    if not isinstance(key, str) or PROJECT_KEY_PATTERN.fullmatch(key) is None:
        return None
    return key


def _trace_id_pattern(
    project_key: str, trace_types: tuple[str, ...]
) -> re.Pattern[str]:
    invalid = set(trace_types) - set(TRACE_TYPES)
    if invalid:
        raise ValueError(f"unknown trace ID types: {sorted(invalid)}")
    type_pattern = "|".join(re.escape(item) for item in trace_types)
    layer_pattern = "|".join(TRACE_LAYERS)
    return re.compile(
        rf"^{re.escape(project_key)}-(?P<type>{type_pattern})"
        rf"(?:-(?P<layer>{layer_pattern}))?-(?P<number>[0-9]{{3,}})$"
    )


def _missing_semantic_fields(
    paths: list[Path], identifier: str, trace_type: str
) -> list[str]:
    section: str | None = None
    heading_pattern = re.compile(
        rf"^(?P<marks>#{{1,6}})[^\n]*\b{re.escape(identifier)}\b[^\n]*$",
        flags=re.MULTILINE,
    )
    for path in paths:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        match = heading_pattern.search(text)
        if match is None:
            continue
        level = len(match.group("marks"))
        next_heading = re.compile(rf"^#{{1,{level}}}\s+", flags=re.MULTILINE).search(
            text, match.end()
        )
        section = text[match.start() : next_heading.start() if next_heading else None]
        break
    if section is None:
        return ["record heading"]
    normalized = re.sub(r"[*_`]", "", section).lower()
    if trace_type == "STORY":
        fields = {
            "actor or stakeholder": ("actor or stakeholder", "actor/stakeholder"),
            "desired capability or outcome": ("desired capability or outcome",),
            "value or purpose": ("value or purpose",),
            "linked Requirements": ("linked requirements",),
            "linked Scenarios": ("linked scenarios",),
        }
    elif trace_type == "OUTCOME":
        fields = {
            "baseline": ("baseline",),
            "target": ("target",),
            "observation method/source": (
                "observation method/source",
                "source and method",
                "measurement source and method",
            ),
            "evaluation window": (
                "evaluation window",
                "measurement window",
                "| window |",
            ),
            "Problem/Opportunity links": (
                "linked problems/opportunities",
                "problem or opportunity",
                "| problem |",
                "| opportunity |",
            ),
            "User Story links/disposition": (
                "linked user stories",
                "| user stories |",
            ),
            "Eval links": ("linked evals", "| evals |"),
        }
    else:
        return []
    return [
        label
        for label, alternatives in fields.items()
        if not any(alternative in normalized for alternative in alternatives)
    ]


def _is_legacy_change(data: dict[str, Any]) -> bool:
    return str(data.get("schema_version")) in {"1.0", "1.0-draft"}


def _safe_load(path: Path, diagnostics: list[Diagnostic]) -> dict[str, Any] | None:
    try:
        data = load(path)
    except (OSError, YamlSubsetError) as error:
        diagnostics.append(_diag("DSET-E119", path, str(error)))
        return None
    if not isinstance(data, dict):
        diagnostics.append(_diag("DSET-E119", path, "root must be a mapping"))
        return None
    return data


def _diag(code: str, path: Path, message: str) -> Diagnostic:
    return Diagnostic(code=code, path=path, message=message)
