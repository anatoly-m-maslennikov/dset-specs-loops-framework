"""Provide DSET evidence behavior."""

from __future__ import annotations

import re
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from typing import Any

from .diagnostics import Diagnostic
from .frontmatter import FrontmatterError
from .frontmatter import load as load_frontmatter
from .identity import has_logical_part

# ID_PATTERN validates id pattern; this module owns the accepted syntax.
ID_PATTERN = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)+$")
# SESSION_PATTERN validates session pattern; this module owns the accepted syntax.
SESSION_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*:[A-Za-z0-9._:-]+$")
# EVIDENCE_SUBTYPES defines evidence subtypes; this module owns the default.
EVIDENCE_SUBTYPES = frozenset(
    {"test_result", "evaluation_result", "review_report", "run_record"}
)
# POLARITIES defines polarities; this module owns the default.
POLARITIES = frozenset({"supports", "contradicts", "mixed", "inconclusive"})
# CURRENTNESS defines currentness; this module owns the default.
CURRENTNESS = frozenset({"current", "stale", "superseded"})
# REQUIRED_FIELDS defines required fields; this module owns the default.
REQUIRED_FIELDS = frozenset(
    {
        "schema_version",
        "artifact_type",
        "artifact_subtype",
        "artifact_id",
        "priority",
        "llm_session_ids",
        "subject",
        "producer",
        "method",
        "context",
        "evidence_location",
        "polarity",
        "currentness",
        "reopen_when",
        "relations",
    }
)
# OPTIONAL_FIELDS defines optional fields; this module owns the default.
OPTIONAL_FIELDS = frozenset(
    {
        "observed_at",
        "validity_window",
        "independent_producer",
        "rival_explanations",
        "limitations",
        "rationale",
    }
)


def validate_evidence_records(
    root: Path,
    paths: Iterable[Path],
    legacy_paths: frozenset[str],
    *,
    allow_unversioned_legacy: bool = False,
) -> list[Diagnostic]:
    """Validate native Evidence Records while preserving a finite legacy set."""

    root = root.resolve()
    diagnostics: list[Diagnostic] = []
    for candidate in paths:
        path = candidate.resolve()
        if path.suffix.lower() != ".md" or has_logical_part(
            path.relative_to(root), {"templates"}
        ):
            continue
        relative = path.relative_to(root).as_posix()
        try:
            parsed = load_frontmatter(path)
        except (OSError, UnicodeError, FrontmatterError) as error:
            if relative in legacy_paths:
                continue
            diagnostics.append(_diag(path, str(error)))
            continue
        metadata = parsed[0] if parsed is not None else None
        artifact_type = metadata.get("artifact_type") if metadata is not None else None
        if relative in legacy_paths:
            if artifact_type not in {None, "evidence_record"}:
                diagnostics.append(
                    _diag(
                        path,
                        "legacy evidence compatibility path has a conflicting "
                        "artifact type",
                    )
                )
            continue
        if (
            allow_unversioned_legacy
            and artifact_type == "evidence_record"
            and metadata is not None
            and "schema_version" not in metadata
        ):
            continue
        if artifact_type != "evidence_record":
            continue
        if parsed is None or parsed[2] != "toml":
            diagnostics.append(
                _diag(path, "new Evidence Records require TOML frontmatter")
            )
            continue
        assert metadata is not None
        diagnostics.extend(_validate_native_record(path, metadata))
    return diagnostics


def _validate_native_record(path: Path, data: dict[str, Any]) -> list[Diagnostic]:
    """Validate native record using the declared repository contract."""
    diagnostics: list[Diagnostic] = []
    keys = set(data)
    missing = sorted(REQUIRED_FIELDS - keys)
    unknown = sorted(keys - REQUIRED_FIELDS - OPTIONAL_FIELDS)
    if missing:
        diagnostics.append(
            _diag(path, "Evidence Record is missing fields: " + ", ".join(missing))
        )
    if unknown:
        diagnostics.append(
            _diag(path, "Evidence Record has unknown fields: " + ", ".join(unknown))
        )
    if data.get("schema_version") != "1.0":
        diagnostics.append(_diag(path, "Evidence Record schema_version must be 1.0"))
    if data.get("artifact_type") != "evidence_record":
        diagnostics.append(_diag(path, "artifact_type must be evidence_record"))
    if data.get("artifact_subtype") not in EVIDENCE_SUBTYPES:
        diagnostics.append(_diag(path, "Evidence Record subtype is invalid"))
    _required_id(path, data.get("artifact_id"), "artifact_id", diagnostics)
    _nonempty(path, data.get("priority"), "priority", diagnostics)
    _sessions(path, data.get("llm_session_ids"), diagnostics)
    _subject(path, data.get("subject"), diagnostics)
    _producer(path, data.get("producer"), diagnostics)
    _method(path, data.get("method"), diagnostics)
    _nonempty_list(path, data.get("context"), "context", diagnostics)
    _nonempty(path, data.get("evidence_location"), "evidence_location", diagnostics)
    if data.get("polarity") not in POLARITIES:
        diagnostics.append(_diag(path, "Evidence Record polarity is invalid"))
    if data.get("currentness") not in CURRENTNESS:
        diagnostics.append(_diag(path, "Evidence Record currentness is invalid"))
    _nonempty(path, data.get("reopen_when"), "reopen_when", diagnostics)
    _observation_time(path, data, diagnostics)
    _relations(path, data.get("relations"), diagnostics)
    _optional_extensions(path, data, diagnostics)
    return diagnostics


