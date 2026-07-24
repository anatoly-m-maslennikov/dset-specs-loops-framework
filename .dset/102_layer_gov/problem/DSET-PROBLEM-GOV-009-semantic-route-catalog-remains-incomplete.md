---
artifact_type: problem
artifact_id: DSET-PROBLEM-GOV-009
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-PROBLEM-GOV-008"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-035"
      - "DSET-REQUIREMENT-META-041"
      - "DSET-REQUIREMENT-META-070"
      - "DSET-REQUIREMENT-GOV-121"
---

# Problem — Semantic route catalog remains incomplete

META requires exactly one canonical Type for every combination of three
Revision modes, seven Content roles, and three Governance loci: 63 semantic
routes.

Current GOV authority names one internal, external, and relational Type for
each Content role, producing 21 named Types. Because each registered Type
resolves to exactly one Revision mode, the other 42 full routes have no
canonical Type.

The accepted role-and-locus matrix is therefore a valid partial naming surface
but not yet the total three-axis catalog required by META. Project settings and
validators cannot fail closed against a complete whitelist until GOV either
names the remaining routes or a new accepted META successor changes the
totality invariant.

## Primary claim

The current 21-Type GOV matrix leaves 42 of 63 required three-axis semantic
routes unnamed and therefore does not satisfy the active total-catalog
invariant.

## Rationale

The predecessor counted six Content roles and 54 routes and described an older
catalog. Assurance added a seventh role, while the accepted role-and-locus
matrix clarified 21 names without completing all Revision-mode variants.
