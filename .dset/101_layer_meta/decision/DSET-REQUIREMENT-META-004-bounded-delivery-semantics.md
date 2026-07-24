---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-META-004"
scope_path:
  - "layer:meta"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Requirement — Bounded delivery semantics

A retryable receiver declares its deduplication or idempotency key, retention
window, owner, and atomic check/write boundary. DSET does not claim universal
exactly-once execution.

## Primary claim

Retryable delivery is described as at-least-once plus receiving-side deduplication or idempotency, with effectively-once effects claimed only inside an explicit boundary.

## Rationale

At-least-once delivery does not create universal exactly-once behavior; the key, retention, and atomic check/write boundary determine the effect guarantee.
