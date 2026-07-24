---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-046
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-035"
      - "DSET-REQUIREMENT-META-045"
---

# Requirement — Keep every semantic route occupied

Every possible combination of one Revision mode, one Content role, and one
Governance locus has one registered canonical `artifact_type`.

Empty semantic routes are forbidden. Because the current axes define three
Revision modes, six Content roles, and three Governance loci, the canonical
catalog must contain exactly 54 top-level artifact types with 54 distinct
routes.

Optional direct subtypes may refine those types later, but neither subtype
availability nor project settings may remove a canonical route from the
framework catalog. A project may disable use of a type without making its
framework route undefined.

## Rationale

Total route coverage makes the classifier closed and deterministic. Any
governed artifact can be routed without inventing an ad hoc type, overloading a
neighboring route, or treating an unoccupied coordinate as an undefined case.
