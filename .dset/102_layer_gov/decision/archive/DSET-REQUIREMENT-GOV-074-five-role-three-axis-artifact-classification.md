---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-074"
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
      - "DSET-REQUIREMENT-GOV-073"
---

# Requirement — Use five content roles across three artifact axes

Every governed artifact has exactly one value on each canonical axis:

```toml
artifact_type = "atomic"       # atomic | evergreen | maintained
content_role = "definition"    # definition | rationale | method | implementation | observation
authority_origin = "internal"  # internal | external
```

The artifact types mean:

- `atomic`: an immutable governed claim or observation;
- `evergreen`: a mutable semantic projection compiled from applicable active
  atoms; and
- `maintained`: directly maintained material, including code, settings,
  documentation, dependencies, Tests, and Evaluations.

The content roles mean:

- `definition`: desired, required, or accepted state;
- `rationale`: reasoning that explains or justifies another artifact;
- `method`: the path, mechanism, dependency, or check used to achieve or
  evaluate a definition;
- `implementation`: realized project assets; and
- `observation`: evidence, findings, results, and conclusions about actual
  state.

The authority origins mean:

- `internal`: originates in or is owned by the project; and
- `external`: originates outside the project.

Canonical implementation classifications include:

| Artifact | Artifact type | Content role | Authority origin |
|---|---|---|---|
| Actual project code | maintained | implementation | internal |
| Executable Test | maintained | method | internal |
| Executable Evaluation | maintained | method | internal |
| Test result | atomic | observation | internal |
| Evaluation result | atomic | observation | internal |
| Selected third-party library | maintained | method | external |
| Dependency declaration or lockfile | maintained | method | internal |
| Requirement | atomic | definition | internal |
| Constraint | atomic | definition | external |
| Rationale | atomic | rationale | internal or external |
| Current specification | evergreen | definition | internal |

Tests and Evaluations are maintained checking mechanisms. Their results are
immutable observations. Actual code is the maintained implementation being
checked.

`relation_shape = standalone | relational` is optional orthogonal metadata,
not a fourth matrix dimension. Contract, Conflict, Gap, Defect, and
Verification commonly use `relational` because their primary meaning requires
explicitly related subjects.

## Primary claim

DSET classifies governed artifacts through artifact_type = atomic | evergreen | maintained, content_role = definition | rationale | method | implementation | observation, and authority_origin = internal | external; relation_shape = standalone | relational remains optional orthogonal metadata.

## Rationale

The five content roles distinguish desired truth, reasoning, mechanisms, realized project assets, and observations without overlapping phase-role and answer-to axes or conflating code with Test and Evaluation results.
