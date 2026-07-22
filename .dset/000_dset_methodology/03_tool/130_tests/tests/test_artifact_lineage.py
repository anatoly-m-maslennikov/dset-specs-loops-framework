from __future__ import annotations

import subprocess
import unittest
from pathlib import Path
from typing import Any

from dset_toolchain import yaml_subset
from dset_toolchain.lineage import (
    RELATION_TYPES,
    build_commit_implementation_relations,
    build_relation_index,
    collect_artifact_relations,
    validate_artifact_relations,
)
from dset_toolchain.temp_paths import temporary_directory
from tests import repository_root


class ArtifactRelationTests(unittest.TestCase):
    def test_all_canonical_forward_relations_are_indexed_without_inverses(
        self,
    ) -> None:
        with temporary_directory() as raw:
            root = Path(raw).resolve()
            self._artifact(root, "TARGET", "APP-DECISION-GOV-001")
            sources = {
                "child_of": ("atomic_record", "decision", None),
                "analysis_of": ("analysis_report", None, None),
                "implementation_of": ("implementation", None, None),
                "check_of": ("atomic_record", "qa", "test"),
                "evidence_for": ("evidence_record", None, None),
                "resolution_of": ("atomic_record", "decision", None),
                "override_of": ("atomic_record", "decision", None),
                "relates_to": ("navigation", None, None),
            }
            for sequence, (relation_type, source) in enumerate(
                sources.items(), start=2
            ):
                artifact_type, semantic_type, subtype = source
                self._artifact(
                    root,
                    relation_type,
                    f"APP-SOURCE-{sequence:03d}",
                    artifact_type=artifact_type,
                    semantic_type=semantic_type,
                    subtype=subtype,
                    relations=[
                        {"type": relation_type, "target": "APP-DECISION-GOV-001"}
                    ],
                )
            self._atom(root, 10, "APP-DECISION-GOV-010")
            self._projection(root, through="APP-ATOMIC-RECORD-010")
            self._replacement_fixture(root)

            nodes, diagnostics = collect_artifact_relations(root)
            rows = build_relation_index(root)

            self.assertEqual(diagnostics, [])
            self.assertEqual({row["type"] for row in rows}, RELATION_TYPES)
            self.assertTrue(nodes["APP-SOURCE-002"].child_of)
            self.assertFalse(
                any("parent_to" in row or "implemented_by" in row for row in rows)
            )

    def test_projection_range_rejects_stale_or_mismatched_frontier(self) -> None:
        cases = {
            "stale": ("APP-ATOMIC-RECORD-001", "stale projection frontier"),
            "wrong-layer": ("APP-ATOMIC-RECORD-003", "outside its range"),
            "unknown": ("APP-ATOMIC-RECORD-999", "must name an atom carrier"),
        }
        for name, (through, expected) in cases.items():
            with self.subTest(name=name), temporary_directory() as raw:
                root = Path(raw).resolve()
                self._atom(root, 1, "APP-DECISION-GOV-001")
                self._atom(root, 2, "APP-DECISION-GOV-002")
                self._atom(root, 3, "APP-DECISION-TOOL-003")
                self._projection(root, through=through)

                messages = [item.message for item in validate_artifact_relations(root)]

                self.assertTrue(any(expected in item for item in messages), messages)

    def test_invalid_authored_relations_fail_closed(self) -> None:
        cases = {
            "scalar": ("relations: APP-DECISION-001\n", "non-empty list"),
            "unknown-type": (
                "relations:\n  - type: depends_on\n    target: APP-DECISION-001\n",
                "unknown relation type",
            ),
            "missing": (
                "relations:\n  - type: child_of\n    target: APP-MISSING-001\n",
                "unresolved child_of target",
            ),
            "reverse": (
                "parent_to:\n  - APP-DECISION-001\n",
                "reverse relations must not be authored",
            ),
            "both-shapes": (
                "relations:\n  - type: child_of\n    target: APP-DECISION-001\n"
                "child_of:\n  - APP-DECISION-001\n",
                "cannot be authored together",
            ),
            "two-types-one-pair": (
                "relations:\n"
                "  - type: child_of\n    target: APP-DECISION-001\n"
                "  - type: relates_to\n    target: APP-DECISION-001\n",
                "one primary relation",
            ),
        }
        for name, (extra, expected) in cases.items():
            with self.subTest(name=name), temporary_directory() as raw:
                root = Path(raw).resolve()
                self._artifact(root, "TARGET", "APP-DECISION-001")
                self._artifact(root, "SOURCE", "APP-DECISION-002", extra=extra)
                messages = [item.message for item in validate_artifact_relations(root)]
                self.assertTrue(any(expected in item for item in messages), messages)

    def test_self_relations_and_structural_cycles_fail_closed(self) -> None:
        with temporary_directory() as raw:
            root = Path(raw).resolve()
            self._artifact(
                root,
                "SELF",
                "APP-DECISION-001",
                relations=[{"type": "child_of", "target": "APP-DECISION-001"}],
            )
            self._artifact(
                root,
                "A",
                "APP-DECISION-002",
                relations=[{"type": "override_of", "target": "APP-DECISION-003"}],
            )
            self._artifact(
                root,
                "B",
                "APP-DECISION-003",
                relations=[{"type": "child_of", "target": "APP-DECISION-002"}],
            )

            messages = [item.message for item in validate_artifact_relations(root)]

            self.assertTrue(any("itself" in item for item in messages))
            self.assertTrue(any("relation cycle" in item for item in messages))

    def test_replacement_requires_matching_absorption(self) -> None:
        with temporary_directory() as raw:
            root = Path(raw).resolve()
            self._artifact(root, "OLD", "APP-DECISION-001")
            self._artifact(
                root,
                "NEW",
                "APP-DECISION-002",
                artifact_type="atomic_record",
                semantic_type="decision",
                relations=[{"type": "replacement_of", "target": "APP-DECISION-001"}],
            )
            messages = [item.message for item in validate_artifact_relations(root)]
            self.assertTrue(
                any("matching append-only absorption" in item for item in messages)
            )

    def test_inactive_legacy_child_of_remains_readable(self) -> None:
        with temporary_directory() as raw:
            root = Path(raw).resolve()
            self._artifact(
                root,
                "OLD",
                "APP-ATOMIC-RECORD-001",
                artifact_type="atomic_record",
                semantic_id="APP-REQUIREMENT-GOV-001",
                child_of=["APP-LEGACY-DECISION-001"],
            )
            self._artifact(root, "NEW", "APP-REQUIREMENT-GOV-002")
            self._lifecycle(
                root,
                "APP-REQUIREMENT-GOV-001",
                "APP-REQUIREMENT-GOV-002",
            )

            nodes, diagnostics = collect_artifact_relations(root)

            self.assertEqual(diagnostics, [])
            relation = nodes["APP-REQUIREMENT-GOV-001"].relations[0]
            self.assertEqual(relation.type, "child_of")
            self.assertEqual(relation.origin, "legacy_child_of")

    def test_commit_trailers_form_typed_implementation_relations(self) -> None:
        root = repository_root(Path(__file__))
        rows = build_commit_implementation_relations(root)
        matching = [row for row in rows if row["target"] == "DSET-REQUIREMENT-GOV-024"]
        self.assertTrue(matching)
        self.assertTrue(all(row["type"] == "implementation_of" for row in rows))
        self.assertTrue(matching[0]["llm_session_ids"])

    def test_generated_only_commits_do_not_form_implementation_relations(
        self,
    ) -> None:
        with temporary_directory() as raw:
            root = Path(raw).resolve()
            self._git(root, "init")
            self._git(root, "config", "user.name", "DSET Test")
            self._git(root, "config", "user.email", "dset@example.invalid")

            source = root / "source.py"
            source.write_text("value = 1\n", encoding="utf-8")
            substantive = self._commit(
                root,
                "feat: add source\n\n"
                "Implements: APP-DECISION-GOV-001\n"
                "Session: codex:test",
            )

            generated = root / "dset/generated/trace.toml"
            generated.parent.mkdir(parents=True)
            generated.write_text('state = "fresh"\n', encoding="utf-8")
            refresh = self._commit(
                root,
                "chore: refresh trace\n\n"
                "Implements: APP-DECISION-GOV-002\n"
                "Session: codex:test",
            )

            source.write_text("value = 2\n", encoding="utf-8")
            generated.write_text('state = "updated"\n', encoding="utf-8")
            mixed = self._commit(
                root,
                "feat: update source and trace\n\n"
                "Implements: APP-DECISION-GOV-003\n"
                "Session: codex:test",
            )

            rows = build_commit_implementation_relations(root)
            sources = {row["source"] for row in rows}

            self.assertIn(substantive, sources)
            self.assertIn(mixed, sources)
            self.assertNotIn(refresh, sources)

    @staticmethod
    def _git(root: Path, *args: str) -> str:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()

    @classmethod
    def _commit(cls, root: Path, message: str) -> str:
        cls._git(root, "add", "-A")
        cls._git(root, "commit", "-m", message)
        return cls._git(root, "rev-parse", "HEAD")

    @classmethod
    def _replacement_fixture(cls, root: Path) -> None:
        cls._artifact(
            root,
            "OLD-REPLACE",
            "APP-TEST-GOV-020",
            artifact_type="atomic_record",
            semantic_type="qa",
            subtype="test",
        )
        cls._artifact(
            root,
            "NEW-REPLACE",
            "APP-TEST-GOV-021",
            artifact_type="atomic_record",
            semantic_type="qa",
            subtype="test",
            relations=[{"type": "replacement_of", "target": "APP-TEST-GOV-020"}],
        )
        cls._lifecycle(root, "APP-TEST-GOV-020", "APP-TEST-GOV-021")

    @classmethod
    def _projection(cls, root: Path, *, through: str) -> None:
        cls._artifact(
            root,
            "SPEC",
            "APP-SPECIFICATION-001",
            artifact_type="specification",
            relations=[
                {
                    "type": "projection_of",
                    "range": {
                        "semantic_type": "decision",
                        "layer": "gov",
                        "scope": {"kind": "project", "id": "app"},
                        "through": through,
                    },
                }
            ],
        )

    @classmethod
    def _atom(cls, root: Path, sequence: int, semantic_id: str) -> None:
        cls._artifact(
            root,
            f"ATOM-{sequence}",
            f"APP-ATOMIC-RECORD-{sequence:03d}",
            artifact_type="atomic_record",
            semantic_id=semantic_id,
            semantic_type="decision",
            scope={"kind": "project", "id": "app"},
        )

    @staticmethod
    def _lifecycle(root: Path, old: str, new: str) -> None:
        path = root / "dset/governance/lifecycle.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            yaml_subset.dump(
                {
                    "schema_version": "1.0",
                    "events": [
                        {
                            "id": "APP-LIFECYCLE-EVENT-001",
                            "atom_id": old,
                            "event": "absorbed",
                            "occurred_at": "2026-07-20T12:00:00+04:00",
                            "llm_session_ids": ["codex:test"],
                            "related": [new],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )

    @staticmethod
    def _artifact(
        root: Path,
        name: str,
        artifact_id: str,
        *,
        artifact_type: str = "atomic_record",
        semantic_id: str | None = None,
        semantic_type: str | None = None,
        subtype: str | None = None,
        scope: dict[str, str] | None = None,
        relations: list[dict[str, Any]] | None = None,
        child_of: list[str] | None = None,
        extra: str = "",
    ) -> None:
        data: dict[str, Any] = {
            "artifact_type": artifact_type,
            "artifact_id": artifact_id,
        }
        if semantic_id is not None:
            data["semantic_id"] = semantic_id
        if semantic_type is not None:
            data["type"] = semantic_type
        if subtype is not None:
            data["subtype"] = subtype
        if scope is not None:
            data["scope"] = scope
        if relations is not None:
            data["relations"] = relations
        if child_of is not None:
            data["child_of"] = child_of
        text = f"---\n{yaml_subset.dump(data)}"
        if extra:
            text += extra
        text += f"---\n\n# {name}\n"
        (root / f"{name}.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
