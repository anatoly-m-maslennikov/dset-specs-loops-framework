from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from . import __version__
from .diagnostics import Diagnostic
from .governance import validate_governance
from .profiles import VALID_PROFILES, required_artifacts
from .yaml_subset import YamlSubsetError, load

ID_PATTERN = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)+$")
CHANGE_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROJECT_KEY_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*$")
TRACE_LAYERS = ("META", "GOV", "TOOL", "SKILL", "OPS")
TRACE_TYPES = (
    "REQUIREMENT",
    "SCENARIO",
    "INVARIANT",
    "TEST",
    "EVAL",
    "TASK",
    "PROBLEM",
    "OPPORTUNITY",
    "QUESTION",
    "DECISION",
    "CONTRACT",
    "STORY",
    "OUTCOME",
)
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CALLOUT_PATTERN = re.compile(r"^> \[!([^\]]+)\]", re.MULTILINE)
GITHUB_CALLOUTS = {"NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION"}


def validate_repository(root: Path) -> list[Diagnostic]:
    root = root.resolve()
    diagnostics: list[Diagnostic] = []
    dset_root = root / "dset"
    manifest_path = dset_root / "dset.yaml"
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
        diagnostics.extend(_validate_artifacts(root, manifest_path, manifest))
        profiles = manifest.get("profiles", {})
        if isinstance(profiles, dict) and profiles.get("repository_governance"):
            diagnostics.extend(
                validate_governance(root, str(profiles["repository_governance"]))
            )
        diagnostics.extend(_validate_version(root, manifest))
    diagnostics.extend(_validate_schemas(dset_root / "schemas"))
    diagnostics.extend(_validate_provenance(root))
    diagnostics.extend(_validate_packages(root, manifest or {}))
    active = dset_root / "changes"
    if active.is_dir():
        for path in sorted(active.iterdir()):
            if path.is_dir() and path.name != "archive":
                diagnostics.extend(validate_change(root, path, archived=False))
    archive = active / "archive"
    if archive.is_dir():
        for path in sorted(archive.iterdir()):
            if path.is_dir() and re.match(r"^\d{4}-\d{2}-\d{2}-", path.name):
                diagnostics.extend(validate_change(root, path, archived=True))
    diagnostics.extend(_validate_markdown(root))
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
    change_id = str(data.get("id", ""))
    folder_id = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", change_dir.name)
    if not CHANGE_PATTERN.fullmatch(change_id) or change_id != folder_id:
        diagnostics.append(
            _diag(
                "DSET-E101",
                manifest_path,
                "change ID must be kebab-case and match its directory",
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
    diagnostics.extend(_validate_change_ids(root, change_dir, data))
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
                        "DSET-E108",
                        manifest_path,
                        "archive path does not match the change directory",
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
    if data.get("scope_mode") != "multi-scope":
        diagnostics.append(
            _diag("DSET-E142", path, "intake must use the registered layer scopes")
        )
    raw_scopes = data.get("scopes")
    if not isinstance(raw_scopes, list):
        diagnostics.append(_diag("DSET-E142", path, "scopes must be a list"))
        return diagnostics
    scopes: dict[str, str] = {}
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
    item_pattern = _trace_id_pattern(
        project_key, ("PROBLEM", "OPPORTUNITY", "QUESTION")
    )
    decision_pattern = _trace_id_pattern(project_key, ("DECISION",))
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
        if (
            match is None
            or identifier in seen_ids
            or not isinstance(item_type, str)
            or match.group("type").lower() != item_type
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
        decision = raw_item.get("decision")
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


def _validate_version(root: Path, manifest: dict[str, Any]) -> list[Diagnostic]:
    project = manifest.get("project", {})
    role = project.get("repository_role") if isinstance(project, dict) else None
    path = root / "dset" / "version.yaml"
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
        or schemas.get("version") != "1.1"
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
    return diagnostics


def _python_release_version(product_version: str) -> str:
    return product_version.replace("-rc.", "rc")


def _validate_packages(root: Path, manifest: dict[str, Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
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
        base = root / "dset" / str(package.get("path", ""))
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
            pattern = _trace_id_pattern(project_key, (trace_type,))
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


def _validate_artifacts(
    root: Path, manifest_path: Path, manifest: dict[str, Any]
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
    registry_path = root / "dset" / "artifacts.yaml"
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
    return diagnostics


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
    manifest = _safe_load(root / "dset" / "dset.yaml", diagnostics) or {}
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
            else _trace_id_pattern(project_key, (group_types[group],))
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
        registry_path = root / "dset" / "intake.yaml"
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


def _validate_schemas(schema_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for path in sorted(schema_root.glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            diagnostics.append(_diag("DSET-E118", path, str(error)))
    return diagnostics


def _validate_provenance(root: Path) -> list[Diagnostic]:
    path = root / "dset" / "provenance.yaml"
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
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
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
