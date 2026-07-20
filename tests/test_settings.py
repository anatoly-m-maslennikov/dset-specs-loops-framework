from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from dset_toolchain.settings import (
    DEFAULT_PRIORITY_SCALE,
    SETTINGS_SCHEMA_VERSION,
    load_project_settings,
)
from dset_toolchain.toml_codec import loads as load_toml

ROOT = Path(__file__).resolve().parents[1]


class ProjectSettingsTests(unittest.TestCase):
    def test_emitted_settings_are_documented_1_1_defaults(self) -> None:
        root_text = (ROOT / "dset.toml").read_text(encoding="utf-8")
        template_text = (
            ROOT / "dset/scopes/meta/templates/dset.toml"
        ).read_text(encoding="utf-8")
        self.assertEqual(root_text, template_text)
        for setting in (
            "schema_version",
            "subtype_in_names",
            "creation_strictness",
            "mode",
            "scale",
            "default",
        ):
            self.assertIn("#", root_text.split(setting, 1)[0])
        parsed = load_toml(root_text)
        self.assertEqual(parsed["schema_version"], SETTINGS_SCHEMA_VERSION)
        self.assertEqual(parsed["artifacts"]["subtype_in_names"], False)
        self.assertEqual(parsed["artifacts"]["creation_strictness"], "medium")
        self.assertEqual(parsed["workflows"]["implement"]["mode"], "lazy")
        self.assertEqual(parsed["priority"]["scale"], list(DEFAULT_PRIORITY_SCALE))
        self.assertEqual(parsed["priority"]["default"], "medium")

    def test_legacy_1_0_names_remain_read_compatible(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            root = Path(raw)
            (root / "dset.toml").write_text(
                "\n".join(
                    (
                        'schema_version = "1.0"',
                        "",
                        "[optional_capabilities]",
                        "artifact_subtype_in_names = true",
                        'artifact_creation_strictness = "high"',
                        "",
                        "[priority]",
                        'scale = "urgent,normal,later"',
                        'default = "normal"',
                        "",
                    )
                ),
                encoding="utf-8",
            )
            settings, issues = load_project_settings(root)
        self.assertEqual(issues, ())
        self.assertEqual(settings.schema_version, "1.0")
        self.assertTrue(settings.artifact_subtype_in_names)
        self.assertEqual(settings.artifact_creation_strictness, "high")
        self.assertEqual(settings.implementation_mode, "lazy")
        self.assertEqual(settings.priority_scale, ("urgent", "normal", "later"))

    def test_invalid_schema_or_implementation_mode_stops_deterministically(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            root = Path(raw)
            path = root / "dset.toml"
            path.write_text(
                "\n".join(
                    (
                        'schema_version = "9.9"',
                        "[workflows.implement]",
                        'mode = "automatic"',
                        "",
                    )
                ),
                encoding="utf-8",
            )
            _settings, issues = load_project_settings(root)
        self.assertEqual(
            issues,
            (
                "settings schema_version must be 1.0 or 1.1",
                "workflows.implement.mode must be lazy or strict",
            ),
        )


if __name__ == "__main__":
    unittest.main()
