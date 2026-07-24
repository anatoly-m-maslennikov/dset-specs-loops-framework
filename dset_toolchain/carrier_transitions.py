"""Read and validate the legacy aggregate transitions authorized by GOV-018."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from .frontmatter import parse as parse_frontmatter
from .frontmatter import render as render_frontmatter
from .toml_codec import dumps as dump_toml
from .toml_codec import loads as load_toml
from .structured_data import load as load_structured

# SCHEMA_VERSION defines schema version; this module owns the default.
SCHEMA_VERSION = "1.0"
# AUTHORITY_DECISION defines authority decision; this module owns the default.
AUTHORITY_DECISION = "DSET-DECISION-GOV-018"
# LAYOUT_AUTHORITY defines layout authority; this module owns the default.
LAYOUT_AUTHORITY = "DSET-REQUIREMENT-GOV-041"
# AUTHORITY_DECISIONS defines authority decisions; this module owns the default.
AUTHORITY_DECISIONS = frozenset(
    {
        AUTHORITY_DECISION,
        LAYOUT_AUTHORITY,
        "DSET-REQUIREMENT-GOV-044",
        "DSET-DECISION-GOV-022",
    }
)
# SESSION_ID defines session id; this module owns the default.
SESSION_ID = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
# LEDGER_RELATIVE defines ledger relative; this module owns the default.
LEDGER_RELATIVE = Path(".dset/100_project/legacy/migrations/carrier-transitions.toml")
# LEGACY_LEDGER_RELATIVES defines legacy ledger relatives; this module owns the default.
LEGACY_LEDGER_RELATIVES = (
    Path("00_project/migrations/carrier-transitions.toml"),
    Path("dset/scopes/gov/migrations/carrier-transitions.toml"),
    Path("dset/migrations/carrier-transitions.toml"),
)
# _NULL_SENTINEL validates null sentinel; this module owns the accepted syntax.
_NULL_SENTINEL = "__DSET_EXPLICIT_NULL__"
# _MARKDOWN_LINK validates markdown link; this module owns the accepted syntax.
_MARKDOWN_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")


class CarrierTransitionError(ValueError):
    """A carrier transition is missing, lossy, ambiguous, or tampered."""


def ledger_path(root: Path) -> Path:
    """Handle path using the declared repository contract."""
    current = root / LEDGER_RELATIVE
    if current.is_file():
        return current
    for relative in LEGACY_LEDGER_RELATIVES:
        legacy = root / relative
        if legacy.is_file():
            return legacy
    return current


def transition_id(original_path: str, original_sha256: str) -> str:
    """Handle id using the declared repository contract."""
    digest = hashlib.sha256(f"{original_path}\0{original_sha256}".encode()).hexdigest()
    return f"DSET-CARRIER-TRANSITION-{digest[:16].upper()}"


def semantic_sha256(value: Any) -> str:
    """Handle sha256 using the declared repository contract."""
    try:
        payload = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as error:
        raise CarrierTransitionError(
            f"semantic value is not deterministically serializable: {error}"
        ) from error
    return hashlib.sha256(payload.encode()).hexdigest()


def encode_nulls(value: Any) -> tuple[Any, list[str]]:
    """Handle nulls using the declared repository contract."""
    paths: list[str] = []

    def visit(item: Any, path: tuple[str, ...]) -> Any:
        """Handle visit using the declared repository contract."""
        if item is None:
            paths.append(_render_null_path(path))
            return _NULL_SENTINEL
        if isinstance(item, dict):
            encoded: dict[str, Any] = {}
            for key, child in item.items():
                rendered_key = str(key)
                if child is None:
                    paths.append(_render_null_path(path + (rendered_key,)))
                    continue
                encoded[rendered_key] = visit(child, path + (rendered_key,))
            return encoded
        if isinstance(item, list):
            return [
                visit(child, path + (str(index),)) for index, child in enumerate(item)
            ]
        return item

    return visit(deepcopy(value), ()), sorted(paths)


def decode_nulls(value: Any, null_paths: list[str]) -> Any:
    """Handle nulls using the declared repository contract."""
    decoded = deepcopy(value)
    for rendered in null_paths:
        parts = _parse_null_path(rendered)
        current = decoded
        for part in parts[:-1]:
            current = current[int(part)] if isinstance(current, list) else current[part]
        final = parts[-1] if parts else ""
        if isinstance(current, list):
            if not final.isdigit() or int(final) >= len(current):
                raise CarrierTransitionError(
                    f"invalid null reconstruction path: {rendered}"
                )
            current[int(final)] = None
        elif isinstance(current, dict):
            current[final] = None
        else:
            raise CarrierTransitionError(
                f"invalid null reconstruction path: {rendered}"
            )
    return decoded


def historical_envelope(
    root: Path, source: Path, target: Path
) -> tuple[str, dict[str, Any]]:
    """Handle envelope using the declared repository contract."""
    value = load_structured(source)
    encoded, null_paths = encode_nulls(value)
    _validate_null_paths(source, null_paths, markdown=False)
    original_path = source.relative_to(root).as_posix()
    original_digest = hashlib.sha256(source.read_bytes()).hexdigest()
    semantic_digest = semantic_sha256(value)
    identifier = transition_id(original_path, original_digest)
    envelope = {
        "schema_version": SCHEMA_VERSION,
        "transition_id": identifier,
        "authority_decision": AUTHORITY_DECISION,
        "original_path": original_path,
        "original_format": source.suffix.lstrip("."),
        "original_sha256": original_digest,
        "semantic_sha256": semantic_digest,
        "null_paths": null_paths,
        "declared_loss": [],
        "payload": encoded,
    }
    rendered = dump_toml(envelope)
    reconstructed = decode_historical_envelope(rendered)
    if semantic_sha256(reconstructed) != semantic_digest:
        raise CarrierTransitionError(f"semantic drift while converting {original_path}")
    return rendered, transition_record(
        root,
        source,
        target,
        rendered,
        semantic_digest,
        null_paths,
        kind="structured_yaml",
    )


def decode_historical_envelope(text: str) -> Any:
    """Handle historical envelope using the declared repository contract."""
    data = load_toml(text)
    payload = data.get("payload")
    null_paths = data.get("null_paths")
    if not isinstance(null_paths, list) or not all(
        isinstance(item, str) for item in null_paths
    ):
        raise CarrierTransitionError("historical envelope null_paths must be strings")
    return decode_nulls(payload, null_paths)


def markdown_transition(root: Path, source: Path) -> tuple[str, dict[str, Any]]:
    """Handle transition using the declared repository contract."""
    before = source.read_text(encoding="utf-8")
    parsed = parse_frontmatter(before)
    if parsed is None or parsed[2] != "yaml":
        raise CarrierTransitionError(f"expected YAML frontmatter: {source}")
    metadata, body, _format = parsed
    encoded, null_paths = encode_nulls(metadata)
    _validate_null_paths(source, null_paths, markdown=True)
    if not isinstance(encoded, dict):
        raise CarrierTransitionError(f"frontmatter root changed type: {source}")
    if _contains_null_sentinel(encoded):
        raise CarrierTransitionError(
            f"live TOML frontmatter cannot contain a null sentinel: {source}"
        )
    rendered = render_frontmatter(encoded, body, format="toml")
    reparsed = parse_frontmatter(rendered)
    if reparsed is None:
        raise CarrierTransitionError(f"TOML frontmatter disappeared: {source}")
    source_semantics = {"metadata": metadata, "body": body}
    target_semantics = {
        "metadata": decode_nulls(reparsed[0], null_paths),
        "body": reparsed[1],
    }
    semantic_digest = semantic_sha256(source_semantics)
    if semantic_sha256(target_semantics) != semantic_digest:
        raise CarrierTransitionError(f"semantic drift while converting {source}")
    if semantic_sha256(decode_nulls(encoded, null_paths)) != semantic_sha256(metadata):
        raise CarrierTransitionError(f"null reconstruction failed: {source}")
    return rendered, transition_record(
        root,
        source,
        source,
        rendered,
        semantic_digest,
        null_paths,
        kind="markdown_frontmatter",
    )


def markdown_link_transition(
    root: Path, source: Path, mapping: dict[Path, Path]
) -> tuple[str, dict[str, Any]] | None:
    """Rewrite physical legacy links while preserving their logical targets."""

    before = source.read_text(encoding="utf-8")
    rewrites: list[dict[str, str]] = []

    def replace(match: re.Match[str]) -> str:
        """Handle replace using the declared repository contract."""
        label, raw_target = match.groups()
        wrapped = raw_target.startswith("<") and raw_target.endswith(">")
        target_text = raw_target[1:-1] if wrapped else raw_target
        path_text, marker, anchor = target_text.partition("#")
        if not path_text or path_text.startswith(("http://", "https://", "mailto:")):
            return match.group(0)
        resolved = (source.parent / unquote(path_text)).resolve()
        current = mapping.get(resolved)
        if current is None:
            return match.group(0)
        relative = os.path.relpath(current, source.parent).replace(os.sep, "/")
        replacement_target = relative + (f"#{anchor}" if marker else "")
        if wrapped:
            replacement_target = f"<{replacement_target}>"
        rewrites.append(
            {
                "source": raw_target,
                "target": replacement_target,
                "original_path": resolved.relative_to(root).as_posix(),
                "current_path": current.relative_to(root).as_posix(),
            }
        )
        return f"[{label}]({replacement_target})"

    rendered = _MARKDOWN_LINK.sub(replace, before)
    if rendered == before:
        return None
    reconstructed = rendered
    for rewrite in reversed(rewrites):
        reconstructed = reconstructed.replace(rewrite["target"], rewrite["source"])
    if reconstructed != before:
        raise CarrierTransitionError(
            f"Markdown link transition is not exactly reversible: {source}"
        )
    semantic_digest = semantic_sha256({"body": before})
    record = transition_record(
        root,
        source,
        source,
        rendered,
        semantic_digest,
        [],
        kind="markdown_links",
    )
    record["link_rewrites"] = rewrites
    return rendered, record


def transition_record(
    root: Path,
    source: Path,
    target: Path,
    rendered: str,
    semantic_digest: str,
    null_paths: list[str],
    *,
    kind: str,
) -> dict[str, Any]:
    """Handle record using the declared repository contract."""
    original_path = source.relative_to(root).as_posix()
    original_digest = hashlib.sha256(source.read_bytes()).hexdigest()
    target_digest = hashlib.sha256(rendered.encode()).hexdigest()
    commit = git_head(root)
    if commit is None:
        raise CarrierTransitionError("carrier transition requires a Git HEAD")
    blob = git_blob(root, original_path)
    if blob is None:
        raise CarrierTransitionError(
            f"carrier transition requires a source Git blob: {original_path}"
        )
    return {
        "id": transition_id(original_path, original_digest),
        "kind": kind,
        "authority_decision": AUTHORITY_DECISION,
        "original_path": original_path,
        "original_format": (
            "markdown_yaml_frontmatter"
            if kind == "markdown_frontmatter"
            else "markdown"
            if kind == "markdown_links"
            else source.suffix.lstrip(".")
        ),
        "original_sha256": original_digest,
        "source_git_blob": blob,
        "current_path": target.relative_to(root).as_posix(),
        "current_format": (
            "markdown_toml_frontmatter"
            if kind == "markdown_frontmatter"
            else "markdown"
            if kind == "markdown_links"
            else "toml"
        ),
        "current_sha256": target_digest,
        "source_semantic_sha256": semantic_digest,
        "current_semantic_sha256": semantic_digest,
        "null_paths": null_paths,
        "declared_loss": [],
        "source_commit": commit,
        "transitioned_at": git_commit_time(root),
        "llm_session_ids": [SESSION_ID],
    }


def relocation_record(
    root: Path,
    source: Path,
    target: Path,
    *,
    carrier_ids: list[str] | None = None,
    semantic_ids: list[str] | None = None,
    authority: str = LAYOUT_AUTHORITY,
    session_id: str = SESSION_ID,
) -> dict[str, Any]:
    """Describe a byte-exact carrier move without changing its semantics."""

    if authority not in AUTHORITY_DECISIONS:
        raise CarrierTransitionError(f"unsupported relocation authority: {authority}")
    original_path = source.relative_to(root).as_posix()
    original_digest = hashlib.sha256(source.read_bytes()).hexdigest()
    blob = git_blob(root, original_path)
    if blob is None:
        raise CarrierTransitionError(
            f"carrier relocation requires a source Git blob: {original_path}"
        )
    semantic_digest = semantic_sha256({"carrier_sha256": original_digest})
    return {
        "id": transition_id(original_path, original_digest),
        "kind": "carrier_relocation",
        "authority_decision": authority,
        "original_path": original_path,
        "original_format": source.suffix.lstrip("."),
        "original_sha256": original_digest,
        "source_git_blob": blob,
        "current_path": target.relative_to(root).as_posix(),
        "current_format": target.suffix.lstrip("."),
        "current_sha256": original_digest,
        "source_semantic_sha256": semantic_digest,
        "current_semantic_sha256": semantic_digest,
        "null_paths": [],
        "declared_loss": [],
        "source_commit": git_head(root),
        "transitioned_at": git_commit_time(root),
        "llm_session_ids": [session_id],
        "carrier_ids": sorted(set(carrier_ids or [])),
        "semantic_ids": sorted(set(semantic_ids or [])),
    }


def git_head(root: Path) -> str | None:
    """Handle head using the declared repository contract."""
    return _git_value(root, ["rev-parse", "HEAD"])


def git_blob(root: Path, relative: str) -> str | None:
    """Handle blob using the declared repository contract."""
    return _git_value(root, ["rev-parse", f"HEAD:{relative}"])


def git_commit_time(root: Path) -> str:
    """Handle commit time using the declared repository contract."""
    value = _git_value(root, ["show", "-s", "--format=%cI", "HEAD"])
    if value is None:
        raise CarrierTransitionError("carrier transition requires a commit timestamp")
    return value


def load_ledger(root: Path) -> dict[str, Any]:
    """Load ledger using the declared repository contract."""
    path = ledger_path(root)
    if not path.is_file():
        return {"schema_version": SCHEMA_VERSION, "transitions": []}
    value = load_structured(path)
    if not isinstance(value, dict):
        raise CarrierTransitionError("carrier transition ledger must be a mapping")
    transitions = value.get("transitions")
    if str(value.get("schema_version")) != SCHEMA_VERSION or not isinstance(
        transitions, list
    ):
        raise CarrierTransitionError("invalid carrier transition ledger")
    return value


def render_ledger(root: Path, additions: list[dict[str, Any]]) -> str:
    """Render ledger using the declared repository contract."""
    ledger = deepcopy(load_ledger(root))
    existing = ledger["transitions"]
    assert isinstance(existing, list)
    by_id = {item.get("id"): item for item in existing if isinstance(item, dict)}
    for item in additions:
        current = by_id.get(item["id"])
        if current is not None and current != item:
            raise CarrierTransitionError(
                f"transition ledger entry changed: {item['id']}"
            )
        if current is None:
            existing.append(item)
            by_id[item["id"]] = item
    existing.sort(
        key=lambda item: str(item.get("id", "")) if isinstance(item, dict) else ""
    )
    return dump_toml(ledger)


def transition_aliases(root: Path) -> dict[Path, Path]:
    """Return original-to-current logical link aliases from the sealed ledger."""

    try:
        data = load_ledger(root)
    except (OSError, UnicodeError, ValueError):
        return {}
    transitions = data.get("transitions")
    if not isinstance(transitions, list):
        return {}
    aliases: dict[Path, Path] = {}
    for item in transitions:
        if not isinstance(item, dict):
            continue
        original = item.get("original_path")
        current = item.get("current_path")
        if (
            isinstance(original, str)
            and isinstance(current, str)
            and original != current
        ):
            aliases[(root / original).resolve()] = (root / current).resolve()
    return {
        original: _resolve_transition_target(root, target.as_posix(), aliases)
        for original, target in aliases.items()
    }


def _resolve_transition_target(
    root: Path, current: str, aliases: dict[Path, Path]
) -> Path:
    """Resolve transition target using the declared repository contract."""
    target = (root / current).resolve()
    seen: set[Path] = set()
    while target in aliases:
        if target in seen:
            raise CarrierTransitionError(f"carrier relocation cycle: {current}")
        seen.add(target)
        target = aliases[target]
    return target


def validate_carrier_transition_ledger(root: Path) -> list[str]:
    """Validate append-only transition identity, bytes, semantics, and Git return."""

    path = ledger_path(root)
    if not path.is_file():
        return []
    try:
        data = load_ledger(root)
    except (OSError, UnicodeError, ValueError) as error:
        return [str(error)]
    transitions = data.get("transitions")
    assert isinstance(transitions, list)
    errors: list[str] = []
    seen: set[str] = set()
    aliases = transition_aliases(root)
    required = {
        "id",
        "kind",
        "authority_decision",
        "carrier_ids",
        "semantic_ids",
        "original_path",
        "original_format",
        "original_sha256",
        "source_git_blob",
        "current_path",
        "current_format",
        "current_sha256",
        "source_semantic_sha256",
        "current_semantic_sha256",
        "null_paths",
        "declared_loss",
        "source_commit",
        "transitioned_at",
        "llm_session_ids",
    }
    for item in transitions:
        if not isinstance(item, dict) or not required.issubset(item):
            errors.append("transition record has missing required fields")
            continue
        identifier = item.get("id")
        original = item.get("original_path")
        original_digest = item.get("original_sha256")
        current = item.get("current_path")
        current_digest = item.get("current_sha256")
        null_paths = item.get("null_paths")
        if (
            not all(
                isinstance(value, str)
                for value in (
                    identifier,
                    original,
                    original_digest,
                    current,
                    current_digest,
                )
            )
            or not isinstance(null_paths, list)
            or not all(isinstance(value, str) for value in null_paths)
        ):
            errors.append("transition record has invalid identity fields")
            continue
        assert isinstance(identifier, str)
        assert isinstance(original, str)
        assert isinstance(original_digest, str)
        assert isinstance(current, str)
        assert isinstance(current_digest, str)
        if identifier in seen:
            errors.append(f"duplicate transition ID: {identifier}")
        seen.add(identifier)
        if identifier != transition_id(original, original_digest):
            errors.append(f"transition identity changed: {identifier}")
        if item.get("authority_decision") not in AUTHORITY_DECISIONS:
            errors.append(f"transition authority changed: {identifier}")
        if item.get("declared_loss") != []:
            errors.append(f"transition declares semantic loss: {identifier}")
        carrier_ids = item.get("carrier_ids")
        semantic_ids = item.get("semantic_ids")
        sessions = item.get("llm_session_ids")
        if not _canonical_ids(carrier_ids) or not _canonical_ids(semantic_ids):
            errors.append(f"transition identities are invalid: {identifier}")
        if (
            not isinstance(sessions, list)
            or not sessions
            or any(
                not isinstance(value, str)
                or re.fullmatch(r"[a-z][a-z0-9_-]*:[A-Za-z0-9._:-]+", value) is None
                for value in sessions
            )
        ):
            errors.append(f"transition session provenance is invalid: {identifier}")
        if item.get("source_semantic_sha256") != item.get("current_semantic_sha256"):
            errors.append(f"transition semantic digests differ: {identifier}")
        try:
            target = _resolve_transition_target(root, current, aliases)
        except CarrierTransitionError as error:
            errors.append(str(error))
            continue
        if not _within(root, target) or not target.is_file():
            errors.append(f"transition current carrier is missing: {current}")
            continue
        if hashlib.sha256(target.read_bytes()).hexdigest() != current_digest:
            errors.append(f"transition current carrier digest changed: {current}")
            continue
        try:
            if item.get("kind") == "carrier_relocation":
                semantics = {"carrier_sha256": current_digest}
            elif item.get("kind") == "structured_yaml":
                semantics = decode_historical_envelope(
                    target.read_text(encoding="utf-8")
                )
            elif item.get("kind") == "markdown_frontmatter":
                parsed = parse_frontmatter(target.read_text(encoding="utf-8"))
                if parsed is None or parsed[2] != "toml":
                    raise CarrierTransitionError("current Markdown is not TOML")
                semantics = {
                    "metadata": decode_nulls(parsed[0], null_paths),
                    "body": parsed[1],
                }
            elif item.get("kind") == "markdown_links":
                rendered = target.read_text(encoding="utf-8")
                rewrites = item.get("link_rewrites")
                if not isinstance(rewrites, list):
                    raise CarrierTransitionError("link_rewrites must be a list")
                reconstructed = rendered
                for rewrite in reversed(rewrites):
                    if not isinstance(rewrite, dict) or not all(
                        isinstance(rewrite.get(field), str)
                        for field in (
                            "source",
                            "target",
                            "original_path",
                            "current_path",
                        )
                    ):
                        raise CarrierTransitionError("invalid link rewrite")
                    reconstructed = reconstructed.replace(
                        str(rewrite["target"]), str(rewrite["source"])
                    )
                semantics = {"body": reconstructed}
            else:
                raise CarrierTransitionError("unknown transition kind")
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"cannot reconstruct {identifier}: {error}")
            continue
        if semantic_sha256(semantics) != item.get("current_semantic_sha256"):
            errors.append(f"transition semantic reconstruction changed: {identifier}")
        blob = item.get("source_git_blob")
        source_bytes = _git_blob_bytes(root, blob) if isinstance(blob, str) else None
        if source_bytes is None:
            errors.append(f"transition source Git blob is missing: {identifier}")
        elif hashlib.sha256(source_bytes).hexdigest() != original_digest:
            errors.append(f"transition source Git blob digest changed: {identifier}")
    return errors


def _git_value(root: Path, arguments: list[str]) -> str | None:
    """Handle value using the declared repository contract."""
    completed = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    value = completed.stdout.strip()
    return value if completed.returncode == 0 and value else None


def _git_blob_bytes(root: Path, identifier: str) -> bytes | None:
    """Handle blob bytes using the declared repository contract."""
    completed = subprocess.run(
        ["git", "cat-file", "blob", identifier],
        cwd=root,
        check=False,
        capture_output=True,
    )
    return completed.stdout if completed.returncode == 0 else None


def _within(root: Path, path: Path) -> bool:
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _canonical_ids(value: object) -> bool:
    """Handle ids using the declared repository contract."""
    return (
        isinstance(value, list)
        and len(value) == len(set(value))
        and all(
            isinstance(item, str)
            and re.fullmatch(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+", item) is not None
            for item in value
        )
    )


def _validate_null_paths(
    source: Path, null_paths: list[str], *, markdown: bool
) -> None:
    """Validate null paths using the declared repository contract."""
    for rendered in null_paths:
        parts = _parse_null_path(rendered)
        allowed = markdown and parts[-2:] == ("promotion", "parent_scope")
        allowed = allowed or (
            source.name in {"intake.yaml", "intake.yml"}
            and len(parts) == 3
            and parts[0] == "items"
            and parts[2] == "decision"
        )
        allowed = allowed or (
            source.name in {"pull-requests.yaml", "pull-requests.yml"}
            and len(parts) == 3
            and parts[0] == "pull_requests"
            and parts[2] == "merge_commit"
        )
        if not allowed:
            raise CarrierTransitionError(
                f"undeclared null normalization in {source}: {rendered}"
            )


def _contains_null_sentinel(value: Any) -> bool:
    """Handle null sentinel using the declared repository contract."""
    if value == _NULL_SENTINEL:
        return True
    if isinstance(value, dict):
        return any(_contains_null_sentinel(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_null_sentinel(item) for item in value)
    return False


def _render_null_path(path: tuple[str, ...]) -> str:
    return "/" + "/".join(item.replace("~", "~0").replace("/", "~1") for item in path)


def _parse_null_path(path: str) -> tuple[str, ...]:
    """Parse null path using the declared repository contract."""
    if not path.startswith("/"):
        raise CarrierTransitionError(f"invalid null reconstruction path: {path}")
    if path == "/":
        return ()
    return tuple(
        item.replace("~1", "/").replace("~0", "~") for item in path[1:].split("/")
    )
