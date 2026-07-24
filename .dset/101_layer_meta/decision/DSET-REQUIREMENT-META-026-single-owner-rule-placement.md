---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-META-026"
scope_path:
  - "layer:meta"
priority: "high"
promotion:
  affected_children:
    - "governance"
    - "tool"
    - "skill"
    - "implementation"
    - "operations"
  applies_unchanged: true
  local_context_required: false
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "relates_to"
    targets:
      - "DSET-REQUIREMENT-META-022"
      - "DSET-REQUIREMENT-META-025"
---

# Requirement — Place each claim with one owner

Every governed claim has exactly one authoritative owner. Place it in the
earliest layer that can define it completely while respecting the META
eligibility rule.

Downstream layers may reference, specialize, realize, check, or observe earlier
truth. They must not copy the claim into a second authority. Paths, filenames,
directory numbers, hubs, diagrams, generated views, evidence, and
implementation do not create authority by appearance.

If defining a proposed upstream rule requires entities owned only by a later
layer, the rule is misplaced. Move it to the earliest complete owner or split
the stable invariant from its downstream mechanism.

## Primary claim

Every governed claim has one authoritative owner and is placed in the earliest layer that can define it completely without importing later-layer concepts.

## Rationale

One owner and earliest-complete placement prevent duplicated truth, shadow governance, and upstream dependence on volatile realization details.
