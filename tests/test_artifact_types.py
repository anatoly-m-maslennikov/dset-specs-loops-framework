from __future__ import annotations

import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from typing import Any

from dset_toolchain.validation import (
    ARTIFACT_TYPE_SUBTYPES,
    validate_artifact_type_registry,
)
from dset_toolchain.yaml_subset import load, loads

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "dset/scopes/gov/artifact-types.yaml"
TEMPLATE_PATH = ROOT / "dset/scopes/gov/templates/artifact-types.yaml"
SCHEMA_PATH = ROOT / "dset/scopes/gov/schemas/artifact-types.schema.json"


class ArtifactTypeRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = load(REGISTRY_PATH)
        assert isinstance(self.registry, dict)

    def test_live_registry_is_valid_and_matches_template(self) -> None:
        self.assertEqual(
            validate_artifact_type_registry(ROOT, REGISTRY_PATH, self.registry), []
        )
        self.assertEqual(self.registry, load(TEMPLATE_PATH))
        json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_exact_thirteen_types_and_analysis_subtypes_are_registered(self) -> None:
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
                content = (template_root / name).read_text(encoding="utf-8")
                self.assertTrue(
                    content.startswith("---\nartifact_type: analysis_report")
                )
                self.assertIn(f"artifact_subtype: {subtype}", content)

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

    def test_type_only_names_are_default_and_subtype_names_are_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            base = root / "APP-SPECIFICATION-001-core.md"
            self._write_classified(base, "APP-SPECIFICATION-001")
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
            advanced = root / "APP-SPECIFICATION-VERSION-SCOPE-001-core.md"
            self._write_classified(
                advanced,
                "APP-SPECIFICATION-VERSION-SCOPE-001",
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
        settings = (ROOT / "dset.toml").read_text(encoding="utf-8")
        template = (ROOT / "dset/scopes/meta/templates/dset.toml").read_text(
            encoding="utf-8"
        )
        self.assertEqual(settings, template)
        self.assertIn("artifact_subtype_in_names = false", settings)
        self.assertIn('artifact_creation_strictness = "medium"', settings)

    def test_release_lifecycle_projection_is_compiled(self) -> None:
        rule = (
            ROOT / "dset/scopes/gov/governance/artifact-classification.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "`specification/version_scope`",
            "`plan/roadmap`",
            "`plan/release_plan`",
            "Readiness Record",
            "Release Record",
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
            "---\n"
            "artifact_type: specification\n"
            "artifact_subtype: version_scope\n"
            f"artifact_id: {artifact_id}\n"
            "---\n",
            encoding="utf-8",
        )

    @staticmethod
    def _matches(path: PurePosixPath, pattern: str) -> bool:
        return path.match(pattern) or (
            pattern.startswith("**/") and path.match(pattern.removeprefix("**/"))
        )

    @staticmethod
    def _direct_classification(path: Path) -> tuple[str, str | None] | None:
        if path.suffix.lower() != ".md":
            return None
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0] != "---":
            return None
        try:
            end = lines.index("---", 1)
        except ValueError:
            return None
        metadata = loads("\n".join(lines[1:end]))
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
