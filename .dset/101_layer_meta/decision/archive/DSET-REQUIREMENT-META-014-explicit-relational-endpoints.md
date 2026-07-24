---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-META-014"
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

# Requirement — Explicit relational endpoints

Endpoint origin is a qualifier of each endpoint, not another artifact-routing
axis. A relational name or suffix cannot replace the endpoint record.

## Primary claim

An artifact with relation governance declares a stable relation kind and at least two role-bearing endpoints whose internal or external origins are explicit.

## Rationale

Endpoint-explicit relations preserve polarity, participants, and boundary meaning without encoding them in artifact names.
