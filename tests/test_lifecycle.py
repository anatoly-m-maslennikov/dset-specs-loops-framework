from __future__ import annotations

import unittest

from dset_toolchain.lifecycle import (
    LifecycleClosureError,
    advance_closure,
    initial_closure,
)


class LifecycleClosureTests(unittest.TestCase):
    def test_implementation_closure_is_ordered_and_finite(self) -> None:
        closure = initial_closure("dset-implement", "implement")
        self.assertEqual(closure["next_workflow"], "decisions")

        closure = advance_closure(
            closure,
            workflow_id="decisions",
            observations={
                "proof_plan_complete": False,
                "implementation_plan_complete": False,
                "implementation_authorized": False,
            },
        )
        self.assertEqual(closure["next_workflow"], "plan-proof")

        closure = advance_closure(closure, workflow_id="plan-proof")
        self.assertEqual(closure["next_workflow"], "plan-implementation")

        closure = advance_closure(closure, workflow_id="plan-implementation")
        self.assertEqual(closure["status"], "authorization-required")
        self.assertIsNone(closure["next_workflow"])

        closure = advance_closure(
            closure, observations={"implementation_authorized": True}
        )
        self.assertEqual(closure["status"], "ready")
        self.assertEqual(closure["next_workflow"], "implement")

        closure = advance_closure(closure, workflow_id="implement")
        self.assertEqual(closure["status"], "completed")
        self.assertIsNone(closure["next_workflow"])
        self.assertEqual(
            [item["workflow_id"] for item in closure["history"]],
            ["decisions", "plan-proof", "plan-implementation", "implement"],
        )

    def test_unknown_criteria_stop_until_authoritative_observation(self) -> None:
        closure = advance_closure(
            initial_closure("dset-implement", "implement"),
            workflow_id="decisions",
        )
        self.assertEqual(closure["status"], "blocked")
        self.assertEqual(closure["reason_code"], "DSET-RUNTIME-CRITERIA-UNKNOWN")

        closure = advance_closure(
            closure,
            observations={
                "proof_plan_complete": True,
                "implementation_plan_complete": True,
                "implementation_authorized": True,
            },
        )
        self.assertEqual(closure["next_workflow"], "implement")

    def test_mismatch_failure_and_no_progress_fail_closed(self) -> None:
        initial = initial_closure("dset-implement", "implement")
        with self.assertRaisesRegex(LifecycleClosureError, "workflow mismatch"):
            advance_closure(initial, workflow_id="plan-proof")

        failed = advance_closure(
            initial, workflow_id="decisions", child_status="failed"
        )
        self.assertEqual(failed["status"], "stopped")
        self.assertEqual(failed["reason_code"], "DSET-RUNTIME-CHILD-FAILED")

        blocked = advance_closure(initial, workflow_id="decisions")
        stopped = advance_closure(blocked, observations={"proof_plan_complete": None})
        self.assertEqual(stopped["status"], "stopped")
        self.assertEqual(stopped["reason_code"], "DSET-RUNTIME-NO-PROGRESS")

    def test_direct_skill_has_no_prerequisite_closure(self) -> None:
        direct = initial_closure("dset-verify", "verify")
        self.assertEqual(direct["status"], "direct")
        with self.assertRaisesRegex(LifecycleClosureError, "no prerequisite"):
            advance_closure(direct, workflow_id="verify")


if __name__ == "__main__":
    unittest.main()
