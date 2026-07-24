---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-060
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-045"
      - "DSET-REQUIREMENT-META-046"
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-035"
      - "DSET-REQUIREMENT-META-041"
      - "DSET-REQUIREMENT-META-047"
      - "DSET-REQUIREMENT-META-051"
---

# Requirement — Keep the semantic route catalog total and one-to-one

Every possible combination of one Revision mode, one Content role, and one
Governance locus has exactly one canonical `artifact_type`.

No semantic route may be empty or occupied by multiple top-level types. Direct
subtypes may refine a canonical type but inherit its complete route and do not
create another top-level occupant.

## Primary claim

The semantic route catalog is total and one-to-one: each route has exactly one
canonical type.

## Rationale

The former occupancy and uniqueness atoms are inseparable halves of one
bijection requirement and therefore have one owner.
