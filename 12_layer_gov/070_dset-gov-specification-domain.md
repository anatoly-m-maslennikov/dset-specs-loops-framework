---
artifact_type: specification
artifact_subtype: domain_model
scope_path:
  - layer:gov
priority: high
---

# Governance domain model

This model defines GOV entities in dependency order. A definition uses only
entities defined above it; later sections add relations without changing an
earlier definition.

## Entities

| Entity | Definition | Atomic sources |
|---|---|---|
| **Project** | The current repository selected for one DSET governance context | `DSET-REQUIREMENT-GOV-100` |
| **Structural scope** | A Project-relative owner address composed from enabled layers, features, feature groups, Work Areas, or future registered structural dimensions | `DSET-REQUIREMENT-META-015`, `DSET-REQUIREMENT-GOV-032` |
| **Revision mode** | Exactly one permitted write behavior: `atomic`, `append_only`, or `maintained` | `DSET-REQUIREMENT-META-041` |
| **Content role** | Exactly one contribution: `inquiry`, `analysis`, `definition`, `method`, `implementation`, or `observation` | `DSET-REQUIREMENT-META-035`, `DSET-REQUIREMENT-META-047`, `DSET-REQUIREMENT-META-048` |
| **Governance locus** | Exactly one primary governance position: `internal`, `external`, or `relation` | `DSET-REQUIREMENT-META-035`, `DSET-REQUIREMENT-GOV-101` |
| **Artifact route** | One Revision mode, Content role, and Governance locus assigned together, with exactly one canonical Artifact type | `DSET-REQUIREMENT-META-035`, `DSET-REQUIREMENT-META-045`, `DSET-REQUIREMENT-META-046` |
| **Governed artifact** | One persisted Project item with one registered artifact type, at most one direct subtype, one derived Artifact route, and one Structural scope | `DSET-REQUIREMENT-META-035`, `DSET-REQUIREMENT-GOV-102` |
| **Relation endpoint** | One role-bearing participant identity with independently declared internal or external origin | `DSET-REQUIREMENT-META-014`, `DSET-REQUIREMENT-GOV-101` |
| **Artifact relation** | One registered directional semantic edge from a Governed artifact to one or more stable target identities, or one relational artifact whose meaning is carried by at least two Relation endpoints | `DSET-REQUIREMENT-META-014`, `DSET-IMPL-GOV-004` |
| **Atomic artifact** | A Governed artifact whose accepted meaning is immutable after emission | `DSET-REQUIREMENT-META-041`, `DSET-REQUIREMENT-GOV-061` |
| **Append-only artifact** | A Governed artifact whose accepted records and order are immutable and that accepts only complete new records | `DSET-REQUIREMENT-META-041`, `DSET-REQUIREMENT-GOV-100` |
| **Maintained artifact** | A Governed artifact whose registered procedure may revise existing content | `DSET-REQUIREMENT-META-041`, `DSET-REQUIREMENT-GOV-070` |
| **Active atom** | An Atomic artifact located in its active type folder and eligible for current routing, authority, work, or assurance according to its registered type | `DSET-DECISION-GOV-035`, `DSET-REQUIREMENT-GOV-061` |
| **Archived atom** | The same immutable Atomic artifact relocated byte-for-byte to its type-local `archive/` and excluded from the active set | `DSET-DECISION-GOV-035`, `DSET-REQUIREMENT-GOV-096` |
| **Artifact catalog** | The single project-local executable registry assigning exactly one canonical type to every Artifact route and mapping its direct route-inheriting subtypes to identity kinds, carriers, and persistence behavior | `DSET-REQUIREMENT-META-045`, `DSET-REQUIREMENT-META-046`, `DSET-REQUIREMENT-GOV-102` |
| **Project settings** | The single project-local operator configuration selecting enabled catalog entries, workflow behavior, optional surfaces, and other policy choices without restating catalog mappings | `DSET-REQUIREMENT-GOV-070`, `DSET-REQUIREMENT-GOV-102` |
| **Governing document** | The single Maintained artifact that owns the current application of one or more normative rule IDs | `DSET-DECISION-GOV-002` |
| **Governance registry** | The project-local mapping from workflow and rule IDs to a Governing document, its prerequisites, applicability, and profile identity | `DSET-DECISION-GOV-002`, `DSET-REQUIREMENT-GOV-052` |
| **Maintained semantic view** | A thin Maintained artifact synthesized from applicable Active atoms, with domain flow, dependency-ordered definitions, lifecycle criteria, and structured atomic traceability | `DSET-REQUIREMENT-META-042`, `DSET-REQUIREMENT-GOV-092` |
| **Governance surface** | A named optional Maintained artifact whose activation adds its registered currentness and entry-gate obligations | `DSET-REQUIREMENT-META-033`, `DSET-REQUIREMENT-GOV-092` |
| **Hub** | A thin Maintained navigation artifact linking stable folders and long-lived owners without listing every atom or owning normative truth | `DSET-REQUIREMENT-GOV-053` |
| **Framework source** | The repository-root reusable DSET methodology from which released methodology packages are produced | `DSET-DECISION-GOV-022`, `DSET-REQUIREMENT-GOV-052` |
| **Installed methodology** | A materialized project-local copy of selected Framework source under `.dset/000_dset_methodology/` | `DSET-IMPL-GOV-002`, `DSET-REQUIREMENT-GOV-052` |
| **Applied project artifact** | A project-owned Governed artifact outside Installed methodology that records the current Project's requirements, work, implementation, assurance, or history | `DSET-DECISION-GOV-022` |
| **Journal** | Durable Append-only artifacts stored as NDJSON under `.dset_journal/` | `DSET-REQUIREMENT-GOV-100` |
| **Runtime state** | Disposable locks, caches, scratch data, and process-local output under `.dset_runtime/` | `DSET-REQUIREMENT-GOV-100` |
| **Priority** | The stored `high`, `medium`, or `low` rank, with `highest` available only as a virtual capped comparison result | `DSET-REQUIREMENT-GOV-063` |
| **Ruleset identity** | The selected profile/version provenance plus whether Installed methodology remains equivalent or forms an explicitly custom Project ruleset | `DSET-DECISION-GOV-002` |

