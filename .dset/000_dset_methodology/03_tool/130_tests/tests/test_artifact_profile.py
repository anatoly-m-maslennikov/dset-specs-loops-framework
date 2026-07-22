from __future__ import annotations

import copy
import unittest
from pathlib import Path
from typing import Any

from dset_toolchain.diagnostics import Diagnostic
from dset_toolchain.temp_paths import temporary_directory
from dset_toolchain.validation import validate_artifact_registry


class ArtifactProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = temporary_directory()
        self.root = Path(self.temporary.name).resolve()
        (self.root / "dset").mkdir()
        (self.root / "docs").mkdir()
        (self.root / "methodology").mkdir()
        self._write_root_hub(include_methodology=True)
        self._write_area_hub(self.root / "docs" / "README.md")
        self._write_area_hub(self.root / "methodology" / "README.md")
        self.registry_path = self.root / "dset" / "artifacts.yaml"
        self.registry_path.write_text("profile: documentation-v1\n", encoding="utf-8")
        self.registry = self._registry()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_valid_registry_passes(self) -> None:
        self.assertEqual(self._validate(self.registry), [])

    def test_missing_hub_is_rejected(self) -> None:
        data = copy.deepcopy(self.registry)
        data["areas"][0]["hub"] = "docs/MISSING.md"
        self.assertIn("DSET-E121", self._codes(self._validate(data)))

    def test_duplicate_root_is_rejected(self) -> None:
        data = copy.deepcopy(self.registry)
        data["areas"][1]["root"] = "docs"
        self.assertIn("DSET-E121", self._codes(self._validate(data)))

    def test_missing_parent_is_rejected(self) -> None:
        data = copy.deepcopy(self.registry)
        data["areas"][0]["parent"] = "missing"
        self.assertIn("DSET-E122", self._codes(self._validate(data)))

    def test_parent_cycle_is_rejected(self) -> None:
        data = copy.deepcopy(self.registry)
        data["areas"][0]["parent"] = "methodology"
        data["areas"][1]["parent"] = "docs"
        self.assertIn("DSET-E122", self._codes(self._validate(data)))

    def test_root_must_link_every_top_level_area(self) -> None:
        self._write_root_hub(include_methodology=False)
        self.assertIn("DSET-E123", self._codes(self._validate(self.registry)))

    def test_area_hub_requires_standard_sections(self) -> None:
        path = self.root / "docs" / "README.md"
        path.write_text("# Docs\n\n## Purpose\n\nDocs.\n", encoding="utf-8")
        self.assertIn("DSET-E123", self._codes(self._validate(self.registry)))

    def _validate(self, data: dict[str, Any]) -> list[Diagnostic]:
        return validate_artifact_registry(self.root, self.registry_path, data)

    @staticmethod
    def _codes(diagnostics: list[Diagnostic]) -> set[str]:
        return {item.code for item in diagnostics}

    def _write_root_hub(self, *, include_methodology: bool) -> None:
        links = "[Docs](docs/README.md)\n"
        if include_methodology:
            links += "[Methodology](methodology/README.md)\n"
        content = (
            "# Repository\n\n"
            "## Purpose\n\nRepository.\n\n"
            "## Boundaries\n\nPublic truth.\n\n"
            f"## Repository areas\n\n{links}"
        )
        (self.root / "README.md").write_text(content, encoding="utf-8")

    @staticmethod
    def _write_area_hub(path: Path) -> None:
        path.write_text(
            "# Area\n\n"
            "## Purpose\n\nArea purpose.\n\n"
            "## Boundaries\n\nArea boundary.\n\n"
            "## Start here\n\nRead this.\n",
            encoding="utf-8",
        )

    @staticmethod
    def _registry() -> dict[str, Any]:
        return {
            "schema_version": 1.0,
            "profile": "documentation-v1",
            "root": {
                "id": "repository",
                "root": ".",
                "hub": "README.md",
                "owner": "framework",
                "purpose": "Repository navigation",
            },
            "areas": [
                {
                    "id": "docs",
                    "root": "docs",
                    "hub": "docs/README.md",
                    "parent": "repository",
                    "owner": "docs",
                    "purpose": "Documentation",
                },
                {
                    "id": "methodology",
                    "root": "methodology",
                    "hub": "methodology/README.md",
                    "parent": "repository",
                    "owner": "methodology",
                    "purpose": "Methodology",
                },
            ],
        }


if __name__ == "__main__":
    unittest.main()
