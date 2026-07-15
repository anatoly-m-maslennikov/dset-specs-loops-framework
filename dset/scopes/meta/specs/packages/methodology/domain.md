# Methodology META domain

This is one layer-owned fragment of the logical methodology package. Use the sibling layer hubs for connected definitions; this file owns only the entities and invariants below.

## Entities

| Entity | Definition |
|---|---|
| **Project truth** | Accepted User Stories, Outcomes, Requirements, Scenarios, Contracts, and proof plans owned by one adopting project's layer fragments under `dset/scopes/<layer>/specs/` |
| **User Story** | Optional accepted truth that names an actor or stakeholder, a desired capability or outcome, its value or purpose, and links to the Requirements and Scenarios that make it normative and verifiable; its ID token is `STORY` |
| **Outcome** | A measurable change in user, business, operational, or system state, recorded with a baseline, target, observation method/source, evaluation window, and trace links; it is not a delivered output or feature |
| **Requirement** | A stable-ID statement of observable, verifiable delivered behavior, result, or constraint with at least one scenario or acceptance check |
| **Scenario** | An observable example or edge case that makes Requirement behavior concrete without prescribing internal logic |
| **Design** | The internal structure and logic chosen to satisfy accepted Requirements, Scenarios, and Contracts |
| **Implementation plan** | The ordered build and rollout sequence for realizing accepted truth and Design |
| **Test plan** | Deterministic proof for exact behavior, contracts, regressions, and machine gates |
| **Eval plan** | Probabilistic or qualitative proof using datasets/cases, criteria, rubrics, thresholds, and calibration |
| **Runtime risk profile** | Selection of recovery and operational semantics triggered by persistence, retry, concurrency, or external effects |
| **Durability topology** | Selection of authoritative files, a local database, or external backing services based on deployment, write volume, and concurrency |
| **Contract** | A versioned non-choosable authoritative boundary, such as an existing DDL, required CSV/XLSX schema, supplied OpenAPI/message/protocol, host package format, platform matrix, hosted-CI interface, or dependency policy; implementation conforms to it, and only its named authority may issue a superseding version |
| **Work Area** | A declared repository-relative folder that bounds DSET scope without implying code, deployability, or a particular architecture; it may contain local tools, deployable services, libraries, documentation, methodology, data, or mixed content |

## Invariants

- **DSET-INVARIANT-META-001:** Deterministic tests and probabilistic/qualitative evals remain separate artifacts and evidence streams.
- **DSET-INVARIANT-META-002:** Runtime risk, durability topology, effect safety, language enforcement, and artifact governance are selected explicitly rather than inherited from one universal tool class.
- **DSET-INVARIANT-META-003:** Each durable concern has one authoritative owner; process memory and derived views are not independent truth.
- **DSET-INVARIANT-META-004:** Exact governance and recursion behavior remains deterministic test proof; agent interpretation, rule-following, navigation, and diagnostic usefulness remain separate eval proof.
- **DSET-INVARIANT-META-005:** An active Contract remains the authoritative implementation boundary until its named authority issues a superseding version or retires it. Implementation and Decisions cannot rewrite it: ambiguity becomes a Question, incompatibility becomes a Problem, and lifecycle is limited to `declared -> active -> superseded` or `declared -> active -> retired`.
- **DSET-INVARIANT-META-006:** A User Story is optional accepted truth and never an intake queue or a substitute for a normative verifiable Requirement. User Stories own actor, desired outcome, and value context; Requirements own observable verifiable delivered behavior, results, and constraints; Scenarios own observable examples and edge cases; Decisions own consequential choices among alternatives; Design owns internal logic; implementation plans own build sequence; and Contracts own non-choosable boundaries.
- **DSET-INVARIANT-META-007:** An Outcome is accepted truth, not an intake item, and owns a measurable change in user, business, operational, or system state without relabeling a delivered output or feature as impact. Requirements define delivered behavior; Outcome evidence, evaluated against a recorded baseline, target, observation method/source, and window, shows whether that behavior had the intended effect.
- **DSET-INVARIANT-META-008:** Every scope-dependent DSET artifact or run resolves against the repository-level scope or one or more declared Work Areas. A Work Area declaration owns that scope boundary; session continuity may reference it but cannot define, modify, or replace it. Neither repository-level scope nor a Work Area implies code, a deployment unit, a service, a feature, or a module.
