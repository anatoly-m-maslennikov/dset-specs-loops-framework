# Proposal — Make DSET self-hosting and skills thin

- **Change ID:** `make-dset-self-hosting-and-skills-thin`
- **Profile:** `standard`
- **Target package:** `methodology`
- **Implementing PR:** [anatoly-m-maslennikov/dset-specs-loops-framework#9](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/9)
- **Status:** in progress; roadmap §§0–§4 implemented and proven locally plus in hosted CI

## Problem

DSET 0.2 must become self-hosting and let adopting repositories own their rules without turning skills, templates, installed copies, or agent memory into competing authorities. It also needs a small coherent skill surface and a release cycle that cannot reach `1.0.0` by arithmetic. The roadmap states the intent, but accepted project truth does not yet define release applicability, bounded recursion, local rule ownership, wrapper limits, orchestration, run evidence, version transitions, RC/final readiness, or their proof boundaries precisely enough to govern implementation.

## Outcome

Implement the first bounded self-hosting fixed point and finalize the next contracts: coordinated pre-1.0 product/package releases, repository-local rule authority, five thin adaptive wrappers, one primary lifecycle orchestrator, bounded local run evidence, and guarded release preparation/publication. Keep deterministic tests and qualitative evals separate and retain the TypeScript profile, pilots, distribution, and release mechanics as explicit open implementation scope.

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
- Exactly five core user-facing skills, with `dset` as the primary orchestrator and `dset-release` as the explicit release boundary.
- Machine-local bounded skill-run records that inform but never own next-step decisions.
- A complete SemVer-compatible bootstrap, pre-1.0, RC/final, and post-1.0 transition policy for each configured release PR.
- Separate pre-merge preparation, post-merge publication, RC, and final-1.0 readiness contracts.
- Coordinated product/package versions with independent schema/profile compatibility versions.
- Same-model/same-effort delegation by default, medium useful fan-out, and explicit deviation reporting.
- Low/medium/high budget profiles based on expected completed-task cost rather than token price alone.
- One project-owned problem/opportunity/question intake registry with stable layer IDs, Decision as the entity and Decision record as its canonical artifact, tasks kept inside accepted Changes, and the possible Action entity tracked only as a project open question.
- Concrete conformance contracts for installable host-native skills, declared macOS/native-Windows/WSL/Linux applicability, dependency provenance and bounded exceptions, and real protected GitHub delivery evidence.
- One measurable DSET 0.2 adoption-readiness Outcome with baseline, target, source/method, window, and proof links; features and task completion remain contributing outputs rather than the Outcome.
- Six deferred product-practice Questions covering Journey, Actor/Persona, Hypothesis/Experiment, prioritization, feedback/analytics, and generated roadmap/release views, without introducing new artifact types or queues.

## Non-goals

- TypeScript profile implementation or external pilots.
- Claudian evaluation, pinned distribution, complete qualitative evals, release automation, or archive work.
- Any claim that `dset`, `dset-release`, run records, automated version transitions, or DSET 0.2 adoption readiness are implemented before their later deterministic/eval/hosted gates pass.

## Risk

No adopter runtime or production-data behavior changes. Governance risk is medium: a faulty resolver, duplicate owner, silent template fallback, or recursive runner could misdirect agents. Stable diagnostics, local path containment, source digests, no-overwrite transactions, fixed-depth execution, explicit non-goals, and separate proof categories contain that risk. Repository delivery remains governed by the existing supportability runbook.
