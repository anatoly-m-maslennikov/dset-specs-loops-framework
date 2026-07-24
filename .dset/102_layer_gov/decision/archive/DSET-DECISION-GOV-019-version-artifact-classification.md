---
artifact_type: "implementation_decision"
artifact_id: "DSET-DECISION-GOV-019"
scope_path:
  - "layer:gov"
priority: "high"
promotion:
  affected_children:
    - "meta"
    - "gov"
    - "tool"
    - "skill"
    - "ops"
  applies_unchanged: false
  local_context_required: true
  parent_scope:
    kind: "project"
    id: "dset-specs-loops-framework"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "replacement_of"
    targets:
      - "DSET-DECISION-GOV-012"
  - type: "relates_to"
    targets:
      - "DSET-DECISION-OPS-007"
---

# Decision — Classify release lifecycle artifacts as Version

The canonical artifact registry uses the primary Type `version` for Roadmap,
Version Scope, Change, Release Plan, Readiness Record, and Release Record.
Those six direct subtypes remain flat. Default type-bearing artifact IDs and
filenames use `VERSION`.

Current schemas, templates, examples, validation, settings documentation,
generated views, and active carriers must not accept or emit `delivery` as an
artifact Type. Ordinary prose may still use the English word “delivery” for a
development flow, deployment, message transport, or historical evidence when
it is not naming the governed Type.

This Decision completely replaces `DSET-DECISION-GOV-012` and is the
classification sibling of `DSET-DECISION-OPS-007`, which owns the unchanged
release-lifecycle behavior.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle event.

## Primary claim

The artifact registry classifies the six release-lifecycle roles under the primary Version artifact Type, never Delivery.

## Rationale

Version identifies the governed artifact subject without requiring readers to distinguish DSET's prior use of Delivery from deployment or workflow delivery.
