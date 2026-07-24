"""Move schema-1.3 layer carriers to visibly ordered directory names.

The migration keeps logical layer IDs unchanged, records byte-exact moves for
immutable atom/evidence carriers, updates their current carrier pointers, and
rewrites mutable current-path references. It is repository-specific and
idempotent after a successful cutover.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dset_toolchain.carrier_transitions import (  # noqa: E402
    git_blob,
    git_commit_time,
    git_head,
    relocation_record,
    render_ledger,
    semantic_sha256,
    transition_id,
)
from dset_toolchain.frontmatter import parse as parse_frontmatter  # noqa: E402
from dset_toolchain.layout import LAYER_DIRECTORIES  # noqa: E402
from dset_toolchain.toml_codec import dumps as dump_toml  # noqa: E402
from dset_toolchain.toml_codec import load as load_toml  # noqa: E402

AUTHORITY = "DSET-REQUIREMENT-GOV-044"
SESSION = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
IMMUTABLE_OWNERS = frozenset({"decision", "question", "problem", "qa", "evidence"})
TEXT_SUFFIXES = frozenset({".json", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"})
ATOMS = ROOT / "00_project/atoms.toml"
LEGACY_AUTHORITY = ROOT / "00_project/legacy-authority.toml"
TRANSITIONS = ROOT / "00_project/migrations/carrier-transitions.toml"


def _git_lines(*arguments: str) -> list[str]:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in completed.stdout.splitlines() if line]


def _tracked_layer_files() -> list[Path]:
    prefixes = [f".dset/{layer}" for layer in LAYER_DIRECTORIES]
    return [ROOT / relative for relative in _git_lines("ls-files", *prefixes)]


def _protected_transition_targets() -> dict[str, dict[str, Any]]:
    data = load_toml(TRANSITIONS)
    protected: dict[str, dict[str, Any]] = {}
    for item in data.get("transitions", []):
        if not isinstance(item, dict):
            continue
        current = item.get("current_path")
        digest = item.get("current_sha256")
        if not isinstance(current, str) or not isinstance(digest, str):
            continue
        relative = Path(current)
        if len(relative.parts) < 3 or relative.parts[:1] != (".dset",):
            continue
        if relative.parts[1] not in LAYER_DIRECTORIES:
            continue
        entry = protected.setdefault(
            current,
            {
                "current_sha256": digest,
                "carrier_ids": set(),
                "semantic_ids": set(),
            },
        )
        if entry["current_sha256"] != digest:
            raise RuntimeError(f"conflicting protected carrier digests: {current}")
        entry["carrier_ids"].update(item.get("carrier_ids", []))
        entry["semantic_ids"].update(item.get("semantic_ids", []))
    return protected


def _target(source: Path) -> Path:
    relative = source.relative_to(ROOT / ".dset")
    layer, *tail = relative.parts
    return ROOT / ".dset" / LAYER_DIRECTORIES[layer] / Path(*tail)


def _is_immutable(path: Path) -> bool:
    relative = path.relative_to(ROOT / ".dset")
    return len(relative.parts) > 2 and relative.parts[1] in IMMUTABLE_OWNERS


def _metadata(path: Path) -> dict[str, Any]:
    if path.suffix != ".md":
        return {}
    parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
    return parsed[0] if parsed is not None and isinstance(parsed[0], dict) else {}


def _identities(path: Path) -> tuple[list[str], list[str]]:
    metadata = _metadata(path)
    carrier = metadata.get("artifact_id")
    semantic = metadata.get("semantic_id")
    carriers = [carrier] if isinstance(carrier, str) else []
    semantics = [semantic] if isinstance(semantic, str) else []
    return carriers, semantics


def _sealed_relocation_record(
    original: str,
    target: Path,
    protected: dict[str, Any],
) -> dict[str, Any]:
    digest = str(protected["current_sha256"])
    if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        raise RuntimeError(f"protected carrier bytes changed before move: {original}")
    blob = git_blob(ROOT, original)
    head = git_head(ROOT)
    if blob is None or head is None:
        raise RuntimeError(f"protected carrier has no source Git return: {original}")
    semantics = semantic_sha256({"carrier_sha256": digest})
    return {
        "id": transition_id(original, digest),
        "kind": "carrier_relocation",
        "authority_decision": AUTHORITY,
        "original_path": original,
        "original_format": Path(original).suffix.lstrip("."),
        "original_sha256": digest,
        "source_git_blob": blob,
        "current_path": target.relative_to(ROOT).as_posix(),
        "current_format": target.suffix.lstrip("."),
        "current_sha256": digest,
        "source_semantic_sha256": semantics,
        "current_semantic_sha256": semantics,
        "null_paths": [],
        "declared_loss": [],
        "source_commit": head,
        "transitioned_at": git_commit_time(ROOT),
        "llm_session_ids": [SESSION],
        "carrier_ids": sorted(protected["carrier_ids"]),
        "semantic_ids": sorted(protected["semantic_ids"]),
    }


def _repair_completed_cutover() -> None:
    data = load_toml(TRANSITIONS)
    existing = {
        str(item.get("original_path"))
        for item in data.get("transitions", [])
        if isinstance(item, dict)
        and item.get("authority_decision") == AUTHORITY
        and item.get("kind") == "carrier_relocation"
    }
    additions: list[dict[str, Any]] = []
    for original, protected in _protected_transition_targets().items():
        if original in existing:
            continue
        source = ROOT / original
        target = _target(source)
        if not target.is_file():
            raise RuntimeError(f"moved protected carrier is missing: {target}")
        additions.append(_sealed_relocation_record(original, target, protected))
    if additions:
        TRANSITIONS.write_text(render_ledger(ROOT, additions), encoding="utf-8")


def _replace_current_carrier(
    data: dict[str, Any],
    section: str,
    moves: dict[str, dict[str, Any]],
) -> None:
    records = data.get(section)
    if not isinstance(records, list):
        return
    for record in records:
        if not isinstance(record, dict):
            continue
        active = record.get("current_path", record.get("path"))
        move = moves.get(str(active))
        if move is None:
            continue
        record["current_path"] = move["current_path"]
        record["current_sha256"] = move["current_sha256"]
        record["transition_id"] = move["id"]


def _update_legacy_authority(moves: dict[str, dict[str, Any]]) -> None:
    data = load_toml(LEGACY_AUTHORITY)
    records = data.get("records")
    if not isinstance(records, list):
        return
    for record in records:
        fragments = record.get("fragments") if isinstance(record, dict) else None
        if not isinstance(fragments, list):
            continue
        for fragment in fragments:
            if not isinstance(fragment, dict):
                continue
            active = fragment.get("current_path", fragment.get("path"))
            move = moves.get(str(active))
            if move is None:
                continue
            fragment["current_path"] = move["current_path"]
            fragment["current_sha256"] = move["current_sha256"]
            fragment["transition_id"] = move["id"]
    LEGACY_AUTHORITY.write_text(dump_toml(data), encoding="utf-8")


def _rewrite_mutable_text(immutable_targets: set[Path]) -> None:
    replacements: list[tuple[str, str]] = []
    for layer, directory in LAYER_DIRECTORIES.items():
        replacements.extend(
            (
                (f".dset/{layer}", f".dset/{directory}"),
                (f"../{layer}", f"../{directory}"),
            )
        )
    candidates: set[Path] = {ROOT / relative for relative in _git_lines("ls-files")}
    for source in _tracked_layer_files():
        candidates.discard(source)
        candidates.add(_target(source))
    candidates.add(Path(__file__).resolve())
    for path in sorted(candidates):
        if (
            not path.is_file()
            or path.suffix.lower() not in TEXT_SUFFIXES
            or path in immutable_targets
            or path in {ATOMS, LEGACY_AUTHORITY, TRANSITIONS}
            or ".git" in path.parts
            or ".dset_runtime" in path.parts
        ):
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeError:
            continue
        current = original
        for before, after in replacements:
            current = current.replace(before, after)
        if path == ROOT / ".dset/README.md":
            for layer, directory in LAYER_DIRECTORIES.items():
                current = current.replace(
                    f"]({layer}/README.md)", f"]({directory}/README.md)"
                )
        if current != original:
            path.write_text(current, encoding="utf-8")


def migrate() -> None:
    old_roots = [ROOT / ".dset" / layer for layer in LAYER_DIRECTORIES]
    new_roots = [ROOT / ".dset" / path for path in LAYER_DIRECTORIES.values()]
    if all(path.is_dir() for path in new_roots) and not any(
        path.exists() for path in old_roots
    ):
        _repair_completed_cutover()
        return
    if not all(path.is_dir() for path in old_roots) or any(
        path.exists() for path in new_roots
    ):
        raise RuntimeError("numbered-layer migration requires exactly old roots")

    additions: list[dict[str, Any]] = []
    moves: dict[str, dict[str, Any]] = {}
    immutable_targets: set[Path] = set()
    protected_targets = _protected_transition_targets()
    for source in _tracked_layer_files():
        relative = source.relative_to(ROOT).as_posix()
        protected = protected_targets.get(relative)
        if not source.is_file() or (not _is_immutable(source) and protected is None):
            continue
        target = _target(source)
        if protected is None:
            carriers, semantics = _identities(source)
            record = relocation_record(
                ROOT,
                source,
                target,
                carrier_ids=carriers,
                semantic_ids=semantics,
                authority=AUTHORITY,
                session_id=SESSION,
            )
        else:
            record = _sealed_relocation_record(relative, source, protected)
            record["current_path"] = target.relative_to(ROOT).as_posix()
        additions.append(record)
        moves[relative] = record
        immutable_targets.add(target)

    for layer, directory in LAYER_DIRECTORIES.items():
        (ROOT / ".dset" / layer).rename(ROOT / ".dset" / directory)

    TRANSITIONS.write_text(render_ledger(ROOT, additions), encoding="utf-8")
    atoms = load_toml(ATOMS)
    _replace_current_carrier(atoms, "records", moves)
    ATOMS.write_text(dump_toml(atoms), encoding="utf-8")
    _update_legacy_authority(moves)
    _rewrite_mutable_text(immutable_targets)


if __name__ == "__main__":
    migrate()
