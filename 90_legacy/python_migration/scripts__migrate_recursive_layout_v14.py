"""One-time repository migration to the recursive DSET 1.4 layout.

The migration deliberately separates distributable framework material below
``.dset`` from the DSET repository's own visible self-hosting artifacts. It is
repository-specific, conservative, and idempotent after a completed cutover.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any

from dset_toolchain.toml_codec import dumps, load

ROOT = Path(__file__).resolve().parents[1]
DSET = ROOT / ".dset"
SESSION = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"

LAYERS = {
    "meta": ("01_layer_meta", "01_layer_meta"),
    "gov": ("02_layer_gov", "02_layer_gov"),
    "tool": ("03_layer_tool", "03_layer_tool"),
    "skill": ("04_layer_skill", "04_layer_skill"),
    "ops": ("05_layer_ops", "05_layer_ops"),
}
ATOMIC_DIRECTORIES = {"decision", "problem", "question", "qa", "evidence", "analysis"}
REFERENCE_PREFIXES = ("specification-", "procedure-", "navigation-")
AGGREGATES = (
    "artifact-types.toml",
    "artifacts.toml",
    "atoms.toml",
    "governance.toml",
    "intake.toml",
    "lifecycle.toml",
    "legacy-authority.toml",
    "provenance.toml",
)


def main() -> None:
    if not DSET.is_dir():
        raise SystemExit(".dset does not exist")
    if (DSET / "01_layer_meta").is_dir() and not (DSET / "01_layer_meta").exists():
        return

    for _layer, (_old, new) in LAYERS.items():
        (ROOT / new).mkdir(parents=True, exist_ok=True)
    (ROOT / "00_project").mkdir(exist_ok=True)
    (ROOT / "10_versions").mkdir(exist_ok=True)
    (DSET / "00_project").mkdir(exist_ok=True)
    (DSET / "10_versions").mkdir(exist_ok=True)

    settings_additions = _collect_settings_additions()
    _move_project_truth()
    _move_versions()
    _move_layers(settings_additions)
    _move_licenses(settings_additions)
    _rewrite_settings(settings_additions)
    _rewrite_current_paths()
    _write_hubs()


def _collect_settings_additions() -> dict[str, Any]:
    project = DSET / "project"
    aggregate_archive = ROOT / "00_project" / "legacy" / "aggregate-v1.3"
    additions: dict[str, Any] = {}

    def aggregate(name: str) -> dict[str, Any]:
        current = project / name
        archived = aggregate_archive / name
        return load(current if current.is_file() else archived)

    artifact_types = aggregate("artifact-types.toml")
    additions["artifact_catalog"] = {
        "schema_version": "1.0",
        "profile": artifact_types.get("profile", "documentation-v1"),
        "classification": artifact_types.get("classification", {}),
        "exclusions": artifact_types.get("exclusions", []),
        "artifact_types": artifact_types.get("artifact_types", []),
    }
    additions["artifact_structure"] = aggregate("artifacts.toml")
    additions["governance_registry"] = aggregate("governance.toml")
    additions["source_provenance"] = aggregate("provenance.toml")
    additions["version_registry"] = load(DSET / "versions" / "version.toml")

    packages: list[dict[str, Any]] = []
    for _layer, (old, _new) in LAYERS.items():
        path = DSET / old / "package.toml"
        if path.is_file():
            packages.append(load(path))
    additions["package_catalog"] = {"packages": packages}
    return additions


def _move_project_truth() -> None:
    source = DSET / "project"
    destination = ROOT / "00_project"
    legacy = destination / "legacy"
    aggregate_archive = legacy / "aggregate-v1.3"
    aggregate_archive.mkdir(parents=True, exist_ok=True)

    if (source / "intake.toml").is_file():
        _atomize_intake(source / "intake.toml")
    if (source / "lifecycle.toml").is_file():
        _atomize_lifecycle(source / "lifecycle.toml")

    for name in AGGREGATES:
        path = source / name
        if path.is_file():
            _move_file(path, aggregate_archive / name)

    migrations = source / "migrations"
    if migrations.is_dir():
        _merge_tree(migrations, destination / "migrations")

    generated = source / "generated"
    if generated.is_dir():
        _merge_tree(generated, ROOT / ".dset_runtime" / "generated")

    for directory in ATOMIC_DIRECTORIES:
        path = source / directory
        if path.is_dir():
            _merge_tree(path, destination / directory)

    direct_files = list(source.iterdir()) if source.is_dir() else []
    for path in direct_files:
        if not path.is_file():
            continue
        if path.name.endswith(".legacy.toml"):
            _move_file(path, legacy / path.name)
        elif path.name.startswith("analysis-"):
            _move_file(path, destination / "analysis" / path.name)
        elif path.name == "verification.md":
            _move_file(path, destination / "plan-verification.md")
        elif path.suffix == ".md":
            _move_file(path, destination / path.name)

    if source.exists():
        for path in sorted(source.rglob("*"), reverse=True):
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
        if source.is_dir() and not any(source.iterdir()):
            source.rmdir()

    for legacy_file in sorted(DSET.rglob("*.legacy.toml")):
        relative = legacy_file.relative_to(DSET)
        _move_file(legacy_file, legacy / relative)


def _move_versions() -> None:
    source = DSET / "versions"
    if not source.is_dir():
        return
    version_file = source / "version.toml"
    if version_file.exists():
        version_file.unlink()
    _merge_tree(source, ROOT / "10_versions")


def _move_layers(settings_additions: dict[str, Any]) -> None:
    for layer, (old_name, new_name) in LAYERS.items():
        old = DSET / old_name
        framework = DSET / new_name
        project = ROOT / new_name
        if not old.is_dir():
            continue

        for directory in ATOMIC_DIRECTORIES:
            path = old / directory
            if path.is_dir():
                _merge_tree(path, project / directory)

        for path in list(old.glob("plan-*.md")):
            _move_file(path, project / path.name)

        package = old / "package.toml"
        if package.exists():
            package.unlink()

        _merge_tree(old, framework)
        _write_references(layer, framework, project)

    settings_additions["structure_roots"] = {
        "project": "00_project",
        "meta": "01_layer_meta",
        "gov": "02_layer_gov",
        "tool": "03_layer_tool",
        "skill": "04_layer_skill",
        "ops": "05_layer_ops",
        "versions": "10_versions",
    }
    settings_additions["framework_roots"] = {
        "project": ".dset/00_project",
        "meta": ".dset/01_layer_meta",
        "gov": ".dset/02_layer_gov",
        "tool": ".dset/03_layer_tool",
        "skill": ".dset/04_layer_skill",
        "ops": ".dset/05_layer_ops",
        "versions": ".dset/10_versions",
    }


def _write_references(layer: str, framework: Path, project: Path) -> None:
    references = project / "references"
    for path in sorted(framework.glob("*.md")):
        if not path.name.startswith(REFERENCE_PREFIXES):
            continue
        target = path.relative_to(ROOT).as_posix()
        role = "plan" if path.name.startswith("plan-") else "specification"
        if path.name.startswith("procedure-"):
            role = "specification"
        data = {
            "schema_version": "1.0",
            "artifact_type": "reference",
            "target": target,
            "expected_role": role,
            "scope": layer,
            "reason": "Recursive project truth currently equals distributable framework truth.",
        }
        name = path.stem + ".reference.toml"
        _write_text(references / name, dumps(data))


def _atomize_intake(path: Path) -> None:
    data = load(path)
    next_carrier = 124
    for item in data.get("items", []):
        identifier = str(item["id"])
        if identifier == "DSET-PROBLEM-TOOL-006":
            continue
        layer = str(item["scope"]).lower()
        root = ROOT / LAYERS[layer][1]
        item_type = str(item["type"])
        subtype = "none"
        directory = "question" if item_type in {"question", "opportunity"} else "problem"
        semantic_type = directory
        if item_type == "opportunity":
            subtype = "opportunity"
        title = str(item["title"])
        slug = _slug(title)
        carrier = root / directory / f"{identifier}-{slug}.md"
        if carrier.exists():
            continue
        metadata = [
            "+++",
            'artifact_type = "atomic_record"',
            f'artifact_id = "DSET-ATOMIC-RECORD-{next_carrier:03d}"',
            f'type = "{semantic_type}"',
            f'subtype = "{subtype}"',
            f'semantic_id = "{identifier}"',
            'status = "accepted"',
            'priority = "medium"',
            'authority = "operator:anatoly-m-maslennikov"',
            f"claim = {_toml_string(str(item['statement']))}",
            f'llm_session_ids = ["{SESSION}"]',
            "",
            "[scope]",
            'kind = "project"',
            'id = "dset-specs-loops-framework"',
            "",
            "[promotion]",
            "+++",
            "",
            f"# {semantic_type.title()} — {title}",
            "",
            str(item["statement"]),
            "",
            "## Migrated context",
            "",
            f"- Original intake status: `{item.get('status', 'unknown')}`",
            f"- Original owner Change: `{item.get('owner_change', 'none')}`",
        ]
        refs = item.get("external_refs", [])
        if refs:
            metadata.append("- External references: " + ", ".join(str(ref) for ref in refs))
        metadata.extend(
            [
                "",
                "This one-claim carrier replaces the former aggregate intake row. Current",
                "status is derived from atomic lifecycle events.",
                "",
            ]
        )
        _write_text(carrier, "\n".join(metadata))
        next_carrier += 1


def _atomize_lifecycle(path: Path) -> None:
    data = load(path)
    for event in data.get("events", []):
        identifier = str(event["id"])
        atom = str(event["atom_id"])
        layer = _layer_from_id(atom)
        destination = ROOT / LAYERS[layer][1] / "lifecycle"
        name = f"{identifier}-{event['event']}-{atom}.toml"
        if (destination / name).exists():
            continue
        record = {"schema_version": "1.0", "artifact_type": "lifecycle_event", **event}
        _write_text(destination / name, dumps(record))


def _move_licenses(additions: dict[str, Any]) -> None:
    source = ROOT / "third_party" / "licenses"
    target = ROOT / "LICENSES"
    if source.is_dir():
        _merge_tree(source, target)
    third_party = ROOT / "third_party"
    if third_party.is_dir() and not any(third_party.iterdir()):
        third_party.rmdir()
    provenance = additions.get("source_provenance")
    if isinstance(provenance, dict):
        for item in provenance.get("sources", []):
            value = item.get("license_file")
            if isinstance(value, str):
                item["license_file"] = Path(value).name


def _rewrite_settings(additions: dict[str, Any]) -> None:
    path = DSET / "dset_settings.toml"
    text = path.read_text(encoding="utf-8")
    text = text.replace('schema_version = "1.3"', 'schema_version = "1.4"', 1)
    text = text.replace('Accepted for new writers: "1.3".', 'Accepted for new writers: "1.4".')
    text = text.replace('layout = "numbered-layers-v1"', 'layout = "recursive-framework-v1"')
    text = text.replace(
        '[work_items]\nregistry = "00_project/intake.toml"',
        '[work_items]\natomic_roots = ["00_project", "01_layer_meta", "02_layer_gov", "03_layer_tool", "04_layer_skill", "05_layer_ops"]',
    )
    text = text.replace(
        'runbook = ".dset/05_layer_ops/supportability/delivery-runbook.md"',
        'runbook = ".dset/05_layer_ops/supportability/delivery-runbook.md"',
    )
    compilation = (
        "\n[compilation]\n"
        "# Semantic compilation is performed by dset-compile only when requested\n"
        "# or required by a downstream entry gate. New atoms do not force it.\n"
        'mode = "on_demand"\n'
        'skill = "dset-compile"\n'
        'runtime_output = ".dset_runtime/generated"\n'
    )
    marker = "\n[changes]\n"
    if "[compilation]" not in text:
        text = text.replace(marker, compilation + marker, 1)

    for key, value in additions.items():
        if f"[{key}]" in text or f"[[{key}." in text:
            continue
        text += "\n# Migrated canonical settings; this section is not an artifact ledger.\n"
        text += dumps({key: value})
    path.write_text(text, encoding="utf-8")


def _rewrite_current_paths() -> None:
    replacements = {
        ".dset/01_layer_meta": ".dset/01_layer_meta",
        ".dset/02_layer_gov": ".dset/02_layer_gov",
        ".dset/03_layer_tool": ".dset/03_layer_tool",
        ".dset/04_layer_skill": ".dset/04_layer_skill",
        ".dset/05_layer_ops": ".dset/05_layer_ops",
        "01_layer_meta": "01_layer_meta",
        "02_layer_gov": "02_layer_gov",
        "03_layer_tool": "03_layer_tool",
        "04_layer_skill": "04_layer_skill",
        "05_layer_ops": "05_layer_ops",
        "00_project": "00_project",
        "10_versions": "10_versions",
    }
    roots = [DSET, ROOT / "00_project", ROOT / "01_layer_meta", ROOT / "02_layer_gov", ROOT / "03_layer_tool", ROOT / "04_layer_skill", ROOT / "05_layer_ops", ROOT / "10_versions", ROOT / "documentation", ROOT / "methodology", ROOT / "skills", ROOT / "dset_toolchain", ROOT / "scripts", ROOT / "tests", ROOT / "README.md"]
    for root in roots:
        paths = [root] if root.is_file() else list(root.rglob("*")) if root.exists() else []
        for path in paths:
            if not path.is_file() or path.suffix.lower() not in {".md", ".toml", ".json", ".py"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeError:
                continue
            updated = text
            for old, new in replacements.items():
                updated = updated.replace(old, new)
            if updated != text:
                path.write_text(updated, encoding="utf-8")


def _write_hubs() -> None:
    _write_text(
        DSET / "00_project" / "README.md",
        "# DSET framework project surface\n\nThis folder contains current project-wide material distributed with DSET. The framework repository's recursive project artifacts live in `00_project/`.\n",
    )
    _write_text(
        DSET / "10_versions" / "README.md",
        "# DSET version surface\n\nRelease templates are owned by `.dset/05_layer_ops/templates/release/`. A repository's version artifacts live in its configured version root; this framework repository uses `10_versions/`.\n",
    )
    for layer, (_old, new) in LAYERS.items():
        project = ROOT / new
        lines = [
            f"# {layer.upper()} self-hosting project scope",
            "",
            "Atomic artifacts and project-specific plans live here. Current",
            f"distributable framework material lives in [`.dset/{new}/`](../.dset/{new}/).",
            "Exact shared evergreen truth is declared by one-file TOML references",
            "under `references/`; semantic compilation replaces a reference only",
            "when project truth diverges.",
            "",
        ]
        _write_text(project / "README.md", "\n".join(lines))


def _layer_from_id(identifier: str) -> str:
    for layer in LAYERS:
        if f"-{layer.upper()}-" in identifier:
            return layer
    return "gov"


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:72] or "artifact"


def _toml_string(value: str) -> str:
    return dumps({"value": value}).split("=", 1)[1].strip()


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content if content.endswith("\n") else content + "\n", encoding="utf-8")


def _move_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if source.read_bytes() != destination.read_bytes():
            raise RuntimeError(f"refusing conflicting move: {source} -> {destination}")
        source.unlink()
        return
    shutil.move(str(source), str(destination))


def _merge_tree(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for path in sorted(source.iterdir()):
        target = destination / path.name
        if path.is_dir():
            _merge_tree(path, target)
            if path.exists() and not any(path.iterdir()):
                path.rmdir()
        else:
            _move_file(path, target)
    if source.is_dir() and not any(source.iterdir()):
        source.rmdir()


if __name__ == "__main__":
    main()
