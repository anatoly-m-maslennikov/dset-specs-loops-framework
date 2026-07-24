---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-057
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-031"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-023"
      - "DSET-REQUIREMENT-META-026"
      - "DSET-REQUIREMENT-META-054"
---

# Requirement — Bound recursive self-hosting

DSET applies the same layer constitution and governance semantics to its own
repository while keeping reusable framework source, installed methodology, and
applied project truth under distinct owners.

The recursion terminates at a declared fixed point: the repository-local
applied authority selects a materialized methodology version, and that
methodology resolves without following a live reference back to its reusable
source or creating another governance owner.

## Rationale

The successor preserves self-application while correcting the former malformed
dependency reference and making the termination boundary explicit.
