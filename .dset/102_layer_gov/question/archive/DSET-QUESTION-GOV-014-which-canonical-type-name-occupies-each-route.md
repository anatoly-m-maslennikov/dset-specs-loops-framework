---
artifact_type: question
artifact_id: DSET-QUESTION-GOV-014
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-045"
      - "DSET-REQUIREMENT-META-046"
      - "DSET-PROBLEM-GOV-008"
      - "DSET-IMPL-GOV-009"
      - "DSET-QUESTION-GOV-013"
---

# Question — Which canonical type name occupies each semantic route?

Which single understandable artifact type name should GOV assign to each of the
54 required Revision mode × Content role × Governance locus routes?

The resolution must:

- assign exactly one canonical type to every route;
- leave no empty route and no route with multiple top-level types;
- give every type one unambiguous identity kind;
- keep internal, external, and relational loci distinguishable;
- preserve the route cycle from Inquiry through Analysis, Definition, Method,
  Implementation, and Observation; and
- leave finer meanings to direct subtypes rather than duplicate top-level
  types.

This Question owns canonical type naming. `DSET-QUESTION-GOV-013` separately
owns subtype refinement after the top-level names are accepted.
