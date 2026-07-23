+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-231"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-073"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET classifies governed artifacts through three independent axes: artifact_type = atomic | evergreen | maintained, content_role = to_be | why | how | as_is, and authority_origin = internal | external; actual project code is maintained + as_is + internal, while executable Tests and Evaluations are maintained + how + internal."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Revision semantics, lifecycle meaning, and authority origin are independent concerns; classifying realized code as current state and assurance implementations as checking mechanisms removes the overlapping phase-role, answer-to, and special Implementation-class model."

[scope]
kind = "layer"
id = "governance"

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "resolution_of"
target = "DSET-QUESTION-GOV-012"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-047"
+++

# Requirement — Classify artifacts through three independent axes

Every governed artifact has exactly one value on each canonical axis:

```toml
artifact_type = "atomic"       # atomic | evergreen | maintained
content_role = "to_be"         # to_be | why | how | as_is
authority_origin = "internal"  # internal | external
```

## Artifact type

- `atomic` is an immutable governed claim or observation.
- `evergreen` is a mutable semantic projection compiled from applicable active
  atoms.
- `maintained` is directly maintained material, including implementation,
  settings, documentation, dependencies, Tests, and Evaluations.

## Content role

- `to_be` defines the desired or required state.
- `why` explains or justifies a What or How artifact.
- `how` provides the path, mechanism, or check that turns or compares desired
  state with actual state.
- `as_is` is actual implementation or observed current state.

## Authority origin

- `internal` originates in or is owned by the project.
- `external` originates outside the project.

## Canonical implementation classifications

| Artifact | Artifact type | Content role | Authority origin |
|---|---|---|---|
| Actual project code | maintained | as_is | internal |
| Executable Test | maintained | how | internal |
| Executable Evaluation | maintained | how | internal |
| Test result | atomic | as_is | internal |
| Evaluation result | atomic | as_is | internal |
| Selected third-party library | maintained | how | external |
| Dependency declaration or lockfile | maintained | how | internal |
| Requirement | atomic | to_be | internal |
| Constraint | atomic | to_be | external |
| Rationale | atomic | why | internal or external |
| Current specification | evergreen | to_be | internal |

Test Plans and Evaluation Plans define intended checks; executable Test and
Evaluation implementations perform those checks; results record what was
observed. These remain distinct artifacts.

`relation_shape = standalone | relational` remains optional orthogonal
metadata and is not a fourth matrix dimension.
