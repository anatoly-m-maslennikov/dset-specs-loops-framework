# Methodology META domain

This is one layer-owned fragment of the logical methodology package. Use the sibling layer hubs for connected definitions; this file owns only the entities and invariants below.

## Entities

Definitions are ordered. Each row uses only ordinary language and entities
defined above it. Cross-entity connections that require later entities are
declared separately below.

| Entity | Definition | Atomic sources |
|---|---|---|
| **Revision mode** | How a persisted project item may change: `atomic` is accepted and immutable; `evergreen` is a mutable current view; `maintained` is a mutable operative item | `DSET-REQUIREMENT-META-012`, `DSET-REQUIREMENT-META-018` |
| **Content role** | What a persisted project item contributes: `inquiry`, `definition`, `rationale`, `method`, `implementation`, or `observation` | `DSET-REQUIREMENT-META-001`, `DSET-REQUIREMENT-META-016`, `DSET-REQUIREMENT-META-018` |
| **Governance locus** | What a persisted project item primarily governs: an `internal` project-owned non-relational subject, an `external` outside-owned non-relational subject, or a `relation` among participants | `DSET-REQUIREMENT-META-012`, `DSET-REQUIREMENT-META-018` |
| **Scope path** | A project-relative structural coordinate, such as layer, feature, feature group, declared repository folder, or a configured composition; the current project is ambient and project scope is an empty path | `DSET-REQUIREMENT-META-011`, `DSET-REQUIREMENT-META-015` |
| **Artifact route** | One explicit Revision mode, Content role, and Governance locus assigned together | `DSET-REQUIREMENT-META-012`, `DSET-REQUIREMENT-META-018` |
| **Governed artifact** | One persisted project record, current view, or operative asset with an explicit Artifact route and Scope path | `DSET-REQUIREMENT-META-012`, `DSET-REQUIREMENT-META-018` |
| **Atomic record** | A Governed artifact whose accepted semantic content is immutable; correction or changed meaning creates another Atomic record | `DSET-REQUIREMENT-META-020`, `DSET-REQUIREMENT-META-027`, `DSET-REQUIREMENT-META-028` |
| **Registered name** | An optional human-facing label assigned one-to-one to an occupied Artifact route without defining or changing that route | `DSET-REQUIREMENT-META-013`, `DSET-REQUIREMENT-META-018` |
| **Relation endpoint** | One referenced participant with an explicit role and independently declared `internal` or `external` origin | `DSET-REQUIREMENT-META-014`, `DSET-REQUIREMENT-META-018` |
| **Relation record** | A Governed artifact with `relation` Governance locus, one typed relation kind, and at least two Relation endpoints | `DSET-REQUIREMENT-META-014`, `DSET-REQUIREMENT-META-018` |
| **Requirement** | The Registered name for an internal atomic Definition that states a required observable, verifiable result, capability, quality, prevention condition, or obligation | `DSET-REQUIREMENT-META-008`, `DSET-REQUIREMENT-META-009`, `DSET-REQUIREMENT-META-012` |
| **Constraint** | The Registered name for an external atomic Definition that records an imposed limit on acceptable technologies, dependencies, environments, resources, formats, or operation | `DSET-REQUIREMENT-META-008`, `DSET-REQUIREMENT-META-012` |
| **Contract** | The Registered name for an atomic relational Definition whose Relation record binds explicit participants across a boundary | `DSET-REQUIREMENT-META-008`, `DSET-REQUIREMENT-META-014` |
| **Implementation Decision** | The Registered name for an internal atomic Method that selects a material architecture, structure, algorithm, data, tooling, or operating approach | `DSET-REQUIREMENT-META-008`, `DSET-REQUIREMENT-META-012` |
| **Constitutional invariant** | A technology-independent rule that governs multiple responsibility boundaries or defines a boundary between them | `DSET-REQUIREMENT-META-022` |
| **DSET layer** | One ordered responsibility boundary that owns a distinct class of project concerns | `DSET-REQUIREMENT-META-023`, `DSET-REQUIREMENT-META-030` |
| **Layer authority flow** | The forward order in which an earlier DSET layer constrains or refines a later DSET layer | `DSET-REQUIREMENT-META-023`, `DSET-REQUIREMENT-META-025` |
| **Layer dependency** | A consumption edge from one DSET layer to itself or an earlier DSET layer | `DSET-REQUIREMENT-META-025` |
| **Layer handoff** | The declared input, output, entry criteria, exit criteria, and failure behavior between two adjacent DSET layers | `DSET-REQUIREMENT-META-024` |
| **Work Area** | A declared repository-relative folder that bounds Scope path resolution without implying code, deployability, or a particular architecture | `DSET-REQUIREMENT-META-011` |
| **Evergreen document** | A thin, reasoned, mutable Governed artifact that presents current meaning while returning every summarized claim directly to Atomic records | `DSET-REQUIREMENT-META-020`, `DSET-REQUIREMENT-META-033` |
| **Governance surface** | A named optional Governed artifact with `evergreen` or `maintained` Revision mode whose activation creates currentness or gate obligations | `DSET-REQUIREMENT-META-033` |
| **Project truth** | Active authoritative Atomic records, current applicable Evergreen documents, and applicable maintained Governed artifacts | `DSET-REQUIREMENT-META-020`, `DSET-REQUIREMENT-META-026`, `DSET-REQUIREMENT-META-028`, `DSET-REQUIREMENT-META-033` |
| **Exploration Mode** | A session state that permits candidate reasoning without creating a Governed artifact until explicit operator acceptance | `DSET-REQUIREMENT-META-021`, `DSET-REQUIREMENT-META-032` |
| **Design** | Internal structure and logic selected to satisfy accepted Requirements and Contracts | `DSET-REQUIREMENT-META-008`, `DSET-REQUIREMENT-META-017` |
| **Implementation plan** | An ordered Method for realizing accepted Project truth and Design | `DSET-REQUIREMENT-META-001` |
| **Test plan** | An evergreen Method that organizes deterministic check obligations and their Atomic records | `DSET-REQUIREMENT-META-001`, `DSET-REQUIREMENT-META-002`, `DSET-REQUIREMENT-META-007` |
| **Evaluation plan** | An evergreen Method that organizes qualitative, probabilistic, statistical, or model-judged obligations and their Atomic records | `DSET-REQUIREMENT-META-001`, `DSET-REQUIREMENT-META-002`, `DSET-REQUIREMENT-META-007` |
| **Runtime risk profile** | A selection of recovery and operational semantics triggered by persistence, retry, concurrency, or external effects | `DSET-REQUIREMENT-META-003`, `DSET-REQUIREMENT-META-006`, `DSET-REQUIREMENT-META-029` |
| **Durability topology** | A selection of authoritative files, a local database, or external backing services based on deployment, write volume, and concurrency | `DSET-REQUIREMENT-META-003`, `DSET-REQUIREMENT-META-006`, `DSET-REQUIREMENT-META-029` |

