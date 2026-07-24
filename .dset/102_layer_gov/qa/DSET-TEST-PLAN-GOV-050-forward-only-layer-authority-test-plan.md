---
artifact_type: "test_plan"
artifact_id: "DSET-TEST-PLAN-GOV-050"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "check_of"
    targets:
      - "DSET-REQUIREMENT-GOV-045"
---

# Test Plan — Reject backward layer authority

Prove that the governance registry accepts same-layer and forward authority,
including explicit longer forward influence, while rejecting:

1. a rule that depends on a rule from a later layer; and
2. a rule that declares precedence over a rule from an earlier layer.

Also prove that the canonical and materialized governance profiles contain no
backward authority edges and that the project architecture map renders the
ordered layer chain. A detected backward edge must propose resolving or
re-homing it and, when irreducible, reclassifying the peers as features with
horizontal Contracts; the validator must not transform structure itself.

This Test atom is immutable. Later correction requires a successor Test and
append-only lifecycle event.

## Primary claim

Deterministic validation rejects rule dependencies and precedence that create backward authority across the ordered DSET layers.
