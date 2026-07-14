# Methodology delta specification

## ADDED — DSET-REQUIREMENT-GOV-001 Visible project root

The repository must keep project truth under the visible `dset/` root and reserve `.dset/` for future generated/local machine state.

**Scenario DSET-SCENARIO-GOV-001:** A new contributor opens `dset/README.md` and can identify accepted truth, active changes, archive history, templates, and schemas without private context.

## ADDED — DSET-REQUIREMENT-GOV-002 One explicit package

The bootstrap must register exactly one package, `methodology`, under `dset/specs/packages/methodology/`. It must not add `specs/global/` until cross-package ownership exists.

**Scenario DSET-SCENARIO-GOV-002:** The manifest resolves the `methodology` package to one current-truth root and reports `global_truth_root: null`.

## ADDED — DSET-REQUIREMENT-META-001 Standard change artifact set

A standard active change must contain eight document artifacts—proposal, test plan, eval plan, solution landscape, design, implementation plan, tasks, and verification—plus requirement deltas and optional proof evidence.

**Scenario DSET-SCENARIO-META-001:** A structural check distinguishes the eight documents from the `specs/` and `proofs/` evidence directories.

## ADDED — DSET-REQUIREMENT-OPS-001 PR-safe archival

The implementing PR must remain draft throughout a two-phase archive transaction. After fresh baseline verification and current-truth reconciliation, the change moves to an explicitly incomplete dated candidate and is pushed so remote checks can inspect the real PR head. An evidence-only commit records final proof and archived status after those checks pass. With executable enforcement configured, its canonical command and generated traceability must pass. Under an explicit pending enforcement profile, verification instead records the manual PR/link/archive audit and exact read-only checks without claiming unavailable CI or generation. Any later implementation/specification change invalidates prior archive readiness.

**Scenario DSET-SCENARIO-OPS-001:** With `Implementing PR: pending`, the bootstrap change remains under active `changes/` and cannot appear under `archive/`.

## ADDED — DSET-REQUIREMENT-GOV-003 Honest enforcement status

The manifest must expose the documentation enforcement profile and canonical command as pending until executable tooling exists.

**Scenario DSET-SCENARIO-GOV-003:** Public metadata cannot imply that a documentation gate or canonical validator is active when no such executable asset exists.
