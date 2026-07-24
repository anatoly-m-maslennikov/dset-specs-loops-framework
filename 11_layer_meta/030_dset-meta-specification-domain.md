---
artifact_type: specification
artifact_subtype: domain_model
scope_path:
  - layer:meta
priority: high
---

# Methodology META domain

This is one layer-owned fragment of the logical methodology package. Use the sibling layer hubs for connected definitions; this file owns only the entities and invariants below.

## Entities

Definitions are ordered. Each row uses only ordinary language and entities
defined above it. Cross-entity connections that require later entities are
declared separately below.

| Entity | Definition | Atomic sources |
|---|---|---|
| **Revision mode** | How a persisted project item may change: `atomic` is one independently governed immutable unit; `append_only` preserves accepted records and permits only complete new records; `maintained` permits governed revision of existing content | `DSET-REQUIREMENT-META-041` |
| **Content role** | What a persisted project item contributes: `inquiry`, `definition`, `rationale`, `method`, `implementation`, or `observation` | `DSET-REQUIREMENT-META-001`, `DSET-REQUIREMENT-META-016`, `DSET-REQUIREMENT-META-035` |
| **Governance locus** | What a persisted project item primarily governs: an `internal` project-owned non-relational subject, an `external` outside-owned non-relational subject, or a `relation` among participants | `DSET-REQUIREMENT-META-035` |
| **Scope path** | A project-relative structural coordinate, such as layer, feature, feature group, declared repository folder, or a configured composition; the current project is ambient and project scope is an empty path | `DSET-REQUIREMENT-META-011`, `DSET-REQUIREMENT-META-015` |
| **Artifact route** | One Revision mode, Content role, and Governance locus assigned together | `DSET-REQUIREMENT-META-035` |
| **Artifact type** | One canonical persisted classifier whose optional direct subtype and registered mapping resolve exactly one Artifact route; distinct classifiers may share a route | `DSET-REQUIREMENT-META-035`, `DSET-REQUIREMENT-META-043` |
| **Governed artifact** | One persisted project record, current view, or operative asset with an Artifact type, derived Artifact route, and explicit Scope path | `DSET-REQUIREMENT-META-035` |
| **Atomic record** | A Governed artifact whose accepted semantic content is immutable; correction or changed meaning creates another Atomic record | `DSET-REQUIREMENT-META-041`, `DSET-REQUIREMENT-META-027`, `DSET-REQUIREMENT-META-028` |
| **Append-only sequence** | A Governed artifact whose accepted records remain immutable and ordered while complete new records may be appended | `DSET-REQUIREMENT-META-041` |
| **Relation endpoint** | One referenced participant with an explicit role and independently declared `internal` or `external` origin | `DSET-REQUIREMENT-META-014`, `DSET-REQUIREMENT-META-035` |
| **Relation record** | A Governed artifact with `relation` Governance locus, one typed relation kind, and at least two Relation endpoints | `DSET-REQUIREMENT-META-014`, `DSET-REQUIREMENT-META-035` |
| **Requirement** | The Artifact type for an internal atomic Definition that states a required observable, verifiable result, capability, quality, prevention condition, or obligation | `DSET-REQUIREMENT-META-008`, `DSET-REQUIREMENT-META-009`, `DSET-REQUIREMENT-META-035` |
| **Constraint** | The Artifact type for an external atomic Definition that records an imposed limit on acceptable technologies, dependencies, environments, resources, formats, or operation | `DSET-REQUIREMENT-META-008`, `DSET-REQUIREMENT-META-035` |
| **Contract** | The Artifact type for an atomic relational Definition whose Relation record binds explicit participants across a boundary | `DSET-REQUIREMENT-META-008`, `DSET-REQUIREMENT-META-014` |
| **Implementation Decision** | The Artifact type for an internal atomic Method that selects a material architecture, structure, algorithm, data, tooling, or operating approach | `DSET-REQUIREMENT-META-008`, `DSET-REQUIREMENT-META-035` |
| **Constitutional invariant** | A technology-independent rule that governs multiple responsibility boundaries or defines a boundary between them | `DSET-REQUIREMENT-META-022` |
| **DSET layer** | One ordered responsibility boundary that owns a distinct class of project concerns | `DSET-REQUIREMENT-META-023`, `DSET-REQUIREMENT-META-030` |
| **Layer authority flow** | The forward order in which an earlier DSET layer constrains or refines a later DSET layer | `DSET-REQUIREMENT-META-023`, `DSET-REQUIREMENT-META-025` |
| **Layer dependency** | A consumption edge from one DSET layer to itself or an earlier DSET layer | `DSET-REQUIREMENT-META-025` |
| **Layer handoff** | The declared input, output, entry criteria, exit criteria, and failure behavior between two adjacent DSET layers | `DSET-REQUIREMENT-META-024` |
| **Work Area** | A declared repository-relative folder that bounds Scope path resolution without implying code, deployability, or a particular architecture | `DSET-REQUIREMENT-META-011`, `DSET-CONTRACT-META-001` |
| **Maintained semantic view** | A thin, reasoned, maintained Governed artifact that presents current meaning while returning every summarized claim directly to Atomic records | `DSET-REQUIREMENT-META-042` |
| **Governance surface** | A named optional maintained Governed artifact whose activation creates currentness or gate obligations | `DSET-REQUIREMENT-META-033`, `DSET-REQUIREMENT-META-041` |
| **Project truth** | Active authoritative Atomic records plus applicable maintained Methods, Implementations, and other operative owners; a Maintained semantic view presents but does not override atomic authority | `DSET-REQUIREMENT-META-042`, `DSET-REQUIREMENT-META-026`, `DSET-REQUIREMENT-META-028`, `DSET-REQUIREMENT-META-033` |
| **Exploration Mode** | A session state that permits candidate reasoning without creating a Governed artifact until explicit operator acceptance; question and idea intent enter it silently unless the same input explicitly authorizes a governed change | `DSET-REQUIREMENT-META-021`, `DSET-REQUIREMENT-META-032`, `DSET-REQUIREMENT-META-036`, `DSET-REQUIREMENT-META-037` |
| **Design** | Internal structure and logic selected to satisfy accepted Requirements and Contracts | `DSET-REQUIREMENT-META-008` |
| **Implementation plan** | An ordered Method for realizing accepted Project truth and Design | `DSET-REQUIREMENT-META-001` |
| **Test Plan** | An atomic Method that defines one deterministic check obligation, its exact conditions, and its pass/fail disposition | `DSET-REQUIREMENT-META-001`, `DSET-REQUIREMENT-META-002`, `DSET-REQUIREMENT-META-007`, `DSET-REQUIREMENT-META-041` |
| **Evaluation Plan** | An atomic Method that defines one qualitative, probabilistic, statistical, or model-judged assessment obligation, its criteria, and its disposition rule | `DSET-REQUIREMENT-META-001`, `DSET-REQUIREMENT-META-002`, `DSET-REQUIREMENT-META-007`, `DSET-REQUIREMENT-META-041` |
| **Test-plan view** | A maintained Method that organizes applicable Test Plans without changing their check definitions | `DSET-REQUIREMENT-META-002`, `DSET-REQUIREMENT-META-041`, `DSET-REQUIREMENT-META-042` |
| **Evaluation-plan view** | A maintained Method that organizes applicable Evaluation Plans without changing their assessment definitions | `DSET-REQUIREMENT-META-002`, `DSET-REQUIREMENT-META-041`, `DSET-REQUIREMENT-META-042` |
| **Runtime risk profile** | A selection of recovery and operational semantics triggered by persistence, retry, concurrency, or external effects | `DSET-REQUIREMENT-META-003`, `DSET-REQUIREMENT-META-006`, `DSET-REQUIREMENT-META-029` |
| **Durability topology** | A selection of authoritative files, a local database, or external backing services based on deployment, write volume, and concurrency | `DSET-REQUIREMENT-META-003`, `DSET-REQUIREMENT-META-006`, `DSET-REQUIREMENT-META-029` |

