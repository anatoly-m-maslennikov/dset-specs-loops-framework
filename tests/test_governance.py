from __future__ import annotations

import contextlib
import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from typing import Any, cast

from dset_toolchain.adopter import create_adopter
from dset_toolchain.cli import main
from dset_toolchain.governance import (
    diff_governance,
    find_repository,
    materialize_governance,
    refresh_customization,
    resolve_workflow,
    validate_governance,
)
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
        resolved, diagnostics = resolve_workflow(self.root, "domain-grilling")
        self.assertEqual(diagnostics, [])
        self.assertIsNotNone(resolved)
        assert resolved is not None
        self.assertEqual(resolved["workflow_id"], "domain-grilling")
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
                    "domain-grilling",
                    str(self.root),
                    "--format",
                    "json",
                ]
            )
        self.assertEqual(result, 0)
        output = stream.getvalue()
        self.assertIn('"workflow_id": "domain-grilling"', output)
        self.assertIn('"customization": "unmodified"', output)

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

    def test_customization_changes_rules_not_wrapper(self) -> None:
        wrapper = self.root / "skills" / "dset-grill" / "SKILL.md"
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
        resolved, diagnostics = resolve_workflow(self.root, "domain-grilling")
        self.assertEqual(diagnostics, [])
        assert resolved is not None
        self.assertEqual(resolved["customization"], "custom")
        self.assertEqual(hashlib.sha256(wrapper.read_bytes()).hexdigest(), before)
        self.assertIn("Local output rule.", diff_governance(self.root, ROOT))

    def test_materialization_refuses_existing_destination(self) -> None:
        with self.assertRaises(FileExistsError):
            materialize_governance(ROOT, self.root)

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
