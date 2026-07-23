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
  profiles, including project-selected artifact-routing loci in
  `.dset/dset_settings.toml`.
- Applied project-wide truth under `.dset/100_project/`, applied layer truth
  under `.dset/101_layer_meta/` through `.dset/106_layer_ops/`, and Version
  lifecycle artifacts under `.dset/150_versions/`.
- Thin evergreen semantic views that expose current flows, ordered entities,
  lifecycle models, and direct atomic provenance without duplicating atomic
  authority.
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

DSET routes every governed artifact through three independent axes:
`revision_mode`, `content_role`, and `governance_locus`. The complete values are:

- `revision_mode`: `atomic`, `evergreen`, or `maintained`;
- `content_role`: `inquiry`, `definition`, `rationale`, `method`,
  `implementation`, or `observation`;
- `governance_locus`: `internal`, `external`, or `relation`.

Internal governance is mandatory. External and relational governance are
independently optional. Scope path remains structural context outside this
semantic matrix.

Each occupied route has at most one registered human-facing name, and each name
maps to exactly one route. The name does not establish an ontology, infer a
route, or create a semantic name hierarchy.
Requirement maps to atomic Definition/internal, Constraint to atomic
Definition/external, Contract to atomic Definition/relation, and Implementation
Decision to atomic Method/internal.

User Stories, Outcomes, Scenarios, and Invariants may structure artifact prose,
analysis, or compatibility history. Independently enforceable claims remain
separate atomic records.

## Layer constitution boundary

DSET exposes one ordered layer constitution:
`META → GOV → TOOL → SKILL → IMPL → OPS`.

META owns technology-independent invariants and inter-layer semantics. GOV
owns governed carriers. TOOL owns executable enforcement. SKILL owns thin
provider-neutral orchestration. IMPL owns development realization. OPS owns
post-implementation delivery and operation.

Authority and refinement flow forward; later layers consume earlier authority.
Every adjacent handoff declares inputs, outputs, entry criteria, exit criteria,
and blocker behavior. Feedback may create a new Inquiry through Exploration
Mode, but it cannot govern an earlier layer.

Atomic sources: `DSET-REQUIREMENT-META-022`,
`DSET-REQUIREMENT-META-023`, `DSET-REQUIREMENT-META-024`, and
`DSET-REQUIREMENT-META-025`.

## Evergreen document boundary

Evergreen documents are reasoned current views rather than compiled
restatements. Their semantic source links target atomic records only.
Evergreen-to-evergreen and hub links are navigation and cannot establish
semantic provenance. Refresh occurs on demand after accepted atomic change and
before a downstream gate requires a current view.

## Non-contractual surfaces

Examples, diagrams, and cited candidates may evolve without compatibility guarantees when they do not change a requirement, invariant, artifact shape, or ownership boundary.

## Authoritative boundary contracts

A Contract is an atomic relational Definition, not implementation advice. Every
Contract names its operator-accepted source, version or digest, relation kind,
role-bearing endpoints, direction, conformance, compatibility, priority,
creation state, and archived predecessors. Each endpoint independently declares
internal or external origin. Implementation cannot rewrite the Contract.
Ambiguity creates an Inquiry, incompatible active authority creates a Conflict,
and observed nonconformance creates a Problem. Change requires explicit
precedence or an operator-accepted replacement Contract.

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
