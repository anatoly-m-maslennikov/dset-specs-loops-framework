"""Migrate the repository-owned DSET control plane to schema 1.3.

The migration is intentionally repository-specific. It preserves immutable
carrier bytes, records every such relocation, rewrites mutable links against
the complete move map, and combines project facts with operator settings in
one documented ``.dset/dset_settings.toml`` carrier.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dset_toolchain.carrier_transitions import (  # noqa: E402
    relocation_record,
    render_ledger,
)
from dset_toolchain.frontmatter import parse as parse_frontmatter  # noqa: E402
from dset_toolchain.layout import LAYER_DIRECTORIES  # noqa: E402
from dset_toolchain.toml_codec import dumps as dump_toml  # noqa: E402
from dset_toolchain.toml_codec import load as load_toml  # noqa: E402
from dset_toolchain.toml_codec import loads as loads_toml  # noqa: E402

OLD_DSET = ROOT / "dset"
CURRENT_DSET = ROOT / ".dset"
LEGACY_RUNTIME = CURRENT_DSET / "runtime"
CURRENT_RUNTIME = ROOT / ".dset_runtime"
OLD_SCOPES = OLD_DSET / "scopes"
NEW_SETTINGS = CURRENT_DSET / "dset_settings.toml"
OLD_SETTINGS = ROOT / "dset_settings.toml"
OLD_MANIFEST = OLD_SCOPES / "meta" / "dset.toml"
CHANGE_SLUG = "make-dset-self-hosting-and-skills-thin"
OLD_ACTIVE_CHANGE = OLD_SCOPES / "skill" / "changes" / CHANGE_SLUG
LAYERS = {"meta", "gov", "tool", "skill", "ops"}
TEXT_SUFFIXES = {".md", ".toml", ".json", ".py", ".yml", ".yaml"}
MARKDOWN_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
SEMANTIC_ID = re.compile(
    r"DSET-(?:DECISION|REQUIREMENT|CONSTRAINT|CONTRACT|STORY|OUTCOME|"
    r"SCENARIO|INVARIANT|QUESTION|CONFLICT|RISK|OPPORTUNITY|PROBLEM|"
    r"DEFECT|GAP|DEBT|TEST|EVAL|EVALUATION)-([A-Z]+)-\d{3}"
)


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _layer_root(layer: str) -> Path:
    return CURRENT_DSET / LAYER_DIRECTORIES[layer]


def _slug(value: str) -> str:
    value = value.lower().replace("&", " and ")
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", value))


def _metadata(path: Path) -> dict[str, Any]:
    if path.suffix != ".md":
        return {}
    try:
        parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        return {}
    return parsed[0] if parsed is not None and isinstance(parsed[0], dict) else {}


def _semantic_layer(identifier: str) -> str | None:
    match = SEMANTIC_ID.fullmatch(identifier)
    return (
        match.group(1).lower() if match and match.group(1).lower() in LAYERS else None
    )


def _first_semantic_id(metadata: dict[str, Any]) -> str | None:
    direct = metadata.get("semantic_id")
    if isinstance(direct, str):
        return direct
    subject = metadata.get("subject")
    if isinstance(subject, dict) and isinstance(subject.get("id"), str):
        return str(subject["id"])
    relations = metadata.get("relations")
    if isinstance(relations, list):
        for relation in relations:
            target = relation.get("target") if isinstance(relation, dict) else None
            if isinstance(target, str) and _semantic_layer(target) is not None:
                return target
    return None


def _semantic_target(path: Path) -> Path:
    metadata = _metadata(path)
    identifier = metadata.get("semantic_id")
    if not isinstance(identifier, str):
        raise ValueError(f"atomic carrier has no semantic_id: {_relative(path)}")
    layer = _semantic_layer(identifier)
    owner = CURRENT_DSET / "project" if layer is None else _layer_root(layer)
    semantic_type = metadata.get("type")
    if semantic_type not in {"decision", "question", "problem", "qa"}:
        raise ValueError(f"atomic carrier has invalid Type: {_relative(path)}")
    summary = re.sub(r"^DSET-ATOMIC-RECORD-\d+-", "", path.stem)
    return owner / str(semantic_type) / f"{identifier}-{summary}.md"


def _legacy_decision_target(path: Path) -> Path:
    identifier_match = re.search(r"DSET-DECISION-([A-Z]+)-\d{3}", path.name)
    if identifier_match is None:
        raise ValueError(f"legacy Decision has no ID: {_relative(path)}")
    identifier = identifier_match.group(0)
    layer = identifier_match.group(1).lower()
    heading = next(
        (
            line.partition("—")[2].strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.startswith("# Decision —")
        ),
        "decision",
    )
    return _layer_root(layer) / "decision" / f"{identifier}-{_slug(heading)}.md"


def _analysis_target(path: Path) -> Path:
    metadata = _metadata(path)
    layers = {
        layer
        for identifier in _all_semantic_ids(metadata)
        if (layer := _semantic_layer(identifier)) is not None
    }
    owner = (
        CURRENT_DSET / next(iter(layers))
        if len(layers) == 1
        else CURRENT_DSET / "project"
    )
    return owner / "analysis" / path.name


def _evidence_target(path: Path) -> Path:
    metadata = _metadata(path)
    identifier = _first_semantic_id(metadata)
    layer = _semantic_layer(identifier) if identifier else None
    owner = _layer_root(layer) if layer else CURRENT_DSET / "project"
    return owner / "evidence" / path.name


def _all_semantic_ids(value: object) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for child in value.values():
            found.update(_all_semantic_ids(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_all_semantic_ids(child))
    elif isinstance(value, str) and _semantic_layer(value) is not None:
        found.add(value)
    return found


def _package_target(layer: str, relative: Path) -> Path | None:
    name_map = {
        "README.md": "navigation-methodology.md",
        "package.toml": "package.toml",
        "spec.md": "specification-methodology.md",
        "domain.md": "specification-domain.md",
        "contracts.md": "specification-contracts.md",
        "stories.md": "specification-user-stories.md",
        "outcomes.md": "specification-outcomes.md",
        "test-plan.md": "plan-tests.md",
        "eval-plan.md": "plan-evaluations.md",
    }
    if relative.name == "package.legacy.toml":
        return (
            ROOT
            / "dset"
            / "project"
            / "migrations"
            / "legacy"
            / (f"{layer}-package.legacy.toml")
        )
    selected = name_map.get(relative.name)
    if selected is not None:
        return _layer_root(layer) / selected
    if relative.name.startswith("DSET-SPECIFICATION-"):
        return CURRENT_DSET / "project" / relative.name
    return None


def _governance_target(layer: str, relative: Path) -> Path:
    name_map = {
        "README.md": "navigation-governance.md",
        "architecture.md": "specification-architecture.md",
        "artifact-classification.md": "specification-artifact-classification.md",
        "artifact-maintenance.md": "specification-artifact-maintenance.md",
        "work-items.md": "specification-work-items.md",
        "domain-spec-authoring.md": "procedure-domain-spec-authoring.md",
        "eval-planning.md": "procedure-evaluation-planning.md",
        "test-planning.md": "procedure-test-planning.md",
        "build-rules.md": "specification-build-rules.md",
        "delegation-budget.md": "procedure-delegation-budget.md",
        "diagnosis.md": "procedure-diagnosis.md",
        "lifecycle-orchestration.md": "procedure-lifecycle-orchestration.md",
        "prototyping.md": "procedure-prototyping.md",
        "skill-runs.md": "procedure-skill-runs.md",
        "release.md": "procedure-release.md",
        "supportability.md": "specification-supportability.md",
    }
    if relative.name in {"atoms.toml", "legacy-authority.toml", "lifecycle.toml"}:
        return CURRENT_DSET / "project" / relative.name
    return _layer_root(layer) / name_map.get(relative.name, relative.name)


def _active_change_target(path: Path, relative: Path) -> Path | None:
    if relative.name == "change.toml":
        return CURRENT_DSET / "versions" / "changes" / CHANGE_SLUG / "change.toml"
    if relative.name.startswith("DSET-ATOMIC-RECORD-"):
        return _semantic_target(path)
    if relative.name.startswith("decision-DSET-DECISION-"):
        return _legacy_decision_target(path)
    if relative.name.startswith("DSET-ANALYSIS-REPORT-"):
        return _analysis_target(path)
    if relative.name.startswith("DSET-EVIDENCE-RECORD-"):
        return _evidence_target(path)
    if relative.name.startswith("DSET-VERSION-"):
        return CURRENT_DSET / "versions" / relative.name
    if relative.name.startswith("DSET-PLAN-"):
        return CURRENT_DSET / "project" / "analysis" / relative.name
    if relative.parts and relative.parts[0] == "proofs":
        if relative.name == "README.md":
            return CURRENT_DSET / "project" / "evidence" / "README.md"
        return CURRENT_DSET / "project" / "evidence" / "archive" / relative.name
    name_map = {
        "design.md": "specification-design.md",
        "eval-plan.md": "plan-evaluations.md",
        "implementation-plan.md": "plan-implementation.md",
        "proposal.md": "analysis-proposal.md",
        "solution-landscape.md": "analysis-solution-landscape.md",
        "tasks.md": "plan-work.md",
        "test-plan.md": "plan-tests.md",
        "verification.md": "verification.md",
    }
    if relative.parts and relative.parts[0] == "specs":
        spec_map = {
            "methodology.md": "specification-methodology.md",
            "contracts.md": "specification-contracts.md",
            "outcomes.md": "specification-outcomes.md",
        }
        selected = spec_map.get(relative.name)
        return CURRENT_DSET / "project" / selected if selected else None
    selected = name_map.get(relative.name)
    return CURRENT_DSET / "project" / selected if selected else None


def target_for(path: Path) -> Path | None:
    if path == OLD_DSET / "README.md":
        return CURRENT_DSET / "project" / "README.md"
    relative = path.relative_to(OLD_SCOPES)
    layer = relative.parts[0]
    local = Path(*relative.parts[1:])

    if layer == "meta" and local == Path("dset.toml"):
        return None
    if layer == "meta" and local == Path("version.toml"):
        return CURRENT_DSET / "versions" / "version.toml"
    if (
        layer == "gov"
        and local.name
        in {
            "artifact-types.toml",
            "artifacts.toml",
            "governance.toml",
            "intake.toml",
            "intake.legacy.toml",
            "provenance.toml",
            "provenance.legacy.toml",
        }
        and len(local.parts) == 1
    ):
        return CURRENT_DSET / "project" / local.name
    if layer == "gov" and local.parts[0] in {"generated", "migrations"}:
        return CURRENT_DSET / "project" / local
    if layer == "ops" and local.parts[0] == "history":
        return CURRENT_DSET / "versions" / local
    if layer == "ops" and local.parts[0] == "planning":
        return CURRENT_DSET / "versions" / Path(*local.parts[1:])
    if local.parts[0] == "changes":
        if len(local.parts) >= 3 and local.parts[1] == "archive":
            if local.name == "README.md" and len(local.parts) == 3:
                return None
            return CURRENT_DSET / "versions" / "archive" / Path(*local.parts[2:])
        if layer == "skill" and len(local.parts) >= 2 and local.parts[1] == CHANGE_SLUG:
            return _active_change_target(path, Path(*local.parts[2:]))
        return None
    package_prefix = Path("specs/packages/methodology")
    try:
        package_relative = local.relative_to(package_prefix)
    except ValueError:
        package_relative = None
    if package_relative is not None:
        return _package_target(layer, package_relative)
    if local.parts[0] == "governance":
        return _governance_target(layer, Path(*local.parts[1:]))
    return _layer_root(layer) / local


def build_mapping() -> dict[Path, Path]:
    sources = [OLD_DSET / "README.md"]
    sources.extend(path for path in OLD_SCOPES.rglob("*") if path.is_file())
    mapping: dict[Path, Path] = {}
    targets: dict[Path, Path] = {}
    for source in sorted(sources):
        target = target_for(source)
        if target is None:
            continue
        previous = targets.get(target)
        if previous is not None:
            raise ValueError(
                f"layout collision: {_relative(previous)} and {_relative(source)} "
                f"-> {_relative(target)}"
            )
        mapping[source] = target
        targets[target] = source
    return mapping


def build_historical_mapping() -> dict[Path, Path]:
    """Reconstruct the complete source map after an interrupted apply."""

    mapping: dict[Path, Path] = {}
    ledger = CURRENT_DSET / "project" / "migrations" / "carrier-transitions.toml"
    if ledger.is_file():
        data = load_toml(ledger)
        for item in data.get("transitions", []):
            if not isinstance(item, dict) or item.get("authority_decision") != (
                "DSET-REQUIREMENT-GOV-041"
            ):
                continue
            original = item.get("original_path")
            current = item.get("current_path")
            if isinstance(original, str) and isinstance(current, str):
                final = (
                    f".{current}"
                    if current.startswith("dset/")
                    and not current.startswith("dset/scopes/")
                    else current
                )
                mapping[ROOT / original] = ROOT / final
    completed = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", "dset"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    for relative in completed.stdout.splitlines():
        source = ROOT / relative
        if source in mapping or not (
            relative == "dset/README.md" or relative.startswith("dset/scopes/")
        ):
            continue
        try:
            target = target_for(source)
        except (OSError, UnicodeError, ValueError):
            continue
        if target is not None:
            mapping[source] = target
    return mapping


def _is_immutable(source: Path) -> bool:
    relative = _relative(source)
    if "/changes/archive/" in relative:
        return True
    if source.name.startswith(("DSET-ATOMIC-RECORD-", "decision-DSET-DECISION-")):
        return True
    metadata = _metadata(source)
    artifact_type = metadata.get("artifact_type")
    if artifact_type in {"atomic_record", "analysis_report", "evidence_record"}:
        return True
    if artifact_type == "plan" and isinstance(metadata.get("packet_id"), str):
        return True
    if artifact_type == "version":
        return True
    if source.name.endswith(".legacy.toml"):
        return True
    return OLD_ACTIVE_CHANGE in source.parents and "proofs" in source.parts


def _identities(source: Path) -> tuple[list[str], list[str]]:
    metadata = _metadata(source)
    carrier = metadata.get("artifact_id")
    carriers = (
        [carrier]
        if isinstance(carrier, str)
        and re.fullmatch(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+", carrier)
        else []
    )
    semantics = sorted(_all_semantic_ids(metadata))
    if not semantics and source.name.startswith("decision-DSET-DECISION-"):
        match = re.search(r"DSET-DECISION-[A-Z]+-\d{3}", source.name)
        semantics = [match.group(0)] if match else []
    return carriers, semantics


def _combined_settings() -> str:
    settings = OLD_SETTINGS.read_text(encoding="utf-8")
    manifest = OLD_MANIFEST.read_text(encoding="utf-8")
    settings = settings.replace(
        "# DSET project behavior settings.\n",
        "# DSET project settings and manifest.\n",
        1,
    )
    start = settings.index("# This file selects operator-controlled")
    end = settings.index("# All settings below")
    settings = (
        settings[:start]
        + "# This is the sole canonical DSET project configuration. It combines\n"
        + "# project identity and topology with operator-controlled behavior so\n"
        + "# discovery never has to reconcile two competing configuration owners.\n"
        + "# Repository-local governing documents still define the policies and\n"
        + "# values that these settings are allowed to select.\n#\n"
        + settings[end:]
    )
    settings = settings.replace(
        "# New DSET writers use only this filename: dset_settings.toml.\n"
        "# The retired root name dset.toml is read-only migration input. A repository\n"
        "# containing both filenames is invalid because settings must have one "
        "owner.\n",
        "# New DSET writers use only this path: .dset/dset_settings.toml.\n"
        "# Retired root settings and split manifest paths are read-only migration\n"
        "# inputs. Competing configuration carriers fail closed.\n",
    )
    settings = settings.replace(
        '# Accepted: "1.2". Default for a missing settings file: "1.2" behavior.\n'
        'schema_version = "1.2"',
        '# Accepted for new writers: "1.3".\n'
        'schema_version = "1.3"\n'
        'canonical_command = "python -m dset_toolchain verify ."',
    )
    settings = settings.replace(
        "dset/scopes/skill/budget.toml", ".dset/layer_4_skill/budget.toml"
    )
    manifest = (
        manifest.replace(
            'runbook = "dset/scopes/ops/supportability/delivery-runbook.md"',
            'runbook = ".dset/layer_5_ops/supportability/delivery-runbook.md"',
        )
        .replace(
            'registry = "dset/scopes/gov/intake.toml"',
            'registry = ".dset/project/intake.toml"',
        )
        .replace(
            'layout = "layered-v1"',
            'layout = "numbered-layers-v1"',
        )
    )
    manifest_lines = manifest.splitlines()
    if manifest_lines and manifest_lines[0].startswith("schema_version"):
        manifest_lines = manifest_lines[1:]
    manifest_lines = [
        line for line in manifest_lines if not line.startswith("canonical_command = ")
    ]
    return (
        settings.rstrip()
        + "\n\n# Project identity, topology, and executable repository boundaries.\n"
        + "\n".join(manifest_lines).lstrip()
        + "\n"
    )


def _rewrite_markdown_links(
    text: str, source: Path, target: Path, mapping: dict[Path, Path]
) -> str:
    def replace(match: re.Match[str]) -> str:
        label, raw = match.groups()
        wrapped = raw.startswith("<") and raw.endswith(">")
        value = raw[1:-1] if wrapped else raw
        path_text, marker, anchor = value.partition("#")
        if not path_text or path_text.startswith(("http://", "https://", "mailto:")):
            return match.group(0)
        old_target = (source.parent / unquote(path_text)).resolve()
        new_target = mapping.get(old_target)
        if new_target is None:
            return match.group(0)
        rendered = os.path.relpath(new_target, target.parent).replace(os.sep, "/")
        if marker:
            rendered += f"#{anchor}"
        if wrapped:
            rendered = f"<{rendered}>"
        return f"[{label}]({rendered})"

    return MARKDOWN_LINK.sub(replace, text)


def _rewrite_text(
    text: str, source: Path, target: Path, mapping: dict[Path, Path]
) -> str:
    if source.suffix == ".md":
        text = _rewrite_markdown_links(text, source, target, mapping)
    replacements = sorted(
        ((_relative(old), _relative(new)) for old, new in mapping.items()),
        key=lambda pair: len(pair[0]),
        reverse=True,
    )
    for old, new in replacements:
        text = re.sub(rf"(?<![.A-Za-z0-9_-]){re.escape(old)}", new, text)
    text = re.sub(r"(?<![.A-Za-z0-9_-])dset/scopes/", ".dset/", text)
    text = text.replace("root `dset_settings.toml`", "`.dset/dset_settings.toml`")
    text = text.replace("root dset_settings.toml", ".dset/dset_settings.toml")
    return text


def _update_package_manifests() -> None:
    names = {
        "hub": "navigation-methodology.md",
        "domain": "specification-domain.md",
        "spec": "specification-methodology.md",
        "contracts": "specification-contracts.md",
        "stories": "specification-user-stories.md",
        "outcomes": "specification-outcomes.md",
        "test_plan": "plan-tests.md",
        "eval_plan": "plan-evaluations.md",
    }
    for layer in sorted(LAYERS):
        path = _layer_root(layer) / "package.toml"
        text = path.read_text(encoding="utf-8")
        for key, name in names.items():
            text = re.sub(rf'^{key} = "[^"]+"$', f'{key} = "{name}"', text, flags=re.M)
        path.write_text(text, encoding="utf-8", newline="\n")


def _update_artifact_type_registry() -> None:
    """Install the MECE path classification for the slim control plane."""

    path = CURRENT_DSET / "project/artifact-types.toml"
    data = load_toml(path)
    data["path_rules"] = [
        {
            "pattern": pattern,
            "artifact_type": artifact_type,
            **({"artifact_subtype": subtype} if subtype else {}),
        }
        for pattern, artifact_type, subtype in (
            ("**/templates/change/adoption-decision.md", "atomic_record", None),
            ("**/templates/change/decision.md", "atomic_record", None),
            ("**/templates/change/tasks.md", "atomic_record", None),
            ("**/templates/change/dependency-map.toml", "specification", "governance"),
            ("**/templates/change/global-impact.md", "analysis_report", "proposal"),
            ("**/templates/change/specs/package.md", "specification", "governance"),
            ("**/templates/package/contracts.md", "specification", "behavior"),
            ("**/templates/package/stories.md", "specification", "behavior"),
            ("**/templates/package/outcomes.md", "specification", "behavior"),
            ("**/templates/package/*/package.toml", "implementation", "configuration"),
            ("**/templates/artifact-types.toml", "specification", "governance"),
            (
                "**/templates/governance/*/profile.toml",
                "implementation",
                "configuration",
            ),
            ("**/templates/profiles.toml", "implementation", "configuration"),
            (
                "**/templates/enforcement-profiles/*.toml",
                "implementation",
                "configuration",
            ),
            ("**/templates/intake.toml", "implementation", "configuration"),
            ("**/templates/budget.toml", "implementation", "configuration"),
            ("**/templates/dset_settings.toml", "implementation", "configuration"),
            ("**/templates/dependency-policy.toml", "implementation", "configuration"),
            (
                "**/templates/governance/*/architecture.md",
                "specification",
                "governance",
            ),
            (
                "**/templates/governance/*/artifact-classification.md",
                "specification",
                "governance",
            ),
            (
                "**/templates/governance/*/artifact-maintenance.md",
                "specification",
                "governance",
            ),
            ("**/templates/governance/*/work-items.md", "specification", "governance"),
            (
                "**/templates/governance/*/domain-spec-authoring.md",
                "specification",
                "governance",
            ),
            (
                "**/templates/governance/*/eval-planning.md",
                "specification",
                "governance",
            ),
            (
                "**/templates/governance/*/test-planning.md",
                "specification",
                "governance",
            ),
            ("**/templates/governance/*/release.md", "specification", "governance"),
            (
                "**/templates/governance/*/supportability.md",
                "specification",
                "governance",
            ),
            (
                "**/templates/governance/*/delegation-budget.md",
                "specification",
                "governance",
            ),
            ("**/templates/governance/*/diagnosis.md", "specification", "governance"),
            (
                "**/templates/governance/*/lifecycle-orchestration.md",
                "specification",
                "governance",
            ),
            ("**/templates/governance/*/prototyping.md", "specification", "governance"),
            ("**/templates/governance/*/skill-runs.md", "specification", "governance"),
            ("**/templates/governance/*/build-rules.md", "specification", "governance"),
            ("**/analysis-report.md", "analysis_report", None),
            ("**/solution-landscape.md", "analysis_report", "solution_landscape"),
            ("**/root-cause.md", "analysis_report", "root_cause_analysis"),
            (
                "**/technical-investigation.md",
                "analysis_report",
                "technical_investigation",
            ),
            (
                "**/external-audit-analysis.md",
                "analysis_report",
                "external_audit_analysis",
            ),
            ("**/proposal.md", "analysis_report", "proposal"),
            ("**/domain.md", "specification", "domain_model"),
            ("**/spec.md", "specification", "behavior"),
            ("**/design.md", "specification", "design"),
            ("**/implementation-plan.md", "plan", "implementation_plan"),
            ("**/test-plan.md", "plan", "test_plan"),
            ("**/eval-plan.md", "plan", "evaluation_plan"),
            ("**/version-scope.md", "version", "version_scope"),
            ("**/roadmap.md", "version", "roadmap"),
            ("**/release-plan.md", "version", "release_plan"),
            ("**/readiness-record.md", "version", "readiness_record"),
            ("**/release-record.md", "version", "release_record"),
            ("**/change.toml", "version", "change"),
            ("**/verification.md", "verification", None),
            ("**/README.md", "navigation", "hub"),
            (".dset/dset_settings.toml", "implementation", "configuration"),
            (".dset/project/artifact-types.toml", "specification", "governance"),
            (".dset/project/artifacts.toml", "implementation", "configuration"),
            (".dset/project/governance.toml", "implementation", "configuration"),
            (".dset/project/intake.toml", "implementation", "configuration"),
            (".dset/project/provenance.toml", "implementation", "configuration"),
            (".dset/project/atoms.toml", "implementation", "configuration"),
            (".dset/project/legacy-authority.toml", "implementation", "configuration"),
            (".dset/project/lifecycle.toml", "implementation", "configuration"),
            (".dset/project/migrations/*.toml", "implementation", "migration"),
            (".dset/project/generated/*.toml", "derived_view", "traceability_index"),
            (".dset/project/generated/*.md", "derived_view", "health_dashboard"),
            (".dset/project/plan-implementation.md", "plan", "implementation_plan"),
            (".dset/project/plan-work.md", "plan", "implementation_plan"),
            (".dset/project/analysis-*.md", "analysis_report", None),
            (".dset/*/decision/*.md", "atomic_record", None),
            (".dset/*/question/*.md", "atomic_record", None),
            (".dset/*/problem/*.md", "atomic_record", None),
            (".dset/*/qa/*.md", "atomic_record", None),
            (".dset/*/navigation-*.md", "navigation", "hub"),
            (".dset/*/specification-*.md", "specification", "governance"),
            (".dset/*/procedure-*.md", "procedure", "playbook"),
            (".dset/*/plan-tests.md", "plan", "test_plan"),
            (".dset/*/plan-evaluations.md", "plan", "evaluation_plan"),
            (".dset/*/package.toml", "implementation", "configuration"),
            (".dset/*/schemas/*.json", "implementation", "configuration"),
            (".dset/*/dependency-policy.toml", "implementation", "configuration"),
            (".dset/*/budget.toml", "implementation", "configuration"),
            (".dset/*/fixtures/*.toml", "implementation", "test_implementation"),
            (".dset/versions/version.toml", "implementation", "configuration"),
            (".dset/versions/history/*.toml", "implementation", "configuration"),
            (".dset/versions/archive/*/specs/*.md", "specification", "governance"),
            (".dset/versions/archive/*/tasks.md", "atomic_record", None),
            (
                ".dset/layer_3_tool/fixtures/bases/*/specs/example.md",
                "specification",
                "behavior",
            ),
            (".dset/layer_3_tool/fixtures/bases/*/tasks.md", "atomic_record", None),
            ("dset_toolchain/*.py", "implementation", "source_code"),
            ("scripts/*.py", "implementation", "source_code"),
            ("tests/*.py", "implementation", "test_implementation"),
            (".gitattributes", "implementation", "configuration"),
            (".github/workflows/*.yml", "implementation", "configuration"),
            ("dset_toolchain/bootstrap_bundle.json", "implementation", "configuration"),
            ("pyproject.toml", "implementation", "configuration"),
            ("skills/*/agents/*.yaml", "implementation", "configuration"),
            ("skills/*/SKILL.md", "procedure", "playbook"),
            (".github/DELIVERY.md", "procedure", "runbook"),
            ("documentation/maintenance-playbook.md", "procedure", "playbook"),
            (
                ".dset/layer_5_ops/supportability/delivery-runbook.md",
                "procedure",
                "runbook",
            ),
            ("skills/host-distribution.md", "procedure", "runbook"),
            ("documentation/artifact-architecture.md", "specification", "architecture"),
            ("documentation/artifact-types.md", "specification", "governance"),
            ("documentation/authoring-rules.md", "specification", "governance"),
            ("documentation/documentation-v1.md", "specification", "governance"),
            ("documentation/hub-rules.md", "specification", "governance"),
            ("documentation/rationale.md", "analysis_report", None),
            ("methodology/00_Tool Development Playbook.md", "procedure", "playbook"),
            (
                "methodology/01_Spec Authoring Patterns — Service Spec Conventions.md",
                "specification",
                "governance",
            ),
            (
                "methodology/02_Test and Eval Plan Patterns — Proof Artifact "
                "Conventions.md",
                "specification",
                "governance",
            ),
            (
                "methodology/03_Implementation Plan Patterns — Service Build "
                "Conventions.md",
                "specification",
                "governance",
            ),
            (
                "methodology/04_General Build Rules — Tool Code Conventions.md",
                "specification",
                "governance",
            ),
            (
                "methodology/05_Layered Build Standard — DDD, TDD, Small "
                "Functions, Typed Gates.md",
                "specification",
                "governance",
            ),
            (
                "methodology/06_External Grounding — LLM Power-User Practice.md",
                "specification",
                "governance",
            ),
            (
                "methodology/TODO — DSET 0.3 Self-Hosting and "
                "Repository-Governed Skills.md",
                "plan",
                "implementation_plan",
            ),
            (
                "methodology/TODO — Operationalize OpenSpec and Composable "
                "Engineering Skills.md",
                "plan",
                "implementation_plan",
            ),
        )
    ]
    path.write_text(dump_toml(data), encoding="utf-8", newline="\n")
    template_path = _layer_root("gov") / "templates/artifact-types.toml"
    template = load_toml(template_path)
    template["legacy_evidence_paths"] = data["legacy_evidence_paths"]
    template["path_rules"] = data["path_rules"]
    template_path.write_text(dump_toml(template), encoding="utf-8", newline="\n")


def _refresh_governance_hashes() -> None:
    path = CURRENT_DSET / "project/governance.toml"
    data = load_toml(path)
    for rule in data.get("rules", []):
        if not isinstance(rule, dict) or rule.get("customization") != "unmodified":
            continue
        local = rule.get("path")
        source = rule.get("source")
        if not isinstance(local, str) or not isinstance(source, dict):
            continue
        template = source.get("template")
        if isinstance(template, str):
            source["template"] = template.replace("dset/scopes/", ".dset/")
        carrier = ROOT / local
        if carrier.is_file():
            source["sha256"] = hashlib.sha256(carrier.read_bytes()).hexdigest()
    path.write_text(dump_toml(data), encoding="utf-8", newline="\n")


def _repair_mutable_links() -> None:
    path = CURRENT_DSET / "project/verification.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("../../../../../", "../../")
    text = text.replace("../../dset_settings.toml", "../dset_settings.toml")
    path.write_text(text, encoding="utf-8", newline="\n")
    adopter = ROOT / "dset_toolchain/adopter.py"
    text = adopter.read_text(encoding="utf-8").replace(
        "[DSET project control](.dset/project/README.md)",
        "[DSET project control](dset/README.md)",
    )
    adopter.write_text(text, encoding="utf-8", newline="\n")


def _migrate_runtime_boundary() -> None:
    """Move schema 1.3 runtime state out of the committed control root."""

    CURRENT_RUNTIME.mkdir(exist_ok=True)
    if LEGACY_RUNTIME.is_dir():
        for source in sorted(LEGACY_RUNTIME.iterdir()):
            target = CURRENT_RUNTIME / source.name
            if source.name == ".gitignore" and target.exists():
                source.unlink()
                continue
            if target.exists():
                raise ValueError(
                    "runtime boundary collision: "
                    f"{_relative(source)} -> {_relative(target)}"
                )
            shutil.move(source, target)
        LEGACY_RUNTIME.rmdir()
    (CURRENT_RUNTIME / ".gitignore").write_text(
        "*\n!.gitignore\n", encoding="utf-8", newline="\n"
    )


def apply() -> None:
    resumed = NEW_SETTINGS.is_file() and not OLD_SETTINGS.exists()
    if resumed:
        mapping = build_historical_mapping()
        _resume_mutable_rewrites(mapping)
        _migrate_runtime_boundary()
        print("resumed schema 1.3 mutable-reference migration")
        return
    if (
        not OLD_SCOPES.is_dir()
        or not OLD_SETTINGS.is_file()
        or not OLD_MANIFEST.is_file()
    ):
        raise ValueError("expected the complete schema 1.2 source layout")

    mapping = build_mapping()
    immutable = {source for source in mapping if _is_immutable(source)}
    additions = []
    for source in sorted(immutable):
        carriers, semantics = _identities(source)
        additions.append(
            relocation_record(
                ROOT,
                source,
                mapping[source],
                carrier_ids=carriers,
                semantic_ids=semantics,
            )
        )
    ledger = render_ledger(ROOT, additions)
    combined_settings = _combined_settings()

    external_text_files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix in TEXT_SUFFIXES
        and ".git" not in path.parts
        and ".venv" not in path.parts
        and ".uv-cache" not in path.parts
        and path not in mapping
        and path != Path(__file__).resolve()
    ]

    for source, target in sorted(mapping.items(), key=lambda item: _relative(item[0])):
        target.parent.mkdir(parents=True, exist_ok=True)
        if source in immutable:
            shutil.move(source, target)
            continue
        data = source.read_bytes()
        if source.suffix in TEXT_SUFFIXES:
            text = data.decode("utf-8")
            text = _rewrite_text(text, source, target, mapping)
            target.write_text(text, encoding="utf-8", newline="\n")
            source.unlink()
        else:
            shutil.move(source, target)

    NEW_SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    NEW_SETTINGS.write_text(combined_settings, encoding="utf-8", newline="\n")
    OLD_SETTINGS.unlink()
    OLD_MANIFEST.unlink(missing_ok=True)

    ledger_path = CURRENT_DSET / "project" / "migrations" / "carrier-transitions.toml"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(ledger, encoding="utf-8", newline="\n")

    for path in external_text_files:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        rendered = _rewrite_text(text, path, path, mapping)
        if rendered != text:
            path.write_text(rendered, encoding="utf-8", newline="\n")

    _update_package_manifests()
    _update_artifact_type_registry()
    _refresh_governance_hashes()
    _repair_mutable_links()
    _migrate_runtime_boundary()

    for directory in sorted(
        (path for path in (CURRENT_DSET).rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    ):
        with contextlib.suppress(OSError):
            directory.rmdir()

    root_readme = CURRENT_DSET / "README.md"
    root_readme.write_text(
        "# DSET control plane\n\n"
        "- [Project truth and records](project/README.md)\n"
        "- [Settings and project manifest](dset_settings.toml)\n"
        "- [Version lifecycle](versions/README.md)\n"
        "- [META](meta/README.md)\n"
        "- [GOV](gov/README.md)\n"
        "- [TOOL](tool/README.md)\n"
        "- [SKILL](skill/README.md)\n"
        "- [OPS](ops/README.md)\n",
        encoding="utf-8",
        newline="\n",
    )

    if OLD_SCOPES.exists():
        raise ValueError("schema 1.2 scopes root was not emptied")

    print(f"migrated {len(mapping)} carriers; sealed {len(additions)} relocations")


def _resume_mutable_rewrites(mapping: dict[Path, Path]) -> None:
    _retarget_transition_ledger(mapping)
    for path in ROOT.rglob("*"):
        if (
            not path.is_file()
            or path.suffix not in TEXT_SUFFIXES
            or path.relative_to(ROOT).parts[:1] in {("dset",), (".dset",)}
            or ".git" in path.parts
            or ".venv" in path.parts
            or ".uv-cache" in path.parts
            or path.relative_to(ROOT).parts[0] == "tests"
            or path == Path(__file__).resolve()
        ):
            continue
        text = path.read_text(encoding="utf-8")
        rendered = _rewrite_text(text, path, path, mapping)
        if rendered != text:
            path.write_text(rendered, encoding="utf-8", newline="\n")
    _update_package_manifests()
    _repair_transitioned_registries(mapping)
    _update_artifact_type_registry()
    _refresh_governance_hashes()
    _repair_mutable_links()
    for path in OLD_SCOPES.glob("*/changes/README.md"):
        path.unlink(missing_ok=True)
    for path in OLD_SCOPES.glob("*/changes/archive/README.md"):
        path.unlink(missing_ok=True)
    for directory in sorted(
        (path for path in OLD_SCOPES.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    ):
        with contextlib.suppress(OSError):
            directory.rmdir()
    with contextlib.suppress(OSError):
        OLD_SCOPES.rmdir()
    root_readme = CURRENT_DSET / "README.md"
    root_readme.write_text(
        "# DSET control plane\n\n"
        "- [Project truth and records](project/README.md)\n"
        "- [Settings and project manifest](dset_settings.toml)\n"
        "- [Version lifecycle](versions/README.md)\n"
        "- [META](meta/README.md)\n"
        "- [GOV](gov/README.md)\n"
        "- [TOOL](tool/README.md)\n"
        "- [SKILL](skill/README.md)\n"
        "- [OPS](ops/README.md)\n",
        encoding="utf-8",
        newline="\n",
    )


def _retarget_transition_ledger(mapping: dict[Path, Path]) -> None:
    """Point unfinished schema-1.3 relocations at the final hidden root."""

    ledger_path = CURRENT_DSET / "project/migrations/carrier-transitions.toml"
    data = load_toml(ledger_path)
    changed = False
    for item in data.get("transitions", []):
        if (
            not isinstance(item, dict)
            or item.get("kind") != "carrier_relocation"
            or item.get("authority_decision") != "DSET-REQUIREMENT-GOV-041"
        ):
            continue
        original = item.get("original_path")
        if not isinstance(original, str):
            continue
        target = mapping.get(ROOT / original)
        if target is None:
            continue
        if not target.is_file():
            candidates = [
                path
                for path in CURRENT_DSET.rglob(target.name)
                if path.is_file()
                and hashlib.sha256(path.read_bytes()).hexdigest()
                == item.get("current_sha256")
            ]
            if len(candidates) == 1:
                target = candidates[0]
        current = _relative(target)
        if item.get("current_path") != current:
            item["current_path"] = current
            changed = True
    if changed:
        ledger_path.write_text(dump_toml(data), encoding="utf-8", newline="\n")


def _git_text(relative: str) -> str:
    completed = subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def _repair_transitioned_registries(mapping: dict[Path, Path]) -> None:
    ledger_path = CURRENT_DSET / "project/migrations/carrier-transitions.toml"
    ledger = load_toml(ledger_path)
    relocations = {
        str(item["original_path"]): item
        for item in ledger.get("transitions", [])
        if isinstance(item, dict)
        and item.get("kind") == "carrier_relocation"
        and isinstance(item.get("original_path"), str)
    }

    current_atoms_path = CURRENT_DSET / "project/atoms.toml"
    current_atoms = load_toml(current_atoms_path)
    original_atoms = loads_toml(_git_text("dset/scopes/gov/governance/atoms.toml"))
    for record in original_atoms.get("records", []):
        if not isinstance(record, dict):
            continue
        active = str(record.get("current_path", record.get("path", "")))
        transition = relocations.get(active)
        if transition is None:
            continue
        record["current_path"] = transition["current_path"]
        record["current_sha256"] = transition["current_sha256"]
        record["transition_id"] = transition["id"]
    original_records = original_atoms.get("records", [])
    known_semantic_ids = {
        str(record.get("semantic_id"))
        for record in original_records
        if isinstance(record, dict)
    }
    for record in current_atoms.get("records", []):
        if (
            isinstance(record, dict)
            and str(record.get("semantic_id")) not in known_semantic_ids
        ):
            original_records.append(record)
    original_records.sort(key=lambda item: str(item.get("semantic_id", "")))
    current_atoms_path.write_text(
        dump_toml(original_atoms), encoding="utf-8", newline="\n"
    )

    original_authority = loads_toml(
        _git_text("dset/scopes/gov/governance/legacy-authority.toml")
    )
    for record in original_authority.get("records", []):
        fragments = record.get("fragments") if isinstance(record, dict) else None
        if not isinstance(fragments, list):
            continue
        for fragment in fragments:
            if not isinstance(fragment, dict):
                continue
            active = str(fragment.get("current_path", fragment.get("path", "")))
            transition = relocations.get(active)
            if transition is None:
                continue
            fragment["current_path"] = transition["current_path"]
            fragment["current_sha256"] = transition["current_sha256"]
            fragment["transition_id"] = transition["id"]
    (CURRENT_DSET / "project/legacy-authority.toml").write_text(
        dump_toml(original_authority), encoding="utf-8", newline="\n"
    )

    current_types = load_toml(CURRENT_DSET / "project/artifact-types.toml")
    original_types = loads_toml(_git_text("dset/scopes/gov/artifact-types.toml"))
    original_types["legacy_evidence_paths"] = current_types.get(
        "legacy_evidence_paths", []
    )
    original_types["path_rules"] = current_types.get("path_rules", [])
    for entry in original_types.get("legacy_structured", []):
        if not isinstance(entry, dict):
            continue
        active = str(entry.get("current_path", entry.get("path", "")))
        transition = relocations.get(active)
        if transition is not None:
            entry["current_path"] = transition["current_path"]
            entry["current_sha256"] = transition["current_sha256"]
        owner = entry.get("current_owner")
        if isinstance(owner, str):
            target = mapping.get(ROOT / owner)
            if target is not None:
                entry["current_owner"] = _relative(target)
        retained = entry.get("retained_for")
        if isinstance(retained, list):
            for item in retained:
                carrier = item.get("carrier_path") if isinstance(item, dict) else None
                if isinstance(carrier, str):
                    target = mapping.get(ROOT / carrier)
                    if target is not None:
                        item["carrier_path"] = _relative(target)
    (CURRENT_DSET / "project/artifact-types.toml").write_text(
        dump_toml(original_types), encoding="utf-8", newline="\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    arguments = parser.parse_args()
    mapping = build_mapping() if OLD_SCOPES.is_dir() else {}
    if not arguments.apply:
        print(f"planned carriers: {len(mapping)}")
        print(
            f"planned immutable relocations: {sum(_is_immutable(p) for p in mapping)}"
        )
        return
    apply()


if __name__ == "__main__":
    main()
