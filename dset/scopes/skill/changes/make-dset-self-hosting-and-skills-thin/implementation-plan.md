# Implementation plan — Make DSET self-hosting and skills thin

- **Implementing PR:** [anatoly-m-maslennikov/dset-specs-loops-framework#9](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/9)

## Batch 0 — Invariant contract — complete

- Refine the nine roadmap invariants for applicability, non-applicability, and rule-ID ownership.
- Add one candidate requirement and scenario per invariant.
- Reconcile one accepted methodology invariant and release-gated requirement per roadmap invariant.
- Add deterministic test mappings for exact behavior and separate eval mappings for interpretation and diagnostic usefulness.
- Run the current canonical validator and diff hygiene without claiming planned 0.2 mechanics pass.

## Batch 1 — Version, bootstrap, and governance — complete

- Publish coordinated product/Python-package version semantics plus independent schema compatibility without rewriting archived v1 evidence.
- Select `core-v1` in the project manifest and materialize the framework repository's local governing documents.
- Add the governance schema, stable diagnostics, root discovery, read-only workflow resolution, explicit customization refresh, and source-profile diff.
- Make `dset check` and `dset verify` validate selected governance.

## Batch 2 — Thin wrappers and materialization — complete

- Inventory every former skill rule and assign one registered owner.
- Reduce the three skills to trigger/bootstrap/resolution/authorization/handoff wrappers.
- Add versioned `core-v1` templates, explicit materialization, no-overwrite behavior, migration mapping, and generated-wrapper identity proof.

## Batch 3 — Bounded self-hosting — degraded bootstrap transition

- Extract the pinned pre-transition validator from Git history and record its
  schema 1.2 rejection as degraded bootstrap assurance rather than a pass.
- Use the candidate to check this repository, create and check one temporary adopter, mutate one local rule, preserve wrapper bytes, and stop recursion.
- Corrupt each bootstrap boundary and assert the earliest stable failure.
- Keep candidate-to-repository and candidate-to-adopter proof mandatory, isolate
  temporary work outside the repository, and rerun exact-head hosted proof after
  the current branch is pushed.

## Batch 4 — Skill topology and release cycle — local implementation complete; native/hosted proof pending

- Define the five-skill core surface and make `dset` the only general lifecycle/next-step entrypoint.
- Implement and register all five thin source packages, including applicability-aware adopter materialization and recursive wrapper-identity proof.
- Define bounded ignored skill-run evidence and its non-authoritative relationship to repository/Git/hosted state.
- Package the governance templates and wrappers into a verified bootstrap bundle; add dry-run-first initialization for empty or existing repositories with collision stops, rollback, and post-write validation.
- Expose persistent start/resume/checkpoint/finish runtime commands that resolve repository-owned rules before recording bounded machine-local state.
- Add copy-based, digest-verified, no-overwrite Codex/Claude distribution plus invocation-receipt validation without making installed copies authoritative.
- Replace decimal version arithmetic with normal/small integer-component transitions and reserve `1.0.0-rc.N` plus `1.0.0` for fully working release gates.
- Coordinate the product and CLI package release while retaining schema/profile/template compatibility versions independently.
- Separate explicit pre-merge release preparation from an idempotent exact-merge-SHA tag/GitHub Release publisher with collision stops and no post-merge content commit.
- Run the complete local gate and clean-wheel adopter/runtime/host-layout fixed point; retain real authenticated host invocation, hosted OS/WSL, and publication evidence as explicit open gates.
- Run three independent high-effort specification reviews, reconcile blocking findings, and preserve bounded evidence.
- Define default main-model/main-effort inheritance, medium useful fan-out, explicit override reporting, and outcome-cost-aware low/high budget behavior.
- Define one project-owned problem/opportunity/question registry, stable layer IDs, and Decision records; keep tasks inside Changes and retain the Action entity as a project open question pending Decision.

## Batch 5 — Concrete conformance contracts — specification complete

- Define `DSET-CONTRACT-SKILL-001` for real installable host-native skill artifacts and clean install/discovery/load/invocation proof on every declared agent host.
- Define `DSET-CONTRACT-TOOL-001` for macOS, native Windows, WSL, and Linux behavior or explicitly narrower applicability proven before execution.
- Define `DSET-CONTRACT-TOOL-002` for dependency allowlist/denylist, exact registry/version/license/provenance and lockfile authority, plus bounded authorized exceptions with expiry.
- Define `DSET-CONTRACT-OPS-001` for real GitHub Actions workflow/run/check evidence bound to the actual implementing PR SHA and protected integration.
- Keep these observable conformance boundaries separate from Decisions, which record choices and rationale.

## Batch 6 — Outcome and deferred product practices — specification complete

- Define Outcome as a measurable state change rather than an output, feature, milestone, or task completion.
- Record one DSET 0.3 adoption-readiness Outcome with baseline, target, source/method, window, and related Problem, Opportunity, User Story, and Eval dispositions.
- Register Journey, Actor/Persona, Hypothesis/Experiment, prioritization, feedback/analytics, and generated roadmap/release views as concise open Questions only.
- Preserve the three intake queues; add Conflict only under
  `DSET-DECISION-GOV-005`, keep its open register/view separate, and classify
  every artifact by semantics rather than workflow.

## Batch 7 — Work Area Contract — deterministic implementation complete

- Define Work Area as a neutral repository-relative folder boundary that may contain local, deployable, library, documentation, methodology, data, or mixed content.
- Support repository-level scope and one or many Work Areas without assuming code, deployability, services, features, modules, or a specific architecture.
- Keep the accepted repository declaration authoritative; session continuity may reference and re-resolve it but cannot own or change it.
- Register separate deterministic test and qualitative eval obligations plus Change verification links.
- Implement the declaration and Change-target schemas, safe repository-relative
  path/identity validation, `dset new --work-area`, and trace propagation.
- Keep the independent qualitative eval pending until the runtime session
  resume capability can exercise stale-scope re-resolution end to end.

## Batch 8 — Provenance and artifact roles — extension specified

- Distinguish immutable atomic authority sources, evergreen compiled
  projections, transactional context/evidence, and implementation artifacts.
- Require active Requirements, Contracts, Decisions, and other normative atoms
  to compile into evergreen projections; the atom wins when a projection is
  stale.
- Require append-only lifecycle events, explicit acyclic absorption, derived
  current state, and byte-stable archive relocation only after full retirement.
- Require commits that change evergreen truth or implementation artifacts to
  cite the Decision they implement, or the authorizing Problem, Opportunity,
  Question, or Change when no Decision is required.
- Require explicit `llm_session_ids` provenance, or an explicit human-only
  disposition, across Change manifests, intake items, Decisions, promoted
  proofs, skill-run records, and session checkpoints.
- Enforce current Change/intake/Decision/proof records with stable
  `DSET-E155`, version and test run/checkpoint schemas, and backfill this
  repository's transactional artifacts with the material-review session.
- Preserve host-prefixed IDs as YAML scalar list values and cover the parser,
  schemas, templates, validators, current repository, and generated adopter.

## Batch 9 — Governance constitution — complete

- Keep `DSET-RULE-ARCHITECTURE` as the sole dependency-free governance root and
  separate rule authority from assurance.
- Add explicit per-rule `precedence_over` alongside `depends_on`; validate
  missing targets, duplicate targets, and precedence cycles independently from
  dependency closure.
- Promote the project-local artifact classes, transactional discharge,
  commit/session provenance, and work-item compile-down rules into `core-v1`
  profile version 0.3.
- Compile `DSET-DECISION-GOV-002` into GOV requirements, tests, evals, schema,
  validator, profile templates, active Change traceability, and bounded FPF
  provenance.

## Batch 10 — Project health, external review, and ranking — specification complete

- Define a non-authoritative project-health projection with artifact inventory,
  explicit coverage denominators/applicability/freshness, and canonical return
  links; require portable Markdown first and keep interactive rendering optional.
- Define provider-independent review packets and transactional reports with a
  mandatory provenance/evidence envelope, free-form findings body, explicit
  dispositions, compile-down, and smallest-closure proof reopening.
- Use priority as the only generic rank across every governed artifact, allow
  visible inheritance for implementation files, keep impact/severity/value in
  their existing semantics, classify every governed artifact pairing, apply
  active-source/projection and absorbing/absorbed lifecycle rules, auto-resolve
  only selectable policy conflicts after immutable authority and explicit
  precedence, stop on unsatisfiable obligations/ties/unknown/incomparability,
  and leave the exact scale/inheritance policy to the open governance Question.
- Register deterministic tests, qualitative evals, implementation tasks, and
  current missing-capability Problems without claiming the renderer, schemas,
  reconciliation runtime, or cross-host proof exists.

## Later batches

Complete Batch 4's native authenticated Codex/Claude receipts, hosted Linux/macOS/native-Windows and WSL execution, RC/final readiness integration, and real exact-SHA publication proof. Implement Batch 10 health/review/ranking mechanics plus roadmap §§5–§10 for the TypeScript profile, owned Your Harness pilot, clean-room Claudian evaluation, and complete qualitative evals. Keep unfinished evidence and behavior out of public capability claims.

## Rollout and recovery

Governance materialization refuses existing destinations and cleans up partial copies. Repository-local rule edits require explicit customization refresh and never pull invisible template updates. Revert the affected logical commit if review finds a faulty boundary; any later invariant, requirement, scenario, registry, template, wrapper, or proof change invalidates current evidence and requires fresh DSET validation and self-hosting.
