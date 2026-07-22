"""Deterministic, preview-first migration of DSET authority to TOML.

The migration command intentionally does not guess ownership.  It converts
DSET-owned structured YAML/JSON and DSET Markdown YAML frontmatter only after
building a complete source/target/digest/reference plan. Host carriers,
runtime journals, wire payloads, and standard JSON Schema contracts remain
explicit boundary-format exceptions.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterable
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .carrier_transitions import (
    CarrierTransitionError,
    historical_envelope,
    markdown_link_transition,
    markdown_transition,
)
from .carrier_transitions import ledger_path as carrier_transition_ledger_path
from .carrier_transitions import render_ledger as render_transition_ledger
from .compilation import compilation_path
from .frontmatter import parse as parse_frontmatter
from .health import health_path
from .layout import LAYER_ID_TOKENS, discover_layout
from .semantic_atoms import TERMINAL_STATES, collect_semantic_atoms
from .temp_paths import temporary_directory
from .toml_codec import TomlCodecError
from .toml_codec import dumps as dump_toml
from .toml_codec import loads as load_toml
from .yaml_subset import YamlSubsetError
from .yaml_subset import load as load_structured
from .yaml_subset import loads as load_yaml

# MIGRATION_SCHEMA_VERSION defines migration schema version; this module owns the default.
MIGRATION_SCHEMA_VERSION = "1.0"
# _STRUCTURED_SUFFIXES validates structured suffixes; this module owns the accepted syntax.
_STRUCTURED_SUFFIXES = {".yaml", ".yml", ".json"}
# _IGNORED_TOP_LEVEL validates ignored top level; this module owns the accepted syntax.
_IGNORED_TOP_LEVEL = {
    ".git",
    ".cache",
    ".uv-cache",
    ".venv",
    "build",
    "dist",
    "__pycache__",
}
# _RUNTIME_READINESS_PATH validates runtime readiness path; this module owns the accepted syntax.
_RUNTIME_READINESS_PATH = ".dset_runtime/toml-migration-runtime-readiness.json"
# _NON_REWRITABLE_EXCEPTIONS validates non rewritable exceptions; this module owns the accepted syntax.
_NON_REWRITABLE_EXCEPTIONS = {
    "cli-wire-json",
    "external-json-schema",
    "immutable-legacy-decision-carrier",
    "immutable-promoted-proof",
    "immutable-sealed-atom",
    "machine-local-runtime-journal",
    "retained-symlink",
}
# _PACKAGE_FIELD_BY_CLASSIFICATION validates package field by classification; this module owns the accepted syntax.
_PACKAGE_FIELD_BY_CLASSIFICATION: dict[tuple[str, str | None], str] = {
    ("decision", "requirement"): "requirements",
    ("decision", "contract"): "contracts",
    ("decision", "user_story"): "stories",
    ("decision", "outcome"): "outcomes",
    ("qa", "test"): "tests",
    ("qa", "evaluation"): "evals",
}
# _PACKAGE_ARTIFACT_BY_FIELD validates package artifact by field; this module owns the accepted syntax.
_PACKAGE_ARTIFACT_BY_FIELD = {
    "requirements": "spec",
    "contracts": "contracts",
    "stories": "stories",
    "outcomes": "outcomes",
    "tests": "test_plan",
    "evals": "eval_plan",
}


class TomlMigrationError(ValueError):
    """The requested migration is incomplete, ambiguous, or unsafe to apply."""


@dataclass(frozen=True)
class MigrationEntry:
    kind: str
    source: Path
    target: Path
    before_text: str
    after_text: str
    normalizations: tuple[str, ...] = ()

    @property
    def source_digest(self) -> str:
        return _sha256(self.before_text)

    @property
    def target_digest(self) -> str:
        return _sha256(self.after_text)


@dataclass(frozen=True)
class ReferenceRewrite:
    path: Path
    source: str
    target: str
    count: int


@dataclass(frozen=True)
class PackageSuccessor:
    """One current TOML registry derived from an immutable package carrier."""

    source: Path
    target: Path
    source_text: str
    target_text: str
    status: str

    @property
    def source_digest(self) -> str:
        return _sha256(self.source_text)

    @property
    def target_digest(self) -> str:
        return _sha256(self.target_text)


@dataclass(frozen=True)
class MigrationPlan:
    root: Path
    entries: tuple[MigrationEntry, ...]
    exceptions: tuple[dict[str, object], ...]
    references: tuple[ReferenceRewrite, ...]
    blockers: tuple[str, ...]
    runtime_readiness: dict[str, object]
    package_successors: tuple[PackageSuccessor, ...] = ()
    preserved_structured: tuple[Path, ...] = ()

    @property
    def ready(self) -> bool:
        return not self.blockers

    @property
    def digest(self) -> str:
        payload = json.dumps(
            self.report(), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        )
        return _sha256(payload)

    def report(self) -> dict[str, object]:
        changes_by_kind = _count_by(
            (entry.kind for entry in self.entries),
        )
        exceptions_by_category = _count_by(
            str(item["category"]) for item in self.exceptions
        )
        blocker_categories = _count_by(
            _blocker_category(item) for item in self.blockers
        )
        normalizations = [
            {
                "source": _relative(self.root, entry.source),
                "key_path": key_path,
            }
            for entry in self.entries
            for key_path in entry.normalizations
        ]
        return {
            "schema_version": MIGRATION_SCHEMA_VERSION,
            "root": str(self.root),
            "status": "ready" if self.ready else "blocked",
            "changes": [
                {
                    "kind": entry.kind,
                    "source": _relative(self.root, entry.source),
                    "target": _relative(self.root, entry.target),
                    "before_sha256": entry.source_digest,
                    "after_sha256": entry.target_digest,
                }
                for entry in self.entries
            ],
            "normalizations": normalizations,
            "reference_rewrites": [
                {
                    "path": _relative(self.root, reference.path),
                    "source": reference.source,
                    "target": reference.target,
                    "count": reference.count,
                }
                for reference in self.references
            ],
            "package_successors": [
                {
                    "source": _relative(self.root, successor.source),
                    "target": _relative(self.root, successor.target),
                    "before_sha256": successor.source_digest,
                    "after_sha256": successor.target_digest,
                    "status": successor.status,
                }
                for successor in self.package_successors
            ],
            "preserved_structured": [
                {
                    "path": _relative(self.root, path),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
                for path in self.preserved_structured
            ],
            "exceptions": list(self.exceptions),
            "blockers": list(self.blockers),
            "runtime_readiness": self.runtime_readiness,
            "counts": {
                "changes": len(self.entries),
                "changes_by_kind": changes_by_kind,
                "reference_rewrites": len(self.references),
                "reference_occurrences": sum(item.count for item in self.references),
                "package_successors": len(self.package_successors),
                "pending_package_successors": sum(
                    successor.status == "pending"
                    for successor in self.package_successors
                ),
                "preserved_structured": len(self.preserved_structured),
                "exceptions": len(self.exceptions),
                "exceptions_by_category": exceptions_by_category,
                "normalizations": len(normalizations),
                "blockers": len(self.blockers),
                "blockers_by_category": blocker_categories,
            },
        }


def plan_toml_migration(
    root: Path, *, bypass_runtime_readiness: bool = False
) -> MigrationPlan:
    """Inventory a root without modifying it.

    A plan may be ``blocked`` while still being complete: blockers are the
    exact conditions an operator must resolve before an explicit ``--apply``.
    """

    root = root.resolve()
    entries: list[MigrationEntry] = []
    exceptions: list[dict[str, object]] = []
    blockers: list[str] = []
    paths = list(_project_files(root))
    legacy_structured, legacy_blockers = _legacy_structured_registry(root)
    blockers.extend(legacy_blockers)
    immutable, immutable_blockers, shared_packages = _immutable_classifications(
        root, paths
    )
    blockers.extend(immutable_blockers)
    transition_entries, transition_sources, transition_blockers = (
        _carrier_transition_entries(root, paths, legacy_structured, immutable)
    )
    entries.extend(transition_entries)
    blockers.extend(transition_blockers)
    for path in paths:
        if path in transition_sources:
            continue
        classification = _exception_classification(root, path, immutable)
        if classification is not None:
            exceptions.append(classification)
            if classification["category"] == "retained-symlink" and not bool(
                classification["resolves_within_root"]
            ):
                blockers.append(
                    "path-safety: retained symlink resolves outside repository: "
                    f"{classification['path']}"
                )
            continue
        if _is_owned_structured(root, path):
            if (
                path in legacy_structured
                and legacy_structured[path]["current_owner"].is_file()
                and _toml_cutover_complete(root)
            ):
                continue
            try:
                entries.append(_structured_entry(root, path))
            except (OSError, UnicodeError, ValueError, TomlCodecError) as error:
                blockers.append(
                    f"conversion: unsupported source {_relative(root, path)}: {error}"
                )
            continue
        if _is_owned_markdown(root, path):
            try:
                entry = _frontmatter_entry(root, path)
            except (OSError, UnicodeError, ValueError, TomlCodecError) as error:
                blockers.append(
                    "conversion: unsupported frontmatter "
                    f"{_relative(root, path)}: {error}"
                )
            else:
                if entry is not None:
                    entries.append(entry)

    entries.sort(key=lambda item: (_relative(root, item.source), item.kind))
    successors, successor_blockers = _package_successors(
        root, shared_packages - transition_sources, entries
    )
    blockers.extend(successor_blockers)
    blockers.extend(_collision_blockers(root, entries, successors))
    successor_mapping = {successor.source: successor.target for successor in successors}
    successor_mapping.update(
        {
            source: item["current_owner"]
            for source, item in legacy_structured.items()
            if source not in shared_packages
            and not (item["current_owner"].is_file() and _toml_cutover_complete(root))
        }
    )
    references, reference_blockers = _reference_rewrites(
        root,
        paths,
        entries,
        immutable,
        successor_mapping,
        legacy_structured=set(legacy_structured),
        historical_trace_sources=shared_packages,
        transition_sources=transition_sources,
    )
    blockers.extend(reference_blockers)
    runtime_readiness, runtime_blockers = _runtime_readiness(
        root,
        entries,
        references,
        exceptions,
        successors,
        tuple(sorted(set(legacy_structured) - transition_sources)),
    )
    if bypass_runtime_readiness:
        runtime_readiness = {**runtime_readiness, "bypassed_for_proof": True}
    else:
        blockers.extend(runtime_blockers)
    return MigrationPlan(
        root=root,
        entries=tuple(entries),
        exceptions=tuple(sorted(exceptions, key=lambda item: str(item["path"]))),
        references=tuple(references),
        blockers=tuple(sorted(set(blockers))),
        runtime_readiness=runtime_readiness,
        package_successors=tuple(successors),
        preserved_structured=tuple(sorted(set(legacy_structured) - transition_sources)),
    )


def apply_toml_migration(
    root: Path, *, bypass_runtime_readiness: bool = False
) -> MigrationPlan:
    """Apply a fully planned migration with backup-and-restore recovery."""

    plan = plan_toml_migration(root, bypass_runtime_readiness=bypass_runtime_readiness)
    if not plan.ready:
        raise TomlMigrationError("; ".join(plan.blockers))
    if (
        not plan.entries
        and not plan.references
        and not any(item.status == "pending" for item in plan.package_successors)
    ):
        return plan

    writes = _planned_writes(plan)
    deletes = {
        entry.source
        for entry in plan.entries
        if entry.source != entry.target
        and (
            entry.source not in plan.preserved_structured
            or entry.kind == "historical-envelope"
        )
    }
    _preflight_apply(plan)
    backup_root = plan.root / ".dset_runtime" / "toml-migration-backups" / plan.digest
    bundle_path = plan.root / "dset_toolchain" / "bootstrap_bundle.json"
    regenerates_bundle = (
        bundle_path.is_file()
        and (plan.root / "scripts" / "build_bootstrap_bundle.py").is_file()
    )
    generated = {bundle_path} if regenerates_bundle else set()
    generated.update(_existing_reconciliation_outputs(plan.root))
    affected = sorted(set(writes) | deletes | generated)
    originals = {
        path: path.read_bytes() if path.exists() else None for path in affected
    }
    _write_recovery_manifest(plan, backup_root, originals)
    try:
        for path in sorted(writes):
            _atomic_write_text(path, writes[path])
        for path in sorted(deletes):
            path.unlink()
        if regenerates_bundle:
            _atomic_write_text(bundle_path, _render_bootstrap_bundle(plan.root))
        _reconcile_migrated_authority(plan.root)
        _validate_staged_tree(plan, writes)
        _validate_migrated_runtime(plan.root)
        if not bypass_runtime_readiness and (plan.root / "dset_toolchain").is_dir():
            _validate_proven_output(plan)
    except Exception as error:
        _restore(originals)
        _remove_failed_recovery(backup_root)
        raise TomlMigrationError(
            f"migration rolled back after staged validation failure: {error}"
        ) from error
    return plan


def _project_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in _IGNORED_TOP_LEVEL for part in relative.parts):
            continue
        if relative.parts[:2] == (".dset_runtime", "toml-migration-backups"):
            continue
        if path.is_symlink():
            paths.append(path)
            continue
        if path.is_file():
            paths.append(path)
    return sorted(paths, key=lambda item: item.relative_to(root).as_posix())


def _existing_reconciliation_outputs(root: Path) -> set[Path]:
    layout = discover_layout(root)
    candidates = {
        layout.governance_path,
        compilation_path(root),
        layout.traceability_path,
    }
    with suppress(KeyError, OSError, TypeError, ValueError, YamlSubsetError):
        candidates.add(health_path(root))
    return {path for path in candidates if path.is_file()}


def _exception_classification(
    root: Path,
    path: Path,
    immutable: dict[Path, dict[str, object]] | None = None,
) -> dict[str, object] | None:
    immutable_classification = (immutable or {}).get(path)
    if immutable_classification is not None:
        return immutable_classification
    if path.is_symlink():
        resolved = path.resolve(strict=False)
        return {
            **_exception(root, path, "retained-symlink"),
            "resolves_within_root": _is_within_root(root, resolved),
            "resolved_target": str(resolved),
        }
    relative = path.relative_to(root)
    parts = relative.parts
    suffix = path.suffix.lower()
    if parts[:1] == (".dset_runtime",) or parts[:2] == (".dset", "runtime"):
        if suffix == ".json":
            return _exception(root, path, "machine-local-runtime-journal")
        return None
    if parts[:2] == (".github", "workflows") and suffix in {".yaml", ".yml"}:
        return _exception(root, path, "github-actions")
    if (
        len(parts) >= 3
        and parts[0] == "skills"
        and parts[-2:] == ("agents", "openai.yaml")
    ):
        return _exception(root, path, "host-skill-metadata")
    if (
        len(parts) >= 2
        and parts[0] == "skills"
        and parts[-1] == "SKILL.md"
        and _has_yaml_frontmatter(path)
    ):
        return _exception(root, path, "host-skill-frontmatter")
    if path.name in {
        "package-lock.json",
        "npm-shrinkwrap.json",
        "composer.lock",
        "Pipfile.lock",
    }:
        return _exception(root, path, "ecosystem-manifest-or-lockfile")
    if relative.as_posix() == "dset_toolchain/bootstrap_bundle.json":
        return {
            **_exception(root, path, "cli-wire-json"),
            "migration_action": "regenerated-transactionally",
        }
    if suffix == ".json" and "schemas" in parts and path.name.endswith(".schema.json"):
        return _external_contract_exception(root, path, "external-json-schema")
    return None


def _immutable_classifications(
    root: Path, paths: list[Path]
) -> tuple[dict[Path, dict[str, object]], list[str], set[Path]]:
    """Locate byte-stable historical carriers before planning any writes."""

    classifications: dict[Path, dict[str, object]] = {}
    blockers: list[str] = []
    path_set = set(paths)

    atom_ledger, atom_errors = _load_history_ledger(
        root,
        (
            "00_project/atoms",
            "dset/scopes/gov/governance/atoms",
            "dset/governance/atoms",
        ),
        "atom seal",
    )
    blockers.extend(atom_errors)
    if atom_ledger is not None:
        records = atom_ledger.get("records")
        if not isinstance(records, list):
            blockers.append("immutability: atom seal ledger requires records")
        else:
            for record in records:
                if not isinstance(record, dict) or not isinstance(
                    record.get("path"), str
                ):
                    blockers.append(
                        "immutability: atom seal ledger contains an invalid path"
                    )
                    continue
                _register_immutable_path(
                    root,
                    path_set,
                    classifications,
                    blockers,
                    str(record.get("current_path", record["path"])),
                    "immutable-sealed-atom",
                    "canonical-history",
                )

    legacy_ledger, legacy_errors = _load_history_ledger(
        root,
        (
            "00_project/legacy-authority",
            "dset/scopes/gov/governance/legacy-authority",
            "dset/governance/legacy-authority",
        ),
        "legacy Decision authority",
    )
    blockers.extend(legacy_errors)
    shared_paths: set[Path] = set()
    if legacy_ledger is not None:
        records = legacy_ledger.get("records")
        if not isinstance(records, list):
            blockers.append(
                "immutability: legacy Decision authority ledger requires records"
            )
        else:
            for record in records:
                fragments = (
                    record.get("fragments") if isinstance(record, dict) else None
                )
                if not isinstance(fragments, list):
                    blockers.append(
                        "immutability: legacy Decision authority record "
                        "requires fragments"
                    )
                    continue
                for fragment in fragments:
                    if not isinstance(fragment, dict) or not isinstance(
                        fragment.get("path"), str
                    ):
                        blockers.append(
                            "immutability: legacy Decision fragment has an invalid path"
                        )
                        continue
                    raw_path = str(fragment["path"])
                    active_path = str(fragment.get("current_path", raw_path))
                    selector = fragment.get("selector")
                    shared = selector != "whole-carrier"
                    _register_immutable_path(
                        root,
                        path_set,
                        classifications,
                        blockers,
                        active_path,
                        "immutable-legacy-decision-carrier",
                        "canonical-history",
                        shared=shared,
                    )
                    _validate_legacy_fragment(
                        root,
                        raw_path,
                        selector,
                        fragment.get("sha256"),
                        blockers,
                        current_path=fragment.get("current_path"),
                        current_digest=fragment.get("current_sha256"),
                    )
                    if shared and not isinstance(fragment.get("current_path"), str):
                        shared_paths.add((root / active_path).resolve())

    for path in paths:
        relative = path.relative_to(root)
        if (
            path.suffix.lower() == ".md"
            and "proofs" in relative.parts
            and path.name != "README.md"
        ):
            classifications.setdefault(
                path,
                {
                    **_exception(root, path, "immutable-promoted-proof"),
                    "authority": "canonical-history",
                },
            )

    package_paths = {
        path
        for path in shared_paths
        if _is_within_root(root, path)
        and path.name in {"package.yaml", "package.yml"}
        and _is_owned_structured(root, path)
    }
    unsupported = shared_paths - package_paths
    for path in sorted(unsupported):
        blockers.append(
            "authority-boundary: shared legacy Decision carrier has no governed "
            f"native successor: {_relative(root, path)}"
        )
    return classifications, blockers, package_paths


def _validate_legacy_fragment(
    root: Path,
    raw_path: str,
    selector: object,
    declared_digest: object,
    blockers: list[str],
    *,
    current_path: object = None,
    current_digest: object = None,
) -> None:
    """Verify the ledger-bound fragment without altering its historical carrier."""

    active_raw = str(current_path) if isinstance(current_path, str) else raw_path
    path = (root / active_raw).resolve()
    if not _is_within_root(root, path) or not path.is_file():
        return
    if not isinstance(selector, str) or not isinstance(declared_digest, str):
        blockers.append(
            f"immutability: legacy Decision fragment seal is incomplete: {raw_path}"
        )
        return
    if selector == "whole-carrier":
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        expected = (
            current_digest if isinstance(current_digest, str) else declared_digest
        )
    else:
        field, separator, identifier = selector.partition(":")
        if isinstance(current_digest, str):
            carrier_digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if carrier_digest != current_digest:
                blockers.append(
                    f"immutability: current legacy carrier digest changed: {active_raw}"
                )
                return
        try:
            data = load_structured(path)
            if isinstance(current_path, str) and path.name.endswith(".legacy.toml"):
                from .carrier_transitions import decode_historical_envelope

                data = decode_historical_envelope(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, YamlSubsetError) as error:
            blockers.append(
                f"immutability: cannot read selector-sealed carrier {raw_path}: {error}"
            )
            return
        values = data.get(field) if isinstance(data, dict) and separator else None
        if not isinstance(values, list) or identifier not in values:
            blockers.append(
                "immutability: selector-sealed legacy fragment is missing or changed: "
                f"{raw_path}#{selector}"
            )
            return
        actual = hashlib.sha256(f"{selector}\n".encode()).hexdigest()
        expected = declared_digest
    if actual != expected:
        blockers.append(
            "immutability: selector-sealed legacy fragment digest changed: "
            f"{raw_path}#{selector}"
        )


def _load_history_ledger(
    root: Path, stems: tuple[str, ...], label: str
) -> tuple[dict[str, Any] | None, list[str]]:
    candidates = [
        root / f"{stem}{suffix}"
        for stem in stems
        for suffix in (".toml", ".yaml", ".yml")
        if (root / f"{stem}{suffix}").is_file()
    ]
    if not candidates:
        return None, []
    if len(candidates) > 1:
        rendered = ", ".join(_relative(root, path) for path in candidates)
        return None, [f"immutability: duplicate {label} ledgers: {rendered}"]
    path = candidates[0]
    try:
        data = load_structured(path)
    except (OSError, UnicodeError, YamlSubsetError) as error:
        return None, [f"immutability: invalid {label} ledger: {error}"]
    if not isinstance(data, dict):
        return None, [f"immutability: {label} ledger must be a mapping"]
    return data, []


def _legacy_structured_registry(
    root: Path,
) -> tuple[dict[Path, dict[str, Any]], list[str]]:
    """Load exact historical structured snapshots without accepting wildcards."""

    candidates = (
        root / "00_project/artifact-types.toml",
        root / "dset/scopes/gov/artifact-types.toml",
        root / "dset/scopes/gov/artifact-types.yaml",
        root / "dset/artifact-types.toml",
        root / "dset/artifact-types.yaml",
    )
    registry = next((path for path in candidates if path.is_file()), None)
    if registry is None:
        return {}, []
    try:
        data = load_structured(registry)
    except (OSError, UnicodeError, YamlSubsetError) as error:
        return {}, [f"legacy-structured: cannot read registry: {error}"]
    raw_entries = data.get("legacy_structured") if isinstance(data, dict) else None
    if raw_entries is None:
        return {}, []
    if not isinstance(raw_entries, list):
        return {}, ["legacy-structured: registry must be a list"]

    result: dict[Path, dict[str, Any]] = {}
    owners: set[Path] = set()
    blockers: list[str] = []
    for item in raw_entries:
        if not isinstance(item, dict):
            blockers.append("legacy-structured: every entry must be a mapping")
            continue
        raw_path = item.get("path")
        raw_owner = item.get("current_owner")
        digest = item.get("sha256")
        raw_current = item.get("current_path")
        current_digest = item.get("current_sha256")
        current_transition = item.get("transition_id")
        if not isinstance(raw_path, str) or not isinstance(raw_owner, str):
            blockers.append("legacy-structured: path and current_owner are required")
            continue
        if any(token in raw_path or token in raw_owner for token in "*?[]"):
            blockers.append(
                f"legacy-structured: wildcard paths are forbidden: {raw_path}"
            )
            continue
        source = (root / raw_path).resolve()
        owner = (root / raw_owner).resolve()
        if not _is_within_root(root, source) or not _is_within_root(root, owner):
            blockers.append(f"legacy-structured: path escapes repository: {raw_path}")
            continue
        if source in result:
            blockers.append(f"legacy-structured: duplicate path: {raw_path}")
            continue
        if owner in owners:
            blockers.append(f"legacy-structured: duplicate current owner: {raw_owner}")
            continue
        valid_owner = owner.suffix.lower() == ".toml"
        if source.suffix.lower() not in {".yaml", ".yml"} or not valid_owner:
            blockers.append(
                "legacy-structured: current_owner must be a TOML carrier for "
                f"{raw_path}"
            )
            continue
        if not source.is_file() or source.is_symlink():
            if all(
                isinstance(value, str)
                for value in (raw_current, current_digest, current_transition)
            ):
                current = (root / str(raw_current)).resolve()
                if (
                    _is_within_root(root, current)
                    and current.is_file()
                    and not current.is_symlink()
                    and hashlib.sha256(current.read_bytes()).hexdigest()
                    == current_digest
                ):
                    owners.add(owner)
                    continue
            blockers.append(
                f"legacy-structured: registered snapshot is missing: {raw_path}"
            )
            continue
        actual = hashlib.sha256(source.read_bytes()).hexdigest()
        if not isinstance(digest, str) or actual != digest:
            blockers.append(f"legacy-structured: snapshot digest changed: {raw_path}")
            continue
        result[source] = {**item, "current_owner": owner}
        owners.add(owner)
    return result, blockers


def _carrier_transition_entries(
    root: Path,
    paths: list[Path],
    legacy_structured: dict[Path, dict[str, Any]],
    immutable: dict[Path, dict[str, object]],
) -> tuple[list[MigrationEntry], set[Path], list[str]]:
    """Plan GOV-018 carriers plus their append-only reseal registries."""

    # GOV-018 is feature-gated by its canonical append-only ledger. Older
    # repositories and compatibility fixtures retain the previous behavior
    # until they materialize that authority.
    if not carrier_transition_ledger_path(root).is_file():
        return [], set(), []

    entries: list[MigrationEntry] = []
    blockers: list[str] = []
    transition_sources: set[Path] = set()
    records: list[dict[str, Any]] = []
    by_source: dict[str, tuple[MigrationEntry, dict[str, Any]]] = {}

    candidates: list[tuple[Path, Path, str]] = []
    for source in sorted(legacy_structured):
        if source.is_file():
            target = source.with_name(f"{source.stem}.legacy.toml")
            candidates.append((source, target, "structured"))
    for source in sorted(paths):
        classification = _exception_classification(root, source, immutable)
        if (
            _is_owned_markdown(root, source)
            and _has_yaml_frontmatter(source)
            and not (
                classification is not None
                and str(classification["category"])
                in {"host-skill-frontmatter", "github-actions"}
            )
        ):
            candidates.append((source, source, "markdown"))

    seen: set[Path] = set()
    for source, target, kind in candidates:
        if source in seen:
            continue
        seen.add(source)
        if target != source and target.exists():
            blockers.append(
                f"carrier-transition: target collision {_relative(root, target)}"
            )
            continue
        try:
            if kind == "structured":
                rendered, record = historical_envelope(root, source, target)
                entry_kind = "historical-envelope"
            else:
                rendered, record = markdown_transition(root, source)
                entry_kind = "immutable-frontmatter"
        except (OSError, UnicodeError, ValueError, CarrierTransitionError) as error:
            blockers.append(f"carrier-transition: {_relative(root, source)}: {error}")
            continue
        carrier_ids, semantic_ids = _transition_identities(root, source)
        record["carrier_ids"] = carrier_ids
        record["semantic_ids"] = semantic_ids
        entry = MigrationEntry(
            entry_kind,
            source,
            target,
            source.read_text(encoding="utf-8"),
            rendered,
            tuple(f"null:{item}" for item in record["null_paths"]),
        )
        entries.append(entry)
        records.append(record)
        transition_sources.add(source)
        by_source[_relative(root, source)] = (entry, record)

    historical_mapping = {
        entry.source.resolve(): entry.target.resolve()
        for entry in entries
        if entry.kind == "historical-envelope"
    }
    for source in sorted(paths):
        classification = immutable.get(source)
        if (
            source in transition_sources
            or source.suffix != ".md"
            or classification is None
            or classification.get("category") != "immutable-promoted-proof"
        ):
            continue
        try:
            result = markdown_link_transition(root, source, historical_mapping)
        except (OSError, UnicodeError, ValueError, CarrierTransitionError) as error:
            blockers.append(f"carrier-transition: {_relative(root, source)}: {error}")
            continue
        if result is None:
            continue
        rendered, record = result
        carrier_ids, semantic_ids = _transition_identities(root, source)
        record["carrier_ids"] = carrier_ids
        record["semantic_ids"] = semantic_ids
        entry = MigrationEntry(
            "immutable-links",
            source,
            source,
            source.read_text(encoding="utf-8"),
            rendered,
        )
        entries.append(entry)
        records.append(record)
        transition_sources.add(source)
        by_source[_relative(root, source)] = (entry, record)

    if not records:
        return entries, transition_sources, blockers

    for relative in (
        "00_project/atoms.toml",
        "00_project/legacy-authority.toml",
        "00_project/artifact-types.toml",
        "dset/scopes/gov/governance/atoms.toml",
        "dset/scopes/gov/governance/legacy-authority.toml",
        "dset/scopes/gov/artifact-types.toml",
        "dset/governance/atoms.toml",
        "dset/governance/legacy-authority.toml",
        "dset/artifact-types.toml",
    ):
        path = root / relative
        if not path.is_file():
            continue
        try:
            data = load_structured(path)
            if not isinstance(data, dict):
                raise CarrierTransitionError("registry root must be a mapping")
            _reseal_transition_registry(relative, data, by_source)
            rendered = dump_toml(data)
        except (OSError, UnicodeError, ValueError, CarrierTransitionError) as error:
            blockers.append(f"carrier-transition: cannot reseal {relative}: {error}")
            continue
        before = path.read_text(encoding="utf-8")
        if rendered != before:
            entries.append(
                MigrationEntry("transition-registry", path, path, before, rendered)
            )

    ledger = carrier_transition_ledger_path(root)
    if not ledger.is_file():
        blockers.append(
            "carrier-transition: missing canonical ledger "
            + ledger.relative_to(root).as_posix()
        )
    else:
        try:
            before = ledger.read_text(encoding="utf-8")
            rendered = render_transition_ledger(root, records)
        except (OSError, UnicodeError, ValueError, CarrierTransitionError) as error:
            blockers.append(f"carrier-transition: cannot update ledger: {error}")
        else:
            if rendered != before:
                entries.append(
                    MigrationEntry(
                        "transition-registry", ledger, ledger, before, rendered
                    )
                )
    return entries, transition_sources, blockers


def _transition_identities(root: Path, source: Path) -> tuple[list[str], list[str]]:
    relative = _relative(root, source)
    carrier_ids: set[str] = set()
    semantic_ids: set[str] = set()
    for stems, record_field in (
        (
            (
                "00_project/atoms",
                "dset/scopes/gov/governance/atoms",
                "dset/governance/atoms",
            ),
            "records",
        ),
        (
            (
                "00_project/legacy-authority",
                "dset/scopes/gov/governance/legacy-authority",
                "dset/governance/legacy-authority",
            ),
            "records",
        ),
    ):
        data, _errors = _load_history_ledger(root, stems, "carrier transition")
        values = data.get(record_field) if isinstance(data, dict) else None
        if not isinstance(values, list):
            continue
        for item in values:
            if not isinstance(item, dict):
                continue
            if item.get("path") == relative:
                carrier = item.get("carrier_id")
                semantic = item.get("semantic_id")
                if isinstance(carrier, str):
                    carrier_ids.add(carrier)
                if isinstance(semantic, str):
                    semantic_ids.add(semantic)
            fragments = item.get("fragments")
            if isinstance(fragments, list) and any(
                isinstance(fragment, dict) and fragment.get("path") == relative
                for fragment in fragments
            ):
                value = item.get("semantic_id")
                if isinstance(value, str):
                    semantic_ids.add(value)
    type_registry = next(
        (
            path
            for path in (
                root / "00_project/artifact-types.toml",
                root / "dset/scopes/gov/artifact-types.toml",
                root / "dset/artifact-types.toml",
            )
            if path.is_file()
        ),
        None,
    )
    if type_registry is not None:
        try:
            registry_data = load_structured(type_registry)
        except (OSError, UnicodeError, YamlSubsetError):
            registry_data = {}
        legacy = (
            registry_data.get("legacy_structured")
            if isinstance(registry_data, dict)
            else None
        )
        if isinstance(legacy, list):
            for item in legacy:
                if not isinstance(item, dict) or item.get("path") != relative:
                    continue
                retained = item.get("retained_for")
                if not isinstance(retained, list):
                    continue
                semantic_ids.update(
                    str(identity["semantic_id"])
                    for identity in retained
                    if isinstance(identity, dict)
                    and isinstance(identity.get("semantic_id"), str)
                )
    try:
        metadata = parse_frontmatter(source.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        metadata = None
    if metadata is not None:
        carrier = metadata[0].get("artifact_id")
        semantic = metadata[0].get("semantic_id")
        if isinstance(carrier, str):
            carrier_ids.add(carrier)
        if isinstance(semantic, str):
            semantic_ids.add(semantic)
    return sorted(carrier_ids), sorted(semantic_ids)


def _reseal_transition_registry(
    relative: str,
    data: dict[str, Any],
    by_source: dict[str, tuple[MigrationEntry, dict[str, Any]]],
) -> None:
    records = data.get("records")
    if relative.endswith("atoms.toml") and isinstance(records, list):
        for item in records:
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                continue
            transition = by_source.get(str(item["path"]))
            if transition is not None:
                entry, record = transition
                item["current_path"] = record["current_path"]
                item["current_sha256"] = entry.target_digest
                item["transition_id"] = record["id"]
        return
    if relative.endswith("legacy-authority.toml") and isinstance(records, list):
        for item in records:
            fragments = item.get("fragments") if isinstance(item, dict) else None
            if not isinstance(fragments, list):
                continue
            for fragment in fragments:
                if not isinstance(fragment, dict) or not isinstance(
                    fragment.get("path"), str
                ):
                    continue
                transition = by_source.get(str(fragment["path"]))
                if transition is None:
                    continue
                entry, record = transition
                fragment["current_path"] = record["current_path"]
                fragment["current_sha256"] = entry.target_digest
                fragment["transition_id"] = record["id"]
        return
    legacy = data.get("legacy_structured")
    if relative.endswith("artifact-types.toml") and isinstance(legacy, list):
        for item in legacy:
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                continue
            transition = by_source.get(str(item["path"]))
            if transition is not None:
                entry, record = transition
                item["current_path"] = record["current_path"]
                item["current_sha256"] = entry.target_digest
                item["transition_id"] = record["id"]


def _toml_cutover_complete(root: Path) -> bool:
    return any(
        path.is_file()
        for path in (
            root / ".dset/dset_settings.toml",
            root / "dset/dset_settings.toml",
            root / "dset/scopes/meta/dset.toml",
            root / "dset/dset.toml",
        )
    )


def _register_immutable_path(
    root: Path,
    project_paths: set[Path],
    classifications: dict[Path, dict[str, object]],
    blockers: list[str],
    raw_path: str,
    category: str,
    authority: str,
    *,
    shared: bool = False,
) -> None:
    path = (root / raw_path).resolve()
    if not _is_within_root(root, path):
        blockers.append(
            f"path-safety: immutable carrier escapes repository: {raw_path}"
        )
        return
    if path not in project_paths:
        blockers.append(f"immutability: registered carrier is missing: {raw_path}")
        return
    current = classifications.get(path)
    if current is not None and current.get("category") != category:
        blockers.append(
            "immutability: carrier has conflicting historical classifications: "
            f"{raw_path}"
        )
        return
    classifications[path] = {
        **_exception(root, path, category),
        "authority": authority,
        "shared_carrier": shared,
    }


def _package_successors(
    root: Path,
    shared_packages: set[Path],
    entries: list[MigrationEntry],
) -> tuple[list[PackageSuccessor], list[str]]:
    """Build deterministic current registries for selector-sealed packages."""

    if not shared_packages:
        return [], []
    blockers: list[str] = []
    entry_by_source = {entry.source.resolve(): entry for entry in entries}
    path_mapping = {
        entry.source.resolve(): entry.target.resolve()
        for entry in entries
        if entry.source != entry.target
    }
    packages: list[dict[str, Any]] = []
    targets: dict[Path, list[Path]] = {}
    inactive, lifecycle_blockers = _inactive_semantic_ids(root)
    blockers.extend(lifecycle_blockers)

    for source in sorted(shared_packages):
        target = source.with_suffix(".toml")
        targets.setdefault(target, []).append(source)
        try:
            loaded = load_structured(source)
        except (OSError, UnicodeError, YamlSubsetError) as error:
            blockers.append(
                f"package-successor: cannot read {_relative(root, source)}: {error}"
            )
            continue
        if not isinstance(loaded, dict):
            blockers.append(
                f"package-successor: package root must be a mapping: "
                f"{_relative(root, source)}"
            )
            continue
        data = _copy_structured(loaded)
        layer = data.get("layer")
        if not isinstance(layer, str):
            blockers.append(
                "package-successor: package layer is missing: "
                f"{_relative(root, source)}"
            )
            continue
        for field in _PACKAGE_ARTIFACT_BY_FIELD:
            values = data.get(field)
            if isinstance(values, list):
                data[field] = [
                    value
                    for value in values
                    if not isinstance(value, str) or value not in inactive
                ]
        _reconcile_package_artifact_paths(root, source, data, path_mapping, blockers)
        packages.append(
            {
                "source": source,
                "target": target,
                "layer": layer,
                "data": data,
                "entry_by_source": entry_by_source,
            }
        )

    for target, sources in sorted(targets.items()):
        if len(sources) > 1:
            rendered = ", ".join(_relative(root, source) for source in sources)
            blockers.append(
                f"package-successor: competing sealed carriers for "
                f"{_relative(root, target)}: {rendered}"
            )
        for suffix in (".yaml", ".yml"):
            candidate = target.with_suffix(suffix)
            if candidate.is_file() and candidate.resolve() not in shared_packages:
                blockers.append(
                    "package-successor: competing writable package carrier: "
                    f"{_relative(root, candidate)}"
                )

    atoms, atom_diagnostics = collect_semantic_atoms(root)
    if atom_diagnostics:
        blockers.append(
            "package-successor: native atom inventory is invalid: "
            + atom_diagnostics[0].message
        )
    else:
        for atom in sorted(atoms.values(), key=lambda item: item.semantic_id):
            atom_field = _PACKAGE_FIELD_BY_CLASSIFICATION.get(
                (atom.semantic_type, atom.subtype)
            )
            if (
                atom_field is None
                or atom.emission_status != "accepted"
                or atom.semantic_id in inactive
            ):
                continue
            layer = _semantic_id_layer(atom.semantic_id)
            candidates = [
                package
                for package in packages
                if package["layer"] == layer
                and _package_projection_contains(package, atom_field, atom.semantic_id)
            ]
            if len(candidates) != 1:
                condition = (
                    "no current package projection"
                    if not candidates
                    else ("ambiguous current package projections")
                )
                blockers.append(
                    f"package-successor: active native ID has {condition}: "
                    f"{atom.semantic_id}"
                )
                continue
            values = candidates[0]["data"].get(atom_field)
            if not isinstance(values, list):
                blockers.append(
                    f"package-successor: {atom_field} is not a list for "
                    f"{atom.semantic_id}"
                )
            elif atom.semantic_id not in values:
                values.append(atom.semantic_id)

    successors: list[PackageSuccessor] = []
    for package in packages:
        source = package["source"]
        target = package["target"]
        data = package["data"]
        for field in _PACKAGE_ARTIFACT_BY_FIELD:
            values = data.get(field)
            if isinstance(values, list) and all(
                isinstance(value, str) for value in values
            ):
                data[field] = sorted(dict.fromkeys(values))
        source_text = source.read_bytes().decode("utf-8")
        try:
            target_text = dump_toml(data)
        except TomlCodecError as error:
            blockers.append(
                f"package-successor: cannot render {_relative(root, target)}: {error}"
            )
            continue
        status = "pending"
        if target.exists():
            if target.is_symlink() or not target.is_file():
                blockers.append(
                    "package-successor: current successor is not a regular file: "
                    f"{_relative(root, target)}"
                )
                status = "conflicting"
            else:
                current = target.read_text(encoding="utf-8")
                if current == target_text:
                    status = "current"
                else:
                    status = (
                        "incomplete"
                        if _successor_incomplete(current, data)
                        else "conflicting"
                    )
                    blockers.append(
                        f"package-successor: {status} current successor: "
                        f"{_relative(root, target)}"
                    )
        successors.append(
            PackageSuccessor(source, target, source_text, target_text, status)
        )
    return sorted(successors, key=lambda item: _relative(root, item.source)), blockers


def _inactive_semantic_ids(root: Path) -> tuple[set[str], list[str]]:
    ledger, blockers = _load_history_ledger(
        root,
        (
            "00_project/lifecycle",
            "dset/scopes/gov/governance/lifecycle",
            "dset/governance/lifecycle",
        ),
        "semantic lifecycle",
    )
    if ledger is None:
        return set(), blockers
    events = ledger.get("events")
    if not isinstance(events, list):
        return set(), blockers + [
            "package-successor: semantic lifecycle requires events"
        ]
    current: dict[str, str] = {}
    for event in events:
        if isinstance(event, dict) and isinstance(event.get("atom_id"), str):
            current[str(event["atom_id"])] = str(event.get("event", ""))
    return {
        identifier for identifier, state in current.items() if state in TERMINAL_STATES
    }, blockers


def _reconcile_package_artifact_paths(
    root: Path,
    source: Path,
    data: dict[str, Any],
    path_mapping: dict[Path, Path],
    blockers: list[str],
) -> None:
    artifacts = data.get("artifacts")
    if not isinstance(artifacts, dict):
        return
    for key, raw in list(artifacts.items()):
        if not isinstance(raw, str):
            continue
        candidate = Path(raw)
        if candidate.is_absolute() or "\\" in raw or ".." in candidate.parts:
            blockers.append(
                f"package-successor: artifact path is not package-relative: "
                f"{_relative(root, source)}#{key}"
            )
            continue
        current = (source.parent / candidate).resolve()
        target = path_mapping.get(current)
        if target is not None:
            artifacts[key] = os.path.relpath(target, source.parent).replace(os.sep, "/")


def _package_projection_contains(
    package: dict[str, Any], field: str, identifier: str
) -> bool:
    data = package["data"]
    artifacts = data.get("artifacts")
    if not isinstance(artifacts, dict):
        return False
    raw = artifacts.get(_PACKAGE_ARTIFACT_BY_FIELD[field])
    if not isinstance(raw, str):
        return False
    source = package["source"]
    path = (source.parent / raw).resolve()
    entry = package["entry_by_source"].get(path)
    try:
        text = (
            entry.after_text if entry is not None else path.read_text(encoding="utf-8")
        )
    except (OSError, UnicodeError):
        return False
    return identifier in text


def _semantic_id_layer(identifier: str) -> str | None:
    parts = identifier.split("-")
    matches = [layer for layer, token in LAYER_ID_TOKENS.items() if token in parts]
    return matches[0] if len(matches) == 1 else None


def _successor_incomplete(current: str, expected: dict[str, Any]) -> bool:
    try:
        actual = load_toml(current)
    except TomlCodecError:
        return False
    for key, expected_value in expected.items():
        actual_value = actual.get(key)
        if isinstance(expected_value, list):
            if not isinstance(actual_value, list) or any(
                item not in actual_value for item in expected_value
            ):
                return True
        elif isinstance(expected_value, dict):
            if not isinstance(actual_value, dict) or any(
                actual_value.get(child) != value
                for child, value in expected_value.items()
            ):
                return True
        elif actual_value != expected_value:
            return True
    return False


def _copy_structured(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _copy_structured(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_copy_structured(item) for item in value]
    return value


def _exception(root: Path, path: Path, category: str) -> dict[str, object]:
    return {
        "path": _relative(root, path),
        "category": category,
        "authority": "non-authoritative",
        "retained": True,
    }


def _external_contract_exception(
    root: Path, path: Path, category: str
) -> dict[str, object]:
    return {
        "path": _relative(root, path),
        "category": category,
        "authority": "canonical-external-contract",
        "retained": True,
        "editable_toml_duplicate": False,
    }


def _is_owned_structured(root: Path, path: Path) -> bool:
    relative = path.relative_to(root)
    return (
        bool(relative.parts)
        and relative.parts[0] == "dset"
        and path.suffix.lower() in _STRUCTURED_SUFFIXES
    )


def _is_owned_markdown(root: Path, path: Path) -> bool:
    relative = path.relative_to(root)
    return bool(relative.parts) and relative.parts[0] == "dset" and path.suffix == ".md"


def _structured_entry(root: Path, source: Path) -> MigrationEntry:
    before = source.read_text(encoding="utf-8")
    if source.suffix.lower() == ".json":
        value = json.loads(before)
    else:
        value = load_yaml(before)
    if not isinstance(value, dict):
        raise TomlMigrationError("DSET structured root must be a mapping")
    if source.name == "artifact-types.yaml":
        _reconcile_artifact_type_patterns(value)
    normalizations = _normalize_allowed_nulls(
        value,
        _relative(root, source),
    )
    target = source.with_suffix(".toml")
    return MigrationEntry(
        "structured",
        source,
        target,
        before,
        dump_toml(value),
        normalizations,
    )


def _reconcile_artifact_type_patterns(value: dict[str, Any]) -> None:
    """Move only DSET-owned path rules; retain boundary YAML classifiers."""

    rules = value.get("path_rules")
    if not isinstance(rules, list):
        return
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        pattern = rule.get("pattern")
        if not isinstance(pattern, str) or pattern.startswith((".github/", "skills/")):
            continue
        if pattern.endswith(".yaml"):
            rule["pattern"] = pattern[: -len(".yaml")] + ".toml"
        elif pattern.endswith(".yml"):
            rule["pattern"] = pattern[: -len(".yml")] + ".toml"


def _frontmatter_entry(root: Path, source: Path) -> MigrationEntry | None:
    before = source.read_text(encoding="utf-8")
    parsed = _yaml_frontmatter(before)
    if parsed is None:
        return None
    metadata, body = parsed
    if not isinstance(metadata, dict):
        raise TomlMigrationError("Markdown frontmatter root must be a mapping")
    normalizations = _normalize_allowed_nulls(
        metadata,
        _relative(root, source),
    )
    after = "+++\n" + dump_toml(metadata) + "+++\n" + body
    return MigrationEntry(
        "markdown-frontmatter",
        source,
        source,
        before,
        after,
        normalizations,
    )


def _yaml_frontmatter(text: str) -> tuple[dict[str, Any], str] | None:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            metadata = "".join(lines[1:index])
            try:
                value = load_yaml(metadata)
            except YamlSubsetError as error:
                raise TomlMigrationError(str(error)) from error
            if not isinstance(value, dict):
                raise TomlMigrationError("frontmatter root must be a mapping")
            return value, "".join(lines[index + 1 :])
    raise TomlMigrationError("frontmatter opening delimiter has no closing delimiter")


def _normalize_allowed_nulls(value: dict[str, Any], source: str) -> tuple[str, ...]:
    """Drop only null fields whose omission has the declared same meaning."""

    normalized: list[str] = []

    def visit(current: object, path: tuple[str, ...]) -> None:
        if isinstance(current, dict):
            for key in list(current):
                item = current[key]
                key_path = path + (key,)
                if item is None and _null_is_omittable(source, key_path):
                    del current[key]
                    normalized.append(".".join(key_path))
                else:
                    visit(item, key_path)
        elif isinstance(current, list):
            for index, item in enumerate(current):
                visit(item, path + (str(index),))

    visit(value, ())
    return tuple(normalized)


def _null_is_omittable(source: str, path: tuple[str, ...]) -> bool:
    if path[-2:] == ("promotion", "parent_scope"):
        return True
    if source.endswith("/intake.yaml") or source.endswith("/intake.yml"):
        return len(path) == 3 and path[0] == "items" and path[2] == "decision"
    return (
        (
            source.endswith("/pull-requests.yaml")
            or source.endswith("/pull-requests.yml")
        )
        and len(path) == 3
        and path[0] == "pull_requests"
        and path[2] == "merge_commit"
    )


def _has_yaml_frontmatter(path: Path) -> bool:
    try:
        return path.read_text(encoding="utf-8").startswith("---")
    except (OSError, UnicodeError):
        return False


def _runtime_readiness(
    root: Path,
    entries: list[MigrationEntry],
    references: list[ReferenceRewrite],
    exceptions: list[dict[str, object]],
    successors: list[PackageSuccessor],
    preserved_structured: tuple[Path, ...] = (),
) -> tuple[dict[str, object], list[str]]:
    pending_successors = [item for item in successors if item.status == "pending"]
    if not entries and not references and not pending_successors:
        return {
            "evidence_path": _RUNTIME_READINESS_PATH,
            "target_count": 0,
            "preserved_input_count": 0,
            "status": "not-required",
        }, []
    target_digests = _target_digests(root, entries, references, successors)
    targets = _expected_target_paths(root, entries, references, successors)
    preserved_inputs = _preserved_input_digests(root, successors, preserved_structured)
    input_digest = _migration_input_digest(root, entries, references, exceptions)
    evidence_path = root / _RUNTIME_READINESS_PATH
    result: dict[str, object] = {
        "evidence_path": _RUNTIME_READINESS_PATH,
        "target_count": len(targets),
        "preserved_input_count": len(preserved_inputs),
    }
    if not (root / "dset_toolchain").is_dir():
        result["status"] = "not-applicable"
        return result, []
    if not targets:
        result["status"] = "not-required"
        return result, []
    if not evidence_path.is_file() or evidence_path.is_symlink():
        result["status"] = "missing"
        return result, [
            "runtime-readiness: missing explicit TOML runtime mapping evidence "
            f"at {_RUNTIME_READINESS_PATH}"
        ]
    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        result["status"] = "invalid"
        return result, [f"runtime-readiness: invalid evidence: {error}"]
    mapped = evidence.get("targets") if isinstance(evidence, dict) else None
    if not isinstance(mapped, dict) or not all(
        isinstance(path, str) and isinstance(digest, str)
        for path, digest in mapped.items()
    ):
        result["status"] = "invalid"
        return result, ["runtime-readiness: evidence targets must map paths to digests"]
    mapped_planned = (
        evidence.get("planned_targets", mapped) if isinstance(evidence, dict) else None
    )
    if not isinstance(mapped_planned, dict) or not all(
        isinstance(path, str) and isinstance(digest, str)
        for path, digest in mapped_planned.items()
    ):
        result["status"] = "invalid"
        return result, [
            "runtime-readiness: evidence planned_targets must map paths to digests"
        ]
    mapped_preserved = (
        evidence.get("preserved_inputs", {}) if isinstance(evidence, dict) else None
    )
    if not isinstance(mapped_preserved, dict) or not all(
        isinstance(path, str) and isinstance(digest, str)
        for path, digest in mapped_preserved.items()
    ):
        result["status"] = "invalid"
        return result, [
            "runtime-readiness: evidence preserved_inputs must map paths to digests"
        ]
    missing_or_stale = sorted(set(targets).symmetric_difference(mapped))
    missing_or_stale.extend(
        path
        for path in sorted(set(target_digests).symmetric_difference(mapped_planned))
    )
    missing_or_stale.extend(
        path
        for path in sorted(set(target_digests) & set(mapped_planned))
        if mapped_planned[path] != target_digests[path]
    )
    missing_or_stale.extend(
        f"preserved:{path}"
        for path in sorted(set(preserved_inputs).symmetric_difference(mapped_preserved))
    )
    missing_or_stale.extend(
        f"preserved:{path}"
        for path in sorted(set(preserved_inputs) & set(mapped_preserved))
        if mapped_preserved[path] != preserved_inputs[path]
    )
    if evidence.get("input_sha256") != input_digest:
        missing_or_stale.append("input_sha256")
    source_tool_digest = evidence.get("source_tool_sha256")
    current_tool_digest = _tool_digest(root)
    if source_tool_digest != current_tool_digest:
        missing_or_stale.append("source_tool_sha256")
    if evidence.get("source_commit") != _git_head(root):
        missing_or_stale.append("source_commit")
    missing_or_stale = sorted(set(missing_or_stale))
    result["status"] = "current" if not missing_or_stale else "stale"
    result["mapped_target_count"] = len(mapped)
    result["missing_or_stale"] = missing_or_stale
    if missing_or_stale:
        return result, [
            "runtime-readiness: stale or missing mapping for "
            + ", ".join(missing_or_stale)
        ]
    return result, []


def _target_digests(
    root: Path,
    entries: list[MigrationEntry],
    references: list[ReferenceRewrite],
    successors: Iterable[PackageSuccessor] = (),
) -> dict[str, str]:
    writes = {entry.target: entry.after_text for entry in entries}
    writes.update({successor.target: successor.target_text for successor in successors})
    grouped: dict[Path, list[ReferenceRewrite]] = {}
    for reference in references:
        grouped.setdefault(reference.path, []).append(reference)
    source_targets = {entry.source: entry.target for entry in entries}
    for path, path_references in grouped.items():
        target = source_targets.get(path, path)
        current = writes.get(target)
        if current is None:
            current = path.read_text(encoding="utf-8")
        for reference in sorted(
            path_references, key=lambda item: len(item.source), reverse=True
        ):
            current = current.replace(reference.source, reference.target)
        writes[target] = current
    return {
        _relative(root, path): _sha256(content)
        for path, content in sorted(writes.items())
    }


def _expected_target_paths(
    root: Path,
    entries: list[MigrationEntry],
    references: list[ReferenceRewrite],
    successors: Iterable[PackageSuccessor] = (),
) -> set[str]:
    paths = set(_target_digests(root, entries, references, successors))
    bundle = root / "dset_toolchain" / "bootstrap_bundle.json"
    builder = root / "scripts" / "build_bootstrap_bundle.py"
    if bundle.is_file() and builder.is_file():
        paths.add(bundle.relative_to(root).as_posix())
    return paths


def _preserved_input_digests(
    root: Path,
    successors: Iterable[PackageSuccessor],
    preserved_structured: Iterable[Path] = (),
) -> dict[str, str]:
    digests = {
        _relative(root, successor.source): successor.source_digest
        for successor in successors
    }
    digests.update(
        {
            _relative(root, path): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in preserved_structured
        }
    )
    return dict(sorted(digests.items()))


def _migration_input_digest(
    root: Path,
    entries: list[MigrationEntry],
    references: list[ReferenceRewrite],
    exceptions: list[dict[str, object]],
) -> str:
    reference_paths = sorted({reference.path for reference in references})
    retained_paths = sorted(
        root / str(item["path"])
        for item in exceptions
        if item.get("category") != "machine-local-runtime-journal"
        and isinstance(item.get("path"), str)
    )
    payload = {
        "entries": [
            {
                "kind": entry.kind,
                "source": _relative(root, entry.source),
                "target": _relative(root, entry.target),
                "source_sha256": entry.source_digest,
                "target_sha256": entry.target_digest,
            }
            for entry in entries
        ],
        "references": [
            {
                "path": _relative(root, reference.path),
                "source": reference.source,
                "target": reference.target,
                "count": reference.count,
            }
            for reference in references
        ],
        "reference_sources": {
            _relative(root, path): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in reference_paths
        },
        "retained_sources": {
            _relative(root, path): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in retained_paths
            if path.is_file()
        },
    }
    return _sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    )


def _validate_proven_output(plan: MigrationPlan) -> None:
    evidence_path = plan.root / _RUNTIME_READINESS_PATH
    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise TomlMigrationError(
            f"cannot read runtime readiness evidence: {error}"
        ) from error
    mapped = evidence.get("targets") if isinstance(evidence, dict) else None
    if not isinstance(mapped, dict):
        raise TomlMigrationError("runtime readiness evidence has no target digests")
    expected_paths = _expected_target_paths(
        plan.root,
        list(plan.entries),
        list(plan.references),
        plan.package_successors,
    )
    mismatches: list[str] = sorted(expected_paths.symmetric_difference(mapped))
    for relative, expected in sorted(mapped.items()):
        if not isinstance(relative, str) or not isinstance(expected, str):
            mismatches.append(str(relative))
            continue
        path = plan.root / relative
        if not path.is_file():
            mismatches.append(relative)
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            mismatches.append(relative)
    preserved = evidence.get("preserved_inputs", {})
    expected_preserved = _preserved_input_digests(
        plan.root, plan.package_successors, plan.preserved_structured
    )
    if not isinstance(preserved, dict):
        mismatches.append("preserved_inputs")
    else:
        mismatches.extend(
            f"preserved:{relative}"
            for relative in sorted(
                set(expected_preserved).symmetric_difference(preserved)
            )
        )
        for relative, expected in sorted(expected_preserved.items()):
            path = plan.root / relative
            if (
                preserved.get(relative) != expected
                or not path.is_file()
                or hashlib.sha256(path.read_bytes()).hexdigest() != expected
            ):
                mismatches.append(f"preserved:{relative}")
    if mismatches:
        raise TomlMigrationError(
            "post-migration output differs from runtime readiness proof: "
            + ", ".join(mismatches)
        )


def _collision_blockers(
    root: Path,
    entries: list[MigrationEntry],
    successors: list[PackageSuccessor],
) -> list[str]:
    blockers: list[str] = []
    sources_by_target: dict[Path, list[Path]] = {}
    for entry in entries:
        sources_by_target.setdefault(entry.target, []).append(entry.source)
    successor_targets = {successor.target for successor in successors}
    for target, sources in sorted(sources_by_target.items()):
        if len(sources) > 1:
            listed = ", ".join(_relative(root, source) for source in sorted(sources))
            blockers.append(
                f"conversion: target collision {_relative(root, target)}: {listed}"
            )
        elif (
            target != sources[0] and target.exists() and target not in successor_targets
        ):
            blockers.append(
                f"conversion: target collision {_relative(root, target)} already exists"
            )
    return blockers


def _reference_rewrites(
    root: Path,
    paths: list[Path],
    entries: list[MigrationEntry],
    immutable: dict[Path, dict[str, object]] | None = None,
    successor_mapping: dict[Path, Path] | None = None,
    *,
    legacy_structured: set[Path] | None = None,
    historical_trace_sources: set[Path] | None = None,
    transition_sources: set[Path] | None = None,
) -> tuple[list[ReferenceRewrite], list[str]]:
    mapping = {
        entry.source: entry.target for entry in entries if entry.source != entry.target
    }
    mapping.update(successor_mapping or {})
    if not mapping:
        return [], []
    legacy_carriers = legacy_structured or set()
    historical_sources = historical_trace_sources or set()
    sealed_transition_sources = transition_sources or set()
    converting_sources = {entry.source for entry in entries}
    rewrites: list[ReferenceRewrite] = []
    blockers: list[str] = []
    for path in paths:
        if path in sealed_transition_sources:
            continue
        if path in legacy_carriers and path not in converting_sources:
            continue
        classification = _exception_classification(root, path, immutable)
        # Tests intentionally retain legacy YAML fixtures so one staged suite
        # can verify the compatibility readers after the production tree has
        # crossed to TOML.  They are not runtime reference carriers.
        if path.relative_to(root).parts[:1] == ("tests",):
            continue
        if path.stem == "legacy-authority":
            continue
        if path.stem == "artifact-types":
            # The registry contains both current path rules and intentionally
            # historical snapshot paths.  Its conversion reconciles only the
            # former structurally in ``_reconcile_artifact_type_patterns``.
            continue
        if (
            _is_runtime_source(root, path)
            or not _is_text_path(path)
            or classification is not None
            and str(classification["category"]) in _NON_REWRITABLE_EXCEPTIONS
        ):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        remaining = text
        path_mapping = mapping
        if _is_generated_traceability(root, path):
            path_mapping = {
                source: target
                for source, target in mapping.items()
                if source not in historical_sources
            }
        for source_text, target_texts in _reference_spellings(
            root, path, path_mapping
        ).items():
            count = remaining.count(source_text)
            if not count:
                continue
            if len(target_texts) != 1:
                rendered = ", ".join(sorted(target_texts))
                blockers.append(
                    "reference: ambiguous spelling "
                    f"{source_text} in {_relative(root, path)}: {rendered}"
                )
                continue
            target_text = next(iter(target_texts))
            rewrites.append(ReferenceRewrite(path, source_text, target_text, count))
            remaining = remaining.replace(source_text, target_text)
    return sorted(
        rewrites,
        key=lambda item: (_relative(root, item.path), item.source, item.target),
    ), blockers


def _is_generated_traceability(root: Path, path: Path) -> bool:
    relative = path.relative_to(root)
    return path.stem == "traceability" and "generated" in relative.parts


def _is_runtime_source(root: Path, path: Path) -> bool:
    relative = path.relative_to(root)
    return (
        path.suffix == ".py"
        and bool(relative.parts)
        and relative.parts[0] in {"dset_toolchain", "scripts"}
    )


def _reference_spellings(
    root: Path, referrer: Path, mapping: dict[Path, Path]
) -> dict[str, set[str]]:
    spellings: dict[str, set[str]] = {}
    for source, target in mapping.items():
        root_source = _relative(root, source)
        root_target = _relative(root, target)
        relative_source = _reference_spelling(source, referrer)
        relative_target = _reference_spelling(target, referrer)
        for source_text, target_text in (
            (root_source, root_target),
            (relative_source, relative_target),
            (f"./{relative_source}", f"./{relative_target}"),
            (source.name, target.name),
        ):
            spellings.setdefault(source_text, set()).add(target_text)
    return dict(sorted(spellings.items(), key=lambda item: (-len(item[0]), item[0])))


def _is_text_path(path: Path) -> bool:
    return path.suffix.lower() in {
        ".md",
        ".toml",
        ".yaml",
        ".yml",
        ".json",
        ".py",
        ".txt",
    }


def _reference_spelling(target: Path, referrer: Path) -> str:
    return os.path.relpath(target, referrer.parent).replace(os.sep, "/")


def _planned_writes(plan: MigrationPlan) -> dict[Path, str]:
    writes = {entry.target: entry.after_text for entry in plan.entries}
    writes.update(
        {
            successor.target: successor.target_text
            for successor in plan.package_successors
            if successor.status == "pending"
        }
    )
    grouped: dict[Path, list[ReferenceRewrite]] = {}
    for reference in plan.references:
        grouped.setdefault(reference.path, []).append(reference)
    source_targets = {entry.source: entry.target for entry in plan.entries}
    for path, references in grouped.items():
        target = source_targets.get(path, path)
        current = writes.get(target)
        if current is None:
            current = path.read_text(encoding="utf-8")
        for reference in sorted(
            references, key=lambda item: len(item.source), reverse=True
        ):
            current = current.replace(reference.source, reference.target)
        writes[target] = current
    return writes


def _preflight_apply(plan: MigrationPlan) -> None:
    for entry in plan.entries:
        if not entry.source.is_file():
            raise TomlMigrationError(
                f"source disappeared: {_relative(plan.root, entry.source)}"
            )
        current = entry.source.read_text(encoding="utf-8")
        if _sha256(current) != entry.source_digest:
            raise TomlMigrationError(
                f"source changed: {_relative(plan.root, entry.source)}"
            )
        if entry.target != entry.source and entry.target.exists():
            raise TomlMigrationError(
                f"target collision {_relative(plan.root, entry.target)}"
            )
    for successor in plan.package_successors:
        if not successor.source.is_file():
            raise TomlMigrationError(
                f"preserved package source disappeared: "
                f"{_relative(plan.root, successor.source)}"
            )
        if hashlib.sha256(successor.source.read_bytes()).hexdigest() != (
            successor.source_digest
        ):
            raise TomlMigrationError(
                f"preserved package source changed: "
                f"{_relative(plan.root, successor.source)}"
            )
        if successor.status == "pending" and successor.target.exists():
            raise TomlMigrationError(
                f"package successor appeared: {_relative(plan.root, successor.target)}"
            )
        if successor.status == "current" and (
            not successor.target.is_file()
            or hashlib.sha256(successor.target.read_bytes()).hexdigest()
            != successor.target_digest
        ):
            raise TomlMigrationError(
                f"package successor changed: {_relative(plan.root, successor.target)}"
            )


def _write_recovery_manifest(
    plan: MigrationPlan, backup_root: Path, originals: dict[Path, bytes | None]
) -> None:
    if backup_root.exists():
        shutil.rmtree(backup_root)
    backup_root.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    for index, path in enumerate(sorted(originals)):
        content = originals[path]
        record: dict[str, object] = {
            "path": _relative(plan.root, path),
            "existed": content is not None,
        }
        if content is not None:
            backup = backup_root / f"{index:04d}.bak"
            backup.write_bytes(content)
            record["backup"] = backup.name
            record["sha256"] = hashlib.sha256(content).hexdigest()
        records.append(record)
    manifest = {
        "schema_version": MIGRATION_SCHEMA_VERSION,
        "plan_digest": plan.digest,
        "root": str(plan.root),
        "files": records,
    }
    _atomic_write_text(
        backup_root / "manifest.json",
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
    )


def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    except OSError:
        temporary_path.unlink(missing_ok=True)
        raise


def _validate_staged_tree(plan: MigrationPlan, writes: dict[Path, str]) -> None:
    for entry in plan.entries:
        staged = writes[entry.target]
        if entry.kind in {
            "structured",
            "historical-envelope",
            "transition-registry",
        }:
            load_toml(staged)
        elif entry.kind == "immutable-links":
            continue
        else:
            if not staged.startswith("+++\n"):
                raise TomlMigrationError(
                    f"invalid TOML frontmatter {_relative(plan.root, entry.target)}"
                )
            closing = staged.find("\n+++\n", 4)
            if closing < 0:
                raise TomlMigrationError(
                    "missing TOML frontmatter delimiter "
                    f"{_relative(plan.root, entry.target)}"
                )
            load_toml(staged[4:closing])
    for successor in plan.package_successors:
        if hashlib.sha256(successor.source.read_bytes()).hexdigest() != (
            successor.source_digest
        ):
            raise TomlMigrationError(
                "selector-sealed package changed during migration: "
                f"{_relative(plan.root, successor.source)}"
            )
        rendered = successor.target.read_text(encoding="utf-8")
        load_toml(rendered)
        if _sha256(rendered) != successor.target_digest:
            raise TomlMigrationError(
                "package successor differs from planned output: "
                f"{_relative(plan.root, successor.target)}"
            )


def _render_bootstrap_bundle(root: Path) -> str:
    """Use the root-parameterized builder without trusting ambient imports."""

    script = root / "scripts" / "build_bootstrap_bundle.py"
    specification = importlib.util.spec_from_file_location("_dset_bundle", script)
    if specification is None or specification.loader is None:
        raise TomlMigrationError("cannot load bootstrap bundle builder")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    render = getattr(module, "render_bundle", None)
    if not callable(render):
        raise TomlMigrationError("bootstrap bundle builder has no render_bundle(root)")
    rendered = render(root)
    if not isinstance(rendered, str):
        raise TomlMigrationError("bootstrap bundle builder returned non-text output")
    return rendered


def _reconcile_migrated_authority(root: Path) -> None:
    """Rebase governed digests and derived views in a fresh interpreter."""

    module = root / "dset_toolchain" / "migration_reconcile.py"
    if not module.is_file():
        return
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "dset_toolchain.migration_reconcile", "."],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired as error:
        raise TomlMigrationError(
            "migrated authority reconciliation timed out"
        ) from error
    if completed.returncode:
        message = completed.stderr.strip() or completed.stdout.strip()
        raise TomlMigrationError(
            "migrated authority reconciliation failed"
            + (f": {message}" if message else f" (exit {completed.returncode})")
        )


def _validate_migrated_runtime(root: Path) -> None:
    """Run the migrated tree in a new interpreter before committing the cutover."""

    if not (root / "dset_toolchain").is_dir():
        return
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "dset_toolchain", "check", "."],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired as error:
        raise TomlMigrationError("migrated dset check timed out") from error
    if completed.returncode:
        message = completed.stderr.strip() or completed.stdout.strip()
        raise TomlMigrationError(
            "migrated dset check failed"
            + (f": {message}" if message else f" (exit {completed.returncode})")
        )


def prove_runtime_readiness(root: Path) -> dict[str, object]:
    """Prove the exact preview in a disposable migrated copy, then write evidence.

    The real repository is never migrated by this function.  It receives only
    the compact digest-bound proof after all fresh-process checks pass.
    """

    root = root.resolve()
    source_plan = plan_toml_migration(root)
    non_runtime_blockers = [
        blocker
        for blocker in source_plan.blockers
        if not blocker.startswith("runtime-readiness:")
    ]
    if non_runtime_blockers:
        raise TomlMigrationError("; ".join(non_runtime_blockers))
    if not (root / "dset_toolchain").is_dir():
        raise TomlMigrationError("runtime readiness is not applicable to this root")

    input_digest = _migration_input_digest(
        root,
        list(source_plan.entries),
        list(source_plan.references),
        list(source_plan.exceptions),
    )
    target_paths = _expected_target_paths(
        root,
        list(source_plan.entries),
        list(source_plan.references),
        source_plan.package_successors,
    )
    planned_targets = _target_digests(
        root,
        list(source_plan.entries),
        list(source_plan.references),
        source_plan.package_successors,
    )
    preserved_inputs = _preserved_input_digests(
        root, source_plan.package_successors, source_plan.preserved_structured
    )
    source_tool_digest = _tool_digest(root)
    with temporary_directory(prefix="dset-toml-proof-") as raw:
        staged, git_context = _stage_proof_tree(root, Path(raw))
        staged_plan = apply_toml_migration(staged, bypass_runtime_readiness=True)
        results = [git_context, *_proof_commands(staged)]
        targets = {
            relative: hashlib.sha256((staged / relative).read_bytes()).hexdigest()
            for relative in sorted(target_paths)
        }
        evidence: dict[str, object] = {
            "schema_version": 1,
            "source_commit": _git_head(root),
            "source_tool_sha256": source_tool_digest,
            "input_sha256": input_digest,
            "migrated_tool_sha256": _tool_digest(staged),
            "preserved_inputs": preserved_inputs,
            "planned_targets": planned_targets,
            "targets": targets,
            "proof": {
                "plan_digest": source_plan.digest,
                "applied_plan_digest": staged_plan.digest,
                "commands": results,
            },
        }
    _atomic_write_text(
        root / _RUNTIME_READINESS_PATH,
        json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
    )
    return evidence


def _proof_ignore(_directory: str, names: list[str]) -> set[str]:
    return {
        name
        for name in names
        if name
        in {
            ".git",
            ".venv",
            ".cache",
            ".uv-cache",
            "build",
            "dist",
            "__pycache__",
            ".mypy_cache",
            ".pytest_cache",
            ".ruff_cache",
        }
    }


def _stage_proof_tree(
    root: Path, temporary_root: Path
) -> tuple[Path, dict[str, object]]:
    """Stage exact Git authority plus inspected working bytes for proof."""

    git_root = _git_top_level(root)
    source_head = _git_head(root)
    if git_root is None or source_head is None:
        staged = temporary_root / "repository"
        shutil.copytree(root, staged, ignore=_proof_ignore)
        return staged, _initialize_synthetic_proof_head(staged)

    checkout = temporary_root / "repository"
    clone = _run_proof_git(
        root,
        [
            "git",
            "clone",
            "--local",
            "--shared",
            "--no-checkout",
            "--quiet",
            "--",
            str(git_root),
            str(checkout),
        ],
        "clone exact source history",
    )
    _run_proof_git(
        checkout,
        [
            "git",
            "-c",
            "core.autocrlf=false",
            "checkout",
            "--detach",
            "--force",
            "--quiet",
            source_head,
        ],
        "checkout exact source HEAD",
    )
    relative_root = root.relative_to(git_root)
    staged = checkout / relative_root
    _clear_proof_scope(staged, checkout)
    _overlay_proof_working_tree(root, staged)
    staged_head = _git_head(staged)
    if staged_head != source_head:
        raise TomlMigrationError(
            "isolated readiness checkout does not preserve source HEAD"
        )
    return staged, {
        "argv": ["git", "exact-readiness-head"],
        "returncode": 0,
        "stdout_sha256": _sha256(clone.stdout + clone.stderr),
        "stderr_sha256": _sha256(""),
        "head": staged_head,
    }


def _git_top_level(root: Path) -> Path | None:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode or not completed.stdout.strip():
        return None
    return Path(completed.stdout.strip()).resolve()


def _run_proof_git(
    root: Path, command: list[str], purpose: str
) -> subprocess.CompletedProcess[str]:
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        stdout = error.stdout if isinstance(error, subprocess.TimeoutExpired) else ""
        stderr = error.stderr if isinstance(error, subprocess.TimeoutExpired) else ""
        raise TomlMigrationError(
            f"cannot {purpose}" + _proof_output_tail(stdout, stderr)
        ) from error
    if completed.returncode:
        raise TomlMigrationError(
            f"cannot {purpose} (exit {completed.returncode})"
            + _proof_output_tail(completed.stdout, completed.stderr)
        )
    return completed


def _clear_proof_scope(staged: Path, checkout: Path) -> None:
    """Clear checked-out bytes while preserving the isolated Git database."""

    if staged != checkout:
        shutil.rmtree(staged, ignore_errors=True)
        staged.mkdir(parents=True)
        return
    for path in staged.iterdir():
        if path.name == ".git":
            continue
        if path.is_symlink() or path.is_file():
            path.unlink()
        else:
            shutil.rmtree(path)


def _overlay_proof_working_tree(root: Path, staged: Path) -> None:
    """Overlay tracked and untracked, nonignored working-tree bytes."""

    try:
        completed = subprocess.run(
            [
                "git",
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                ".",
            ],
            cwd=root,
            check=False,
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise TomlMigrationError("cannot inventory proof working tree") from error
    if completed.returncode:
        raise TomlMigrationError(
            "cannot inventory proof working tree"
            + _proof_output_tail(completed.stdout, completed.stderr)
        )
    for raw_path in completed.stdout.split(b"\0"):
        if not raw_path:
            continue
        relative = Path(os.fsdecode(raw_path))
        if (
            any(part in _IGNORED_TOP_LEVEL for part in relative.parts)
            or relative.parts[:1] == (".dset_runtime",)
            or relative.parts[:2] == (".dset", "runtime")
        ):
            continue
        source = root / relative
        target = staged / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_symlink():
            target.symlink_to(os.readlink(source))
        elif source.is_file():
            shutil.copy2(source, target)


def _proof_commands(root: Path) -> list[dict[str, object]]:
    check = [sys.executable, "-m", "dset_toolchain", "check", "."]
    tests = [
        sys.executable,
        "-m",
        "unittest",
        "tests.test_settings",
        "tests.test_layout",
        "tests.test_layered_validation",
        "tests.test_semantic_atoms",
        "tests.test_semantic_types",
        "tests.test_external_review",
        "tests.test_scaffold_archive",
        "tests.test_runtime",
        "tests.test_bootstrap",
        "tests.test_toml_migration",
    ]
    return [_run_proof_command(root, check), _run_proof_command(root, tests)]


def _run_proof_command(root: Path, command: list[str]) -> dict[str, object]:
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired as error:
        details = _proof_output_tail(error.stdout, error.stderr)
        raise TomlMigrationError(
            f"runtime readiness proof timed out: {' '.join(command)}{details}"
        ) from error
    result = {
        "argv": command,
        "returncode": completed.returncode,
        "stdout_sha256": _sha256(completed.stdout),
        "stderr_sha256": _sha256(completed.stderr),
    }
    if completed.returncode:
        raise TomlMigrationError(
            "runtime readiness proof failed: "
            + " ".join(command)
            + f" (exit {completed.returncode})"
            + _proof_output_tail(completed.stdout, completed.stderr)
        )
    return result


def _initialize_synthetic_proof_head(root: Path) -> dict[str, object]:
    """Create a deterministic local HEAD without importing the source Git store."""

    environment = dict(os.environ)
    environment.update(
        {
            "GIT_AUTHOR_DATE": "2000-01-01T00:00:00+00:00",
            "GIT_COMMITTER_DATE": "2000-01-01T00:00:00+00:00",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_ATTR_NOSYSTEM": "1",
        }
    )
    commands = (
        ["git", "-c", "init.defaultBranch=dset-proof", "init", "-q"],
        ["git", "-c", "core.autocrlf=false", "add", "-A"],
        [
            "git",
            "-c",
            "user.name=DSET Runtime Readiness",
            "-c",
            "user.email=dset-readiness@example.invalid",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "-q",
            "--no-gpg-sign",
            "-m",
            "DSET TOML runtime readiness snapshot",
        ],
    )
    output = []
    for command in commands:
        try:
            completed = subprocess.run(
                command,
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
                env=environment,
            )
        except subprocess.TimeoutExpired as error:
            raise TomlMigrationError(
                "synthetic readiness Git initialization timed out: "
                + " ".join(command)
                + _proof_output_tail(error.stdout, error.stderr)
            ) from error
        output.append(completed.stdout + completed.stderr)
        if completed.returncode:
            raise TomlMigrationError(
                "synthetic readiness Git initialization failed: "
                + " ".join(command)
                + f" (exit {completed.returncode})"
                + _proof_output_tail(completed.stdout, completed.stderr)
            )
    head = _git_head(root)
    if head is None:
        raise TomlMigrationError("synthetic readiness Git HEAD is unavailable")
    combined = "".join(output)
    return {
        "argv": ["git", "synthetic-readiness-head"],
        "returncode": 0,
        "stdout_sha256": _sha256(combined),
        "stderr_sha256": _sha256(""),
        "head": head,
    }


def _proof_output_tail(stdout: object, stderr: object, *, limit: int = 4000) -> str:
    sections: list[str] = []
    for label, raw in (("stdout", stdout), ("stderr", stderr)):
        if isinstance(raw, bytes):
            value = raw.decode("utf-8", errors="replace")
        elif isinstance(raw, str):
            value = raw
        else:
            value = ""
        value = value.strip()
        if value:
            sections.append(f"\n{label} tail:\n{value[-limit:]}")
    return "".join(sections)


def _tool_digest(root: Path) -> str:
    digest = hashlib.sha256()
    candidates = [
        path
        for directory in (root / "dset_toolchain", root / "scripts")
        if directory.is_dir()
        for path in directory.rglob("*.py")
    ]
    for path in sorted(candidates):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _git_head(root: Path) -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    value = completed.stdout.strip()
    return value if completed.returncode == 0 and value else None


def _restore(originals: dict[Path, bytes | None]) -> None:
    for path, content in originals.items():
        if content is None:
            path.unlink(missing_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)


def _remove_failed_recovery(backup_root: Path) -> None:
    """Remove the failed transaction record after its originals are restored."""

    shutil.rmtree(backup_root, ignore_errors=True)
    recovery_root = backup_root.parent
    with suppress(OSError):
        recovery_root.rmdir()


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _is_within_root(root: Path, path: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _count_by(values: Iterable[object]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = str(value)
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def _blocker_category(blocker: str) -> str:
    category, separator, _message = blocker.partition(":")
    return category if separator else "other"
