---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-103
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-079"
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-035"
      - "DSET-REQUIREMENT-GOV-101"
---

# Requirement — Distinguish internal and external Git commits

An internal project commit uses artifact type `git_commit` and derives the route
`atomic / implementation / internal`.

An outside-owned commit governed as an external input uses artifact type
`external_git_commit` and derives the route
`atomic / implementation / external`.

Both types use the repository-qualified native commit SHA as identity rather
than a DSET artifact sequence. Precise repository, author, signer, and source
facts remain provenance. They do not replace the type-derived Governance locus.

## Primary claim

Internal and external Git commits use separate registered artifact types so
each type derives exactly one Governance locus.

## Rationale

Distinct names preserve the one-type-to-one-route invariant while retaining the
native identity and provenance required to trace internal and outside-owned
implementation records.
