+++
artifact_id = "DSET-ATOMIC-RECORD-094"
semantic_id = "DSET-TEST-PLAN-OPS-019"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:ops"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic verification proves that a Windows Python executable path containing backslashes and spaces remains one exact subprocess argument after command-template expansion."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-DECISION-OPS-010"

[[relations]]
type = "check_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Test Plan — Preserve a native-Windows Python executable argument

Parse a representative verification template with `{python}` and substitute a
Windows executable path containing both backslashes and spaces. The resulting
argument vector must contain the original path byte-for-byte as its first and
only executable argument, followed by the expected module arguments.

Run the focused verifier suite, the complete DSET verification suite, and fresh
hosted Linux, macOS, and native-Windows jobs. The platform gate closes only
when the exact pushed head passes on every hosted runner.

This emitted Test atom is immutable. Later correction requires a successor Test
and append-only lifecycle event.
