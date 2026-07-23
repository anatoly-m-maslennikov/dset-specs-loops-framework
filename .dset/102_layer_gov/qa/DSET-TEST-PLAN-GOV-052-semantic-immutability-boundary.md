+++
artifact_id = "DSET-ATOMIC-RECORD-209"
semantic_id = "DSET-TEST-PLAN-GOV-052"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic validation distinguishes permitted identity or carrier recoding from a forbidden atomic semantic mutation."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-060"

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-061"
+++

# Test Plan — Enforce the semantic immutability boundary

Accept a complete one-to-one migration that changes only canonical identity and
carrier-representation fields. Reject any migration that changes a claim,
rationale, authority, provenance fact, scope or applicability meaning,
creation priority, relation meaning or connected artifact, or QA condition,
criterion, threshold, or expected disposition.

Also prove that lifecycle state and effective priority change only through
append-only events or derived state, and that a semantic correction uses a new
successor atom rather than a migrated predecessor.
