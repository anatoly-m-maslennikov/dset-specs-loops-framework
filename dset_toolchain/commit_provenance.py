from __future__ import annotations

import re
import subprocess
from collections.abc import Mapping
from pathlib import Path

from .diagnostics import Diagnostic
from .layout import discover_layout
from .semantic_types import build_semantic_classification_index
from .yaml_subset import load

ID_PATTERN = re.compile(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+")
SESSION_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*:[A-Za-z0-9._:-]+$")


def validate_commit_provenance(root: Path) -> list[Diagnostic]:
    root = root.resolve()
    if not (root / ".git").exists():
        return []
    manifest_path = discover_layout(root).manifest_path
    manifest = load(manifest_path)
    raw_policy = (
        manifest.get("commit_provenance") if isinstance(manifest, dict) else None
    )
    if not isinstance(raw_policy, Mapping):
        return [
            Diagnostic(
                "DSET-E168",
                manifest_path,
                "project manifest requires commit_provenance policy",
            )
        ]
    start = raw_policy.get("start_commit")
    if not isinstance(start, str) or not start:
        return [
            Diagnostic(
                "DSET-E168",
                manifest_path,
                "commit_provenance.start_commit is required",
            )
        ]
    if not _has_head(root):
        return []
    try:
        base = _resolve_base(root, manifest_path, start)
        commits = _commits_after(root, base)
        known = {
            str(row["id"]): (str(row["type"]), str(row["subtype"]))
            for row in build_semantic_classification_index(root)
        }
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        return [Diagnostic("DSET-E168", manifest_path, str(error))]
    diagnostics: list[Diagnostic] = []
    for commit, message in commits:
        for problem in validate_commit_message(message, known):
            diagnostics.append(
                Diagnostic(
                    "DSET-E168", manifest_path, f"commit {commit[:12]}: {problem}"
                )
            )
    return diagnostics


def validate_commit_message(
    message: str, known: Mapping[str, tuple[str, str]]
) -> list[str]:
    trailers = _trailers(message)
    sessions = trailers.get("Session", [])
    if len(sessions) != 1 or not SESSION_PATTERN.fullmatch(sessions[0]):
        session_problem = "requires exactly one valid Session trailer"
    else:
        session_problem = ""
    implements = _ids(trailers.get("Implements", []))
    decisions = _ids(trailers.get("Decision", []))
    verifies = _ids(trailers.get("Verifies", []))
    problems: list[str] = [session_problem] if session_problem else []
    if implements and (decisions or verifies):
        problems.append("cannot mix implementation and evidence provenance modes")
    elif implements:
        problems.extend(_decision_reference_problems("Implements", implements, known))
    elif decisions and verifies:
        problems.extend(_decision_reference_problems("Decision", decisions, known))
        problems.extend(_known_reference_problems("Verifies", verifies, known))
    else:
        problems.append(
            "requires Implements, or the evidence pair Decision and Verifies"
        )
    resolves = _ids(trailers.get("Resolves", []))
    for identifier in resolves:
        classification = known.get(identifier)
        if classification is None:
            problems.append(f"Resolves references unknown ID: {identifier}")
        elif classification[0] != "problem":
            problems.append(f"Resolves must reference a Problem: {identifier}")
    return problems


def _resolve_base(root: Path, manifest_path: Path, start: str) -> str | None:
    if start == "root":
        return None
    if start == "manifest-addition":
        relative = manifest_path.relative_to(root).as_posix()
        completed = subprocess.run(
            [
                "git",
                "log",
                "--reverse",
                "--format=%H",
                "--diff-filter=A",
                "--",
                relative,
            ],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        commits = completed.stdout.split()
        return commits[0] if commits else None
    completed = subprocess.run(
        ["git", "rev-parse", "--verify", f"{start}^{{commit}}"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _commits_after(root: Path, base: str | None) -> list[tuple[str, str]]:
    revision = f"{base}..HEAD" if base else "HEAD"
    completed = subprocess.run(
        ["git", "log", "--no-merges", "--reverse", "--format=%H%x1f%B%x1e", revision],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    records: list[tuple[str, str]] = []
    for raw in completed.stdout.split("\x1e"):
        raw = raw.strip()
        if raw and "\x1f" in raw:
            commit, message = raw.split("\x1f", 1)
            records.append((commit, message))
    return records


def _has_head(root: Path) -> bool:
    completed = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


def _trailers(message: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for line in message.splitlines():
        key, separator, value = line.partition(":")
        if separator and key in {
            "Implements",
            "Decision",
            "Verifies",
            "Resolves",
            "Session",
        }:
            found.setdefault(key, []).append(value.strip())
    return found


def _ids(values: list[str]) -> set[str]:
    return {identifier for value in values for identifier in ID_PATTERN.findall(value)}


def _decision_reference_problems(
    label: str,
    identifiers: set[str],
    known: Mapping[str, tuple[str, str]],
) -> list[str]:
    problems = _known_reference_problems(label, identifiers, known)
    for identifier in identifiers:
        if identifier in known and known[identifier][0] != "decision":
            problems.append(f"{label} must reference a Decision: {identifier}")
    return problems


def _known_reference_problems(
    label: str,
    identifiers: set[str],
    known: Mapping[str, tuple[str, str]],
) -> list[str]:
    if not identifiers:
        return [f"{label} requires at least one canonical ID"]
    return [
        f"{label} references unknown ID: {identifier}"
        for identifier in sorted(identifiers)
        if identifier not in known
    ]
