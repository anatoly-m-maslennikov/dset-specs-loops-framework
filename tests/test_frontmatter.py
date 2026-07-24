"""Verify DSET Markdown property envelope parsing and rendering."""

from __future__ import annotations

import unittest

from dset_toolchain.frontmatter import FrontmatterError, parse, render


class FrontmatterTests(unittest.TestCase):
    """Cover canonical YAML and compatibility TOML envelopes."""

    def test_yaml_round_trip_preserves_metadata_and_body(self) -> None:
        metadata = {
            "artifact_type": "requirement",
            "artifact_id": "DSET-REQUIREMENT-META-001",
            "scope_path": ["layer:meta"],
            "priority": "high",
            "llm_session_ids": ["codex:test-session"],
            "relations": [
                {
                    "type": "analysis_of",
                    "targets": [
                        "DSET-REQUIREMENT-META-002",
                        "DSET-REQUIREMENT-META-003",
                    ],
                }
            ],
        }
        body = "\n# Requirement\n"

        parsed = parse(render(metadata, body, format="yaml"))

        self.assertEqual(parsed, (metadata, body, "yaml"))

    def test_toml_remains_supported_during_layered_migration(self) -> None:
        metadata = {
            "artifact_id": "DSET-REQUIREMENT-TOOL-001",
            "priority": "medium",
        }
        body = "\n# Requirement\n"

        parsed = parse(render(metadata, body, format="toml"))

        self.assertEqual(parsed, (metadata, body, "toml"))

    def test_yaml_requires_a_mapping_root(self) -> None:
        with self.assertRaisesRegex(
            FrontmatterError,
            "frontmatter root must be a mapping",
        ):
            parse("---\n- item\n---\n# Body\n")

    def test_markdown_without_properties_is_unchanged(self) -> None:
        self.assertIsNone(parse("# Plain Markdown\n"))


if __name__ == "__main__":
    unittest.main()
