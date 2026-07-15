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
- Three implemented specialist skill sources under `skills/`; the active DSET 0.3 Change owns the unimplemented five-skill release target.
- A coordinated DSET product/CLI-package release contract, with project-configured delivery and independent schema/profile/template compatibility versions.
- Active authoritative-boundary Contract records with explicit ownership, direction, conformance, compatibility, and lifecycle.

## Specification boundary surface

A User Story is optional accepted truth, not an intake queue. When present, `DSET-STORY-<NNN>` or `DSET-STORY-<LAYER>-<NNN>` records an actor or stakeholder, desired capability or outcome, value or purpose, and links to normative Requirements and applicable Scenarios. Absence is valid where no meaningful User Story exists. A User Story never substitutes for a Requirement; `STORY` remains its compact ID token.

Requirements own observable verifiable delivered behavior, results, and constraints; Scenarios own observable examples and edge cases. Decisions own consequential choices among alternatives with rationale, tradeoffs, and consequences, not every implementation detail. Design owns internal logic, implementation plans own build sequence, and Contracts own boundaries the project cannot choose or rewrite.

An Outcome is a measurable change in user, business, operational, or system state, not a delivered output or feature. `DSET-OUTCOME-<NNN>` or `DSET-OUTCOME-<LAYER>-<NNN>` records baseline, target, observation method/source, evaluation window, originating Problem or Opportunity links, relevant User Story links when present, and applicable Eval links. Requirements and their deterministic evidence prove delivered behavior; Outcome evidence shows whether that behavior had the intended effect. This model-only change defines the type without asserting a concrete Outcome.

## Non-contractual surfaces

Examples, diagrams, and cited candidates may evolve without compatibility guarantees when they do not change a requirement, invariant, artifact shape, or ownership boundary.

## Authoritative boundary contracts

A Contract is not implementation advice. It is an authoritative boundary that implementation must satisfy without rewriting. Every immutable Contract atom names its authority, source, exactly one version or digest, direction, producer, consumer, conformance rule, compatibility rule, priority, creation state, and any older Contract atoms it absorbs. Current lifecycle is derived from append-only events: `declared -> active -> absorbed` or `declared -> active -> retired`; only the named authority may emit an absorbing version or retirement event. Ambiguity creates a Question, incompatibility creates a Problem, and a Decision cannot override an active Contract.

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
