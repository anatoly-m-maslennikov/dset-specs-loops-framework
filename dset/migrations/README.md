# Migrate an existing project to DSET 0.2 governance

The migration goal is exactly one writable `dset/` project-truth root with one editable governing document per normative rule ID. Existing agent guidance, project rules, specs, test plans, eval plans, implementation plans, ADRs, runbooks, and evidence are inputs; they do not remain competing writable authorities. The DSET product and Python package share candidate version `0.2.0`; schemas retain their independent v1 compatibility identity.

## 1. Inventory before writing

Record every existing artifact root, owner, current writer, consumers, accepted/current status, and retention decision in a copy of [`migration-map.template.yaml`](migration-map.template.yaml). Stop if two roots claim current truth for the same concern.

## 2. Choose package boundaries

Start with one package when one capability boundary is sufficient. Add `specs/global/` only when multiple real packages create cross-package invariants, contracts, end-to-end proof, or release gates.

## 3. Map artifacts without collapsing proof

| Existing surface | DSET owner |
|---|---|
| `AGENTS.md`, `CLAUDE.md`, or runtime instructions | Concise wrapper/hub pointing to registered local governing documents |
| Build, architecture, authoring, safety, and supportability rules | One registered file under the project's selected local governance layout |
| Accepted domain and behavioral specs | `dset/specs/packages/<package>/domain.md` and `spec.md` |
| APIs, events, schemas, formats | package `contracts.md` or linked implementation schema |
| Deterministic test plan | package or change `test-plan.md` |
| Probabilistic/qualitative evaluation | package or change `eval-plan.md` |
| Implementation plan and tasks | active `dset/changes/<change-id>/` |
| ADRs | existing ADR owner, bidirectionally linked to the DSET change and PR |
| Runbooks | registered project runbook/supportability owner linked from requirements and incidents |
| Old completed plans/evidence | retained read-only history with a migration-map pointer or imported archive when proof is sufficient |

Never rename deterministic tests to evals because they are automated. Never copy one rule into both old and new writable roots.

## 4. Create and verify

1. Run `dset new <change-id> --package <package-id> --profile standard` for the migration change.
2. Run `dset rules materialize <project-root> --source <framework-root> --profile core-v1` only after inventory and destination preflight pass.
3. Create accepted package truth from reviewed existing artifacts, not unfinished code assumptions.
4. Register each local governing owner and reduce old agent instructions/skills to concise pointers or wrappers.
5. Mark every old root `migrated-read-only`, `redirect`, `archive`, or `delete-after-verification` in the map.
6. Run `dset rules check`, `dset check`, and `dset verify` before disabling old writers.
7. Reconcile and archive the migration through its draft PR; only then make DSET the default writer.

## Framework updates after cutover

Run `dset rules diff --source <new-framework-root>` to compare new templates with local governing documents. Review the output as a proposed delta, edit local owners deliberately, and run `dset rules refresh` to record customization status. Never copy the framework template over a materialized local file. If a destination, owner, profile, or proof gate conflicts, keep the existing owner writable and leave the migration active.

## Candidate workflow rename

The unreleased 0.2 candidate renamed `dset-grill` to `dset-clarify` and `domain-grilling` to `domain-clarification`. Replace the generated wrapper directory and registry workflow/path together, then run `dset rules check`. The deprecated workflow ID intentionally fails closed instead of acting as a hidden alias. Archived v1 evidence retains the former name.

## Recovery

If verification fails, keep the migration change active and leave the previous accepted source writable. Do not partially switch writers. Correct the earliest mapping/spec defect, rerun proof, then perform the ownership cutover as one reviewed change.