## Cross-entity relations

| Relation | Source | Target | Atomic sources |
|---|---|---|---|
| `derives_route_for` | Artifact catalog | Governed artifact | `DSET-REQUIREMENT-GOV-102` |
| `selects` | Project settings | Artifact catalog | `DSET-REQUIREMENT-GOV-102` |
| `resolves` | Governance registry | Governing document | `DSET-DECISION-GOV-002` |
| `materialization_of` | Installed methodology | Framework source | `DSET-IMPL-GOV-002`, `DSET-REQUIREMENT-GOV-052` |
| `represents` | Maintained semantic view | Active atom | `DSET-REQUIREMENT-META-042` |
| `stores` | Journal | Append-only artifact | `DSET-REQUIREMENT-GOV-100` |

## Stateful entity lifecycles

These tables own GOV status meanings. Procedures and tools may perform or check
the transitions but do not redefine them.

### Atomic artifact

Identity is its stable artifact ID. Archive relocation is the only state
transition.

| Status | Entry criteria | Exit criteria | Allowed next status | Required evidence | Atomic sources |
|---|---|---|---|---|---|
| Active | A valid immutable artifact is emitted and committed in its active type folder | Replacement, resolution, or withdrawal authorizes byte-stable archive relocation | Archived | Valid carrier, seal or identity registration, and emission commit | `DSET-REQUIREMENT-GOV-061`, `DSET-REQUIREMENT-GOV-065` |
| Archived | The same bytes and identity are relocated to the type-local archive and excluded from the active set | Terminal; recurrence or changed meaning creates a new artifact | — | Archive trailers, relation or Version reference when applicable, and Git return path | `DSET-DECISION-GOV-035`, `DSET-REQUIREMENT-GOV-096` |

Failed validation or relocation leaves the artifact Active. Reopening and
in-place semantic correction are forbidden.

### Append-only artifact

Identity is the registered stream or segment identity.

