# Methodology META specification

## DSET-REQUIREMENT-META-001 — One governed pipeline

The methodology must define one five-stage pipeline: spec; test plan plus eval plan; implementation plan; code under general rules; and executable enforcement.

**Scenario DSET-SCENARIO-META-001:** Given a contributor deciding where a rule belongs, the document map identifies exactly one owning stage document and treats cross-links as pointers rather than duplicate ownership.

## DSET-REQUIREMENT-META-002 — Tests and evals remain distinct

The methodology must keep deterministic tests in `test-plan.md` and probabilistic or qualitative evaluation in `eval-plan.md`.

**Scenario DSET-SCENARIO-META-002:** Given behavior with one exact expected output, it is routed to the test plan even when the check is automated. Given multiple acceptable outputs judged by criteria or a rubric, it is routed to the eval plan.

## DSET-REQUIREMENT-META-003 — Runtime rules are selected by independent concerns

The methodology must select recovery semantics by runtime risk and durable backing by topology, write volume, and concurrency. Event sourcing, reconciliation, durable execution, and observed-progress liveness apply only when their specific semantics are required.

**Scenario DSET-SCENARIO-META-003:** A stateless CRUD service keeps durable state in its database without adding an application file WAL or event store unless audit/replay requirements independently demand one.

**Scenario DSET-SCENARIO-META-004:** A modest-write local resumable tool keeps accepted state in declared files with one writer and atomic/durable writes; a higher-volume or concurrent local tool selects a database instead of two writable authorities.

## DSET-REQUIREMENT-META-004 — Delivery semantics are bounded

The methodology must describe retries as at-least-once delivery plus receiving-side deduplication or idempotency. It may claim effectively-once effects only inside the declared key, retention, and atomicity boundary.

**Scenario DSET-SCENARIO-META-005:** A retryable receiver documents its deduplication key, retention window, owner, and atomic check/write operation without claiming universal exactly-once execution.

## DSET-REQUIREMENT-META-005 — Public identity is stable

The public framework identity must use the display name **DSET Spec Loops**, the title **DSET Spec Loops: A Production Vibecoding Framework**, the expansion **Domain–Supportability–Evals–Tests**, and the repository slug `dset-specs-loops-framework`.

**Scenario DSET-SCENARIO-META-006:** README, project metadata, repository slug, and active methodology truth use the same identity; historical archive evidence may retain prior URLs when redirects preserve the recorded provenance.

## DSET-REQUIREMENT-META-006 — Profile axes remain orthogonal

DSET must select implementation-language enforcement and artifact-governance enforcement independently. Runtime risk selects recovery/supportability semantics; durability topology selects durable authority; a language profile selects code tools and thresholds; an artifact profile selects document architecture, ownership, navigation, and authoring gates.

**Scenario DSET-SCENARIO-META-007:** A Python repository selects `python-v1` and `documentation-v1` together; a documentation-only repository selects `documentation-v1` without inheriting Python tools; a future TypeScript repository combines its own language profile with the same artifact profile.

## DSET-REQUIREMENT-META-007 — DSET 0.3 proof categories remain separate

Exact resolver, ownership, path, identity, wrapper, and recursion behavior must be proven by deterministic tests. Agent interpretation, rule-following, navigation, and diagnostic usefulness must be proven by separate qualitative or probabilistic evals. Automation does not change the proof category.

**Scenario DSET-SCENARIO-META-008:** A scripted assertion that a cycle emits one stable code remains a test; an automated agent run measuring whether the diagnostic enables a safe correction remains an eval.

## DSET-REQUIREMENT-META-008 — Contracts preserve authoritative boundaries

An existing DDL, required CSV/XLSX schema, supplied OpenAPI/message/protocol, host-native package format, supported-platform interface, hosted-CI interface, dependency policy, or comparable externally constrained boundary must be represented as a first-class Contract when implementation is not authorized to redefine it. A project-wide Contract uses `DSET-CONTRACT-<NNN>` and a layer-owned Contract uses `DSET-CONTRACT-<LAYER>-<NNN>`. Each record must name its authority, source, exactly one record version or digest, direction, producer, consumer, conformance rule, compatibility rule, and lifecycle state. Sources that define external formats must themselves be pinned by version or digest in the applicable release evidence.

Contract lifecycle is `declared -> active -> superseded` or `declared -> active -> retired`. An implementation must conform to every applicable active Contract and cannot edit the boundary to fit itself. Only the named authority may issue the superseding version. Ambiguity routes to a Question; demonstrated incompatibility routes to a Problem; a Decision cannot override a Contract. A mandated dependency is therefore a Contract constraint rather than a Decision, although a consequential choice among Contract-allowed alternatives may become a Decision.

