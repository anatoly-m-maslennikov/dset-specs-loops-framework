+++
artifact_id = "DSET-ATOMIC-RECORD-041"
semantic_id = "DSET-TEST-PLAN-SKILL-014"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:skill"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic tests prove lazy prerequisite closure and strict implementation-only behavior from project settings."
promotion = {}
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-SKILL-012"

[[relations]]
type = "replacement_of"
target = "DSET-TEST-PLAN-SKILL-012"
+++

# Test Plan — Validate implementation preparation modes

Deterministic proof must show that a missing setting selects `lazy`; explicit
`lazy` uses the ordered decisions, proof-plan, implementation-plan, implement
closure; and explicit `strict` selects only `implement` without creating a
prerequisite child run. Invalid values must stop before a run is created.

Strict mode must report insufficient or ambiguous accepted input rather than
silently switching to lazy behavior. Both modes must preserve project-local
rule resolution, authorization, session/run identity, provenance, terminal
finish behavior, and the Verification/release stop boundary.

This Test completely replaces `DSET-TEST-PLAN-SKILL-012`. Runs and evidence are
separate.
