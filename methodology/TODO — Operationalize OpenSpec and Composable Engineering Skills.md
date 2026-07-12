# TODO — Operationalize OpenSpec and Composable Engineering Skills

**Outcome:** Keep [[00_Tool Development Playbook]] as the canonical methodology, make its SPEC → EVAL/TEST PLAN → IMPL PLAN → CODE → GATES pipeline operational in repositories through an OpenSpec-derived change package, and add only the Matt Pocock workflows that fill real gaps. Do not install a second methodology or duplicate rules already owned by 00–06.

**Sources:** [[Fission - OpenSpec (github.com, 2025-08-05)]], [[Matt Pocock - skills (github.com, 2026-02-03)]], [OpenSpec](https://github.com/Fission-AI/OpenSpec), [Matt Pocock’s skills](https://github.com/mattpocock/skills).

## §0 | Decisions to preserve

- [ ] Keep `51_DEV/00_META/00_Methodology/` as the human-owned source of truth; external frameworks inform it but do not govern it.
- [ ] Keep the five-stage pipeline and the existing document ownership boundaries in 00–05.
- [ ] Use OpenSpec for repo-local change packaging and current-truth reconciliation, not as a replacement methodology.
- [ ] Adapt selected Matt Pocock workflows into small vault-native skills only when each skill runs a distinct workflow.
- [ ] Do not install BMAD or the complete Superpowers/Matt Pocock workflow stack as another orchestration layer.
- [ ] Require one pilot and evidence before making the new change package the default for all repositories.

### Source-of-truth ownership to formalize

| Concern | Authoritative source |
|---|---|
| Accepted behavioral requirements | `openspec/specs/` |
| Stored data shape and constraints | DDL/schema linked from the behavioral spec |
| Architectural rationale and accepted decisions | ADRs linked from `design.md` |
| Runtime state and observed outcomes | The external system, durable store, or append-only event log |
| Work-in-progress change intent and evidence | `openspec/changes/<change-id>/` until archive |

## §1 | Define the repository change-package contract

- [ ] Decide the canonical repo-local root. Start the pilot with `openspec/`; change the name only if a concrete collision appears.
- [ ] Define `openspec/specs/` as accepted current truth and `openspec/changes/<change-id>/` as bounded work in progress.
- [ ] Inventory each pilot repository’s existing spec roots before creating `openspec/`; define an explicit migration or compatibility map and never leave two writable sources of truth for the same concern.
- [ ] Define a stable lowercase kebab-case `<change-id>` convention.
- [ ] Define the required artifact set:

```text
openspec/
├── specs/                              # Accepted current truth
└── changes/
    └── <change-id>/
        ├── proposal.md                 # Why, scope, non-goals, risk
        ├── specs/                      # ADDED/MODIFIED/REMOVED requirements
        ├── eval-plan.md                # Proof designed with the spec, before code
        ├── design.md                   # Technical design linking accepted ADRs
        ├── implementation-plan.md      # Ordered batches and rollout
        ├── tasks.md                    # Executable checklist
        └── verification.md             # Fresh commands, redacted summaries, evidence pointers
```

- [ ] Define which artifacts may collapse for a small fix. Minimum: proposal/scope, acceptance proof, tasks, and verification must survive.
- [ ] Define artifact readiness gates rather than rigid waterfall phases: implementation may start only when requirements and proof are explicit, but any artifact may be corrected when new evidence appears.
- [ ] Require each requirement to carry a stable ID and at least one scenario or acceptance check.
- [ ] Require delta specs to mark requirements as `ADDED`, `MODIFIED`, or `REMOVED` and identify the current-truth target they affect.
- [ ] Require `eval-plan.md` to distinguish deterministic checks, integration/E2E checks, and probabilistic/LLM evals where applicable.
- [ ] Require `implementation-plan.md` to map every batch to requirement IDs and eval IDs.
- [ ] Require `verification.md` to record fresh commands, exit status, redacted result summaries, evidence pointers, unresolved failures, and whether completion is accepted; do not persist secrets or sensitive full command output.
- [ ] Require schema validation to prove the dependency graph: proposal → delta specs plus eval plan → design plus implementation plan → tasks → verification → archive.
- [ ] Define the archive transaction: verify → reconcile deltas into `openspec/specs/` → preserve the completed change under `openspec/changes/archive/YYYY-MM-DD-<change-id>/` → run spec-sync/link checks.
- [ ] Define failure behavior: an incomplete or failed change remains unarchived and its current-truth specs remain unchanged.

## §2 | Define the large-project package tree

- [ ] Make a package tree mandatory for a large project; do not use file count or lines of code as the primary threshold.
- [ ] Classify a project as large when it has multiple independently meaningful capabilities, deployment units, domain boundaries, ownership/security boundaries, or cross-feature workflows that cannot be understood and verified comfortably as one unit.
- [ ] Keep a small project as one implicit package until decomposition reduces actual cognitive load.
- [ ] Define a **package** as a cohesive capability or architectural unit with an explicit boundary, public contract, owned domain vocabulary, accepted requirements, local tests/evals, and dependency edges. A package is not necessarily a published code package.
- [ ] Put system-wide truth above the package tree and package-specific truth inside it:

```text
openspec/
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
- [ ] Require package IDs, requirement IDs, test/eval IDs, change IDs, and evidence pointers to remain traceable across the tree.
- [ ] Define package split, merge, rename, and retirement as explicit changes with spec, contract, dependency, test/eval, and migration updates.

### Framework namespace and naming contract

- [ ] Adopt **`dset`** as the canonical machine namespace and **`dset-`** as the canonical human-visible prefix. Keep **DSET Loops Framework** as the display name and expand DSET as **Domain–Spec–Eval–Test**.
- [ ] Do not use `dsetl-`: “loops” is part of the display/mental model, while adding `l` makes the namespace harder to pronounce and visually closer to the established SETL language family.
- [ ] Reserve framework-owned names; do not prefix ordinary product features, domain packages, or application code merely because they use the framework.

| Surface | Convention | Examples |
|---|---|---|
| Framework display name | `DSET Loops Framework` | README title, documentation title |
| Short name | `DSET Loops` | prose, diagrams, discussion |
| Machine namespace | `dset` | CLI, config root, schema IDs |
| Skills | `dset-<workflow>` | `dset-grill`, `dset-diagnose`, `dset-prototype`, `dset-review` |
| Framework-owned folders | `dset/` or `.dset/` by ownership | `dset/specs/`, `.dset/cache/` |
| Framework-owned files | `dset[.<purpose>].<ext>` | `dset.toml`, `dset.schema.json` |
| Commands | `dset <verb>` | `dset new`, `dset check`, `dset verify`, `dset archive` |
| Environment variables | `DSET_<NAME>` | `DSET_CONFIG`, `DSET_NO_TELEMETRY` |
| CI jobs | `dset-<gate>` | `dset-spec-sync`, `dset-evals`, `dset-release-gate` |
| GitHub labels | `dset:<state>` | `dset:proposal`, `dset:ready`, `dset:blocked` |
| Change IDs | unprefixed kebab-case inside the namespace | `tmux-controls`, not `dset-tmux-controls` |
| Package IDs | unprefixed domain/capability names | `conversation-history`, not `dset-conversation-history` |

- [ ] If the official OpenSpec CLI is adopted, retain its required `openspec/` artifact root and use `dset-` only for framework-owned skills, validators, profiles, and extensions; do not create a parallel `dset/specs/` tree.
- [ ] If vault-owned tooling is selected instead, prefer `dset/` as the visible artifact root:

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

- [ ] Keep committed source-of-truth artifacts under visible `dset/`; reserve hidden `.dset/` for generated, local, cached, or machine-owned state.
- [ ] Never maintain both `openspec/specs/` and `dset/specs/` as writable sources for the same project; the CLI/tooling decision selects one artifact root.
- [ ] Publish a reserved-name list and make the validator reject ambiguous framework-owned paths or mixed namespaces.

## §3 | Decide whether to use the OpenSpec CLI

- [ ] Test the current OpenSpec CLI in a disposable repository, not first in a live project.
- [ ] Check whether a custom schema can require `eval-plan.md`, `implementation-plan.md`, and `verification.md` without fighting upgrades.
- [ ] Check generated agent instructions for context bloat, conflicting rules, tool-specific assumptions, and unexpected file rewrites.
- [ ] Check whether `propose`, `apply`, `verify`, and `archive` preserve the methodology’s stage ownership and evidence gates.
- [ ] Check update behavior and telemetry controls before adoption.
- [ ] Compare CLI-backed operation with a small vault-owned template/script implementation.
- [ ] Choose the CLI only if it reduces maintenance while preserving the exact local contract; otherwise keep the OpenSpec model and own the templates/scripts.

## §4 | Pilot the contract in Claudian

- [ ] Split the current Claudian input work into three independent changes because the verification gates differ: input growth first, readline keybindings second, tmux controls last.
- [ ] Map Claudian’s existing `claudian_plus_specs/1 - Spec/`, `2 - Eval Plan/`, and `2 - Implementation Plan/` artifacts into the pilot contract; decide whether to migrate, redirect, or retain them as read-only history before writing new current-truth specs.
- [ ] Pilot **input growth** first: reconstruct intent without treating unfinished code as the specification, write the 50%-height/layout scenarios and eval plan, correct the implementation, verify it, and archive it before starting the next change.
- [ ] Pilot **readline keybindings** second: specify cursor, deletion, selection, conflict, and platform behavior; test the public input seam with independent expected-value oracles; implement one vertical red/green slice per keybinding group.
- [ ] Pilot **tmux controls** last: specify prefix parsing, command configuration, tab numbering/navigation, confirmation, tab/session lists, accessibility, settings lifecycle, and conflict behavior; separate pure key routing from Obsidian integration.
- [ ] Execute the pilot under the existing TDD, typed, lint, layering, and verification gates.
- [ ] Scale pilot review by risk: gates/self-review for the mechanical input-growth change, one independent review for readline behavior, and separate spec-compliance and code-quality reviews for tmux controls.
- [ ] Archive only after the delta specs reconcile cleanly into current truth and all accepted verification evidence is recorded.
- [ ] Retrospect: record friction, missing artifacts, redundant ceremony, agent context cost, and whether the structure improved recovery after interruption.

## §5 | Adapt the useful Matt Pocock workflows

### Adopt first

- [ ] **`grill-with-docs` plus `domain-modeling` pattern** — create one vault-native pre-spec interview workflow that resolves ambiguous branches, sharpens ubiquitous language, stress-tests entities/invariants with edge cases, and records ADRs before a spec is accepted.
- [ ] **`diagnosing-bugs` pattern** — create a disciplined reproduce → minimise → hypothesise → instrument → fix → regression-test workflow; diagnosis must remain separate from implementation authorization.
- [ ] **`prototype` pattern** — define an explicitly disposable prototype lane for answering design questions; require a decision record before any prototype code is promoted.

### Refine existing stages after the pilot; do not create first-wave standalone skills

- [ ] **`code-review` pattern** — refine review around a fixed comparison point, explicit spec/standards sources, and separately reported compliance and quality findings.
- [ ] **`to-tickets` tracer-bullet pattern** — add dependency edges and independently verifiable vertical slices to implementation tasks when work spans sessions.
- [ ] **`handoff` pattern** — add an optional pointer-only summary when the change package itself is insufficient; do not duplicate its contents.
- [ ] **`codebase-design` pattern** — add a deep-module/interface-pressure rubric to design and review: prefer more behavior behind smaller stable interfaces and test through those interfaces.

### Consider only after a demonstrated gap

- [ ] **`wayfinder` pattern** — add only for investigations too large for one change package; its output must feed a later bounded change, not become a permanent parallel planning system.

### Do not duplicate

- [ ] Do not import `to-spec` as a second spec format; the OpenSpec-derived change package owns repo-local specifications.
- [ ] Do not import another generic `tdd` methodology; strengthen [[02_Eval and Test Plan Patterns — Test Plan Authoring Conventions]] and [[05_Layered Build Standard — DDD, TDD, Small Functions, Typed Gates]] with any missing executable details.
- [ ] Do not import `implement` as a competing execution orchestrator; implementation follows the accepted change package and repo-local agent contract.
- [ ] Do not import generic `research` where the existing reference workflow already creates source-backed records.
- [ ] Do not import `triage` until a real issue-tracker state-machine gap is demonstrated.
- [ ] Do not copy third-party skills verbatim into the canonical methodology. Extract the workflow, preserve provenance, adapt terminology, validate behavior, and keep the vault copy canonical.

## §6 | Map accepted changes back into 00–06

- [ ] Update [[00_Tool Development Playbook]] only with the scale/routing rule: when a repo-local change package is required and when a lightweight inline artifact is enough.
- [ ] Update [[01_Spec Authoring Patterns — Service Spec Conventions]] with the final current-truth, delta-spec, requirement-ID, and scenario contract.
- [ ] Update [[02_Eval and Test Plan Patterns — Test Plan Authoring Conventions]] with the final `eval-plan.md` and `verification.md` contracts, the diagnosis workflow boundary, public-seam testing, independent expected-value oracles, and one vertical red/green slice per cycle.
- [ ] Update [[03_Implementation Plan Patterns — Service Build Conventions]] with artifact readiness, batch mapping, archive transaction, failed-change behavior, and the deep-module design rubric.
- [ ] Update [[04_General Build Rules — Tool Code Conventions]] only if pilot evidence reveals a genuinely universal rule not already owned elsewhere.
- [ ] Update [[05_Layered Build Standard — DDD, TDD, Small Functions, Typed Gates]] with deterministic spec-sync/archive gates, public-seam TDD enforcement where feasible, and risk-scaled review.
- [ ] Update [[06_External Grounding — LLM Power-User Practice]] with Matt Pocock’s skills as provenance and refresh OpenSpec provenance after the pilot.
- [ ] Keep detailed templates and executable workflows out of 00–06; place them in repo templates, scripts, or focused vault-native skills and link to them.
- [ ] Update [[00_Tool Development Playbook]]’s document map only if a permanent new governing document is truly required. This TODO is temporary and should not become stage 7.

## §7 | Build the reusable assets

- [ ] Create the approved change-package template in the canonical owned tooling location.
- [ ] Create a validator that checks required artifacts, IDs, delta markers, links, task-to-requirement/eval mapping, archive readiness, and current-truth reconciliation.
- [ ] Make the validator cross-platform and runnable through one canonical command.
- [ ] Create only the three accepted focused skills from §5; keep each skill small, script-backed where useful, and explicit about trigger/stop conditions.
- [ ] Install custom skills through the existing vault-to-runtime symlink workflow; never maintain copied canonical duplicates.
- [ ] Add fixtures containing one small fix, one normal feature, one failed/unarchived change, and one archived change.
- [ ] Add a migration guide for repositories with existing specs and implementation-plan folders.

## §8 | Acceptance criteria

- [ ] The methodology remains understandable without installing OpenSpec or Matt Pocock’s skills.
- [ ] One repo-local change folder contains intent, proof, design, execution, and verification without duplicating the same rule across artifacts.
- [ ] Every large project has a justified package tree, explicit global artifacts, a dependency DAG, and no duplicated source of truth across global and package specs.
- [ ] Every package can be understood and verified as a bounded unit, while global E2E tests and evals prove cross-package behavior.
- [ ] Framework-owned skills, commands, folders, files, CI gates, and environment variables follow the `dset` namespace contract without prefixing ordinary product/domain names.
- [ ] Tests/evals are designed before implementation and remain independently reviewable.
- [ ] Archiving is deterministic, preserves history, and cannot silently overwrite current truth after failed verification.
- [ ] Every adopted skill fills a documented gap and has a distinct trigger, output, verification step, and stop condition.
- [ ] Review effort scales with risk: gates/self-review for mechanical changes, one independent review for normal changes, and separate spec-compliance and code-quality reviews for high-risk changes.
- [ ] Agents can resume an interrupted change from files alone without relying on chat history.
- [ ] The canonical verification command detects malformed change packages and spec drift.
- [ ] The Claudian pilot demonstrates lower ambiguity and reliable recovery without unacceptable ceremony or context overhead.
- [ ] Independent review finds no competing methodology, duplicate ownership, stale links, or tool-specific lock-in in 00–06.
- [ ] After acceptance, move durable rules/assets to their owners and delete this TODO.

## §9 | Final rollout order

1. Finalize the change-package contract.
2. Finalize the large-project package tree, decomposition decision guide, global/package ownership rules, and `dset` namespace contract.
3. Evaluate CLI versus vault-owned templates/scripts.
4. Run the three Claudian pilots and exercise both package-local and global proof.
5. Correct the contracts from pilot evidence.
6. Adapt the three first-wave Matt Pocock workflow patterns and refine existing stages with the non-skill review/task/design ideas.
7. Update only the owning 00–06 sections.
8. Build validators, fixtures, and migration guidance.
9. Run independent methodology and implementation reviews.
10. Adopt as the default for qualifying changes.
11. Delete this TODO after all durable outputs are linked from their canonical owners.
