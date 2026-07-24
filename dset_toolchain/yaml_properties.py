"""Parse and render the portable YAML subset used by Markdown properties."""

from __future__ import annotations

import json
import re
from typing import Any


class YamlPropertiesError(ValueError):
    """A Markdown property block exceeds the portable YAML subset."""


def loads(text: str) -> Any:
    """Parse mappings, lists, and scalar values with two-space indentation."""
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
            _parse_list_entry(
                entries,
                index,
                indent,
                content,
                line_number,
                parent,
                stack,
            )
        else:
            _parse_mapping_entry(
                entries,
                index,
                indent,
                content,
                line_number,
                parent,
                stack,
            )
    return root


def dumps(data: Any) -> str:
    """Render the portable subset with stable insertion order."""
    lines: list[str] = []
    _emit(data, 0, lines)
    return "\n".join(lines) + "\n"


def _entries(text: str) -> list[tuple[int, str, int]]:
    entries: list[tuple[int, str, int]] = []
    for number, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        prefix = raw[: len(raw) - len(raw.lstrip())]
        if "\t" in prefix:
            raise _error(number, "tabs are not valid indentation")
        indent = len(prefix)
        if indent % 2:
            raise _error(number, "indentation must use two-space steps")
        entries.append((indent, raw.strip(), number))
    return entries


def _parse_list_entry(
    entries: list[tuple[int, str, int]],
    index: int,
    indent: int,
    content: str,
    line_number: int,
    parent: Any,
    stack: list[tuple[int, Any]],
) -> None:
    if not isinstance(parent, list):
        raise _error(line_number, "list item outside a list")
    rest = content[1:].strip()
    if not rest:
        child = _next_container(entries, index, indent)
        parent.append(child)
        stack.append((indent, child))
    elif _is_inline_mapping(rest):
        _parse_inline_mapping(
            entries,
            index,
            indent,
            rest,
            line_number,
            parent,
            stack,
        )
    else:
        parent.append(_parse_scalar(rest, line_number))


def _parse_inline_mapping(
    entries: list[tuple[int, str, int]],
    index: int,
    indent: int,
    content: str,
    line_number: int,
    parent: list[Any],
    stack: list[tuple[int, Any]],
) -> None:
    key, raw = _split_mapping(content, line_number)
    item: dict[str, Any] = {}
    parent.append(item)
    stack.append((indent, item))
    if raw:
        item[key] = _parse_scalar(raw, line_number)
        return
    child = _next_container(entries, index, indent)
    item[key] = child
    stack.append((indent + 1, child))


def _parse_mapping_entry(
    entries: list[tuple[int, str, int]],
    index: int,
    indent: int,
    content: str,
    line_number: int,
    parent: Any,
    stack: list[tuple[int, Any]],
) -> None:
    if not isinstance(parent, dict):
        raise _error(line_number, "mapping entry outside a mapping")
    key, raw = _split_mapping(content, line_number)
    if raw:
        parent[key] = _parse_scalar(raw, line_number)
        return
    child = _next_container(entries, index, indent)
    parent[key] = child
    stack.append((indent, child))


def _next_container(
    entries: list[tuple[int, str, int]],
    index: int,
    indent: int,
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


def _is_inline_mapping(value: str) -> bool:
    return (
        not value.startswith(('"', "'"))
        and re.match(r"^[^:]+:(?:\s|$)", value) is not None
    )


def _parse_scalar(raw: str, line_number: int) -> Any:
    if raw in {"[]", "{}"}:
        return [] if raw == "[]" else {}
    if raw in {"null", "Null", "NULL", "~"}:
        return None
    if raw.lower() in {"true", "false"}:
        return raw.lower() == "true"
    if raw.startswith(('"', "[", "{")):
        try:
            return json.loads(raw)
        except json.JSONDecodeError as error:
            raise _error(line_number, str(error)) from error
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
            if isinstance(item, dict):
                _emit_mapping_list_item(item, indent, lines)
            elif isinstance(item, list):
                lines.append(f"{prefix}-")
                _emit(item, indent + 2, lines)
            else:
                lines.append(f"{prefix}- {_format_scalar(item)}")
        return
    lines.append(f"{prefix}{_format_scalar(value)}")


def _emit_mapping_list_item(
    item: dict[str, Any],
    indent: int,
    lines: list[str],
) -> None:
    prefix = " " * indent
    first_key, first_value = next(iter(item.items()))
    if isinstance(first_value, (dict, list)):
        lines.append(f"{prefix}- {first_key}:")
        _emit(first_value, indent + 4, lines)
    else:
        lines.append(f"{prefix}- {first_key}: {_format_scalar(first_value)}")
    for key, value in list(item.items())[1:]:
        if isinstance(value, (dict, list)) and value:
            lines.append(f"{prefix}  {key}:")
            _emit(value, indent + 4, lines)
        elif isinstance(value, dict):
            lines.append(f"{prefix}  {key}: {{}}")
        elif isinstance(value, list):
            lines.append(f"{prefix}  {key}: []")
        else:
            lines.append(f"{prefix}  {key}: {_format_scalar(value)}")


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


def _error(line_number: int, message: str) -> YamlPropertiesError:
    return YamlPropertiesError(f"line {line_number}: {message}")
