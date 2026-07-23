# Artifact classification rules

**Rule ID:** `DSET-RULE-ARTIFACT-CLASSIFICATION`

## Purpose

DSET classifies every governed artifact through exactly three primary axes:
Revision Mode, Content Role, and Scope Path.

Concrete Type and subtype definitions are governed separately. A Type occupies
an eligible cell in this three-dimensional artifact cube; the axes are not
themselves Types.

## Revision mode

`revision_mode` declares how the artifact changes:

| Value | Definition |
|---|---|
| `atomic` | Immutable identified record or native immutable snapshot; correction or changed meaning creates another artifact |
| `evergreen` | Mutable current projection derived, compiled, generated, or synchronized from declared governed inputs and rebuildable from them |
| `maintained` | Mutable primary artifact edited or operated directly by its governing owner |

The boundary between Evergreen and Maintained is derived and rebuildable versus
directly maintained. Mutable alone does not mean Evergreen. An external
artifact is not Evergreen merely because it changes upstream.

## Content role

`content_role` declares the artifact's one primary contribution:

| Value | Definition |
|---|---|
| `definition` | States intended, required, selected, or accepted conditions |
| `rationale` | Explains why another claim, selection, or interpretation is justified |
| `method` | Describes a reusable way, mechanism, procedure, or check |
| `implementation` | Is an operative realization or asset |
| `observation` | Records or reports what was observed, found, or produced |

File format, executability, folder, layer, workflow stage, and carrier kind do
not select the role.

Tests and Evaluations are Method when they define reusable checks. A dated
execution is a work occurrence rather than another content role. Its persisted
result is Observation.

## Scope path

`scope_path` is an extensible structural address composed from enabled project,
feature-group, feature, layer, and future structural dimensions. It supplies
the third primary coordinate and follows narrowest-common-owner rules.

Scope Path never determines Revision Mode, Content Role, Type, subtype, or any
qualifying property.

OPS is a layer in `scope_path`, not a Content Role:

| OPS concern | Content role |
|---|---|
| Deployment, release, readiness, or SLO condition | `definition` |
| Reason for a deployment or recovery choice | `rationale` |
| Deployment, rollback, runbook, Test, or Evaluation procedure | `method` |
| CI/CD code, IaC, manifest, configuration, or instrumentation | `implementation` |
| Deployment result, log, metric, incident, or support evidence | `observation` |

A deployment procedure is Method, a deployment run is a dated work occurrence,
and the persisted result is Observation.

## Qualifying properties

Relation Shape and Governance Origin refine an artifact inside the
three-dimensional cube. They are not additional primary axes.

### Relation shape

`relation_shape` declares the artifact's inherent semantic arity:

| Value | Definition |
|---|---|
| `standalone` | Primary meaning does not require multiple typed endpoints |
| `relational` | Primary meaning requires at least two typed, directed endpoints |

An ordinary citation, provenance field, or traceability link does not make an
artifact Relational. A Relational artifact declares its relation kind,
endpoint roles, direction, and endpoint origins.

Relational and Standalone artifacts use the same three primary axes. Separate
renderings may improve readability, but they do not create different
classification systems.

### Governance origin

A Standalone artifact declares:

```toml
governance_origin = "internal" # internal | external
```

Governance Origin identifies who controls the artifact's semantic content and
currentness. It does not establish truth, project authority, authorship,
storage location, or provenance.

A Relational artifact has no single Governance Origin. Each endpoint declares
its own `origin = "internal"` or `origin = "external"`.

Origin qualifies a Type; it does not create a second canonical Type. A UI may
show an origin-qualified label for readability without changing catalog
identity.

## Pull-request direction

A pull request demonstrates the Relational boundary:

```toml
revision_mode = "maintained"
content_role = "method"
relation_shape = "relational"
```

It has `source` and `target` endpoints:

| Direction | Source origin | Target origin |
|---|---|---|
| Project PR | internal | internal |
| Inbound contribution | external | internal |
| Upstream contribution | internal | external |
| External PR reference | external | external |

The merge or squash commit is a separate Atomic Implementation. Immutable
proof of final PR state, when required, is a separate Atomic Observation.

## Classification order

1. Recover the EntityOfConcern and one primary artifact job. Split a
   multi-head artifact.
2. Assign `scope_path`.
3. Select `content_role` from the primary contribution.
4. Select `revision_mode` from the change semantics.
5. Select `relation_shape`. For a Relational artifact, recover the relation
   kind, endpoint roles, direction, and endpoint origins.
6. For a Standalone artifact, select `governance_origin`.
7. Select one admitted concrete Type and at most one direct subtype.
8. Add provenance, evidence, and traceability without treating them as truth
   or authority.

No primary-axis value is inferred from another. Classification never derives
meaning from a filename, workflow, host, tool, or next action. DSET does not
force every cube cell to contain a Type.

## Matrix rendering

Each `scope_path` selects one two-dimensional matrix slice. The slice uses
Revision Mode as rows and Content Role as columns. Standalone views may qualify
occupants as Internal or External. Relational views show Types together with
their required endpoint roles and origin combinations.

The current cut finalizes the axes only. Concrete Type names, direct subtype
definitions, and cell occupancy require a separate accepted authority set
before they become canonical.
