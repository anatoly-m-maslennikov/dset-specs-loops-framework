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

## DSET-REQUIREMENT-META-008 — Contract Decisions preserve boundaries

When the operator supplies or accepts a DDL, CSV/XLSX schema,
OpenAPI/message/protocol, host-native package format, supported-platform
interface, hosted-CI interface, dependency boundary, or comparable obligation,
DSET must represent it as `type: decision`, `subtype: contract`. A Contract uses
a stable `CONTRACT` ID. Each immutable atom names the accepted source,
direction, provider, consumer, conformance rule, compatibility rule, priority,
creation state, and any older Contract atoms it absorbs. External formats are
pinned by version or digest in applicable evidence.

Contract lifecycle is derived from append-only events. Implementation conforms
to every applicable active Contract and cannot rewrite the boundary. Ambiguity
routes to a Question; incompatible active authority becomes Question/Conflict;
observed nonconformance becomes Problem/Defect. A general or unrelated Decision
does not silently override a Contract; change requires explicit precedence or
an operator-accepted absorbing Contract. A mandated dependency is
Decision/Constraint when it restricts the solution space and Decision/Contract
when a boundary participant relies on it.

**Scenario DSET-SCENARIO-META-009:** The operator accepts host, platform,
dependency, and GitHub Actions boundaries as Contract Decisions. Descriptive
Markdown or local scripts alone cannot satisfy them. An unclear host format is
a Question, incompatible active formats are a Question/Conflict, and a failing
platform or disallowed dependency is a Problem with the applicable subtype.

## DSET-REQUIREMENT-META-009 — User Story is a direct Requirement subtype

When meaningful, accepted project truth records a User Story with
`type: decision`, `subtype: user_story`, and a stable `STORY` compatibility ID.
It captures the actor or stakeholder, desired capability or outcome, and value
or purpose without absorbing acceptance criteria. User Story, Requirement,
Constraint, Contract, Outcome, Scenario,
and Invariant are sibling Requirement subtypes. Links among them never create
subtype nesting, and a User Story is never represented as
Decision/Requirement/User Story.

Each sibling owns its own semantics: Requirement owns residual observable
obligations; Constraint narrows solutions when no boundary participant relies
on the restriction; Contract owns boundary obligations; Outcome owns intended
measurable state change; Scenario owns a concrete accepted behavior rather than
its execution; Invariant owns an always-true condition rather than evidence
that it currently holds. Design owns internal logic
and implementation plans own build order. A package with no meaningful actor
perspective may omit User Story without inventing one.

**Scenario DSET-SCENARIO-META-010:** `DSET-STORY-SKILL-001` states that a
contributor wants a released DSET skill to load in a declared host and links to
sibling Requirement, Contract, Scenario, and QA atoms. The links make behavior
traceable without making any atom a subtype of User Story or Requirement.

## DSET-REQUIREMENT-META-010 — Outcomes measure intended state change

An accepted Outcome uses `type: decision`, `subtype: outcome`, and a stable
`OUTCOME` ID. It describes a measurable change in user, business, operational,
or system state that the project intends rather than a delivered output,
feature, or observed result and records its
baseline, target, observation method/source, evaluation window, originating
Problem or Question/Opportunity links, relevant sibling User Story links, and
applicable QA/Evaluation links. A model-only methodology change does not invent
a concrete Outcome atom.

Requirement and Outcome are sibling Requirement forms with different proof. A
Requirement defines observable behavior or result the implementation must
deliver. Deterministic QA/Test evidence proves delivery. Outcome observations
are evidence and use
the declared source and window to show whether delivery produced the intended
state change; shipping an artifact alone cannot satisfy an Outcome.

**Scenario DSET-SCENARIO-META-011:** A Requirement states that the release
workflow records a stable failed check on the exact pull-request SHA. A linked
operational Outcome instead targets a measurable reduction from a recorded
baseline in time-to-diagnose failed releases over a stated window, using hosted
check/run timestamps as its observation source and QA/Evaluation to judge the
evidence. Adding the workflow file proves the Requirement, not the Outcome.

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