| Status | Entry criteria | Exit criteria | Allowed next status | Required evidence | Atomic sources |
|---|---|---|---|---|---|
| Open | A valid sequence exists and can accept one complete next record | Rotation or terminal closure seals the sequence | Sealed | Sequence identity and validated record boundary | `DSET-REQUIREMENT-META-041`, `DSET-REQUIREMENT-GOV-100` |
| Sealed | Accepted records and order are fixed | Terminal; continued recording opens a new sequence | — | Final frontier and integrity check | `DSET-REQUIREMENT-META-041`, `DSET-REQUIREMENT-GOV-100` |

A malformed or incomplete append is rejected without changing the accepted
frontier.

### Maintained semantic view

Identity is its unique carrier name and Structural scope.

| Status | Entry criteria | Exit criteria | Allowed next status | Required evidence | Atomic sources |
|---|---|---|---|---|---|
| Current | Reasoned content represents the applicable active atomic frontier | The frontier changes or an omission, mismatch, or unresolved source is found | Stale | Structured source-to-fragment traceability plus reviewed refresh | `DSET-REQUIREMENT-META-042`, `DSET-REQUIREMENT-GOV-092` |
| Stale | The view no longer truthfully represents its applicable frontier | A reasoned refresh restores truthful representation | Current | Staleness reason and affected atomic identities | `DSET-REQUIREMENT-META-027`, `DSET-REQUIREMENT-META-042` |

A loose source mention is navigation, not proof of representation. Failed
refresh leaves the view Stale.

### Governance surface

Identity is its configured surface key plus Structural scope.

| Status | Entry criteria | Exit criteria | Allowed next status | Required evidence | Atomic sources |
|---|---|---|---|---|---|
| Inactive | The surface creates no currentness or gate obligation | Activation is authorized and reconciliation starts | Reconciling | Surface identity and authorization | `DSET-REQUIREMENT-META-033`, `DSET-REQUIREMENT-GOV-092` |
| Reconciling | Its applicable frontier is identified | Reconciliation succeeds, finds a blocker, or deactivation is authorized | Current, Blocked, Inactive | Frontier, coverage result, and provenance | `DSET-REQUIREMENT-META-042`, `DSET-REQUIREMENT-GOV-092` |
| Current | Reconciliation establishes truthful representation and its gates apply | The frontier changes, representation fails, or deactivation is authorized | Stale, Inactive | Reviewed reconciliation with structured traceability | `DSET-REQUIREMENT-META-042`, `DSET-REQUIREMENT-GOV-092` |
| Stale | The active surface no longer represents its frontier | Reconciliation starts or deactivation is authorized | Reconciling, Inactive | Staleness reason and affected identities | `DSET-REQUIREMENT-META-027`, `DSET-REQUIREMENT-GOV-092` |
| Blocked | Reconciliation cannot establish Current | The blocker is resolved and reconciliation restarts, or deactivation is authorized | Reconciling, Inactive | Blocker and affected identities | `DSET-REQUIREMENT-META-033`, `DSET-REQUIREMENT-GOV-092` |

Failed reconciliation never preserves or restores Current. Deactivation
preserves the carrier and Git history.

## Core invariants

- **DSET-INVARIANT-GOV-001:** Framework source, installed methodology, and
  applied project artifacts never share a writable owner. Installation
  materializes ordinary files; governed execution never follows a live
  reference back to framework source. Sources:
  `DSET-DECISION-GOV-022`, `DSET-IMPL-GOV-002`, and
  `DSET-REQUIREMENT-GOV-052`.
- **DSET-INVARIANT-GOV-002:** Every governed artifact has one registered
  type/subtype and derives exactly one Artifact route. No parent semantic-Type
  hierarchy, workflow name, carrier, folder, or requested next action supplies
  a second classification. Every route has exactly one canonical type, and a
  direct subtype inherits its complete route. Sources:
  `DSET-REQUIREMENT-META-035`, `DSET-REQUIREMENT-META-045`,
  `DSET-REQUIREMENT-META-046`, `DSET-IMPL-GOV-003`, and
  `DSET-REQUIREMENT-GOV-101`.
