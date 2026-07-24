+++
artifact_id = "DSET-ATOMIC-RECORD-004"
semantic_id = "DSET-REQUIREMENT-GOV-033"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "unknown"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Requirement — Inherit parent artifacts through child artifacts

Project, feature-group, feature, and layer artifacts may form an inheritance
tree using only `child_of` and `parent_to`.

A newly emitted local child records `child_of: <parent-id>`. Because atomic
artifacts are immutable, the parent is never edited when a later child appears;
`parent_to` is the derived reverse view of all active `child_of` links.

For a target feature or layer:

- when no local child exists, the nearest inherited parent applies directly;
- when a local child exists, the parent and child govern together unless the
  child's accepted directive explicitly replaces or cancels the parent in that
  local scope; and
- a local effect applies only to that scope and its descendants, never to its
  parent, ancestors, or siblings.

A child may be a local implementation Decision explaining how the parent is
implemented, or a local Decision cancelling the parent. No separate
`applies_to`, `realizes`, `implements`, or override relation is required for
inheritance. Multiple incompatible active children for the same parent and
scope stop as unresolved authority.

## Rationale

Structural inheritance gives every feature or layer an effective rule without
forcing boilerplate local copies. A single child link also permits an explicit
local implementation choice or cancellation while preserving the immutable
global artifact and unaffected sibling scopes.

This emitted Requirement atom is immutable. Later correction, absorption, or
retirement requires a new linked atom or append-only lifecycle event.
