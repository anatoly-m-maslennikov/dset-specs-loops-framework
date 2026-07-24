+++
artifact_id = "DSET-ATOMIC-RECORD-100"
semantic_id = "DSET-TEST-PLAN-OPS-021"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:ops"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic verification requires temporary Git fixtures to retain exact working-tree and blob bytes independent of ambient Windows autocrlf and text newline defaults."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-DECISION-OPS-012"

[[relations]]
type = "check_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Test Plan — Enforce deterministic temporary Git bytes

Initialize every temporary Git repository through one helper that writes the
local newline policy before staging. Assert that byte-sealed transition source
digests match their Git blobs and that a rejected retirement leaves the exact
materialized carrier bytes unchanged.

Run carrier-transition, semantic-atom, migration, bootstrap, and artifact-type
fixtures; then run the complete suite and fresh hosted Linux, macOS, and
native-Windows jobs. The gate closes only on the exact pushed head.

This emitted Test atom is immutable. Later correction requires a successor Test
and append-only lifecycle event.
