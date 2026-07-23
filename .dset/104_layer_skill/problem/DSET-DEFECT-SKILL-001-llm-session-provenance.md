+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-026"
type = "problem"
subtype = "defect"
semantic_id = "DSET-DEFECT-SKILL-001"
status = "accepted"
priority = "high"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Defect — Thin wrappers erase LLM session provenance

All thin wrappers invoke `dset skills context` without an LLM session ID, and
the CLI defaults the field to an empty list. The governing runtime interprets
an empty list as a human-only run, so ordinary LLM-driven skill runs are
misclassified unless a host supplies an undocumented extra argument.

## Rationale

This is a current skill defect because session provenance is required at the
wrapper-to-runtime boundary and empty provenance has a defined, different
meaning.
