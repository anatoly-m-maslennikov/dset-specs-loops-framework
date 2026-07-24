"""Verify DSET profiles behavior.

Assurance scope: deterministic behavior owned by this module.
Non-obvious fixtures: documented by the fixture that owns them.
Host requirements: an isolated supported Python environment.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from dset_toolchain.profiles import required_artifacts
from tests import repository_root

# ROOT locates the repository fixture; repository layout is authoritative.
ROOT = repository_root(Path(__file__))


class ProfileTests(unittest.TestCase):
    """Verify profile behavior."""

    def test_standard_has_eight_documents(self) -> None:
        files, directories = required_artifacts(ROOT, "standard")
        documents = {item for item in files if item.endswith(".md")}
        self.assertEqual(len(documents), 8)
        self.assertEqual(directories, {"specs", "proofs"})

    def test_profiles_add_only_their_supplements(self) -> None:
        large_files, _ = required_artifacts(ROOT, "large")
        defect_files, _ = required_artifacts(ROOT, "defect")
        adoption_files, adoption_dirs = required_artifacts(ROOT, "adoption")
        self.assertIn("global-impact.md", large_files)
        self.assertIn("dependency-map.toml", large_files)
        self.assertIn("root-cause.md", defect_files)
        self.assertIn("adoption-decision.md", adoption_files)
        adoption_template = (
            ROOT / ".dset/02_layer_gov/templates/change/adoption-decision.md"
        ).read_text(encoding="utf-8")
        self.assertIn("(decision.md)", adoption_template)
        self.assertIn("proofs/candidate-fit", adoption_dirs)


if __name__ == "__main__":
    unittest.main()
