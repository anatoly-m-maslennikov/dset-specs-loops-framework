---
artifact_type: "question"
artifact_id: "DSET-QUESTION-GOV-009"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "relates_to"
    targets:
      - "DSET-DECISION-GOV-032"
---

# Question — Which direct Decision subtypes?

The current five-Type boundary remains useful: Requirements state required
results and Decisions state material selected approaches. The unresolved
classification is how to specialize Decisions without duplicating structural
layers or restoring Requirements as Decision subtypes.

The filename policy is a separate project setting. Once the subtype vocabulary
is selected, this repository can enable subtype-bearing names for newly emitted
atomic artifacts without renaming immutable history.

## Primary claim

Which direct Decision subtypes should DSET define, and are they semantic categories such as architecture and implementation or the former Requirement, Constraint, and Contract set?

## Rationale

The operator explicitly requires Decision subtypes, but the accepted Requirement-versus-Decision boundary does not determine their vocabulary; choosing the wrong set would either duplicate layers or collapse required results back into selected approaches.
