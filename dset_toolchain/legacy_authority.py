from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .diagnostics import Diagnostic
from .layout import discover_layout
from .semantic_types import build_semantic_classification_index
from .yaml_subset import YamlSubsetError, dump, load


def build_legacy_authority_ledger(root: Path) -> dict[str, Any]:
    """Digest-seal legacy Decision authority without freezing shared carriers."""
    root = root.resolve()
    records: list[dict[str, Any]] = []
    for row in build_semantic_classification_index(root):
        origins = [
            str(origin)
            for origin in row["origins"]
            if origin == "legacy_decision" or str(origin).startswith("package:")
        ]
        if row["type"] != "decision" or not origins:
            continue
        fragments: list[dict[str, str]] = []
        for origin in origins:
            for relative in row["carriers"]:
                path = root / str(relative)
                fragment = _authority_fragment(root, path, str(row["id"]), origin)
                if fragment is not None:
                    fragments.append(fragment)
        if not fragments:
            raise ValueError(f"legacy authority has no sealable fragment: {row['id']}")
        records.append(
            {
                "semantic_id": row["id"],
                "type": row["type"],
                "subtype": row["subtype"],
                "fragments": sorted(
                    fragments,
                    key=lambda item: (item["path"], item["selector"]),
                ),
            }
        )
    return {
        "schema_version": "1.0",
        "records": sorted(records, key=lambda item: str(item["semantic_id"])),
    }


def write_legacy_authority_ledger(root: Path) -> Path:
    root = root.resolve()
    path = legacy_authority_ledger_path(root)
    content = dump(build_legacy_authority_ledger(root))
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)
    return path


def validate_legacy_authority_ledger(root: Path) -> list[Diagnostic]:
    root = root.resolve()
    path = legacy_authority_ledger_path(root)
    try:
        expected = build_legacy_authority_ledger(root)
    except (OSError, ValueError) as error:
        return [Diagnostic("DSET-E167", path, str(error))]
    if not path.is_file():
        if expected["records"]:
            return [Diagnostic("DSET-E167", path, "legacy authority ledger is missing")]
        return []
    try:
        actual = load(path)
    except (OSError, UnicodeError, YamlSubsetError) as error:
        return [Diagnostic("DSET-E167", path, f"invalid legacy ledger: {error}")]
    if actual != expected:
        return [
            Diagnostic(
                "DSET-E167",
                path,
                "legacy Decision authority changed without native successors",
            )
        ]
    return []


def legacy_authority_ledger_path(root: Path) -> Path:
    return discover_layout(root.resolve()).governance_root / "legacy-authority.yaml"


def _authority_fragment(
    root: Path, path: Path, semantic_id: str, origin: str
) -> dict[str, str] | None:
    if origin == "legacy_decision":
        if path.suffix != ".md" or not path.is_file():
            return None
        payload = path.read_bytes()
        selector = "whole-carrier"
    else:
        field = origin.partition(":")[2]
        try:
            data = load(path)
        except (OSError, UnicodeError, YamlSubsetError):
            return None
        values = data.get(field, []) if isinstance(data, dict) else []
        if semantic_id not in values:
            return None
        selector = f"{field}:{semantic_id}"
        payload = f"{selector}\n".encode()
    return {
        "path": path.relative_to(root).as_posix(),
        "selector": selector,
        "sha256": hashlib.sha256(payload).hexdigest(),
    }
