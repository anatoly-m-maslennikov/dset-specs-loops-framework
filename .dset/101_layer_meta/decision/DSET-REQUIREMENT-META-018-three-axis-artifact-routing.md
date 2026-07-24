+++
artifact_id = "DSET-ATOMIC-RECORD-250"
semantic_id = "DSET-REQUIREMENT-META-018"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET routes every governed artifact through exactly three independent semantic axes: revision_mode, content_role, and governance_locus; scope_path remains structural, registered names remain sparse interface vocabulary, and relational artifacts declare explicit endpoints."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "FPF E.24 warns against names and local frames creating a shadow ontology, A.6.P requires relations to expose their participants, and A.02.01 keeps contextual roles and optional slots explicit. A sparse three-axis route preserves these boundaries without recreating a Type hierarchy."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-090"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-091"
+++

# Requirement — Three-axis artifact routing

Every governed artifact declares exactly one value from each axis:

```toml
revision_mode = "atomic"       # atomic | evergreen | maintained
content_role = "definition"    # inquiry | definition | rationale |
                               # method | implementation | observation
governance_locus = "internal"  # internal | external | relation
```

The governance locus classifies the primary Entity of Concern:

- `internal` governs a project-owned non-relational subject;
- `external` governs an outside-owned non-relational subject through a
  project-owned carrier;
- `relation` governs a typed relation among explicit endpoints.

A relational artifact declares a stable `relation_kind` and at least two
role-bearing endpoints. Each endpoint independently declares internal or
external origin.

`scope_path` remains an independent structural coordinate. An occupied route
has at most one registered name, and each name maps to exactly one route. Names
do not infer routing, establish authority, or create a semantic hierarchy.

The routing matrix is intentionally sparse. Internal governance is mandatory;
external and relation governance are independently optional. Empty cells do
not require placeholder names or artifacts.

Authority, provenance, priority, lifecycle state, and applicability remain
explicit metadata outside the route.
