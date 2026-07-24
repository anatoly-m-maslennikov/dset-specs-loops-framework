---
artifact_type: implementation_decision
artifact_id: DSET-IMPL-GOV-006
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-DECISION-GOV-020"
  - type: resolution_of
    targets:
      - "DSET-DEFECT-GOV-007"
---

# Implementation Decision — Exclude generated-only implementation edges

Commit-provenance validation inspects every commit in the governed range. A
commit contributes an implementation relation, implementation coverage, or
semantic traceability edge only when it changes at least one non-generated
governed path.

A generated-only commit is an auditable refresh transaction. It retains its
required provenance but cannot become an implementation input to the semantic
graph that produced the generated carrier. A mixed commit participates because
it includes a substantive governed change.

## Primary claim

Generated-only commits retain provenance but do not create implementation
relations or implementation-coverage credit.

## Rationale

This preserves auditability without allowing a derived view to prove or
implement its own source authority.
