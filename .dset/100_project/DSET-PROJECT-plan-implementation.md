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

## Batch 4 — Skill topology and release cycle — expanded implementation in progress; native/hosted proof pending

- Keep `dset` as the only general lifecycle/next-step entrypoint and expose one thin direct wrapper for every stable lifecycle mode.
- Implement and register all 16 thin source packages, including the two pre-resolution exceptions, applicability-aware adopter materialization, and recursive wrapper-identity proof.
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
- Define project-owned semantic routing, stable IDs, and immutable atoms; keep
  tasks inside Changes and retain the Action entity as a project Question
  pending Decision.

## Batch 5 — Concrete conformance contracts — specification complete

- Define `DSET-CONTRACT-SKILL-001` for real installable host-native skill artifacts and clean install/discovery/load/invocation proof on every declared agent host.
- Define `DSET-CONTRACT-TOOL-001` for macOS, native Windows, WSL, and Linux behavior or explicitly narrower applicability proven before execution.
- Define `DSET-CONTRACT-TOOL-002` for dependency allowlist/denylist, exact registry/version/license/provenance and lockfile authority, plus bounded authorized exceptions with expiry.
- Define `DSET-CONTRACT-OPS-001` for real GitHub Actions workflow/run/check evidence bound to the actual implementing PR SHA and protected integration.
- Keep these observable conformance boundaries separate from Decisions, which record choices and rationale.

## Batch 6 — Outcome and deferred product practices — specification complete

- Define Outcome as a measurable state change rather than an output, feature, milestone, or task completion.
- Record one DSET 0.3 adoption-readiness Decision/Outcome with baseline,
  target, source/method, window, and related Problem, Question/Opportunity,
  sibling Decision/User Story, and QA/Evaluation dispositions.
- Register Journey, Actor/Persona, Hypothesis/Experiment, prioritization, feedback/analytics, and generated roadmap/release views as concise open Questions only.
- Apply the flat semantic model under `DSET-DECISION-GOV-007`; keep Conflict as
  a direct Question subtype and classify every atom by semantics rather than
  workflow.

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
  cite the Decision or Decisions they implement; linked Problems, Questions,
  QA atoms, and Changes are additional provenance rather than authority.
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

## Batch 10 — Project health, external review, and ranking — deterministic implementation complete; independent review pending

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
- Implement and deterministically verify the health renderer, review
  packet/report/reconciliation runtime, priority/lifecycle model, and conflict
  resolver. Retain the authenticated independent review and its reconciled
  findings as a separate open Evaluation gate.

## Batch 11 — Implementation modes and canonical TOML — in progress

- Add a documented `workflows.implement.mode` setting with `lazy` as the
  default and `strict` as the implementation-only option.
- Keep `dset-implement` thin: the resolved lifecycle owns lazy prerequisite
  closure and strict no-prerequisite behavior.
- Replace the hand-written settings parser with schema-versioned TOML parsing;
  keep schema 1.0 read compatibility while emitting documented schema 1.1.
- Build one portable dry-run-first migration command that inventories owned
  YAML/JSON and Markdown frontmatter, classifies explicit external boundaries,
  preserves parsed values/IDs/provenance, rewrites references, emits digest
  mapping, refuses collisions/unsupported values, and is idempotent.
- Migrate DSET-owned structured artifacts and Markdown frontmatter to TOML.
  Keep host skill metadata, GitHub workflows, ecosystem/wire/runtime formats,
  and generated compatibility adapters non-authoritative and freshness-gated.
- Commit migration tooling before applying it. Apply the migration as a
  separate logical commit, then regenerate adapters/derived views and record
  deterministic evidence after the complete repository and adopter gates pass.

## Batch 12 — Complete DSET-owned TOML cutover — complete

- Replace byte-level immutability with semantic immutability under
  `DSET-DECISION-GOV-018`; permit carrier changes only through a lossless,
  authority-bound transition with an append-only return path.
- Add a validated carrier-transition ledger and schema containing the source
  and target paths, whole-file digests, normalized semantic digest, source Git
  blob, declared loss, governing Decision, and session provenance.
- Convert every DSET-owned standalone YAML artifact to an adjacent historical
  TOML envelope, and convert every DSET-owned Markdown YAML frontmatter block
  to TOML frontmatter without changing its semantic payload or body.
- Retain YAML only at externally prescribed host boundaries such as GitHub
  Actions and host skill metadata; those files are not DSET artifact carriers.
- Prove zero DSET YAML artifact paths, zero DSET Markdown YAML frontmatter,
  semantic equivalence, complete resealing, rollback coverage, idempotency,
  current compilation, and the full repository verification suite.

## Later batches

Complete only the remaining DSET core gates: native authenticated Codex/Claude
receipts, hosted Linux/macOS/native-Windows and WSL execution, the independent
review report and reconciliation, RC/final readiness integration, and real
exact-SHA publication proof. JavaScript/TypeScript applied enforcement and all
external adopter work belong to separately owned project Changes and are not
prerequisites for this DSET release. Keep unfinished evidence and behavior out
of public capability claims.

## Rollout and recovery

Governance materialization refuses existing destinations and cleans up partial copies. Repository-local rule edits require explicit customization refresh and never pull invisible template updates. Revert the affected logical commit if review finds a faulty boundary; any later invariant, requirement, scenario, registry, template, wrapper, or proof change invalidates current evidence and requires fresh DSET validation and self-hosting.
