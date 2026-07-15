from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "dset" / "scopes" / "skill"


class SessionContractTests(unittest.TestCase):
    def test_run_records_link_every_invocation_to_one_session(self) -> None:
        schema = json.loads(
            (SKILL_ROOT / "schemas" / "skill-run.schema.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(schema["properties"]["schema_version"]["const"], "1.1")
        self.assertTrue(
            {
                "session_id",
                "root_run_id",
                "parent_run_id",
                "invocation_source",
                "checkpoint",
            }.issubset(schema["required"])
        )
        self.assertEqual(
            set(schema["properties"]["invocation_source"]["enum"]),
            {
                "operator",
                "public-skill",
                "chained-skill",
                "governed-model",
                "delegated-run",
            },
        )
        self.assertIn("target", schema["properties"]["scope"]["required"])

    def test_checkpoint_is_bounded_and_points_back_to_authority(self) -> None:
        schema = json.loads(
            (SKILL_ROOT / "schemas" / "session-checkpoint.schema.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(schema["properties"]["objective"]["maxLength"], 1024)
        self.assertEqual(schema["properties"]["completed"]["maxItems"], 64)
        self.assertEqual(schema["properties"]["pending"]["maxItems"], 32)
        self.assertEqual(schema["properties"]["touched_paths"]["maxItems"], 64)
        self.assertIn("authority_snapshot", schema["required"])
        self.assertIn("next", schema["required"])
        self.assertIn("target", schema["$defs"]["scope"]["required"])
        forbidden = {"prompt", "messages", "source_content", "tool_output", "secret"}
        self.assertTrue(forbidden.isdisjoint(schema["properties"]))

    def test_live_and_template_continuity_rules_match(self) -> None:
        for name in ("skill-runs.md", "lifecycle-orchestration.md"):
            with self.subTest(rule=name):
                live = SKILL_ROOT / "governance" / name
                template = SKILL_ROOT / "templates" / "governance" / "core-v1" / name
                self.assertEqual(live.read_bytes(), template.read_bytes())

    def test_session_state_is_ignored_machine_local_evidence(self) -> None:
        ignored = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn(".dset/runs/", ignored)
        self.assertIn(".dset/sessions/", ignored)


if __name__ == "__main__":
    unittest.main()
