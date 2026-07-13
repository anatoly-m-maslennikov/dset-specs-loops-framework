# Methodology delta specification

## ADDED — BOOT-REQ-001 Visible project root

The repository must keep project truth under the visible `dset/` root and reserve `.dset/` for future generated/local machine state.

**Scenario BOOT-SCN-001:** A new contributor opens `dset/README.md` and can identify accepted truth, active changes, archive history, templates, and schemas without private context.

## ADDED — BOOT-REQ-002 One explicit package

The bootstrap must register exactly one package, `methodology`, under `dset/specs/packages/methodology/`. It must not add `specs/global/` until cross-package ownership exists.

**Scenario BOOT-SCN-002:** The manifest resolves the `methodology` package to one current-truth root and reports `global_truth_root: null`.

## ADDED — BOOT-REQ-003 Standard change artifact set

A standard active change must contain eight document artifacts—proposal, test plan, eval plan, solution landscape, design, implementation plan, tasks, and verification—plus requirement deltas and optional proof evidence.

**Scenario BOOT-SCN-003:** A structural check distinguishes the eight documents from the `specs/` and `proofs/` evidence directories.

## ADDED — BOOT-REQ-004 PR-safe archival

The implementing PR must remain draft until fresh verification, current-truth reconciliation, and the applicable traceability and archive-readiness checks pass. With executable enforcement configured, its canonical command and generated traceability must pass. Under an explicit pending enforcement profile, verification must instead record the manual PR/link/archive audit and exact read-only checks without claiming unavailable CI or generation. Any later implementation/specification change invalidates prior archive readiness.

**Scenario BOOT-SCN-004:** With `Implementing PR: pending`, the bootstrap change remains under active `changes/` and cannot appear under `archive/`.

## ADDED — BOOT-REQ-005 Honest enforcement status

The manifest must expose the documentation enforcement profile and canonical command as pending until executable tooling exists.

**Scenario BOOT-SCN-005:** Public metadata cannot imply that a documentation gate or canonical validator is active when no such executable asset exists.
