# Implementation plan — Bootstrap structure

## Batch 1 — Project root contract

- Create manifest and root ownership documentation.
- Create active/archive, templates, and schemas roots.
- Verify YAML and diff hygiene.
- Evidence: commit `ef7b813`.

## Batch 2 — Accepted methodology truth

- Add domain, requirements, public contract, deterministic test plan, and qualitative eval plan for the `methodology` package.
- Resolve all package-local links.
- Evidence: commit `759bf8e`.

## Batch 3 — Dogfood the standard change

- Add the eight document artifacts, methodology delta, and proof-evidence directory for this bootstrap.
- Verify artifact count, links, and terminology.

## Batch 4 — Repository navigation and handoff

- Link the project root from the repository README.
- Run the complete fresh structural validation.
- Record final local evidence while leaving PR/archive gates pending.

## Rollout

Open a draft PR, record its repository-qualified identity, obtain required review, rerun verification after the last content change, reconcile the delta into accepted truth, archive inside the PR, pass archive-readiness CI, then mark the PR ready for merge.
