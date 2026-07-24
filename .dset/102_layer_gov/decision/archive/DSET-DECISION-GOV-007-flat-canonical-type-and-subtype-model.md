---
artifact_type: implementation_decision
artifact_id: DSET-DECISION-GOV-007
scope_path: ["layer:gov"]
priority: high
decided_at: 2026-07-20
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-DECISION-GOV-006"
---

# Decision — Flat canonical Type and subtype model

- **Resolves Question:** direct operator correction prohibiting sub-subtypes and
  classifying User Story directly under Decision
- **Replaces claims:** the incomplete Decision-subtype list in
  `DSET-DECISION-GOV-006`; every other Type, lifecycle, authority, compilation,
  and migration claim is carried forward below
- **Selected option:** use exactly four Types and one optional flat subtype
  level; User Story, Outcome, Scenario, and Invariant are direct Decision
  subtypes rather than Requirement subtypes or representation forms

## Context and scope

DSET needs a small semantic model that can classify authoritative product,
governance, implementation, and QA atoms without hidden nesting. The previous
Decision correctly reduced the model to four Types but listed only Requirement,
Constraint, and Contract under Decision. That would force established
authoritative entities such as User Story, Outcome, Scenario, and Invariant to
be untyped roles or nested below another subtype.

Subtype depth is now fixed at one. An atom has a Type and either no subtype or
one direct subtype. A subtype never owns another subtype.

This Decision governs semantic atomic Types. Hubs, specifications, plans,
implementation files, evidence, Verification, Changes, and releases remain
document roles, artifact layers, derived views, or optional workflow
containers rather than additional semantic Types.

## Canonical model

| Type | Empty subtype means | Direct subtypes |
|---|---|---|
| **Decision** | General operator-accepted authority | `requirement`, `constraint`, `contract`, `user_story`, `outcome`, `scenario`, `invariant` |
| **Question** | General missing knowledge, interpretation, or choice | `conflict`, `risk`, `opportunity` |
| **Problem** | General current evidence-backed insufficiency | `defect`, `gap`, `debt` |
| **QA** | Not permitted for an emitted QA atom | `test`, `evaluation` |

The representation has exactly two semantic fields:

```yaml
type: decision
subtype: user_story
```

There is no subtype path, parent subtype, `subtype_of`, or nested subtype list.
The following representation is invalid:

```yaml
type: decision
subtype: requirement
sub_subtype: user_story
```

Omit `subtype` for a general Decision, Question, or Problem. Never repeat the
Type name as its own subtype. Every emitted QA atom declares Test or
Evaluation. Type and subtype are immutable after emission and never depend on
workflow, queue, skill, host, tool, status, filename, folder, or next action.

When a subtype exists, its full name is the external artifact and ID kind. A
User Story carries `type: decision`, `subtype: user_story`, and a `STORY` or
future full `USER-STORY` compatibility-resolved ID kind; a general Decision
omits subtype and uses `DECISION`. Existing stable IDs are not renamed in
place.

## Decision subtypes

A Decision is immutable project authority explicitly supplied or accepted by
the operator. External law, customer text, DDL, API schema, platform rules, and
library policies remain source provenance until operator acceptance.

- **Requirement** states an observable result, behavior, capability, quality,
  or outcome the project must provide or prevent.
- **Constraint** restricts acceptable solutions, including required or
  forbidden technologies, dependencies, environments, resources, formats, or
  operating limits.
- **Contract** states an obligation at a boundary between the project and an
  external system or between project components, including provider, consumer,
  interface, schema, protocol, compatibility, and failure obligations.
- **User Story** states which actor or stakeholder wants which capability or
  outcome and why it has value.
- **Outcome** states a measurable change in user, business, operational, or
  system state, including baseline, target, observation method, and evaluation
  window where applicable.
- **Scenario** states a concrete accepted behavioral example through
  preconditions, interaction or event, and observable result.
- **Invariant** states a condition that must always hold within its declared
  scope.
- An empty-subtype **Decision** owns any other accepted authoritative choice,
  including material governance, logic, design, implementation, or edge-case
  resolution.

These are sibling subtypes. A User Story may link Requirements, Outcomes,
Scenarios, and QA atoms, but those relations never make it a child of
Requirement. A Scenario may demonstrate a Requirement and an Invariant may
constrain it, but all remain direct Decision subtypes.

