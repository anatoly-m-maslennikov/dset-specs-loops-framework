from __future__ import annotations

import contextlib
import hashlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any, cast

from dset_toolchain.adopter import create_adopter
from dset_toolchain.cli import main
from dset_toolchain.errors import DsetCommandError
from dset_toolchain.governance import (
    diff_governance,
    find_repository,
    materialize_governance,
    refresh_customization,
    resolve_workflow,
    validate_governance,
)
from dset_toolchain.validation import validate_repository
from dset_toolchain.yaml_subset import dump, load

ROOT = Path(__file__).resolve().parents[1]


class GovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "adopter"
        create_adopter(ROOT, self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_valid_registry_resolves_stable_order(self) -> None:
        self.assertEqual(validate_governance(self.root), [])
        resolved, diagnostics = resolve_workflow(self.root, "domain-clarification")
        self.assertEqual(diagnostics, [])
        self.assertIsNotNone(resolved)
        assert resolved is not None
        self.assertEqual(resolved["workflow_id"], "domain-clarification")
        self.assertEqual(resolved["customization"], "unmodified")
        self.assertGreater(len(cast(list[Any], resolved["rules"])), 3)

    def test_find_repository_walks_upward(self) -> None:
        nested = self.root / "src" / "feature"
        nested.mkdir(parents=True)
        self.assertEqual(find_repository(nested), self.root)

    def test_cli_resolve_reports_rule_identity(self) -> None:
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = main(
                [
                    "rules",
                    "resolve",
                    "domain-clarification",
                    str(self.root),
                    "--format",
                    "json",
                ]
            )
        self.assertEqual(result, 0)
        output = stream.getvalue()
        self.assertIn('"workflow_id": "domain-clarification"', output)
        self.assertIn('"customization": "unmodified"', output)

    def test_resolution_is_stable_and_read_only(self) -> None:
        registry = self.root / "dset" / "governance.yaml"
        before = hashlib.sha256(registry.read_bytes()).hexdigest()
        first, first_diagnostics = resolve_workflow(self.root, "diagnosis")
        second, second_diagnostics = resolve_workflow(self.root, "diagnosis")
        self.assertEqual(first_diagnostics, [])
        self.assertEqual(second_diagnostics, [])
        self.assertEqual(first, second)
        self.assertEqual(hashlib.sha256(registry.read_bytes()).hexdigest(), before)

    def test_registry_failure_codes_are_stable(self) -> None:
        cases = {
            "missing-registry": ("DSET-E130", self._remove_registry),
            "missing-owner": ("DSET-E131", self._missing_owner),
            "duplicate-owner": ("DSET-E132", self._duplicate_owner),
            "missing-document": ("DSET-E133", self._missing_document),
            "outside-root": ("DSET-E134", self._outside_root),
            "dependency-cycle": ("DSET-E135", self._dependency_cycle),
            "incompatible-profile": ("DSET-E137", self._incompatible_profile),
            "wrapper-mismatch": ("DSET-E138", self._wrapper_mismatch),
        }
        for name, (expected, mutation) in cases.items():
            with self.subTest(case=name), tempfile.TemporaryDirectory() as raw:
                target = Path(raw) / "adopter"
                create_adopter(ROOT, target)
                mutation(target)
                codes = {item.code for item in validate_governance(target)}
                self.assertIn(expected, codes)

    def test_unknown_workflow_is_stable(self) -> None:
        resolved, diagnostics = resolve_workflow(self.root, "unknown-workflow")
        self.assertIsNone(resolved)
        self.assertEqual([item.code for item in diagnostics], ["DSET-E136"])

    def test_deprecated_grill_workflow_is_not_registered(self) -> None:
        resolved, diagnostics = resolve_workflow(self.root, "domain-grilling")
        self.assertIsNone(resolved)
        self.assertEqual([item.code for item in diagnostics], ["DSET-E136"])

    def test_customization_changes_rules_not_wrapper(self) -> None:
        wrapper = self.root / "skills" / "dset-clarify" / "SKILL.md"
        before = hashlib.sha256(wrapper.read_bytes()).hexdigest()
        rule = self.root / "dset" / "governance" / "domain-spec-authoring.md"
        rule.write_text(
            rule.read_text(encoding="utf-8") + "\nLocal output rule.\n",
            encoding="utf-8",
        )
        self.assertIn(
            "DSET-E139", {item.code for item in validate_governance(self.root)}
        )
        refresh_customization(self.root)
        self.assertEqual(validate_governance(self.root), [])
        resolved, diagnostics = resolve_workflow(self.root, "domain-clarification")
        self.assertEqual(diagnostics, [])
        assert resolved is not None
        self.assertEqual(resolved["customization"], "custom")
        self.assertEqual(hashlib.sha256(wrapper.read_bytes()).hexdigest(), before)
        self.assertIn("Local output rule.", diff_governance(self.root, ROOT))

    def test_materialized_rules_do_not_read_changed_source_template(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            source = Path(raw) / "framework"
            source.mkdir()
            for name in ("dset", "skills"):
                source_path = ROOT / name
                target_path = source / name
                shutil.copytree(source_path, target_path)
            target = Path(raw) / "materialized-adopter"
            create_adopter(source, target)
            template = (
                source
                / "dset"
                / "templates"
                / "governance"
                / "core-v1"
                / "domain-spec-authoring.md"
            )
            template.write_text("# Replaced source template\n", encoding="utf-8")
            resolved, diagnostics = resolve_workflow(target, "domain-clarification")
            self.assertEqual(diagnostics, [])
            assert resolved is not None
            local_rule = next(
                item
                for item in cast(list[dict[str, Any]], resolved["rules"])
                if item["id"] == "DSET-RULE-DOMAIN-SPEC"
            )
            local = target / str(local_rule["path"])
            self.assertIn("Establish ubiquitous language", local.read_text())
            self.assertNotIn("Replaced source template", local.read_text())

    def test_generated_wrappers_match_canonical_sources(self) -> None:
        registry = cast(dict[str, Any], load(self.root / "dset" / "governance.yaml"))
        for wrapper in cast(list[dict[str, Any]], registry["wrappers"]):
            with self.subTest(workflow=wrapper["workflow"]):
                generated = self.root / str(wrapper["path"])
                canonical = ROOT / str(wrapper["path"])
                self.assertEqual(generated.read_bytes(), canonical.read_bytes())
                self.assertEqual(
                    wrapper["sha256"],
                    hashlib.sha256(canonical.read_bytes()).hexdigest(),
                )

    def test_justified_unselected_non_applicability_is_valid(self) -> None:
        path, registry = self._registry(self.root)
        rule = registry["rules"][-1]
        rule["applicability"] = "not-applicable"
        rule["reason"] = "prototype workflow is not selected in this fixture"
        registry["workflows"] = [
            workflow
            for workflow in registry["workflows"]
            if workflow["id"] != "prototyping"
        ]
        registry["wrappers"] = [
            wrapper
            for wrapper in registry["wrappers"]
            if wrapper["workflow"] != "prototyping"
        ]
        path.write_text(dump(registry), encoding="utf-8")
        self.assertEqual(validate_governance(self.root), [])

    def test_materialization_refuses_existing_destination(self) -> None:
        with self.assertRaises(FileExistsError):
            materialize_governance(ROOT, self.root)

    def test_version_semantics_remain_independent(self) -> None:
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = main(["version", str(ROOT)])
        self.assertEqual(result, 0)
        output = stream.getvalue()
        self.assertIn("framework milestone: 0.2", output)
        self.assertIn("python package: 1.0.0 (independent)", output)
        self.assertIn("schemas: 1.0 (independent)", output)

    def test_wrappers_are_thin_and_registered(self) -> None:
        workflows = {
            "domain-clarification": "dset-clarify",
            "diagnosis": "dset-diagnose",
            "prototyping": "dset-prototype",
        }
        for workflow, skill in workflows.items():
            with self.subTest(workflow=workflow):
                path = ROOT / "skills" / skill / "SKILL.md"
                text = path.read_text(encoding="utf-8")
                self.assertLessEqual(len(text.splitlines()), 24)
                self.assertIn(f"rules resolve {workflow}", text)
                self.assertNotIn("## Workflow", text)
                self.assertNotIn("git bisect", text)
                self.assertNotIn("proofs/<candidate>-fit", text)

    def test_manifest_and_template_boundaries_are_stable(self) -> None:
        with self.assertRaises(DsetCommandError) as captured:
            materialize_governance(ROOT, self.root, "missing-profile")
        self.assertEqual(captured.exception.code, "DSET-E140")
        (self.root / "dset" / "dset.yaml").unlink()
        self.assertEqual(validate_repository(self.root)[0].code, "DSET-E001")

    @staticmethod
    def _registry(root: Path) -> tuple[Path, dict[str, Any]]:
        path = root / "dset" / "governance.yaml"
        return path, cast(dict[str, Any], load(path))

    @classmethod
    def _write_registry(cls, root: Path, data: dict[str, Any]) -> None:
        path, _ = cls._registry(root)
        path.write_text(dump(data), encoding="utf-8")

    @staticmethod
    def _remove_registry(root: Path) -> None:
        (root / "dset" / "governance.yaml").unlink()

    @classmethod
    def _missing_owner(cls, root: Path) -> None:
        _, data = cls._registry(root)
        del data["rules"][0]["owner"]
        cls._write_registry(root, data)

    @classmethod
    def _duplicate_owner(cls, root: Path) -> None:
        _, data = cls._registry(root)
        data["rules"].append(dict(data["rules"][0]))
        cls._write_registry(root, data)

    @classmethod
    def _missing_document(cls, root: Path) -> None:
        _, data = cls._registry(root)
        data["rules"][0]["path"] = "dset/governance/missing.md"
        cls._write_registry(root, data)

    @classmethod
    def _outside_root(cls, root: Path) -> None:
        _, data = cls._registry(root)
        data["rules"][0]["path"] = "../outside.md"
        cls._write_registry(root, data)

    @classmethod
    def _dependency_cycle(cls, root: Path) -> None:
        _, data = cls._registry(root)
        first = data["rules"][0]
        second = data["rules"][1]
        first["depends_on"] = [second["id"]]
        second["depends_on"] = [first["id"]]
        cls._write_registry(root, data)

    @classmethod
    def _incompatible_profile(cls, root: Path) -> None:
        _, data = cls._registry(root)
        data["profile"]["id"] = "other-profile"
        cls._write_registry(root, data)

    @classmethod
    def _wrapper_mismatch(cls, root: Path) -> None:
        _, data = cls._registry(root)
        data["wrappers"][0]["sha256"] = "0" * 64
        cls._write_registry(root, data)


if __name__ == "__main__":
    unittest.main()
