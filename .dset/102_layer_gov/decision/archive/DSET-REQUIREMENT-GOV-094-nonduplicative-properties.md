---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-094
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-012"
      - "DSET-REQUIREMENT-META-013"
      - "DSET-REQUIREMENT-GOV-093"
---

# Requirement — Give every property one meaning

An artifact property section contains no two properties that express the same
meaning and no property whose value is deterministically derived from another
canonical property, the artifact catalog, the current project, or repository
placement.

The artifact type and optional subtype determine their registered route.
Therefore Markdown frontmatter does not repeat `revision_mode`,
`content_role`, or `governance_locus`. Atomic artifacts do not carry an
acceptance status: creation follows explicit acceptance, while archive
placement represents removal from active authority.

Project identity is ambient. Internal acceptance does not require a repeated
operator-authority property. External origin uses a precise source reference,
issuer, or relation endpoint instead of a generic authority string.

Repeated relations of the same kind use one non-empty `targets` array.
Relations with different roles, qualifiers, or meanings remain separate.

## Rationale

Redundant properties can disagree and create competing sources of truth.
Derived values belong in deterministic resolution and validation, not in every
artifact carrier.
