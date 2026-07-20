from __future__ import annotations

import fnmatch
import json
import re
import subprocess
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any

from .diagnostics import Diagnostic
from .layout import discover_layout
from .yaml_subset import YamlSubsetError, load

PROFILE_SCHEMA_VERSION = "1.0"
GATE_IDS = (
    "conformance",
    "purity",
    "spec_sync",
    "typing_contracts",
    "lint_static_analysis",
    "secret_hygiene",
)
PROFILE_STATUSES = frozenset({"candidate", "active", "custom"})
REVISION_POLICIES = frozenset({"exact", "descendant"})
GATE_STATUSES = frozenset({"enforced", "ratcheted", "blocked", "not-applicable"})
_ID = re.compile(r"^[a-z][a-z0-9-]*$")
_SHA = re.compile(r"^[0-9a-f]{40}$")


def resolve_profile_path(root: Path, profile_id: str) -> Path:
    """Resolve project-owned profiles before framework candidate templates."""

    layout = discover_layout(root.resolve())
    local = layout.layer_root("tool") / "profiles" / f"{profile_id}.yaml"
    if local.is_file():
        return local
    candidate = (
        layout.layer_root("tool")
        / "templates"
        / "enforcement-profiles"
        / f"{profile_id}.yaml"
    )
    if candidate.is_file():
        return candidate
    raise FileNotFoundError(f"enforcement profile is missing: {profile_id}")


def validate_profile_file(path: Path) -> tuple[dict[str, Any], list[Diagnostic]]:
    try:
        data = load(path)
    except (OSError, UnicodeError, YamlSubsetError) as error:
        return {}, [_diag(path, f"profile cannot be loaded: {error}")]
    if not isinstance(data, dict):
        return {}, [_diag(path, "profile must be a mapping")]
    return data, validate_profile_data(path, data)


