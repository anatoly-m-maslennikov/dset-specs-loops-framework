---
artifact_type: "problem"
artifact_subtype: "defect"
artifact_id: "DSET-DEFECT-GOV-003"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Defect — Artifact emission eligibility is self-attested

The emission assessor can return `emission_allowed` from caller-supplied text
without resolving the repository's enabled scopes, lineage, material links,
acceptance act, or affected descendants. Atom sealing does not consume or
verify the assessment, so the mandatory gate can be bypassed.

## Rationale

This is a current governance defect because the accepted rule describes a
repository-backed pre-emission gate, not an advisory questionnaire.
