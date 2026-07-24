---
artifact_type: test_plan
artifact_id: DSET-TEST-PLAN-GOV-054
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-TEST-PLAN-GOV-036"
  - type: check_of
    targets:
      - "DSET-IMPL-GOV-004"
---

# Test Plan — Validate the canonical relation vocabulary

## Controlled checks

1. Admit one valid example of every registered relation kind.
2. Reject an unknown relation kind.
3. Reject a relation without the endpoint cardinality required by its kind.
4. Resolve every target by active identity and reject zero or multiple active
   matches.
5. Confirm an archived target remains addressable as history but does not
   become active authority.

## Expected disposition

All valid examples pass and every invalid fixture fails with the exact relation
and endpoint identified.
