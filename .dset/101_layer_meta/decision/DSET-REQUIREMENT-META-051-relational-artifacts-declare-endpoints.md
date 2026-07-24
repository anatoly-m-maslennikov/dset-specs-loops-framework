---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-051
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-014"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-035"
      - "DSET-REQUIREMENT-META-045"
---

# Requirement — Make relational endpoints explicit

An artifact routed to relational governance declares one stable relation kind
and at least two role-bearing endpoints. Each endpoint independently declares
whether its participant is internal or external.

Endpoint origin is not another semantic routing axis. Ordinary citations,
traceability links, and relations among otherwise standalone artifacts do not
change their Governance locus.

## Rationale

Explicit participants keep a governed boundary distinguishable from an
ordinary link and prevent a relation's meaning from being encoded only in its
name or carrier location.
