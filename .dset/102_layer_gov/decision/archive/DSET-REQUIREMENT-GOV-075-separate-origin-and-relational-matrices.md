+++
artifact_id = "DSET-ATOMIC-RECORD-233"
semantic_id = "DSET-REQUIREMENT-GOV-075"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET presents artifact type, content role, and internal or external authority origin in the primary classification matrix, and presents relational or between-subject semantics only in a separate relation-shape matrix."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Authority origin and relational shape are orthogonal: a Contract or Conflict may relate several subjects while its governing artifact still has an internal or external origin."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-074"
+++

# Requirement — Separate origin and relational matrices

The primary classification matrix has:

- artifact type as rows;
- content role as columns; and
- `internal | external` authority origin inside each cell.

It contains no shared, between, or relational ownership category.

A separate relational matrix identifies artifacts whose primary meaning
requires explicit endpoints. That matrix records endpoint roles without
changing the artifact's independent internal or external authority origin.

Contract, Conflict, Gap, Defect, Verification, Rationale, checks, Evidence
Records, and dependency selections may use the relational matrix when their
primary claim requires two or more subjects.
