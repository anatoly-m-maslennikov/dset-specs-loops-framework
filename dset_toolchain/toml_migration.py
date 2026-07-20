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

from .toml_codec import TomlCodecError
from .toml_codec import dumps as dump_toml
from .toml_codec import loads as load_toml
from .yaml_subset import YamlSubsetError
from .yaml_subset import loads as load_yaml

MIGRATION_SCHEMA_VERSION = "1.0"
_STRUCTURED_SUFFIXES = {".yaml", ".yml", ".json"}
_IGNORED_TOP_LEVEL = {".git", ".cache", ".venv", "build", "dist", "__pycache__"}
_RUNTIME_READINESS_PATH = ".dset/toml-migration-runtime-readiness.json"
_NON_REWRITABLE_EXCEPTIONS = {
    "cli-wire-json",
    "external-json-schema",
    "machine-local-runtime-journal",
    "retained-symlink",
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
class MigrationPlan:
    root: Path
    entries: tuple[MigrationEntry, ...]
    exceptions: tuple[dict[str, object], ...]
    references: tuple[ReferenceRewrite, ...]
    blockers: tuple[str, ...]
    runtime_readiness: dict[str, object]

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
            "exceptions": list(self.exceptions),
            "blockers": list(self.blockers),
            "runtime_readiness": self.runtime_readiness,
            "counts": {
                "changes": len(self.entries),
                "changes_by_kind": changes_by_kind,
                "reference_rewrites": len(self.references),
                "reference_occurrences": sum(
                    item.count for item in self.references
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
    for path in paths:
        classification = _exception_classification(root, path)
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
    blockers.extend(_collision_blockers(root, entries))
    references, reference_blockers = _reference_rewrites(root, paths, entries)
    blockers.extend(reference_blockers)
    runtime_readiness, runtime_blockers = _runtime_readiness(
        root, entries, references
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
    )


def apply_toml_migration(
    root: Path, *, bypass_runtime_readiness: bool = False
) -> MigrationPlan:
    """Apply a fully planned migration with backup-and-restore recovery."""

    plan = plan_toml_migration(root, bypass_runtime_readiness=bypass_runtime_readiness)
    if not plan.ready:
        raise TomlMigrationError("; ".join(plan.blockers))
    if not plan.entries:
        return plan

    writes = _planned_writes(plan)
    deletes = {entry.source for entry in plan.entries if entry.source != entry.target}
    _preflight_apply(plan)
    backup_root = (
        plan.root / ".dset" / "toml-migration-backups" / plan.digest
    )
    bundle_path = plan.root / "dset_toolchain" / "bootstrap_bundle.json"
    regenerates_bundle = bundle_path.is_file() and (
        plan.root / "scripts" / "build_bootstrap_bundle.py"
    ).is_file()
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


def _exception_classification(root: Path, path: Path) -> dict[str, object] | None:
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
        source.endswith("/pull-requests.yaml")
        or source.endswith("/pull-requests.yml")
    ) and len(path) == 3 and path[0] == "pull_requests" and path[2] == "merge_commit"


def _has_yaml_frontmatter(path: Path) -> bool:
    try:
        return path.read_text(encoding="utf-8").startswith("---")
    except (OSError, UnicodeError):
        return False


def _runtime_readiness(
    root: Path,
    entries: list[MigrationEntry],
    references: list[ReferenceRewrite],
) -> tuple[dict[str, object], list[str]]:
    targets = _target_digests(root, entries, references)
    evidence_path = root / _RUNTIME_READINESS_PATH
    result: dict[str, object] = {
        "evidence_path": _RUNTIME_READINESS_PATH,
        "target_count": len(targets),
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
    missing_or_stale = sorted(
        set(targets).symmetric_difference(mapped)
        | {path for path, digest in targets.items() if mapped.get(path) != digest}
    )
    source_tool_digest = evidence.get("source_tool_sha256")
    current_tool_digest = _tool_digest(root)
    if source_tool_digest != current_tool_digest:
        missing_or_stale.append("source_tool_sha256")
    if evidence.get("source_commit") != _git_head(root):
        missing_or_stale.append("source_commit")
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
) -> dict[str, str]:
    if not entries:
        return {}
    writes = {entry.target: entry.after_text for entry in entries}
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


def _collision_blockers(root: Path, entries: list[MigrationEntry]) -> list[str]:
    blockers: list[str] = []
    sources_by_target: dict[Path, list[Path]] = {}
    for entry in entries:
        sources_by_target.setdefault(entry.target, []).append(entry.source)
    for target, sources in sorted(sources_by_target.items()):
        if len(sources) > 1:
            listed = ", ".join(_relative(root, source) for source in sorted(sources))
            blockers.append(
                f"conversion: target collision {_relative(root, target)}: {listed}"
            )
        elif target != sources[0] and target.exists():
            blockers.append(
                "conversion: target collision "
                f"{_relative(root, target)} already exists"
            )
    return blockers


def _reference_rewrites(
    root: Path, paths: list[Path], entries: list[MigrationEntry]
) -> tuple[list[ReferenceRewrite], list[str]]:
    mapping = {
        entry.source: entry.target
        for entry in entries
        if entry.source != entry.target
    }
    if not mapping:
        return [], []
    rewrites: list[ReferenceRewrite] = []
    blockers: list[str] = []
    for path in paths:
        classification = _exception_classification(root, path)
        # Tests intentionally retain legacy YAML fixtures so one staged suite
        # can verify the compatibility readers after the production tree has
        # crossed to TOML.  They are not runtime reference carriers.
        if path.relative_to(root).parts[:1] == ("tests",):
            continue
        if (
            not _is_text_path(path)
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

    targets = _target_digests(
        root, list(source_plan.entries), list(source_plan.references)
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
        evidence: dict[str, object] = {
            "schema_version": 1,
            "source_commit": _git_head(root),
            "source_tool_sha256": source_tool_digest,
            "migrated_tool_sha256": _tool_digest(staged),
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
