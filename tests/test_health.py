from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from dset_toolchain.adopter import create_adopter
from dset_toolchain.health import (
    _ordered_source_entries,
    _qa_ids,
    build_health_model,
    health_is_fresh,
    health_path,
    render_health,
    write_health,
)
from dset_toolchain.layout import discover_layout
from dset_toolchain.yaml_subset import dump, load

ROOT = Path(__file__).resolve().parents[1]


class ProjectHealthTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT.parent)
        self.root = create_adopter(ROOT, Path(self.temporary.name) / "adopter")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_markdown_is_stable_and_exposes_every_denominator_field(self) -> None:
        first = render_health(self.root)
        second = render_health(self.root)

        self.assertEqual(first, second)
        header = "| Numerator | Denominator | Excluded | N/A | Unknown | Stale |"
        self.assertIn(header, first)
        self.assertIn("This generated view is not authority", first)
        self.assertIn("## Semantic inventory", first)
        self.assertIn("Compatibility-classified legacy IDs", first)
        self.assertIn("## Typed relation inventory", first)
        self.assertIn("## Canonical return paths", first)

    def test_explicit_refresh_and_staleness_check(self) -> None:
        path = write_health(self.root)

        self.assertEqual(path, health_path(self.root))
        self.assertTrue(health_is_fresh(self.root))

        spec = self.root / "dset/specs/packages/sample/spec.md"
        spec.write_text(
            spec.read_text(encoding="utf-8") + "\nChanged authority.\n",
            encoding="utf-8",
        )
        self.assertFalse(health_is_fresh(self.root))
        self.assertEqual(write_health(self.root), path)
        self.assertTrue(health_is_fresh(self.root))

    def test_source_digest_uses_case_sensitive_posix_path_order(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            root = Path(raw)
            (root / "a.txt").write_text("lower\n", encoding="utf-8")
            (root / "Z.txt").write_text("upper\n", encoding="utf-8")

            ordered = [relative for relative, _ in _ordered_source_entries(root)]

        self.assertEqual(ordered, ["Z.txt", "a.txt"])

    def test_model_has_repository_drill_downs_and_honest_coverage(self) -> None:
        model = build_health_model(self.root)

        self.assertIn("sample", model["packages"])
        self.assertEqual(len(model["coverage"]), 4)
        semantic_types = set(model["semantic_counts"]["by_type"])
        self.assertTrue(
            semantic_types.issubset({"decision", "problem", "qa", "question"})
        )
        self.assertIn("decision", semantic_types)
        self.assertIn("qa", semantic_types)
        self.assertGreater(model["semantic_counts"]["compatibility"], 0)
        self.assertEqual(
            model["semantic_counts"]["native_atoms"]
            + model["semantic_counts"]["compatibility"],
            model["semantic_counts"]["total"],
        )
        repository = build_health_model(ROOT)
        relation_types = set(repository["relation_counts"]["by_type"])
        self.assertIn("implementation_of", relation_types)
        self.assertIn("projection_of", relation_types)
        self.assertGreater(repository["relation_counts"]["total"], 0)
        for coverage in model["coverage"]:
            self.assertGreaterEqual(coverage.denominator, 0)
            self.assertGreaterEqual(coverage.unknown, 0)
            self.assertGreaterEqual(coverage.stale, 0)

    def test_prose_mentions_do_not_create_coverage(self) -> None:
        package_root = self.root / "dset/specs/packages/sample"
        manifest = discover_layout(self.root).structured_file(
            package_root, "package.toml"
        )
        data = load(manifest)
        assert isinstance(data, dict)
        requirements = data["requirements"]
        tests = data["tests"]
        assert isinstance(requirements, list)
        assert isinstance(tests, list)
        requirements.append("DSET-REQUIREMENT-999")
        tests.append("DSET-TEST-999")
        manifest.write_text(dump(data, manifest), encoding="utf-8")

        spec = self.root / "dset/specs/packages/sample/spec.md"
        spec.write_text(
            spec.read_text(encoding="utf-8")
            + "\nLoose reference to DSET-REQUIREMENT-999.\n",
            encoding="utf-8",
        )
        test_plan = self.root / "dset/specs/packages/sample/test-plan.md"
        test_plan.write_text(
            test_plan.read_text(encoding="utf-8")
            + "\nDSET-TEST-999 mentions DSET-REQUIREMENT-999.\n",
            encoding="utf-8",
        )
        proofs = self.root / "dset/changes/sample/proofs"
        proofs.mkdir(parents=True, exist_ok=True)
        (proofs / "mention.md").write_text(
            "DSET-TEST-999 is mentioned without an evidence_for relation.\n",
            encoding="utf-8",
        )

        coverage = {
            item.name: item for item in build_health_model(self.root)["coverage"]
        }

        compiled = coverage["Decision authority compiled into evergreen truth"]
        checked = coverage["Applicable authority connected to Test or Evaluation"]
        evidenced = coverage["QA definitions connected to current evidence"]
        self.assertIn("DSET-REQUIREMENT-999", compiled.gaps)
        self.assertIn("DSET-REQUIREMENT-999", checked.gaps)
        self.assertIn("DSET-TEST-999", evidenced.gaps)

    def test_inactive_qa_is_excluded_from_current_evidence_coverage(self) -> None:
        identifier = "DSET-TEST-998"
        atom = SimpleNamespace(
            semantic_id=identifier,
            semantic_type="qa",
            emission_status="accepted",
        )

        self.assertIn(identifier, _qa_ids(self.root, {identifier: atom}, []))
        self.assertNotIn(
            identifier,
            _qa_ids(
                self.root,
                {identifier: atom},
                [{"atom_id": identifier, "event": "absorbed"}],
            ),
        )

    def test_version_roles_are_derived_from_direct_subtypes(self) -> None:
        before = build_health_model(self.root)["artifact_counts"]["by_role"]
        folder = self.root / "dset/version-role-fixtures"
        folder.mkdir(parents=True)
        subtypes = (
            "roadmap",
            "version_scope",
            "release_plan",
            "change",
            "readiness_record",
            "release_record",
        )
        for sequence, subtype in enumerate(subtypes, start=900):
            (folder / f"DSET-VERSION-{sequence}.md").write_text(
                "+++\n"
                'artifact_type = "version"\n'
                f'artifact_subtype = "{subtype}"\n'
                f'artifact_id = "DSET-VERSION-{sequence}"\n'
                'priority = "medium"\n'
                "llm_session_ids = []\n"
                "+++\n",
                encoding="utf-8",
            )

        after = build_health_model(self.root)["artifact_counts"]["by_role"]

        self.assertEqual(after["evergreen"] - before.get("evergreen", 0), 3)
        self.assertEqual(after["transactional"] - before.get("transactional", 0), 3)
        self.assertEqual(
            after.get("derived_or_navigation", 0),
            before.get("derived_or_navigation", 0),
        )


if __name__ == "__main__":
    unittest.main()
