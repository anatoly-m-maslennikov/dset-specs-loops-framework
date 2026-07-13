# Implementation plan — DSET v1

- **Implementing PR:** pending

## Batch 1 — Change identity and provenance

- Create this change and push its first reviewable commit.
- Open a draft `dev → main` PR and replace pending PR references.
- Add third-party notices before adapting any external workflow ideas.
- IDs: DSET-V1-REQ-003/005; TEST-004/006.

## Batch 2 — Contracts and reusable artifacts

- Release schemas, change/package templates, baseline fixtures, and migration guidance.
- Backfill machine-readable manifests for the two archived session changes.
- IDs: DSET-V1-REQ-002/003; TEST-002/003/004; EVAL-004.

## Batch 3 — CLI and tests

- Implement the standard-library parser, model, diagnostics, validation, trace generation, scaffolding, verification, and guarded archive operation.
- Run unit tests and fixture tests on the repository.
- IDs: DSET-V1-REQ-001–004; TEST-001–005.

## Batch 4 — Focused skills

- Initialize and implement `dset-grill`, `dset-diagnose`, and `dset-prototype`.
- Validate frontmatter, UI metadata, portability, triggers, outputs, verification, and stop conditions.
- IDs: DSET-V1-REQ-005; TEST-006; EVAL-003.

## Batch 5 — Enforcement and current truth

- Add the stable CI gate and update the protected-main required check after it passes on the draft PR.
- Reconcile methodology requirements/test/eval plans and project configuration.
- Update repository navigation and replace completed roadmap items with durable links.
- IDs: DSET-V1-REQ-001–006; TEST-007/008; EVAL-001/002.

## Batch 6 — Evidence and archive

- Generate traceability from the real PR and prior PR/archive history.
- Run deterministic verification and qualitative evals; record bounded evidence.
- Move the verified change to the dated archive candidate, push it, rerun the canonical command against the real head, finalize evidence, and mark the PR ready only after all gates pass.
