# Proposal — Make DSET self-hosting and skills thin

- **Change ID:** `DSET-CHANGE-SKILL-001`
- **Profile:** `standard`
- **Target package:** `methodology`
- **Implementing PR:** [anatoly-m-maslennikov/dset-specs-loops-framework#9](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/9)
- **Status:** in progress; roadmap §§0–§4 implemented and proven locally;
  current exact-head hosted proof remains pending

## Problem

DSET 0.3 must become self-hosting and let adopting repositories own their rules without turning skills, templates, installed copies, or agent memory into competing authorities. It also needs a small coherent skill surface and a release cycle that cannot reach `1.0.0` by arithmetic. The roadmap states the intent, but accepted project truth does not yet define release applicability, bounded recursion, local rule ownership, wrapper limits, orchestration, run evidence, version transitions, RC/final readiness, or their proof boundaries precisely enough to govern implementation.

## Outcome

Implement the first bounded self-hosting fixed point and finalize the next contracts: coordinated pre-1.0 product/package releases, repository-local rule authority, thin adaptive wrappers for every lifecycle mode, one primary lifecycle orchestrator, bounded local run evidence, and guarded release preparation/publication. Keep deterministic tests and qualitative evals separate and retain the TypeScript profile, pilots, distribution, and release mechanics as explicit open implementation scope.

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
- One primary `dset` orchestrator plus one thin direct-entry wrapper for every stable lifecycle mode, with `dset-release` as the explicit release boundary.
- Machine-local bounded skill-run records that inform but never own next-step decisions.
- A complete SemVer-compatible bootstrap, pre-1.0, RC/final, and post-1.0 transition policy for each configured release PR.
- Separate pre-merge preparation, post-merge publication, RC, and final-1.0 readiness contracts.
- Coordinated product/package versions with independent schema/profile compatibility versions.
- Same-model/same-effort delegation by default, medium useful fan-out, and explicit deviation reporting.
- Low/medium/high budget profiles based on expected completed-task cost rather than token price alone.
- One project-owned semantic registry with stable IDs, exactly four Types and
  one direct subtype level, immutable Decision authority, tasks kept inside
  accepted Changes, and the possible Action entity tracked only as a project
  Question.
- Concrete conformance contracts for installable host-native skills, declared macOS/native-Windows/WSL/Linux applicability, dependency provenance and bounded exceptions, and real protected GitHub delivery evidence.
- One measurable DSET 0.3 adoption-readiness Outcome with baseline, target, source/method, window, and proof links; features and task completion remain contributing outputs rather than the Outcome.
- Six candidate 0.6 Roadmap items covering Journey, Actor/Persona, Hypothesis/Experiment, prioritization, feedback/analytics, and generated roadmap/release views, without introducing current atomic authority, new semantic Types, or queues.

## Non-goals

- TypeScript profile implementation or external pilots.
- Claudian evaluation, pinned distribution, complete qualitative evals, release automation, or archive work.
- Any claim that `dset`, `dset-release`, run records, automated version transitions, or DSET 0.3 adoption readiness are implemented before their later deterministic/eval/hosted gates pass.

## Risk

No adopter runtime or production-data behavior changes. Governance risk is medium: a faulty resolver, duplicate owner, silent template fallback, or recursive runner could misdirect agents. Stable diagnostics, local path containment, source digests, no-overwrite transactions, fixed-depth execution, explicit non-goals, and separate proof categories contain that risk. Repository delivery remains governed by the existing supportability runbook.
