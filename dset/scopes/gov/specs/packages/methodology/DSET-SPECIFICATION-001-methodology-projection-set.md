---
artifact_type: specification
artifact_subtype: governance
artifact_id: DSET-SPECIFICATION-001
scope:
  kind: project
  id: dset-specs-loops-framework
relations:
  - type: projection_of
    range:
      semantic_type: decision
      layer: gov
      scope:
        kind: project
        id: dset-specs-loops-framework
      through: DSET-ATOMIC-RECORD-047
  - type: projection_of
    range:
      semantic_type: qa
      subtype: test
      layer: gov
      scope:
        kind: project
        id: dset-specs-loops-framework
      through: DSET-ATOMIC-RECORD-042
  - type: projection_of
    range:
      semantic_type: qa
      subtype: evaluation
      layer: gov
      scope:
        kind: project
        id: dset-specs-loops-framework
      through: DSET-ATOMIC-RECORD-044
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Methodology projection set

This evergreen carrier binds the current GOV semantic frontiers to the package
fragments that compile them:

- [Behavior specification](spec.md)
- [Deterministic Test plan](test-plan.md)
- [Qualitative Evaluation plan](eval-plan.md)

It owns projection metadata only. The linked fragments own their respective
compiled content, and the immutable atoms own authority and QA definitions.
