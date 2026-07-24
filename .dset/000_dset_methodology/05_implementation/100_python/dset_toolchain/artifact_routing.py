"""Resolve governed artifact routes from registered types or legacy fields."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final

# REVISION_MODES defines how a governed artifact may change.
REVISION_MODES: Final[tuple[str, ...]] = ("atomic", "append_only", "maintained")
# CONTENT_ROLES defines the artifact contribution and canonical loop order.
CONTENT_ROLES: Final[tuple[str, ...]] = (
    "inquiry",
    "analysis",
    "definition",
    "method",
    "implementation",
    "observation",
)
# GOVERNANCE_LOCI define internal, external, and relational governance.
GOVERNANCE_LOCI: Final[tuple[str, ...]] = ("internal", "external", "relation")
# ENDPOINT_ORIGINS define independently declared relation endpoint origins.
ENDPOINT_ORIGINS: Final[tuple[str, ...]] = ("internal", "external")
# SCOPE_SEGMENT validates one extensible structural path segment.
SCOPE_SEGMENT: Final[re.Pattern[str]] = re.compile(
    r"^[a-z][a-z0-9_-]*:[A-Za-z0-9][A-Za-z0-9._-]*$"
)
# RELATION_TOKEN validates relation and endpoint-role vocabulary.
RELATION_TOKEN: Final[re.Pattern[str]] = re.compile(
    r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$"
)
# TYPE_ROUTES maps one registered type pair to one complete semantic route.
TYPE_ROUTES: Final[
    dict[tuple[str, str | None], tuple[str, str, str]]
] = {
    ("requirement", None): ("atomic", "definition", "internal"),
    ("constraint", None): ("atomic", "definition", "external"),
    ("contract", None): ("atomic", "definition", "relation"),
    ("implementation_decision", None): ("atomic", "method", "internal"),
    ("question", None): ("atomic", "inquiry", "internal"),
    ("question", "risk"): ("atomic", "inquiry", "internal"),
    ("question", "opportunity"): ("atomic", "inquiry", "internal"),
    ("question", "conflict"): ("atomic", "inquiry", "relation"),
    ("problem", None): ("atomic", "observation", "internal"),
    ("problem", "defect"): ("atomic", "observation", "internal"),
    ("problem", "gap"): ("atomic", "observation", "internal"),
    ("problem", "debt"): ("atomic", "observation", "internal"),
    ("test_plan", None): ("atomic", "method", "internal"),
    ("evaluation_plan", None): ("atomic", "method", "internal"),
    ("rationale", None): ("atomic", "analysis", "internal"),
    ("analysis_report", None): ("atomic", "analysis", "internal"),
    ("analysis_report", "solution_landscape"): (
        "atomic",
        "analysis",
        "internal",
    ),
    ("analysis_report", "root_cause_analysis"): (
        "atomic",
        "analysis",
        "internal",
    ),
    ("analysis_report", "proposal"): ("atomic", "analysis", "internal"),
    ("analysis_report", "technical_investigation"): (
        "atomic",
        "analysis",
        "internal",
    ),
    ("analysis_report", "external_audit_analysis"): (
        "atomic",
        "analysis",
        "internal",
    ),
    ("evidence_record", None): ("atomic", "observation", "internal"),
    ("evidence_record", "test_result"): (
        "atomic",
        "observation",
        "internal",
    ),
    ("evidence_record", "evaluation_result"): (
        "atomic",
        "observation",
        "internal",
    ),
    ("evidence_record", "review_report"): (
        "atomic",
        "observation",
        "internal",
    ),
    ("evidence_record", "run_record"): (
        "atomic",
        "observation",
        "internal",
    ),
}


@dataclass(frozen=True)
class ArtifactEndpoint:
    """Represent one role-bearing endpoint of a relational artifact."""

    role: str
    identity: str
    origin: str


@dataclass(frozen=True)
class ArtifactRoute:
    """Represent one complete deterministic artifact route."""

    revision_mode: str
    content_role: str
    governance_locus: str
    scope_path: tuple[str, ...]
    relation_kind: str | None = None
    endpoints: tuple[ArtifactEndpoint, ...] = ()

    @property
    def relational(self) -> bool:
        """Return whether this route governs an explicit relation."""
        return self.governance_locus == "relation"

    @property
    def key(self) -> str:
        """Return the stable machine routing key."""
        return ".".join(
            (
                self.revision_mode,
                self.content_role,
                self.governance_locus,
            )
        )

    @property
    def name(self) -> str:
        """Return the one canonical human name for this complete route."""
        words = (self.governance_locus, self.revision_mode, self.content_role)
        return " ".join(word.replace("_", " ").title() for word in words)

    def as_dict(self) -> dict[str, Any]:
        """Render the route without introducing Type or subtype fields."""
        rendered: dict[str, Any] = {
            "key": self.key,
            "name": self.name,
            "revision_mode": self.revision_mode,
            "content_role": self.content_role,
            "governance_locus": self.governance_locus,
            "scope_path": list(self.scope_path),
        }
        if self.relation_kind is not None:
            rendered["relation_kind"] = self.relation_kind
            rendered["endpoints"] = [
                {
                    "role": endpoint.role,
                    "identity": endpoint.identity,
                    "origin": endpoint.origin,
                }
                for endpoint in self.endpoints
            ]
        return rendered


def parse_artifact_route(metadata: Mapping[str, Any]) -> ArtifactRoute:
    """Resolve a registered type route or parse a legacy explicit route."""
    issues = route_issues(metadata)
    if issues:
        raise ValueError("; ".join(issues))
    resolved = type_route(metadata)
    if resolved is None:
        revision_mode = str(metadata["revision_mode"])
        content_role = str(metadata["content_role"])
        governance_locus = str(metadata["governance_locus"])
    else:
        revision_mode, content_role, governance_locus = resolved
    return ArtifactRoute(
        revision_mode=revision_mode,
        content_role=content_role,
        governance_locus=governance_locus,
        scope_path=tuple(str(item) for item in metadata["scope_path"]),
        relation_kind=(
            str(metadata["relation_kind"])
            if governance_locus == "relation"
            else None
        ),
        endpoints=(
            tuple(_endpoint(item) for item in metadata["endpoints"])
            if governance_locus == "relation"
            else ()
        ),
    )


def route_issues(metadata: Mapping[str, Any]) -> list[str]:
    """Return deterministic validation issues for one route candidate."""
    issues: list[str] = []
    resolved = type_route(metadata)
    if resolved is not None:
        repeated = sorted(
            {
                "revision_mode",
                "content_role",
                "governance_locus",
                "governance_origin",
                "relation_shape",
            }.intersection(metadata)
        )
        if repeated:
            issues.append("derived route fields must be omitted: " + ", ".join(repeated))
        _scope_issues(metadata.get("scope_path"), issues)
        _relation_issues_for_locus(metadata, resolved[2], issues)
        return issues
    if isinstance(metadata.get("artifact_type"), str):
        issues.append("artifact_type and artifact_subtype do not map to one route")
        return issues
    _allowed(metadata, "revision_mode", REVISION_MODES, issues)
    _allowed(metadata, "content_role", CONTENT_ROLES, issues)
    _allowed(metadata, "governance_locus", GOVERNANCE_LOCI, issues)
    _scope_issues(metadata.get("scope_path"), issues)
    _relation_issues(metadata, issues)
    retired = sorted(
        {"artifact_type", "artifact_subtype", "type", "subtype"}.intersection(metadata)
    )
    if retired:
        issues.append(
            "Type/subtype metadata is not part of routing: " + ", ".join(retired)
        )
    return issues


def type_route(metadata: Mapping[str, Any]) -> tuple[str, str, str] | None:
    """Return the route registered for one type pair."""
    artifact_type = metadata.get("artifact_type")
    subtype = metadata.get("artifact_subtype")
    if not isinstance(artifact_type, str):
        return None
    key = (
        artifact_type,
        str(subtype) if isinstance(subtype, str) else None,
    )
    return TYPE_ROUTES.get(key)


def _allowed(
    metadata: Mapping[str, Any],
    field: str,
    allowed: Sequence[str],
    issues: list[str],
) -> None:
    value = metadata.get(field)
    if value not in allowed:
        issues.append(f"{field} must be one of: {', '.join(allowed)}")


def _scope_issues(value: object, issues: list[str]) -> None:
    if not isinstance(value, list):
        issues.append("scope_path must be a list of kind:id segments")
        return
    if any(
        not isinstance(item, str) or not SCOPE_SEGMENT.fullmatch(item)
        for item in value
    ):
        issues.append("scope_path must contain only kind:id segments")
        return
    normalized = [str(item) for item in value]
    if any(item.startswith("project:") for item in normalized):
        issues.append("scope_path must not repeat the ambient project identity")
    if len(normalized) != len(set(normalized)):
        issues.append("scope_path segments must be unique")


def _relation_issues(metadata: Mapping[str, Any], issues: list[str]) -> None:
    locus = metadata.get("governance_locus")
    kind = metadata.get("relation_kind")
    endpoints = metadata.get("endpoints")
    if locus in {"internal", "external"}:
        if kind is not None or endpoints is not None:
            issues.append(
                "non-relational routes must not declare relation_kind or endpoints"
            )
        return
    if locus != "relation":
        return
    if not isinstance(kind, str) or not RELATION_TOKEN.fullmatch(kind):
        issues.append("relational routes require a snake_case relation_kind")
    if not isinstance(endpoints, list) or len(endpoints) < 2:
        issues.append("relational routes require at least two endpoints")
        return
    for index, item in enumerate(endpoints):
        if not isinstance(item, Mapping):
            issues.append(f"endpoints[{index}] must be a table")
            continue
        role = item.get("role")
        identity = item.get("identity")
        origin = item.get("origin")
        if not isinstance(role, str) or not RELATION_TOKEN.fullmatch(role):
            issues.append(f"endpoints[{index}].role must be a snake_case token")
        if not isinstance(identity, str) or not identity.strip():
            issues.append(
                f"endpoints[{index}].identity must be a non-empty identity"
            )
        if origin not in ENDPOINT_ORIGINS:
            issues.append(
                f"endpoints[{index}].origin must be internal or external"
            )


def _relation_issues_for_locus(
    metadata: Mapping[str, Any],
    locus: str,
    issues: list[str],
) -> None:
    projected = dict(metadata)
    projected["governance_locus"] = locus
    _relation_issues(projected, issues)


def _endpoint(value: object) -> ArtifactEndpoint:
    assert isinstance(value, Mapping)
    return ArtifactEndpoint(
        role=str(value["role"]),
        identity=str(value["identity"]),
        origin=str(value["origin"]),
    )
