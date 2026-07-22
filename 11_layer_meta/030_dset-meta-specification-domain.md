# Methodology META domain

This is one layer-owned fragment of the logical methodology package. Use the sibling layer hubs for connected definitions; this file owns only the entities and invariants below.

## Entities

| Entity | Definition |
|---|---|
| **Project truth** | Active Decision atoms and their mutable evergreen projections plus applicable QA definitions owned by one adopting project under `dset/` |
| **User Story** | A direct Requirement subtype naming an actor or stakeholder, desired capability or outcome, and value or purpose without absorbing linked acceptance criteria; its ID token remains `STORY` for compatibility |
| **Outcome** | A direct Requirement subtype defining an intended measurable change in user, business, operational, or system state with baseline, target, observation method/source, and evaluation window where applicable; the observed result is evidence |
| **Requirement** | A required observable, verifiable behavior, result, capability, quality, prevention condition, or obligation accepted as project authority |
| **Constraint** | A direct Requirement subtype restricting acceptable technologies, dependencies, environments, resources, formats, or operating limits when no boundary participant relies on it as a Contract |
| **Scenario** | A direct Requirement subtype defining a concrete accepted behavior or edge case through preconditions, interaction or event, and expected observable result; the executed run is work/evidence |
| **Invariant** | A direct Requirement subtype defining a condition that must always hold in its declared scope |
| **Design** | The internal structure and logic chosen to satisfy accepted Requirements, Scenarios, and Contracts |
| **Implementation plan** | The ordered build and rollout sequence for realizing accepted truth and Design |
| **Test plan** | Evergreen projection that organizes QA/Test atoms and their deterministic implementation/evidence obligations |
| **Evaluation plan** | Evergreen projection that organizes QA/Evaluation atoms and their qualitative, probabilistic, statistical, or model-judged implementation/evidence obligations |
| **Runtime risk profile** | Selection of recovery and operational semantics triggered by persistence, retry, concurrency, or external effects |
| **Durability topology** | Selection of authoritative files, a local database, or external backing services based on deployment, write volume, and concurrency |
| **Contract** | A direct Requirement subtype for an operator-accepted obligation across an external or internal project boundary, such as a DDL, CSV/XLSX schema, OpenAPI/message/protocol, host package format, platform matrix, hosted-CI interface, or dependency policy |
| **Work Area** | A declared repository-relative folder that bounds DSET scope without implying code, deployability, or a particular architecture; it may contain local tools, deployable services, libraries, documentation, methodology, data, or mixed content |

## Invariants

- **DSET-INVARIANT-META-001:** QA/Test and QA/Evaluation remain separate direct subtypes, implementations, and evidence streams.
- **DSET-INVARIANT-META-002:** Runtime risk, durability topology, effect safety, language enforcement, and artifact governance are selected explicitly rather than inherited from one universal tool class.
- **DSET-INVARIANT-META-003:** Each durable concern has one authoritative owner; process memory and derived views are not independent truth.
- **DSET-INVARIANT-META-004:** Exact governance and recursion behavior remains deterministic test proof; agent interpretation, rule-following, navigation, and diagnostic usefulness remain separate eval proof.
- **DSET-INVARIANT-META-005:** Contract is a direct Requirement subtype. An emitted Contract atom is immutable and remains authoritative while active; a successor or retirement requires operator-accepted authority plus an explicit append-only lifecycle relation. Implementation cannot rewrite it. Ambiguity becomes a Question, incompatible active authority becomes a Question/Conflict, and observed nonconformance becomes a Problem.
- **DSET-INVARIANT-META-006:** Constraint, Contract, User Story, Outcome, Scenario, and Invariant are sibling Requirement subtypes. Links between them never create a subtype path. User Story owns actor, desired capability/outcome, and value but not acceptance criteria; an empty-subtype Requirement owns residual observable obligations; Constraint narrows solutions without boundary reliance; Contract owns boundary obligations; Outcome owns intended measurable state change; Scenario owns a concrete accepted behavior example rather than its run; Invariant owns an always-true condition rather than evidence that it currently holds.
- **DSET-INVARIANT-META-007:** An Outcome is a direct Requirement subtype, not an intake item or observed result, and owns an intended measurable change in user, business, operational, or system state without relabeling a delivered output or feature as impact. Requirement evidence proves delivery; Outcome evidence, evaluated against its baseline, target, observation method/source, and window, shows whether delivery had the intended effect.
- **DSET-INVARIANT-META-008:** Every scope-dependent DSET artifact or run resolves against the repository-level scope or one or more declared Work Areas. A Work Area declaration owns that scope boundary; session continuity may reference it but cannot define, modify, or replace it. Neither repository-level scope nor a Work Area implies code, a deployment unit, a service, a feature, or a module.
