from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from dset_toolchain import yaml_subset
from dset_toolchain.lineage import (
    build_commit_implementation_edges,
    build_lineage_index,
    collect_artifact_lineage,
    derived_parent_to,
    transitive_ancestors,
    validate_artifact_lineage,
)


class ArtifactLineageTests(unittest.TestCase):
    def test_many_to_many_lineage_derives_reverse_and_transitive_views(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self._artifact(root, "PLAN", "APP-PLAN-001")
            self._artifact(
                root,
                "REQ",
                "APP-ATOMIC-RECORD-001",
                artifact_type="atomic_record",
                semantic_id="APP-REQUIREMENT-001",
                child_of=["APP-PLAN-001"],
            )
            self._artifact(
                root,
                "CONTRACT",
                "APP-ATOMIC-RECORD-002",
                artifact_type="atomic_record",
                semantic_id="APP-CONTRACT-001",
                child_of=["APP-PLAN-001"],
            )
            self._artifact(
                root,
                "TEST",
                "APP-ATOMIC-RECORD-003",
                artifact_type="atomic_record",
                semantic_id="APP-TEST-001",
                child_of=["APP-REQUIREMENT-001", "APP-CONTRACT-001"],
            )

            nodes, diagnostics = collect_artifact_lineage(root)

            self.assertEqual(diagnostics, [])
            self.assertEqual(
                nodes["APP-TEST-001"].child_of,
                ("APP-REQUIREMENT-001", "APP-CONTRACT-001"),
            )
            reverse = derived_parent_to(nodes)
            self.assertEqual(
                reverse["APP-PLAN-001"], ("APP-CONTRACT-001", "APP-REQUIREMENT-001")
            )
            self.assertEqual(
                transitive_ancestors(nodes, "APP-TEST-001"),
                ("APP-CONTRACT-001", "APP-PLAN-001", "APP-REQUIREMENT-001"),
            )
            indexed = {item["id"]: item for item in build_lineage_index(root)}
            self.assertEqual(
                indexed["APP-REQUIREMENT-001"]["parent_to"], ["APP-TEST-001"]
            )

    def test_invalid_authored_lineage_fails_closed(self) -> None:
        cases = {
            "scalar": ("child_of: APP-PLAN-001\n", "non-empty list"),
            "empty": ("child_of: []\n", "non-empty list"),
            "duplicate": (
                "child_of:\n  - APP-PLAN-001\n  - APP-PLAN-001\n",
                "must be unique",
            ),
            "missing": (
                "child_of:\n  - APP-MISSING-001\n",
                "unresolved child_of ID",
            ),
            "reverse": ("parent_to:\n  - APP-CHILD-001\n", "must not be authored"),
        }
        for name, (metadata, expected) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                self._artifact(root, "PLAN", "APP-PLAN-001")
                self._artifact(root, "CHILD", "APP-DECISION-001", extra=metadata)
                messages = [item.message for item in validate_artifact_lineage(root)]
                self.assertTrue(
                    any(expected in message for message in messages), messages
                )

    def test_self_links_and_cycles_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self._artifact(
                root,
                "SELF",
                "APP-DECISION-001",
                child_of=["APP-DECISION-001"],
            )
            self._artifact(
                root,
                "A",
                "APP-DECISION-002",
                child_of=["APP-DECISION-003"],
            )
            self._artifact(
                root,
                "B",
                "APP-DECISION-003",
                child_of=["APP-DECISION-002"],
            )

            messages = [item.message for item in validate_artifact_lineage(root)]

            self.assertTrue(any("child_of itself" in message for message in messages))
            self.assertTrue(any("lineage cycle" in message for message in messages))

    def test_absorption_preserves_invalid_history_without_blocking_successor(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self._artifact(
                root,
                "OLD",
                "APP-ATOMIC-RECORD-001",
                artifact_type="atomic_record",
                semantic_id="APP-REQUIREMENT-001",
                child_of=["APP-LEGACY-DECISION-001"],
            )
            self._artifact(
                root,
                "NEW",
                "APP-ATOMIC-RECORD-002",
                artifact_type="atomic_record",
                semantic_id="APP-REQUIREMENT-002",
            )
            lifecycle = root / "dset/governance/lifecycle.yaml"
            lifecycle.parent.mkdir(parents=True)
            lifecycle.write_text(
                yaml_subset.dump(
                    {
                        "schema_version": "1.0",
                        "events": [
                            {
                                "id": "APP-LIFECYCLE-EVENT-001",
                                "atom_id": "APP-REQUIREMENT-001",
                                "event": "absorbed",
                                "occurred_at": "2026-07-20T12:00:00+04:00",
                                "llm_session_ids": ["codex:test"],
                                "related": ["APP-REQUIREMENT-002"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            nodes, diagnostics = collect_artifact_lineage(root)

            self.assertEqual(diagnostics, [])
            self.assertEqual(
                nodes["APP-REQUIREMENT-001"].child_of,
                ("APP-LEGACY-DECISION-001",),
            )
            self.assertEqual(nodes["APP-REQUIREMENT-002"].child_of, ())

    def test_commit_implements_trailers_form_derived_edges(self) -> None:
        edges = build_commit_implementation_edges(Path(__file__).resolve().parents[1])
        by_commit = {item["commit"]: item for item in edges}
        health_commit = next(
            item
            for item in by_commit.values()
            if "DSET-REQUIREMENT-GOV-024" in item["implements"]
        )
        self.assertIn("DSET-REQUIREMENT-TOOL-018", health_commit["implements"])
        self.assertTrue(health_commit["llm_session_ids"])

    @staticmethod
    def _artifact(
        root: Path,
        name: str,
        artifact_id: str,
        *,
        artifact_type: str = "plan",
        semantic_id: str | None = None,
        child_of: list[str] | None = None,
        extra: str = "",
    ) -> None:
        lines = [
            "---",
            f"artifact_type: {artifact_type}",
            f"artifact_id: {artifact_id}",
        ]
        if semantic_id is not None:
            lines.append(f"semantic_id: {semantic_id}")
        if child_of is not None:
            lines.append("child_of:")
            lines.extend(f"  - {parent}" for parent in child_of)
        if extra:
            lines.extend(extra.rstrip().splitlines())
        lines.extend(["---", "", f"# {name}", ""])
        (root / f"{name}.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
