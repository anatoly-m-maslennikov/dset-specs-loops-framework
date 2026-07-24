#!/usr/bin/env python3
"""Safely migrate the root META/GOV methodology to job-specific carriers.

Parameters:
  ROOT: repository root, defaulting to the parent of this script.
  --apply: execute the fully validated plan; omission is a dry run.
  --check: verify the post-migration invariants without writing.

The migration is intentionally bounded to ``11_layer_meta`` and
``12_layer_gov``. It converts Markdown property blocks to YAML, adds explicit
YAML properties where a Markdown artifact has none, and converts JSON Schema
documents encoded as TOML to canonical JSON. Human-edited configuration remains
TOML. Any unrecognized structure, parse failure, symlink, target collision,
preimage change, or postcondition failure aborts the operation.
"""

# ruff: noqa: E402, E501

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomllib

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from dset_toolchain.frontmatter import (  # noqa: E402
    FrontmatterError,
)
from dset_toolchain.frontmatter import (
    parse as parse_frontmatter,
)
from dset_toolchain.frontmatter import (
    render as render_frontmatter,
)

MIGRATION_ROOTS = ("11_layer_meta", "12_layer_gov")
SCHEMA_SUFFIX = ".schema.toml"
JSON_SCHEMA_SUFFIX = ".schema.json"
CONFIGURATION_TOML_NAMES = {
    "010_dset-meta-templates-dset-settings.toml",
    "000_dset-meta-templates-package-layered-package.toml",
    "030_dset-gov-templates-change-dependency-map.toml",
    "000_dset-gov-templates-change-layered-change.toml",
    "040_dset-gov-templates-governance-core-v1-profile.toml",
    "060_dset-gov-templates-profiles.toml",
}
IGNORED_HOST_FILES = {".DS_Store"}
GOV_POLICY_SECTION_START = (
    "## DSET-REQUIREMENT-GOV-040 — Project settings are verbose "
    "and all DSET artifacts use TOML\n"
)
GOV_POLICY_SECTION_END = (
    "## DSET-DECISION-GOV-014 — TOML null normalization is allowlisted\n"
)
GOV_POLICY_SECTION = """## DSET-REQUIREMENT-GOV-040 — Project settings are verbose

The canonical settings and project-manifest carrier is
`.dset/dset_settings.toml`. It must explain its boundary with governing
documents, every setting, every accepted value, the behavior each value
selects, the default, and practical examples. New writers and bootstraps emit
only this path. Retired root settings and split manifests are read-only
migration inputs; if competing carriers exist, validation stops.

Settings own operator-selectable behavior: artifact subtype naming,
medium/high artifact-creation strictness, lazy/strict implementation
preparation, integration-branch/branch-worktree Change workspace selection,
low/medium/high delegation budget selection, and the priority scale/default.
The manifest section owns identity, repository and Work Area structure,
runtime-risk and durability topology, external contracts, release targets,
verification commands, and commit-provenance boundaries. Governing documents
own definitions and policy; settings select registered behavior only.

**Scenario DSET-SCENARIO-GOV-037:** A cold reader opens
`.dset/dset_settings.toml`, finds every operator choice and predicts its effect,
and reads the same carrier for runtime topology and release truth. Bootstrap
emits only the canonical path; a repository containing competing settings
carriers fails.

## DSET-REQUIREMENT-GOV-097 — Select artifact carriers by their actual job

One concern has one canonical carrier selected by its job:

| Carrier | Canonical use |
|---|---|
| Markdown with YAML frontmatter | Human-governed artifacts with narrative meaning |
| TOML | Human-edited configuration executed directly by tools |
| JSON | External contracts, standardized schemas, wire data, and generated machine data |
| JSONL/NDJSON | Append-only runtime logs and event streams |
| Native format | Source code, CI workflows, lockfiles, and host manifests |

Markdown with restricted, GitHub-compatible YAML frontmatter is the default for
atomic, evergreen, analysis, evidence, verification, navigation, plan, and
other human-governed narrative artifacts. TOML is not a generic structured-data
default; it owns settings and configuration that tools execute directly.
Standards-compliant JSON Schema remains canonical JSON. JSONL/NDJSON is reserved
for append-only runtime records, and implementation ecosystems retain their
native formats.

Migration inventories and validates every source before writing, refuses
unknown structures and collisions, preserves semantic values and narrative
bodies, stages outputs outside the repository, checks exact preimages, rewrites
in-scope references, validates the complete bounded result, and rolls back every
touched file on failure. A second run is a no-op.

**Scenario DSET-SCENARIO-GOV-038:** A dry run classifies every in-scope carrier
and reports its exact operation. Apply leaves every narrative Markdown artifact
with YAML frontmatter, every JSON Schema as JSON, every executable human-edited
configuration as TOML, and no competing editable representation of one concern.

`DSET-REQUIREMENT-GOV-036` and the universal-TOML clause formerly compiled
under `DSET-REQUIREMENT-GOV-040` are historical. The verbose-settings clause of
`DSET-REQUIREMENT-GOV-040` remains active; carrier selection is governed by
`DSET-REQUIREMENT-GOV-097`.

## Historical DSET-DECISION-GOV-014 — TOML null normalization is allowlisted
"""
MAINTENANCE_OLD = """- Use TOML for DSET-owned structured artifacts and TOML frontmatter for DSET
  Markdown. Keep host/ecosystem/wire/runtime formats and generated compatibility
  adapters explicit and non-authoritative. Never keep editable YAML/JSON and
  TOML copies of the same claim.
- Keep standards-compliant JSON Schema files as canonical external contract
  carriers. Validate and retain them as JSON; do not create an editable TOML
  duplicate or call them generated without a governed source and freshness map.
"""
MAINTENANCE_NEW = """- Select one canonical carrier by job: Markdown with YAML frontmatter for
  human-governed narrative artifacts; TOML for directly executed human-edited
  configuration; JSON for external contracts, standardized schemas, wire data,
  and generated machine data; JSONL/NDJSON for append-only runtime records; and
  native formats for source code, CI, lockfiles, and host manifests.
- Keep standards-compliant JSON Schema files as canonical JSON. Never keep
  competing editable representations of one concern.
"""
DOMAIN_INVARIANT_OLD = (
    "- **DSET-INVARIANT-GOV-026:** Every DSET-owned structured artifact has one "
    "canonical TOML encoding. Markdown uses TOML frontmatter. Generated adapters "
    "and host/ecosystem/wire/runtime formats are explicit non-authoritative "
    "boundaries, never parallel writable sources. Migration preserves values, "
    "IDs, references, and provenance or fails before cutover."
)
DOMAIN_INVARIANT_NEW = (
    "- **DSET-INVARIANT-GOV-026:** Every governed concern has one canonical "
    "carrier selected by job: Markdown with YAML frontmatter for human-governed "
    "narrative artifacts; TOML for directly executed human-edited configuration; "
    "JSON for external contracts, standardized schemas, wire data, and generated "
    "machine data; JSONL/NDJSON for append-only runtime records; and native "
    "formats for source code, CI, lockfiles, and host manifests. Competing "
    "editable representations fail, and migration preserves meaning or stops "
    "before cutover."
)


