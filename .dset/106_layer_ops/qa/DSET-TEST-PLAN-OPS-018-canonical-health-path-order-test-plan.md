+++
artifact_id = "DSET-ATOMIC-RECORD-091"
semantic_id = "DSET-TEST-PLAN-OPS-018"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:ops"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic verification proves that project-health source entries use case-sensitive POSIX relative-path ordering rather than host-native Path ordering."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-DECISION-OPS-009"

[[relations]]
type = "check_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Test Plan — Enforce canonical project-health path ordering

Create a governed fixture containing relative paths whose case-sensitive POSIX
order differs from Windows-native Path order. The source-entry sequence must
use the POSIX text order and the rendered health digest must remain stable.

Run the focused project-health suite, the complete DSET verification suite, and
fresh hosted Linux, macOS, and native-Windows jobs. The platform gate closes
only when the exact pull-request head passes on every hosted runner.

This emitted Test atom is immutable. Later correction requires a successor Test
and append-only lifecycle event.
