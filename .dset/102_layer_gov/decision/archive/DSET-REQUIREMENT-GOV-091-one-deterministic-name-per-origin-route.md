---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-091"
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
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-GOV-090"
---

# Requirement — One deterministic name per origin route

Every admitted route has exactly one internal name and one external name.

The name is derived from the complete route:

```text
<Governance Origin> <Revision Mode> <Content Role> <Artifact | Relation>
```

Examples:

```text
Internal Atomic Definition Artifact
External Atomic Definition Artifact
Internal Maintained Method Relation
External Evergreen Observation Artifact
```

The origin word is selected only from `Internal` or `External`. The final word
is selected only from `Artifact` or `Relation`.

Route names are deterministic display outputs. They are not stored Types,
subtypes, aliases, routing inputs, identity authorities, or lifecycle owners.

## Primary claim

Every admitted artifact route has exactly one deterministic internal name and one deterministic external name; route names are derived display outputs rather than artifact Types.

## Rationale

One name per governance origin keeps interfaces readable without recreating a competing Type taxonomy or allowing aliases to affect routing.