## Cross-entity relations

| Relation | Source | Target | Atomic sources |
|---|---|---|---|
| `orders` | Layer authority flow | DSET layer | `DSET-REQUIREMENT-META-023`, `DSET-REQUIREMENT-META-025` |
| `consumes` | Layer dependency | DSET layer | `DSET-REQUIREMENT-META-025` |
| `connects` | Layer handoff | DSET layer | `DSET-REQUIREMENT-META-024` |
| `scopes` | Work Area | Governed artifact | `DSET-REQUIREMENT-META-011`, `DSET-CONTRACT-META-001` |
| `summarizes` | Maintained semantic view | Atomic record | `DSET-REQUIREMENT-META-042` |
| `constrains` | Contract | Design | `DSET-REQUIREMENT-META-008` |
| `plans_realization_of` | Implementation plan | Design | `DSET-REQUIREMENT-META-001`, `DSET-REQUIREMENT-META-028` |
| `organizes` | Test-plan view | Test Plan | `DSET-REQUIREMENT-META-002`, `DSET-REQUIREMENT-META-007`, `DSET-REQUIREMENT-META-042` |
| `organizes` | Evaluation-plan view | Evaluation Plan | `DSET-REQUIREMENT-META-002`, `DSET-REQUIREMENT-META-007`, `DSET-REQUIREMENT-META-042` |

