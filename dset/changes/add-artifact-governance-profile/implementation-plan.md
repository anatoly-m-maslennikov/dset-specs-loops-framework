# Implementation plan — Add artifact governance profiles

- **Implementing PR:** pending

## Batch 1 — Identity and accepted shape

- Open the draft PR and record its repository-qualified identity.
- Define the artifact-profile schema, repository adoption shape, requirements, tests, evals, and public document tree.
- IDs: ART-REQ-001–006; ART-TEST-001; ART-EVAL-004.

## Batch 2 — Public artifact architecture

- Add the documentation and methodology hubs.
- Add separate architecture, type, authoring, hub, applied-profile, maintenance, and rationale documents.
- Rework the root README into an area-level helicopter view without removing access to current framework surfaces.
- IDs: ART-REQ-002–004/006; ART-TEST-003/004; ART-EVAL-001–003.

## Batch 3 — Executable profile

- Add `dset/artifacts.yaml`, its JSON Schema, stable diagnostics, repository validation, and unit/fixture coverage.
- Activate `documentation-v1` independently from `python-v1` in `dset/dset.yaml` and the project schema.
- IDs: ART-REQ-001/002/005/006; ART-TEST-001/002/005.

## Batch 4 — Reconciliation and evidence

- Reconcile accepted methodology domain/spec/contracts/test/eval truth.
- Run canonical deterministic checks and independent qualitative evals; correct the earliest ambiguous artifact.
- Archive through PR identity, push the candidate, record final evidence, and hand off to protected merge.
- IDs: all requirements, tests, and evals.

## Rollout and recovery

The new profile is additive until the repository itself passes. If navigation or validator behavior regresses, keep the change active or revert the bounded PR before merge. Any later change to public hubs, registry structure, validator code, or accepted artifact rules invalidates earlier readiness evidence.
