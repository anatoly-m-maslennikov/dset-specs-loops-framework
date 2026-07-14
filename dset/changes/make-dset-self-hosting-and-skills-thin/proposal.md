# Proposal — Make DSET self-hosting and skills thin

- **Change ID:** `make-dset-self-hosting-and-skills-thin`
- **Profile:** `standard`
- **Target package:** `methodology`
- **Implementing PR:** pending
- **Status:** in progress; invariant-contract batch

## Problem

DSET 0.2 must become self-hosting and let adopting repositories own their rules without turning skills, templates, installed copies, or agent memory into competing authorities. The roadmap states this intent, but accepted project truth does not yet define release applicability, bounded recursion, local rule ownership, wrapper limits, customization identity, or their proof boundaries precisely enough to govern implementation.

## Outcome

Define nine release invariants as observable requirements with stable scenarios and separate deterministic and qualitative proof mappings. Reconcile the invariant contract into candidate accepted methodology truth without claiming that the resolver, materializer, thin wrappers, or recursive gate are already implemented.

## Scope

- Precise framework-first applicability and bounded self-hosting termination.
- Repository-local normative rule authority and one editable owner per rule ID.
- Thin, unchanged wrappers that resolve and apply changed local rules.
- Fail-closed selection with valid justified non-applicability.
- Honest custom-profile identity.
- Separate deterministic tests and qualitative evals.
- Candidate accepted-truth IDs and package registration for the contract.

## Non-goals

- Governance registry/schema/resolver implementation.
- Skill refactoring or installation changes.
- Template materialization and migration commands.
- Recursive execution, TypeScript profile implementation, or external pilots.
- Any DSET 0.2 capability or release-readiness claim.

## Risk

No runtime or production-data behavior changes in this batch. Governance risk is medium because ambiguous invariants could either permit parallel rule stores or make profile-specific self-hosting impossible. Stable IDs, one-to-one scenarios, explicit non-goals, and proof-category separation contain that risk. Repository delivery remains governed by the existing supportability runbook.
