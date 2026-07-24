---
artifact_type: implementation_decision
artifact_id: DSET-IMPL-GOV-009
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-IMPL-GOV-003"
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-035"
      - "DSET-REQUIREMENT-GOV-071"
---

# Implementation Decision — Derive identity kind from the registered route

Each governed artifact declares one enabled canonical artifact type and, when
the catalog permits it, one direct subtype. That classification resolves to
exactly one semantic route and one visible identity kind.

Artifact IDs and filenames use the catalog's identity kind for the canonical
type, or the enabled subtype identity kind when project settings explicitly
select subtype-bearing names. No parallel parent-family hierarchy or hardcoded
type table determines identity.

A vocabulary change is a governed whole-graph migration: identifiers,
filenames, headings, and stored references change together, and superseded
aliases cease to be valid after cutover.

## Primary claim

Artifact identity kinds are derived from the single registered route
classification rather than a parallel or hardcoded type hierarchy.

## Rationale

The successor retains direct, readable identities without freezing exploratory
type names into implementation authority.
