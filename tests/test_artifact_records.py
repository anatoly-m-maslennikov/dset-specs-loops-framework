"""Verify persisted atomic artifacts use route-first metadata."""

from __future__ import annotations

import unittest
from pathlib import Path

from dset_toolchain.artifact_records import (
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
                    'schema_version = "1.5"',
                    "[artifacts]",
                    'creation_strictness = "medium"',
                    "[routing]",
                    'revision_modes = ["atomic", "evergreen", "maintained"]',
                    'content_roles = ["inquiry", "definition", "rationale", '
                    '"method", "implementation", "observation"]',
                    'governance_origins = ["internal", "external"]',
                    'relation_shapes = ["standalone", "relational"]',
                    "[priority]",
                    'scale = ["high", "medium", "low"]',
                    'default = "medium"',
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
                    'governance_origin = "internal"',
                    'relation_shape = "standalone"',
                    'scope_path = ["project:dset"]',
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
            "Internal Atomic Definition Artifact",
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


if __name__ == "__main__":
    unittest.main()
