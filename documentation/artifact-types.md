# Semantic Types, subtypes, and artifact roles

## Authority

This document is the public framework definition of DSET semantic Types and
subtypes. The DSET repository applies it through
[`DSET-RULE-WORK-ITEMS`](../dset/scopes/gov/governance/work-items.md), compiled
from [`DSET-DECISION-GOV-008`](../dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/decision-DSET-DECISION-GOV-008.md).

## Type rule

DSET has exactly four core semantic Types:

1. **Decision**
2. **Question**
3. **Problem**
4. **QA**

A Type identifies what an atomic project claim or directive means for DSET
governance and routing. It does not classify every real-world condition, work
occurrence, or file. A subtype adds precision without creating a second
top-level Type. Type is not a “family,” and an empty subtype is represented by
omitting `subtype`; it is never represented by repeating the Type name.

```yaml
# General Decision: valid
type: decision

# Requirement: valid
type: decision
subtype: requirement

# Synthetic self-subtype: invalid
type: decision
subtype: decision
```

Every emitted atom has one primary Type and at most one direct subtype. There
are no sub-subtypes. Type and subtype follow semantic content, never workflow,
queue, skill, host, tool, status, filename, folder, or intended next action.
They are immutable after emission. Changed semantics require a new linked atom,
not an in-place retype.

Classify the smallest independently reviewable primary claim, not its entire
file, ticket, paragraph, or workflow. If a statement contains several
independently enforceable or verifiable claims, split it into linked sibling
atoms. If an irreducible claim still fits several subtypes, use the empty
subtype of its Type and record a Question when the ambiguity matters. Never
guess from location or encode multiple subtypes.

When a subtype exists, its full name is the artifact's external kind and ID
kind. A Requirement therefore carries `type: decision` and
`subtype: requirement` but uses `REQUIREMENT` in its ID. An empty-subtype
Decision uses `DECISION`. Legacy IDs and records remain compatibility history
until a provenance-preserving migration replaces or absorbs them.

## Decision

**Definition:** Immutable directive content that the operator has explicitly
accepted as project authority. It states what must govern the project and
compiles into mutable evergreen specifications, plans, and rules.

The operator's acceptance is an act or append-only lifecycle event that grants
authority to the directive; it is not the directive itself. A Markdown, YAML,
database, or hosted record is only its carrier or representation. The record
may store both atom and acceptance metadata, but their semantics stay distinct.

An external law, customer statement, DDL, API schema, platform rule, or library
policy is source material until the operator supplies or accepts it as project
authority. The source remains linked provenance; the Decision owns the
project's accepted directive.

An empty subtype means a general authoritative instruction or consequential
choice that is not more precisely one of the direct subtypes below.

| Subtype | Canonical definition | Classification test | Must not represent |
|---|---|---|---|
| `requirement` | The residual observable result, behavior, capability, quality, or prevention condition that the project must provide and no more precise Decision subtype owns | Can satisfaction be judged from the required result, and do none of the more specific subtype recognition rules own the claim? | A preferred implementation, boundary obligation, story, outcome target, scenario, or invariant |
| `constraint` | A restriction on the acceptable solution space, including required or forbidden technologies, dependencies, environments, resources, formats, or operating limits | Does it remove otherwise valid implementation choices without a boundary participant relying on it as a Contract? | A boundary obligation between named participants |
| `contract` | An obligation at a boundary between the project and an external system or between project components | Are provider, consumer, interface, schema/protocol, compatibility, or failure obligations identifiable? | An internal preference that no boundary participant relies on |
| `user_story` | An actor's or stakeholder's desired capability or outcome and its value | Does it clearly state who wants what and why? | Acceptance criteria or a Requirement nested beneath the story; link sibling atoms instead |
| `outcome` | An intended measurable change in user, business, operational, or system state | Are baseline, target, observation method, and evaluation window identifiable where applicable? | An observed result, which is evidence, or an output with no state change |
| `scenario` | A concrete accepted behavioral example with preconditions, interaction or event, and expected observable result | Does it define one behavior instance that can guide implementation or QA? | An executed run, which is work and evidence |
| `invariant` | A condition that must always hold in every state within a declared scope | Would any violation make the governed state invalid? | Evidence that the condition currently holds |

Choose the subtype whose defining acceptance condition owns the claim:
Contract before Constraint when a boundary participant relies on it; User
Story for actor/want/value framing; Outcome for intended measurable change;
Scenario for one accepted example; Invariant for an always-hold condition; and
Requirement for a remaining observable obligation. Requirements own **what**
the project must provide. Constraints narrow the
allowed solution space. Contracts define what must hold across a boundary.
User Stories, Outcomes, Scenarios, and Invariants express other direct forms of
accepted authority. They may link each other, but none is nested under another
subtype. A general Decision owns other accepted choices, including material
governance, logic, design, implementation, and edge-case resolutions.

## Question

**Definition:** An immutable record of missing knowledge, interpretation, or
choice. A Question does not authorize implementation merely by existing.

An empty subtype means a general uncertainty that is not more precisely a
Conflict, Risk, or Opportunity. Evidence may answer a factual Question; an
authoritative choice is resolved through a Decision. Resolution is an
append-only lifecycle event linked to the immutable Question atom.

| Subtype | Canonical definition | Classification test | Must not represent |
|---|---|---|---|
| `conflict` | Verified incompatible active and applicable authority claims over the same scope, concern, and effective time | Can the exact governing claims be identified, and is it impossible to satisfy all of them as written? | Runtime failure, stale compilation, wording differences, or contradictory evidence alone |
| `risk` | An uncertain future harmful condition | Is the harm not currently true, with likelihood, impact, trigger, or mitigation relevant to handling it? | An observed current insufficiency |
| `opportunity` | A possible beneficial improvement when no current obligation is unmet | Could value be created without correcting a violation or missing requirement? | Required work or a current gap |

