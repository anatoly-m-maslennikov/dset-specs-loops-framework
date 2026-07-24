+++
artifact_id = "DSET-ATOMIC-RECORD-273"
semantic_id = "DSET-REQUIREMENT-META-004"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Retryable delivery is described as at-least-once plus receiving-side deduplication or idempotency, with effectively-once effects claimed only inside an explicit boundary."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "At-least-once delivery does not create universal exactly-once behavior; the key, retention, and atomic check/write boundary determine the effect guarantee."
+++

# Requirement — Bounded delivery semantics

A retryable receiver declares its deduplication or idempotency key, retention
window, owner, and atomic check/write boundary. DSET does not claim universal
exactly-once execution.
