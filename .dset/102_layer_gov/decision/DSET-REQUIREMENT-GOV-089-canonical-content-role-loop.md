+++
artifact_id = "DSET-ATOMIC-RECORD-247"
semantic_id = "DSET-REQUIREMENT-GOV-089"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET uses the canonical content-role loop Inquiry to Definition to Rationale to Method to Implementation to Observation to new Inquiry."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The loop separates uncertainty, intended truth, justification, reusable approach, operative realization, and observed state while making feedback explicitly recursive."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-086"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-087"
+++

# Requirement — Canonical Content Role loop

DSET uses this canonical semantic loop:

```text
Inquiry
  -> Definition
  -> Rationale
  -> Method
  -> Implementation
  -> Observation
  -> Inquiry
  -> ...
```

- Inquiry identifies unresolved knowledge, choice, or clarification.
- Definition establishes the intended, required, selected, or accepted state.
- Rationale explains why the Definition or its interpretation is justified.
- Method describes the reusable way to realize or check the Definition.
- Implementation is the operative realization.
- Observation records what was actually found, measured, or produced.
- Observation exposes new uncertainty or discrepancy and starts another
  Inquiry.

The loop orders successor roles. It does not mutate one artifact through
multiple roles: each artifact keeps one primary Content Role. One artifact may
produce multiple successors, and a role may be omitted when its own entry
criteria say that no persisted artifact is necessary.
