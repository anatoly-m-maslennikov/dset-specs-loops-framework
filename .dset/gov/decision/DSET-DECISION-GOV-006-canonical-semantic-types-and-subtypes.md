# Decision — Canonical semantic Types and subtypes

- **Decision ID:** `DSET-DECISION-GOV-006`
- **Status:** accepted
- **Decision date:** 2026-07-20
- **Resolves Question:** direct operator definition of the canonical DSET Type
  and subtype model
- **Absorbs:** `DSET-DECISION-GOV-005` in full
- **Replaces claims:** the standalone Conflict-Type claim and the classification
  of Risk as a Problem in `DSET-DECISION-GOV-003`; its immutability, priority,
  absorption, and role-aware conflict-handling claims remain active
- **Priority:** unknown pending the registered core-v1 scale
- **Selected option:** use exactly four core semantic Types—Decision, Question,
  Problem, and QA—with bounded subtypes and no synthetic family layer
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Context and scope

DSET currently mixes semantic entities, document roles, lifecycle roles, and
workflow containers under the term “artifact type.” It also represents
Opportunity and Conflict as standalone Types, classifies Risk as a Problem,
and treats Requirements and Contracts as authority peers of Decisions.

The operator has now fixed a smaller model. Every Requirement, Constraint, and
Contract originates in direct operator input or explicit operator acceptance
and states what the project must provide, avoid, use, or preserve. They are
therefore specialized Decisions in DSET. Tests and Evaluations are the two
distinct QA subtypes. Current insufficiencies are Problems; unresolved
knowledge, incompatible authority, future uncertainty, and optional value are
Questions with more precise subtypes when applicable.

This Decision governs semantic atomic Types. It does not turn hubs,
specifications, plans, implementation files, evidence, verification, Changes,
or releases into additional semantic Types. Those remain document roles,
artifact layers, derived views, or optional workflow containers.

## Decision

DSET has exactly four core semantic Types:

| Type | Empty subtype means | Allowed subtypes |
|---|---|---|
| **Decision** | An authoritative operator-accepted instruction or consequential choice that is not more precisely a Requirement, Constraint, or Contract | `requirement`, `constraint`, `contract` |
| **Question** | Missing knowledge, interpretation, or choice that is not more precisely a Conflict, Risk, or Opportunity | `conflict`, `risk`, `opportunity` |
| **Problem** | A presently true, evidence-backed insufficiency that is not more precisely a Defect, Gap, or Debt | `defect`, `gap`, `debt` |
| **QA** | Not permitted for an emitted QA atom because its proof semantics would be ambiguous | `test`, `evaluation` |

`subtype` never repeats its Type. A general Decision is represented by
`type: decision` with no subtype, not by `type: decision` plus
`subtype: decision`. The same empty-subtype rule applies to general Questions
and Problems. Every emitted QA atom must declare either `test` or
`evaluation`.

When a subtype exists, its full name is the artifact's external kind and ID
kind. For example, a Requirement uses `type: decision`,
`subtype: requirement`, and a `REQUIREMENT` ID; a general Decision omits the
subtype and uses a `DECISION` ID. Type and subtype are fixed when the atom is
emitted and never change with workflow, status, location, or intended action.

## Canonical subtype boundaries

### Decision

- **Requirement** states an observable result, behavior, capability, quality,
  or outcome the project must provide or prevent.
- **Constraint** restricts the acceptable solution space, including required or
  forbidden technologies, dependencies, environments, resources, formats, or
  operating limits.
- **Contract** states an obligation at a boundary between the project and an
  external system or between project components, including provider, consumer,
  interface, schema, protocol, compatibility, and failure obligations.

Operator input is the source of project authority. A law, DDL, OpenAPI schema,
library policy, platform rule, or customer document is source material until
the operator explicitly supplies or accepts it as a project Decision. The
source remains linked provenance; the accepted Decision owns project authority.

### Question

- **Conflict** records verified incompatible active and applicable authority
  claims over the same scope, concern, and effective time. It is unresolved
  spec-level authority, not a runtime defect.
