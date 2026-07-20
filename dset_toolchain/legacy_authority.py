from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from .carrier_transitions import decode_historical_envelope
from .diagnostics import Diagnostic
from .layout import discover_layout
from .yaml_subset import YamlSubsetError, dump, load

ID_PATTERN = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)+$")


def build_legacy_authority_ledger(root: Path) -> dict[str, Any]:
    """Digest-seal legacy Decision authority without freezing shared carriers."""
    from .semantic_types import build_semantic_classification_index

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
    content = dump(build_legacy_authority_ledger(root), path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)
    return path


def validate_legacy_authority_ledger(root: Path) -> list[Diagnostic]:
    root = root.resolve()
    path = legacy_authority_ledger_path(root)
    if not path.is_file():
        try:
            expected = build_legacy_authority_ledger(root)
        except (OSError, ValueError) as error:
            return [Diagnostic("DSET-E167", path, str(error))]
        if expected["records"]:
            if not (root / ".git").exists():
                return []
            return [Diagnostic("DSET-E167", path, "legacy authority ledger is missing")]
        return []
    try:
        actual = load(path)
    except (OSError, UnicodeError, YamlSubsetError) as error:
        return [Diagnostic("DSET-E167", path, f"invalid legacy ledger: {error}")]
    if _recorded_fragment_errors(root, actual):
        return [
            Diagnostic(
                "DSET-E167",
                path,
                "legacy Decision authority changed without native successors",
            )
        ]
    return []


def legacy_shared_package_paths(root: Path) -> tuple[Path, ...]:
    """Return package carriers trusted as selector-sealed historical input."""

    root = root.resolve()
    ledger = _load_recorded_ledger(root)
    records = ledger.get("records") if isinstance(ledger, dict) else None
    if not isinstance(records, list):
        return ()
    paths: set[Path] = set()
    for record in records:
        fragments = record.get("fragments") if isinstance(record, dict) else None
        if not isinstance(fragments, list):
            continue
        for fragment in fragments:
            if not isinstance(fragment, dict):
                continue
            raw_path = fragment.get("path")
            current_path = fragment.get("current_path")
            selector = fragment.get("selector")
            if not isinstance(raw_path, str) or selector == "whole-carrier":
                continue
            active = current_path if isinstance(current_path, str) else raw_path
            candidate = (root / active).resolve()
            if (
                _within(root, candidate)
                and (
                    candidate.name in {"package.yaml", "package.yml"}
                    or candidate.name == "package.legacy.toml"
                )
                and candidate.is_file()
            ):
                paths.add(candidate)
    return tuple(sorted(paths))


def legacy_authority_ids(root: Path) -> set[str]:
    """Expose historical IDs without making them current package ownership."""

    identifiers: set[str] = set()
    for path in legacy_shared_package_paths(root):
        try:
            data = _load_fragment_carrier(path)
        except (OSError, UnicodeError, YamlSubsetError):
            continue
        if not isinstance(data, dict):
            continue
        for value in data.values():
            if isinstance(value, list):
                identifiers.update(
                    item
                    for item in value
                    if isinstance(item, str) and ID_PATTERN.fullmatch(item)
                )
    ledger = _load_recorded_ledger(root)
    records = ledger.get("records") if isinstance(ledger, dict) else None
    if isinstance(records, list):
        identifiers.update(
            str(record["semantic_id"])
            for record in records
            if isinstance(record, dict) and isinstance(record.get("semantic_id"), str)
        )
    return identifiers


def legacy_authority_ledger_path(root: Path) -> Path:
    layout = discover_layout(root.resolve())
    return layout.structured_file(layout.governance_root, "legacy-authority.toml")


def _load_recorded_ledger(root: Path) -> dict[str, Any] | None:
    path = legacy_authority_ledger_path(root)
    if not path.is_file():
        return None
    try:
        data = load(path)
    except (OSError, UnicodeError, YamlSubsetError):
        return None
    return data if isinstance(data, dict) else None


def _recorded_fragment_errors(root: Path, ledger: object) -> list[str]:
    if not isinstance(ledger, dict) or str(ledger.get("schema_version")) != "1.0":
        return ["legacy authority ledger schema_version must be 1.0"]
    records = ledger.get("records")
    if not isinstance(records, list):
        return ["legacy authority ledger records must be a list"]
    errors: list[str] = []
    seen: set[str] = set()
    for record in records:
        if not isinstance(record, dict) or not isinstance(
            record.get("semantic_id"), str
        ):
            errors.append("legacy authority record is malformed")
            continue
        semantic_id = str(record["semantic_id"])
        if semantic_id in seen:
            errors.append(f"duplicate legacy authority ID: {semantic_id}")
        seen.add(semantic_id)
        fragments = record.get("fragments")
        if not isinstance(fragments, list) or not fragments:
            errors.append(f"legacy authority has no fragments: {semantic_id}")
            continue
        for fragment in fragments:
            error = _validate_recorded_fragment(root, semantic_id, fragment)
            if error is not None:
                errors.append(error)
    return errors


def _validate_recorded_fragment(
    root: Path, semantic_id: str, fragment: object
) -> str | None:
    if not isinstance(fragment, dict):
        return f"legacy authority fragment is malformed: {semantic_id}"
    raw_path = fragment.get("path")
    selector = fragment.get("selector")
    expected = fragment.get("sha256")
    if not all(isinstance(item, str) for item in (raw_path, selector, expected)):
        return f"legacy authority fragment seal is incomplete: {semantic_id}"
    assert isinstance(raw_path, str)
    assert isinstance(selector, str)
    assert isinstance(expected, str)
    raw_current = fragment.get("current_path")
    current_digest = fragment.get("current_sha256")
    transition_id = fragment.get("transition_id")
    transitioned = isinstance(raw_current, str)
    if transitioned and not all(
        isinstance(item, str) for item in (current_digest, transition_id)
    ):
        return f"legacy authority current seal is incomplete: {semantic_id}"
    active = str(raw_current) if transitioned else raw_path
    path = (root / active).resolve()
    if not _within(root, path) or not path.is_file():
        return f"legacy authority carrier is missing: {raw_path}"
    if selector == "whole-carrier":
        payload = path.read_bytes()
        expected = current_digest if transitioned else expected
    else:
        if (
            transitioned
            and hashlib.sha256(path.read_bytes()).hexdigest() != current_digest
        ):
            return f"legacy authority current carrier digest changed: {semantic_id}"
        field, separator, selected_id = selector.partition(":")
        if not separator or selected_id != semantic_id:
            return f"legacy authority selector is invalid: {semantic_id}"
        try:
            data = _load_fragment_carrier(path)
        except (OSError, UnicodeError, YamlSubsetError):
            return f"legacy authority carrier is invalid: {raw_path}"
        values = data.get(field) if isinstance(data, dict) else None
        if not isinstance(values, list) or semantic_id not in values:
            return f"legacy authority selector is missing: {semantic_id}"
        payload = f"{selector}\n".encode()
    if hashlib.sha256(payload).hexdigest() != expected:
        return f"legacy authority fragment digest changed: {semantic_id}"
    return None


def _load_fragment_carrier(path: Path) -> Any:
    if path.name.endswith(".legacy.toml"):
        return decode_historical_envelope(path.read_text(encoding="utf-8"))
    return load(path)


def _within(root: Path, path: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


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
