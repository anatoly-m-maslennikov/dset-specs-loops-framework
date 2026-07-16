from __future__ import annotations

import difflib
import hashlib
import re
import shutil
from pathlib import Path
from typing import Any, cast

from .diagnostics import Diagnostic
from .errors import DsetCommandError
from .layout import LAYERS, discover_layout, has_manifest
from .yaml_subset import YamlSubsetError, dump, load

RULE_PATTERN = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)+$")
WORKFLOW_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
CUSTOMIZATION = {"unmodified", "custom"}
APPLICABILITY = {"applicable", "not-applicable"}
RULE_LAYERS = {layer.upper() for layer in LAYERS}
GOVERNANCE_SCHEMA_VERSION = 1.1


def find_repository(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if has_manifest(candidate):
            return candidate
    raise FileNotFoundError(f"DSET project root not found from: {start}")


def validate_governance(
    root: Path, expected_profile: str | None = None
) -> list[Diagnostic]:
    root = root.resolve()
    layout = discover_layout(root)
    manifest_path = layout.manifest_path
    if expected_profile is None:
        try:
            manifest = load(manifest_path)
        except (OSError, YamlSubsetError):
            manifest = {}
        profiles = manifest.get("profiles", {}) if isinstance(manifest, dict) else {}
        if isinstance(profiles, dict):
            selected = profiles.get("repository_governance")
            expected_profile = str(selected) if selected else None
    if not expected_profile:
        return [
            _diag(
                "DSET-E137",
                manifest_path,
                "repository-governance profile is not selected",
            )
        ]
    registry_path = layout.governance_path
    if not registry_path.is_file():
        return [_diag("DSET-E130", registry_path, "governance registry is missing")]
    try:
        data = load(registry_path)
    except (OSError, YamlSubsetError) as error:
        return [_diag("DSET-E131", registry_path, str(error))]
    if not isinstance(data, dict):
        return [_diag("DSET-E131", registry_path, "registry must be a mapping")]
    return validate_governance_registry(root, registry_path, data, expected_profile)


def validate_governance_registry(
    root: Path,
    registry_path: Path,
    data: dict[str, Any],
    expected_profile: str,
) -> list[Diagnostic]:
    root = root.resolve()
    layout = discover_layout(root)
    diagnostics: list[Diagnostic] = []
    if data.get("schema_version") != GOVERNANCE_SCHEMA_VERSION:
        diagnostics.append(
            _diag(
                "DSET-E131",
                registry_path,
                "unsupported governance registry schema version",
            )
        )
    profile = data.get("profile")
    if not isinstance(profile, dict):
        return [_diag("DSET-E137", registry_path, "profile must be a mapping")]
    if profile.get("id") != expected_profile:
        diagnostics.append(
            _diag(
                "DSET-E137",
                registry_path,
                "registry profile does not match the selected project profile",
            )
        )
    profile_version = profile.get("version")
    if not isinstance(profile_version, str) or not profile_version:
        diagnostics.append(
            _diag("DSET-E137", registry_path, "profile version is missing")
        )
    profile_custom = profile.get("customization")
    if profile_custom not in CUSTOMIZATION:
        diagnostics.append(
            _diag("DSET-E139", registry_path, "invalid profile customization status")
        )

    rules = data.get("rules")
    if not isinstance(rules, list) or not rules:
        return diagnostics + [
            _diag("DSET-E131", registry_path, "rules must be a non-empty list")
        ]
    rule_items = [item for item in rules if isinstance(item, dict)]
    if len(rule_items) != len(rules):
        diagnostics.append(
            _diag("DSET-E131", registry_path, "every rule must be a mapping")
        )
    by_id: dict[str, dict[str, Any]] = {}
    actual_custom: set[str] = set()
    for rule in rule_items:
        rule_id = rule.get("id")
        if not isinstance(rule_id, str) or not RULE_PATTERN.fullmatch(rule_id):
            diagnostics.append(
                _diag("DSET-E131", registry_path, f"invalid rule ID: {rule_id}")
            )
            continue
        if rule_id in by_id:
            diagnostics.append(
                _diag("DSET-E132", registry_path, f"duplicate rule owner: {rule_id}")
            )
            continue
        by_id[rule_id] = rule
        layer = rule.get("layer")
        if layer not in RULE_LAYERS:
            diagnostics.append(
                _diag("DSET-E131", registry_path, f"invalid rule layer: {rule_id}")
            )
        owner = rule.get("owner")
        if not isinstance(owner, str) or not owner.strip():
            diagnostics.append(
                _diag("DSET-E131", registry_path, f"missing rule owner: {rule_id}")
            )
        applicability = rule.get("applicability")
        if applicability not in APPLICABILITY:
            diagnostics.append(
                _diag(
                    "DSET-E137",
                    registry_path,
                    f"invalid applicability for {rule_id}: {applicability}",
                )
            )
        if applicability == "not-applicable" and not str(rule.get("reason", "")):
            diagnostics.append(
                _diag(
                    "DSET-E137",
                    registry_path,
                    f"not-applicable rule requires a reason: {rule_id}",
                )
            )
        local = _local_path(root, rule.get("path"))
        if local is None:
            diagnostics.append(
                _diag(
                    "DSET-E134", registry_path, f"rule path is outside root: {rule_id}"
                )
            )
            continue
        if not local.is_file():
            diagnostics.append(
                _diag("DSET-E133", local, f"governing document is missing: {rule_id}")
            )
            continue
        if layout.layered and layer in RULE_LAYERS:
            expected_root = layout.layer_root(str(layer).lower()) / "governance"
            try:
                local.relative_to(expected_root)
            except ValueError:
                diagnostics.append(
                    _diag(
                        "DSET-E134",
                        local,
                        f"rule is outside its owning layer: {rule_id}/{layer}",
                    )
                )
        source = rule.get("source")
        source_sha = source.get("sha256") if isinstance(source, dict) else None
        if not isinstance(source_sha, str) or not SHA256_PATTERN.fullmatch(source_sha):
            diagnostics.append(
                _diag("DSET-E139", registry_path, f"invalid source digest: {rule_id}")
            )
            continue
        customization = rule.get("customization")
        if customization not in CUSTOMIZATION:
            diagnostics.append(
                _diag("DSET-E139", registry_path, f"invalid customization: {rule_id}")
            )
            continue
        if customization == "custom":
            actual_custom.add(rule_id)
        if customization == "unmodified" and _sha256(local) != source_sha:
            diagnostics.append(
                _diag(
                    "DSET-E139",
                    local,
                    f"local rule changed without custom status: {rule_id}",
                )
            )
    if profile_custom == "unmodified" and actual_custom:
        diagnostics.append(
            _diag(
                "DSET-E139", registry_path, "custom rules require custom profile status"
            )
        )

    diagnostics.extend(_validate_dependencies(registry_path, by_id))
    diagnostics.extend(_validate_precedence(registry_path, by_id))
    workflows = data.get("workflows")
    workflow_items = workflows if isinstance(workflows, list) else []
    if not workflow_items:
        diagnostics.append(
            _diag("DSET-E136", registry_path, "workflows must be a non-empty list")
        )
    workflow_ids: set[str] = set()
    for workflow in workflow_items:
        if not isinstance(workflow, dict):
            diagnostics.append(
                _diag("DSET-E136", registry_path, "every workflow must be a mapping")
            )
            continue
        workflow_id = workflow.get("id")
        if (
            not isinstance(workflow_id, str)
            or not WORKFLOW_PATTERN.fullmatch(workflow_id)
            or workflow_id in workflow_ids
        ):
            diagnostics.append(
                _diag("DSET-E136", registry_path, f"invalid workflow: {workflow_id}")
            )
            continue
        workflow_ids.add(workflow_id)
        selected = workflow.get("rules")
        if not isinstance(selected, list) or not selected:
            diagnostics.append(
                _diag(
                    "DSET-E136", registry_path, f"workflow has no rules: {workflow_id}"
                )
            )
            continue
        seen: set[str] = set()
        for rule_id in selected:
            if not isinstance(rule_id, str) or rule_id not in by_id:
                diagnostics.append(
                    _diag(
                        "DSET-E131",
                        registry_path,
                        f"workflow references missing rule owner: {rule_id}",
                    )
                )
                continue
            rule = by_id[rule_id]
            if rule.get("applicability") != "applicable":
                diagnostics.append(
                    _diag(
                        "DSET-E137",
                        registry_path,
                        f"workflow selects incompatible rule: {rule_id}",
                    )
                )
            dependencies = rule.get("depends_on", [])
            if isinstance(dependencies, list) and not set(dependencies).issubset(seen):
                diagnostics.append(
                    _diag(
                        "DSET-E135",
                        registry_path,
                        "workflow dependency order is invalid: "
                        f"{workflow_id}/{rule_id}",
                    )
                )
            seen.add(rule_id)
    diagnostics.extend(
        _validate_wrappers(root, registry_path, data.get("wrappers"), workflow_ids)
    )
    return sorted(set(diagnostics))


def resolve_workflow(
    root: Path, workflow_id: str
) -> tuple[dict[str, Any] | None, list[Diagnostic]]:
    root = root.resolve()
    diagnostics = validate_governance(root)
    if diagnostics:
        return None, diagnostics
    path = discover_layout(root).governance_path
    data = cast(dict[str, Any], load(path))
    workflow = next(
        (
            item
            for item in data["workflows"]
            if isinstance(item, dict) and item.get("id") == workflow_id
        ),
        None,
    )
    if workflow is None:
        return None, [_diag("DSET-E136", path, f"unknown workflow: {workflow_id}")]
    by_id = {item["id"]: item for item in data["rules"]}
    wrapper = next(
        (
            item
            for item in data.get("wrappers", [])
            if isinstance(item, dict) and item.get("workflow") == workflow_id
        ),
        None,
    )
    rules: list[dict[str, Any]] = []
    for rule_id in workflow["rules"]:
        rule = by_id[rule_id]
        source = rule["source"]
        local = root / rule["path"]
        rules.append(
            {
                "id": rule_id,
                "layer": rule["layer"],
                "path": rule["path"],
                "owner": rule["owner"],
                "applicability": rule["applicability"],
                "precedence_over": list(rule["precedence_over"]),
                "customization": rule["customization"],
                "source_profile": source["profile"],
                "source_version": source["version"],
                "sha256": _sha256(local),
            }
        )
    profile = data["profile"]
    return (
        {
            "workflow_id": workflow_id,
            "profile": profile["id"],
            "profile_version": profile["version"],
            "customization": profile["customization"],
            "rules": rules,
            "wrapper": wrapper,
            "conflicts": [],
            "conflict_resolution": {
                "status": "unavailable",
                "coverage": [],
                "reason_code": "DSET-CONFLICT-RESOLUTION-UNAVAILABLE",
            },
        },
        [],
    )


def materialize_governance(
    source_root: Path,
    target_root: Path,
    profile_id: str = "core-v1",
    *,
    install_wrappers: bool = False,
) -> Path:
    source_root = source_root.resolve()
    target_root = target_root.resolve()
    source_layout = discover_layout(source_root)
    target_layout = discover_layout(target_root)
    manifest = target_layout.manifest_path
    if not manifest.is_file():
        raise DsetCommandError("DSET-E001", manifest, "project manifest is missing")
    try:
        profile_path = source_layout.find_template(
            Path("governance") / profile_id / "profile.yaml"
        )
    except (FileNotFoundError, ValueError) as error:
        raise DsetCommandError(
            "DSET-E140",
            source_layout.template_roots[0]
            / "governance"
            / profile_id
            / "profile.yaml",
            str(error),
        ) from error
    profile = cast(dict[str, Any], load(profile_path))
    project = cast(dict[str, Any], load(manifest))
    release = project.get("release", {})
    release_not_applicable = (
        isinstance(release, dict) and release.get("status") == "not-applicable"
    )
    if profile.get("id") != profile_id:
        raise DsetCommandError(
            "DSET-E140", profile_path, "governance profile identity mismatch"
        )
    registry_path = target_layout.governance_path
    rules = cast(list[dict[str, Any]], profile.get("rules", []))
    profile_relative = Path("governance") / profile_id

    def source_template(relative: Path) -> Path:
        try:
            return source_layout.find_template(relative)
        except (FileNotFoundError, ValueError) as error:
            raise DsetCommandError(
                "DSET-E140", source_layout.template_roots[0] / relative, str(error)
            ) from error

    readme_template = source_template(profile_relative / "README.md")
    templates: dict[str, Path] = {}
    targets: dict[str, Path] = {}
    governance_roots = {target_layout.governance_root}
    for item in rules:
        rule_id = str(item.get("id", ""))
        layer = item.get("layer")
        if layer not in RULE_LAYERS:
            raise DsetCommandError(
                "DSET-E140", profile_path, f"invalid rule layer: {rule_id}/{layer}"
            )
        templates[rule_id] = source_template(profile_relative / str(item["template"]))
        destination = target_layout.governance_root
        if target_layout.layered:
            destination = target_layout.layer_root(str(layer).lower()) / "governance"
            governance_roots.add(destination)
        targets[rule_id] = destination / str(item["target"])
    existing = [path for path in governance_roots if path.exists()]
    if registry_path.exists() or existing:
        occupied = registry_path if registry_path.exists() else sorted(existing)[0]
        raise FileExistsError(f"governance destination already exists: {occupied}")
    copied_wrappers: list[Path] = []
    for destination in sorted(governance_roots):
        destination.mkdir(parents=True)
    try:
        _write_governance_hub(
            readme_template,
            target_layout.governance_root / "README.md",
            layered=target_layout.layered,
        )
        rendered_rules: list[dict[str, Any]] = []
        for item in rules:
            rule_id = str(item["id"])
            template = templates[rule_id]
            target = targets[rule_id]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(template, target)
            applicability = item.get("applicability", "applicable")
            reason = item.get("reason", "selected by the local profile")
            if item["id"] == "DSET-RULE-RELEASE" and release_not_applicable:
                applicability = "not-applicable"
                reason = str(release.get("reason"))
            dependencies = list(item.get("depends_on", []))
            if release_not_applicable:
                dependencies = [
                    dependency
                    for dependency in dependencies
                    if dependency != "DSET-RULE-RELEASE"
                ]
            rendered_rules.append(
                {
                    "id": rule_id,
                    "layer": item["layer"],
                    "path": target.relative_to(target_root).as_posix(),
                    "owner": "project",
                    "applicability": applicability,
                    "reason": reason,
                    "depends_on": dependencies,
                    "precedence_over": list(item.get("precedence_over", [])),
                    "customization": "unmodified",
                    "source": {
                        "profile": profile_id,
                        "version": str(profile["version"]),
                        "template": template.relative_to(source_root).as_posix(),
                        "sha256": _sha256(template),
                    },
                }
            )
        wrappers: list[dict[str, Any]] = []
        for item in cast(list[dict[str, Any]], profile.get("wrappers", [])):
            if release_not_applicable and item.get("workflow") == "release":
                continue
            source = source_root / str(item["path"])
            target = target_root / str(item["path"])
            if source_root != target_root and install_wrappers:
                folder = target.parent
                if folder.exists():
                    raise FileExistsError(f"wrapper destination exists: {folder}")
                shutil.copytree(source.parent, folder)
                copied_wrappers.append(folder)
            if target.is_file():
                wrappers.append(
                    {
                        "workflow": item["workflow"],
                        "path": target.relative_to(target_root).as_posix(),
                        "sha256": _sha256(source),
                    }
                )
        rendered_workflows = []
        for workflow in cast(list[dict[str, Any]], profile["workflows"]):
            if release_not_applicable and workflow.get("id") == "release":
                continue
            rendered = dict(workflow)
            if release_not_applicable:
                rendered["rules"] = [
                    rule
                    for rule in cast(list[str], workflow.get("rules", []))
                    if rule != "DSET-RULE-RELEASE"
                ]
            rendered_workflows.append(rendered)
        registry = {
            "schema_version": profile.get("schema_version", GOVERNANCE_SCHEMA_VERSION),
            "profile": {
                "id": profile_id,
                "version": str(profile["version"]),
                "customization": "unmodified",
            },
            "rules": rendered_rules,
            "workflows": rendered_workflows,
            "wrappers": wrappers,
        }
        registry_path.write_text(dump(registry), encoding="utf-8")
    except Exception:
        if registry_path.exists():
            registry_path.unlink()
        for destination in sorted(governance_roots, reverse=True):
            if destination.exists():
                shutil.rmtree(destination)
        for wrapper in copied_wrappers:
            if wrapper.exists():
                shutil.rmtree(wrapper)
        raise
    return registry_path


def _write_governance_hub(source: Path, target: Path, *, layered: bool) -> None:
    content = source.read_text(encoding="utf-8")
    if layered:
        for layer in ("meta", "tool", "skill", "ops"):
            content = content.replace(
                f"../../../../{layer}/templates/governance/core-v1/",
                f"../../{layer}/governance/",
            )
    target.write_text(content, encoding="utf-8")


def refresh_customization(root: Path) -> Path:
    root = root.resolve()
    path = discover_layout(root).governance_path
    data = cast(dict[str, Any], load(path))
    custom = False
    for rule in cast(list[dict[str, Any]], data.get("rules", [])):
        local = _local_path(root, rule.get("path"))
        source = rule.get("source")
        source_sha = source.get("sha256") if isinstance(source, dict) else None
        if local is None or not local.is_file() or not isinstance(source_sha, str):
            continue
        status = "unmodified" if _sha256(local) == source_sha else "custom"
        rule["customization"] = status
        custom = custom or status == "custom"
    cast(dict[str, Any], data["profile"])["customization"] = (
        "custom" if custom else "unmodified"
    )
    path.write_text(dump(data), encoding="utf-8")
    return path


def diff_governance(root: Path, source_root: Path) -> str:
    root = root.resolve()
    source_root = source_root.resolve()
    data = cast(dict[str, Any], load(discover_layout(root).governance_path))
    output: list[str] = []
    for rule in cast(list[dict[str, Any]], data.get("rules", [])):
        source = cast(dict[str, Any], rule["source"])
        template = source_root / str(source["template"])
        local = root / str(rule["path"])
        if not template.is_file() or not local.is_file():
            continue
        output.extend(
            difflib.unified_diff(
                template.read_text(encoding="utf-8").splitlines(keepends=True),
                local.read_text(encoding="utf-8").splitlines(keepends=True),
                fromfile=template.relative_to(source_root).as_posix(),
                tofile=local.relative_to(root).as_posix(),
            )
        )
    return "".join(output) or "No local governance differences.\n"


def _validate_dependencies(
    path: Path, by_id: dict[str, dict[str, Any]]
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for rule_id, rule in by_id.items():
        dependencies = rule.get("depends_on", [])
        if not isinstance(dependencies, list):
            diagnostics.append(
                _diag("DSET-E135", path, f"dependencies must be a list: {rule_id}")
            )
            continue
        for dependency in dependencies:
            if dependency not in by_id:
                diagnostics.append(
                    _diag(
                        "DSET-E131",
                        path,
                        f"dependency has no rule owner: {rule_id}/{dependency}",
                    )
                )
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(rule_id: str) -> None:
        if rule_id in visiting:
            diagnostics.append(
                _diag("DSET-E135", path, f"rule dependency cycle includes: {rule_id}")
            )
            return
        if rule_id in visited:
            return
        visiting.add(rule_id)
        dependencies = by_id[rule_id].get("depends_on", [])
        if isinstance(dependencies, list):
            for dependency in dependencies:
                if isinstance(dependency, str) and dependency in by_id:
                    visit(dependency)
        visiting.remove(rule_id)
        visited.add(rule_id)

    for rule_id in by_id:
        visit(rule_id)
    return diagnostics


def _validate_precedence(
    path: Path, by_id: dict[str, dict[str, Any]]
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    graph: dict[str, list[str]] = {}
    for rule_id, rule in by_id.items():
        precedence = rule.get("precedence_over")
        if not isinstance(precedence, list):
            diagnostics.append(
                _diag(
                    "DSET-E150",
                    path,
                    f"precedence_over must be a list: {rule_id}",
                )
            )
            graph[rule_id] = []
            continue
        if len(precedence) != len(set(map(str, precedence))):
            diagnostics.append(
                _diag(
                    "DSET-E150",
                    path,
                    f"precedence targets must be unique: {rule_id}",
                )
            )
        graph[rule_id] = []
        for target in precedence:
            if not isinstance(target, str) or target not in by_id:
                diagnostics.append(
                    _diag(
                        "DSET-E150",
                        path,
                        f"precedence target has no rule owner: {rule_id}/{target}",
                    )
                )
                continue
            graph[rule_id].append(target)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(rule_id: str) -> None:
        if rule_id in visiting:
            diagnostics.append(
                _diag(
                    "DSET-E150",
                    path,
                    f"rule precedence cycle includes: {rule_id}",
                )
            )
            return
        if rule_id in visited:
            return
        visiting.add(rule_id)
        for target in graph.get(rule_id, []):
            visit(target)
        visiting.remove(rule_id)
        visited.add(rule_id)

    for rule_id in by_id:
        visit(rule_id)
    return diagnostics


def _validate_wrappers(
    root: Path,
    registry_path: Path,
    raw: Any,
    workflow_ids: set[str],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    wrappers = raw if isinstance(raw, list) else []
    seen: set[str] = set()
    for wrapper in wrappers:
        if not isinstance(wrapper, dict):
            diagnostics.append(
                _diag("DSET-E138", registry_path, "every wrapper must be a mapping")
            )
            continue
        workflow = wrapper.get("workflow")
        if not isinstance(workflow, str) or workflow not in workflow_ids:
            diagnostics.append(
                _diag(
                    "DSET-E138", registry_path, f"unknown wrapper workflow: {workflow}"
                )
            )
            continue
        if workflow in seen:
            diagnostics.append(
                _diag("DSET-E138", registry_path, f"duplicate wrapper: {workflow}")
            )
        seen.add(workflow)
        path = _local_path(root, wrapper.get("path"))
        expected = wrapper.get("sha256")
        if path is None or not path.is_file():
            diagnostics.append(
                _diag("DSET-E138", registry_path, f"wrapper is missing: {workflow}")
            )
        elif not isinstance(expected, str) or _sha256(path) != expected:
            diagnostics.append(
                _diag("DSET-E138", path, f"wrapper identity mismatch: {workflow}")
            )
    return diagnostics


def _local_path(root: Path, raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw or Path(raw).is_absolute():
        return None
    path = (root / raw).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return None
    return path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _diag(code: str, path: Path, message: str) -> Diagnostic:
    return Diagnostic(code=code, path=path, message=message)
