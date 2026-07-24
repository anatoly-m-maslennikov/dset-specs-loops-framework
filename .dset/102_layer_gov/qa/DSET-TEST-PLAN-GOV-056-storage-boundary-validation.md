---
artifact_type: test_plan
artifact_id: DSET-TEST-PLAN-GOV-056
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-TEST-PLAN-GOV-048"
  - type: check_of
    targets:
      - "DSET-REQUIREMENT-GOV-111"
---

# Test Plan — Validate storage boundaries

## Controlled checks

1. Persist governed authority only under `.dset`.
2. Append journal records only as complete NDJSON lines under
   `.dset_journal`.
3. Remove `.dset_runtime` after a completed workflow and prove governed truth
   and journal history remain intact.
4. Create scratch under the host temporary root, force success and handled
   failure, and prove cleanup in both cases.
5. Reject repository-local scratch and any attempt to keep the only governed
   copy in runtime or scratch.

## Expected disposition

Every boundary accepts only its governed content, and cleanup cannot remove
authority or journal history.
