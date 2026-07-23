+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-097"
type = "qa"
subtype = "test_plan"
semantic_id = "DSET-TEST-PLAN-OPS-020"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic verification proves that repository path aliases compare by resolved identity and that a Windows relative Path becomes canonical POSIX repository text without weakening string validation."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "check_of"
target = "DSET-DECISION-OPS-011"

[[relations]]
type = "check_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Test Plan — Enforce canonical repository path identity

Create a directory alias and require layout discovery, containment, evidence,
and archive operations to compare the alias and target by resolved identity.
Pass a representative Windows relative Path and require POSIX repository text;
continue rejecting a string containing backslashes.

Run the focused layout/archive/evidence suites, the complete DSET verification
suite, and fresh hosted Linux, macOS, and native-Windows jobs. The platform gate
closes only when the exact pushed head passes on every hosted runner.

This emitted Test atom is immutable. Later correction requires a successor Test
and append-only lifecycle event.
