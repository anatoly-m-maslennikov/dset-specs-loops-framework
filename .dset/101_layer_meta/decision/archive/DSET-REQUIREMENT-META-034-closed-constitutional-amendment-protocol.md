---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-META-034"
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
      - "DSET-REQUIREMENT-META-021"
      - "DSET-REQUIREMENT-META-022"
      - "DSET-REQUIREMENT-META-027"
      - "DSET-REQUIREMENT-META-031"
---

# Requirement — Close constitutional amendments

A semantic change to META is not complete when prose is edited. It is complete
only after the project can replay why the change was accepted, what it affects,
how its authority propagated, and why the resulting state is coherent.

The required sequence is:

1. explore the candidate without creating governed artifacts;
2. obtain explicit operator acceptance and create one atomic META claim per
   primary claim, with rationale;
3. map affected invariants, entities, layer boundaries, handoffs, profiles,
   governance surfaces, implementations, and assurance;
4. confirm META eligibility, single ownership, topological definitions, and an
   acyclic layer graph;
5. update the root evergreen META view with direct atomic provenance;
6. propagate potential staleness forward to every affected active descendant;
7. verify META self-application and each affected downstream handoff; and
8. declare a fixed point only when all affected active surfaces are Current or
   explicitly deactivated and no unresolved conflict is concealed.

Failure never permits editing the accepted atomic claim. A correction or
changed meaning creates a successor atomic record. An authorized withdrawal
archives the atom, records the future intention in the applicable Version
artifact when needed, and leaves every affected view Stale until reconciled.

## Primary claim

Every semantic change to META follows a closed amendment protocol from Exploration and explicit acceptance through impact mapping, eligibility and topology review, reasoned evergreen update, forward staleness propagation, verification, and fixed-point declaration.

## Rationale

A constitution that governs its own evolution needs a replayable amendment boundary; otherwise a valid local edit can silently change downstream meaning, lose rationale, or create backward governance.
