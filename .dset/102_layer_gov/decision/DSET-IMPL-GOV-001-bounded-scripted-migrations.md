---
artifact_type: "implementation_decision"
artifact_id: "DSET-IMPL-GOV-001"
scope_path:
  - "layer:gov"
priority: "medium"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "relates_to"
    targets:
      - "DSET-REQUIREMENT-GOV-055"
---

# Implementation Decision — Bounded scripted migrations

A migration script must be scoped to named carriers or exact patterns, fail
when an expected source pattern is absent, and leave reviewable repository
diffs. It does not rewrite immutable atomic artifacts unless a separately
accepted carrier migration explicitly authorizes that transformation.

## Primary claim

Bounded deterministic Python scripts may perform mechanical content and filename migrations when their scope is explicit and the resulting diff is reviewed before commit.

## Rationale

Mechanical repository-wide migrations are less error-prone when one explicit transformation is applied consistently than when equivalent replacements are repeated manually.
