# Methodology META domain

This is one layer-owned fragment of the logical methodology package. Use the sibling layer hubs for connected definitions; this file owns only the entities and invariants below.

## Entities

| Entity | Definition |
|---|---|
| **Project truth** | Active authoritative atomic records, their current thin evergreen semantic views, and applicable maintained project artifacts |
| **Artifact route** | The independent `revision_mode`, `content_role`, and `governance_locus` values assigned to one governed artifact |
| **Revision mode** | How an artifact may change: `atomic` is an immutable accepted record; `evergreen` is a mutable thin current view; `maintained` is a mutable operative artifact |
| **Content role** | What the artifact contributes to the development cycle: `inquiry`, `definition`, `rationale`, `method`, `implementation`, or `observation` |
| **Governance locus** | What the artifact primarily governs: an `internal` project-owned non-relational subject, an `external` outside-owned non-relational subject, or a `relation` among explicit endpoints; it classifies the subject, not the project-owned carrier |
| **Scope path** | The independently resolved structural coordinate of an artifact, such as project, layer, feature, feature group, or a configured composition of them |
| **Registered name** | The optional human-facing name assigned one-to-one to an occupied route; it does not define the route or create a semantic name hierarchy |
| **Relation record** | An artifact whose governance locus is `relation` and whose primary subject is a typed relation among two or more explicit endpoints |
| **Relation endpoint** | A referenced participant in a Relation record, including its role and independently declared `internal` or `external` origin |
| **Requirement** | The registered name for an internal atomic Definition that states a required observable, verifiable result, capability, quality, prevention condition, or obligation |
| **Constraint** | The registered name for an external atomic Definition that records an imposed limitation on acceptable technologies, dependencies, environments, resources, formats, or operating limits |
| **Design** | The internal structure and logic chosen to satisfy accepted Requirements, Scenarios, and Contracts |
| **Implementation plan** | The ordered build and rollout sequence for realizing accepted truth and Design |
| **Test plan** | Evergreen Method view that organizes deterministic test obligations and their atomic sources |
| **Evaluation plan** | Evergreen Method view that organizes qualitative, probabilistic, statistical, or model-judged evaluation obligations and their atomic sources |
| **Runtime risk profile** | Selection of recovery and operational semantics triggered by persistence, retry, concurrency, or external effects |
| **Durability topology** | Selection of authoritative files, a local database, or external backing services based on deployment, write volume, and concurrency |
| **Contract** | The registered name for an atomic relational Definition that binds explicit participants across an internal or external boundary |
| **Implementation Decision** | The registered name for an internal atomic Method that selects a material architecture, design, algorithm, data, tooling, or operating approach |
| **Work Area** | A declared repository-relative folder that bounds DSET scope without implying code, deployability, or a particular architecture; it may contain local tools, deployable services, libraries, documentation, methodology, data, or mixed content |
| **Analysis Mode** | A session workflow state that permits exploration without governed artifact creation until explicit operator acceptance |
| **Evergreen document** | A thin, reasoned, mutable semantic view that makes the current domain or plan readable while linking every summarized claim directly to authoritative atomic records |

## Invariants

- **DSET-INVARIANT-META-001:** Test and Evaluation remain separate registered Methods, implementations, and Observation streams.
- **DSET-INVARIANT-META-002:** Runtime risk, durability topology, effect safety, language enforcement, and artifact governance are selected explicitly rather than inherited from one universal tool class.
- **DSET-INVARIANT-META-003:** Each durable concern has one authoritative owner; process memory and derived views are not independent truth.
- **DSET-INVARIANT-META-004:** Exact governance and recursion behavior remains deterministic test proof; agent interpretation, rule-following, navigation, and diagnostic usefulness remain separate eval proof.
- **DSET-INVARIANT-META-005:** Every governed artifact has exactly one value on each routing axis. Names, folders, filename tokens, and workflow position cannot infer or override that route.
- **DSET-INVARIANT-META-006:** The routing matrix is sparse. A route has zero or one registered name, and an empty cell is valid; DSET does not create placeholders to complete a Cartesian product.
- **DSET-INVARIANT-META-007:** `internal` governance is mandatory. A project may enable `external` and `relation` governance independently when its boundaries require them.
- **DSET-INVARIANT-META-008:** A Relation record declares a relation kind and at least two role-bearing endpoints. Each endpoint independently declares internal or external origin; endpoint origin is not another artifact-routing axis.
- **DSET-INVARIANT-META-009:** Scope path is structural context, not a fourth semantic routing axis. Every scope-dependent DSET artifact or run resolves against the repository-level scope or one or more declared Work Areas.
- **DSET-INVARIANT-META-010:** Registered names are interface vocabulary for valid routes, not ontological parents or children. Requirement, Constraint, Contract, and Implementation Decision therefore do not require a Decision-centered name hierarchy.
- **DSET-INVARIANT-META-011:** The development feedback cycle is Inquiry → Definition → Rationale → Method → Implementation → Observation → Inquiry. A record may enter at any justified role; the flow does not determine its identity.
- **DSET-INVARIANT-META-012:** Generated Code is an internal evergreen Implementation only when it is a reproducible current projection with generator and source provenance. Hand-maintained executable truth is an internal maintained Implementation.
- **DSET-INVARIANT-META-013:** Outcome framing may describe an intended measurable state inside a Definition or Method, while an observed outcome is an Observation. Outcome is not a routing axis or mandatory registered name.
- **DSET-INVARIANT-META-014:** A Contract is an atomic relational Definition. Complete replacement requires an operator-accepted successor with `replacement_of`, followed by archive relocation of the predecessor. Implementation cannot rewrite it.
- **DSET-INVARIANT-META-015:** A Work Area declaration owns a scope boundary; session continuity may reference it but cannot define, modify, or replace it. Neither repository-level scope nor a Work Area implies code, a deployment unit, a service, a feature, or a module.
- **DSET-INVARIANT-META-016:** Authority, provenance, priority, lifecycle state, and applicability remain explicit metadata. None is inferred from an artifact route.
- **DSET-INVARIANT-META-017:** Analysis Mode creates no governed artifacts or governance commits. Only explicit operator acceptance closes it and authorizes durable emission.
- **DSET-INVARIANT-META-018:** Evergreen documents are thin semantic views, not compiled restatements. Atomic records remain the semantic authority.
- **DSET-INVARIANT-META-019:** A domain entity is defined only with entities already defined above it. References to later entities are connections recorded outside the definition.
- **DSET-INVARIANT-META-020:** Every stateful domain entity declares identity, invariants, status meanings, entry and exit criteria, transition authority, allowed transitions, required evidence, and applicable failure/recovery behavior.
- **DSET-INVARIANT-META-021:** Semantic provenance inside an evergreen document targets atomic records only. Links to evergreen documents or hubs are navigation only.
