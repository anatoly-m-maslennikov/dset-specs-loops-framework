---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-054"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-GOV-030"
---

# Requirement — Subtype-bearing atomic filenames

For newly emitted atomic artifacts in this repository, the semantic ID and
filename use the selected direct Decision subtype token: `REQUIREMENT`, `CONSTRAINT`,
`CONTRACT`, or `IMPL`. An empty-subtype Decision continues to use `DECISION`.

The project setting enables this naming form. It never renames or mutates an
existing atom, and readers continue to resolve long-form historical kinds as
compatibility input.

## Primary claim

This project enables subtype-bearing names for newly emitted atomic artifacts so the REQUIREMENT, CONSTRAINT, CONTRACT, or IMPL kind is visible in the file list, while immutable existing names remain unchanged.

## Rationale

The compact subtype tokens make atomic project authority distinguishable during filesystem browsing without requiring the reader to open every carrier.
