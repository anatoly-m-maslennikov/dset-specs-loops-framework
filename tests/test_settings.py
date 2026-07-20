from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from dset_toolchain.adopter import create_adopter
from dset_toolchain.settings import (
    DEFAULT_PRIORITY_SCALE,
    LEGACY_SETTINGS_FILENAME,
    SETTINGS_FILENAME,
    SETTINGS_SCHEMA_VERSION,
    load_project_settings,
)
from dset_toolchain.toml_codec import loads as load_toml
from dset_toolchain.validation import validate_repository

ROOT = Path(__file__).resolve().parents[1]


class ProjectSettingsTests(unittest.TestCase):
    def test_emitted_settings_are_documented_1_2_defaults(self) -> None:
        root_text = (ROOT / SETTINGS_FILENAME).read_text(encoding="utf-8")
        template_text = (
            ROOT / f"dset/scopes/meta/templates/{SETTINGS_FILENAME}"
        ).read_text(encoding="utf-8")
        self.assertEqual(root_text, template_text)
        for setting in (
            "schema_version",
            "subtype_in_names",
            "creation_strictness",
            "mode",
            "default_workspace",
            "budget_profile",
            "scale",
            "default",
        ):
            self.assertIn("#", root_text.split(setting, 1)[0])
        parsed = load_toml(root_text)
        self.assertEqual(parsed["schema_version"], SETTINGS_SCHEMA_VERSION)
        self.assertEqual(parsed["artifacts"]["subtype_in_names"], False)
        self.assertEqual(parsed["artifacts"]["creation_strictness"], "medium")
        self.assertEqual(parsed["workflows"]["implement"]["mode"], "lazy")
        self.assertEqual(parsed["changes"]["default_workspace"], "integration-branch")
        self.assertEqual(parsed["delegation"]["budget_profile"], "medium")
        self.assertEqual(parsed["priority"]["scale"], list(DEFAULT_PRIORITY_SCALE))
        self.assertEqual(parsed["priority"]["default"], "medium")
        self.assertIn("project manifest", root_text)
        self.assertIn("governing documents", root_text)
        self.assertIn("branch-worktree", root_text)
        self.assertIn("0-1 subagents", root_text)

    def test_legacy_1_0_names_remain_read_compatible(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            root = Path(raw)
            (root / LEGACY_SETTINGS_FILENAME).write_text(
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
        self.assertEqual(settings.change_workspace_mode, "integration-branch")
        self.assertEqual(settings.delegation_budget_profile, "medium")
        self.assertEqual(settings.priority_scale, ("urgent", "normal", "later"))

    def test_previous_1_1_contract_remains_read_compatible(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            root = Path(raw)
            (root / LEGACY_SETTINGS_FILENAME).write_text(
                "\n".join(
                    (
                        'schema_version = "1.1"',
                        "[artifacts]",
                        "subtype_in_names = false",
                        'creation_strictness = "medium"',
                        "[workflows.implement]",
                        'mode = "strict"',
                        "[priority]",
                        'scale = ["now", "later"]',
                        'default = "now"',
                        "",
                    )
                ),
                encoding="utf-8",
            )
            settings, issues = load_project_settings(root)
        self.assertEqual(issues, ())
        self.assertEqual(settings.schema_version, "1.1")
        self.assertEqual(settings.implementation_mode, "strict")
        self.assertEqual(settings.change_workspace_mode, "integration-branch")
        self.assertEqual(settings.delegation_budget_profile, "medium")

    def test_competing_settings_filenames_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            root = Path(raw)
            for name in (SETTINGS_FILENAME, LEGACY_SETTINGS_FILENAME):
                (root / name).write_text('schema_version = "1.2"\n', encoding="utf-8")
            _settings, issues = load_project_settings(root)
        self.assertEqual(
            issues,
            ("dset_settings.toml and legacy dset.toml cannot coexist",),
        )

    def test_repository_validation_reports_competing_names_at_canonical_path(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            root = create_adopter(ROOT, Path(raw) / "adopter")
            (root / LEGACY_SETTINGS_FILENAME).write_text(
                'schema_version = "1.1"\n', encoding="utf-8"
            )
            diagnostics = validate_repository(root)
        conflict = [item for item in diagnostics if item.code == "DSET-E157"]
        self.assertEqual(len(conflict), 1)
        self.assertEqual(conflict[0].path, root / SETTINGS_FILENAME)
        self.assertIn("cannot coexist", conflict[0].message)

    def test_invalid_schema_or_implementation_mode_stops_deterministically(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            root = Path(raw)
            path = root / SETTINGS_FILENAME
            path.write_text(
                "\n".join(
                    (
                        'schema_version = "9.9"',
                        "[workflows.implement]",
                        'mode = "automatic"',
                        "[unexpected]",
                        "enabled = true",
                        "",
                    )
                ),
                encoding="utf-8",
            )
            _settings, issues = load_project_settings(root)
        self.assertEqual(
            issues,
            (
                "settings schema_version must be 1.0, 1.1, or 1.2",
                "settings has unknown setting: unexpected",
                "workflows.implement.mode must be lazy or strict",
            ),
        )

    def test_invalid_new_behavior_values_name_the_owning_keys(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            root = Path(raw)
            (root / SETTINGS_FILENAME).write_text(
                "\n".join(
                    (
                        'schema_version = "1.2"',
                        "[changes]",
                        'default_workspace = "shared"',
                        "[delegation]",
                        'budget_profile = "unlimited"',
                        "",
                    )
                ),
                encoding="utf-8",
            )
            _settings, issues = load_project_settings(root)
        self.assertIn(
            "changes.default_workspace must be integration-branch or branch-worktree",
            issues,
        )
        self.assertIn(
            "delegation.budget_profile must be low, medium, or high",
            issues,
        )

    def test_published_priority_schemas_defer_vocabulary_to_settings(self) -> None:
        paths = {
            "atom": ROOT / "dset/scopes/gov/schemas/atom.schema.json",
            "change": ROOT / "dset/scopes/gov/schemas/change.schema.json",
            "review": ROOT / "dset/scopes/gov/schemas/review-report.schema.json",
            "conflict": (
                ROOT / "dset/scopes/gov/schemas/conflict-candidate.schema.json"
            ),
            "lifecycle": ROOT / "dset/scopes/gov/schemas/lifecycle.schema.json",
            "traceability": (
                ROOT / "dset/scopes/tool/schemas/traceability.schema.json"
            ),
        }
        schemas = {
            name: json.loads(path.read_text(encoding="utf-8"))
            for name, path in paths.items()
        }
        definitions = (
            schemas["atom"]["properties"]["priority"],
            schemas["change"]["$defs"]["priority"],
            schemas["review"]["properties"]["priority"],
            schemas["review"]["$defs"]["finding"]["properties"]["priority"],
            schemas["conflict"]["$defs"]["priority"],
            schemas["lifecycle"]["properties"]["events"]["items"]["properties"][
                "priority"
            ],
            schemas["traceability"]["$defs"]["semantic_atom"]["properties"]["priority"],
        )
        for definition in definitions:
            self.assertEqual(definition, {"type": "string", "minLength": 1})


if __name__ == "__main__":
    unittest.main()
