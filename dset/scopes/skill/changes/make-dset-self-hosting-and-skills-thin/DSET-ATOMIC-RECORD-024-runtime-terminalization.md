---
artifact_type: atomic_record
artifact_id: DSET-ATOMIC-RECORD-024
type: problem
subtype: defect
semantic_id: DSET-DEFECT-TOOL-001
status: accepted
priority: critical
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Defect — Skill runs are started but not terminalized

Skill context starts a runtime run and persists a running checkpoint, but the
thin-wrapper path has no guaranteed finish operation. Nested calls overwrite
the single latest-run checkpoint, leaving parent runs running and later unable
to finish through the checkpoint route.

## Rationale

This is a current tool defect because normal skill invocation produces
misleading operational state and loses resumable parent identity.