**Scenario DSET-SCENARIO-META-009:** A release claims support for Claude, Codex, macOS, native Windows, WSL, Linux, and protected GitHub pull requests while also adopting a governed dependency set. `DSET-CONTRACT-SKILL-001` requires real install/load/invoke proof for each declared host-native skill package, `DSET-CONTRACT-TOOL-001` requires platform execution or an honest pre-release non-applicability declaration, `DSET-CONTRACT-TOOL-002` constrains dependencies and exceptions, and `DSET-CONTRACT-OPS-001` requires a real workflow and hosted run on the exact PR head. Descriptive Markdown or local scripts alone cannot satisfy those Contracts. An unclear host format becomes a Question, a failing platform or disallowed dependency becomes a Problem, and no Decision rewrites the active boundary.

## DSET-REQUIREMENT-META-009 — User Stories add optional actor and value context

When a meaningful User Story exists, accepted project truth may record it with project-wide ID `DSET-STORY-<NNN>` or layer-owned ID `DSET-STORY-<LAYER>-<NNN>`. A User Story must capture the actor or stakeholder, desired capability or outcome, value or purpose, and links to the normative Requirements and applicable Scenarios that make the desired behavior verifiable. A package with no meaningful User Story remains valid without one. User Stories are accepted truth, not a fourth intake queue, and never substitute for a normative verifiable Requirement. `STORY` is the compact ID token for the public User Story entity.

Artifact boundaries remain explicit. A Requirement states observable, verifiable delivered behavior, result, or constraint. An observable edge case is a Scenario. A consequential choice among alternatives is a Decision only when its rationale, tradeoffs, and consequences matter; ordinary implementation details are not Decisions. Internal logic belongs to Design, build and rollout sequence belongs to the implementation plan, and a boundary the project is not authorized to choose or rewrite is a Contract.

**Scenario DSET-SCENARIO-META-010:** `DSET-STORY-SKILL-001` states that a contributor wants a released DSET skill to load in the contributor's declared host so the workflow is usable there, then links to the exact host-native packaging Requirement and install/load/invoke Scenarios. The pinned host format remains a Contract, a failed-load edge case remains a Scenario, loader internals remain Design, and the build order remains in the implementation plan. If no meaningful actor perspective adds context, the package omits a User Story and retains the Requirements.

## DSET-REQUIREMENT-META-010 — Outcomes measure intended state change

An accepted Outcome uses project-wide ID `DSET-OUTCOME-<NNN>` or layer-owned ID `DSET-OUTCOME-<LAYER>-<NNN>`. It must describe a measurable change in user, business, operational, or system state rather than a delivered output or feature, and record its baseline, target, observation method and source, evaluation window, originating Problem or Opportunity links, relevant User Story links when User Stories exist, and applicable Eval links. An Outcome is accepted truth, not an intake queue or item. A model-only methodology change may define Outcome without inventing a concrete Outcome record.

Requirements and Outcomes own different proof. A Requirement defines the observable, verifiable behavior, result, or constraint the implementation must deliver. Deterministic Requirement evidence proves delivery. Outcome evidence observes the declared source over the declared evaluation window and shows whether the delivered behavior produced the intended state change; shipping a feature or artifact alone cannot satisfy an Outcome.

**Scenario DSET-SCENARIO-META-011:** A Requirement states that the release workflow records a stable failed check on the exact pull-request SHA. A linked operational Outcome may instead target a measurable reduction from a recorded baseline in time-to-diagnose failed releases over a stated window, using hosted check/run timestamps as its observation source and an Eval to judge the evidence. Adding the workflow file proves the Requirement, not the Outcome.

## DSET-REQUIREMENT-META-011 — Work Areas bound repository scope without assuming implementation type

DSET must support either one repository-level scope or one or more declared Work
Areas. A Work Area is a repository-relative folder declaration used to scope
accepted truth, Changes, proof, runs, and operational handoffs. Its content may
be a local tool, deployable service, library, documentation, methodology, data,
or any mixture of these. Declaring a Work Area must not classify it as code,
deployable, a service, a feature, or a module, and DSET must not require those
properties to use the boundary.

The repository's accepted Work Area declaration is authoritative. A session or
session checkpoint may reference the repository-level scope or declared Work
Areas so chained work can resume in the intended scope, but session continuity
does not own, create, rename, or supersede a Work Area. Every resume must
re-resolve the current authoritative declaration.

**Scenario DSET-SCENARIO-META-012:** A monorepo declares a deployable API folder,
a shared library folder, a documentation-and-methodology folder, and a mixed
data/tooling folder as separate Work Areas. Another repository declares only
its root. DSET scopes both projects without inventing services, modules,
features, or deployment semantics, and a resumed session follows the current
declaration rather than a stale checkpoint hint.
