---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-META-001"
scope_path:
  - "layer:meta"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-META-018"
---

# Requirement — Governed feedback cycle

Test plans, evaluation plans, and implementation plans are Methods. Code and
generated operative outputs are Implementations. Test and evaluation results
are Observations. Each governed artifact has one primary content role while
relations connect it to other roles.

## Primary claim

DSET uses one six-role feedback cycle: Inquiry, Definition, Rationale, Method, Implementation, and Observation.

## Rationale

One role cycle keeps desired state, reasoning, realization, and observed feedback distinct without turning workflow position into artifact identity.
