from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from typing import Any

from dset_toolchain.frontmatter import metadata as frontmatter_metadata
from dset_toolchain.frontmatter import render as render_frontmatter
from dset_toolchain.layout import discover_layout
from dset_toolchain.validation import (
    ARTIFACT_TYPE_SUBTYPES,
    validate_artifact_type_registry,
)
from dset_toolchain.yaml_subset import load

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = discover_layout(ROOT)
REGISTRY_PATH = LAYOUT.artifact_type_registry_path
TEMPLATE_PATH = LAYOUT.find_template("artifact-types.toml")
SCHEMA_PATH = ROOT / "dset/scopes/gov/schemas/artifact-types.schema.json"


class ArtifactTypeRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = load(REGISTRY_PATH)
        assert isinstance(self.registry, dict)

    def test_live_registry_owns_exact_project_legacy_customization(self) -> None:
        template = load(TEMPLATE_PATH)
        assert isinstance(template, dict)
        self.assertEqual(template["legacy_structured"], [])
        self.assertEqual(len(self.registry["legacy_structured"]), 10)
        self.assertNotEqual(self.registry, template)
        for key in set(template) - {"legacy_structured"}:
            self.assertEqual(self.registry[key], template[key])
        with tempfile.TemporaryDirectory() as raw:
            self.assertEqual(
                validate_artifact_type_registry(Path(raw), TEMPLATE_PATH, template),
                [],
            )
        json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_legacy_structured_registry_rejects_wildcards_and_duplicates(self) -> None:
        data = self._copy()
        data["legacy_structured"][0]["path"] = "dset/**/package.yaml"
        self.assert_error(data, "wildcard legacy_structured path")

        data = self._copy()
        duplicate = copy.deepcopy(data["legacy_structured"][0])
        data["legacy_structured"].append(duplicate)
        self.assert_error(data, "duplicate legacy_structured path")

    def test_legacy_structured_registry_fails_missing_owner_and_unregistered_pair(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            registry_path = root / "dset/scopes/gov/artifact-types.yaml"
            snapshot = root / "dset/scopes/gov/items.yaml"
            snapshot.parent.mkdir(parents=True)
            snapshot.write_text("id: historical\n", encoding="utf-8")
            snapshot.with_suffix(".toml").write_text(
                'id = "current"\n', encoding="utf-8"
            )
            data = self._copy()
            data["legacy_structured"] = []
            diagnostics = validate_artifact_type_registry(root, registry_path, data)
            self.assertTrue(
                any(
                    "unregistered YAML/TOML pair" in item.message
                    for item in diagnostics
                )
            )

            snapshot.with_suffix(".toml").unlink()
            data["legacy_structured"] = [
                {
                    "path": "dset/scopes/gov/items.yaml",
                    "sha256": hashlib.sha256(snapshot.read_bytes()).hexdigest(),
                    "current_owner": "dset/scopes/gov/items.toml",
                    "artifact_type": "implementation",
                    "artifact_subtype": "configuration",
                    "retained_for": [
                        {
                            "carrier_path": "dset/scopes/gov/changes/x/proofs/p.md",
                            "reason": "Historical proof link.",
                        }
                    ],
                }
            ]
            diagnostics = validate_artifact_type_registry(root, registry_path, data)
            self.assertTrue(
                any("current owner is missing" in item.message for item in diagnostics)
            )

    def test_exact_eleven_types_and_direct_subtypes_are_registered(self) -> None:
        catalog = {
            entry["id"]: frozenset(entry["subtypes"])
            for entry in self.registry["artifact_types"]
        }
        self.assertEqual(catalog, ARTIFACT_TYPE_SUBTYPES)
        self.assertEqual(
            catalog["analysis_report"],
            {
                "solution_landscape",
                "root_cause_analysis",
                "proposal",
                "technical_investigation",
                "external_audit_analysis",
            },
        )
        self.assertEqual(
            catalog["version"],
            {
                "roadmap",
                "version_scope",
                "change",
                "release_plan",
                "readiness_record",
                "release_record",
            },
        )
        self.assertNotIn("version_scope", catalog["specification"])
        self.assertTrue({"roadmap", "release_plan"}.isdisjoint(catalog["plan"]))

    def test_analysis_report_templates_cover_every_direct_subtype(self) -> None:
        template_root = ROOT / "dset/scopes/gov/templates/change"
        expected = {
            "solution-landscape.md": "solution_landscape",
            "root-cause.md": "root_cause_analysis",
            "proposal.md": "proposal",
            "technical-investigation.md": "technical_investigation",
            "external-audit-analysis.md": "external_audit_analysis",
        }
        for name, subtype in expected.items():
            with self.subTest(name=name):
                metadata = frontmatter_metadata(template_root / name)
                assert metadata is not None
                self.assertEqual(metadata["artifact_type"], "analysis_report")
                self.assertEqual(metadata["artifact_subtype"], subtype)

    def test_every_distributed_template_has_one_effective_classification(self) -> None:
        template_files = sorted(
            path
            for scope in (ROOT / "dset/scopes").iterdir()
            for path in (scope / "templates").rglob("*")
            if path.is_file()
        )
        self.assertTrue(template_files)
        for path in template_files:
            relative = PurePosixPath(path.relative_to(ROOT).as_posix())
            matches = [
                rule
                for rule in self.registry["path_rules"]
                if self._matches(relative, rule["pattern"])
            ]
            direct = self._direct_classification(path)
            with self.subTest(path=relative.as_posix()):
                self.assertLessEqual(len(matches), 1, matches)
                self.assertTrue(direct is not None or matches, "unclassified template")
                if direct is not None and matches:
                    expected = (
                        matches[0]["artifact_type"],
                        matches[0].get("artifact_subtype"),
                    )
                    self.assertEqual(direct, expected)

    def test_unknown_type_is_rejected(self) -> None:
        data = self._copy()
        data["path_rules"][0]["artifact_type"] = "unknown"
        self.assert_error(data, "unknown artifact type")

    def test_mismatched_subtype_is_rejected(self) -> None:
        data = self._copy()
        data["path_rules"][0]["artifact_subtype"] = "roadmap"
        self.assert_error(data, "subtype/type mismatch")

    def test_nested_subtype_is_rejected(self) -> None:
        data = self._copy()
        analysis = self._type(data, "analysis_report")
        analysis["subtypes"][0] = {"solution_landscape": ["vendor_comparison"]}
        self.assert_error(data, "invalid or nested subtype")

    def test_duplicate_primary_question_is_rejected(self) -> None:
        data = self._copy()
        data["artifact_types"][1]["primary_question"] = data["artifact_types"][0][
            "primary_question"
        ]
        self.assert_error(data, "duplicate primary_question")

    def test_direct_metadata_fields_are_fixed(self) -> None:
        data = self._copy()
        data["classification"]["direct_metadata_fields"]["type"] = "type"
        self.assert_error(data, "direct metadata fields")

    def test_duplicate_path_rule_is_rejected(self) -> None:
        data = self._copy()
        data["path_rules"].append(copy.deepcopy(data["path_rules"][0]))
        self.assert_error(data, "duplicate path rule")

    def test_multiple_matching_path_rules_are_rejected(self) -> None:
        data = self._copy()
        data["path_rules"].append(
            {
                "pattern": "dset/**/spec.md",
                "artifact_type": "specification",
                "artifact_subtype": "behavior",
            }
        )
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path = root / "dset/sample/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text("# Spec\n", encoding="utf-8")
            diagnostics = validate_artifact_type_registry(root, REGISTRY_PATH, data)
        self.assertTrue(
            any("matches multiple rules" in item.message for item in diagnostics)
        )

    def test_direct_metadata_subtype_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path = root / "APP-SPECIFICATION-001-example.md"
            path.write_text(
                "---\n"
                "artifact_type: specification\n"
                "artifact_subtype: roadmap\n"
                "artifact_id: APP-SPECIFICATION-001\n"
                "---\n",
                encoding="utf-8",
            )
            diagnostics = validate_artifact_type_registry(
                root,
                REGISTRY_PATH,
                self.registry,
                project_key="APP",
            )
        self.assertTrue(
            any(
                "direct metadata has a subtype/type mismatch" in item.message
                for item in diagnostics
            )
        )

    def test_git_ignored_runtime_artifacts_are_outside_classification(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / ".gitignore").write_text("tmp/\n", encoding="utf-8")
            ignored = root / "tmp/APP-SPECIFICATION-001-runtime.md"
            ignored.parent.mkdir(parents=True)
            ignored.write_text(
                "---\nartifact_type: unknown\n"
                "artifact_id: APP-SPECIFICATION-001\n---\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)

            diagnostics = validate_artifact_type_registry(
                root,
                REGISTRY_PATH,
                self.registry,
                project_key="APP",
            )

            self.assertEqual(diagnostics, [])

    def test_unclassified_carrier_fails_closed_and_exclusion_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path = root / "notes.md"
            path.write_text("# Notes\n", encoding="utf-8")
            diagnostics = validate_artifact_type_registry(
                root, REGISTRY_PATH, self.registry
            )
            self.assertTrue(
                any(
                    "no artifact classification or exclusion" in item.message
                    for item in diagnostics
                )
            )

            data = self._copy()
            data["exclusions"].append(
                {
                    "pattern": "notes.md",
                    "rationale": "Fixture-only non-artifact carrier.",
                }
            )
            self.assertEqual(
                validate_artifact_type_registry(root, REGISTRY_PATH, data), []
            )

    def test_procedure_paths_are_registered(self) -> None:
        expected = {
            "skills/*/SKILL.md": ("procedure", "playbook"),
            "documentation/maintenance-playbook.md": ("procedure", "playbook"),
            "dset/scopes/ops/supportability/delivery-runbook.md": (
                "procedure",
                "runbook",
            ),
        }
        actual = {
            item["pattern"]: (
                item["artifact_type"],
                item.get("artifact_subtype"),
            )
            for item in self.registry["path_rules"]
        }
        for pattern, classification in expected.items():
            self.assertEqual(actual[pattern], classification)

    def test_legacy_evidence_compatibility_is_an_exact_finite_list(self) -> None:
        paths = self.registry["legacy_evidence_paths"]
        self.assertTrue(paths)
        self.assertEqual(len(paths), len(set(paths)))
        self.assertTrue(all("/proofs/" in path for path in paths))
        self.assertTrue(all(not any(char in path for char in "*?[]") for path in paths))

    def test_type_only_names_are_default_and_subtype_names_are_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            base = root / "APP-VERSION-001-core.md"
            self._write_classified(base, "APP-VERSION-001")
            self.assertEqual(
                validate_artifact_type_registry(
                    root,
                    REGISTRY_PATH,
                    self.registry,
                    project_key="APP",
                ),
                [],
            )
            base.unlink()
            advanced = root / "APP-VERSION-VERSION-SCOPE-001-core.md"
            self._write_classified(
                advanced,
                "APP-VERSION-VERSION-SCOPE-001",
            )
            default_diagnostics = validate_artifact_type_registry(
                root,
                REGISTRY_PATH,
                self.registry,
                project_key="APP",
            )
            self.assertTrue(
                any(item.code == "DSET-E157" for item in default_diagnostics)
            )
            self.assertEqual(
                validate_artifact_type_registry(
                    root,
                    REGISTRY_PATH,
                    self.registry,
                    project_key="APP",
                    include_subtype_in_names=True,
                ),
                [],
            )

    def test_project_settings_default_to_type_only_names(self) -> None:
        settings = (ROOT / "dset_settings.toml").read_text(encoding="utf-8")
        template = (ROOT / "dset/scopes/meta/templates/dset_settings.toml").read_text(
            encoding="utf-8"
        )
        self.assertEqual(settings, template)
        self.assertIn("subtype_in_names = false", settings)
        self.assertIn('creation_strictness = "medium"', settings)

    def test_release_lifecycle_projection_is_compiled(self) -> None:
        rule = (
            ROOT / "dset/scopes/gov/governance/artifact-classification.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "`version`",
            "`roadmap`",
            "`version_scope`",
            "`change`",
            "`release_plan`",
            "`readiness_record`",
            "`release_record`",
        ):
            self.assertIn(phrase, rule)

    def assert_error(self, data: dict[str, Any], fragment: str) -> None:
        diagnostics = validate_artifact_type_registry(ROOT, REGISTRY_PATH, data)
        self.assertTrue(
            any(
                item.code == "DSET-E156" and fragment in item.message
                for item in diagnostics
            ),
            diagnostics,
        )

    def _copy(self) -> dict[str, Any]:
        return copy.deepcopy(self.registry)

    @staticmethod
    def _write_classified(path: Path, artifact_id: str) -> None:
        path.write_text(
            render_frontmatter(
                {
                    "artifact_type": "version",
                    "artifact_subtype": "version_scope",
                    "artifact_id": artifact_id,
                },
                "",
            ),
            encoding="utf-8",
        )

    @staticmethod
    def _matches(path: PurePosixPath, pattern: str) -> bool:
        if "/" not in pattern:
            return path.as_posix() == pattern
        return path.match(pattern) or (
            pattern.startswith("**/") and path.match(pattern.removeprefix("**/"))
        )

    @staticmethod
    def _direct_classification(path: Path) -> tuple[str, str | None] | None:
        if path.suffix.lower() != ".md":
            return None
        metadata = frontmatter_metadata(path)
        if not isinstance(metadata, dict) or metadata.get("artifact_type") is None:
            return None
        subtype = metadata.get("artifact_subtype")
        return (
            str(metadata["artifact_type"]),
            str(subtype) if subtype is not None else None,
        )

    @staticmethod
    def _type(data: dict[str, Any], identifier: str) -> dict[str, Any]:
        return next(item for item in data["artifact_types"] if item["id"] == identifier)


if __name__ == "__main__":
    unittest.main()
