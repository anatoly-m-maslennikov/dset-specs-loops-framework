---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-045"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-GOV-044"
---

# Requirement — Keep layer authority forward-only

Features are peer capabilities. Their interactions are horizontal and use
explicit Contracts at the narrowest common structural owner. A feature does
not acquire authority over another feature merely because it calls it,
supplies data to it, or is delivered earlier.

Layers are ordered `META → GOV → TOOL → SKILL → OPS`. A layer may govern itself
and later layers, never an earlier layer. Direct influence on the immediately
following layer is preferred. A longer forward jump is allowed when explicit
and when an intermediate layer has no meaningful ownership to contribute.

Downstream artifacts may cite, depend on, implement, check, or evidence
upstream authority; this consumes earlier authority and does not reverse it.
Rule dependencies must therefore point to the same or an earlier layer, while
rule precedence may target only the same or a later layer. Backward authority
fails closed.

When a backward dependency cannot be deleted, re-homed, or resolved without
misrepresenting the system, DSET proposes reclassifying the coupled structural
owners as features and expressing their interaction through horizontal
Contracts. It never performs that structural transformation without operator
acceptance.

This Requirement atom is immutable. Later correction requires a successor and
append-only lifecycle event.

## Primary claim

Features are horizontal peers joined by Contracts, while DSET layers form a forward-only META to GOV to TOOL to SKILL to OPS authority chain with adjacent influence preferred and irreducible backward coupling proposed for feature reclassification.

## Rationale

Separating horizontal feature collaboration from ordered layer refinement prevents later implementation and operational concerns from silently governing earlier semantic or governance truth.