def validate_profile_data(path: Path, data: dict[str, Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    profile_id = data.get("id")
    status = data.get("status")
    if data.get("schema_version") != PROFILE_SCHEMA_VERSION:
        diagnostics.append(_diag(path, "schema_version must be 1.0"))
    if not isinstance(profile_id, str) or _ID.fullmatch(profile_id) is None:
        diagnostics.append(_diag(path, "profile id must be kebab-case"))
    if status not in PROFILE_STATUSES:
        diagnostics.append(_diag(path, "profile status is invalid"))
    if data.get("target_revision_policy") not in REVISION_POLICIES:
        diagnostics.append(_diag(path, "target_revision_policy is invalid"))
    for field in ("version", "language_family"):
        if not _nonempty(data.get(field)):
            diagnostics.append(_diag(path, f"{field} must be non-empty"))

    evidence = _mapping(data.get("evidence"))
    revision = evidence.get("revision")
    upstream = evidence.get("upstream_revision")
    if not _https(evidence.get("repository")):
        diagnostics.append(_diag(path, "evidence repository must be HTTPS"))
    if not isinstance(revision, str) or _SHA.fullmatch(revision) is None:
        diagnostics.append(_diag(path, "evidence revision must be a full SHA"))
    if upstream is not None and (
        not isinstance(upstream, str) or _SHA.fullmatch(upstream) is None
    ):
        diagnostics.append(_diag(path, "upstream_revision must be a full SHA"))
    if not _nonempty(evidence.get("license")):
        diagnostics.append(_diag(path, "evidence license must be non-empty"))
    try:
        date.fromisoformat(str(evidence.get("observed_on")))
    except ValueError:
        diagnostics.append(_diag(path, "observed_on must be an ISO date"))

    toolchain = _mapping(data.get("toolchain"))
    scripts = _string_mapping(toolchain.get("scripts"))
    if not scripts:
        diagnostics.append(_diag(path, "toolchain scripts must be a mapping"))
    for field in ("runtime", "runtime_range", "package_manager", "lockfile"):
        if not _nonempty(toolchain.get(field)):
            diagnostics.append(_diag(path, f"toolchain {field} is missing"))

    scope = _mapping(data.get("scope"))
    for field in (
        "source_roots",
        "test_roots",
        "required_files",
        "generated_outputs",
        "exclusions",
    ):
        values = _string_list(scope.get(field))
        if values is None or not values:
            diagnostics.append(_diag(path, f"scope {field} must be non-empty"))
            continue
        for value in values:
            if not _safe_relative(value):
                diagnostics.append(_diag(path, f"unsafe profile path: {value}"))

    counts = _int_mapping(_mapping(data.get("observed")).get("file_counts"))
    for field in ("source_typescript", "test_typescript", "lint_files"):
        if field not in counts:
            diagnostics.append(_diag(path, f"observed file count is missing: {field}"))

    baseline = _mapping(data.get("warning_baseline"))
    rules = _int_mapping(baseline.get("rules"))
    warning_count = baseline.get("warning_count")
    if baseline.get("revision") != revision:
        diagnostics.append(_diag(path, "warning baseline revision must match evidence"))
    if baseline.get("error_count") != 0:
        diagnostics.append(_diag(path, "hard errors cannot enter the warning baseline"))
    if not isinstance(warning_count, int) or warning_count < 0:
        diagnostics.append(_diag(path, "warning_count must be non-negative"))
    elif warning_count != sum(rules.values()):
        diagnostics.append(_diag(path, "warning_count must equal per-rule counts"))
    if baseline.get("policy") != "shrink-only":
        diagnostics.append(_diag(path, "warning baseline policy must be shrink-only"))

    sequence = _string_list(data.get("canonical_sequence"))
    if sequence is None or not sequence or len(sequence) != len(set(sequence)):
        diagnostics.append(
            _diag(path, "canonical_sequence must be unique and non-empty")
        )
        sequence = []
    gates = data.get("gates")
    seen: set[str] = set()
    blocked = False
    if not isinstance(gates, list):
        diagnostics.append(_diag(path, "gates must be a list"))
    else:
        for item in gates:
            if not isinstance(item, dict):
                diagnostics.append(_diag(path, "every gate must be a mapping"))
                continue
            gate_id = item.get("id")
            gate_status = item.get("status")
            if not isinstance(gate_id, str) or gate_id not in GATE_IDS:
                diagnostics.append(_diag(path, f"unknown gate id: {gate_id}"))
                continue
            if gate_id in seen:
                diagnostics.append(_diag(path, f"duplicate gate: {gate_id}"))
            seen.add(gate_id)
            if gate_status not in GATE_STATUSES:
                diagnostics.append(_diag(path, f"invalid gate status: {gate_id}"))
            commands = _string_list(item.get("commands"))
            if commands is None:
                diagnostics.append(_diag(path, f"gate commands are invalid: {gate_id}"))
                commands = []
            for command in commands:
                if command not in sequence:
                    diagnostics.append(
                        _diag(
                            path,
                            f"gate command is outside canonical sequence: {command}",
                        )
                    )
            if gate_status in {"enforced", "ratcheted"} and not commands:
                diagnostics.append(
                    _diag(path, f"enforced gate has no command: {gate_id}")
                )
            if gate_status in {"blocked", "not-applicable"} and not _nonempty(
                item.get("reason")
            ):
                diagnostics.append(_diag(path, f"gate reason is missing: {gate_id}"))
            if gate_status == "blocked":
                blocked = True
    if seen != set(GATE_IDS):
        missing = ", ".join(sorted(set(GATE_IDS) - seen))
        diagnostics.append(_diag(path, f"profile must define all six gates: {missing}"))

    blockers = _string_list(data.get("known_blockers"))
    if blockers is None:
        diagnostics.append(_diag(path, "known_blockers must be a list"))
        blockers = []
    if status == "active" and (blockers or blocked):
        diagnostics.append(_diag(path, "active profile cannot retain blockers"))
    promotion = _mapping(data.get("promotion"))
    if not _string_list(promotion.get("requires")):
        diagnostics.append(_diag(path, "promotion requirements must be non-empty"))
    return diagnostics


def inspect_target(
    profile_path: Path,
    profile: dict[str, Any],
    target: Path,
) -> dict[str, Any]:
    """Inspect pinned target structure without executing target-owned commands."""

    target = target.resolve()
    diagnostics = validate_profile_data(profile_path, profile)
    revision = _git(target, "rev-parse", "HEAD")
    expected_revision = _mapping(profile.get("evidence")).get("revision")
    revision_policy = profile.get("target_revision_policy")
    if revision_policy == "exact" and revision != expected_revision:
        diagnostics.append(
            _diag(target, f"target revision drift: {revision or 'unavailable'}")
        )
    elif revision_policy == "descendant" and (
        not isinstance(expected_revision, str)
        or not _git_is_ancestor(target, expected_revision)
    ):
        diagnostics.append(
            _diag(target, "target revision is not descended from profile evidence")
        )

    scope = _mapping(profile.get("scope"))
    required_files = _string_list(scope.get("required_files")) or []
    for relative in required_files:
        if not (target / relative).is_file():
            diagnostics.append(
                _diag(target / relative, "required profile file is missing")
            )

    package_path = target / "package.json"
    try:
        package = json.loads(package_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        diagnostics.append(_diag(package_path, f"package.json cannot be read: {error}"))
        package = {}
    actual_scripts = package.get("scripts", {}) if isinstance(package, dict) else {}
    expected_scripts = _string_mapping(
        _mapping(profile.get("toolchain")).get("scripts")
    )
    for name, command in expected_scripts.items():
        if not isinstance(actual_scripts, dict) or actual_scripts.get(name) != command:
            diagnostics.append(_diag(package_path, f"target script drift: {name}"))

    tracked = _git_files(target)
    source_roots = _string_list(scope.get("source_roots")) or []
    test_roots = _string_list(scope.get("test_roots")) or []
    counts = {
        "source_typescript": _count_typescript(tracked, source_roots),
        "test_typescript": _count_typescript(tracked, test_roots),
    }
    counts["lint_files"] = counts["source_typescript"] + counts["test_typescript"]
    expected_counts = _int_mapping(_mapping(profile.get("observed")).get("file_counts"))
    for name, expected in expected_counts.items():
        if counts.get(name) != expected:
            diagnostics.append(
                _diag(
                    target, f"target file population drift: {name}={counts.get(name)}"
                )
            )

    blockers = _string_list(profile.get("known_blockers")) or []
    return {
        "schema_version": PROFILE_SCHEMA_VERSION,
        "profile": profile.get("id"),
        "profile_status": profile.get("status"),
        "target_revision_policy": revision_policy,
        "profile_path": profile_path.as_posix(),
        "target": target.as_posix(),
        "target_revision": revision,
        "file_counts": counts,
        "known_blockers": blockers,
        "promotion_eligible": not diagnostics and not blockers,
        "diagnostics": [item.render(target) for item in sorted(set(diagnostics))],
        "commands_executed": False,
    }


def _count_typescript(paths: list[str], roots: list[str]) -> int:
    return sum(
        1
        for path in paths
        if path.endswith((".ts", ".tsx"))
        and any(
            path == root or path.startswith(root.rstrip("/") + "/") for root in roots
        )
    )


def _git(root: Path, *args: str) -> str | None:
    result = subprocess.run(
        ["git", *args], cwd=root, check=False, capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _git_is_ancestor(root: Path, ancestor: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, "HEAD"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _git_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, check=False, capture_output=True
    )
    if result.returncode:
        return []
    return [item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def _safe_relative(value: str) -> bool:
    path = PurePosixPath(value)
    return (
        bool(value)
        and "\\" not in value
        and not path.is_absolute()
        and ".." not in path.parts
        and not fnmatch.fnmatchcase(value, "*/./*")
    )


def _mapping(value: object) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _string_mapping(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {
        str(key): item
        for key, item in value.items()
        if isinstance(key, str) and isinstance(item, str) and item.strip()
    }


def _int_mapping(value: object) -> dict[str, int]:
    if not isinstance(value, dict):
        return {}
    return {
        str(key): item
        for key, item in value.items()
        if isinstance(key, str) and isinstance(item, int) and item >= 0
    }


def _string_list(value: object) -> list[str] | None:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        return None
    return list(value)


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _https(value: object) -> bool:
    return isinstance(value, str) and value.startswith("https://")


def _diag(path: Path, message: str) -> Diagnostic:
    return Diagnostic("DSET-E167", path, message)
