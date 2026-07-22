"""Verify DSET compilation behavior.

Assurance scope: deterministic behavior owned by this module.
Non-obvious fixtures: documented by the fixture that owns them.
Host requirements: an isolated supported Python environment.
"""

from __future__ import annotations

import shutil
import unittest
from pathlib import Path

from dset_toolchain.compilation import (
    _projection_fragments,
    active_authority_ids,
    build_compilation_index,
    compilation_is_fresh,
    compilation_path,
    write_compilation,
)
from dset_toolchain.temp_paths import temporary_directory
from tests import repository_root

# ROOT locates the repository fixture; repository layout is authoritative.
ROOT = repository_root(Path(__file__))


class CompilationTests(unittest.TestCase):
    def test_loose_id_mentions_are_not_compiled_claim_fragments(self) -> None:
        with temporary_directory() as raw:
            path = (Path(raw) / "spec.md").resolve()
            path.write_text(
                "A loose mention of DSET-REQUIREMENT-GOV-035 is not a claim.\n",
                encoding="utf-8",
            )
            self.assertEqual(
                _projection_fragments(path, "DSET-REQUIREMENT-GOV-035"), []
            )
            path.write_text(
                "## DSET-REQUIREMENT-GOV-035 — Explicit claim\n\n"
                "The governed consequence is stated here.\n",
                encoding="utf-8",
            )
            fragments = _projection_fragments(path, "DSET-REQUIREMENT-GOV-035")
            self.assertEqual(fragments[0]["kind"], "section")
            self.assertTrue(fragments[0]["sha256"])

    def test_every_active_authority_has_a_digest_bound_projection(self) -> None:
        model = build_compilation_index(ROOT)
        records = {item["id"]: item for item in model["records"]}
        self.assertEqual(set(records), active_authority_ids(ROOT))
        self.assertIn("DSET-DECISION-GOV-008", records)
        self.assertNotIn("DSET-DECISION-GOV-007", records)
        self.assertTrue(all(item["source"]["sha256"] for item in records.values()))
        self.assertTrue(all(item["projections"] for item in records.values()))

    def test_projection_change_makes_explicit_compilation_stale(self) -> None:
        with temporary_directory() as raw:
            root = Path(raw).resolve()
            shutil.copytree(ROOT / ".dset", root / ".dset")
            write_compilation(root)
            self.assertTrue(compilation_is_fresh(root))
            spec = root / ".dset/02_layer_gov/specification-methodology.md"
            spec.write_text(spec.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            self.assertFalse(compilation_is_fresh(root))
            write_compilation(root)
            self.assertTrue(compilation_is_fresh(root))
            self.assertTrue(compilation_path(root).is_file())


if __name__ == "__main__":
    unittest.main()
