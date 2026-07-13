from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from .diagnostics import Diagnostic
from .profiles import VALID_PROFILES, required_artifacts
from .yaml_subset import YamlSubsetError, load

ID_PATTERN = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)+$")
CHANGE_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
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
    diagnostics.extend(_validate_change_ids(change_dir, data))
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
    if project.get("repository_slug") != "dset-specs-loops-framework":
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
    return diagnostics


def _validate_packages(root: Path, manifest: dict[str, Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
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
        for relative in artifacts.values():
            path = base / str(relative)
            if not path.is_file():
                diagnostics.append(
                    _diag("DSET-E117", path, "package artifact is missing")
                )
    return diagnostics


def _validate_change_ids(change_dir: Path, data: dict[str, Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    groups = {
        "requirements": list((change_dir / "specs").glob("*.md")),
        "tests": [change_dir / "test-plan.md"],
        "evals": [change_dir / "eval-plan.md"],
        "adrs": list(change_dir.glob("*adr*.md")),
    }
    for group, paths in groups.items():
        ids = data.get(group, [])
        if not isinstance(ids, list):
            diagnostics.append(
                _diag(
                    "DSET-E106", change_dir / "change.yaml", f"{group} must be a list"
                )
            )
            continue
        content = "\n".join(
            path.read_text(encoding="utf-8") for path in paths if path.is_file()
        )
        for identifier in ids:
            if not isinstance(identifier, str) or not ID_PATTERN.fullmatch(identifier):
                diagnostics.append(
                    _diag(
                        "DSET-E106",
                        change_dir / "change.yaml",
                        f"invalid ID: {identifier}",
                    )
                )
            elif identifier not in content:
                diagnostics.append(
                    _diag(
                        "DSET-E106",
                        change_dir / "change.yaml",
                        f"{identifier} is not present in its owning artifact",
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
                change_dir / "change.yaml",
                "requirements and tests cannot be empty",
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
