---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-066
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-022"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-026"
      - "DSET-REQUIREMENT-META-065"
---

# Requirement — Apply the META eligibility rule

A rule belongs in META only when all three conditions hold:

1. it remains true when downstream languages, tools, hosts, providers, and
   repository layouts change;
2. it governs multiple layers or defines a boundary between layers; and
3. it can be stated without importing downstream implementation concepts.

If any condition fails, place the rule in the earliest downstream layer that
can own it completely. META owns the invariant; that layer owns the mechanism.

For example, META may require durable changes to be traceable. GOV owns the
carrier and provenance policy, while IMPL owns applicable executable
enforcement. META must not absorb either mechanism merely because several
later layers use it.

## Primary claim

META owns only invariants that remain valid across downstream technologies,
govern multiple layers or a layer boundary, and can be stated without importing
downstream implementation vocabulary.

## Rationale

The predecessor's invariant remains correct, but its example and applicability
metadata used retired TOOL and SKILL layers. The successor preserves one
technology-independent eligibility rule under the current topology.
