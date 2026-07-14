# TODO — Operationalize OpenSpec and Composable Engineering Skills

**Outcome:** Make this public repository the canonical source for the complete DSET Spec Loops framework—methodology, documentation, schemas, templates, validators, utilities, skills, fixtures, and migration guidance. Operationalize the SPEC → TEST PLAN + EVAL PLAN → IMPL PLAN → CODE → GATES pipeline through a DSET-owned change package under `dset/`, borrowing useful OpenSpec concepts without installing a second methodology or duplicating rules already owned by 00–06.

**Sources:** [OpenSpec](https://github.com/Fission-AI/OpenSpec) and [Matt Pocock’s skills](https://github.com/mattpocock/skills).

**Implementation status (2026-07-14):** Checked items are implemented and verified by DSET change `operationalize-dset-v1` in [PR #7](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/7). Unchecked items remain roadmap work; the v1 scope does not claim the external pilot, complete Solution Landscape and Back-to-Left enforcement, large-project hardening, or the evidence-derived JavaScript/TypeScript profile.

## §0 | Decisions to preserve

- [x] Keep this public repository as the sole editable source of framework truth; external frameworks inform it but do not govern it.
- [x] Keep all framework-owned methodology, documentation, schemas, templates, validators, utilities, skills, fixtures, and migration guidance public and versioned in this repository.
- [x] Keep the five-stage pipeline and the existing document ownership boundaries in 00–05.
- [x] Use a DSET-owned, OpenSpec-derived model for project-local change packaging and current-truth reconciliation, not OpenSpec as a replacement methodology.
- [x] Adapt selected Matt Pocock workflows into small repository-native skills only when each skill runs a distinct workflow.
- [x] Do not install BMAD or the complete Superpowers/Matt Pocock workflow stack as another orchestration layer.
- [ ] Require one pilot and evidence before making the new change package the default for all repositories.

### Source-of-truth ownership to formalize

| Concern | Authoritative source |
|---|---|
| DSET framework rules, assets, skills, and tooling | This public repository |
| Accepted behavioral requirements for an adopting project | That project's `dset/specs/` |
| Stored data shape and constraints | DDL/schema linked from the behavioral spec |
| Architectural rationale and accepted decisions | ADRs linked from `design.md` |
| Runtime state and observed outcomes | One authoritative owner per concern: local files for modest-write local tools; an embedded/local database or database server for higher volume/concurrency; external databases, brokers, object stores, or workflow stores for stateless services; the external platform for the resources it owns |
| Work-in-progress project intent and evidence | That project's `dset/changes/<change-id>/` until archive |

## §1 | Define the repository change-package contract

- [x] Use `dset/` as the canonical project-local artifact root.
- [x] Define `dset/specs/` as accepted current truth and `dset/changes/<change-id>/` as bounded work in progress.
- [ ] Inventory each pilot repository’s existing spec roots before creating `dset/`; define an explicit migration or compatibility map and never leave two writable sources of truth for the same concern.
- [x] Define a stable lowercase kebab-case `<change-id>` convention.
- [x] Define the required artifact set:

```text
dset/
├── specs/                              # Accepted current truth
└── changes/
    └── <change-id>/
        ├── proposal.md                 # Why, scope, non-goals, risk
        ├── specs/                      # ADDED/MODIFIED/REMOVED requirements
        ├── test-plan.md                # Deterministic proof designed before code
        ├── eval-plan.md                # Probabilistic/qualitative proof, or N/A with reason
        ├── solution-landscape.md       # Capability gaps, candidates and adopt/adapt/build decision
        ├── proofs/                     # Disposable framework/library proof-of-fit evidence
        ├── design.md                   # Technical design linking accepted ADRs
        ├── implementation-plan.md      # Ordered batches and rollout
        ├── tasks.md                    # Executable checklist
        └── verification.md             # Fresh commands, redacted summaries, evidence pointers
```

- [x] Define change-package profiles—small fix, standard change, large/cross-package change, defect repair, and external-component adoption—with an explicit required-artifact matrix. Minimum proposal/scope, deterministic acceptance proof, tasks, and verification survive every profile; an eval plan may be an explicit N/A only when no probabilistic or qualitative behavior exists.
- [ ] Link the change-package profile to both of 04's selections: runtime risk determines required recovery/safety semantics, while deployment topology plus write volume/concurrency selects file-backed, local-database-backed, or external-backing-service durability. Require event sourcing, reconciliation, durable workflow execution, and observed-progress liveness only when their narrower triggers apply.
- [ ] Require specs and implementation plans to carry a concern-scoped durability table covering authority, schema/format, writer model, refresh boundary, failure model, receiving-side idempotency boundary, and recovery proof; prohibit both durable state that exists only in process memory and duplicate writable authorities for the same concern.
- [x] Define artifact readiness gates rather than rigid waterfall phases: implementation may start only when requirements and proof are explicit, but any artifact may be corrected when new evidence appears.
- [x] Require each requirement to carry a stable ID and at least one scenario or acceptance check.
- [x] Require delta specs to mark requirements as `ADDED`, `MODIFIED`, or `REMOVED` and identify the current-truth target they affect.
- [x] Require `test-plan.md` to define deterministic unit, integration, end-to-end, property, regression, and machine-gate proof.
- [x] Require `eval-plan.md` to define probabilistic or qualitative datasets, criteria, rubrics, thresholds, calibration, drift cases, and budgets; allow an explicit not-applicable declaration when no such behavior exists.
- [x] Require `implementation-plan.md` to map every batch to requirement, test, and eval IDs as applicable.
- [x] Require `verification.md` to record fresh commands, exit status, redacted result summaries, evidence pointers, unresolved failures, and whether completion is accepted; do not persist secrets or sensitive full command output.
- [ ] Require schema validation to prove the dependency graph: proposal → delta specs plus test plan and applicable eval plan → solution landscape plus proof-of-fit → ADR/design plus implementation plan → tasks → verification → archive.
- [x] Define the PR-centered archive transaction: open a draft PR early and record its repository-qualified PR ID → complete implementation and pre-merge verification → reconcile deltas into `dset/specs/` → move the completed change to `dset/changes/archive/YYYY-MM-DD-<change-id>/` inside the same PR → regenerate traceability from artifact metadata plus the PR → run spec-sync/link checks → merge. The archive records the stable PR ID, not a not-yet-existing merge SHA.
- [x] Define failure behavior: an incomplete or failed change remains unarchived and its current-truth specs remain unchanged.

### Solution Landscape and Reuse Gate

- [ ] Add a mandatory **Solution Landscape and Reuse Gate** after domain, specification, test-plan, and applicable eval-plan readiness but before architecture selection, detailed design, and implementation planning.
- [ ] State the governing rule: select frameworks, libraries, services, protocols, and reusable components by testing them against accepted requirements and proof—not by reshaping the domain around a fashionable tool.
- [ ] Define the gate sequence as capability-gap map → ecosystem discovery → evidence-backed shortlist → proof-of-fit → adopt/adapt/build decision → ADR/design integration.
- [ ] Derive a capability-gap map from requirement IDs plus relevant test and eval IDs. For each capability, record required behavior, quality attributes, constraints, risk, whether it differentiates the product, and whether an existing component could own it.
- [ ] Classify capabilities before searching: product-defining domain behavior should remain DSET-owned; commodity or infrastructural behavior should prefer reuse when a candidate satisfies the proof and operational constraints.
- [ ] Search across appropriate solution types rather than libraries alone: frameworks, focused libraries, managed services, standards/protocols, platform-native capabilities, reference implementations, and a minimal custom implementation as the comparison baseline.
- [ ] Record discovery provenance in `solution-landscape.md`: candidate name, source URL, exact version or commit evaluated, license, maintenance/release evidence, documentation used, known constraints, and the requirement, test, and eval IDs it claims to cover.
- [ ] Require a comparison matrix that scores verified requirement coverage, quality-attribute fit, custom glue, architecture fit, testability, observability, reliability/recovery, performance, latency, cost, security, privacy/data ownership, deployment and operational burden, portability, ecosystem maturity, maintenance health, transitive dependency risk, license compatibility, lock-in, and exit cost.
- [ ] Distinguish vendor claims from observed evidence. Mark every criterion as proven, partially proven, unproven, failed, or not applicable and attach an evidence pointer.
- [ ] Shortlist only candidates with plausible hard-constraint coverage. Reject candidates early when licensing, security, data residency, platform support, architecture, or operational requirements are incompatible.
- [ ] Build disposable proof-of-fit spikes under `proofs/<candidate>-fit/`; prohibit prototype code from entering production until it is deliberately redesigned, tested, and accepted through the normal implementation plan.
- [ ] Run proof-of-fit candidates against representative scenarios from the test plan and applicable eval plan, including happy paths, failure paths, restart/recovery, concurrency, boundary conditions, upgrade/migration behavior, and operational diagnostics.
- [ ] Use the same acceptance thresholds for candidates and custom alternatives so the comparison cannot be biased by easier proof for the preferred option.
- [ ] Measure the uncovered surface explicitly: missing requirements, adapter code, policy glue, persistence, migrations, operational tooling, extra tests, and long-term maintenance that DSET would still own after adoption.
- [ ] Prefer the smallest stable component that owns a coherent problem. Do not adopt a broad framework merely because it covers the largest raw percentage of requirements if its coupling, glue, or operational cost is worse.
- [ ] Define the decision outcomes:
  - **Adopt** when the component satisfies the required proof with acceptable ownership, operational cost, and exit risk.
  - **Adapt** when the component is useful but must sit behind a DSET-owned port, adapter, anti-corruption layer, or policy wrapper.
  - **Build** when the capability differentiates the product, candidates fail hard requirements, or owning a minimal implementation is demonstrably cheaper and safer.
  - **Defer** when evidence is insufficient and the capability is not yet required; record the trigger for reassessment.
- [ ] Require selected external components to remain behind stable DSET-owned contracts where replacement cost or domain contamination is material; keep vendor/framework types out of the domain core.
- [ ] Create an ADR for every material adoption decision, including selected version, evidence, rejected alternatives, trade-offs, integration boundary, data ownership, upgrade policy, failure/rollback plan, and exit/migration strategy.
- [ ] Link the adoption ADR bidirectionally to requirement, test, and eval IDs, `solution-landscape.md`, proof artifacts, design, implementation tasks, dependency manifests, and the repository-qualified implementing PR ID; the PR owns the actual code diff and eventual merge result.
- [ ] Require dependency pinning and reproducible installation, plus checks for transitive licenses, known vulnerabilities, abandoned dependencies, unbounded telemetry, unexpected network access, and incompatible update behavior before acceptance.
- [ ] Define upgrade handling as a new bounded change when behavior, contracts, data, security posture, licensing, or operational characteristics may change; rerun only the affected fit proofs and regression evals.
- [ ] Require a replacement seam and exit test for high-lock-in components: demonstrate that DSET-owned domain behavior and accepted specs survive replacement of the external adapter.
- [ ] Add an LLM-agent-workflow example: map requirements such as durable state, checkpointing, pause/resume, branching, human approval, retries/idempotency, concurrency, recovery, observability, and storage control; treat LangGraph as one candidate alongside focused libraries and a minimal custom state machine, then decide from proof-of-fit evidence.
- [ ] Make completion of the gate explicit: no candidate advances into design or the implementation plan until hard constraints pass, open risks have owners, the decision ADR is accepted, and rejected or deferred alternatives are recorded.

### ADR-to-implementation traceability

- [ ] Give every ADR a stable ID such as `ADR-0042`; treat the ADR as the owner of the decision and rationale, not as a manually maintained ledger of every implementation commit.
- [x] Open a draft PR as soon as the branch contains its first reviewable commit so the stable repository-qualified PR ID exists before final ADR, task, verification, archive, and traceability updates.
- [x] Require ADRs, proposals, implementation plans, tasks, test/eval evidence, and verification records to reference that PR ID. Meaningful commits made after the PR exists may additionally use trailers such as `PR: owner/repo#123`, `ADR: ADR-0042`, `DSET-Change: tmux-controls`, `Requirement: TMUX-REQ-07`, `Test: TMUX-TEST-04`, or `Eval: TMUX-EVAL-03`; the first pre-PR commit is linked by PR membership and need not be rewritten.
- [x] Define the canonical traceability chain as ADR → DSET change → requirements plus test/eval evidence → repository-qualified PR ID. The PR is the implementation record: its files view owns the actual code modifications/additions, its checks own pre-merge evidence, and GitHub records the eventual merge or close result.
- [ ] Define merge-strategy behavior around the PR identity: squash, merge, or rebase may change commit topology but must preserve the same linked PR and change-package references; no artifact inside the PR is required to predict the final merge SHA.
- [x] Generate a committed `dset/traceability.yaml` or equivalent index from ADR/change/evidence metadata and repository-qualified PR references; derive changed files and symbols from the PR rather than asking humans to maintain a duplicate code-file ledger.
- [x] Keep the generated index reproducible and reviewable: stable ordering, no timestamps unless semantically required, and a clean regeneration check in CI.
- [ ] Make CI reject references to missing ADRs, changes, requirements, tests, evals, evidence, or PRs, and report accepted ADRs that claim implementation but have no repository-qualified PR evidence. Pre-merge CI validates PR existence and identity; post-merge reporting may verify its final state without creating a second archive commit.
- [ ] Do not use Git notes as the primary relationship store because they are not reliably transferred by ordinary clone, fetch, and push workflows.

### Shift-left and Back-to-Left Repair Loop

- [ ] Make **shift-left** and **back-to-left** complementary mandatory behaviors: design specs and proof before implementation, then trace every downstream defect back to the earliest defective decision or artifact before replaying the pipeline forward.
- [ ] State the governing rule: every downstream defect triggers a backward provenance pass followed by a forward consistency replay.
- [ ] Define the default repair sequence: reproduce with a failing regression test or eval → identify the first bad commit → follow commit/change/ADR/spec links → classify the earliest incorrect artifact → correct or supersede it → propagate the correction through specs, proof, code, verification, and archive.
- [ ] Require `git bisect`, focused history analysis, or equivalent evidence to identify the first bad commit where feasible; do not treat the nearest `git blame` result or the bug-fix hunch as proven origin.
- [ ] Classify each defect at least as an ADR/decision defect, spec ambiguity/defect, design defect, implementation drift, missing test, missing eval, missing verification gate, or external-assumption change.
- [ ] Require an explicit disposition for every relevant upstream artifact: corrected, superseded, amended, or reviewed with no change and a recorded reason. Always inspect upstream; change it only when evidence shows that it contributed to the defect.
- [ ] Preserve decision history: never silently rewrite an accepted ADR to make the past look correct. Add a dated correction/addendum or a superseding ADR, link both directions, and retain the original decision and its implementation evidence.
- [ ] Keep accepted behavioral truth in the spec rather than the ADR. Propagate a corrected decision into current truth through a delta spec instead of copying or merging ADR prose directly into the spec.
- [ ] Do not rewrite the introducing commit. Link the immutable history from the repair commit and traceability index using trailers such as `Bug: BUG-0123`, `Introduced-By: <sha>`, `ADR: ADR-0042`, `DSET-Change: <change-id>`, `Requirement: <id>`, and `Regression-Test: <id>`.
- [ ] Extend the defect change package with structured root-cause data: first bad commit, classification, affected ADRs/specs, test gap, eval gap where applicable, correcting or superseding ADR, spec delta, fix commit, and final verification evidence.
- [ ] Require the regression proof to fail against the defective revision and pass after the repair where reproducible; for probabilistic behavior, retain a failing baseline and demonstrate the accepted improvement threshold.
- [ ] Allow emergency containment before the regression test only when operational urgency is recorded. The regression proof, backward provenance pass, upstream disposition, and forward replay must still complete before the change is closed.
- [ ] Make defect closure require forward consistency: corrected ADR/design → delta spec → test plan plus applicable eval plan → regression proof → implementation → verification → reconciliation into accepted current truth.
- [ ] Add the full causal chain to generated `dset/traceability.yaml` so a bug, introducing commit, decision, corrected spec, regression proof, and repair commit are discoverable in both directions.

## §2 | Define the large-project package tree

- [ ] Make a package tree mandatory for a large project; do not use file count or lines of code as the primary threshold.
- [ ] Classify a project as large when it has multiple independently meaningful capabilities, deployment units, domain boundaries, ownership/security boundaries, or cross-feature workflows that cannot be understood and verified comfortably as one unit.
- [ ] Keep a small project as one implicit package until decomposition reduces actual cognitive load.
- [ ] Define a **package** as a cohesive capability or architectural unit with an explicit boundary, public contract, owned domain vocabulary, accepted requirements, local deterministic tests, applicable evals, and dependency edges. A package is not necessarily a published code package.
- [ ] Put system-wide truth above the package tree and package-specific truth inside it:

```text
dset/
├── specs/
│   ├── global/
│   │   ├── system-spec.md              # Product purpose, actors, global behavior and invariants
│   │   ├── domain-map.md               # Shared language, bounded contexts and ownership
│   │   ├── architecture.md             # Package topology, dependency DAG and layer rules
│   │   ├── contracts.md                # Cross-package APIs, events, schemas and compatibility
│   │   ├── e2e-test-plan.md             # Whole-system user journeys and failure paths
│   │   ├── global-eval-plan.md          # Cross-cutting quality, safety and LLM evals
│   │   └── release-gates.md             # Aggregate readiness and rollout criteria
│   └── packages/
│       └── <package-id>/
│           ├── README.md                # Purpose, ownership, boundary and dependencies
│           ├── domain.md                # Local entities, states, invariants and vocabulary
│           ├── spec.md                  # Accepted package behavior
│           ├── contracts.md             # Public inputs, outputs, APIs and events
│           ├── test-plan.md              # Deterministic package proof
│           └── eval-plan.md              # Package-local probabilistic/quality proof
└── changes/
    └── <change-id>/                     # Deltas may target one or more packages plus global truth
```

- [ ] Keep the global spec thin: own system-wide behavior and invariants, link to package specs, and never copy package requirements.
- [ ] Keep the global domain map responsible for shared language, bounded-context relationships, and term ownership; package domain files own local detail.
- [ ] Make the global architecture describe package boundaries and an acyclic dependency graph, not restate internal designs.
- [ ] Put end-to-end journeys, cross-package integration failures, upgrade/rollback paths, and release smoke tests in the global E2E plan.
- [ ] Put cross-cutting LLM quality, safety, latency, cost, adversarial, and regression evals in the global eval plan; keep package-specific eval criteria with the package.
- [ ] Make global release gates aggregate package gates plus cross-package E2E/eval results; local green does not imply system green.
- [ ] Allow a change package to modify multiple feature packages only when one user-visible outcome requires it; list every affected package and global artifact explicitly.
- [ ] Require every package to run its own DSET loop, then reconcile accepted changes upward into global contracts, E2E coverage, evals, and release gates where affected.

### Decomposition variants to support

#### Variant A — Feature/capability first (default)

```text
packages/
├── conversation-history/
├── provider-runtime/
├── inline-edit/
├── usage-metering/
└── tmux-navigation/
```

- [ ] Prefer this when a feature can be specified, implemented, tested, evaluated, and released as a vertical user-visible slice.
- [ ] Keep frontend, backend, storage, and adapters inside the feature package unless they have an independent operational boundary.

#### Variant B — Domain/bounded-context first

```text
packages/
├── conversations/
│   ├── history/
│   └── branching/
├── providers/
│   ├── claude/
│   └── codex/
└── workspace/
    ├── instructions/
    └── skills/
```

- [ ] Prefer this when domain language, invariants, and lifecycle ownership are stronger boundaries than individual UI features.
- [ ] Allow nested feature packages inside a bounded context, but cap nesting unless another level demonstrably reduces cognitive load.

#### Variant C — Layer first

```text
packages/
├── frontend/
├── backend/
├── data/
├── integrations/
└── infrastructure/
```

- [ ] Use this only when layers have genuinely independent deployment, ownership, security, scaling, or technology boundaries.
- [ ] Require each feature change to name all affected layers and include global E2E proof; avoid layer-local completion claims for incomplete vertical behavior.

#### Variant D — Feature first with internal layers (recommended hybrid)

```text
packages/
└── conversation-history/
    ├── core/
    ├── frontend/
    ├── storage/
    └── provider-adapters/
```

- [ ] Use this for most large single-product applications: the top-level unit remains the capability while internal layer boundaries preserve architecture.
- [ ] Keep package-level requirements and proof vertical; internal layers implement the package contract rather than becoming separate product specs.

#### Variant E — Product/application plus platform

```text
packages/
├── apps/
│   ├── desktop/
│   └── cli/
├── capabilities/
│   ├── conversations/
│   └── usage/
└── platform/
    ├── runtime/
    └── persistence/
```

- [ ] Use this for multiple applications sharing stable capabilities or infrastructure.
- [ ] Keep product-specific behavior with the application, reusable domain behavior with capabilities, and technical mechanisms with the platform.

### Package-boundary rules

- [ ] Choose one primary decomposition axis at each tree level; do not mix features, layers, teams, and technologies as peer packages without an explicit rationale.
- [ ] Prefer vertical feature/capability boundaries over horizontal layers when both are viable.
- [ ] Extract a shared/platform package only after multiple real consumers need the same stable contract; do not package anticipated reuse.
- [ ] Give each package one owning spec and one public contract; consumers link to the contract rather than copy it.
- [ ] Keep package dependencies directional and acyclic; introduce ports/events or move the shared invariant upward when a cycle appears.
- [ ] Record cross-package behavior once at the lowest common owner: package spec for local behavior, global spec/contracts for system behavior.
- [ ] Require package IDs, requirement IDs, test IDs, eval IDs where applicable, change IDs, and evidence pointers to remain traceable across the tree.
- [ ] Define package split, merge, rename, and retirement as explicit changes with spec, contract, dependency, test, applicable eval, and migration updates.

### Framework namespace and naming contract

- [x] Adopt **`dset`** as the canonical machine namespace and **`dset-`** as the canonical human-visible prefix. Use **DSET Spec Loops** as the display name, **DSET Spec Loops: A Production Vibecoding Framework** as the full title, and expand DSET as **Domain–Supportability–Evals–Tests**.
- [ ] Do not use `dsetl-`: “loops” is part of the display/mental model, while adding `l` makes the namespace harder to pronounce and visually closer to the established SETL language family.
- [ ] Reserve framework-owned names; do not prefix ordinary product features, domain packages, or application code merely because they use the framework.

| Surface | Convention | Examples |
|---|---|---|
| Framework display name | `DSET Spec Loops` | documentation title, prose, diagrams |
| Full title | `DSET Spec Loops: A Production Vibecoding Framework` | README title, repository description |
| Repository slug | `dset-specs-loops-framework` | GitHub repository, project manifest |
| Machine namespace | `dset` | CLI, config root, schema IDs |
| Skills | `dset-<workflow>` | `dset-clarify`, `dset-diagnose`, `dset-prototype`, `dset-review` |
| Framework-owned folders | `dset/` or `.dset/` by ownership | `dset/specs/`, `.dset/cache/` |
| Framework-owned files | `dset[.<purpose>].<ext>` | `dset.toml`, `dset.schema.json` |
| Commands | `dset <verb>` | `dset new`, `dset check`, `dset verify`, `dset archive` |
| Environment variables | `DSET_<NAME>` | `DSET_CONFIG`, `DSET_NO_TELEMETRY` |
| CI jobs | `dset-<gate>` | `dset-spec-sync`, `dset-evals`, `dset-release-gate` |
| GitHub labels | `dset:<state>` | `dset:proposal`, `dset:ready`, `dset:blocked` |
| Change IDs | unprefixed kebab-case inside the namespace | `tmux-controls`, not `dset-tmux-controls` |
| Package IDs | unprefixed domain/capability names | `conversation-history`, not `dset-conversation-history` |

- [x] Keep `dset/` as the visible artifact root regardless of whether any OpenSpec code or concepts are reused; reject tooling that requires a competing writable project-truth root.

```text
dset/
├── specs/
├── changes/
├── templates/
└── schemas/

.dset/
├── cache/
├── state/
└── local-overrides.yaml
```

- [x] Keep committed source-of-truth artifacts under visible `dset/`; reserve hidden `.dset/` for generated, local, cached, or machine-owned state.
- [x] Reject `openspec/specs/`, parallel spec roots, or compatibility mirrors as writable sources for the same project; migration inputs may remain read-only history only.
- [ ] Publish a reserved-name list and make the validator reject ambiguous framework-owned paths or mixed namespaces.

## §3 | Establish third-party licensing and provenance first

- [x] Keep DSET's original work under Apache-2.0 while preserving the original MIT copyright and permission notices for any copied or substantially adapted OpenSpec, Matt Pocock Skills, Superpowers, or BMAD material.
- [x] Add a root `THIRD_PARTY_NOTICES.md` before copying or substantially adapting external material; record upstream project, author/copyright holder, source URL, exact commit or release, license, affected DSET files, what was adapted, and DSET modifications.
- [x] Add applicable upstream license texts under `third_party/licenses/` before the corresponding material enters the repository.
- [x] Add a provenance header or adjacent README note to every copied or substantially adapted file; do not present third-party MIT material as exclusively Apache-2.0.
- [x] Preserve upstream `NOTICE`, attribution, contributor information, and separately licensed assets required by the exact source version.
- [x] Prefer independently implementing ideas and workflow patterns in DSET terminology; treat substantial wording, templates, code, scripts, or skill reuse as licensed material.
- [x] Keep trademarks separate from copyright licensing; use third-party names only for truthful source, inspiration, or compatibility references and never imply endorsement.
- [x] Define a pre-merge provenance check: verify source/version, record the license, confirm notices, check trademark-safe naming, and confirm no source-specific exception was overlooked.
- [x] Add deterministic notice/link checks to the minimum validator before the pilot and expand them as new third-party material is introduced.

## §4 | Build minimum tooling and decide OpenSpec CLI usage

- [x] Create the repository-owned `dset/` change-package template and schemas needed by the pilot.
- [ ] Create a minimum validator for required artifacts, IDs, delta markers, test-plan/eval-plan separation, task-to-requirement/proof mapping, archive readiness, current-truth reconciliation, and licensing/provenance. The v1 validator covers artifacts, IDs, test/eval separation, archive guards, and provenance; delta-marker and complete dependency-edge enforcement remain open.
- [x] Expose the validator through one cross-platform canonical command and make this repository's dogfood change use that command.
- [x] Add baseline fixtures for one small fix, one normal feature, one failed/unarchived change, and one archived change before the pilot.
- [ ] Test the current OpenSpec CLI in a disposable repository, not first in a live project.
- [ ] Check whether OpenSpec can operate on the canonical `dset/` contract without a competing writable root, unexpected rewrites, generated context bloat, or tool-specific assumptions.
- [ ] Check whether custom schemas can require `test-plan.md`, `eval-plan.md`, `implementation-plan.md`, and `verification.md` without fighting upgrades.
- [ ] Check whether `propose`, `apply`, `verify`, and `archive` preserve DSET stage ownership, evidence gates, update controls, and telemetry policy.
- [ ] Compare CLI-backed operation with the repository-owned template/script implementation through the Solution Landscape and Reuse Gate.
- [ ] Adopt OpenSpec code only if it reduces maintenance while preserving `dset/` exactly; otherwise retain useful concepts and own the implementation here.

## §5 | Pilot the contract in Claudian

- [ ] Treat Claudian as one pilot program with three independently archived changes: input growth first, readline keybindings second, tmux controls last.
- [ ] Map Claudian’s existing spec, test-plan, eval-plan, and implementation-plan roots into `dset/`; decide whether to migrate, redirect, or retain them as read-only history before writing new current truth.
- [ ] Pilot **input growth** first: reconstruct intent without treating unfinished code as the specification, write deterministic 50%-height/layout scenarios in the test plan, declare whether an eval plan is applicable, correct the implementation, verify it, and archive it before starting the next change.
- [ ] Pilot **readline keybindings** second: specify cursor, deletion, selection, conflict, and platform behavior; test the public input seam with independent expected-value oracles; implement one vertical red/green slice per keybinding group.
- [ ] Pilot **tmux controls** last: specify prefix parsing, command configuration, tab numbering/navigation, confirmation, tab/session lists, accessibility, settings lifecycle, and conflict behavior; separate pure key routing from Obsidian integration.
- [ ] Execute the pilot under the repository-provided TDD, typed, lint, layering, verification, and archive gates.
- [ ] Scale pilot review by risk: gates/self-review for the mechanical input-growth change, one independent review for readline behavior, and separate spec-compliance and code-quality reviews for tmux controls.
- [ ] Archive only after delta specs reconcile cleanly into current truth and all accepted test, eval, and verification evidence is recorded.
- [ ] Retrospect: record friction, missing artifacts, redundant ceremony, agent context cost, and whether the structure improved recovery after interruption.

## §6 | Adapt the useful Matt Pocock workflows

### Adopt first

- [x] **`grill-with-docs` plus `domain-modeling` pattern** — create one repository-native pre-spec interview workflow that resolves ambiguous branches, sharpens ubiquitous language, stress-tests entities/invariants with edge cases, and records ADRs before a spec is accepted.
- [x] **`diagnosing-bugs` pattern** — create a disciplined reproduce → minimise → hypothesise → instrument → fix → regression-test workflow; diagnosis must remain separate from implementation authorization.
- [x] **`prototype` pattern** — define an explicitly disposable prototype lane for answering design questions; require a decision record before any prototype code is promoted.

### Refine existing stages after the pilot; do not create first-wave standalone skills

- [ ] **`code-review` pattern** — refine review around a fixed comparison point, explicit spec/standards sources, and separately reported compliance and quality findings.
- [ ] **`to-tickets` tracer-bullet pattern** — add dependency edges and independently verifiable vertical slices to implementation tasks when work spans sessions.
- [ ] **`handoff` pattern** — add an optional pointer-only summary when the change package itself is insufficient; do not duplicate its contents.
- [ ] **`codebase-design` pattern** — add a deep-module/interface-pressure rubric to design and review: prefer more behavior behind smaller stable interfaces and test through those interfaces.

### Consider only after a demonstrated gap

- [ ] **`wayfinder` pattern** — add only for investigations too large for one change package; its output must feed a later bounded change, not become a permanent parallel planning system.

### Do not duplicate

- [x] Do not import `to-spec` as a second spec format; the DSET change package owns project-local specifications.
- [x] Do not import another generic `tdd` methodology; strengthen [02_Test and Eval Plan Patterns — Proof Artifact Conventions](<02_Test and Eval Plan Patterns — Proof Artifact Conventions.md>) and [05_Layered Build Standard — DDD, TDD, Small Functions, Typed Gates](<05_Layered Build Standard — DDD, TDD, Small Functions, Typed Gates.md>) with any missing executable details.
- [x] Do not import `implement` as a competing execution orchestrator; implementation follows the accepted change package and project-local agent contract.
- [x] Do not import generic `research` as a parallel system; any research workflow must write source-backed evidence into the DSET change package.
- [ ] Do not import `triage` until a real issue-tracker state-machine gap is demonstrated.
- [x] Do not copy third-party skills verbatim into the methodology. Extract the workflow, preserve provenance, adapt terminology, validate behavior, and keep this repository canonical.

## §7 | Map accepted changes back into 00–06

- [ ] Update [00_Tool Development Playbook](<00_Tool Development Playbook.md>) only with the scale/routing rule: when a project-local change package is required and when a lightweight inline artifact is enough.
- [x] Update [01_Spec Authoring Patterns — Service Spec Conventions](<01_Spec Authoring Patterns — Service Spec Conventions.md>) with the final current-truth, delta-spec, requirement-ID, and scenario contract.
- [x] Update [02_Test and Eval Plan Patterns — Proof Artifact Conventions](<02_Test and Eval Plan Patterns — Proof Artifact Conventions.md>) with the final separate `test-plan.md`, `eval-plan.md`, and `verification.md` contracts, the diagnosis boundary, public-seam testing, independent expected-value oracles, and one vertical red/green slice per cycle.
- [ ] Update [03_Implementation Plan Patterns — Service Build Conventions](<03_Implementation Plan Patterns — Service Build Conventions.md>) with artifact readiness, batch mapping, archive transaction, failed-change behavior, and the deep-module design rubric.
- [ ] Update [04_General Build Rules — Tool Code Conventions](<04_General Build Rules — Tool Code Conventions.md>) only if pilot evidence reveals a genuinely universal rule not already owned elsewhere.
- [x] Keep [05_Layered Build Standard — DDD, TDD, Small Functions, Typed Gates](<05_Layered Build Standard — DDD, TDD, Small Functions, Typed Gates.md>) language-neutral at the gate-category level and implement concrete tools, paths, exclusions, and thresholds through versioned language profiles; Python v1 is the first active profile.
- [ ] Derive the JavaScript/TypeScript profile from `obsidian-your-harness`: inventory its real compiler, linter, tests, package boundaries, scripts, and failure history; then map evidence-backed tools and thresholds to the same six categories without copying Python limits.
- [ ] Update the build standard after the pilot with deterministic spec-sync/archive gates, public-seam TDD enforcement where feasible, and risk-scaled review without collapsing applied profile details back into the general rules.
- [ ] Update [06_External Grounding — LLM Power-User Practice](<06_External Grounding — LLM Power-User Practice.md>) with Matt Pocock’s skills as provenance and refresh OpenSpec provenance after the pilot.
- [x] Keep detailed templates and executable workflows out of 00–06; place them in repository templates, scripts, utilities, or focused skills and link to them.
- [ ] Update [00_Tool Development Playbook](<00_Tool Development Playbook.md>)’s document map only if a permanent new governing document is truly required. This TODO is temporary and should not become stage 7.

## §8 | Harden reusable assets after the pilot

- [ ] Harden the validator to cover solution-landscape/proof/ADR traceability, ADR/commit/change traceability, Back-to-Left completeness, package/global ownership, licensing, archive readiness, and current-truth reconciliation.
- [x] Keep the validator cross-platform and runnable through the same canonical command used by this repository's dogfood change.
- [x] Create only the three accepted focused skills from §6; keep each small, script-backed where useful, and explicit about trigger, output, verification, and stop conditions.
- [x] Keep skill sources in this repository; runtime installations must point back to or be generated from versioned repository releases, never become independent canonical copies.
- [ ] Add advanced fixtures for external-component adoption with competing proofs and a defect traced to an introducing commit and superseded ADR.
- [x] Add migration guidance for repositories with existing spec, test-plan, eval-plan, and implementation-plan folders.
- [ ] Have final methodology, implementation, and licensing reviews verify that every external influence is either independently re-expressed with provenance or distributed with its required notices.

## §9 | Acceptance criteria

- [x] The methodology remains understandable without installing OpenSpec or Matt Pocock’s skills.
- [x] This public repository is the only editable source of framework truth and contains every released framework-owned methodology, document, schema, template, validator, utility, skill, fixture, and migration guide.
- [x] One repo-local change folder contains intent, proof, design, execution, and verification without duplicating the same rule across artifacts.
- [ ] Every large project has a justified package tree, explicit global artifacts, a dependency DAG, and no duplicated source of truth across global and package specs.
- [ ] Every package can be understood and verified as a bounded unit, while global E2E tests and evals prove cross-package behavior.
- [x] Framework-owned skills, commands, folders, files, CI gates, and environment variables follow the `dset` namespace contract without prefixing ordinary product/domain names.
- [x] Tests and evals are designed before implementation in separate artifacts and remain independently reviewable; deterministic tests are never relabeled as evals.
- [ ] Every material external-component decision is derived from requirement IDs plus relevant test and eval IDs, supported by reproducible proof-of-fit evidence, recorded in an ADR, isolated behind an appropriate ownership boundary, and accompanied by an exit strategy.
- [x] Archiving is deterministic, preserves history, and cannot silently overwrite current truth after failed verification.
- [x] Every adopted skill fills a documented gap and has a distinct trigger, output, verification step, and stop condition.
- [ ] Review effort scales with risk: gates/self-review for mechanical changes, one independent review for normal changes, and separate spec-compliance and code-quality reviews for high-risk changes.
- [x] Agents can resume an interrupted change from files alone without relying on chat history.
- [x] The canonical verification command detects malformed change packages and spec drift.
- [ ] Every adopting project has exactly one writable `dset/` artifact root; validators reject competing project-truth roots.
- [x] ADRs, DSET changes, requirements, test/eval evidence, and repository-qualified PR IDs form a bidirectionally discoverable graph; each PR owns its actual code diff and eventual merge result without requiring artifacts in that PR to contain a future merge SHA.
- [ ] Every closed defect demonstrates a regression proof, evidence-backed first-bad-commit disposition, upstream ADR/spec review, and forward propagation into accepted current truth; emergency containment cannot bypass eventual Back-to-Left completion.
- [ ] The Claudian pilot demonstrates lower ambiguity and reliable recovery without unacceptable ceremony or context overhead.
- [ ] Independent review finds no competing methodology, duplicate ownership, stale links, or tool-specific lock-in in 00–06.
- [x] Every copied or substantially adapted third-party component has traceable provenance and all required license, attribution, notice, and trademark safeguards.
- [ ] After acceptance, move durable rules/assets to their owners and delete this TODO.

## §10 | Final rollout order

1. Reconcile any remaining external copies into this repository, declare the repository canonical, and prevent independent writable mirrors.
2. Establish third-party notices, retained licenses, provenance rules, and the pre-merge licensing check before adapting or copying external material.
3. Finalize the `dset/` change-package contract, including separate test-plan and eval-plan artifacts, small/standard/large/defect/adoption profiles, readiness gates, failure behavior, and archive transaction.
4. Finalize the large-project package tree, global/package ownership rules, dependency DAG, and `dset` namespace contract.
5. Formalize and exercise the Solution Landscape and Reuse Gate with competing framework/library proofs.
6. Build the minimum repository-owned templates, schemas, validator, canonical command, and baseline fixtures required to evaluate a pilot.
7. Evaluate OpenSpec CLI reuse against the same requirements; adopt code only if it preserves the canonical `dset/` contract without a parallel root.
8. Run the three-change Claudian pilot and exercise package-local and global proof.
9. Correct the contracts and minimum tooling from pilot evidence.
10. Exercise the Shift-Left and Back-to-Left Repair Loop with an evidence-backed defect fixture.
11. Adapt the three first-wave workflow skills and refine existing stages with the non-skill review/task/design ideas.
12. Update only the owning 00–06 sections and ensure all repository documentation uses portable Markdown links.
13. Harden validators, traceability, advanced fixtures, migration guidance, and licensing checks across supported platforms.
14. Run independent methodology, implementation, documentation-link, and licensing/provenance reviews.
15. Adopt the framework as the default for qualifying changes, then delete this TODO after all durable outputs are linked from their canonical owners.
