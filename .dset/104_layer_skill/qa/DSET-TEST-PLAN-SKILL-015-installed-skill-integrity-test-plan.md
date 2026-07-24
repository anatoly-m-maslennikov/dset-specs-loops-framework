+++
artifact_id = "DSET-ATOMIC-RECORD-065"
semantic_id = "DSET-TEST-PLAN-SKILL-015"
revision_mode = "atomic"
content_role = "method"
governance_origin = "external"
relation_shape = "standalone"
scope_path = ["layer:skill"]
status = "accepted"
priority = "high"
authority = "external:skill-refactor-audit"
claim = "Deterministic installation tests seal every rendered wrapper tree and runtime payload and reject any post-install wrapper, runtime, manifest, or receipt mutation."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-SKILL-011"
+++

# Test Plan — Reject installed skill and runtime mutation

Installation and receipt fixtures must bind expected source/render identities
to every wrapper and runtime payload and fail after any installed file or
manifest is changed, added, removed, or substituted.

This Test definition is immutable. Runs and evidence are separate.
