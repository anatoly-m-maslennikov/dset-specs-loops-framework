---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-043
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-013"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-035"
---

# Requirement — Keep routing sparse without inverse uniqueness

Every registered artifact type and optional direct subtype maps to exactly one
Revision mode, Content role, and Governance locus. The inverse is not required:
several semantically distinct registered names may share the same route.

Internal governance is mandatory. External and relation governance are enabled
independently. Enabling a Governance locus does not require populating every
route, and an empty route requires no placeholder type or artifact.

A route supports dispatch and policy selection; it is not an ontology and does
not determine artifact identity by itself.

## Rationale

The earlier rule correctly rejected placeholder proliferation but incorrectly
required zero or one registered name per route. That collapsed independent
artifact meanings such as Problem, Evidence Record, and Verification merely
because they share atomic/observation/internal routing. Forward uniqueness
from a registered name to one route prevents ambiguity without imposing false
inverse uniqueness.
