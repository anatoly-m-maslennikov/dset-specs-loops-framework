+++
artifact_id = "DSET-ATOMIC-RECORD-260"
semantic_id = "DSET-REQUIREMENT-META-027"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["project:dset-specs-loops-framework", "layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "An accepted upstream change propagates forward by marking affected downstream views, methods, implementations, and assurance potentially stale without mutating historical atoms."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Explicit forward invalidation preserves history while preventing downstream artifacts from appearing current after their governing assumptions change."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "operations"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-020"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-025"
+++

# Requirement — Propagate accepted change forward

When accepted authority changes in an earlier layer, DSET:

1. preserves every historical atomic record;
2. identifies affected downstream evergreen views, Methods, Implementations,
   Observations, and assurance;
3. marks those dependents potentially stale;
4. resumes the forward flow at the changed owner; and
5. restores currentness only after affected downstream gates are satisfied.

Refreshing an evergreen view alone does not complete propagation. Downstream
realization and assurance remain stale until their own owning criteria are met.
