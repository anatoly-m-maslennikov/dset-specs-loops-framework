+++
artifact_id = "DSET-ATOMIC-RECORD-243"
semantic_id = "DSET-REQUIREMENT-GOV-085"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET has exactly three primary artifact axes: revision_mode, content_role, and scope_path; relation_shape and governance_origin remain orthogonal qualifying properties rather than axes of the artifact matrix."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Revision semantics, semantic contribution, and structural ownership form the useful artifact cube. Relational arity and governance origin refine an artifact within that cube but do not create additional semantic dimensions or duplicate Types."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-084"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-079"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-080"

[[relations]]
type = "relates_to"
target = "DSET-DECISION-OPS-013"
+++

# Requirement — Three primary artifact axes

DSET classifies artifacts in a three-dimensional cube:

1. `revision_mode`;
2. `content_role`;
3. `scope_path`.

Concrete Types occupy eligible cells in that cube. Type and optional direct
subtype are catalog selections after the three coordinates are known; they are
not additional axes.

## Revision mode

```toml
revision_mode = "atomic" # atomic | evergreen | maintained
```

- `atomic` — immutable identified record or native immutable snapshot;
- `evergreen` — mutable projection derived from declared governed inputs and
  rebuildable from them;
- `maintained` — mutable primary artifact edited or operated directly.

## Content role

```toml
content_role = "definition"
# definition | rationale | method | implementation | observation
```

- `definition` — intended, required, selected, or accepted conditions;
- `rationale` — reasons for a claim, selection, or interpretation;
- `method` — reusable way, mechanism, procedure, or check;
- `implementation` — operative realization or asset;
- `observation` — observed, found, or produced state.

Tests and Evaluations are Method when they define reusable checks. Their dated
executions are work occurrences, and persisted results are Observation.

## Scope path

`scope_path` is the owning project, feature group, feature, layer, or enabled
nested combination. It is extensible and follows narrowest-common-owner rules.

OPS is a layer in `scope_path`, not a Content Role. The same content roles
apply inside OPS:

- deployment or readiness condition — Definition;
- deployment rationale — Rationale;
- deploy, rollback, runbook, Test, or Evaluation procedure — Method;
- CI/CD, IaC, manifest, configuration, or instrumentation — Implementation;
- deployment result, log, metric, incident, or evidence — Observation.

## Qualifying properties

`relation_shape` is:

```toml
relation_shape = "standalone" # standalone | relational
```

It states whether the artifact's primary meaning requires at least two typed,
directed endpoints. Ordinary links do not make an artifact Relational.

`governance_origin` qualifies Standalone artifacts:

```toml
governance_origin = "internal" # internal | external
```

It states who controls semantic content and currentness, not truth, authority,
authorship, storage, or provenance. Relational artifacts omit one
artifact-level origin and declare origin on each endpoint.

Neither qualifier creates another canonical Type. Qualified display labels are
allowed for readability.

## Pull requests

A pull request occupies:

```toml
revision_mode = "maintained"
content_role = "method"
relation_shape = "relational"
```

Its `scope_path` is the narrowest common structural owner of the integration.
Its `source` and `target` endpoints independently declare internal or external
origin. This represents project, inbound, upstream, and external-reference PRs
without separate origin-derived Types.

The merge or squash commit is a separate Atomic Implementation. Immutable
proof of final PR state, when needed, is a separate Atomic Observation.

## Classification order

1. Recover one primary EntityOfConcern and artifact job.
2. Assign `scope_path`.
3. Assign `content_role`.
4. Assign `revision_mode`.
5. Assign `relation_shape` and, when Relational, its typed endpoints.
6. Assign Standalone `governance_origin` or Relational endpoint origins.
7. Select the concrete Type and optional direct subtype.
8. Add provenance, evidence, and traceability without converting them into
   truth or authority.

No primary axis is inferred from another. DSET does not force every cube cell
to contain a Type.
