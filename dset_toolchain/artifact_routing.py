"""Route governed artifacts through independent, type-free coordinates."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final

# REVISION_MODES defines how a governed artifact may change.
REVISION_MODES: Final[tuple[str, ...]] = ("atomic", "evergreen", "maintained")
# CONTENT_ROLES defines the artifact contribution and canonical loop order.
CONTENT_ROLES: Final[tuple[str, ...]] = (
    "inquiry",
    "definition",
    "rationale",
    "method",
    "implementation",
    "observation",
)
# GOVERNANCE_ORIGINS defines who controls semantic content and currentness.
GOVERNANCE_ORIGINS: Final[tuple[str, ...]] = ("internal", "external")
# RELATION_SHAPES defines whether primary meaning needs role-bearing endpoints.
RELATION_SHAPES: Final[tuple[str, ...]] = ("standalone", "relational")
# SCOPE_SEGMENT validates one extensible structural path segment.
SCOPE_SEGMENT: Final[re.Pattern[str]] = re.compile(
    r"^[a-z][a-z0-9_-]*:[A-Za-z0-9][A-Za-z0-9._-]*$"
)
# RELATION_TOKEN validates relation and endpoint-role vocabulary.
RELATION_TOKEN: Final[re.Pattern[str]] = re.compile(
    r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$"
)


@dataclass(frozen=True)
class ArtifactEndpoint:
    """Represent one role-bearing endpoint of a relational artifact."""

    role: str
    target: str
    origin: str


@dataclass(frozen=True)
class ArtifactRoute:
    """Represent one complete deterministic artifact route."""

    revision_mode: str
    content_role: str
    governance_origin: str
    relation_shape: str
    scope_path: tuple[str, ...]
    relation_kind: str | None = None
    endpoints: tuple[ArtifactEndpoint, ...] = ()

    @property
    def key(self) -> str:
        """Return the stable machine routing key."""
        return ".".join(
            (
                self.revision_mode,
                self.content_role,
                self.governance_origin,
                self.relation_shape,
            )
        )

    @property
    def name(self) -> str:
        """Return the one canonical human name for this complete route."""
        words = (
            self.governance_origin,
            self.revision_mode,
            self.content_role,
            "relation" if self.relation_shape == "relational" else "artifact",
        )
        return " ".join(word.replace("_", " ").title() for word in words)

    def as_dict(self) -> dict[str, Any]:
        """Render the route without introducing Type or subtype fields."""
        rendered: dict[str, Any] = {
            "key": self.key,
            "name": self.name,
            "revision_mode": self.revision_mode,
            "content_role": self.content_role,
            "governance_origin": self.governance_origin,
            "relation_shape": self.relation_shape,
            "scope_path": list(self.scope_path),
        }
        if self.relation_kind is not None:
            rendered["relation_kind"] = self.relation_kind
            rendered["endpoints"] = [
                {
                    "role": endpoint.role,
                    "target": endpoint.target,
                    "origin": endpoint.origin,
                }
                for endpoint in self.endpoints
            ]
        return rendered


def parse_artifact_route(metadata: Mapping[str, Any]) -> ArtifactRoute:
    """Parse and validate one explicit route from artifact metadata."""
    issues = route_issues(metadata)
    if issues:
        raise ValueError("; ".join(issues))
    relation_shape = str(metadata["relation_shape"])
    return ArtifactRoute(
        revision_mode=str(metadata["revision_mode"]),
        content_role=str(metadata["content_role"]),
        governance_origin=str(metadata["governance_origin"]),
        relation_shape=relation_shape,
        scope_path=tuple(str(item) for item in metadata["scope_path"]),
        relation_kind=(
            str(metadata["relation_kind"]) if relation_shape == "relational" else None
        ),
        endpoints=(
            tuple(_endpoint(item) for item in metadata["endpoints"])
            if relation_shape == "relational"
            else ()
        ),
    )


def route_issues(metadata: Mapping[str, Any]) -> list[str]:
    """Return deterministic validation issues for one route candidate."""
    issues: list[str] = []
    _allowed(metadata, "revision_mode", REVISION_MODES, issues)
    _allowed(metadata, "content_role", CONTENT_ROLES, issues)
    _allowed(metadata, "governance_origin", GOVERNANCE_ORIGINS, issues)
    _allowed(metadata, "relation_shape", RELATION_SHAPES, issues)
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
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not SCOPE_SEGMENT.fullmatch(item) for item in value)
    ):
        issues.append("scope_path must be a non-empty list of kind:id segments")
        return
    normalized = [str(item) for item in value]
    if len(normalized) != len(set(normalized)):
        issues.append("scope_path segments must be unique")


def _relation_issues(metadata: Mapping[str, Any], issues: list[str]) -> None:
    shape = metadata.get("relation_shape")
    kind = metadata.get("relation_kind")
    endpoints = metadata.get("endpoints")
    if shape == "standalone":
        if kind is not None or endpoints is not None:
            issues.append("standalone routes must not declare relation_kind or endpoints")
        return
    if shape != "relational":
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
        target = item.get("target")
        origin = item.get("origin")
        if not isinstance(role, str) or not RELATION_TOKEN.fullmatch(role):
            issues.append(f"endpoints[{index}].role must be a snake_case token")
        if not isinstance(target, str) or not target.strip():
            issues.append(f"endpoints[{index}].target must be a non-empty identity")
        if origin not in GOVERNANCE_ORIGINS:
            issues.append(
                f"endpoints[{index}].origin must be internal or external"
            )


def _endpoint(value: object) -> ArtifactEndpoint:
    assert isinstance(value, Mapping)
    return ArtifactEndpoint(
        role=str(value["role"]),
        target=str(value["target"]),
        origin=str(value["origin"]),
    )
