---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-META-027"
scope_path:
  - "layer:meta"
priority: "high"
promotion:
  affected_children:
    - "governance"
    - "tool"
    - "skill"
    - "implementation"
    - "operations"
  applies_unchanged: true
  local_context_required: false
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "relates_to"
    targets:
      - "DSET-REQUIREMENT-META-020"
      - "DSET-REQUIREMENT-META-025"
---

# Requirement — Propagate accepted change forward

When accepted authority changes in an earlier layer, DSET:

1. preserves every historical atomic record;
2. identifies affected downstream evergreen views, Methods, Implementations,
   Observations, and assurance;
3. marks those dependents potentially stale;
4. resumes the forward flow at the changed owner; and
5. restores currentness only after affected downstream gates are satisfied.

Refreshing an evergreen view alone does not complete propagation. Downstream
realization and assurance remain stale until their own owning criteria are met.

## Primary claim

An accepted upstream change propagates forward by marking affected downstream views, methods, implementations, and assurance potentially stale without mutating historical atoms.

## Rationale

Explicit forward invalidation preserves history while preventing downstream artifacts from appearing current after their governing assumptions change.