class MigrationError(RuntimeError):
    """The carrier migration cannot proceed without guessing or data loss."""


@dataclass(frozen=True)
class WriteOperation:
    """One exact file replacement or creation."""

    path: Path
    before_sha256: str | None
    content: bytes
    reason: str


@dataclass(frozen=True)
class DeleteOperation:
    """One exact file deletion after its replacement has been staged."""

    path: Path
    before_sha256: str
    reason: str


@dataclass(frozen=True)
class MigrationPlan:
    """A complete fail-closed set of carrier operations."""

    root: Path
    writes: tuple[WriteOperation, ...]
    deletes: tuple[DeleteOperation, ...]

    def summary(self) -> str:
        """Render a stable human-readable dry-run summary."""
        lines = [
            "META/GOV carrier migration plan",
            f"root: {self.root}",
            f"writes: {len(self.writes)}",
            f"deletes: {len(self.deletes)}",
        ]
        for operation in self.writes:
            relative = operation.path.relative_to(self.root).as_posix()
            verb = "CREATE" if operation.before_sha256 is None else "UPDATE"
            lines.append(f"{verb} {relative} — {operation.reason}")
        for operation in self.deletes:
            relative = operation.path.relative_to(self.root).as_posix()
            lines.append(f"DELETE {relative} — {operation.reason}")
        return "\n".join(lines)


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _read_regular_file(path: Path) -> bytes:
    if path.is_symlink():
        raise MigrationError(f"symlink is outside the migration contract: {path}")
    if not path.is_file():
        raise MigrationError(f"expected a regular file: {path}")
    return path.read_bytes()


