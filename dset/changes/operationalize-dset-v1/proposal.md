# Proposal — Operationalize DSET v1

- **Change ID:** `operationalize-dset-v1`
- **Target package:** `methodology`
- **Implementing PR:** pending
- **Status:** proposed

## Problem

The repository has accepted methodology truth and two evidence-backed archives, but executable enforcement is still pending. Schemas and templates are placeholders, no canonical command validates the contract, no generated traceability index connects changes to real PR history, and the accepted focused skills are not released.

The project manifest also describes the repository as documentation-only even though GitHub Actions and branch rules now operate the production delivery path.

## Outcome

Release a dependency-light, cross-platform DSET v1 toolchain that can create, validate, verify, trace, and safely archive project changes. Backfill the repository's real PR and archive history, enforce the toolchain in CI, publish reusable assets and focused skills, and make supportability metadata reflect the hosted delivery automation.

## Scope

- Apache-2.0 provenance and third-party notice boundary before adaptation.
- Versioned project, change, package, and traceability schemas.
- Released templates for change packages and accepted package truth.
- Valid and invalid fixtures covering active, failed, archived, and malformed changes.
- A standard-library Python CLI with `new`, `check`, `verify`, `trace`, and `archive` commands.
- Deterministic unit and integration tests plus GitHub Actions enforcement.
- Generated `dset/traceability.yaml` using real PRs and archive evidence.
- Migration guidance for existing spec/test/eval/implementation roots.
- Repository-native `dset-grill`, `dset-diagnose`, and `dset-prototype` skills.
- Reconciled methodology truth, project manifest, navigation, and roadmap status.

## Non-goals

- Installing OpenSpec or adopting a competing writable artifact root.
- Requiring a third-party runtime package for the canonical validator.
- Running the Claudian/Your Harness pilot in this change.
- Creating a JavaScript/TypeScript enforcement profile without evidence from that repository.
- Treating generated traceability as a second owner of code diffs or GitHub state.

## Risk

Medium governance and automation risk. A validator defect can admit malformed archives or block valid work; archive and trace writes therefore require explicit commands, fixtures cover both pass and fail paths, and GitHub remains authoritative for PR state and workflow logs.