## Question subtypes

A Question is an immutable record of unresolved knowledge, interpretation, or
choice and never authorizes implementation merely by existing.

- **Conflict** records verified incompatible active and applicable authority
  claims over the same scope, concern, and effective time. It is spec-level
  uncertainty, not a runtime defect.
- **Risk** records an uncertain future harmful condition with likelihood,
  impact, trigger, and mitigation where useful.
- **Opportunity** records a possible beneficial improvement when no current
  obligation is unmet.
- An empty-subtype **Question** owns any other uncertainty.

Evidence may answer a factual Question. A consequential choice closes through
a Decision. Resolution uses an append-only lifecycle event linked to the
immutable Question. An accepted Opportunity becomes authority only when the
operator emits a new Decision or direct subtype.

## Problem subtypes

A Problem is an immutable record of a presently true, evidence-backed
insufficiency and does not select or authorize its correction.

- **Defect** records current behavior or implementation that contradicts an
  active Decision or its current evergreen projection.
- **Gap** records a required capability, artifact, proof, or obligation that is
  absent now.
- **Debt** records a knowingly accepted compromise that works sufficiently now
  but creates continuing maintenance, supportability, delivery, or future
  correction cost.
- An empty-subtype **Problem** owns any other current insufficiency.

Wrong now is Defect; missing now is Gap; working through a known costly
compromise is Debt; possible future harm is Risk; optional possible value is
Opportunity. Choose one primary subtype and link related causes instead of
duplicating the same condition.

## QA subtypes

QA is an immutable definition of how accepted authority is checked. It changes
assurance, not authority.

- **Test** defines a deterministic check with declared conditions and an exact,
  reproducible pass/fail result.
- **Evaluation** defines a qualitative, probabilistic, statistical, or
  model-judged assessment with an explicit method, rubric or metric, threshold,
  and uncertainty treatment where applicable.

Test code, Evaluation prompts, datasets, fixtures, and harnesses are
implementation artifacts. Execution results are evidence for derived
Verification. Neither passing nor failing QA rewrites a Decision.

## Authority and flow

Operator input becomes a Decision or direct Decision subtype. Active Decisions
compile into mutable evergreen specifications and plans. Implementation follows
those projections and retains Decision provenance. QA checks implementation
against accepted authority. A failure exposes a Problem. An unclear correction
raises a Question; a correction already governed by current Decisions returns
directly to implementation.

Problems and Questions route work but do not authorize implementation. QA owns
assurance definitions. Supportability is a cross-cutting concern over evergreen
truth, implementation, QA, and Verification rather than a semantic Type.

## Consequences and migration

This Decision must compile into the public Type catalog, repository-local
governing rules and templates, self-hosted domain/specification, Test and
Evaluation plans, README workflow, and generated traceability.

Schemas, validators, templates, fixtures, health views, and skills must migrate
before DSET claims end-to-end enforcement. Existing emitted atoms remain
immutable. Legacy standalone Opportunity and Conflict Types, Risk-as-Problem,
separate Requirement/Contract authority representations, `EVAL` IDs, and
existing Story/Outcome/Scenario/Invariant records must retain stable IDs,
digests, provenance, and explicit successor or absorption links. They are not
silently retyped or renamed in place.

## Rationale

One flat subtype level keeps every public name independently understandable.
It avoids classifications such as Decision/Requirement/User Story whose meaning
depends on knowing a hidden hierarchy, while retaining precise direct names for
the entities operators already use.

## Lifecycle policy at emission

- **Expected confirmation evidence:** fixtures classify every empty subtype and
  direct subtype without nesting, preserve sibling relations, and keep
  Test/Evaluation distinct
- **Known counter-evidence:** current schemas, validators, IDs, and existing
  atoms still encode the earlier multi-Type model
- **Reopen when:** an ordinary semantic atom requires more than one Type or one
  direct subtype to be classified without information loss
- **If reopened, retain:** operator authority, flat understandable names,
  workflow-independent classification, immutability, and Test/Evaluation
  separation
- **Retirement condition:** a validated successor absorbs every active claim
  and no current projection or implementation relies on this Decision

This emitted Decision atom is immutable. Any later correction, status change,
counter-evidence, absorption, or retirement must be a new atom or append-only
lifecycle event.