## Cross-entity relations

| Relation | Source | Target | Atomic sources |
|---|---|---|---|
| `orders` | Layer authority flow | DSET layer | `DSET-REQUIREMENT-META-023`, `DSET-REQUIREMENT-META-025` |
| `consumes` | Layer dependency | DSET layer | `DSET-REQUIREMENT-META-025` |
| `connects` | Layer handoff | DSET layer | `DSET-REQUIREMENT-META-024` |
| `scopes` | Work Area | Governed artifact | `DSET-REQUIREMENT-META-011` |
| `summarizes` | Evergreen document | Atomic record | `DSET-REQUIREMENT-META-020` |
| `constrains` | Contract | Design | `DSET-REQUIREMENT-META-008` |
| `realizes` | Implementation plan | Design | `DSET-REQUIREMENT-META-001` |
| `organizes` | Test plan or Evaluation plan | Atomic record | `DSET-REQUIREMENT-META-002`, `DSET-REQUIREMENT-META-007` |

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
- **DSET-INVARIANT-META-005:** Every governed artifact has exactly one value on each routing axis. Names, folders, filename tokens, and workflow position cannot infer or override that route. Sources: `DSET-REQUIREMENT-META-012` and `DSET-REQUIREMENT-META-018`.
- **DSET-INVARIANT-META-006:** The routing matrix is sparse. A route has zero or one registered name, and an empty cell is valid; DSET does not create placeholders to complete a Cartesian product. Source: `DSET-REQUIREMENT-META-013`.
- **DSET-INVARIANT-META-007:** `internal` governance is mandatory. A project may enable `external` and `relation` governance independently when its boundaries require them. Sources: `DSET-REQUIREMENT-META-012` and `DSET-REQUIREMENT-META-018`.
- **DSET-INVARIANT-META-008:** A Relation record declares a relation kind and at least two role-bearing endpoints. Each endpoint independently declares internal or external origin; endpoint origin is not another artifact-routing axis. Source: `DSET-REQUIREMENT-META-014`.
- **DSET-INVARIANT-META-009:** Scope path is project-relative structural context, not a fourth semantic routing axis. The current project is ambient and never repeated inside the path; every scope-dependent DSET artifact or run resolves against the repository-level scope or one or more declared Work Areas. Sources: `DSET-REQUIREMENT-META-011` and `DSET-REQUIREMENT-META-015`.
- **DSET-INVARIANT-META-010:** Registered names are interface vocabulary for valid routes, not ontological parents or children. Requirement, Constraint, Contract, and Implementation Decision therefore do not require a Decision-centered name hierarchy. Sources: `DSET-REQUIREMENT-META-008`, `DSET-REQUIREMENT-META-009`, and `DSET-REQUIREMENT-META-018`.
- **DSET-INVARIANT-META-011:** The development feedback cycle is Inquiry → Definition → Rationale → Method → Implementation → Observation → Inquiry. A record may enter at any justified role; the flow does not determine its identity. Sources: `DSET-REQUIREMENT-META-001` and `DSET-REQUIREMENT-META-016`.
- **DSET-INVARIANT-META-012:** Generated Code is an internal evergreen Implementation only when it is a reproducible current projection with generator and source provenance. Hand-maintained executable truth is an internal maintained Implementation. Source: `DSET-REQUIREMENT-META-017`.
- **DSET-INVARIANT-META-013:** Outcome framing may describe an intended measurable state inside a Definition or Method, while an observed outcome is an Observation. Outcome is not a routing axis or mandatory registered name. Source: `DSET-REQUIREMENT-META-010`.
- **DSET-INVARIANT-META-014:** A Contract is an atomic relational Definition. Complete replacement requires an operator-accepted successor with `replacement_of`, followed by archive relocation of the predecessor. Implementation cannot rewrite it. Sources: `DSET-REQUIREMENT-META-008` and `DSET-REQUIREMENT-META-014`.
- **DSET-INVARIANT-META-015:** A Work Area declaration owns a scope boundary; session continuity may reference it but cannot define, modify, or replace it. Neither repository-level scope nor a Work Area implies code, a deployment unit, a service, a feature, or a module. Source: `DSET-REQUIREMENT-META-011`.
- **DSET-INVARIANT-META-016:** Authority, provenance, priority, lifecycle state, and applicability remain explicit metadata. None is inferred from an artifact route. Sources: `DSET-REQUIREMENT-META-012` and `DSET-REQUIREMENT-META-018`.
- **DSET-INVARIANT-META-017:** Exploration Mode creates no governed artifacts or governance commits. Only explicit operator acceptance closes it and authorizes durable emission. Source: `DSET-REQUIREMENT-META-021`.
- **DSET-INVARIANT-META-018:** Evergreen documents are thin semantic views, not compiled restatements. Atomic records remain the semantic authority. Source: `DSET-REQUIREMENT-META-020`.
- **DSET-INVARIANT-META-019:** A domain entity is defined only with entities already defined above it. References to later entities are connections recorded outside the definition. Source: `DSET-REQUIREMENT-META-020`.
- **DSET-INVARIANT-META-020:** Every stateful domain entity declares identity, invariants, status meanings, entry and exit criteria, transition authority, allowed transitions, required evidence, and applicable failure/recovery behavior. Source: `DSET-REQUIREMENT-META-020`.
- **DSET-INVARIANT-META-021:** Semantic provenance inside an evergreen document targets atomic records only. Links to evergreen documents or hubs are navigation only. Source: `DSET-REQUIREMENT-META-020`.
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
- **DSET-INVARIANT-META-033:** DSET starts atomic-first; named evergreen or maintained governance surfaces are optional and may be activated or deactivated without changing atomic authority. Source: `DSET-REQUIREMENT-META-033`.
- **DSET-INVARIANT-META-034:** Every semantic META change follows the closed constitutional amendment sequence from Exploration and explicit acceptance through impact mapping, eligibility and topology review, reasoned evergreen update, forward staleness propagation, verification, and fixed-point declaration. Source: `DSET-REQUIREMENT-META-034`.
