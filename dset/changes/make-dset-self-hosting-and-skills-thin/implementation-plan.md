# Implementation plan — Make DSET self-hosting and skills thin

- **Implementing PR:** pending

## Batch 0 — Invariant contract

- Refine the nine roadmap invariants for applicability, non-applicability, and rule-ID ownership.
- Add one candidate requirement and scenario per invariant.
- Reconcile one accepted methodology invariant and release-gated requirement per roadmap invariant.
- Add deterministic test mappings for exact behavior and separate eval mappings for interpretation and diagnostic usefulness.
- Run the current canonical validator and diff hygiene without claiming planned 0.2 mechanics pass.

## Later batches

Implement roadmap §0–§8 only after this contract is reviewable. Each batch must add failing proof before mechanics and must keep unfinished behavior out of public capability claims.

## Rollout and recovery

This batch adds no runtime migration or feature control. Revert the invariant-contract commits if review finds a faulty boundary. Any later change to an invariant, requirement, scenario, or proof mapping invalidates the contract review and requires fresh DSET validation.
