from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class YamlSubsetError(ValueError):
    """Raised when a file exceeds the documented DSET YAML subset."""


def load(path: Path) -> Any:
    return loads(path.read_text(encoding="utf-8"))


def loads(text: str) -> Any:
    entries = _entries(text)
    if not entries:
        return {}
    root: Any = [] if entries[0][1].startswith("-") else {}
    stack: list[tuple[int, Any]] = [(-1, root)]
    for index, (indent, content, line_number) in enumerate(entries):
        while stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        if content == "-" or content.startswith("- "):
            if not isinstance(parent, list):
                raise _error(line_number, "list item outside a list")
            rest = content[1:].strip()
            if not rest:
                child = _next_container(entries, index, indent)
                parent.append(child)
                stack.append((indent, child))
                continue
            if ":" in rest:
                key, raw = _split_mapping(rest, line_number)
                item: dict[str, Any] = {}
                parent.append(item)
                stack.append((indent, item))
                if raw:
                    item[key] = _parse_scalar(raw)
                else:
                    child = _next_container(entries, index, indent)
                    item[key] = child
                    stack.append((indent + 1, child))
                continue
            parent.append(_parse_scalar(rest))
            continue
        if not isinstance(parent, dict):
            raise _error(line_number, "mapping entry outside a mapping")
        key, raw = _split_mapping(content, line_number)
        if raw:
            parent[key] = _parse_scalar(raw)
            continue
        child = _next_container(entries, index, indent)
        parent[key] = child
        stack.append((indent, child))
    return root


def dump(data: Any) -> str:
    lines: list[str] = []
    _emit(data, 0, lines)
    return "\n".join(lines) + "\n"


def _entries(text: str) -> list[tuple[int, str, int]]:
    entries: list[tuple[int, str, int]] = []
    for number, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise _error(number, "tabs are not valid indentation")
        indent = len(raw) - len(raw.lstrip(" "))
        if indent % 2:
            raise _error(number, "indentation must use two-space steps")
        entries.append((indent, raw.strip(), number))
    return entries


def _next_container(
    entries: list[tuple[int, str, int]], index: int, indent: int
) -> Any:
    if index + 1 >= len(entries) or entries[index + 1][0] <= indent:
        return {}
    return [] if entries[index + 1][1].startswith("-") else {}


def _split_mapping(content: str, line_number: int) -> tuple[str, str]:
    if ":" not in content:
        raise _error(line_number, "expected a key/value mapping")
    key, raw = content.split(":", 1)
    key = key.strip()
    if not key:
        raise _error(line_number, "mapping key is empty")
    return key, raw.strip()


def _parse_scalar(raw: str) -> Any:
    if raw == "[]":
        return []
    if raw == "{}":
        return {}
    if raw in {"null", "Null", "NULL", "~"}:
        return None
    if raw.lower() in {"true", "false"}:
        return raw.lower() == "true"
    if raw.startswith('"') and raw.endswith('"'):
        return json.loads(raw)
    if raw.startswith("'") and raw.endswith("'"):
        return raw[1:-1].replace("''", "'")
    if re.fullmatch(r"-?[0-9]+", raw):
        return int(raw)
    if re.fullmatch(r"-?[0-9]+\.[0-9]+", raw):
        return float(raw)
    return raw


def _emit(value: Any, indent: int, lines: list[str]) -> None:
    prefix = " " * indent
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list)) and item:
                lines.append(f"{prefix}{key}:")
                _emit(item, indent + 2, lines)
            elif isinstance(item, dict):
                lines.append(f"{prefix}{key}: {{}}")
            elif isinstance(item, list):
                lines.append(f"{prefix}{key}: []")
            else:
                lines.append(f"{prefix}{key}: {_format_scalar(item)}")
        return
    if isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                _emit(item, indent + 2, lines)
            else:
                lines.append(f"{prefix}- {_format_scalar(item)}")
        return
    lines.append(f"{prefix}{_format_scalar(value)}")


def _format_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    unsafe = (
        not text
        or text.strip() != text
        or text[0] in "-?{}[]!&*#|>@`\"'"
        or ": " in text
        or " #" in text
        or "\n" in text
        or text.lower() in {"null", "true", "false", "~"}
        or bool(re.fullmatch(r"-?[0-9]+(?:\.[0-9]+)?", text))
    )
    return json.dumps(text, ensure_ascii=False) if unsafe else text


def _error(line_number: int, message: str) -> YamlSubsetError:
    return YamlSubsetError(f"line {line_number}: {message}")