A Conflict is a spec-level unresolved Question, not a runtime issue and not a
separate Type. Risk is future uncertainty; once the harmful condition is true,
record a Problem. Opportunity remains optional until the operator accepts a
Requirement or another Decision that makes it authoritative.

## Problem

**Definition:** An immutable record of a presently true, evidence-backed
insufficiency. A Problem states what is wrong or insufficient; it does not
choose or authorize its correction.

An empty subtype means a current insufficiency that is not more precisely a
Defect, Gap, or Debt.

| Subtype | Canonical definition | Classification test | Must not represent |
|---|---|---|---|
| `defect` | Current behavior or implementation contradicts an active Decision or its current evergreen projection | Is something present but behaving incorrectly? | A required capability that does not exist |
| `gap` | A required capability, artifact, proof, or other obligation is currently absent | Is something required missing now? | Optional improvement or uncertain future harm |
| `debt` | A knowingly accepted compromise works sufficiently now but creates continuing or future cost | Does the current solution work while increasing maintenance, supportability, delivery, or correction cost? | Any missing item regardless of cause |

Use this compact test:

- wrong now → **Defect**;
- missing now → **Gap**;
- working through a known costly compromise → **Debt**;
- might cause harm later → **Risk**;
- could create optional value → **Opportunity**.

A Gap may be caused by Debt, and Debt may later produce a Defect. Debt must not
hide an active Defect or Gap: link separate atoms or emit a Decision that
changes the applicable authority. Record one
primary subtype for the condition being governed and link causes or related
atoms rather than duplicating the same condition under multiple subtypes.

## QA

**Definition:** An immutable definition of how an accepted claim must be
checked. QA changes assurance, not authority.

An emitted QA atom must declare a subtype. Empty-subtype QA is invalid because
it does not say whether deterministic or judgment-based proof semantics apply.

| Subtype | Canonical definition | Classification test | Must not represent |
|---|---|---|---|
| `test` | A deterministic check with declared conditions and an exact reproducible pass/fail result | Should the same controlled inputs and environment always produce the same verdict? | Rubric-based or probabilistic judgment disguised as exact proof |
| `evaluation` | A qualitative, probabilistic, statistical, or model-judged assessment with an explicit method, rubric or metric, threshold, and uncertainty treatment where applicable | Does the conclusion require judgment, sampling, calibration, statistics, probability, or an evaluator/model, even if deterministic code executes the method? | An exact deterministic predicate that should be a Test |

A QA atom defines what must be checked. Test code, Evaluation prompts,
datasets, harnesses, and fixtures are implementation artifacts. Execution
results are evidence used by derived Verification. Neither a passing Test nor
Evaluation becomes project authority.

## Classification order

Classify an atomic artifact in this order:

1. Does it state operator-accepted authority? Use **Decision**, then choose one
   direct Decision subtype or no subtype.
2. Does it state missing knowledge, incompatible authority, possible future
   harm, or optional value? Use **Question**, then choose Conflict, Risk,
   Opportunity, or no subtype.
3. Does it state a currently true insufficiency? Use **Problem**, then choose
   Defect, Gap, Debt, or no subtype.
4. Does it define how to check a claim? Use **QA**, then choose Test or
   Evaluation.

If none applies, the artifact is probably a document role, lifecycle record,
implementation artifact, derived view, or optional workflow container rather
than another semantic Type.

## Artifact roles are not Types

The following classifications remain necessary, but they do not expand the
four-Type model:

| Role or layer | Owning question | Typical artifacts |
|---|---|---|
| Navigation | Where does a reader start? | Hub, README, index |
| Evergreen projection | What is the current compiled truth? | Specification, architecture, implementation plan, Test plan, Evaluation plan, runbook, governing rule |
| Rationale | Why does an authority or structure exist? | Rationale section or linked explanation |
| Implementation | What actually realizes the authority and QA definitions? | Code, documentation, configuration, scripts, Test code, Evaluation prompts, datasets, CI |
| Transactional evidence | What was observed at an identified revision, environment, or time? | Proof result, review report, changelog, session/run record |
| Derived view | What does current source data imply? | Verification, project overview, traceability, health dashboard |
| Agent interface | Which governed workflow should be invoked? | Thin skill wrapper |
| Optional delivery container | Which accepted work is grouped for delivery or publication? | Change, Release |

Document roles may contain or project typed atoms. A specification can compile
many Decisions; a Test plan can compile many QA/Test atoms; neither
“specification” nor “plan” becomes a fifth semantic Type.

## Lifecycle and authority

The mandatory base flow is:

```text
Operator input → acceptance act → Decision directive → Evergreen truth
Decision + Implementation + QA definitions → execution → evidence → Verification
```

Problems and Questions form feedback paths. A Problem returns directly to
implementation when an active Decision already defines the correction. If the
correction requires missing knowledge or a new choice, it raises a Question;
the operator's answer becomes a Decision and recompiles evergreen truth.

All emitted Type atoms are immutable. Acceptance, resolution, replacement,
absorption, retirement, and other later state changes use new linked atoms or
append-only lifecycle events. Evergreen projections remain editable and must
be recompiled when active authority changes.

## Rationale

Every Decision representation should prompt for concise rationale. Any other
atomic Type may carry rationale when it helps review, investigation,
prioritization, absorption, or replacement. Rationale remains optional and
cannot hide authority, lifecycle state, or evidence owned elsewhere.
