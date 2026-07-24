"""Validate reusable Agent Skills against the selected DSET profile.

Parameters: skill roots and optional TOML trigger-case catalogs.
Effects: read-only validation; no files, installs, or hosted state are changed.
Errors: aggregated profile diagnostics identify the skill and failed rule.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .toml_codec import TomlCodecError
from .toml_codec import loads as load_toml

# PROFILE_ID identifies the implementation profile enforced by this module.
PROFILE_ID = "agent-skills-v1"
# NAME_PATTERN defines portable skill directory and frontmatter names.
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# MAX_NAME_CHARACTERS follows the open Agent Skills metadata contract.
MAX_NAME_CHARACTERS = 64
# MAX_DESCRIPTION_CHARACTERS follows the open Agent Skills metadata contract.
MAX_DESCRIPTION_CHARACTERS = 1024
# MAX_BODY_LINES bounds eagerly loaded skill instructions.
MAX_BODY_LINES = 500
# REQUIRED_CASE_KINDS defines the minimum routing Evaluation matrix.
REQUIRED_CASE_KINDS = (
    "should_trigger",
    "should_not_trigger",
    "ambiguous_routing",
)
# ALLOWED_ENTRIES bounds the reusable package surface.
ALLOWED_ENTRIES = {"SKILL.md", "agents", "assets", "references", "scripts"}
# FORBIDDEN_PORTABLE_FRAGMENTS catches machine-specific runtime assumptions.
FORBIDDEN_PORTABLE_FRAGMENTS = (
    "/Users/",
    "/home/",
    "/tmp/",
    "~/",
    "C:\\",
    "CODEX_HOME/skills",
    "CLAUDE_CONFIG_DIR/skills",
)


class SkillProfileError(ValueError):
    """Report one or more Agent Skills profile violations."""


@dataclass(frozen=True)
class SkillAuditSummary:
    """Summarize a successful read-only Agent Skills profile audit."""

    profile_id: str
    skill_count: int
    case_count: int
    status: str = "passed"


def audit_skill_catalog(
    skills_root: Path,
    *,
    expected_skills: set[str] | None = None,
    case_catalog: Path | None = None,
) -> SkillAuditSummary:
    """Validate one complete skill catalog and optional trigger-case matrix."""
    issues: list[str] = []
    skills = _skill_directories(skills_root, issues)
    actual = {skill.name for skill in skills}
    if expected_skills is not None and actual != expected_skills:
        issues.append(
            "public catalog mismatch: "
            f"expected={sorted(expected_skills)}, actual={sorted(actual)}"
        )
    for skill in skills:
        issues.extend(audit_skill_package(skill))
    case_count = 0
    if case_catalog is not None:
        case_count, case_issues = _audit_case_catalog(case_catalog, actual)
        issues.extend(case_issues)
    _raise_issues(issues)
    return SkillAuditSummary(PROFILE_ID, len(skills), case_count)


def audit_skill_package(skill: Path) -> list[str]:
    """Return deterministic profile issues for one reusable skill package."""
    issues = _filesystem_issues(skill)
    skill_file = skill / "SKILL.md"
    if not skill_file.is_file():
        return [*issues, f"{skill.name}: SKILL.md is missing"]
    try:
        text = skill_file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return [*issues, f"{skill.name}: SKILL.md is unreadable: {error}"]
    metadata, body, frontmatter_issues = _parse_frontmatter(skill, text)
    issues.extend(frontmatter_issues)
    issues.extend(_metadata_issues(skill, metadata))
    issues.extend(_instruction_issues(skill, body))
    issues.extend(_script_issues(skill))
    return issues


def _skill_directories(skills_root: Path, issues: list[str]) -> list[Path]:
    """Collect real skill directories in deterministic name order."""
    if skills_root.is_symlink() or not skills_root.is_dir():
        issues.append(f"skills root is missing or is a symlink: {skills_root}")
        return []
    return sorted(
        (
            path
            for path in skills_root.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        ),
        key=lambda path: path.name,
    )


def _filesystem_issues(skill: Path) -> list[str]:
    """Return package-shape and symlink portability issues."""
    issues: list[str] = []
    if skill.is_symlink() or not skill.is_dir():
        return [f"{skill.name}: package must be a copied directory"]
    unexpected = sorted(
        path.name for path in skill.iterdir() if path.name not in ALLOWED_ENTRIES
    )
    if unexpected:
        issues.append(f"{skill.name}: unexpected package entries: {unexpected}")
    for path in skill.rglob("*"):
        if path.is_symlink():
            issues.append(f"{skill.name}: symlink is not portable: {path.name}")
    return issues


def _parse_frontmatter(skill: Path, text: str) -> tuple[dict[str, str], str, list[str]]:
    """Parse the required dependency-free YAML scalar subset."""
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return {}, text, [f"{skill.name}: YAML frontmatter is missing"]
    try:
        closing = lines.index("---", 1)
    except ValueError:
        return {}, text, [f"{skill.name}: YAML frontmatter is not closed"]
    metadata: dict[str, str] = {}
    issues: list[str] = []
    for line in lines[1:closing]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line or line[:1].isspace():
            issues.append(f"{skill.name}: required metadata must use one-line scalars")
            continue
        key, raw_value = line.split(":", 1)
        metadata[key.strip()] = _unquote(raw_value.strip())
    return metadata, "\n".join(lines[closing + 1 :]), issues


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _metadata_issues(skill: Path, metadata: dict[str, str]) -> list[str]:
    """Validate discovery name and what-and-when description fields."""
    issues: list[str] = []
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if name != skill.name or NAME_PATTERN.fullmatch(name) is None:
        issues.append(f"{skill.name}: name must match its kebab-case directory")
    if len(name) > MAX_NAME_CHARACTERS:
        issues.append(f"{skill.name}: name exceeds {MAX_NAME_CHARACTERS} characters")
    if not description or len(description) > MAX_DESCRIPTION_CHARACTERS:
        issues.append(f"{skill.name}: description is missing or too long")
    lowered = description.lower()
    if re.search(r"\buse (?:when|for|before|after|if|to)\b", lowered) is None:
        issues.append(f"{skill.name}: description must state when to use the skill")
    return issues


def _instruction_issues(skill: Path, body: str) -> list[str]:
    """Validate progressive disclosure and portable instruction text."""
    issues: list[str] = []
    if len(body.splitlines()) > MAX_BODY_LINES:
        issues.append(f"{skill.name}: SKILL.md body exceeds {MAX_BODY_LINES} lines")
    for fragment in FORBIDDEN_PORTABLE_FRAGMENTS:
        if fragment in body:
            issues.append(
                f"{skill.name}: machine-specific path is prohibited: {fragment}"
            )
    deep_reference = re.compile(r"(?:references|assets)/[^\s)`]+/[^\s)`]+")
    if deep_reference.search(body):
        issues.append(f"{skill.name}: reference chains must stay one level deep")
    return issues


def _script_issues(skill: Path) -> list[str]:
    """Validate every bundled portable Python helper."""
    scripts = skill / "scripts"
    if not scripts.exists():
        return []
    if scripts.is_symlink() or not scripts.is_dir():
        return [f"{skill.name}: scripts must be a real directory"]
    issues: list[str] = []
    for path in sorted(scripts.rglob("*.py")):
        issues.extend(_python_script_issues(skill.name, path))
    return issues


def _python_script_issues(skill_name: str, path: Path) -> list[str]:
    """Return syntax, documentation, and portability helper issues."""
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (OSError, UnicodeError, SyntaxError) as error:
        return [f"{skill_name}: invalid Python helper {path.name}: {error}"]
    issues: list[str] = []
    if ast.get_docstring(tree) is None:
        issues.append(
            f"{skill_name}: Python helper lacks a module docstring: {path.name}"
        )
    for fragment in FORBIDDEN_PORTABLE_FRAGMENTS:
        if fragment in text:
            issues.append(f"{skill_name}: helper contains nonportable path {fragment}")
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _keyword_is_true(node, "shell"):
            issues.append(
                f"{skill_name}: helper uses subprocess shell=True: {path.name}"
            )
    return issues


def _keyword_is_true(call: ast.Call, name: str) -> bool:
    """Return whether a call passes one literal true keyword."""
    return any(
        keyword.arg == name
        and isinstance(keyword.value, ast.Constant)
        and keyword.value.value is True
        for keyword in call.keywords
    )


def _audit_case_catalog(path: Path, skills: set[str]) -> tuple[int, list[str]]:
    """Validate the complete provider-neutral trigger case catalog."""
    try:
        raw = load_toml(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, TomlCodecError) as error:
        return 0, [f"skill case catalog is unreadable: {path}: {error}"]
    if raw.get("profile_id") != PROFILE_ID:
        return 0, [f"skill case catalog must target {PROFILE_ID}"]
    raw_skills = raw.get("skills")
    if not isinstance(raw_skills, dict):
        return 0, ["skill case catalog requires a [skills] table"]
    issues: list[str] = []
    if set(raw_skills) != skills:
        issues.append(
            "skill case catalog mismatch: "
            f"expected={sorted(skills)}, actual={sorted(raw_skills)}"
        )
    count = 0
    for skill_name, value in sorted(raw_skills.items()):
        case_count, case_issues = _case_table_issues(str(skill_name), value)
        count += case_count
        issues.extend(case_issues)
    return count, issues


def _case_table_issues(skill_name: str, value: Any) -> tuple[int, list[str]]:
    """Validate the minimum three-way routing matrix for one skill."""
    if not isinstance(value, dict):
        return 0, [f"{skill_name}: case definition must be a TOML table"]
    issues: list[str] = []
    for kind in REQUIRED_CASE_KINDS:
        prompt = value.get(kind)
        if not isinstance(prompt, str) or not prompt.strip():
            issues.append(f"{skill_name}: missing non-empty {kind} case")
    expected = value.get("ambiguous_expected")
    if not isinstance(expected, str) or not expected.strip():
        issues.append(f"{skill_name}: ambiguous case requires an expected route")
    allowed = {*REQUIRED_CASE_KINDS, "ambiguous_expected"}
    unknown = sorted(set(value) - allowed)
    if unknown:
        issues.append(f"{skill_name}: unknown case fields: {unknown}")
    count = sum(isinstance(value.get(kind), str) for kind in REQUIRED_CASE_KINDS)
    return count, issues


def _raise_issues(issues: list[str]) -> None:
    if issues:
        raise SkillProfileError(
            f"{PROFILE_ID} failed with {len(issues)} issue(s):\n- "
            + "\n- ".join(issues)
        )
