---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-068
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-025"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-052"
      - "DSET-REQUIREMENT-META-059"
      - "DSET-REQUIREMENT-META-065"
      - "DSET-REQUIREMENT-META-067"
---

# Requirement — Keep current layer dependencies acyclic

The ordered layer graph is a directed acyclic graph:

- authority and refinement flow
  `META → GOV → SPEC → PROFILES → IMPL → OPS`;
- a later layer may consume authority from its own or any earlier layer;
- no layer may govern or redefine an earlier layer;
- dependency is distinct from scope specialization and `child_of`; and
- peer scopes interact through explicit Contracts rather than layer
  precedence.

An Observation from a later layer may become input to Exploration Mode. After
explicit acceptance, the result enters the normal forward flow at its proper
owning layer. This feedback is not a backward authority edge.

If backward coupling cannot be deleted, re-homed, or expressed as feedback,
DSET proposes remodeling the coupled owners as horizontal scopes or features.
The operator must accept that structural change.

## Primary claim

DSET layer dependencies form an acyclic graph in which authority and
refinement follow the current layer order, later layers consume earlier
authority, and feedback cannot create backward governance.

## Rationale

The predecessor's dependency invariant remains correct, but its concrete layer
sequence and applicability metadata described the retired TOOL and SKILL
topology.