## Stateful entity lifecycles

These tables own META status meanings. Methodology procedures may trigger the
transitions but do not redefine the states.

### Atomic record

Identity is the stable artifact ID. Emission authority belongs to the operator
or configured project authority; archive authority belongs to the operator or
the governed lifecycle procedure.

| Status | Entry criteria | Exit criteria | Allowed next status | Required evidence | Atomic sources |
|---|---|---|---|---|---|
| Active | One accepted immutable unit is emitted with valid identity, scope, provenance, and type-derived route | A governed replacement, resolution, or withdrawal authorizes archive relocation | Archived | Emission commit and valid carrier | `DSET-REQUIREMENT-META-035`, `DSET-REQUIREMENT-META-041` |
| Archived | Byte-stable relocation preserves identity and history while removing the record from the active set | Terminal; recurrence or changed meaning creates a new Atomic record | — | Archive instruction, relation or Version reference when applicable, and Git history | `DSET-REQUIREMENT-META-027`, `DSET-REQUIREMENT-META-041` |

Reopening and in-place semantic correction are forbidden. Archive failure keeps
the record Active and reports the failed transition.

### Maintained semantic view

Identity is its unique project-local carrier name and Scope path. Semantic
refresh authority belongs to the configured view owner.

| Status | Entry criteria | Exit criteria | Allowed next status | Required evidence | Atomic sources |
|---|---|---|---|---|---|
| Current | A reasoned refresh represents the applicable active atomic frontier and every semantic source resolves | The frontier changes or a missing, incorrect, or unresolved representation is found | Stale | Reviewed refresh plus structured source/fragment traceability | `DSET-REQUIREMENT-META-042` |
| Stale | The view no longer truthfully represents its applicable atomic frontier | A reasoned refresh restores complete representation | Current | Staleness reason and affected atomic identities | `DSET-REQUIREMENT-META-027`, `DSET-REQUIREMENT-META-042` |

A failed refresh leaves the view Stale. A source mention without an identified
semantic fragment is navigation, not evidence that the source is represented.

### Governance surface

Identity is the configured surface key plus Scope path. Activation,
deactivation, and restoration to Current require the configured owner.

