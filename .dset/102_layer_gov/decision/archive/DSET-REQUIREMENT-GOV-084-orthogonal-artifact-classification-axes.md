+++
artifact_id = "DSET-ATOMIC-RECORD-242"
semantic_id = "DSET-REQUIREMENT-GOV-084"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET classifies every governed artifact through independent revision_mode, content_role, relation_shape, and governance_origin axes; scope_path remains structural addressing, OPS remains a layer rather than a content role, and relational artifacts express internal and external participation through typed endpoint origins."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "FPF strict-distinction, method-work, provenance, relational-precision, and anti-explosion principles require change semantics, semantic contribution, relational arity, governance origin, and structural scope to remain separate rather than being encoded in Type names or workflow stages."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-076"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-081"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-082"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-083"

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

# Requirement — Orthogonal artifact-classification axes

DSET uses four independent semantic-classification axes. A fifth field,
`scope_path`, supplies structural addressing without changing artifact
meaning.

## Revision mode

```toml
revision_mode = "atomic" # atomic | evergreen | maintained
```

- `atomic` — an immutable identified record or native immutable snapshot.
  Correction or changed meaning creates another artifact.
- `evergreen` — a mutable current projection derived, compiled, generated, or
  synchronized from declared governed inputs and rebuildable from them.
- `maintained` — a mutable primary artifact edited or operated directly by its
  governing owner.

The MECE boundary between Evergreen and Maintained is derived and rebuildable
versus directly maintained. An external artifact is not Evergreen merely
because it changes upstream.

## Content role

```toml
content_role = "definition"
# definition | rationale | method | implementation | observation
```

- `definition` — states intended, required, selected, or accepted conditions;
- `rationale` — explains why another claim, selection, or interpretation is
  justified;
- `method` — describes a reusable way, mechanism, procedure, or check;
- `implementation` — is an operative realization or asset;
- `observation` — records or reports what was observed, found, or produced.

Every artifact has one primary content role. File format, executability,
folder, layer, workflow stage, and carrier kind do not select it.

Tests and Evaluations are Method when they define reusable checks. Their dated
executions are work occurrences rather than another content role, and their
persisted results are Observation.

## Relation shape

```toml
relation_shape = "standalone" # standalone | relational
```

- `standalone` — the artifact's primary meaning does not require multiple
  typed endpoints;
- `relational` — the artifact's primary meaning requires at least two typed,
  directed endpoints.

Ordinary citations, provenance, or traceability links do not make an artifact
Relational. Relational artifacts declare the relation kind, endpoint roles,
direction, and endpoint origins.

## Governance origin

Standalone artifacts declare:

```toml
governance_origin = "internal" # internal | external
```

Governance origin identifies who controls the artifact's semantic content and
currentness. It does not by itself establish truth, authority, authorship,
storage location, or provenance.

Relational artifacts omit one artifact-level governance origin. Every endpoint
declares its own origin.

Origin is a qualifier, not a reason to create duplicate canonical Types.
Interfaces may show qualified display labels such as “external commit,” but
the qualifier does not create another semantic Type.

## Structural scope

`scope_path` identifies the project, layer, feature, feature group, or nested
combination that owns the artifact. It is an extensible structural address,
not a matrix axis and not semantic content.

OPS remains a layer value in `scope_path`; it is not a sixth content role:

| OPS concern | Content role |
|---|---|
| Deployment, release, readiness, or SLO condition | Definition |
| Reason for a deployment or recovery choice | Rationale |
| Deployment, rollback, runbook, Test, or Evaluation procedure | Method |
| CI/CD code, IaC, manifest, configuration, or instrumentation | Implementation |
| Deployment result, log, metric, incident, or support evidence | Observation |

A deployment procedure is Method, a deployment run is a dated work
occurrence, and its persisted result is Observation.

## Pull requests

A pull request is:

```toml
revision_mode = "maintained"
content_role = "method"
relation_shape = "relational"
```

It declares `source` and `target` endpoints:

| PR direction | Source origin | Target origin |
|---|---|---|
| Project PR | internal | internal |
| Inbound contribution | external | internal |
| Upstream contribution | internal | external |
| External PR reference | external | external |

The merge or squash commit is a separate Atomic Implementation. Immutable
proof of final PR state, when needed, is a separate Atomic Observation.

## Classification order

1. Recover the EntityOfConcern and one primary artifact job; split multi-head
   artifacts.
2. Assign `scope_path`.
3. Select `relation_shape`; for Relational artifacts, recover relation kind,
   endpoint roles, direction, and endpoint origins.
4. Select `content_role` from the artifact's primary contribution.
5. Select `revision_mode` from its change semantics.
6. For Standalone artifacts, select `governance_origin`.
7. Select the concrete Type and optional direct subtype from the admitted
   catalog.
8. Add provenance, evidence, and traceability without treating them as truth
   or authority.

No axis value is inferred from another. DSET does not force every Cartesian
cell to contain a Type. Concrete Type names, subtype definitions, and cell
occupancy are governed separately and are intentionally deferred from this
requirement.
