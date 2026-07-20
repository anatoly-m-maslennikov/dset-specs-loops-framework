from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from dset_toolchain.frontmatter import parse as parse_frontmatter
from dset_toolchain.frontmatter import render as render_frontmatter
from dset_toolchain.layout import discover_layout
from dset_toolchain.toml_codec import loads as load_toml
from dset_toolchain.validation import _validate_markdown
from dset_toolchain.yaml_subset import dump, load, loads

ROOT = Path(__file__).resolve().parents[1]


class YamlSubsetTests(unittest.TestCase):
    def test_parses_repository_manifests(self) -> None:
        layout = discover_layout(ROOT)
        provenance = load(layout.provenance_path)
        cases = load(layout.structured_file(layout.fixtures_root, "cases.toml"))
        self.assertEqual(provenance["project_license"], "Apache-2.0")
        self.assertEqual(cases["cases"][0]["id"], "valid-small-fix")

    def test_round_trip_nested_data(self) -> None:
        value = {
            "version": 1.0,
            "items": [
                {"id": "one", "enabled": True, "tags": ["a", "b"]},
                {"id": "two", "value": None},
            ],
        }
        self.assertEqual(loads(dump(value)), value)

    def test_host_prefixed_ids_round_trip_as_list_scalars(self) -> None:
        value = {
            "llm_session_ids": ["codex:session-001", "claude:session-002"],
            "external_refs": ["https://example.com/evidence"],
        }

        self.assertEqual(loads(dump(value)), value)

    def test_path_aware_dump_and_load_select_toml(self) -> None:
        value = {"schema_version": "1.0", "items": [{"id": "DSET-ITEM-001"}]}
        path = Path("authority.toml")

        self.assertEqual(load_toml(dump(value, path)), value)

    def test_frontmatter_reads_legacy_yaml_and_renders_toml(self) -> None:
        legacy = "---\nid: DSET-ITEM-001\n---\nBody\n"
        parsed = parse_frontmatter(legacy)
        assert parsed is not None
        self.assertEqual(parsed[0]["id"], "DSET-ITEM-001")
        self.assertEqual(parsed[2], "yaml")

        rendered = render_frontmatter({"id": "DSET-ITEM-001"}, "Body\n")
        self.assertTrue(rendered.startswith("+++\n"))
        self.assertEqual(parse_frontmatter(rendered)[2], "toml")  # type: ignore[index]

    def test_toml_array_tables_in_frontmatter_are_not_wiki_links(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            document = root / "dset" / "record.md"
            document.parent.mkdir()
            document.write_text(
                '+++\n[[relations]]\ntype = "check_of"\n'
                'target = "DSET-REQUIREMENT-001"\n+++\n\nBody.\n',
                encoding="utf-8",
            )

            self.assertEqual(_validate_markdown(root), [])


if __name__ == "__main__":
    unittest.main()