| Status | Entry criteria | Exit criteria | Allowed next status | Required evidence | Atomic sources |
|---|---|---|---|---|---|
| Inactive | The surface creates no currentness or gate obligation | Activation is authorized and reconciliation begins | Reconciling | Surface identity and activation instruction | `DSET-REQUIREMENT-META-033` |
| Reconciling | The applicable atomic frontier is identified for a new or retained carrier | Reconciliation succeeds, finds a blocker, or authorized deactivation occurs | Current, Blocked, Inactive | Frontier, coverage result, and provenance | `DSET-REQUIREMENT-META-033`, `DSET-REQUIREMENT-META-042` |
| Current | Reconciliation establishes truthful representation and the surface's gates apply | The frontier changes, representation fails, or deactivation is authorized | Stale, Inactive | Reviewed reconciliation with structured atomic traceability | `DSET-REQUIREMENT-META-033`, `DSET-REQUIREMENT-META-042` |
| Stale | An active surface no longer represents its applicable frontier | Reconciliation starts or deactivation is authorized | Reconciling, Inactive | Staleness reason and affected atomic identities | `DSET-REQUIREMENT-META-027`, `DSET-REQUIREMENT-META-033` |
| Blocked | Reconciliation cannot truthfully establish Current | The blocker is resolved and reconciliation restarts, or deactivation is authorized | Reconciling, Inactive | Blocker and affected atomic identities | `DSET-REQUIREMENT-META-033`, `DSET-REQUIREMENT-META-042` |

Failed reconciliation never preserves or restores Current. Deactivation
preserves the carrier and history.

### Exploration Mode

Identity is the current bounded session interaction. The operator alone
authorizes exit into governed change.

| Status | Entry criteria | Exit criteria | Allowed next status | Required evidence | Atomic sources |
|---|---|---|---|---|---|
| Inactive | No exploratory intent is active | Question, idea, comparison, critique, or explicit exploration intent is established | Active | Operator/session input | `DSET-REQUIREMENT-META-021`, `DSET-REQUIREMENT-META-036`, `DSET-REQUIREMENT-META-037` |
| Active | Exploratory intent is established | Explicit acceptance, record, apply, implement, fix, or end-exploration instruction | Inactive | Operator instruction scoped to the accepted change | `DSET-REQUIREMENT-META-021`, `DSET-REQUIREMENT-META-036`, `DSET-REQUIREMENT-META-037` |

Exploration failure or abandonment leaves governed truth unchanged.

## Canonical layer responsibilities

| Layer | Responsibility | Atomic source |
|---|---|---|
| **META** | Meanings, routing axes, universal invariants, layer topology, and inter-layer semantics | `DSET-REQUIREMENT-META-023` |
| **GOV** | Governed carriers, identity, settings, provenance, lifecycle, applicability, scope, and conflict governance | `DSET-REQUIREMENT-META-023` |
| **TOOL** | Executable capabilities, validation, resolution, diagnostics, generation, and repository mechanics | `DSET-REQUIREMENT-META-023` |
| **SKILL** | Thin provider-neutral orchestration, gates, workflow chaining, and session continuity | `DSET-REQUIREMENT-META-023` |
| **IMPL** | Development environments, implementation profiles, code, Test implementations, Evaluation implementations, and code-quality gates | `DSET-REQUIREMENT-META-023` |
| **OPS** | Post-implementation delivery, release, publication, runtime supportability, investigation, recovery, and hosted evidence | `DSET-REQUIREMENT-META-023` |

## Invariants

