"""Small, deterministic TOML codec for DSET-owned artifacts.

The project supports Python 3.10 without a runtime dependency.  Python 3.11
and later use :mod:`tomllib`; the fallback deliberately implements the stable
subset emitted by :func:`dumps` (tables, array-of-tables, scalars, and arrays).
It is not a permissive compatibility shim: inputs outside that subset fail
with a useful error instead of being reinterpreted.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

# _BARE_KEY validates bare key; this module owns the accepted syntax.
_BARE_KEY = re.compile(r"^[A-Za-z0-9_-]+$")
# _INTEGER validates integer; this module owns the accepted syntax.
_INTEGER = re.compile(r"^[+-]?[0-9][0-9_]*$")
# _FLOAT validates float; this module owns the accepted syntax.
_FLOAT = re.compile(r"^[+-]?(?:[0-9][0-9_]*\.[0-9_]+|[0-9][0-9_]*[eE][+-]?[0-9_]+)$")

try:  # pragma: no cover - exercised on Python 3.11+ by the standard library.
    import tomllib as _tomllib  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover - exercised on Python 3.10.
    _tomllib = None


class TomlCodecError(ValueError):
    """Raised when a value is outside DSET's portable TOML subset."""


def load(path: Path) -> dict[str, Any]:
    """Load load using the declared repository contract."""
    return loads(path.read_text(encoding="utf-8"))


def loads(text: str) -> dict[str, Any]:
    """Handle loads using the declared repository contract."""
    if _tomllib is not None:
        try:
            value = _tomllib.loads(text)
        except _tomllib.TOMLDecodeError as error:
            raise TomlCodecError(str(error)) from error
        if not isinstance(value, dict):
            raise TomlCodecError("TOML document root must be a table")
        return value
    return _loads_subset(text)


def dumps(value: Mapping[str, Any]) -> str:
    """Handle dumps using the declared repository contract."""
    if not isinstance(value, Mapping):
        raise TomlCodecError("TOML document root must be a mapping")
    lines: list[str] = []
    _emit_table(dict(value), (), lines, header=False)
    return "\n".join(lines).rstrip() + "\n"


def _emit_table(
    table: Mapping[str, Any],
    path: tuple[str, ...],
    lines: list[str],
    *,
    header: bool,
) -> None:
    """Emit table using the declared repository contract."""
    _require_string_keys(table, path)
    if header:
        if lines and lines[-1] != "":
            lines.append("")
        lines.append("[" + ".".join(_format_key(key) for key in path) + "]")

    child_tables: list[tuple[str, Mapping[str, Any]]] = []
    array_tables: list[tuple[str, Sequence[Any]]] = []
    for key, item in table.items():
        if isinstance(item, Mapping) and item:
            child_tables.append((key, item))
        elif _is_array_of_tables(item):
            array_tables.append((key, item))
        else:
            lines.append(f"{_format_key(key)} = {_format_value(item, path + (key,))}")

    for key, child in child_tables:
        _emit_table(child, path + (key,), lines, header=True)
    for key, records in array_tables:
        for record in records:
            if lines and lines[-1] != "":
                lines.append("")
            table_path = path + (key,)
            table_name = ".".join(_format_key(item) for item in table_path)
            lines.append(f"[[{table_name}]]")
            assert isinstance(record, Mapping)
            _emit_table_body(record, table_path, lines)


def _emit_table_body(
    table: Mapping[str, Any], path: tuple[str, ...], lines: list[str]
) -> None:
    """Emit table body using the declared repository contract."""
    _require_string_keys(table, path)
    child_tables: list[tuple[str, Mapping[str, Any]]] = []
    array_tables: list[tuple[str, Sequence[Any]]] = []
    for key, item in table.items():
        if isinstance(item, Mapping) and item:
            child_tables.append((key, item))
        elif _is_array_of_tables(item):
            array_tables.append((key, item))
        else:
            lines.append(f"{_format_key(key)} = {_format_value(item, path + (key,))}")
    for key, child in child_tables:
        _emit_table(child, path + (key,), lines, header=True)
    for key, records in array_tables:
        for record in records:
            if lines and lines[-1] != "":
                lines.append("")
            table_path = path + (key,)
            table_name = ".".join(_format_key(item) for item in table_path)
            lines.append(f"[[{table_name}]]")
            assert isinstance(record, Mapping)
            _emit_table_body(record, table_path, lines)


def _format_value(value: Any, path: tuple[str, ...]) -> str:
    """Format value using the declared repository contract."""
    if value is None:
        raise TomlCodecError(f"{_render_path(path)}: null is not representable in TOML")
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise TomlCodecError(
                f"{_render_path(path)}: non-finite floats are not supported"
            )
        return repr(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, Mapping):
        if value:
            raise TomlCodecError(
                f"{_render_path(path)}: nested mappings must be emitted as tables"
            )
        return "{}"
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        if _is_array_of_tables(value):
            raise TomlCodecError(
                f"{_render_path(path)}: array-of-tables must be emitted as tables"
            )
        if any(isinstance(item, (Mapping, list, tuple)) for item in value):
            raise TomlCodecError(
                f"{_render_path(path)}: nested arrays and mixed mappings are "
                "unsupported"
            )
        _require_homogeneous_scalars(value, path)
        return "[" + ", ".join(_format_value(item, path) for item in value) + "]"
    raise TomlCodecError(
        f"{_render_path(path)}: {type(value).__name__} is not representable in TOML"
    )


