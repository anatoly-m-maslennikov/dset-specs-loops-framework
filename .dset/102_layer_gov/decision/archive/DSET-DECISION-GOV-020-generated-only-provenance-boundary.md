---
artifact_type: "implementation_decision"
artifact_id: "DSET-DECISION-GOV-020"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "resolution_of"
    targets:
      - "DSET-DEFECT-GOV-007"
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-GOV-024"
---

# Decision — Exclude generated-only commits from derived relations

Commit-provenance validation continues to inspect every commit in the governed
range. The derived relation index, implementation coverage, traceability, and
health views include a commit relation only when that commit changes at least
one non-generated governed path.

A commit whose changed paths are all under a `generated/` directory is an
auditable refresh transaction, not a new implementation edge. A mixed commit
still participates because it contains substantive governed changes.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle event.

## Primary claim

Commit provenance remains mandatory for every governed commit, while generated-only commits are excluded from derived implementation relations and coverage inputs.

## Rationale

A generated mirror may carry provenance for auditability, but it cannot be an input to the semantic graph that generated the mirror.