- **DSET-INVARIANT-GOV-003:** The Artifact catalog owns route and identity
  mappings. Project settings own only the enabled whitelist and operator
  choices. The framework catalog defines all 54 routes even when a project
  disables some types. Unknown, disabled, duplicate, empty, or ambiguous
  mappings fail closed. Sources: `DSET-REQUIREMENT-META-045`,
  `DSET-REQUIREMENT-META-046`, and `DSET-REQUIREMENT-GOV-102`.
- **DSET-INVARIANT-GOV-004:** The only Revision modes are `atomic`,
  `append_only`, and `maintained`; no freshness class is a fourth mode.
  Sources: `DSET-REQUIREMENT-META-041` and
  `DSET-REQUIREMENT-META-042`.
- **DSET-INVARIANT-GOV-005:** An Atomic artifact's accepted meaning is
  immutable. Complete semantic correction emits a successor. A proven
  one-to-one identity or carrier migration may recode representation without
  changing the atom. Sources: `DSET-REQUIREMENT-GOV-060` and
  `DSET-REQUIREMENT-GOV-061`.
- **DSET-INVARIANT-GOV-006:** Active and archived are the only Atomic-artifact
  storage states. Replacement, resolution, withdrawal, and recurrence use
  typed relations, archive placement, Version planning, and Git history; DSET
  has no lifecycle-event artifact type. Source: `DSET-DECISION-GOV-035`.
- **DSET-INVARIANT-GOV-007:** Every Markdown artifact has valid YAML
  frontmatter and remains GitHub-preview compatible. Derived route coordinates,
  status, generic authority, and ephemeral worktree state are not duplicated
  in the property block. Sources: `DSET-CONSTRAINT-GOV-002`,
  `DSET-REQUIREMENT-GOV-095`, and `DSET-REQUIREMENT-META-038`.
- **DSET-INVARIANT-GOV-008:** Carrier choice follows job: Markdown with YAML
  frontmatter for human-governed narrative artifacts; TOML for directly
  executed human-edited configuration; JSON for schemas, contracts, wire data,
  or generated machine data; NDJSON for append-only logs; and native formats
  for code, CI, lockfiles, and host manifests. Sources:
  `DSET-DECISION-GOV-015` and `DSET-REQUIREMENT-GOV-097`.
- **DSET-INVARIANT-GOV-009:** Git is mandatory. Every implemented authority or
  resolved Problem has a committed change naming the governed artifact and one
  Session trailer. Source: `DSET-REQUIREMENT-GOV-065`.
- **DSET-INVARIANT-GOV-010:** Stored priority is exactly `high`, `medium`, or
  `low`; `highest` is virtual and future-version work belongs in a Version
  Roadmap rather than a deferred priority. Source:
  `DSET-REQUIREMENT-GOV-063`.
- **DSET-INVARIANT-GOV-011:** `.dset/` owns governed state,
  `.dset_journal/` owns durable append-only running records, and
  `.dset_runtime/` owns disposable state. Source:
  `DSET-REQUIREMENT-GOV-100`.
- **DSET-INVARIANT-GOV-012:** Features are horizontal peers joined by
  Contracts. Layers are ordered `META → GOV → TOOL → SKILL → IMPL → OPS`;
  authority moves only forward, preferably one layer at a time. Sources:
  `DSET-REQUIREMENT-META-023` and `DSET-REQUIREMENT-META-025`.
- **DSET-INVARIANT-GOV-013:** Every claim belongs to the narrowest structural
  scope containing all affected owners and subjects. A project-level artifact
  owns only genuinely cross-child or whole-project concerns. Source:
  `DSET-REQUIREMENT-GOV-032`.
- **DSET-INVARIANT-GOV-014:** Authority and assurance remain distinct.
  Requirements, Constraints, Contracts, and Implementation Decisions may
  authorize; plans define checks; executions create observations; Verification
  derives a bounded reliance statement. Source:
  `DSET-REQUIREMENT-META-028`.
- **DSET-INVARIANT-GOV-015:** Rules resolve locally to one maintained governing
  document and its active atomic sources. Invalid ownership, dependency,
  precedence, applicability, or customization identity fails closed. Sources:
  `DSET-DECISION-GOV-002` and `DSET-REQUIREMENT-GOV-070`.