def _is_array_of_tables(value: Any) -> bool:
    """Handle array of tables using the declared repository contract."""
    return (
        isinstance(value, Sequence)
        and not isinstance(value, (str, bytes, bytearray))
        and bool(value)
        and all(isinstance(item, Mapping) for item in value)
    )


def _require_homogeneous_scalars(value: Sequence[Any], path: tuple[str, ...]) -> None:
    kinds = {type(item) for item in value}
    if len(kinds) > 1:
        raise TomlCodecError(
            f"{_render_path(path)}: TOML array values must share one type"
        )


def _require_string_keys(value: Mapping[str, Any], path: tuple[str, ...]) -> None:
    for key in value:
        if not isinstance(key, str) or not key:
            raise TomlCodecError(
                f"{_render_path(path)}: TOML table keys must be non-empty strings"
            )


def _format_key(key: str) -> str:
    return key if _BARE_KEY.fullmatch(key) else json.dumps(key, ensure_ascii=False)


def _render_path(path: tuple[str, ...]) -> str:
    return ".".join(path) if path else "<root>"


def _loads_subset(text: str) -> dict[str, Any]:
    """Handle subset using the declared repository contract."""
    root: dict[str, Any] = {}
    current: dict[str, Any] = root
    for line_number, raw in enumerate(text.splitlines(), start=1):
        line = _strip_comment(raw).strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            array = line.startswith("[[") and line.endswith("]]")
            raw_path = line[2:-2] if array else line[1:-1]
            keys = [
                _parse_key(piece.strip(), line_number) for piece in raw_path.split(".")
            ]
            current = _select_table(root, keys, array, line_number)
            continue
        key_raw, separator, raw_value = line.partition("=")
        if not separator:
            raise TomlCodecError(f"line {line_number}: expected key = value")
        key = _parse_key(key_raw.strip(), line_number)
        if key in current:
            raise TomlCodecError(f"line {line_number}: duplicate key {key}")
        current[key] = _parse_value(raw_value.strip(), line_number)
    return root


def _select_table(
    root: dict[str, Any], keys: list[str], array: bool, line_number: int
) -> dict[str, Any]:
    """Select table using the declared repository contract."""
    if not keys or any(not key for key in keys):
        raise TomlCodecError(f"line {line_number}: table name is empty")
    current = root
    for key in keys[:-1]:
        existing = current.get(key)
        if existing is None:
            nested: dict[str, Any] = {}
            current[key] = nested
            current = nested
        elif isinstance(existing, dict):
            current = existing
        else:
            raise TomlCodecError(f"line {line_number}: table path conflicts with {key}")
    final = keys[-1]
    if array:
        existing = current.setdefault(final, [])
        if not isinstance(existing, list):
            raise TomlCodecError(
                f"line {line_number}: array table conflicts with {final}"
            )
        record: dict[str, Any] = {}
        existing.append(record)
        return record
    existing = current.setdefault(final, {})
    if not isinstance(existing, dict):
        raise TomlCodecError(f"line {line_number}: table conflicts with {final}")
    return existing


def _parse_key(value: str, line_number: int) -> str:
    """Parse key using the declared repository contract."""
    if _BARE_KEY.fullmatch(value):
        return value
    if value.startswith('"') and value.endswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as error:
            raise TomlCodecError(f"line {line_number}: invalid quoted key") from error
        if isinstance(parsed, str) and parsed:
            return parsed
    raise TomlCodecError(f"line {line_number}: invalid key {value!r}")


def _parse_value(value: str, line_number: int) -> Any:
    """Parse value using the declared repository contract."""
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith('"') and value.endswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as error:
            raise TomlCodecError(f"line {line_number}: invalid string") from error
        if isinstance(parsed, str):
            return parsed
    if _INTEGER.fullmatch(value):
        return int(value.replace("_", ""))
    if _FLOAT.fullmatch(value):
        return float(value.replace("_", ""))
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_value(item, line_number) for item in _split_array(inner)]
    if value == "{}":
        return {}
    raise TomlCodecError(f"line {line_number}: unsupported TOML value {value!r}")


def _split_array(value: str) -> list[str]:
    """Handle array using the declared repository contract."""
    parts: list[str] = []
    quote = False
    escaped = False
    start = 0
    for index, character in enumerate(value):
        if quote and character == "\\" and not escaped:
            escaped = True
            continue
        if character == '"' and not escaped:
            quote = not quote
        if character == "," and not quote:
            parts.append(value[start:index].strip())
            start = index + 1
        escaped = False
    parts.append(value[start:].strip())
    if not all(parts):
        raise TomlCodecError("invalid empty array item")
    return parts


def _strip_comment(value: str) -> str:
    """Handle comment using the declared repository contract."""
    quote = False
    escaped = False
    for index, character in enumerate(value):
        if quote and character == "\\" and not escaped:
            escaped = True
            continue
        if character == '"' and not escaped:
            quote = not quote
        if character == "#" and not quote:
            return value[:index]
        escaped = False
    return value
