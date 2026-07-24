---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-112
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-039"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-GOV-098"
      - "DSET-REQUIREMENT-GOV-102"
---

# Requirement — Gate atomic admission and promotion

`.dset/dset_settings.toml` selects `medium` or `high` through
`artifacts.creation_strictness`; the default is `medium`.

At medium strictness, DSET requires accepted authority, one primary claim, one
enabled artifact type, owning scope, creation provenance, material relations,
priority, and sufficient precision for the atom to remain immutable. Optional
non-authoritative context may remain explicitly unknown.

At high strictness, DSET stops before emission while any material authority,
meaning, boundary, classification, scope, lineage, conflict, or assurance
question remains ambiguous. It asks focused questions until the atom meets the
same immutable-record standard.

Both levels assess one-step promotion eligibility. Promotion is proposed only
when the claim applies unchanged at the broader enabled scope and always
requires explicit operator acceptance.

## Primary claim

Atomic admission uses medium or high project-selected strictness and always
checks, but never automatically performs, one-step scope promotion.

## Rationale

The successor preserves admission rigor and promotion advice while removing
obsolete carrier and lifecycle-event language.
