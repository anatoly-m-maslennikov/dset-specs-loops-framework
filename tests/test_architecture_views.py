"""Verify DSET architecture views behavior.

Assurance scope: deterministic behavior owned by this module.
Non-obvious fixtures: documented by the fixture that owns them.
Host requirements: an isolated supported Python environment.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from dset_toolchain.frontmatter import metadata as frontmatter_metadata
from dset_toolchain.layout import LAYER_DIRECTORIES
from tests import repository_root

# ROOT locates the repository fixture; repository layout is authoritative.
ROOT = repository_root(Path(__file__))


class ArchitectureViewTests(unittest.TestCase):
    def test_project_hub_maps_enabled_layers(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("## Project architecture map", content)
        self.assertIn("```mermaid", content)
        for layer in ("META", "GOV", "TOOL", "SKILL", "OPS"):
            self.assertIn(f'{layer}["{layer}', content)
        for edge in (
            "META --> GOV",
            "GOV --> TOOL",
            "TOOL --> SKILL",
            "SKILL --> OPS",
        ):
            self.assertIn(edge, content)

    def test_features_are_horizontal_and_layers_are_forward_only(self) -> None:
        live = ROOT / ".dset/02_layer_gov/specification-architecture.md"
        template = (
            ROOT / ".dset/02_layer_gov/templates/governance/core-v1/architecture.md"
        )
        content = live.read_text(encoding="utf-8")
        self.assertEqual(content, template.read_text(encoding="utf-8"))
        for phrase in (
            "Features are peer capabilities",
            "interactions are horizontal",
            "`META → GOV → TOOL → SKILL → OPS`",
            "immediately following layer is preferred",
            "same or an earlier layer",
            "or a later layer",
            "Backward authority fails validation",
        ):
            self.assertIn(phrase, content)

    def test_every_layer_hub_maps_its_main_functions(self) -> None:
        expected = {
            "meta": ("Project and version identity", "Evaluation definitions"),
            "gov": ("Governance and artifact registries", "Traceability"),
            "tool": ("CLI and runtime bridge", "self-hosting"),
            "skill": ("Thin host wrappers", "Delegation and budget policy"),
            "ops": ("Release lifecycle", "Supportability and investigation"),
        }
        for layer, phrases in expected.items():
            with self.subTest(layer=layer):
                content = (
                    ROOT / ".dset" / LAYER_DIRECTORIES[layer] / "README.md"
                ).read_text(encoding="utf-8")
                self.assertIn("## Layer map", content)
                self.assertIn("```mermaid", content)
                for phrase in phrases:
                    self.assertIn(phrase, content)

    def test_templates_cover_only_enabled_structural_levels(self) -> None:
        root = ROOT / ".dset/02_layer_gov/templates/architecture-view"
        expected = {"project.md", "feature-group.md", "feature-or-layer.md"}
        self.assertEqual(
            {path.name for path in root.glob("*.md") if path.name != "README.md"},
            expected,
        )
        for name in expected:
            with self.subTest(name=name):
                path = root / name
                content = path.read_text(encoding="utf-8")
                metadata = frontmatter_metadata(path)
                assert metadata is not None
                self.assertEqual(metadata["artifact_type"], "specification")
                self.assertEqual(metadata["artifact_subtype"], "architecture")
                self.assertIn("```mermaid", content)

    def test_governance_requires_one_level_down_without_placeholders(self) -> None:
        live = ROOT / ".dset/02_layer_gov/specification-architecture.md"
        template = (
            ROOT / ".dset/02_layer_gov/templates/governance/core-v1/architecture.md"
        )
        content = live.read_text(encoding="utf-8")
        self.assertEqual(content, template.read_text(encoding="utf-8"))
        self.assertIn("feature groups when present", content)
        self.assertIn("does not\ncreate empty diagrams", content)
        self.assertIn("Each view stays one level deep", content)

    def test_global_truth_owns_only_cross_child_concerns(self) -> None:
        live = ROOT / ".dset/02_layer_gov/specification-architecture.md"
        template = (
            ROOT / ".dset/02_layer_gov/templates/governance/core-v1/architecture.md"
        )
        content = live.read_text(encoding="utf-8")
        self.assertEqual(content, template.read_text(encoding="utf-8"))
        for phrase in (
            "narrowest common structural",
            "Abstract, important, or reusable does",
            "cross-child Contracts and dependency rules",
            "end-to-end Tests and Evaluations",
            "never duplicate it as parallel truth",
        ):
            self.assertIn(phrase, content)

        root = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Project-level truth owns only concerns", root)
        self.assertIn("narrowest common structural owner", root)

    def test_artifact_relations_are_typed_and_forward_only(self) -> None:
        live = ROOT / ".dset/02_layer_gov/specification-architecture.md"
        template = (
            ROOT / ".dset/02_layer_gov/templates/governance/core-v1/architecture.md"
        )
        content = live.read_text(encoding="utf-8")
        self.assertEqual(content, template.read_text(encoding="utf-8"))
        for phrase in (
            "`child_of`, `analysis_of`, `projection_of`, `implementation_of`",
            "`check_of`, `evidence_for`, `resolution_of`, `override_of`",
            "`replacement_of`, or `relates_to`",
            "Reverse edges are derived and never",
            "One source-target pair has one primary relation",
            "one semantic Type, one exact",
            "Historical sealed `child_of` remains readable compatibility input",
        ):
            self.assertIn(phrase, content)


if __name__ == "__main__":
    unittest.main()
