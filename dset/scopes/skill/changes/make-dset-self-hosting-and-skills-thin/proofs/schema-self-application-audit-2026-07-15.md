# Schema and self-application audit — 2026-07-15

## Proof identity

- **Claim:** Current live DSET 0.3.1 surfaces use schema 1.2 terminology and
  ownership consistently, the framework self-applies the corrected delivery and
  governance contracts as far as implemented, and remaining adopter/runtime/
  hosted gaps are explicit.
- **Intended use:** Bound the current 0.3.1 correction and prevent partial
  self-application or historical evidence from being presented as readiness.
- **Producer/performed work:** Independent schema/link migration review,
  independent self-application/adopter review, and main-thread reconciliation.
- **Method/setup:** Inspect live project truth, active Change, schemas, runtime,
  templates, methodology/documentation, current Git refs, generated adopter,
  declared Your Harness pilot, and deferred Claudian evaluation; run DSET link
  and structural validation and preserve archives as historical evidence.
- **Context:** DSET candidate commit
  `8d24d36507357e1831eb4fcdf47e1eb1cf712dc3`, local branch `dev`, schema 1.2,
  product/package target 0.3.1, observed 2026-07-15.
- **Evidence polarity:** Supporting evidence and blocking gaps.
- **Currentness:** Historical and superseded after template, Decision,
  proof-currentness, intake, validation, and test changes. See the replacement
  [schema and self-application re-audit](schema-self-application-reaudit-2026-07-15.md).
- **Reopen when:** Any live schema/path/ID/Decision terminology, version,
  workspace mode, adopter, skill runtime, trace generator, or hosted PR head
  changes.
- **Unsupported uses:** This proof does not claim current hosted proof, external
  pilot adoption, Claudian adoption, completed five-skill runtime, RC readiness,
  or final release readiness.

## Migration result

- Live public methodology and documentation use `Decision`; legacy ADR wording
  remains only in explicit migration/history/provenance contexts.
- The former OpenSpec operationalization TODO is a short superseded pointer, not
  a competing live backlog.
- Active Change deltas connect to current layer-owned accepted IDs and retain
  only genuinely unaccepted additions. `DSET-PROBLEM-GOV-001` is resolved.
- Schema 1.2 is current in the version contract; schema 1.0/1.1 branches and
  archived Change evidence remain deliberate compatibility/history surfaces.
- GitHub-portable link/callout/details validation is part of `dset check`; no
  live broken Markdown link or unsupported Obsidian-only surface remains at the
  evaluated commit.

## Self-application matrix

| Target | Result | Evidence and limit |
|---|---|---|
| DSET framework repository | Partial pass | Schema 1.2 manifest, repository-owned rules, neutral Work Areas, integration-branch default, optional worktrees, validation, trace, and bounded self-hosting are applied. Missing public/runtime capabilities remain below. |
| Generated temporary adopter | Partial pass | Candidate materializes and validates one bounded schema 1.1 compatibility adopter. A second generated current-schema 1.2 adopter remains `DSET-PROBLEM-TOOL-002`. |
| `obsidian-your-harness` | Not adopted | It remains the declared first owned pilot but has no DSET schema 1.2 control plane or proof; roadmap §6 remains open. |
| Upstream Claudian | Not started as designed | It remains a later clean pinned read-only evaluation after the owned pilot, not an adopter claim. |

## Current blockers and questions

- `DSET-PROBLEM-TOOL-001`: published-validator assurance remains a declared
  degraded schema-transition boundary.
- `DSET-PROBLEM-TOOL-002`: no generated current-schema adopter.
- `DSET-PROBLEM-SKILL-001`: `dset`, `dset-release`, run writer, checkpoint, and
  resume runtime are incomplete.
- `DSET-PROBLEM-OPS-001`: no exact-current-head GitHub proof.
- Open design Questions are recorded in
  [`intake.yaml`](../../../../gov/intake.yaml); they add no accepted behavior.

## Delivery/version result

This project now self-applies local `dev` to remote `dev` to PR `dev` → `main`
as its default. `branch-worktree` remains an explicit per-Change option and
archived worktree Changes remain valid. The first coordinated release is the
corrected unpublished bootstrap candidate `0.3.1`; the generic bootstrap policy
requires an explicit first pre-1.0 target rather than hard-coding a framework
version for every adopter.
