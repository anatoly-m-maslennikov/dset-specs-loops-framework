---
artifact_type: test_plan
artifact_id: DSET-TEST-PLAN-GOV-060
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-TEST-PLAN-GOV-045"
  - type: check_of
    targets:
      - "DSET-IMPL-GOV-006"
---

# Test Plan — Validate the generated-only provenance boundary

## Controlled checks

1. Validate required provenance on substantive, generated-only, and mixed
   commits.
2. Include substantive and mixed commits in derived implementation relations
   and coverage.
3. Exclude generated-only commits from those relations and coverage.
4. Confirm generated-only commits remain visible in Git audit history.
5. Reject a generated carrier that cites itself as its semantic input.

## Expected disposition

All commits retain auditable provenance, while only commits with at least one
non-generated governed change contribute implementation edges.
