+++
artifact_id = "DSET-ATOMIC-RECORD-155"
semantic_id = "DSET-PROBLEM-GOV-006"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "Accepted methodology now makes every emitted atomic artifact immutable and requires append-only lifecycle events, explicit acyclic absorption, derived current state, and byte-stable archival only after full retirement, but current schemas and validators still permit in-place mutation and do not maintain canonical ID/digest lookup across archive moves."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}
+++

# Problem — Immutable atomic lifecycle is not enforced

Accepted methodology now makes every emitted atomic artifact immutable and requires append-only lifecycle events, explicit acyclic absorption, derived current state, and byte-stable archival only after full retirement, but current schemas and validators still permit in-place mutation and do not maintain canonical ID/digest lookup across archive moves.

## Migrated context

- Original intake status: `open`
- Original owner Change: `DSET-CHANGE-SKILL-001`

This one-claim carrier replaces the former aggregate intake row. Current
status is derived from atomic lifecycle events.
