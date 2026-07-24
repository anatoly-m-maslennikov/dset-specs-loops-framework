---
artifact_type: test_plan
artifact_id: DSET-TEST-PLAN-GOV-059
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-TEST-PLAN-GOV-053"
  - type: check_of
    targets:
      - "DSET-REQUIREMENT-GOV-107"
---

# Test Plan — Validate effective-priority selection

## Controlled checks

1. Accept only stored `high`, `medium`, or `low`.
2. Reject stored `highest`, `critical`, and `deferred`.
3. Apply the strict-ancestor and earlier-layer increments independently and
   together, capped at virtual `highest`.
4. Confirm `ask_always` always asks.
5. Confirm `auto_by_effective_priority` selects exactly one unique eligible
   winner and asks on ties, incomparable scopes, uncertainty, or multiple
   winners.
6. Confirm unsatisfiable external obligations stop rather than auto-resolve.

## Expected disposition

Every comparison produces the governed effective priorities and never guesses
through a non-unique or ineligible result.