def _scope_path(path: Path) -> list[str]:
    if path.parts[0] == "11_layer_meta":
        return ["layer:meta"]
    if path.parts[0] == "12_layer_gov":
        return ["layer:gov"]
    raise MigrationError(f"path is outside META/GOV: {path}")


def _document_metadata(relative: Path) -> dict[str, Any]:
    """Classify a non-template methodology document without guessing."""
    name = relative.name
    scope_path = _scope_path(relative)
    if "hub" in name:
        return {
            "artifact_type": "navigation",
            "artifact_subtype": "hub",
            "scope_path": scope_path,
            "priority": "medium",
        }
    if "navigation" in name:
        return {
            "artifact_type": "navigation",
            "artifact_subtype": "index",
            "scope_path": scope_path,
            "priority": "medium",
        }
    if "procedure" in name or "guides-" in name:
        return {
            "artifact_type": "procedure",
            "artifact_subtype": "playbook",
            "scope_path": scope_path,
            "priority": "medium",
        }
    if "specification-" in name:
        subtype_by_subject = {
            "architecture": "architecture",
            "artifact-classification": "governance",
            "artifact-maintenance": "governance",
            "contracts": "behavior",
            "domain": "domain_model",
            "methodology": "governance",
            "outcomes": "behavior",
            "user-stories": "behavior",
            "work-items": "governance",
        }
        matches = [
            subtype
            for subject, subtype in subtype_by_subject.items()
            if f"specification-{subject}" in name
        ]
        if len(matches) != 1:
            raise MigrationError(
                f"unrecognized or ambiguous specification subject: {relative}"
            )
        return {
            "artifact_type": "specification",
            "artifact_subtype": matches[0],
            "scope_path": scope_path,
            "priority": "high",
        }
    raise MigrationError(f"unrecognized Markdown artifact: {relative}")


def _template_metadata(relative: Path) -> dict[str, Any]:
    """Classify the artifact emitted from a Markdown template."""
    name = relative.name
    if "hub" in name:
        return {
            "artifact_type": "navigation",
            "artifact_subtype": "hub",
            "scope_path": [],
            "priority": "medium",
        }

    exact_routes: tuple[tuple[str, str, str | None], ...] = (
        ("domain-spec-authoring", "procedure", "playbook"),
        ("eval-planning", "procedure", "playbook"),
        ("test-planning", "procedure", "playbook"),
        ("package-contracts", "specification", "behavior"),
        ("package-domain", "specification", "domain_model"),
        ("package-eval-plan", "plan", "evaluation_plan"),
        ("package-outcomes", "specification", "behavior"),
        ("package-spec", "specification", "behavior"),
        ("package-stories", "specification", "behavior"),
        ("package-test-plan", "plan", "test_plan"),
        ("change-adoption-decision", "implementation_decision", None),
        ("change-decision", "implementation_decision", None),
        ("change-design", "specification", "design"),
        ("change-eval-plan", "plan", "evaluation_plan"),
        ("change-global-impact", "analysis_report", None),
        ("change-implementation-plan", "plan", "implementation_plan"),
        ("change-specs-package", "specification", "behavior"),
        ("change-tasks", "plan", "implementation_plan"),
        ("change-test-plan", "plan", "test_plan"),
        ("change-verification", "verification", None),
        ("governance-core-v1-architecture", "specification", "architecture"),
        (
            "governance-core-v1-artifact-classification",
            "specification",
            "governance",
        ),
        (
            "governance-core-v1-artifact-maintenance",
            "specification",
            "governance",
        ),
        ("governance-core-v1-work-items", "specification", "governance"),
    )
    matches = [
        (artifact_type, artifact_subtype)
        for token, artifact_type, artifact_subtype in exact_routes
        if token in name
    ]
    if len(matches) != 1:
        raise MigrationError(f"unrecognized or ambiguous Markdown template: {relative}")
    artifact_type, artifact_subtype = matches[0]
    metadata: dict[str, Any] = {
        "artifact_type": artifact_type,
        "scope_path": [],
        "priority": "medium",
    }
    if artifact_subtype is not None:
        metadata["artifact_subtype"] = artifact_subtype
    if artifact_type in {"implementation_decision", "analysis_report"}:
        metadata["artifact_id"] = "{{semantic_artifact_id}}"
        metadata["llm_session_ids"] = []
    return metadata


