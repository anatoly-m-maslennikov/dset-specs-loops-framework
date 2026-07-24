---
artifact_type: "test_plan"
artifact_id: "DSET-TEST-PLAN-GOV-053"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "check_of"
    targets:
      - "DSET-REQUIREMENT-GOV-063"
---

# Test Plan — Enforce the three-level priority vocabulary

Verify that:

- current settings declare exactly `high`, `medium`, and `low`;
- current and historical artifact metadata contains neither `critical` nor
  `deferred`;
- writers and priority lifecycle events reject both removed values;
- `highest` remains derived and cannot be stored;
- a meaning-preserving migration maps stored `critical` to `high`; and
- non-current work is represented in a named Version Roadmap rather than by a
  `deferred` priority.

## Primary claim

Verify that DSET stores and accepts only high, medium, or low priority, preserves highest as virtual-only, and routes future work to a Version Roadmap rather than deferred priority.

## Rationale

The vocabulary migration is complete only when settings, atoms, lifecycle events, writers, readers, fixtures, and current projections reject the removed labels consistently.
