"""Provide DSET identity behavior."""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path

# IDENTITY_FIELDS defines identity fields; this module owns the default.
IDENTITY_FIELDS = (
    "artifact_id",
    "semantic_id",
    "document_id",
    "rule_id",
)
# TEXT_SUFFIXES defines text suffixes; this module owns the default.
TEXT_SUFFIXES = {".json", ".md", ".toml", ".txt"}
# NUMBERED_PREFIX defines numbered prefix; this module owns the default.
NUMBERED_PREFIX = re.compile(r"^[0-9]+_")


def logical_part(name: str) -> str:
    """Return a numbered layout entry's semantic directory name."""

    return NUMBERED_PREFIX.sub("", name, count=1)


def has_logical_part(path: Path, names: set[str] | frozenset[str]) -> bool:
    return any(logical_part(part) in names for part in path.parts)


def control_root(root: Path) -> Path:
    return root.resolve() / ".dset"


def iter_control_files(root: Path, pattern: str = "*") -> Iterator[Path]:
    """Yield DSET carriers from the target project's control plane only."""

    directory = control_root(root)
    if not directory.is_dir():
        return
    yield from (path for path in sorted(directory.rglob(pattern)) if path.is_file())


def find_unique_name(root: Path, name: str) -> Path:
    if not name or Path(name).name != name:
        raise ValueError(f"DSET carrier name must not contain a path: {name}")
    matches = list(iter_control_files(root, name))
    if not matches:
        raise FileNotFoundError(f"DSET carrier name is missing: {name}")
    if len(matches) > 1:
        raise ValueError(f"DSET carrier name is not unique: {name}")
    return matches[0]


def find_unique_identity(root: Path, identity: str) -> Path:
    if not identity or "/" in identity or "\\" in identity:
        raise ValueError(f"DSET identity must not contain a path: {identity}")
    escaped = re.escape(identity)
    field_pattern = re.compile(
        rf'^(?:{"|".join(IDENTITY_FIELDS)})\s*=\s*"{escaped}"\s*$',
        re.MULTILINE,
    )
    rule_pattern = re.compile(rf"\*\*Rule ID:\*\*\s*`{escaped}`")
    matches: list[Path] = []
    for path in iter_control_files(root):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if field_pattern.search(text) or rule_pattern.search(text):
            matches.append(path)
    if not matches:
        raise FileNotFoundError(f"DSET identity is missing: {identity}")
    if len(matches) > 1:
        raise ValueError(f"DSET identity is not unique: {identity}")
    return matches[0]
