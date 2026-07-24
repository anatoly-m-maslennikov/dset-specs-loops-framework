---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-039"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-GOV-037"
  - type: "replacement_of"
    targets:
      - "DSET-REQUIREMENT-GOV-035"
---

# Requirement — Select artifact-creation strictness in canonical settings

Root `dset_settings.toml` selects `medium` or `high` through
`artifacts.creation_strictness`; the default is `medium`.

At medium strictness, DSET requires clear authority, one primary claim,
semantic Type, owning scope, provenance, material links, priority, and
acceptance. Optional non-authoritative context may remain explicitly unknown.

At high strictness, DSET stops before emission while any material authority,
meaning, boundary, classification, scope, lineage, conflict, or proof question
remains ambiguous. It asks focused questions until the atom can safely remain
immutable.

Both levels assess one-step promotion eligibility. Promotion is proposed only
when the claim applies unchanged at the broader enabled scope and always
requires operator acceptance.

## Rationale

This successor preserves the admission and promotion policy while correcting
the retired settings carrier in active authority.

This emitted Requirement atom is immutable. Later correction requires a
successor and append-only lifecycle evidence.

## Primary claim

Atomic-artifact admission uses medium or high strictness selected by artifacts.creation_strictness in dset_settings.toml.

## Rationale

The admission behavior remains accepted, but the active authority must name the canonical settings carrier and key.
