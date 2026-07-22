# Methodology META domain

This is one layer-owned fragment of the logical methodology package. Use the sibling layer hubs for connected definitions; this file owns only the entities and invariants below.

## Entities

| Entity | Definition |
|---|---|
| **Project truth** | Active Decision atoms and their mutable evergreen projections plus applicable QA definitions owned by one adopting project under `dset/` |
| **Requirement** | A direct Decision subtype for a required observable, verifiable behavior, result, capability, quality, prevention condition, or obligation |
| **Constraint** | A direct Decision subtype restricting acceptable technologies, dependencies, environments, resources, formats, or operating limits when no boundary participant relies on it as a Contract |
| **Design** | The internal structure and logic chosen to satisfy accepted Requirements, Scenarios, and Contracts |
| **Implementation plan** | The ordered build and rollout sequence for realizing accepted truth and Design |
| **Test plan** | Evergreen projection that organizes QA/Test atoms and their deterministic implementation/evidence obligations |
| **Evaluation plan** | Evergreen projection that organizes QA/Evaluation atoms and their qualitative, probabilistic, statistical, or model-judged implementation/evidence obligations |
| **Runtime risk profile** | Selection of recovery and operational semantics triggered by persistence, retry, concurrency, or external effects |
| **Durability topology** | Selection of authoritative files, a local database, or external backing services based on deployment, write volume, and concurrency |
| **Contract** | A direct Decision subtype for an operator-accepted obligation across an external or internal project boundary, such as a DDL, CSV/XLSX schema, OpenAPI/message/protocol, host package format, platform matrix, hosted-CI interface, or dependency policy |
| **Implementation Decision** | A direct Decision subtype for a material selected architecture, design, algorithm, data, tooling, or operating approach |
| **Work Area** | A declared repository-relative folder that bounds DSET scope without implying code, deployability, or a particular architecture; it may contain local tools, deployable services, libraries, documentation, methodology, data, or mixed content |

## Invariants

- **DSET-INVARIANT-META-001:** QA/Test and QA/Evaluation remain separate direct subtypes, implementations, and evidence streams.
- **DSET-INVARIANT-META-002:** Runtime risk, durability topology, effect safety, language enforcement, and artifact governance are selected explicitly rather than inherited from one universal tool class.
- **DSET-INVARIANT-META-003:** Each durable concern has one authoritative owner; process memory and derived views are not independent truth.
- **DSET-INVARIANT-META-004:** Exact governance and recursion behavior remains deterministic test proof; agent interpretation, rule-following, navigation, and diagnostic usefulness remain separate eval proof.
- **DSET-INVARIANT-META-005:** Contract is a direct Decision subtype. An emitted Contract atom is immutable and remains authoritative while active; a successor or retirement requires operator-accepted authority plus an explicit append-only lifecycle relation. Implementation cannot rewrite it. Ambiguity becomes a Question, incompatible active authority becomes a Question/Conflict, and observed nonconformance becomes a Problem.
- **DSET-INVARIANT-META-006:** Requirement, Constraint, Contract, and Implementation Decision are the only direct Decision subtypes. They own required results, solution restrictions, boundary obligations, and durable selected approaches respectively. User Story, Outcome, Scenario, and Invariant may structure Requirement prose or compatibility history but are not current semantic subtypes.
- **DSET-INVARIANT-META-007:** Outcome framing may describe intended measurable state change inside a Requirement or Evaluation, but an observed outcome is evidence and Outcome is not a current semantic subtype.
- **DSET-INVARIANT-META-008:** Every scope-dependent DSET artifact or run resolves against the repository-level scope or one or more declared Work Areas. A Work Area declaration owns that scope boundary; session continuity may reference it but cannot define, modify, or replace it. Neither repository-level scope nor a Work Area implies code, a deployment unit, a service, a feature, or a module.