- **DSET-INVARIANT-META-001:** Test and Evaluation remain separate registered Methods, implementations, and Observation streams. Source: `DSET-REQUIREMENT-META-002`.
- **DSET-INVARIANT-META-002:** Runtime risk, durability topology, effect safety, language enforcement, and artifact governance are selected explicitly rather than inherited from one universal tool class. Sources: `DSET-REQUIREMENT-META-003` and `DSET-REQUIREMENT-META-006`.
- **DSET-INVARIANT-META-003:** Each durable concern has one authoritative owner; process memory and derived views are not independent truth. Source: `DSET-REQUIREMENT-META-026`.
- **DSET-INVARIANT-META-004:** Exact governance and recursion behavior remains deterministic test proof; agent interpretation, rule-following, navigation, and diagnostic usefulness remain separate eval proof. Source: `DSET-REQUIREMENT-META-007`.
- **DSET-INVARIANT-META-005:** Every governed artifact has exactly one value on each routing axis, derived from its registered artifact type and optional direct subtype. Carriers never repeat the derived route coordinates. Source: `DSET-REQUIREMENT-META-035`.
- **DSET-INVARIANT-META-006:** The routing matrix is sparse. Empty routes are valid and create no placeholder obligation. Each registered type/subtype resolves one route, while several semantically distinct names may share that route. Sources: `DSET-REQUIREMENT-META-035` and `DSET-REQUIREMENT-META-043`.
- **DSET-INVARIANT-META-007:** `internal` governance is mandatory. A project may enable `external` and `relation` governance independently when its boundaries require them. Source: `DSET-REQUIREMENT-META-035`.
- **DSET-INVARIANT-META-008:** A Relation record declares a relation kind and at least two role-bearing endpoints. Each endpoint independently declares internal or external origin; endpoint origin is not another artifact-routing axis. Source: `DSET-REQUIREMENT-META-014`.
- **DSET-INVARIANT-META-009:** Scope path is project-relative structural context, not a fourth semantic routing axis. The current project is ambient and never repeated inside the path; every scope-dependent DSET artifact or run resolves against the repository-level scope or one or more declared Work Areas. Sources: `DSET-REQUIREMENT-META-011`, `DSET-REQUIREMENT-META-015`, and `DSET-CONTRACT-META-001`.
- **DSET-INVARIANT-META-010:** Artifact types are interface vocabulary for valid routes, not ontological parents or children. Requirement, Constraint, Contract, and Implementation Decision therefore do not require a Decision-centered name hierarchy. Sources: `DSET-REQUIREMENT-META-008`, `DSET-REQUIREMENT-META-009`, and `DSET-REQUIREMENT-META-035`.
- **DSET-INVARIANT-META-011:** The development feedback cycle is Inquiry → Definition → Rationale → Method → Implementation → Observation → Inquiry. A record may enter at any justified role; the flow does not determine its identity. Sources: `DSET-REQUIREMENT-META-001` and `DSET-REQUIREMENT-META-016`.
- **DSET-INVARIANT-META-012:** Generated Code and hand-maintained executable truth are maintained Implementations with different update procedures; generated output additionally declares generator and source provenance. A Git commit is a separate atomic Implementation record. Source: `DSET-REQUIREMENT-META-041`.
- **DSET-INVARIANT-META-013:** Outcome framing may describe an intended measurable state inside a Definition or Method, while an observed outcome is an Observation. Outcome is not a routing axis or mandatory registered name. Source: `DSET-REQUIREMENT-META-010`.
- **DSET-INVARIANT-META-014:** A Contract is an atomic relational Definition. Complete replacement requires an operator-accepted successor with `replacement_of`, followed by archive relocation of the predecessor. Implementation cannot rewrite it. Sources: `DSET-REQUIREMENT-META-008` and `DSET-REQUIREMENT-META-014`.
- **DSET-INVARIANT-META-015:** A Work Area declaration owns a scope boundary; session continuity may reference it but cannot define, modify, or replace it. Neither repository-level scope nor a Work Area implies code, a deployment unit, a service, a feature, or a module. Source: `DSET-REQUIREMENT-META-011`.
- **DSET-INVARIANT-META-016:** Non-derived provenance, priority, applicability, relation endpoints, and type-specific facts remain explicit. Acceptance is inherent to emitted atoms, active versus archived state comes from repository placement, and ambient project authority is not repeated. Sources: `DSET-REQUIREMENT-META-035` and `DSET-REQUIREMENT-META-038`.
- **DSET-INVARIANT-META-017:** Exploration Mode creates no governed artifacts or governance commits. Only explicit operator acceptance closes it and authorizes durable emission. Source: `DSET-REQUIREMENT-META-021`.
- **DSET-INVARIANT-META-018:** Maintained semantic views are thin current views, not compiled restatements. Atomic records remain the semantic authority. Source: `DSET-REQUIREMENT-META-042`.
- **DSET-INVARIANT-META-019:** A domain entity is defined only with entities already defined above it. References to later entities are connections recorded outside the definition. Source: `DSET-REQUIREMENT-META-042`.
- **DSET-INVARIANT-META-020:** Every stateful domain entity declares identity, invariants, status meanings, entry and exit criteria, transition authority, allowed transitions, required evidence, and applicable failure/recovery behavior. Source: `DSET-REQUIREMENT-META-042`.
- **DSET-INVARIANT-META-021:** Semantic provenance inside a maintained semantic view targets atomic records only. Links to other maintained views or hubs are navigation only. Source: `DSET-REQUIREMENT-META-042`.
- **DSET-INVARIANT-META-022:** META admits only technology-independent rules that govern multiple layers or a layer boundary; downstream mechanisms remain with the earliest complete downstream owner. Source: `DSET-REQUIREMENT-META-022`.
- **DSET-INVARIANT-META-023:** DSET uses the canonical, non-overlapping `META → GOV → TOOL → SKILL → IMPL → OPS` layer responsibilities. Source: `DSET-REQUIREMENT-META-023`.
- **DSET-INVARIANT-META-024:** Every adjacent layer boundary declares its input, output, entry criteria, exit criteria, and failure behavior. Source: `DSET-REQUIREMENT-META-024`.
- **DSET-INVARIANT-META-025:** Layer dependencies form a DAG; authority flows forward, later layers consume earlier authority, and feedback creates no backward governance. Source: `DSET-REQUIREMENT-META-025`.
- **DSET-INVARIANT-META-026:** Each governed claim has one authoritative owner at the earliest layer that can define it completely. Source: `DSET-REQUIREMENT-META-026`.
- **DSET-INVARIANT-META-027:** Accepted upstream change preserves historical atoms and propagates potential staleness forward through affected views, methods, implementations, and assurance. Source: `DSET-REQUIREMENT-META-027`.
- **DSET-INVARIANT-META-028:** Authority, checking methods, implementations, observations, evidence, and Verification remain distinct; assurance cannot establish or override authority. Source: `DSET-REQUIREMENT-META-028`.
- **DSET-INVARIANT-META-029:** Profiles specialize applicable downstream realization without weakening META invariants or requiring non-applicable placeholders. Source: `DSET-REQUIREMENT-META-029`.
- **DSET-INVARIANT-META-030:** A new layer requires a unique responsibility, explicit handoffs, and an acyclic extension; otherwise use a feature, profile, Work Area, or other scope. Source: `DSET-REQUIREMENT-META-030`.
- **DSET-INVARIANT-META-031:** Recursive self-hosting uses the same constitution, keeps reusable and applied owners distinct, and terminates at a declared fixed point. Source: `DSET-REQUIREMENT-META-031`.
- **DSET-INVARIANT-META-032:** The durable control plane contains accepted current, secret-free, provider-neutral truth; future intentions and unaccepted exploration remain outside current authority. Source: `DSET-REQUIREMENT-META-032`.
- **DSET-INVARIANT-META-033:** DSET starts atomic-first; named maintained governance surfaces are optional and may be activated or deactivated without changing atomic authority. Sources: `DSET-REQUIREMENT-META-033` and `DSET-REQUIREMENT-META-041`.
- **DSET-INVARIANT-META-034:** Every semantic META change follows the closed constitutional amendment sequence from Exploration and explicit acceptance through impact mapping, eligibility and topology review, reasoned maintained-view update, forward staleness propagation, verification, and fixed-point declaration. Source: `DSET-REQUIREMENT-META-034`.
- **DSET-INVARIANT-META-035:** Every governed artifact resolves exactly one Revision mode: `atomic`, `append_only`, or `maintained`. Artifact-specific update mechanisms remain separate from Revision mode. Source: `DSET-REQUIREMENT-META-041`.
- **DSET-INVARIANT-META-036:** An operator question enters Exploration Mode silently when its primary intent is inquiry, explanation, comparison, critique, alternatives, or recommendation; punctuation alone never selects the mode. Source: `DSET-REQUIREMENT-META-036`.
- **DSET-INVARIANT-META-037:** An operator idea enters Exploration Mode silently when it presents a candidate rather than an accepted instruction; explicit change authorization in the same input applies only to the authorized change. Source: `DSET-REQUIREMENT-META-037`.
