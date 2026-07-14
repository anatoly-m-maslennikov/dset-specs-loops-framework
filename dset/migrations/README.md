# Migrate an existing project to DSET v1

The migration goal is exactly one writable `dset/` project-truth root. Existing specs, test plans, eval plans, implementation plans, ADRs, and historical evidence are inputs; they do not remain competing writable authorities.

## 1. Inventory before writing

Record every existing artifact root, owner, current writer, consumers, accepted/current status, and retention decision in a copy of [`migration-map.template.yaml`](migration-map.template.yaml). Stop if two roots claim current truth for the same concern.

## 2. Choose package boundaries

Start with one package when one capability boundary is sufficient. Add `specs/global/` only when multiple real packages create cross-package invariants, contracts, end-to-end proof, or release gates.

## 3. Map artifacts without collapsing proof

| Existing surface | DSET owner |
|---|---|
| Accepted domain and behavioral specs | `dset/specs/packages/<package>/domain.md` and `spec.md` |
| APIs, events, schemas, formats | package `contracts.md` or linked implementation schema |
| Deterministic test plan | package or change `test-plan.md` |
| Probabilistic/qualitative evaluation | package or change `eval-plan.md` |
| Implementation plan and tasks | active `dset/changes/<change-id>/` |
| ADRs | existing ADR owner, bidirectionally linked to the DSET change and PR |
| Old completed plans/evidence | retained read-only history with a migration-map pointer or imported archive when proof is sufficient |

Never rename deterministic tests to evals because they are automated. Never copy one rule into both old and new writable roots.

## 4. Create and verify

1. Run `dset new <change-id> --package <package-id> --profile standard` for the migration change.
2. Create accepted package truth from reviewed existing artifacts, not unfinished code assumptions.
3. Mark every old root `migrated-read-only`, `redirect`, `archive`, or `delete-after-verification` in the map.
4. Run `dset check` and `dset verify` before disabling old writers.
5. Reconcile and archive the migration through its draft PR; only then make DSET the default writer.

## Recovery

If verification fails, keep the migration change active and leave the previous accepted source writable. Do not partially switch writers. Correct the earliest mapping/spec defect, rerun proof, then perform the ownership cutover as one reviewed change.
