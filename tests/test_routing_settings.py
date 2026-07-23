"""Verify project-local selection of the canonical routing vocabulary."""

from __future__ import annotations

import unittest
from pathlib import Path

from dset_toolchain.artifact_routing import (
    CONTENT_ROLES,
    GOVERNANCE_ORIGINS,
    RELATION_SHAPES,
    REVISION_MODES,
)
from dset_toolchain.settings import SETTINGS_FILENAME, load_project_settings
from dset_toolchain.temp_paths import temporary_directory


class RoutingSettingsTests(unittest.TestCase):
    """Verify current settings select the complete route contract."""

    def _write(self, root: Path, routing: str) -> None:
        settings = root / ".dset" / SETTINGS_FILENAME
        settings.parent.mkdir()
        settings.write_text(
            "\n".join(
                (
                    'schema_version = "1.5"',
                    "",
                    "[artifacts]",
                    'creation_strictness = "medium"',
                    "",
                    "[routing]",
                    routing,
                    'content_roles = ["inquiry", "definition", "rationale", '
                    '"method", "implementation", "observation"]',
                    'governance_origins = ["internal", "external"]',
                    'relation_shapes = ["standalone", "relational"]',
                    "",
                )
            ),
            encoding="utf-8",
        )

    def test_current_settings_select_all_axes_exactly(self) -> None:
        with temporary_directory(prefix="dset-routing-settings-") as raw:
            root = Path(raw)
            self._write(
                root,
                'revision_modes = ["atomic", "evergreen", "maintained"]',
            )
            settings, issues = load_project_settings(root)

        self.assertEqual(issues, ())
        self.assertEqual(settings.routing_revision_modes, REVISION_MODES)
        self.assertEqual(settings.routing_content_roles, CONTENT_ROLES)
        self.assertEqual(settings.routing_governance_origins, GOVERNANCE_ORIGINS)
        self.assertEqual(settings.routing_relation_shapes, RELATION_SHAPES)
        self.assertFalse(settings.artifact_subtype_in_names)

    def test_alias_or_partial_axis_fails_closed(self) -> None:
        with temporary_directory(prefix="dset-routing-settings-") as raw:
            root = Path(raw)
            self._write(root, 'revision_modes = ["atomic", "living"]')
            settings, issues = load_project_settings(root)

        self.assertEqual(settings.routing_revision_modes, REVISION_MODES)
        self.assertIn(
            "routing.revision_modes must be: atomic, evergreen, maintained",
            issues,
        )


if __name__ == "__main__":
    unittest.main()
