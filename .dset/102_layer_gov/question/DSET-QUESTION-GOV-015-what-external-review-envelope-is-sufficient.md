---
artifact_type: question
artifact_id: DSET-QUESTION-GOV-015
scope_path: ["layer:gov"]
priority: medium
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-QUESTION-GOV-007"
---

# Question — What external-review envelope is sufficient?

What minimum structured identity, provenance, scope, finding, and disposition
envelope should DSET require when importing an external review, while allowing
the review's analysis body and native attachments to remain free-form?

The resolution should distinguish:

- the external review carrier from DSET's internal Analysis and Observation
  artifacts;
- mandatory review provenance from optional reviewer-specific fields;
- machine-actionable findings from unrestricted narrative;
- imported evidence from project Verification; and
- a stable interoperability contract from provider-specific report schemas.

This successor removes the obsolete DSET 0.3 deadline and asks only the still
open governance question.
