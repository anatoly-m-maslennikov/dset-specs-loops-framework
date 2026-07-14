# Implementation plan — Make DSET self-hosting and skills thin

- **Implementing PR:** [anatoly-m-maslennikov/dset-specs-loops-framework#9](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/9)

## Batch 0 — Invariant contract — complete

- Refine the nine roadmap invariants for applicability, non-applicability, and rule-ID ownership.
- Add one candidate requirement and scenario per invariant.
- Reconcile one accepted methodology invariant and release-gated requirement per roadmap invariant.
- Add deterministic test mappings for exact behavior and separate eval mappings for interpretation and diagnostic usefulness.
- Run the current canonical validator and diff hygiene without claiming planned 0.2 mechanics pass.

## Batch 1 — Version, bootstrap, and governance — complete

- Publish independent framework, Python-package, and schema version semantics without rewriting archived v1 evidence.
- Select `core-v1` in the project manifest and materialize the framework repository's local governing documents.
- Add the governance schema, stable diagnostics, root discovery, read-only workflow resolution, explicit customization refresh, and source-profile diff.
- Make `dset check` and `dset verify` validate selected governance.

## Batch 2 — Thin wrappers and materialization — complete

- Inventory every former skill rule and assign one registered owner.
- Reduce the three skills to trigger/bootstrap/resolution/authorization/handoff wrappers.
- Add versioned `core-v1` templates, explicit materialization, no-overwrite behavior, migration mapping, and generated-wrapper identity proof.

## Batch 3 — Bounded self-hosting — complete

- Extract the pinned released validator from Git history and use it to check the candidate repository.
- Use the candidate to check this repository, create and check one temporary adopter, mutate one local rule, preserve wrapper bytes, and stop recursion.
- Corrupt each bootstrap boundary and assert the earliest stable failure.
- Run the same fixed point on the pushed PR head in hosted CI and preserve the shallow-checkout corrective loop.

## Batch 4 — Skill topology and release-cycle contract — specification complete

- Define the five-skill core surface and make `dset` the only general lifecycle/next-step entrypoint.
- Define bounded ignored skill-run evidence and its non-authoritative relationship to repository/Git/hosted state.
- Replace decimal version arithmetic with normal/small integer-component transitions and reserve `1.0.0-rc.N` plus `1.0.0` for fully working release gates.
- Coordinate the product and CLI package release while retaining schema/profile/template compatibility versions independently.
- Separate pre-merge release preparation from post-merge tag/GitHub Release publication.
- Run three independent high-effort specification reviews, reconcile blocking findings, and preserve bounded evidence.

## Later batches

Implement the Batch 4 orchestration/run/release mechanics and roadmap §§5–§10 for the TypeScript profile, owned Your Harness pilot, clean-room Claudian evaluation, complete tests/evals, and pinned distribution. Keep unfinished behavior out of public capability claims.

## Rollout and recovery

Governance materialization refuses existing destinations and cleans up partial copies. Repository-local rule edits require explicit customization refresh and never pull invisible template updates. Revert the affected logical commit if review finds a faulty boundary; any later invariant, requirement, scenario, registry, template, wrapper, or proof change invalidates current evidence and requires fresh DSET validation and self-hosting.
