---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-035
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-012"
      - "DSET-REQUIREMENT-META-018"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-013"
      - "DSET-REQUIREMENT-GOV-094"
---

# Requirement — Derive artifact routes from registered types

Every governed artifact declares one registered `artifact_type` and, only when
needed, one direct `artifact_subtype`. That canonical type pair maps to exactly
one Revision mode, Content role, and Governance locus.

Artifact carriers do not repeat `revision_mode`, `content_role`, or
`governance_locus`. Writers and validators resolve them from the registered
type pair and fail closed when the pair is unknown, disabled, or ambiguous.

`scope_path` remains an explicit project-relative structural coordinate outside
the route. Priority, provenance, applicability, relation endpoints, and
type-specific facts remain separate when they cannot be derived.

## Rationale

Storing both a type and its deterministic route creates two writable
representations of one meaning. A single registered mapping preserves the
three-axis model while preventing metadata drift.
