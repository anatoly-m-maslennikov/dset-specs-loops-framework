---
artifact_type: atomic_record
artifact_id: DSET-ATOMIC-RECORD-022
type: problem
subtype: gap
semantic_id: DSET-GAP-GOV-001
status: accepted
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Gap — Legacy authority lacks immutable-content protection

Compatibility classification preserves legacy semantic identities but does
not bind their carrier content to immutable digests. Active legacy Decisions
can therefore change without an absorption or successor event while native
atomic records are protected.

## Rationale

This is a missing governance capability, not a retyping request. Stable legacy
IDs and content must remain intact while receiving equivalent mutation checks
or explicit native successors.
