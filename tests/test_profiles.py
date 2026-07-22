from __future__ import annotations

import unittest
from pathlib import Path

from dset_toolchain.profiles import required_artifacts

ROOT = Path(__file__).resolve().parents[1]


class ProfileTests(unittest.TestCase):
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
            ROOT / ".dset/gov/templates/change/adoption-decision.md"
        ).read_text(encoding="utf-8")
        self.assertIn("(decision.md)", adoption_template)
        self.assertIn("proofs/candidate-fit", adoption_dirs)


if __name__ == "__main__":
    unittest.main()