- **Risk** records an uncertain future harmful condition with likelihood,
  impact, trigger, and mitigation where useful. A harm that is already true is
  a Problem instead.
- **Opportunity** records a possible beneficial improvement when no current
  obligation is unmet. Once the operator accepts it as required, a new
  Requirement owns that authority.

A factual Question may close through sufficient evidence. A consequential
choice closes through a Decision. Resolution never edits the Question atom; an
append-only lifecycle event links its answer or resolving Decision.

### Problem

- **Defect** records current behavior or implementation that contradicts an
  active Decision or its current evergreen projection.
- **Gap** records a required capability, artifact, proof, or other obligation
  that is currently absent.
- **Debt** records a knowingly accepted compromise that works sufficiently now
  but creates continuing maintenance, supportability, delivery, or future
  correction cost.

Missing now is a Gap; wrong now is a Defect; working through a known costly
compromise is Debt; possible future harm is Risk; and an optional improvement
without a present obligation is Opportunity. Record one primary subtype and
link causes or related atoms instead of duplicating the same condition.

### QA

- **Test** defines a deterministic check with declared conditions and an exact
  reproducible pass/fail result.
- **Evaluation** defines a qualitative, probabilistic, statistical, or
  model-judged assessment with an explicit method, rubric or metric, threshold,
  and calibration or uncertainty treatment where applicable.

A QA atom defines what must be checked. Its execution result is evidence used
by derived Verification; neither a passing Test nor Evaluation becomes project
authority.

## Authority and flow

Operator input becomes a Decision. Active Decisions compile into mutable
evergreen specifications and plans. Implementation follows that current
projection and retains Decision provenance. QA checks implementation against
the accepted authority. A failure creates or updates the derived state around a
Problem; an unclear correction raises a Question, while a correction already
governed by current Decisions returns directly to implementation.

Problems and Questions route work but never authorize implementation merely by
existing. QA changes assurance, not authority. Supportability is a cross-cutting
concern applied to the evergreen, implementation, QA, and Verification layers;
it is not another semantic Type.

## Consequences and discharge

This Decision must compile into:

- the canonical public Type/subtype definitions and README workflow;
- repository-local work-item, artifact-maintenance, and architecture rules plus
  their distributed templates;
- the self-hosted GOV domain, specification, deterministic Test plan, and
  qualitative Evaluation plan; and
- schemas, validators, templates, fixtures, traceability, and health views
  before DSET claims the representation is implemented end to end.

Existing emitted atoms remain immutable. Legacy Opportunity and Conflict Types,
Risk classifications, and separate Requirement/Contract authority records must
not be silently retyped in place. A schema migration must preserve their IDs,
content digests, provenance, and successor or absorption links.

## Rationale

Four semantic Types give operators a small stable vocabulary. Subtypes add
precision without creating parallel top-level concepts or workflow-defined
entities. Separating semantic Types from document and lifecycle roles also lets
the same model govern code, documentation, methodologies, local tools,
services, and monorepos without pretending that every file is the same kind of
record.

## Lifecycle policy at emission

- **Expected confirmation evidence:** classification fixtures cover every
  empty subtype and named subtype, boundary cases, workflow independence, and
  Test/Evaluation separation
- **Known counter-evidence:** current schemas and validators still encode
  Opportunity and Conflict as standalone Types and do not expose the complete
  Type/subtype representation
- **Reopen when:** ordinary artifacts cannot be classified without multiple
  primary Types or an allowed subtype has incompatible lifecycle semantics
- **If reopened, retain:** operator authority, semantic classification
  independent of workflow, atomic immutability, and Test/Evaluation separation
- **Retirement condition:** a validated successor absorbs every active claim
  and no current schema, projection, skill, or implementation relies on this
  Decision

This emitted Decision atom is immutable. Any later correction, status change,
counter-evidence, absorption, or retirement must be represented by a new atom
or append-only lifecycle event.
