---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-META-013"
scope_path:
  - "layer:meta"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-META-018"
---

# Requirement — Sparse routing matrix

Internal governance is mandatory. External and relation governance are enabled
independently. Enabling a locus does not require filling every route.

## Primary claim

The routing matrix is sparse: an occupied route has zero or one registered name at each enabled governance locus, and empty routes require no placeholder artifacts.

## Rationale

Sparse interface vocabulary avoids ontology and artifact proliferation while preserving precise routing.
