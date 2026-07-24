"""Provide DSET commit provenance behavior."""

from __future__ import annotations

import hashlib
import re
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .diagnostics import Diagnostic
from .layout import discover_layout
from .semantic_types import build_semantic_classification_index
from .structured_data import load

# ID_PATTERN validates id pattern; this module owns the accepted syntax.
ID_PATTERN = re.compile(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+")
# SESSION_PATTERN validates session pattern; this module owns the accepted syntax.
SESSION_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*:[A-Za-z0-9._:-]+$")
# COMMIT_PATTERN validates commit pattern; this module owns the accepted syntax.
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
# DIGEST_PATTERN validates digest pattern; this module owns the accepted syntax.
DIGEST_PATTERN = re.compile(r"^[0-9a-f]{64}$")
# CORRECTION_FIELDS defines correction fields; this module owns the default.
CORRECTION_FIELDS = {
    "commit",
    "original_message_sha256",
    "mode",
    "decision_ids",
    "verifies",
    "resolves",
    "session",
    "rationale",
}


@dataclass(frozen=True)
class CommitRecord:
    """Represent commit record behavior and state."""

    commit: str
    message: str
    message_sha256: str


def validate_commit_provenance(root: Path) -> list[Diagnostic]:
    """Validate commit provenance using the declared repository contract."""
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
    return [
        Diagnostic("DSET-E168", manifest_path, problem)
        for problem in validate_commit_history(
            commits, known, raw_policy.get("corrections", [])
        )
    ]


def validate_commit_history(
    commits: list[CommitRecord],
    known: Mapping[str, tuple[str, str]],
    raw_corrections: object,
) -> list[str]:
    """Validate commit history using the declared repository contract."""
    corrections, problems = _parse_corrections(raw_corrections, commits)
    for record in commits:
        original_problems = validate_commit_message(record.message, known)
        correction = corrections.get(record.commit)
        if correction is None:
            problems.extend(
                f"commit {record.commit[:12]}: {problem}"
                for problem in original_problems
            )
            continue
        if not original_problems:
            problems.append(
                f"correction for commit {record.commit} is unnecessary because "
                "the original provenance is valid"
            )
            continue
        corrected_message = _corrected_message(correction)
        problems.extend(
            f"correction for commit {record.commit}: {problem}"
            for problem in validate_commit_message(corrected_message, known)
        )
    return problems


def validate_commit_message(
    message: str, known: Mapping[str, tuple[str, str]]
) -> list[str]:
    """Validate commit message using the declared repository contract."""
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
        problems.extend(_authority_reference_problems("Implements", implements, known))
    elif decisions and verifies:
        problems.extend(_authority_reference_problems("Decision", decisions, known))
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


def _parse_corrections(
    raw_corrections: object, commits: list[CommitRecord]
) -> tuple[dict[str, Mapping[str, Any]], list[str]]:
    """Parse corrections using the declared repository contract."""
    if not isinstance(raw_corrections, list):
        return {}, ["commit_provenance.corrections must be a list"]
    records = {record.commit: record for record in commits}
    corrections: dict[str, Mapping[str, Any]] = {}
    problems: list[str] = []
    for index, raw in enumerate(raw_corrections, start=1):
        prefix = f"commit_provenance.corrections[{index}]"
        if not isinstance(raw, Mapping):
            problems.append(f"{prefix} must be a mapping")
            continue
        fields = set(raw)
        if fields != CORRECTION_FIELDS:
            missing = sorted(CORRECTION_FIELDS - fields)
            extra = sorted(fields - CORRECTION_FIELDS)
            details: list[str] = []
            if missing:
                details.append(f"missing {', '.join(missing)}")
            if extra:
                details.append(f"unknown {', '.join(extra)}")
            problems.append(f"{prefix} fields are invalid: {'; '.join(details)}")
            continue
        commit = raw.get("commit")
        if not isinstance(commit, str) or not COMMIT_PATTERN.fullmatch(commit):
            problems.append(f"{prefix}.commit requires one full lowercase SHA")
            continue
        if commit in corrections:
            problems.append(f"duplicate provenance correction for commit {commit}")
            continue
        record = records.get(commit)
        if record is None:
            problems.append(
                f"provenance correction commit is outside the validated range: {commit}"
            )
            continue
        digest = raw.get("original_message_sha256")
        if not isinstance(digest, str) or not DIGEST_PATTERN.fullmatch(digest):
            problems.append(f"{prefix}.original_message_sha256 is invalid")
            continue
        if digest != record.message_sha256:
            problems.append(
                f"provenance correction message digest mismatch for commit {commit}"
            )
            continue
        mode = raw.get("mode")
        if mode not in {"implementation", "evidence"}:
            problems.append(f"{prefix}.mode must be implementation or evidence")
            continue
        if not _valid_id_list(raw.get("decision_ids"), allow_empty=False):
            problems.append(f"{prefix}.decision_ids requires unique canonical IDs")
            continue
        verifies = raw.get("verifies")
        if not _valid_id_list(verifies, allow_empty=mode == "implementation"):
            problems.append(
                f"{prefix}.verifies must be empty for implementation or contain "
                "unique canonical IDs for evidence"
            )
            continue
        if mode == "implementation" and verifies:
            problems.append(f"{prefix}.verifies must be empty for implementation")
            continue
        if not _valid_id_list(raw.get("resolves"), allow_empty=True):
            problems.append(f"{prefix}.resolves must contain unique canonical IDs")
            continue
        session = raw.get("session")
        if not isinstance(session, str) or not SESSION_PATTERN.fullmatch(session):
            problems.append(f"{prefix}.session requires exactly one valid session ID")
            continue
        rationale = raw.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            problems.append(f"{prefix}.rationale requires non-empty text")
            continue
        corrections[commit] = raw
    return corrections, problems


def _valid_id_list(value: object, *, allow_empty: bool) -> bool:
    if not isinstance(value, list) or (not allow_empty and not value):
        return False
    if not all(isinstance(item, str) and ID_PATTERN.fullmatch(item) for item in value):
        return False
    return len(value) == len(set(value))


def _corrected_message(correction: Mapping[str, Any]) -> str:
    """Handle message using the declared repository contract."""
    label = "Implements" if correction["mode"] == "implementation" else "Decision"
    lines = [f"{label}: {', '.join(correction['decision_ids'])}"]
    if correction["verifies"]:
        lines.append(f"Verifies: {', '.join(correction['verifies'])}")
    if correction["resolves"]:
        lines.append(f"Resolves: {', '.join(correction['resolves'])}")
    lines.append(f"Session: {correction['session']}")
    return "\n".join(lines)


def _resolve_base(root: Path, manifest_path: Path, start: str) -> str | None:
    """Resolve base using the declared repository contract."""
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


def _commits_after(root: Path, base: str | None) -> list[CommitRecord]:
    """Handle after using the declared repository contract."""
    revision = f"{base}..HEAD" if base else "HEAD"
    completed = subprocess.run(
        ["git", "rev-list", "--no-merges", "--reverse", revision],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return [_read_commit(root, commit) for commit in completed.stdout.split()]


def _read_commit(root: Path, commit: str) -> CommitRecord:
    """Read commit using the declared repository contract."""
    completed = subprocess.run(
        ["git", "cat-file", "commit", commit],
        cwd=root,
        check=True,
        capture_output=True,
    )
    _headers, separator, message = completed.stdout.partition(b"\n\n")
    if not separator:
        raise ValueError(f"commit object has no message boundary: {commit}")
    return CommitRecord(
        commit=commit,
        message=message.decode("utf-8", errors="surrogateescape"),
        message_sha256=hashlib.sha256(message).hexdigest(),
    )


def _has_head(root: Path) -> bool:
    """Handle head using the declared repository contract."""
    completed = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


def _trailers(message: str) -> dict[str, list[str]]:
    """Handle trailers using the declared repository contract."""
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


def _authority_reference_problems(
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
    """Handle reference problems using the declared repository contract."""
    if not identifiers:
        return [f"{label} requires at least one canonical ID"]
    return [
        f"{label} references unknown ID: {identifier}"
        for identifier in sorted(identifiers)
        if identifier not in known
    ]
