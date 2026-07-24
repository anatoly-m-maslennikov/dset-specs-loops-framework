"""Provide DSET dependencies behavior."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

from .diagnostics import Diagnostic
from .layout import discover_layout
from .yaml_subset import YamlSubsetError, load

# PACKAGE_BLOCK defines package block; this module owns the default.
PACKAGE_BLOCK = re.compile(r"(?ms)^\[\[package\]\]\n(.*?)(?=^\[\[package\]\]|\Z)")
# NAME defines name; this module owns the default.
NAME = re.compile(r'^name = "([^"]+)"$', re.MULTILINE)
# VERSION defines version; this module owns the default.
VERSION = re.compile(r'^version = "([^"]+)"$', re.MULTILINE)
# REGISTRY defines registry; this module owns the default.
REGISTRY = re.compile(r'^source = \{ registry = "([^"]+)" \}$', re.MULTILINE)
# SPDX defines spdx; this module owns the default.
SPDX = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.+-]*$")


def dependency_policy_path(root: Path) -> Path:
    layout = discover_layout(root.resolve())
    owner = layout.layer_root("implementation") if layout.layered else layout.dset_root
    local = layout._numbered_file(owner, "dependency-policy.toml")
    if local.is_file():
        return local
    if _repository_role(layout.manifest_path) == "framework-source-and-adopter":
        return layout._numbered_file(
            layout.framework_layer_root("implementation"),
            "dependency-policy.toml",
        )
    return local


def validate_dependency_policy(
    root: Path,
    *,
    policy_path: Path | None = None,
    today: date | None = None,
) -> list[Diagnostic]:
    root = root.resolve()
    path = policy_path or dependency_policy_path(root)
    if not path.is_file():
        return []
    current_date = today or date.today()
    try:
        data = load(path)
    except (OSError, UnicodeError, YamlSubsetError) as error:
        return [_diag(path, f"dependency policy cannot be parsed: {error}")]
    if not isinstance(data, dict):
        return [_diag(path, "dependency policy must be a mapping")]
    required = {
        "schema_version",
        "policy_id",
        "version",
        "authority",
        "exception_authority",
        "ecosystems",
        "allow",
        "deny",
        "exceptions",
    }
    diagnostics: list[Diagnostic] = []
    if set(data) != required or data.get("schema_version") != "1.0":
        return [_diag(path, "dependency policy envelope is invalid")]
    for field in ("policy_id", "version", "authority", "exception_authority"):
        if not isinstance(data.get(field), str) or not str(data[field]).strip():
            diagnostics.append(_diag(path, f"dependency policy {field} is required"))
    ecosystems = _ecosystems(root, path, data.get("ecosystems"), diagnostics)
    allowed = _records(path, data.get("allow"), "allow", diagnostics)
    denied = _records(path, data.get("deny"), "deny", diagnostics, sparse=True)
    exceptions = _exceptions(
        path,
        data.get("exceptions"),
        str(data.get("exception_authority", "")),
        current_date,
        diagnostics,
    )
    _unique_records(path, allowed, "allow", diagnostics)
    _unique_records(path, denied, "deny", diagnostics)
    _unique_records(path, exceptions, "exception", diagnostics)
    for ecosystem, config in ecosystems.items():
        if ecosystem != "python-uv":
            diagnostics.append(_diag(path, f"unsupported ecosystem: {ecosystem}"))
            continue
        locked = _uv_packages(root / config["lockfile"], diagnostics)
        local_name = _project_name(root / config["manifest"])
        locked = {key: value for key, value in locked.items() if key != local_name}
        policy_for_ecosystem = {
            (item["name"], item["version"]): item
            for item in allowed
            if item["ecosystem"] == ecosystem
        }
        active_exceptions = {
            (item["name"], item["version"]): item
            for item in exceptions
            if item["ecosystem"] == ecosystem and item["active"]
        }
        denied_names = {
            (item["name"], item.get("version"))
            for item in denied
            if item["ecosystem"] == ecosystem
        }
        for name, locked_item in locked.items():
            key = (name, locked_item["version"])
            exception = active_exceptions.get(key)
            if (
                (name, None) in denied_names or key in denied_names
            ) and exception is None:
                diagnostics.append(_diag(path, f"denied dependency is locked: {name}"))
                continue
            record = policy_for_ecosystem.get(key) or exception
            if record is None:
                diagnostics.append(
                    _diag(
                        path,
                        f"locked dependency is not allowed exactly: {name}=={key[1]}",
                    )
                )
                continue
            if record["registry"] != config["registry"]:
                diagnostics.append(
                    _diag(
                        path,
                        f"dependency violates ecosystem registry: {name}=={key[1]}",
                    )
                )
            if record["registry"] != locked_item["registry"]:
                diagnostics.append(
                    _diag(path, f"dependency registry drift: {name}=={key[1]}")
                )
        locked_keys = {(name, item["version"]) for name, item in locked.items()}
        for key in policy_for_ecosystem:
            if key not in locked_keys:
                diagnostics.append(
                    _diag(
                        path,
                        "allowed dependency is absent from lockfile: "
                        f"{key[0]}=={key[1]}",
                    )
                )
    return sorted(set(diagnostics))


def dependency_summary(root: Path) -> dict[str, Any]:
    path = dependency_policy_path(root)
    diagnostics = validate_dependency_policy(root, policy_path=path)
    data = load(path) if path.is_file() else {}
    return {
        "policy": path.relative_to(root.resolve()).as_posix(),
        "status": "pass" if not diagnostics else "fail",
        "allowed": len(data.get("allow", [])) if isinstance(data, dict) else 0,
        "denied": len(data.get("deny", [])) if isinstance(data, dict) else 0,
        "exceptions": len(data.get("exceptions", [])) if isinstance(data, dict) else 0,
        "diagnostics": [item.message for item in diagnostics],
    }


def _ecosystems(
    root: Path,
    path: Path,
    value: object,
    diagnostics: list[Diagnostic],
) -> dict[str, dict[str, str]]:
    if not isinstance(value, list) or not value:
        diagnostics.append(_diag(path, "ecosystems must be a non-empty list"))
        return {}
    result: dict[str, dict[str, str]] = {}
    for item in value:
        fields = {"id", "manifest", "lockfile", "registry"}
        if not isinstance(item, dict) or set(item) != fields:
            diagnostics.append(_diag(path, "ecosystem entry is invalid"))
            continue
        if not all(isinstance(item[field], str) and item[field] for field in fields):
            diagnostics.append(_diag(path, "ecosystem values must be non-empty"))
            continue
        identifier = str(item["id"])
        if identifier in result:
            diagnostics.append(_diag(path, f"duplicate ecosystem: {identifier}"))
            continue
        for field in ("manifest", "lockfile"):
            target = root / str(item[field])
            if not target.is_file():
                diagnostics.append(
                    _diag(path, f"dependency {field} is missing: {item[field]}")
                )
        result[identifier] = {field: str(item[field]) for field in fields}
    return result


def _records(
    path: Path,
    value: object,
    label: str,
    diagnostics: list[Diagnostic],
    *,
    sparse: bool = False,
) -> list[dict[str, str]]:
    if not isinstance(value, list):
        diagnostics.append(_diag(path, f"{label} must be a list"))
        return []
    records: list[dict[str, str]] = []
    full = {
        "ecosystem",
        "name",
        "version",
        "registry",
        "license",
        "provenance",
        "rationale",
    }
    sparse_fields = {"ecosystem", "name", "version", "rationale"}
    for item in value:
        if not isinstance(item, dict) or (
            set(item) != full
            and not (
                sparse
                and set(item) in ({"ecosystem", "name", "rationale"}, sparse_fields)
            )
        ):
            diagnostics.append(_diag(path, f"{label} dependency entry is invalid"))
            continue
        if not all(isinstance(raw, str) and raw.strip() for raw in item.values()):
            diagnostics.append(
                _diag(path, f"{label} dependency values must be non-empty")
            )
            continue
        if not sparse:
            if not SPDX.fullmatch(str(item["license"])):
                diagnostics.append(
                    _diag(path, f"{label} dependency license must be SPDX")
                )
            if not str(item["provenance"]).startswith("https://"):
                diagnostics.append(
                    _diag(path, f"{label} dependency provenance must use HTTPS")
                )
        records.append({str(key): str(raw) for key, raw in item.items()})
    return records


def _exceptions(
    path: Path,
    value: object,
    authority: str,
    current_date: date,
    diagnostics: list[Diagnostic],
) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        diagnostics.append(_diag(path, "exceptions must be a list"))
        return []
    records: list[dict[str, Any]] = []
    required = {
        "id",
        "ecosystem",
        "name",
        "version",
        "registry",
        "license",
        "provenance",
        "authority",
        "expires_on",
        "rationale",
    }
    for item in value:
        if not isinstance(item, dict) or set(item) != required:
            diagnostics.append(_diag(path, "dependency exception entry is invalid"))
            continue
        if not all(isinstance(raw, str) and raw.strip() for raw in item.values()):
            diagnostics.append(
                _diag(path, "dependency exception values must be non-empty")
            )
            continue
        try:
            expiry = date.fromisoformat(str(item["expires_on"]))
        except ValueError:
            diagnostics.append(_diag(path, f"invalid exception expiry: {item['id']}"))
            continue
        active = expiry >= current_date
        if not active:
            diagnostics.append(
                _diag(path, f"dependency exception expired: {item['id']}")
            )
        if item["authority"] != authority:
            diagnostics.append(
                _diag(path, f"dependency exception authority mismatch: {item['id']}")
            )
        if not SPDX.fullmatch(str(item["license"])):
            diagnostics.append(
                _diag(path, f"dependency exception license must be SPDX: {item['id']}")
            )
        if not str(item["provenance"]).startswith("https://"):
            diagnostics.append(
                _diag(
                    path,
                    f"dependency exception provenance must use HTTPS: {item['id']}",
                )
            )
        record = {str(key): raw for key, raw in item.items()}
        record["active"] = active
        records.append(record)
    return records


def _unique_records(
    path: Path,
    records: list[dict[str, Any]],
    label: str,
    diagnostics: list[Diagnostic],
) -> None:
    keys = [
        (item.get("ecosystem"), item.get("name"), item.get("version"))
        for item in records
    ]
    if len(keys) != len(set(keys)):
        diagnostics.append(_diag(path, f"duplicate {label} dependency entry"))


def _uv_packages(
    path: Path, diagnostics: list[Diagnostic]
) -> dict[str, dict[str, str]]:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    packages: dict[str, dict[str, str]] = {}
    for match in PACKAGE_BLOCK.finditer(text):
        block = match.group(1)
        name_match = NAME.search(block)
        version_match = VERSION.search(block)
        registry_match = REGISTRY.search(block)
        if name_match is None or version_match is None:
            diagnostics.append(_diag(path, "uv.lock package lacks name or version"))
            continue
        name = name_match.group(1)
        packages[name] = {
            "version": version_match.group(1),
            "registry": registry_match.group(1) if registry_match else "local",
        }
    return packages


def _project_name(path: Path) -> str:
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8")
    project = re.search(r'(?ms)^\[project\]\n.*?^name = "([^"]+)"$', text)
    return project.group(1) if project else ""


def _repository_role(manifest_path: Path) -> str | None:
    try:
        manifest = load(manifest_path)
    except (OSError, UnicodeError, YamlSubsetError):
        return None
    if not isinstance(manifest, dict):
        return None
    project = manifest.get("project")
    if not isinstance(project, dict):
        return None
    role = project.get("repository_role")
    return role if isinstance(role, str) else None


def _diag(path: Path, message: str) -> Diagnostic:
    return Diagnostic("DSET-E163", path, message)
