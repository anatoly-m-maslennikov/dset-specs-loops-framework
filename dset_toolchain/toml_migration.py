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
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .semantic_atoms import TERMINAL_STATES, collect_semantic_atoms
from .toml_codec import TomlCodecError
from .toml_codec import dumps as dump_toml
from .toml_codec import loads as load_toml
from .yaml_subset import YamlSubsetError
from .yaml_subset import load as load_structured
from .yaml_subset import loads as load_yaml

MIGRATION_SCHEMA_VERSION = "1.0"
_STRUCTURED_SUFFIXES = {".yaml", ".yml", ".json"}
_IGNORED_TOP_LEVEL = {".git", ".cache", ".venv", "build", "dist", "__pycache__"}
_RUNTIME_READINESS_PATH = ".dset/toml-migration-runtime-readiness.json"
_NON_REWRITABLE_EXCEPTIONS = {
    "cli-wire-json",
    "external-json-schema",
    "immutable-legacy-decision-carrier",
    "immutable-promoted-proof",
    "immutable-sealed-atom",
    "machine-local-runtime-journal",
    "retained-symlink",
}
_PACKAGE_FIELD_BY_CLASSIFICATION: dict[tuple[str, str | None], str] = {
    ("decision", "requirement"): "requirements",
    ("decision", "contract"): "contracts",
    ("decision", "user_story"): "stories",
    ("decision", "outcome"): "outcomes",
    ("qa", "test"): "tests",
    ("qa", "evaluation"): "evals",
}
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
    immutable, immutable_blockers, shared_packages = _immutable_classifications(
        root, paths
    )
    blockers.extend(immutable_blockers)
    for path in paths:
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
        root, shared_packages, entries
    )
    blockers.extend(successor_blockers)
    blockers.extend(_collision_blockers(root, entries, successors))
    successor_mapping = {
        successor.source: successor.target for successor in successors
    }
    references, reference_blockers = _reference_rewrites(
        root, paths, entries, immutable, successor_mapping
    )
    blockers.extend(reference_blockers)
    runtime_readiness, runtime_blockers = _runtime_readiness(
        root, entries, references, exceptions, successors
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
    deletes = {entry.source for entry in plan.entries if entry.source != entry.target}
    _preflight_apply(plan)
    backup_root = plan.root / ".dset" / "toml-migration-backups" / plan.digest
    bundle_path = plan.root / "dset_toolchain" / "bootstrap_bundle.json"
    regenerates_bundle = (
        bundle_path.is_file()
        and (plan.root / "scripts" / "build_bootstrap_bundle.py").is_file()
    )
    generated = {bundle_path} if regenerates_bundle else set()
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
        _reconcile_migrated_authority(plan.root)
        if regenerates_bundle:
            _atomic_write_text(bundle_path, _render_bootstrap_bundle(plan.root))
        _validate_staged_tree(plan, writes)
        _validate_migrated_runtime(plan.root)
        if not bypass_runtime_readiness and (plan.root / "dset_toolchain").is_dir():
            _validate_proven_output(plan)
    except Exception as error:
        _restore(originals)
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
        if path.is_symlink():
            paths.append(path)
            continue
        if path.is_file():
            paths.append(path)
    return sorted(paths, key=lambda item: item.relative_to(root).as_posix())


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
    if parts and parts[0] == ".dset":
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
                    str(record["path"]),
                    "immutable-sealed-atom",
                    "canonical-history",
                )

    legacy_ledger, legacy_errors = _load_history_ledger(
        root,
        (
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
                    selector = fragment.get("selector")
                    shared = selector != "whole-carrier"
                    _register_immutable_path(
                        root,
                        path_set,
                        classifications,
                        blockers,
                        raw_path,
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
                    )
                    if shared:
                        shared_paths.add((root / raw_path).resolve())

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
) -> None:
    """Verify the ledger-bound fragment without altering its historical carrier."""

    path = (root / raw_path).resolve()
    if not _is_within_root(root, path) or not path.is_file():
        return
    if not isinstance(selector, str) or not isinstance(declared_digest, str):
        blockers.append(
            f"immutability: legacy Decision fragment seal is incomplete: {raw_path}"
        )
        return
    if selector == "whole-carrier":
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
    else:
        field, separator, identifier = selector.partition(":")
        try:
            data = load_structured(path)
        except (OSError, UnicodeError, YamlSubsetError) as error:
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
    if actual != declared_digest:
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
        _reconcile_package_artifact_paths(
            root, source, data, path_mapping, blockers
        )
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
                and _package_projection_contains(
                    package, atom_field, atom.semantic_id
                )
            ]
            if len(candidates) != 1:
                condition = "no current package projection" if not candidates else (
                    "ambiguous current package projections"
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
        source_text = source.read_text(encoding="utf-8")
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
                    status = "incomplete" if _successor_incomplete(
                        current, data
                    ) else "conflicting"
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
        identifier
        for identifier, state in current.items()
        if state in TERMINAL_STATES
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
            entry.after_text
            if entry is not None
            else path.read_text(encoding="utf-8")
        )
    except (OSError, UnicodeError):
        return False
    return identifier in text


