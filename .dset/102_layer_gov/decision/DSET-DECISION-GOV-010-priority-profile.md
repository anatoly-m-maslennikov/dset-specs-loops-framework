+++
artifact_id = "DSET-ATOMIC-RECORD-009"
semantic_id = "DSET-DECISION-GOV-010"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Decision — Use one readable five-level priority scale

The `core-v1` profile uses one ordered priority scale: `critical`, `high`,
`medium`, `low`, and `deferred`. The project default is `medium`.

An artifact may declare a value directly or inherit it through one visible
owning atom or Change and then the project default. A direct `unknown` is an
explicit unresolved state and never inherits silently. Append-only lifecycle
events, not atom edits, change an emitted atom's effective priority.

Priority orders current attention and may select a claim only after the
conflict class and governing policy permit selection. It never turns an unmet
immutable obligation into compliance, converts evidence into authority, or
overrides an explicit absorption or authority relation.

## Rationale

Readable words make the ordering understandable in file lists and review
reports without an extra legend at every use. Five values give enough
separation for release blockers, active work, normal work, low-value work, and
deliberately postponed work while remaining small enough for deterministic
comparison.

This Decision resolves `DSET-QUESTION-GOV-002`. It is immutable; later changes
require a successor Decision and an append-only lifecycle event.
