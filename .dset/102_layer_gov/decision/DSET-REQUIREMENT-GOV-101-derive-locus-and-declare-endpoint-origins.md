---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-101
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-088"
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-014"
      - "DSET-REQUIREMENT-META-035"
      - "DSET-REQUIREMENT-META-038"
---

# Requirement — Derive locus and declare endpoint origins

Each registered artifact type and optional direct subtype derives exactly one
`governance_locus`: `internal`, `external`, or `relation`. Artifact carriers do
not repeat the derived locus or store a separate `governance_origin` property.

A relational artifact declares one stable relation kind and at least two
typed, role-bearing endpoints. Each endpoint independently declares whether its
participant is internal or external relative to the current project boundary.
Direction follows from the relation kind and endpoint roles.

Endpoint origin does not become another artifact-routing axis and cannot be
inferred from the relation carrier's locus. External provenance, issuer, source,
or ownership facts use their precise type-specific properties rather than a
generic duplicate origin field.

## Primary claim

Artifact Governance locus is derived from registered type, while every
relational endpoint declares its own internal or external origin.

## Rationale

The rule preserves the participant information needed for contracts and pull
requests without storing a second artifact-level coordinate that duplicates the
type-derived route.
