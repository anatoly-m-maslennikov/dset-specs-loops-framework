# Artifact routing rules

**Rule ID:** `DSET-RULE-ARTIFACT-CLASSIFICATION`

## Purpose

DSET routes every persisted governed artifact through four independent fields:
Revision Mode, Content Role, Governance Origin, and Relation Shape.

Every artifact also has a required structural coordinate, Scope Path, which
selects a view over the shared matrix. DSET has no canonical artifact Type or
subtype taxonomy.

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
| `inquiry` | Requests unresolved knowledge, choice, or clarification |
| `rationale` | Explains why another claim, selection, or interpretation is justified |
| `method` | Describes a reusable way, mechanism, procedure, or check |
| `implementation` | Is an operative realization or asset |
| `observation` | Records an actual-state claim, finding, measurement, or outcome in a declared time or evidence window |

File format, executability, folder, layer, workflow stage, and carrier kind do
not select the role.

Test and Evaluation definitions are Method when they specify reusable checks.
Their runners and harnesses may instead be Implementation. A dated execution
is a real Work occurrence outside artifact routing; its persisted
result, trace, or proof is Observation and references that occurrence.

## Content Role loop

Content Roles participate in this canonical semantic loop:

```text
Inquiry
  -> Definition
  -> Rationale
  -> Method
  -> Implementation
  -> Observation
  -> Inquiry
  -> ...
```

Inquiry frames an unresolved matter. Definition establishes the intended or
accepted state. Rationale explains why. Method describes how to realize or
check it. Implementation realizes it. Observation records actual state and can
expose the next unresolved matter.

The loop orders relationships between successor artifacts. It does not mutate
one artifact through multiple roles. Each artifact retains one primary Content
Role, one artifact may produce multiple successors, and a role may be omitted
when its own entry criteria do not require a persisted artifact.

## Scope path

`scope_path` is an extensible structural address composed from enabled project,
feature-group, feature, layer, and future structural segments. It identifies
the narrowest common owner that can govern the whole artifact and selects one
matrix slice.

Scope Path never determines any routing field. It does not identify the Entity
of Concern, declare claim applicability, or establish a bounded semantic
context. If meanings or invariants differ across structural scopes, DSET names
the semantic context or an explicit bridge rather than inferring it from the
path.

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

Relation Shape and Governance Origin complete the route selected inside the
Revision Mode by Content Role matrix at its Scope Path.

### Relation shape

`relation_shape` declares the artifact's inherent semantic arity:

| Value | Definition |
|---|---|
| `standalone` | Primary meaning does not require multiple typed endpoints |
| `relational` | Primary meaning requires a relation kind and at least two typed, role-bearing endpoints |

An ordinary citation, provenance field, or traceability link does not make an
artifact Relational. A Relational artifact declares its relation kind,
endpoint roles, and endpoint origins. Direction follows from the Relation Kind
and endpoint roles. Relational structures may be n-ary.

Relational and Standalone artifacts use the same two intrinsic dimensions and
structural Scope Path. Separate renderings may improve readability, but they
do not create different routing systems.

### Governance origin

Every governed artifact declares:

```toml
governance_origin = "internal" # internal | external
```

Governance Origin identifies who controls the artifact's semantic content and
currentness. It does not establish truth, project authority, authorship,
storage location, or provenance.

A Relational artifact additionally declares each endpoint's independent
`origin = "internal"` or `origin = "external"`. Artifact origin identifies who
governs the relation record; endpoint origins identify its participants. One
never substitutes for the other.

Origin participates directly in routing. It does not establish a separate
taxonomy, authority claim, or duplicate artifact identity.

## Deterministic route names

Every complete route has exactly one canonical display name:

```text
<Governance Origin> <Revision Mode> <Content Role> <Artifact | Relation>
```

Examples include `Internal Atomic Definition Artifact` and
`External Maintained Method Relation`. The name is derived from the routing
fields and never used as a routing input. Aliases, Types, and subtypes are not
admitted.

## Pull-request direction

A pull request demonstrates the Relational boundary:

```toml
revision_mode = "maintained"
content_role = "method"
relation_shape = "relational"
governance_origin = "internal"
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

This routing applies when the Entity of Concern is the reusable
integration and review mechanism. A PR carrier may contain proposed
Definitions, observations, and other separately governed claims; the carrier
does not force them all into Method.

## Classification order

1. Recover the EntityOfConcern and one primary artifact job. Split a
   multi-head artifact.
2. Select `content_role` from the primary contribution.
3. Select `revision_mode` from the change semantics.
4. Assign `scope_path` as the structural ownership address.
5. Select `relation_shape`. For a Relational artifact, recover the relation
   kind, endpoint roles, and endpoint origins.
6. Select the artifact's `governance_origin`.
7. Derive the route key and its one deterministic display name.
8. Add provenance, evidence, and traceability without treating them as truth
   or authority.

No routing-field value is inferred from another. Routing never derives meaning
from a filename, display name, workflow, host, tool, or next action. DSET does
not require every route combination to be used.

## Matrix rendering

Each `scope_path` selects one structural slice of the shared two-dimensional
matrix. The slice uses Revision Mode as rows and Content Role as columns.
Views may qualify occupants by artifact Governance Origin. Relational views
also show artifacts with their required Relation Kind, endpoint roles, and
endpoint-origin combinations.
