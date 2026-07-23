# Methodology META public contract

## Inputs

- Domain and product decisions accepted by DSET maintainers.
- Evidence from implementation, tests, evals, pilots, and defect repair.
- External sources used as provenance or candidates for adaptation.
- Language/ecosystem evidence used to create or revise applied gate profiles.

## Outputs

- GitHub-portable reusable framework source under `10_project/` and the ordered
  `11_layer_meta/` through `16_layer_ops/` product layers.
- One project-local installed methodology under
  `.dset/000_dset_methodology/`, distinct from applied artifacts.
- Independently selected implementation-language and artifact-governance
  profiles, including the `documentation-v1` catalog in
  `.dset/dset_settings.toml`.
- Applied project-wide truth under `.dset/100_project/`, applied layer truth
  under `.dset/101_layer_meta/` through `.dset/106_layer_ops/`, and Version
  lifecycle artifacts under `.dset/150_versions/`.
- Versioned schemas, templates, fixtures, migration guidance, provenance, and
  generated traceability in their configured methodology, applied, or runtime
  owners.
- The `dset` CLI through `python -m dset_toolchain` and an installable console entry point.
- Five implemented repository-native source wrappers under `skills/`; runtime,
  host-distribution, cross-platform, and publication claims remain separately
  gated.
- A coordinated DSET product/CLI-package release contract, with project-configured delivery and independent schema/profile/template compatibility versions.
- Active authoritative-boundary Contract records with explicit ownership, direction, conformance, compatibility, and lifecycle.

## Specification boundary surface

Decision is the only authority Type. Its direct subtypes are Requirement,
Constraint, Contract, and Implementation Decision. Requirement owns required
observable results selected by the project or operator; Constraint records an
externally imposed limitation the project must obey; Contract owns boundary
obligations; Implementation Decision owns material selected architecture,
design, algorithm, data, tooling, or operating approaches.

User Stories, Outcomes, Scenarios, and Invariants may structure Requirement
prose, analysis, or compatibility history. They do not create more semantic
subtypes. Independently enforceable claims are separate Requirement atoms.

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
