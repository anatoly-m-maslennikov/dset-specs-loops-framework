---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-090"
scope_path:
  - "layer:gov"
priority: "high"
promotion:
  affected_children:
    - "governance"
    - "tool"
    - "skill"
    - "implementation"
    - "ops"
  applies_unchanged: true
  local_context_required: false
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "replacement_of"
    targets:
      - "DSET-REQUIREMENT-GOV-086"
  - type: "relates_to"
    targets:
      - "DSET-REQUIREMENT-GOV-087"
      - "DSET-REQUIREMENT-GOV-088"
      - "DSET-REQUIREMENT-GOV-089"
---

# Requirement — Axis-routed artifacts without a Type taxonomy

DSET routes every persisted governed artifact through:

```toml
revision_mode = "atomic"          # atomic | evergreen | maintained
content_role = "definition"       # inquiry | definition | rationale |
                                  # method | implementation | observation
governance_origin = "internal"    # internal | external
relation_shape = "standalone"     # standalone | relational
```

Every artifact also has one canonical `scope_path`, which supplies structural
ownership and selects a view over the routing matrix.

These fields are sufficient for routing, validation, lifecycle selection,
matrix placement, and project overview. DSET does not maintain a canonical
artifact Type or subtype taxonomy.

Human-facing names such as Requirement, Question, Test Plan, Evaluation Plan,
Problem, Commit, or Evidence may remain as optional labels, templates, views,
or interface vocabulary. They do not establish identity, routing, validation,
priority, authority, or lifecycle behavior.

A Relational artifact additionally declares:

- `relation_kind`;
- at least two typed, role-bearing endpoints;
- the independent origin of each endpoint.

Relation Kind is conditional relational semantics, not a global artifact Type.

`scope_path` remains a structural coordinate rather than a semantic routing
axis. It does not identify the Entity of Concern, declare applicability, or
establish a bounded semantic context.

The canonical model is:

```text
Route(
  revision_mode,
  content_role,
  governance_origin,
  relation_shape
)
@ scope_path
+ conditional relational metadata
```

## Primary claim

DSET routes governed artifacts through revision_mode, content_role, governance_origin, and relation_shape, plus structural scope_path, without a canonical artifact Type or subtype taxonomy.

## Rationale

Canonical Type and subtype names duplicate combinations already expressed by independent routing fields, create ontology growth, and allow labels to compete with the actual validation and workflow dimensions.
