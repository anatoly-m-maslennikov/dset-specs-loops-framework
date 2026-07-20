from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from dset_toolchain.adopter import create_adopter
from dset_toolchain.health import (
    build_health_model,
    health_is_fresh,
    health_path,
    render_health,
    write_health,
)

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

    def test_model_has_repository_drill_downs_and_honest_coverage(self) -> None:
        model = build_health_model(self.root)

        self.assertIn("sample", model["packages"])
        self.assertEqual(len(model["coverage"]), 4)
        for coverage in model["coverage"]:
            self.assertGreaterEqual(coverage.denominator, 0)
            self.assertGreaterEqual(coverage.unknown, 0)
            self.assertGreaterEqual(coverage.stale, 0)


if __name__ == "__main__":
    unittest.main()
