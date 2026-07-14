# Proposal — Bootstrap the DSET project structure

- **Change ID:** `bootstrap-dset-project-structure`
- **Target package:** `methodology`
- **Implementing PR:** [anatoly-m-maslennikov/dset-loops-framework#2](https://github.com/anatoly-m-maslennikov/dset-loops-framework/pull/2)
- **Status:** archived 2026-07-14 after pushed-head evals and the pending-profile manual readiness audit

## Problem

The repository defines a project-local DSET contract but does not itself use one. Framework decisions therefore live only in methodology prose and a large TODO, with no accepted package truth or bounded dogfood change.

## Outcome

Create a minimal, scalable `dset/` root for one package named `methodology`; capture current accepted truth; and record this bootstrap as an active standard change with eight document artifacts, requirement deltas, and verification evidence.

## Scope

- Project manifest and lifecycle ownership.
- One accepted package under `specs/packages/methodology/`.
- Active and archive change roots.
- Placeholder framework-owned template and schema roots.
- One bootstrap change that remains active until its dated candidate is pushed, remotely evaluated, and finalized through archive readiness.

## Non-goals

- Implementing the canonical validator or documentation enforcement profile.
- Creating a global spec layer before a second package exists.
- Creating Python or JavaScript/TypeScript source packages.
- Archiving without a repository-qualified PR identity.

## Risk

Low runtime risk; medium governance risk. A premature archive could present unmerged structure as accepted history, so PR and archive-readiness requirements remain hard gates.
