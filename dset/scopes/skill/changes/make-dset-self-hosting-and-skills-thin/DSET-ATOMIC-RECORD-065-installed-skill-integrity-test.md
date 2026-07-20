+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-065"
type = "qa"
subtype = "test"
semantic_id = "DSET-TEST-SKILL-015"
status = "accepted"
priority = "critical"
authority = "external:skill-refactor-audit"
claim = "Deterministic installation tests seal every rendered wrapper tree and runtime payload and reject any post-install wrapper, runtime, manifest, or receipt mutation."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-SKILL-011"
+++

# Test — Reject installed skill and runtime mutation

Installation and receipt fixtures must bind expected source/render identities
to every wrapper and runtime payload and fail after any installed file or
manifest is changed, added, removed, or substituted.

This Test definition is immutable. Runs and evidence are separate.
