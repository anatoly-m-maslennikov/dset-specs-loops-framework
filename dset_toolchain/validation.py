from __future__ import annotations

import json
import re
import subprocess
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote

from . import __version__
from .compilation import compilation_is_fresh, compilation_path
from .dependencies import validate_dependency_policy
from .diagnostics import Diagnostic
from .governance import validate_governance
from .health import health_is_fresh, health_path
from .layout import RepositoryLayout, discover_layout
from .lineage import validate_artifact_lineage
from .profiles import VALID_PROFILES, required_artifacts
from .semantic_atoms import validate_semantic_atoms
from .semantic_types import classify_semantic_id, validate_semantic_classifications
from .settings import load_project_settings
from .yaml_subset import YamlSubsetError, load, loads

ID_PATTERN = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)+$")
CHANGE_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROJECT_KEY_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*$")
TRACE_LAYERS = ("META", "GOV", "TOOL", "SKILL", "OPS")
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
            "version_scope",
        }
    ),
    "procedure": frozenset({"playbook", "runbook"}),
    "plan": frozenset(
        {
            "roadmap",
            "implementation_plan",
            "test_plan",
            "evaluation_plan",
            "release_plan",
        }
    ),
    "change": frozenset(),
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
    "readiness_record": frozenset(),
    "release_record": frozenset(),
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
        _diag("DSET-E157", root / "dset.toml", issue) for issue in settings_issues
    )
    try:
        layout = discover_layout(root)
    except ValueError as error:
        return [_diag("DSET-E001", root / "dset", str(error))]
    manifest_path = layout.manifest_path
    if not manifest_path.is_file():
        return [_diag("DSET-E001", manifest_path, "project manifest is missing")]
    if (root / ".dset" / "specs").exists() or (root / ".dset" / "changes").exists():
        diagnostics.append(
            _diag(
                "DSET-E110",
                root / ".dset",
                "hidden state cannot own committed project truth",
            )
        )
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
    diagnostics.extend(_validate_markdown(root))
    diagnostics.extend(validate_semantic_atoms(root))
    diagnostics.extend(validate_semantic_classifications(root))
    diagnostics.extend(validate_artifact_lineage(root))
    diagnostics.extend(validate_dependency_policy(root))
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
    manifest_path = change_dir / "change.yaml"
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
    try:
        files, directories = required_artifacts(root, profile)
    except (KeyError, ValueError, YamlSubsetError) as error:
        diagnostics.append(_diag("DSET-E103", manifest_path, str(error)))
        return diagnostics
    for relative in sorted(files):
        path = change_dir / relative
        if not path.is_file():
            diagnostics.append(_diag("DSET-E104", path, "required artifact is missing"))
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
            expected = expected_relative
            if expected is None:
                try:
                    expected = change_dir.relative_to(root).as_posix()
                except ValueError:
                    expected = None
            if expected and archive.get("path") != expected:
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
    if str(data.get("schema_version")) == "1.2":
        structure = data.get("structure")
        valid_structure = structure == {"layout": "layered-v1"}
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
                    and set(layers).issubset({item.lower() for item in TRACE_LAYERS})
                )
                if not valid_packages:
                    break
        expected_change_contract = {
            "change_id_format": "project-type-layer-sequence",
            "change_slug_format": "kebab-case",
            "workspace_default": "integration-branch",
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
                    "schema 1.2 requires layered-v1 and package id/status/layers",
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
    if data.get("schema_version") == 1.1 and registry != "dset/intake.yaml":
        diagnostics.append(
            _diag("DSET-E115", path, "schema 1.1 requires dset/intake.yaml")
        )
    elif isinstance(registry, str) and not (root / registry).is_file():
        diagnostics.append(
            _diag("DSET-E115", root / registry, "work-item registry is missing")
        )
    if str(data.get("schema_version")) == "1.2":
        if registry != "dset/scopes/gov/intake.yaml":
            diagnostics.append(
                _diag("DSET-E143", path, "schema 1.2 requires the layered intake path")
            )
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
    layered = str(manifest.get("schema_version")) == "1.2"
    scopes: dict[str, str]
    if layered:
        scopes = {segment.lower(): segment for segment in TRACE_LAYERS}
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
                or scope_id != segment.lower()
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
                    "intake must register META, GOV, TOOL, SKILL, and OPS exactly once",
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
        package_manifest = base / "package.yaml"
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
    artifact_names = {
        "hub": "README.md",
        "domain": "domain.md",
        "spec": "spec.md",
        "contracts": "contracts.md",
        "stories": "stories.md",
        "outcomes": "outcomes.md",
        "test_plan": "test-plan.md",
        "eval_plan": "eval-plan.md",
    }
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
        physical_layer = relative.parts[0]
        physical_package = path.parent.name
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
                ) or identifier_layer == physical_layer.upper()
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
        missing_path = (
            layout.layer_root(layer) / "specs/packages" / package_id / "package.yaml"
        )
        diagnostics.append(
            _diag("DSET-E144", missing_path, "declared package fragment is missing")
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
    registry = _safe_load(registry_path, diagnostics)
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
    type_registry = _safe_load(type_registry_path, diagnostics)
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
    diagnostics.extend(
        _validate_artifact_path_rules(
            root,
            registry_path,
            data,
            types,
            project_key=project_key,
            include_subtype_in_names=include_subtype_in_names,
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
                "artifact_types must contain the thirteen canonical types exactly",
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


def _validate_artifact_path_rules(
    root: Path,
    registry_path: Path,
    data: dict[str, Any],
    catalog: dict[str, frozenset[str]],
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
    *,
    project_key: str | None,
    include_subtype_in_names: bool,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    ignored_parts = {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".uv-cache",
        ".venv",
        "__pycache__",
        "dist",
    }
    for path in root.rglob("*"):
        if not path.is_file() or any(part in ignored_parts for part in path.parts):
            continue
        relative = path.relative_to(root).as_posix()
        matched_rules = [
            rule for rule in rules if _path_rule_matches(relative, rule[0])
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
            if (artifact_type, artifact_subtype) != (rule_type, rule_subtype):
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
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    try:
        metadata = loads("\n".join(lines[1:end]))
    except YamlSubsetError:
        return None
    if not isinstance(metadata, dict):
        return None
    artifact_type = metadata.get("artifact_type")
    artifact_subtype = metadata.get("artifact_subtype")
    artifact_id = metadata.get("artifact_id")
    if artifact_type is None and artifact_subtype is None:
        return None
    return (
        str(artifact_type),
        str(artifact_subtype) if artifact_subtype is not None else None,
        str(artifact_id) if artifact_id is not None else None,
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
    tokens = [project_key, type_token]
    if include_subtype_in_names and artifact_subtype is not None:
        tokens.append(artifact_subtype.replace("_", "-").upper())
    prefix = "-".join(tokens) + "-"
    identifier_suffix = artifact_id.removeprefix(prefix)
    filename_suffix = path.stem.removeprefix(prefix)
    if (
        artifact_id.startswith(prefix)
        and path.stem.startswith(prefix)
        and re.match(r"^\d+(?:-|$)", identifier_suffix)
        and re.match(r"^\d+(?:-|$)", filename_suffix)
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
        for field in ("id", "root", "hub", "owner", "purpose"):
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
        area_root = _artifact_path(root, entry.get("root"))
        hub = _artifact_path(root, entry.get("hub"))
        if area_root is None:
            diagnostics.append(
                _diag(
                    "DSET-E121",
                    registry_path,
                    f"invalid artifact root: {entry.get('root')}",
                )
            )
        elif area_root in seen_roots:
            diagnostics.append(
                _diag(
                    "DSET-E121",
                    registry_path,
                    f"duplicate artifact root: {entry.get('root')}",
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
    for entry in [root_entry, *areas]:
        hub = _artifact_path(root, entry.get("hub"))
        if hub is None or not hub.is_file():
            continue
        headings = _level_two_headings(hub.read_text(encoding="utf-8"))
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
    root_hub = _artifact_path(root, root_entry.get("hub"))
    if root_hub is None or not root_hub.is_file() or not isinstance(root_id, str):
        return diagnostics
    targets = _local_link_targets(root_hub)
    for area in areas:
        if area.get("parent") != root_id:
            continue
        hub = _artifact_path(root, area.get("hub"))
        if hub is not None and hub not in targets:
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
    manifest_path = change_dir / "change.yaml"
    legacy = _is_legacy_change(data)
    manifest = _safe_load(discover_layout(root).manifest_path, diagnostics) or {}
    project_key = _manifest_project_key(manifest)
    if project_key is None:
        diagnostics.append(
            _diag("DSET-E106", manifest_path, "project.key is unavailable")
        )
        return diagnostics
    groups: dict[str, list[Path]] = {
        "requirements": list((change_dir / "specs").glob("*.md")),
        "tests": [change_dir / "test-plan.md"],
        "evals": [change_dir / "eval-plan.md"],
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


def _validate_layered_change(
    layout: RepositoryLayout, change_dir: Path, data: dict[str, Any]
) -> list[Diagnostic]:
    path = change_dir / "change.yaml"
    diagnostics: list[Diagnostic] = []
    project = _safe_load(layout.manifest_path, diagnostics) or {}
    diagnostics.extend(_validate_change_target(path, data.get("target"), project))
    primary = data.get("primary_layer")
    affected = data.get("affected_layers")
    try:
        physical = layout.change_layer(change_dir)
    except ValueError:
        physical = None
    layer_names = {layer.lower() for layer in TRACE_LAYERS}
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
        or change_match.group("layer").lower() != primary
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
        if policy is not None and policy != "dset/scopes/ops/governance/release.md":
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
            manifest = change / "change.yaml"
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
    path = discover_layout(root).provenance_path
    diagnostics: list[Diagnostic] = []
    data = _safe_load(path, diagnostics)
    if not data:
        return diagnostics or [_diag("DSET-E112", path, "provenance is missing")]
    for source in data.get("sources", []):
        if not isinstance(source, dict):
            continue
        revision = str(source.get("revision", ""))
        license_path = root / str(source.get("license_file", ""))
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            diagnostics.append(
                _diag("DSET-E112", path, "source revision must be a full commit SHA")
            )
        if not license_path.is_file():
            diagnostics.append(
                _diag("DSET-E112", license_path, "retained license is missing")
            )
    return diagnostics


def _validate_markdown(root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for path in _markdown_paths(root):
        if any(part in MARKDOWN_IGNORED_PARTS for part in path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8")
        rendered = _without_code(text)
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
            resolved = (path.parent / unquote(target)).resolve()
            if not resolved.exists():
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

    try:
        result = subprocess.run(
            [
                "git",
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                "*.md",
            ],
            cwd=root,
            check=False,
            capture_output=True,
        )
    except OSError:
        result = None
    if result is not None and result.returncode == 0:
        return sorted(
            root / item.decode("utf-8") for item in result.stdout.split(b"\0") if item
        )
    return sorted(root.rglob("*.md"))


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
