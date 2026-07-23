# Implementation plan — DSET v1

- **Implementing PR:** [anatoly-m-maslennikov/dset-specs-loops-framework#7](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/7)

## Batch 1 — Change identity and provenance

- Create this change and push its first reviewable commit.
- Open a draft `dev → main` PR and replace pending PR references.
- Add third-party notices before adapting any external workflow ideas.
- IDs: `DSET-REQUIREMENT-TOOL-003`, `DSET-REQUIREMENT-SKILL-001`; `DSET-TEST-PLAN-TOOL-004`, `DSET-TEST-PLAN-SKILL-001`.

## Batch 2 — Contracts and reusable artifacts

- Release schemas, change/package templates, baseline fixtures, and migration guidance.
- Backfill machine-readable manifests for the two archived session changes.
- IDs: `DSET-REQUIREMENT-TOOL-002..003`; `DSET-TEST-PLAN-TOOL-002..004`; `DSET-EVAL-PLAN-GOV-006`.

## Batch 3 — CLI and tests

- Implement the standard-library parser, model, diagnostics, validation, trace generation, scaffolding, verification, and guarded archive operation.
- Run unit tests and fixture tests on the repository.
- IDs: `DSET-REQUIREMENT-TOOL-001..004`; `DSET-TEST-PLAN-TOOL-001..005`.

## Batch 4 — Focused skills

- Initialize and implement `dset-grill`, `dset-diagnose`, and `dset-prototype`.
- Validate frontmatter, UI metadata, portability, triggers, outputs, verification, and stop conditions.
- IDs: `DSET-REQUIREMENT-SKILL-001`; `DSET-TEST-PLAN-SKILL-001`; `DSET-EVAL-PLAN-SKILL-001`.

## Batch 5 — Enforcement and current truth

- Add the stable CI gate and update the protected-main required check after it passes on the draft PR.
- Reconcile methodology requirements/test/eval plans and project configuration.
- Update repository navigation and replace completed roadmap items with durable links.
- IDs: `DSET-REQUIREMENT-TOOL-001..004`, `DSET-REQUIREMENT-SKILL-001`, `DSET-REQUIREMENT-OPS-007`; `DSET-TEST-PLAN-OPS-007`, `DSET-TEST-PLAN-GOV-006`; `DSET-EVAL-PLAN-GOV-005`, `DSET-EVAL-PLAN-OPS-005`.

## Batch 6 — Evidence and archive

- Generate traceability from the real PR and prior PR/archive history.
- Run deterministic verification and qualitative evals; record bounded evidence.
- Move the verified change to the dated archive candidate, push it, rerun the canonical command against the real head, finalize evidence, and mark the PR ready only after all gates pass.
