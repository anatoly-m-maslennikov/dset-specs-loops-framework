# Implementation plan — Bootstrap structure

- **Implementing PR:** [anatoly-m-maslennikov/dset-loops-framework#2](https://github.com/anatoly-m-maslennikov/dset-loops-framework/pull/2)

## Batch 1 — Project root contract

- Create manifest and root ownership documentation.
- Create active/archive, templates, and schemas roots.
- Verify YAML and diff hygiene.
- Evidence: commit `99a8fad` in the implementing PR.

## Batch 2 — Accepted methodology truth

- Add domain, requirements, public contract, deterministic test plan, and qualitative eval plan for the `methodology` package.
- Resolve all package-local links.
- Evidence: commit `fc7c5f4` in the implementing PR.

## Batch 3 — Dogfood the standard change

- Add the eight document artifacts, methodology delta, and proof-evidence directory for this bootstrap.
- Verify artifact count, links, and terminology.
- Evidence: commit `3b369da` in the implementing PR.

## Batch 4 — Repository navigation and handoff

- Link the project root from the repository README.
- Run the complete fresh structural validation.
- Record final local evidence while leaving PR/archive gates pending.
- Evidence: commits `d65a195` and `3d483f8` in the implementing PR.

## Rollout

Open a draft PR, record its repository-qualified identity, obtain required review, rerun verification after the last content change, reconcile the delta into accepted truth, archive inside the PR, and pass the applicable archive-readiness review before marking the PR ready for merge. The `documentation-v1-pending` profile uses the documented manual audit; a canonical command and generated traceability become mandatory only after executable enforcement is configured.