def _subject(path: Path, value: object, diagnostics: list[Diagnostic]) -> None:
    """Handle subject using the declared repository contract."""
    if not isinstance(value, dict) or set(value) != {
        "id",
        "revision",
        "intended_use",
    }:
        diagnostics.append(
            _diag(path, "subject requires exactly id, revision, and intended_use")
        )
        return
    _required_id(path, value.get("id"), "subject.id", diagnostics)
    revision = value.get("revision")
    _nonempty(path, revision, "subject.revision", diagnostics)
    if isinstance(revision, str) and revision.strip().lower() == "pending":
        diagnostics.append(_diag(path, "subject.revision cannot be pending"))
    _nonempty(path, value.get("intended_use"), "subject.intended_use", diagnostics)


def _producer(path: Path, value: object, diagnostics: list[Diagnostic]) -> None:
    """Handle producer using the declared repository contract."""
    if not isinstance(value, dict) or set(value) != {"identity", "performed_work"}:
        diagnostics.append(
            _diag(path, "producer requires exactly identity and performed_work")
        )
        return
    _nonempty(path, value.get("identity"), "producer.identity", diagnostics)
    _nonempty(path, value.get("performed_work"), "producer.performed_work", diagnostics)


def _method(path: Path, value: object, diagnostics: list[Diagnostic]) -> None:
    if not isinstance(value, dict) or set(value) != {"description", "setup"}:
        diagnostics.append(_diag(path, "method requires exactly description and setup"))
        return
    _nonempty(path, value.get("description"), "method.description", diagnostics)
    _nonempty(path, value.get("setup"), "method.setup", diagnostics)


def _observation_time(
    path: Path, data: dict[str, Any], diagnostics: list[Diagnostic]
) -> None:
    """Handle time using the declared repository contract."""
    has_observed = "observed_at" in data
    has_window = "validity_window" in data
    if has_observed == has_window:
        diagnostics.append(
            _diag(
                path,
                "Evidence Record requires exactly one observed_at or validity_window",
            )
        )
        return
    if has_observed:
        _timestamp(path, data.get("observed_at"), "observed_at", diagnostics)
        return
    window = data.get("validity_window")
    if not isinstance(window, dict) or set(window) != {"from", "through"}:
        diagnostics.append(
            _diag(path, "validity_window requires exactly from and through")
        )
        return
    _timestamp(path, window.get("from"), "validity_window.from", diagnostics)
    _timestamp(path, window.get("through"), "validity_window.through", diagnostics)


def _relations(path: Path, value: object, diagnostics: list[Diagnostic]) -> None:
    """Handle relations using the declared repository contract."""
    if not isinstance(value, list) or not value:
        diagnostics.append(_diag(path, "Evidence Record requires relations"))
        return
    evidence_targets: list[str] = []
    for relation in value:
        if not isinstance(relation, dict):
            diagnostics.append(_diag(path, "every evidence relation must be a table"))
            continue
        if relation.get("type") == "evidence_for":
            target = relation.get("target")
            if isinstance(target, str) and ID_PATTERN.fullmatch(target):
                evidence_targets.append(target)
    if not evidence_targets:
        diagnostics.append(
            _diag(path, "Evidence Record requires a canonical evidence_for relation")
        )


def _optional_extensions(
    path: Path, data: dict[str, Any], diagnostics: list[Diagnostic]
) -> None:
    """Handle extensions using the declared repository contract."""
    if "independent_producer" in data and not isinstance(
        data["independent_producer"], bool
    ):
        diagnostics.append(_diag(path, "independent_producer must be boolean"))
    for field in ("rival_explanations", "limitations"):
        if field in data:
            _nonempty_list(path, data[field], field, diagnostics)
    if "rationale" in data:
        _nonempty(path, data["rationale"], "rationale", diagnostics)


def _sessions(path: Path, value: object, diagnostics: list[Diagnostic]) -> None:
    """Handle sessions using the declared repository contract."""
    if not isinstance(value, list):
        diagnostics.append(_diag(path, "llm_session_ids must be a list"))
        return
    if len(value) != len(set(str(item) for item in value)) or any(
        not isinstance(item, str) or SESSION_PATTERN.fullmatch(item) is None
        for item in value
    ):
        diagnostics.append(_diag(path, "llm_session_ids are invalid or duplicated"))


def _required_id(
    path: Path, value: object, field: str, diagnostics: list[Diagnostic]
) -> None:
    if not isinstance(value, str) or ID_PATTERN.fullmatch(value) is None:
        diagnostics.append(_diag(path, f"{field} must be a canonical ID"))


def _nonempty(
    path: Path, value: object, field: str, diagnostics: list[Diagnostic]
) -> None:
    if not isinstance(value, str) or not value.strip():
        diagnostics.append(_diag(path, f"{field} must be non-empty text"))


def _nonempty_list(
    path: Path, value: object, field: str, diagnostics: list[Diagnostic]
) -> None:
    """Handle list using the declared repository contract."""
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item.strip() for item in value)
    ):
        diagnostics.append(_diag(path, f"{field} must be a non-empty text list"))


def _timestamp(
    path: Path, value: object, field: str, diagnostics: list[Diagnostic]
) -> None:
    """Handle timestamp using the declared repository contract."""
    if not isinstance(value, str):
        diagnostics.append(_diag(path, f"{field} must be an ISO-8601 timestamp"))
        return
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        diagnostics.append(_diag(path, f"{field} must be an ISO-8601 timestamp"))
        return
    if parsed.tzinfo is None:
        diagnostics.append(_diag(path, f"{field} must include a timezone"))


def _diag(path: Path, message: str) -> Diagnostic:
    return Diagnostic("DSET-E168", path, message)
