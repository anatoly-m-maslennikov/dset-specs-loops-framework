+++
artifact_id = "DSET-ATOMIC-RECORD-069"
semantic_id = "DSET-TEST-PLAN-SKILL-017"
revision_mode = "atomic"
content_role = "method"
governance_origin = "external"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:skill"]
status = "accepted"
priority = "high"
authority = "external:skill-refactor-audit"
claim = "An end-to-end wrapper test proves handoff keeps one explicit session active across specialist context resolution and only a true terminal outcome completes or stops it."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-SKILL-009"
+++

# Test Plan — Preserve session identity through handoff

The command-level fixture starts `dset`, records a successful handoff without
terminalizing the session, resolves a specialist with the same session ID, and
then proves explicit completion closes it. Ambiguous or absent continuity must
stop rather than silently create a new chain.

This Test definition is immutable. Runs and evidence are separate.
