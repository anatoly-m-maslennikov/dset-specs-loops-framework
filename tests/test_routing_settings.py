"""Verify project-local selection of the canonical routing vocabulary."""

from __future__ import annotations

import unittest
from pathlib import Path

from dset_toolchain.artifact_routing import (
    CONTENT_ROLES,
    GOVERNANCE_LOCI,
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
                    'schema_version = "1.8"',
                    "",
                    "[artifacts]",
                    'creation_strictness = "medium"',
                    'enabled_types = ["requirement"]',
                    "enabled_subtypes = []",
                    "",
                    "[artifacts.routing]",
                    routing,
                    'content_roles = ["inquiry", "analysis", "definition", '
                    '"method", "implementation", "observation"]',
                    'governance_loci = ["internal", "external", "relation"]',
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
                'revision_modes = ["atomic", "append_only", "maintained"]',
            )
            settings, issues = load_project_settings(root)

        self.assertEqual(issues, ())
        self.assertEqual(settings.routing_revision_modes, REVISION_MODES)
        self.assertEqual(settings.routing_content_roles, CONTENT_ROLES)
        self.assertEqual(settings.routing_governance_loci, GOVERNANCE_LOCI)
        self.assertFalse(settings.artifact_subtype_in_names)

    def test_alias_or_partial_axis_fails_closed(self) -> None:
        with temporary_directory(prefix="dset-routing-settings-") as raw:
            root = Path(raw)
            self._write(root, 'revision_modes = ["atomic", "living"]')
            settings, issues = load_project_settings(root)

        self.assertEqual(settings.routing_revision_modes, REVISION_MODES)
        self.assertIn(
            "artifacts.routing.revision_modes must be an ordered unique subset "
            "of: atomic, append_only, maintained",
            issues,
        )


if __name__ == "__main__":
    unittest.main()
