"""Verify persisted atomic artifacts use route-first metadata."""

from __future__ import annotations

import unittest
from pathlib import Path

from dset_toolchain.artifact_records import (
    archive_atom,
    build_atomic_artifact_route_index,
    collect_atomic_artifact_records,
)
from dset_toolchain.temp_paths import temporary_directory


class ArtifactRecordTests(unittest.TestCase):
    """Verify collection, identity, and retired taxonomy rejection."""

    def _project(self, raw: str) -> Path:
        root = Path(raw)
        control = root / ".dset"
        control.mkdir()
        (control / "dset_settings.toml").write_text(
            "\n".join(
                (
                    'schema_version = "1.8"',
                    "[artifacts]",
                    'creation_strictness = "medium"',
                    "enabled_types = []",
                    "enabled_subtypes = []",
                    "[artifacts.routing]",
                    'revision_modes = ["atomic", "append_only", "maintained"]',
                    'content_roles = ["inquiry", "analysis", "definition", '
                    '"method", "implementation", "observation"]',
                    'governance_loci = ["internal", "external", "relation"]',
                    "[priority]",
                    'scale = ["high", "medium", "low"]',
                    'default = "medium"',
                    "[structure]",
                    'layout = "separated-methodology-v1"',
                    "",
                )
            ),
            encoding="utf-8",
        )
        return root

    def _atom(self, root: Path, extra: str = "") -> Path:
        path = root / ".dset/atom.md"
        path.write_text(
            "\n".join(
                (
                    "+++",
                    'artifact_id = "DSET-ATOMIC-001"',
                    'semantic_id = "DSET-CLAIM-001"',
                    'revision_mode = "atomic"',
                    'content_role = "definition"',
                    'governance_locus = "internal"',
                    "scope_path = []",
                    'status = "accepted"',
                    'priority = "high"',
                    'llm_session_ids = ["codex:session-1"]',
                    extra,
                    "+++",
                    "",
                    "# Routed claim",
                    "",
                )
            ),
            encoding="utf-8",
        )
        return path

    def test_index_contains_route_and_no_type_fields(self) -> None:
        with temporary_directory(prefix="dset-route-record-") as raw:
            root = self._project(raw)
            self._atom(root)
            rows = build_atomic_artifact_route_index(root)

        self.assertEqual(len(rows), 1)
        self.assertEqual(
            rows[0]["route"]["name"],
            "Internal Atomic Definition",
        )
        self.assertNotIn("type", rows[0])
        self.assertNotIn("subtype", rows[0])

    def test_retired_type_metadata_is_rejected(self) -> None:
        with temporary_directory(prefix="dset-route-record-") as raw:
            root = self._project(raw)
            self._atom(root, 'type = "decision"')
            records, diagnostics = collect_atomic_artifact_records(root)

        self.assertEqual(records, {})
        self.assertTrue(
            any("Type/subtype metadata" in item.message for item in diagnostics),
            diagnostics,
        )

    def test_archive_moves_bytes_without_changing_route(self) -> None:
        with temporary_directory(prefix="dset-route-record-") as raw:
            root = self._project(raw)
            source = self._atom(root)
            original = source.read_bytes()

            destination = archive_atom(root, "DSET-CLAIM-001")

            self.assertEqual(
                destination,
                root.resolve() / ".dset/archive/atom.md",
            )
            self.assertEqual(destination.read_bytes(), original)
            rows = build_atomic_artifact_route_index(root)
            self.assertTrue(rows[0]["archived"])


if __name__ == "__main__":
    unittest.main()
