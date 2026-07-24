"""Verify optional governance-surface configuration.

Assurance scope: state parsing, previews, comment-preserving writes, and
bounded recommendations.
Host requirements: an isolated supported Python environment.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from dset_toolchain.configuration import (
    execute_surface_change,
    plan_surface_change,
    surface_recommendations,
    surface_states,
)
from dset_toolchain.settings import load_project_settings
from dset_toolchain.temp_paths import temporary_directory


class GovernanceSurfaceTests(unittest.TestCase):
    """Verify deterministic progressive-governance behavior."""

    def test_missing_surface_table_defaults_every_surface_to_inactive(self) -> None:
        with temporary_directory() as raw:
            root = self._root(Path(raw))
            states = surface_states(root)
        self.assertTrue(states)
        self.assertFalse(any(states.values()))

    def test_execute_materializes_defaults_and_preserves_existing_text(self) -> None:
        with temporary_directory() as raw:
            root = self._root(Path(raw))
            path = root / ".dset" / "dset_settings.toml"
            original = path.read_text(encoding="utf-8")
            change = plan_surface_change(
                root,
                "project-overview",
                active=True,
            )
            execute_surface_change(change)
            updated = path.read_text(encoding="utf-8")
            settings, issues = load_project_settings(root)
        self.assertTrue(updated.startswith(original))
        self.assertIn("# retained operator comment", updated)
        self.assertIn("project_overview = true", updated)
        self.assertEqual(issues, ())
        self.assertEqual(settings.active_governance_surfaces, ("project_overview",))

    def test_existing_table_update_preserves_comments_and_peer_states(self) -> None:
        with temporary_directory() as raw:
            root = self._root(Path(raw), with_surfaces=True)
            path = root / ".dset" / "dset_settings.toml"
            change = plan_surface_change(
                root,
                "architecture-view",
                active=True,
            )
            execute_surface_change(change)
            updated = path.read_text(encoding="utf-8")
            states = surface_states(root)
        self.assertIn("project_overview = true # retained state", updated)
        self.assertTrue(states["project-overview"])
        self.assertTrue(states["architecture-view"])
        self.assertFalse(states["test-plan"])

    def test_recommendation_ignores_external_methodology_carriers(self) -> None:
        with temporary_directory() as raw:
            root = self._root(Path(raw))
            external = root / ".dset" / "000_dset_methodology"
            external.mkdir()
            (external / "architecture.md").write_text("external", encoding="utf-8")
            self.assertEqual(surface_recommendations(root), ())
            internal = root / ".dset" / "101_layer_meta"
            internal.mkdir()
            (internal / "architecture.md").write_text("internal", encoding="utf-8")
            recommendations = surface_recommendations(root)
        self.assertEqual(recommendations[0]["surface"], "architecture-view")

    @staticmethod
    def _root(path: Path, *, with_surfaces: bool = False) -> Path:
        root = path.resolve()
        control = root / ".dset"
        control.mkdir()
        lines = [
            'schema_version = "1.5"',
            "# retained operator comment",
            "",
        ]
        if with_surfaces:
            lines.extend(
                (
                    "[governance_surfaces]",
                    "evergreen_specification = false",
                    "test_plan = false",
                    "evaluation_plan = false",
                    "implementation_plan = false",
                    "project_overview = true # retained state",
                    "architecture_view = false",
                    "",
                )
            )
        (control / "dset_settings.toml").write_text(
            "\n".join(lines),
            encoding="utf-8",
        )
        return root


if __name__ == "__main__":
    unittest.main()