def _semantic_id_layer(identifier: str) -> str | None:
    parts = identifier.split("-")
    matches = [
        layer
        for layer in ("meta", "gov", "tool", "skill", "ops")
        if layer.upper() in parts
    ]
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
) -> tuple[dict[str, object], list[str]]:
    target_digests = _target_digests(root, entries, references, successors)
    targets = _expected_target_paths(root, entries, references, successors)
    preserved_inputs = _preserved_input_digests(root, successors)
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
        for path in sorted(set(targets) & set(mapped))
        if path in target_digests and mapped[path] != target_digests[path]
    )
    missing_or_stale.extend(
        f"preserved:{path}"
        for path in sorted(
            set(preserved_inputs).symmetric_difference(mapped_preserved)
        )
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
    writes.update(
        {successor.target: successor.target_text for successor in successors}
    )
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
    root: Path, successors: Iterable[PackageSuccessor]
) -> dict[str, str]:
    return {
        _relative(root, successor.source): successor.source_digest
        for successor in successors
    }


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
        plan.root, plan.package_successors
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
            target != sources[0]
            and target.exists()
            and target not in successor_targets
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
) -> tuple[list[ReferenceRewrite], list[str]]:
    mapping = {
        entry.source: entry.target for entry in entries if entry.source != entry.target
    }
    mapping.update(successor_mapping or {})
    if not mapping:
        return [], []
    rewrites: list[ReferenceRewrite] = []
    blockers: list[str] = []
    for path in paths:
        classification = _exception_classification(root, path, immutable)
        # Tests intentionally retain legacy YAML fixtures so one staged suite
        # can verify the compatibility readers after the production tree has
        # crossed to TOML.  They are not runtime reference carriers.
        if path.relative_to(root).parts[:1] == ("tests",):
            continue
        if path.stem == "legacy-authority":
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
        for source_text, target_texts in _reference_spellings(
            root, path, mapping
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
                f"package successor changed: "
                f"{_relative(plan.root, successor.target)}"
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
        if entry.kind == "structured":
            load_toml(staged)
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
    preserved_inputs = _preserved_input_digests(
        root, source_plan.package_successors
    )
    source_tool_digest = _tool_digest(root)
    with tempfile.TemporaryDirectory(
        prefix="dset-toml-proof-",
        dir=root.parent,
        ignore_cleanup_errors=True,
    ) as raw:
        staged = Path(raw) / "repository"
        shutil.copytree(root, staged, ignore=_proof_ignore)
        staged_plan = apply_toml_migration(staged, bypass_runtime_readiness=True)
        results = _proof_commands(staged)
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
            ".dset",
            "build",
            "dist",
            "__pycache__",
            ".mypy_cache",
            ".pytest_cache",
            ".ruff_cache",
        }
    }


def _proof_commands(root: Path) -> list[dict[str, object]]:
    commands = [
        [sys.executable, "-m", "dset_toolchain", "check", "."],
        [
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
        ],
    ]
    results: list[dict[str, object]] = []
    for command in commands:
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
            raise TomlMigrationError(
                f"runtime readiness proof timed out: {' '.join(command)}"
            ) from error
        result = {
            "argv": command,
            "returncode": completed.returncode,
            "stdout_sha256": _sha256(completed.stdout),
            "stderr_sha256": _sha256(completed.stderr),
        }
        results.append(result)
        if completed.returncode:
            raise TomlMigrationError(
                "runtime readiness proof failed: "
                + " ".join(command)
                + f" (exit {completed.returncode})"
            )
    return results


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