def _new_markdown_metadata(relative: Path) -> dict[str, Any]:
    if any(part.endswith("_templates") for part in relative.parts):
        return _template_metadata(relative)
    return _document_metadata(relative)


def _normalized_markdown(relative: Path, content: bytes) -> bytes:
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise MigrationError(f"Markdown is not UTF-8: {relative}") from error
    try:
        parsed = parse_frontmatter(text)
    except FrontmatterError as error:
        raise MigrationError(f"invalid frontmatter in {relative}: {error}") from error
    if parsed is None:
        metadata = _new_markdown_metadata(relative)
        body = text if text.startswith("\n") else f"\n{text}"
    else:
        metadata, body, _format = parsed
        if not metadata:
            raise MigrationError(f"empty frontmatter in {relative}")
    rendered = render_frontmatter(metadata, body, format="yaml")
    reparsed = parse_frontmatter(rendered)
    if reparsed is None or reparsed[2] != "yaml" or reparsed[0] != metadata:
        raise MigrationError(f"YAML frontmatter round trip failed: {relative}")
    return rendered.encode("utf-8")


def _normalized_schema(relative: Path, content: bytes) -> bytes:
    try:
        data = tomllib.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as error:
        raise MigrationError(
            f"invalid TOML JSON Schema: {relative}: {error}"
        ) from error
    if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise MigrationError(f"unsupported or missing JSON Schema dialect: {relative}")
    if not isinstance(data.get("type"), (str, list)):
        raise MigrationError(f"JSON Schema has no root type: {relative}")
    identifier = data.get("$id")
    if identifier is not None:
        if not isinstance(identifier, str) or not identifier.endswith(".schema.toml"):
            raise MigrationError(
                f"unexpected JSON Schema $id: {relative}: {identifier!r}"
            )
        data["$id"] = identifier[: -len(SCHEMA_SUFFIX)] + JSON_SCHEMA_SUFFIX
    rendered = (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    reparsed = json.loads(rendered)
    if reparsed != data:
        raise MigrationError(f"JSON Schema round trip failed: {relative}")
    return rendered


def _replace_schema_references(content: bytes) -> bytes:
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise MigrationError("scoped text reference file is not UTF-8") from error
    return text.replace(SCHEMA_SUFFIX, JSON_SCHEMA_SUFFIX).encode("utf-8")


def _replace_once_or_confirm(
    text: str,
    old: str,
    new: str,
    relative: Path,
) -> str:
    """Replace one exact block, accepting an already-migrated result."""
    old_count = text.count(old)
    if old_count == 1:
        return text.replace(old, new, 1)
    if old_count == 0 and text.count(new) == 1:
        return text
    raise MigrationError(
        f"guarded replacement mismatch in {relative}: "
        f"old={old_count}, new={text.count(new)}"
    )


def _rewrite_governance_policy(relative: Path, content: bytes) -> bytes:
    """Apply exact, idempotent policy replacements to current GOV owners."""
    if relative.as_posix() not in {
        "12_layer_gov/050_dset-gov-specification-artifact-maintenance.md",
        "12_layer_gov/070_dset-gov-specification-domain.md",
        "12_layer_gov/080_dset-gov-specification-methodology.md",
        ("12_layer_gov/120_schemas/060_dset-gov-schemas-evidence-record.schema.json"),
        (
            "12_layer_gov/130_templates/050_governance/000_core-v1/"
            "030_dset-gov-templates-governance-core-v1-artifact-maintenance.md"
        ),
    }:
        return content
    text = content.decode("utf-8")
    if relative.name == "080_dset-gov-specification-methodology.md":
        start_count = text.count(GOV_POLICY_SECTION_START)
        if start_count == 1:
            start = text.index(GOV_POLICY_SECTION_START)
            end = text.find(GOV_POLICY_SECTION_END, start)
            if end < 0:
                raise MigrationError(f"policy section end marker missing in {relative}")
            text = (
                text[:start]
                + GOV_POLICY_SECTION
                + text[end + len(GOV_POLICY_SECTION_END) :]
            )
        elif (
            start_count == 0
            and text.count(
                "## DSET-REQUIREMENT-GOV-097 — Select artifact carriers by their actual job"
            )
            == 1
        ):
            pass
        else:
            raise MigrationError(f"policy section markers are ambiguous in {relative}")
    elif relative.name == "070_dset-gov-specification-domain.md":
        text = _replace_once_or_confirm(
            text,
            DOMAIN_INVARIANT_OLD,
            DOMAIN_INVARIANT_NEW,
            relative,
        )
    elif relative.name.endswith("artifact-maintenance.md"):
        text = _replace_once_or_confirm(
            text,
            MAINTENANCE_OLD,
            MAINTENANCE_NEW,
            relative,
        )
    else:
        text = _replace_once_or_confirm(
            text,
            '"title": "DSET native Evidence Record TOML frontmatter"',
            '"title": "DSET native Evidence Record YAML frontmatter"',
            relative,
        )
    return text.encode("utf-8")


def _render_schema_hub(
    hub: Path,
    content: bytes,
    schema_names: list[str],
) -> bytes:
    """Render one exact schema inventory while preserving hub metadata."""
    parsed = parse_frontmatter(content.decode("utf-8"))
    if parsed is None or parsed[2] != "yaml":
        raise MigrationError(f"schema hub requires YAML frontmatter: {hub}")
    metadata = parsed[0]
    if hub.parts[0] == "11_layer_meta":
        if len(schema_names) != 4:
            raise MigrationError(
                f"META schema inventory expected 4 entries, found {len(schema_names)}"
            )
        title = "META"
        description = (
            "Project, version, package, and package-fragment schemas owned by META:"
        )
        footer = ""
    elif hub.parts[0] == "12_layer_gov":
        if len(schema_names) != 11:
            raise MigrationError(
                f"GOV schema inventory expected 11 entries, found {len(schema_names)}"
            )
        title = "GOV"
        description = "Repository-governance schemas owned by GOV:"
        footer = (
            "\nOther schema families live with their META, TOOL, SKILL, "
            "IMPL, or OPS owner.\n"
        )
    else:
        raise MigrationError(f"schema hub is outside META/GOV: {hub}")
    inventory = "\n".join(f"- `{name}`" for name in schema_names)
    body = f"\n# {title} schemas\n\n{description}\n\n{inventory}\n{footer}"
    rendered = render_frontmatter(metadata, body, format="yaml").encode("utf-8")
    reparsed = parse_frontmatter(rendered.decode("utf-8"))
    if reparsed is None or reparsed[0] != metadata or reparsed[2] != "yaml":
        raise MigrationError(f"schema hub round trip failed: {hub}")
    return rendered


def build_plan(root: Path) -> MigrationPlan:
    """Build a complete plan against exact current working-tree bytes."""
    root = root.resolve()
    if not (root / ".git").exists():
        raise MigrationError(f"not a repository root: {root}")

    writes: dict[Path, WriteOperation] = {}
    deletes: dict[Path, DeleteOperation] = {}
    schema_sources: list[Path] = []

    for root_name in MIGRATION_ROOTS:
        layer_root = root / root_name
        if not layer_root.is_dir() or layer_root.is_symlink():
            raise MigrationError(f"missing or unsafe migration root: {layer_root}")
        for path in sorted(layer_root.rglob("*")):
            if path.is_symlink():
                raise MigrationError(
                    f"symlink is outside the migration contract: {path}"
                )
            if path.is_dir():
                continue
            relative = path.relative_to(root)
            content = _read_regular_file(path)
            if path.name in IGNORED_HOST_FILES:
                continue
            if path.suffix == ".md":
                normalized = _normalized_markdown(relative, content)
                if normalized != content:
                    writes[path] = WriteOperation(
                        path,
                        _sha256(content),
                        normalized,
                        "use Markdown with YAML frontmatter",
                    )
                continue
            if path.name.endswith(SCHEMA_SUFFIX):
                target = path.with_name(
                    path.name[: -len(SCHEMA_SUFFIX)] + JSON_SCHEMA_SUFFIX
                )
                if target.exists():
                    raise MigrationError(f"JSON Schema target already exists: {target}")
                normalized = _normalized_schema(relative, content)
                writes[target] = WriteOperation(
                    target,
                    None,
                    normalized,
                    "use canonical JSON Schema",
                )
                deletes[path] = DeleteOperation(
                    path,
                    _sha256(content),
                    "replaced by canonical JSON Schema",
                )
                schema_sources.append(path)
                continue
            if path.name.endswith(JSON_SCHEMA_SUFFIX):
                try:
                    data = json.loads(content)
                except (UnicodeDecodeError, json.JSONDecodeError) as error:
                    raise MigrationError(f"invalid JSON Schema: {relative}") from error
                if data.get("$schema") != (
                    "https://json-schema.org/draft/2020-12/schema"
                ):
                    raise MigrationError(f"unsupported JSON Schema: {relative}")
                continue
            if path.suffix == ".toml":
                if path.name not in CONFIGURATION_TOML_NAMES:
                    raise MigrationError(f"unclassified TOML carrier: {relative}")
                try:
                    tomllib.loads(content.decode("utf-8"))
                except (UnicodeDecodeError, tomllib.TOMLDecodeError) as error:
                    raise MigrationError(
                        f"invalid configuration TOML: {relative}"
                    ) from error
                continue
            raise MigrationError(f"unclassified carrier: {relative}")

    if not schema_sources:
        existing_json = sum(
            1
            for root_name in MIGRATION_ROOTS
            for _path in (root / root_name).rglob(f"*{JSON_SCHEMA_SUFFIX}")
        )
        if existing_json != 15:
            raise MigrationError(
                "expected either 15 TOML JSON Schemas to migrate or 15 JSON results"
            )

    for root_name in MIGRATION_ROOTS:
        for path in sorted((root / root_name).rglob("*")):
            if (
                not path.is_file()
                or path in deletes
                or path.suffix
                not in {
                    ".md",
                    ".toml",
                    ".json",
                }
            ):
                continue
            content = writes[path].content if path in writes else path.read_bytes()
            rewritten = _replace_schema_references(content)
            rewritten = _rewrite_governance_policy(path.relative_to(root), rewritten)
            if rewritten != content:
                writes[path] = WriteOperation(
                    path,
                    writes[path].before_sha256 if path in writes else _sha256(content),
                    rewritten,
                    "update in-scope JSON Schema references",
                )

    schema_hubs = {
        Path("11_layer_meta/100_schemas/000_dset-meta-schemas-hub.md"): (
            Path("11_layer_meta/100_schemas")
        ),
        Path("12_layer_gov/120_schemas/000_dset-gov-schemas-hub.md"): (
            Path("12_layer_gov/120_schemas")
        ),
    }
    for hub_relative, directory_relative in schema_hubs.items():
        hub = root / hub_relative
        content = writes[hub].content if hub in writes else _read_regular_file(hub)
        schema_directory = root / directory_relative
        schema_names = sorted(
            {path.name for path in schema_directory.glob(f"*{JSON_SCHEMA_SUFFIX}")}
            | {
                path.name
                for path in writes
                if path.parent == schema_directory
                and path.name.endswith(JSON_SCHEMA_SUFFIX)
            }
        )
        rendered = _render_schema_hub(hub_relative, content, schema_names)
        if rendered != content:
            writes[hub] = WriteOperation(
                hub,
                writes[hub].before_sha256 if hub in writes else _sha256(content),
                rendered,
                "synchronize the exact JSON Schema inventory",
            )

    overlap = set(writes) & set(deletes)
    if overlap:
        raise MigrationError(f"write/delete collision: {sorted(overlap)}")
    return MigrationPlan(
        root=root,
        writes=tuple(sorted(writes.values(), key=lambda item: item.path)),
        deletes=tuple(sorted(deletes.values(), key=lambda item: item.path)),
    )


def _assert_preimages(plan: MigrationPlan) -> None:
    for operation in plan.writes:
        if operation.before_sha256 is None:
            if operation.path.exists():
                raise MigrationError(
                    f"new target appeared after planning: {operation.path}"
                )
            continue
        content = _read_regular_file(operation.path)
        if _sha256(content) != operation.before_sha256:
            raise MigrationError(f"file changed after planning: {operation.path}")
    for operation in plan.deletes:
        content = _read_regular_file(operation.path)
        if _sha256(content) != operation.before_sha256:
            raise MigrationError(f"file changed after planning: {operation.path}")


def verify(root: Path) -> None:
    """Verify the bounded carrier policy after migration."""
    root = root.resolve()
    markdown_count = 0
    schema_count = 0
    for root_name in MIGRATION_ROOTS:
        layer_root = root / root_name
        for path in sorted(layer_root.rglob("*")):
            if path.is_symlink():
                raise MigrationError(
                    f"symlink is outside the migration contract: {path}"
                )
            if path.is_dir():
                continue
            relative = path.relative_to(root)
            if path.name in IGNORED_HOST_FILES:
                continue
            if path.suffix == ".md":
                markdown_count += 1
                parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
                if parsed is None or parsed[2] != "yaml" or not parsed[0]:
                    raise MigrationError(
                        f"Markdown lacks nonempty YAML frontmatter: {relative}"
                    )
                continue
            if path.name.endswith(JSON_SCHEMA_SUFFIX):
                schema_count += 1
                data = json.loads(path.read_text(encoding="utf-8"))
                if (
                    data.get("$schema")
                    != "https://json-schema.org/draft/2020-12/schema"
                ):
                    raise MigrationError(f"invalid JSON Schema dialect: {relative}")
                continue
            if path.name.endswith(SCHEMA_SUFFIX):
                raise MigrationError(f"TOML-encoded JSON Schema remains: {relative}")
            if path.suffix == ".toml":
                if path.name not in CONFIGURATION_TOML_NAMES:
                    raise MigrationError(f"unclassified TOML carrier: {relative}")
                tomllib.loads(path.read_text(encoding="utf-8"))
                continue
            raise MigrationError(f"unclassified carrier: {relative}")
    if markdown_count != 77:
        raise MigrationError(f"expected 77 Markdown artifacts, found {markdown_count}")
    if schema_count != 15:
        raise MigrationError(f"expected 15 JSON Schemas, found {schema_count}")
    for root_name in MIGRATION_ROOTS:
        for path in (root / root_name).rglob("*"):
            if (
                path.is_file()
                and path.suffix in {".md", ".toml", ".json"}
                and SCHEMA_SUFFIX in path.read_text(encoding="utf-8")
            ):
                raise MigrationError(
                    f"stale in-scope TOML schema reference: {path.relative_to(root)}"
                )


def apply_plan(plan: MigrationPlan) -> None:
    """Apply a validated plan with staged bytes and rollback on failure."""
    _assert_preimages(plan)
    original_bytes: dict[Path, bytes | None] = {}
    for operation in plan.writes:
        original_bytes[operation.path] = (
            operation.path.read_bytes() if operation.path.exists() else None
        )
    for operation in plan.deletes:
        original_bytes[operation.path] = operation.path.read_bytes()

    with tempfile.TemporaryDirectory(
        prefix="dset-meta-gov-carriers-", dir="/tmp"
    ) as raw:
        staging_root = Path(raw)
        staged: dict[Path, Path] = {}
        for index, operation in enumerate(plan.writes):
            staged_path = staging_root / f"{index:04d}.stage"
            staged_path.write_bytes(operation.content)
            if _sha256(staged_path.read_bytes()) != _sha256(operation.content):
                raise MigrationError(f"staging digest mismatch: {operation.path}")
            if os.stat(staged_path).st_dev != os.stat(operation.path.parent).st_dev:
                raise MigrationError(
                    f"/tmp and target are on different filesystems: {operation.path}"
                )
            staged[operation.path] = staged_path

        try:
            for operation in plan.writes:
                operation.path.parent.mkdir(parents=True, exist_ok=True)
                os.replace(staged[operation.path], operation.path)
            for operation in plan.deletes:
                operation.path.unlink()
            verify(plan.root)
        except Exception as error:
            rollback_errors: list[str] = []
            for path, content in reversed(tuple(original_bytes.items())):
                try:
                    if content is None:
                        path.unlink(missing_ok=True)
                    else:
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(content)
                except OSError as rollback_error:
                    rollback_errors.append(f"{path}: {rollback_error}")
            suffix = (
                f"; rollback failures: {'; '.join(rollback_errors)}"
                if rollback_errors
                else "; all touched files rolled back"
            )
            raise MigrationError(f"migration failed: {error}{suffix}") from error


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=REPOSITORY_ROOT,
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    """Run the dry-run, apply, or verification mode."""
    arguments = _arguments()
    try:
        if arguments.check:
            verify(arguments.root)
            print("META/GOV carrier verification passed")
            return 0
        plan = build_plan(arguments.root)
        print(plan.summary())
        if arguments.apply:
            apply_plan(plan)
            print("META/GOV carrier migration applied and verified")
        else:
            print("DRY RUN: pass --apply to execute this exact class of operations")
        return 0
    except (MigrationError, FrontmatterError, OSError, json.JSONDecodeError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
