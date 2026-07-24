---
artifact_type: "question"
artifact_id: "DSET-QUESTION-GOV-012"
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
  applies_unchanged: false
  local_context_required: true
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "relates_to"
    targets:
      - "DSET-REQUIREMENT-GOV-047"
---

# Question — Should artifact classification use three simple axes?

The candidate model has three independent axes:

```toml
artifact_type = "atomic" # atomic | evergreen | maintained
content_role = "to_be"   # to_be | why | how | as_is
authority_origin = "internal" # internal | external
```

The candidate meanings are:

- `atomic`: an immutable governed claim or observation;
- `evergreen`: a mutable semantic projection compiled from applicable active
  atoms;
- `maintained`: directly maintained project material, including actual
  implementation;
- `to_be`: the desired or required state;
- `why`: rationale or analysis supporting another artifact;
- `how`: the path or mechanism that turns desired state into actual state;
- `as_is`: actual implementation or observed current state;
- `internal`: authority or realization originating in the project; and
- `external`: authority or mechanism originating outside the project.

Representative classifications:

| Artifact | Artifact type | Content role | Authority origin |
|---|---|---|---|
| Requirement | atomic | to_be | internal |
| Constraint | atomic | to_be | external |
| Rationale | atomic | why | internal or external |
| Implementation Decision | atomic | how | internal |
| Current specification | evergreen | to_be | internal |
| Source code | maintained | as_is | internal |
| Selected third-party library | maintained | how | external |
| Dependency policy | atomic or evergreen | to_be | internal |
| Dependency declaration or lockfile | maintained | how | internal |
| Evidence Record | atomic | as_is | internal or external |

`relation_shape = standalone | relational` remains optional orthogonal
metadata rather than another matrix dimension.

## Primary claim

Should DSET replace the current artifact-classification axes with artifact_type = atomic | evergreen | maintained, content_role = to_be | why | how | as_is, and authority_origin = internal | external, treating actual code as maintained + as_is + internal and selected third-party libraries as maintained + how + external?

## Rationale

The proposed axes directly separate revision semantics, lifecycle meaning, and authority origin while eliminating overlapping phase-role and answer-to classifications and the special Implementation artifact class.
