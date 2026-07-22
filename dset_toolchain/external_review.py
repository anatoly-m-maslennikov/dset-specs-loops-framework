"""Provide DSET external review behavior."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from .frontmatter import FrontmatterError
from .frontmatter import parse as parse_frontmatter
from .frontmatter import render as render_frontmatter
from .identity import find_unique_name
from .layout import discover_layout
from .project_data import project_section
from .settings import load_project_settings
from .yaml_subset import load

# ID_PATTERN validates id pattern; this module owns the accepted syntax.
ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")
# FINDING_PATTERN validates finding pattern; this module owns the accepted syntax.
FINDING_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*-REVIEW-FINDING-[0-9]{3,}$")
# SESSION_PATTERN validates session pattern; this module owns the accepted syntax.
SESSION_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*:[A-Za-z0-9._:-]+$")
# SHA_PATTERN validates sha pattern; this module owns the accepted syntax.
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
# DISPOSITIONS defines dispositions; this module owns the default.
DISPOSITIONS = frozenset(
    {
        "reject",
        "defer",
        "route_problem",
        "route_question",
        "route_decision",
        "route_change",
        "route_evergreen",
        "route_proof",
    }
)


def create_review_packet(
    root: Path,
    output: Path,
    *,
    packet_id: str,
    artifacts: list[str],
    criteria: list[str],
    scope: str,
) -> Path:
    """Create review packet using the declared repository contract."""
    root = root.resolve()
    if not ID_PATTERN.fullmatch(packet_id) or "REVIEW-PACKET" not in packet_id:
        raise ValueError("packet_id must be a canonical REVIEW-PACKET ID")
    if not artifacts or len(set(artifacts)) != len(artifacts):
        raise ValueError("packet requires unique reviewed artifacts")
    if not criteria or any(not item.strip() for item in criteria):
        raise ValueError("packet requires non-empty review criteria")
    if not scope.strip():
        raise ValueError("packet requires a bounded scope")
    reviewed = [_file_identity(root, raw) for raw in artifacts]
    registry = project_section(root, "governance_registry")
    raw_rules = registry.get("rules", []) if isinstance(registry, dict) else []
    rules: list[dict[str, str]] = []
    for item in raw_rules:
        if not isinstance(item, dict) or item.get("applicability") != "applicable":
            continue
        rule_path = item.get("document")
        rule_id = item.get("id")
        if not isinstance(rule_path, str) or not isinstance(rule_id, str):
            continue
        identity = _file_identity(root, rule_path)
        rules.append({"id": rule_id, **identity})
    packet = {
        "schema_version": "1.0",
        "artifact_type": "plan",
        "artifact_id": packet_id.replace("REVIEW-PACKET", "PLAN"),
        "packet_id": packet_id,
        "repository": _repository_identity(root),
        "commit": _head(root),
        "scope": scope,
        "criteria": criteria,
        "reviewed_inputs": reviewed,
        "resolved_rules": sorted(rules, key=lambda item: item["id"]),
        "allowed_effects": ["read_only_report"],
    }
    content = _markdown(packet, "External review packet", _packet_body())
    return _write_new(output, content)


def validate_review_report(
    root: Path, packet_path: Path, report_path: Path
) -> dict[str, Any]:
    """Validate review report using the declared repository contract."""
    root = root.resolve()
    packet, _ = _read_markdown(packet_path)
    report, body = _read_markdown(report_path)
    _validate_packet(root, packet)
    settings, issues = load_project_settings(root)
    if issues:
        raise ValueError(issues[0])
    allowed_priorities = {*settings.priority_scale, "unknown"}
    _validate_report(packet, report, body, allowed_priorities)
    return {
        "report_id": report["artifact_id"],
        "packet_id": report["packet_id"],
        "reviewed_commit": report["reviewed_commit"],
        "report_sha256": _sha256(report_path),
        "finding_ids": [item["id"] for item in report["findings"]],
        "implementation_authorized": False,
    }


def reconcile_review(
    root: Path,
    packet_path: Path,
    report_path: Path,
    candidate_path: Path,
) -> dict[str, Any]:
    """Handle review using the declared repository contract."""
    validated = validate_review_report(root, packet_path, report_path)
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    if not isinstance(candidate, dict):
        raise ValueError("review reconciliation must be a JSON object")
    required = {
        "schema_version",
        "report_id",
        "report_sha256",
        "reconciled_at",
        "llm_session_ids",
        "findings",
    }
    if set(candidate) != required or candidate.get("schema_version") != "1.0":
        raise ValueError("review reconciliation envelope is invalid")
    if candidate.get("report_id") != validated["report_id"]:
        raise ValueError("reconciliation report_id does not match the report")
    if candidate.get("report_sha256") != validated["report_sha256"]:
        raise ValueError("reconciliation report digest does not match the report")
    _datetime(str(candidate.get("reconciled_at")), "reconciled_at")
    _sessions(candidate.get("llm_session_ids"))
    raw_findings = candidate.get("findings")
    if not isinstance(raw_findings, list):
        raise ValueError("reconciliation findings must be a list")
    reconciled = [_validate_disposition(item) for item in raw_findings]
    actual_ids = [item["finding_id"] for item in reconciled]
    expected_ids = list(validated["finding_ids"])
    if len(actual_ids) != len(set(actual_ids)):
        raise ValueError("reconciliation finding IDs must be unique")
    if set(actual_ids) != set(expected_ids):
        raise ValueError("every report finding requires exactly one disposition")
    ordered = sorted(
        reconciled, key=lambda item: expected_ids.index(item["finding_id"])
    )
    return {
        "schema_version": "1.0",
        "artifact_type": "evidence_record",
        "artifact_subtype": "review_report",
        "report_id": validated["report_id"],
        "report_sha256": validated["report_sha256"],
        "reconciled_at": candidate["reconciled_at"],
        "llm_session_ids": candidate["llm_session_ids"],
        "findings": ordered,
        "reopen_proof": sorted(
            {proof for item in ordered for proof in item.get("reopen_proof", [])}
        ),
        "implementation_authorized": False,
    }


def write_reconciliation(root: Path, output: Path, result: dict[str, Any]) -> Path:
    """Write reconciliation using the declared repository contract."""
    root = root.resolve()
    target = output.resolve()
    try:
        target.relative_to(root)
    except ValueError as error:
        raise ValueError(
            "reconciliation output must remain inside the repository"
        ) from error
    return _write_new(target, json.dumps(result, indent=2, sort_keys=True) + "\n")


def _validate_packet(root: Path, packet: dict[str, Any]) -> None:
    """Validate packet using the declared repository contract."""
    required = {
        "schema_version",
        "artifact_type",
        "artifact_id",
        "packet_id",
        "repository",
        "commit",
        "scope",
        "criteria",
        "reviewed_inputs",
        "resolved_rules",
        "allowed_effects",
    }
    if set(packet) != required or packet.get("schema_version") != "1.0":
        raise ValueError("review packet envelope is invalid")
    if packet.get("artifact_type") != "plan":
        raise ValueError("review packet must be classified as a plan")
    if packet.get("allowed_effects") != ["read_only_report"]:
        raise ValueError("review packet may authorize only a read-only report")
    if packet.get("repository") != _repository_identity(root):
        raise ValueError("review packet repository does not match the project")
    if not isinstance(packet.get("commit"), str) or not SHA_PATTERN.fullmatch(
        str(packet["commit"])
    ):
        raise ValueError("review packet requires an exact commit")
    reviewed_inputs = packet.get("reviewed_inputs")
    if not isinstance(reviewed_inputs, list) or not reviewed_inputs:
        raise ValueError("review packet requires exact input identities")
    for item in reviewed_inputs:
        if not _valid_identity(item, with_id=False):
            raise ValueError("review packet input identity is invalid")
    resolved_rules = packet.get("resolved_rules")
    if not isinstance(resolved_rules, list) or not resolved_rules:
        raise ValueError("review packet requires resolved governing rules")
    for item in resolved_rules:
        if not _valid_identity(item, with_id=True):
            raise ValueError("review packet rule identity is invalid")


def _validate_report(
    packet: dict[str, Any],
    report: dict[str, Any],
    body: str,
    allowed_priorities: set[str],
) -> None:
    """Validate report using the declared repository contract."""
    required = {
        "schema_version",
        "artifact_type",
        "artifact_subtype",
        "artifact_id",
        "packet_id",
        "priority",
        "reviewer",
        "llm_session_ids",
        "reviewed_commit",
        "reviewed_inputs",
        "method",
        "observed_at",
        "limitations",
        "findings",
    }
    if set(report) != required or report.get("schema_version") != "1.0":
        raise ValueError("review report envelope is invalid")
    if (report.get("artifact_type"), report.get("artifact_subtype")) != (
        "evidence_record",
        "review_report",
    ):
        raise ValueError("review report classification is invalid")
    if report.get("packet_id") != packet.get("packet_id"):
        raise ValueError("review report packet_id does not match")
    if report.get("reviewed_commit") != packet.get("commit"):
        raise ValueError("review report commit does not match the packet")
    if report.get("reviewed_inputs") != packet.get("reviewed_inputs"):
        raise ValueError("review report inputs do not match the packet")
    if report.get("priority") not in allowed_priorities:
        raise ValueError("review report priority is invalid")
    reviewer = report.get("reviewer")
    reviewer_keys = {"identity", "host", "model", "tool_version"}
    if not isinstance(reviewer, dict) or set(reviewer) != reviewer_keys:
        raise ValueError("reviewer identity envelope is invalid")
    if any(
        not isinstance(value, str) or not value.strip() for value in reviewer.values()
    ):
        raise ValueError("reviewer identity values must be non-empty")
    _sessions(report.get("llm_session_ids"))
    if not isinstance(report.get("method"), str) or not report["method"].strip():
        raise ValueError("review report method is required")
    _datetime(str(report.get("observed_at")), "observed_at")
    limitations = report.get("limitations")
    if not isinstance(limitations, list) or not all(
        isinstance(item, str) and item.strip() for item in limitations
    ):
        raise ValueError("review report limitations must be an explicit list")
    findings = report.get("findings")
    if not isinstance(findings, list):
        raise ValueError("review report findings must be a list")
    finding_ids: list[str] = []
    for finding in findings:
        _validate_finding(finding, allowed_priorities)
        assert isinstance(finding, dict)
        finding_ids.append(str(finding["id"]))
    if len(finding_ids) != len(set(finding_ids)):
        raise ValueError("review finding IDs must be unique")
    if not body.strip():
        raise ValueError("review report requires a findings body")


def _validate_finding(finding: object, allowed_priorities: set[str]) -> None:
    """Validate finding using the declared repository contract."""
    fields = {
        "id",
        "priority",
        "evidence",
        "confidence",
        "impact",
        "proposed_disposition",
    }
    if not isinstance(finding, dict) or set(finding) != fields:
        raise ValueError("review finding envelope is invalid")
    identifier = finding.get("id")
    if not isinstance(identifier, str) or not FINDING_PATTERN.fullmatch(identifier):
        raise ValueError("review finding ID is invalid")
    if finding.get("priority") not in allowed_priorities:
        raise ValueError("review finding priority is invalid")
    if finding.get("confidence") not in {"low", "medium", "high"}:
        raise ValueError("review finding confidence is invalid")
    if finding.get("proposed_disposition") not in DISPOSITIONS:
        raise ValueError("review finding proposed disposition is invalid")
    for key in ("evidence", "impact"):
        if not isinstance(finding.get(key), str) or not finding[key].strip():
            raise ValueError(f"review finding {key} is required")


def _validate_disposition(value: object) -> dict[str, Any]:
    """Validate disposition using the declared repository contract."""
    if not isinstance(value, dict):
        raise ValueError("every reconciliation finding must be an object")
    allowed = {
        "finding_id",
        "disposition",
        "rationale",
        "target_id",
        "reopen_proof",
    }
    if not set(value).issubset(allowed):
        raise ValueError("reconciliation finding contains unknown fields")
    finding_id = value.get("finding_id")
    disposition = value.get("disposition")
    rationale = value.get("rationale")
    if not isinstance(finding_id, str) or not FINDING_PATTERN.fullmatch(finding_id):
        raise ValueError("reconciliation finding_id is invalid")
    if disposition not in DISPOSITIONS:
        raise ValueError("reconciliation disposition is invalid")
    if not isinstance(rationale, str) or not rationale.strip():
        raise ValueError("every reconciliation disposition requires rationale")
    routed = str(disposition).startswith("route_")
    target_id = value.get("target_id")
    valid_target = isinstance(target_id, str) and bool(ID_PATTERN.fullmatch(target_id))
    if routed != valid_target:
        raise ValueError("routed findings require one canonical target_id")
    reopen = value.get("reopen_proof", [])
    if not isinstance(reopen, list) or not all(
        isinstance(item, str) and ID_PATTERN.fullmatch(item) for item in reopen
    ):
        raise ValueError("reopen_proof must contain canonical IDs")
    result = {
        "finding_id": finding_id,
        "disposition": disposition,
        "rationale": rationale,
        "reopen_proof": sorted(set(reopen)),
    }
    if routed:
        result["target_id"] = target_id
    return result


def _read_markdown(path: Path) -> tuple[dict[str, Any], str]:
    """Read markdown using the declared repository contract."""
    try:
        parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
    except FrontmatterError as error:
        raise ValueError(
            f"review artifact frontmatter is invalid: {path}: {error}"
        ) from error
    if parsed is None:
        raise ValueError(f"review artifact requires TOML or YAML frontmatter: {path}")
    data, body, _format = parsed
    return data, body


def _file_identity(root: Path, raw: str) -> dict[str, str]:
    candidate = find_unique_name(root, raw)
    return {"carrier": candidate.name, "sha256": _sha256(candidate)}


def _valid_identity(value: object, *, with_id: bool) -> bool:
    """Handle identity using the declared repository contract."""
    if not isinstance(value, dict):
        return False
    fields = {"carrier", "sha256"}
    if with_id:
        fields.add("id")
    if set(value) != fields:
        return False
    carrier = value.get("carrier")
    digest = value.get("sha256")
    identifier = value.get("id")
    return (
        isinstance(carrier, str)
        and bool(carrier)
        and Path(carrier).name == carrier
        and isinstance(digest, str)
        and bool(re.fullmatch(r"[0-9a-f]{64}", digest))
        and (
            not with_id
            or (isinstance(identifier, str) and bool(ID_PATTERN.fullmatch(identifier)))
        )
    )


def _repository_identity(root: Path) -> str:
    """Handle identity using the declared repository contract."""
    manifest = load(discover_layout(root).manifest_path)
    project = manifest.get("project", {}) if isinstance(manifest, dict) else {}
    value = project.get("repository_slug") or project.get("id")
    if not isinstance(value, str) or not value:
        raise ValueError("project manifest requires repository identity")
    return value


def _head(root: Path) -> str:
    """Handle head using the declared repository contract."""
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    value = completed.stdout.strip()
    if completed.returncode or not SHA_PATTERN.fullmatch(value):
        raise ValueError("review packet requires a Git repository with an exact HEAD")
    return value


def _sessions(value: object) -> None:
    """Handle sessions using the declared repository contract."""
    if not isinstance(value, list) or len(value) != len(set(map(str, value))):
        raise ValueError("llm_session_ids must be a unique list")
    if not all(
        isinstance(item, str) and SESSION_PATTERN.fullmatch(item) for item in value
    ):
        raise ValueError("llm_session_ids must use host-prefixed identities")


def _datetime(value: str, field: str) -> None:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{field} must be an ISO 8601 timestamp") from error


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _markdown(metadata: dict[str, Any], title: str, body: str) -> str:
    return render_frontmatter(metadata, f"\n# {title}\n\n{body.rstrip()}\n")


def _packet_body() -> str:
    return (
        "Review only the exact commit, input digests, rules, scope, and criteria "
        "in the envelope. Return a report; do not edit the project or authorize repair."
    )


def _write_new(path: Path, content: str) -> Path:
    """Write new using the declared repository contract."""
    path = path.resolve()
    if path.exists():
        raise FileExistsError(f"refusing existing review artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path
