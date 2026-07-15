# Schema and self-application re-audit — 2026-07-15

## Proof identity

- **Claim:** At candidate
  `a6738bfed4c222f8e984d615a20be4a6e0d56767`, live DSET repository
  artifacts use the current schema/ID/Decision/path model without unresolved
  links or editor-only syntax, schema-aware templates scaffold correctly, and
  DSET self-application status is bounded honestly across declared targets.
- **Intended use:** Replace the earlier schema/self-application audit and stale
  invariant/Work Area Pass claims for current local review; not provide hosted,
  pilot, clean-room, archive, or release proof.
- **Producer/performed work:** Two independent high-effort subagent reviews
  covering schema/links and cross-repository self-application, plus main-thread
  targeted searches, repository inspections, corrective edits, regression
  tests, and a complete deterministic gate.
- **Method/setup:** Validate live DSET project truth, all public Markdown,
  distributed schemas/templates, accepted/delta ID ownership, generated trace,
  framework runtime, generated adopter, Your Harness checkout, and local
  Claudian checkout. Preserve archives, compatibility fixtures, provenance, and
  superseded pointers as explicitly historical surfaces.
- **Context:** DSET schema 1.2/product 0.3.1 on local `dev`; `origin/dev` remained
  at `30e5d8775091064a487e021d30da8a04b7f71c22`; observed 2026-07-15.
- **Evidence polarity:** Supporting local evidence with explicit blocking gaps.
- **Currentness:** Current for the evaluated implementation, governance,
  templates, tests, and repository-local target state. This proof record,
  candidate pointer, verification links, and trace refresh do not change those
  inputs.
- **Reopen when:** Live schema/path/ID/Decision terminology, distributed
  templates, Work Area/workspace behavior, validation/tests, rules, adopter
  generation, declared pilot checkout, or hosted branch/PR state changes.
- **Unsupported uses:** This proof does not claim published-validator
  compatibility, current-schema generated adoption, five-skill/runtime
  completion, Your Harness adoption, a clean pinned Claudian eval, current
  GitHub checks, archive readiness, or release readiness.

## Corrective migration result

- The active proposal now uses `DSET-CHANGE-SKILL-001` and does not claim current
  hosted proof.
- Roadmap §§8–9 no longer redeclare accepted Test/Eval IDs; they route to the
  layer-owned proof plans and active Change execution plans.
- Legacy and layered Change/package templates are separate, compatibility-
  labeled, and selected by repository layout. Focused legacy and schema 1.2
  scaffold regressions pass.
- The active Change contains a traceable neutral Decision record; comparison
  state remains separate from selection.
- Pre-layer/METH and 0.3.0 Work Area proofs are explicitly historical after
  their reopen conditions fired; this record replaces their current-use claims.
- Live Markdown links, schema `$id` paths, GitHub alert/details syntax, product
  identity, version surfaces, and generated trace pass. Remaining ADR terms and
  central paths occur only in migration, compatibility, provenance, negative
  tests, superseded pointers, or archives.

## Self-application matrix

| Target | Result | Current boundary |
|---|---|---|
| DSET framework repository | Partial pass | Schema 1.2 control plane, neutral Work Areas, repository-owned rules, integration-branch default, optional worktrees, schema-aware templates, validation, traceability, and bounded self-hosting pass. Published-validator, five-skill/runtime, eval, hosted, pilot, and release gaps remain. |
| Generated temporary adopter | Partial pass | Candidate still proves legacy schema 1.1 compatibility and local rule mutation only. `DSET-PROBLEM-TOOL-002` requires a separate current-schema 1.2 adopter. |
| `obsidian-your-harness` | Not adopted | Candidate returns `DSET-E900`; no DSET root exists. Existing `CLAUDE.md`/spec surfaces retain authority, Test/Eval ownership is not migrated, hosted workflows are disabled, and no DSET delivery/supportability lifecycle exists. This is `DSET-PROBLEM-GOV-004`, not a failed rollout claim. |
| Local upstream Claudian checkout | Not started as designed | Candidate returns `DSET-E900`; the checkout is a local feature branch rather than the future clean pinned upstream fixture. Roadmap §7 correctly defers it until after the owned pilot and prohibits upstream writes. |

## Intake disposition

Open blocking Problems are `DSET-PROBLEM-TOOL-001..002`,
`DSET-PROBLEM-SKILL-001`, `DSET-PROBLEM-OPS-001`, and
`DSET-PROBLEM-GOV-004`. The re-audit also registered
`DSET-QUESTION-GOV-006` for machine-readable proof closures and optional
Opportunities `DSET-OPPORTUNITY-GOV-001`, `DSET-OPPORTUNITY-TOOL-001`, and
`DSET-OPPORTUNITY-OPS-001` for generated currentness, compatibility, and
cross-repository adoption views. No new Story or Outcome is needed: the existing
adoption-readiness Outcome already owns the target state, and the active Change
owns execution.

## Deterministic gate

| Gate | Result |
|---|---|
| Ruff format/check | Pass; 29 files |
| mypy | Pass; 29 source files |
| Unit/fixture suite | Pass; 81 tests |
| `python -m dset_toolchain check .` | Pass |
| `python -m dset_toolchain rules check .` | Pass |
| `python -m dset_toolchain self-host .` | Candidate repository/adopter pass; wrapper unchanged; recursion stopped; released boundary remains `bootstrap-transition` |
| `python -m dset_toolchain trace . --check` | Pass |
| `git diff --check` | Pass |

The `uv` invocations emitted the known non-fatal project-environment lock
warning but completed successfully. No warning or degraded released-validator
result was converted into a pass.
