# Proposal — Make DSET self-hosting and skills thin

- **Change ID:** `make-dset-self-hosting-and-skills-thin`
- **Profile:** `standard`
- **Target package:** `methodology`
- **Implementing PR:** pending
- **Status:** in progress; roadmap §§0–§4 implemented locally, hosted proof pending

## Problem

DSET 0.2 must become self-hosting and let adopting repositories own their rules without turning skills, templates, installed copies, or agent memory into competing authorities. The roadmap states this intent, but accepted project truth does not yet define release applicability, bounded recursion, local rule ownership, wrapper limits, customization identity, or their proof boundaries precisely enough to govern implementation.

## Outcome

Implement the first bounded self-hosting fixed point: independent version semantics, repository-local rule authority, thin adaptive wrappers, explicit project-owned materialization/customization, and released-to-candidate-to-adopter validation. Keep deterministic tests and qualitative evals separate and retain later profile/pilot/release work as explicit open scope.

## Scope

- Precise framework-first applicability and bounded self-hosting termination.
- Repository-local normative rule authority and one editable owner per rule ID.
- Thin, unchanged wrappers that resolve and apply changed local rules.
- Fail-closed selection with valid justified non-applicability.
- Honest custom-profile identity.
- Separate deterministic tests and qualitative evals.
- Candidate accepted-truth IDs and package registration for the contract.
- Governance registry/schema/resolver, stable diagnostics, and aggregate validation.
- Thin canonical skills plus a complete former-rule ownership inventory.
- Versioned `core-v1` governing-document templates, materialization, customization, migration, and update comparison.
- Bounded released/candidate/framework/adopter self-hosting with failure-boundary tests.

## Non-goals

- TypeScript profile implementation or external pilots.
- Claudian evaluation, pinned distribution, complete qualitative evals, or release/archive work.
- Any claim that DSET 0.2 is adoption-ready before hosted fixed-point proof and the later roadmap gates pass.

## Risk

No adopter runtime or production-data behavior changes. Governance risk is medium: a faulty resolver, duplicate owner, silent template fallback, or recursive runner could misdirect agents. Stable diagnostics, local path containment, source digests, no-overwrite transactions, fixed-depth execution, explicit non-goals, and separate proof categories contain that risk. Repository delivery remains governed by the existing supportability runbook.
