+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-069"
type = "qa"
subtype = "test"
semantic_id = "DSET-TEST-SKILL-017"
status = "accepted"
priority = "high"
authority = "external:skill-refactor-audit"
claim = "An end-to-end wrapper test proves handoff keeps one explicit session active across specialist context resolution and only a true terminal outcome completes or stops it."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-SKILL-009"
+++

# Test — Preserve session identity through handoff

The command-level fixture starts `dset`, records a successful handoff without
terminalizing the session, resolves a specialist with the same session ID, and
then proves explicit completion closes it. Ambiguous or absent continuity must
stop rather than silently create a new chain.

This Test definition is immutable. Runs and evidence are separate.
