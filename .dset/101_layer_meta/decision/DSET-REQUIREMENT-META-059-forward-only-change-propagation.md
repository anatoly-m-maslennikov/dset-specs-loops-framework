---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-059
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-027"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-025"
      - "DSET-REQUIREMENT-META-054"
---

# Requirement — Propagate accepted change forward

An accepted upstream change propagates only forward through the ordered layer
graph. It:

1. identifies affected downstream maintained views, Methods, Implementations,
   Observations, and assurance;
2. marks each affected downstream artifact potentially stale without mutating
   historical atoms;
3. routes required reconciliation to the artifact's owning layer; and
4. closes only when every affected currentness or assurance gate reaches its
   required disposition.

Refreshing a maintained view alone does not complete propagation. Downstream
implementation and assurance remain independently accountable. Feedback from
a later layer may create a new upstream Inquiry, but cannot rewrite upstream
authority or introduce a backward dependency.

## Primary claim

Accepted upstream change propagates potential staleness forward to every
affected owner without creating backward governance or treating one view
refresh as complete reconciliation.

## Rationale

The successor preserves the forward propagation invariant using the current
maintained-artifact vocabulary.
