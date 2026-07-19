# Methodology META public contract

## Inputs

- Domain and product decisions accepted by DSET maintainers.
- Evidence from implementation, tests, evals, pilots, and defect repair.
- External sources used as provenance or candidates for adaptation.
- Language/ecosystem evidence used to create or revise applied gate profiles.

## Outputs

- A GitHub-portable public methodology under `methodology/`.
- A repository navigation map in `README.md`, stable area hubs, and methodology document 00.
- Artifact architecture, type, authoring, hub, maintenance, and rationale references under `documentation/`.
- Independently selected implementation-language and artifact-governance profiles, including the `documentation-v1` registry under `dset/scopes/gov/artifacts.yaml`.
- Accepted package truth in layer-owned fragments under `dset/scopes/<layer>/specs/`.
- Bounded, PR-traceable Changes under `dset/scopes/<primary-layer>/changes/`.
- Versioned schemas, templates, fixtures, migration guidance, provenance, and generated traceability under `dset/`.
- The `dset` CLI through `python -m dset_toolchain` and an installable console entry point.
- Five implemented repository-native source wrappers under `skills/`; runtime,
  host-distribution, cross-platform, and publication claims remain separately
  gated.
- A coordinated DSET product/CLI-package release contract, with project-configured delivery and independent schema/profile/template compatibility versions.
- Active authoritative-boundary Contract records with explicit ownership, direction, conformance, compatibility, and lifecycle.

## Specification boundary surface

A User Story is a direct Decision subtype. When present, its stable `STORY`
compatibility ID records an actor or stakeholder, desired capability or
outcome, and value or purpose. It may link sibling Requirements, Outcomes,
Scenarios, Invariants, Contracts, and QA atoms, but is never nested beneath a
Requirement. Absence remains valid where no meaningful actor perspective
exists.

Requirement, Constraint, Contract, User Story, Outcome, Scenario, and Invariant
are sibling Decision subtypes. Requirement owns observable required results;
Constraint narrows solutions; Contract owns boundary obligations; User Story
owns actor/value intent; Outcome owns measurable state change; Scenario owns a
concrete behavior; and Invariant owns an always-true condition. Design and
implementation plan remain document roles rather than semantic Types.

Outcome is a direct Decision subtype for measurable user, business,
operational, or system state change, not a delivered output. Its stable
`OUTCOME` ID links baseline, target, observation method/source, evaluation
window, originating Problem or Question/Opportunity, sibling User Stories, and
QA/Evaluations. QA/Test evidence proves Requirement delivery; Outcome evidence
shows whether delivery had the intended effect.

## Non-contractual surfaces

Examples, diagrams, and cited candidates may evolve without compatibility guarantees when they do not change a requirement, invariant, artifact shape, or ownership boundary.

## Authoritative boundary contracts

A Contract is a direct Decision subtype, not implementation advice. Every
immutable Contract atom names its operator-accepted source, version or digest,
direction, provider, consumer, conformance, compatibility, priority, creation
state, and absorbed predecessors. Implementation cannot rewrite it. Ambiguity
creates a Question, incompatible active authority creates Question/Conflict,
and observed nonconformance creates Problem/Defect. Change requires explicit
precedence or an operator-accepted absorbing Contract.

## DSET-CONTRACT-META-001 — Repository Work Area declaration

| Field | Contract value |
|---|---|
| Authority | Accepted DSET methodology META package; each adopting repository owner supplies that repository's conforming declaration |
| Source | `DSET-REQUIREMENT-META-011` and this Contract record |
| Record version | `1.0` |
| Direction | Repository scope declaration → DSET artifacts, workflows, proof, runs, and handoffs |
| Producer | Adopting repository owner or authorized project governance writer |
| Consumer | DSET lifecycle, Change, proof, supportability, and session-continuity consumers |
| Conformance rule | Declare either repository-level scope or one or more existing repository-relative folders as Work Areas; allow local, deployable, library, documentation, methodology, data, and mixed content without requiring code or deployability; require scope-dependent consumers to resolve the current declaration |
| Compatibility rule | Content changes inside a Work Area do not change the boundary; a path rename, removal, or scope split/merge requires an explicit reviewed declaration update and refresh of affected references and evidence. Legacy or simple repositories may remain one repository-level scope |
| Lifecycle state | `active` |

Session continuity may store a bounded reference to a Work Area, but this
Contract and the adopting repository's accepted declaration remain authoritative.
A checkpoint cannot create, rename, reclassify, or supersede the boundary.
