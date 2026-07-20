---
artifact_type: atomic_record
artifact_id: DSET-ATOMIC-RECORD-001
type: decision
subtype: requirement
semantic_id: DSET-REQUIREMENT-GOV-030
status: accepted
priority: unknown
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Requirement — Name artifacts by primary artifact type

New artifact IDs and filenames must include the primary artifact type token by
default. An optional direct artifact subtype lives in artifact metadata and is
not a structural name token. Projects may opt newly emitted artifacts into
subtype-bearing names with
`optional_capabilities.artifact_subtype_in_names = true` in root `dset.toml`.
The setting is one independent optional capability, not a bundled advanced
mode. It never renames an immutable atom or an already stable identity.

## Rationale

Primary types remain mandatory and stable while subtypes are optional. Keeping
the default name aligned to the stable axis makes file lists predictable and
prevents later subtype refinement from forcing identity churn.

This emitted Requirement atom is immutable. Later correction, absorption, or
retirement requires a new linked atom or append-only lifecycle event.
