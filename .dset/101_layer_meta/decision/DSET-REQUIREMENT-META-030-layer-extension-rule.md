+++
artifact_id = "DSET-ATOMIC-RECORD-263"
semantic_id = "DSET-REQUIREMENT-META-030"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["project:dset-specs-loops-framework", "layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "A proposed DSET layer is admitted only when it has one non-overlapping responsibility, explicit predecessor and successor handoffs, and preserves the acyclic layer graph."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "An explicit admission test keeps the layer model extensible without allowing every profile, feature, or organizational preference to become a new layer."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "operations"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-024"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-025"
+++

# Requirement — Govern layer extensions

A candidate layer must declare:

- one responsibility not already owned by another layer;
- its predecessor and successor;
- accepted inputs and produced outputs;
- entry, exit, and failure behavior;
- its dependency direction; and
- why a feature, profile, Work Area, or ordinary scope cannot own the concern.

The candidate is admissible only when the resulting graph remains acyclic and
existing responsibilities remain non-overlapping. Otherwise, model it using
the appropriate horizontal or scoped structure rather than adding a layer.
