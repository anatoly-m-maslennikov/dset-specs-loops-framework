# Semantic Types, subtypes, and artifact types

## Authority

This document is the public framework definition of DSET semantic Types and
subtypes. The DSET repository applies it through
`specification-work-items.md`, compiled from the active Requirement and
Decision authority set.

## Type rule

DSET has exactly five core semantic Types:

1. **Requirement**
2. **Decision**
3. **Question**
4. **Problem**
5. **QA**

A Type identifies what an atomic project claim or directive means for DSET
governance and routing. It does not classify every real-world condition, work
occurrence, or file. A subtype adds precision without creating a second
top-level Type. Type is not a “family,” and an empty subtype is represented by
omitting `subtype`; it is never represented by repeating the Type name.

```yaml
# General Requirement: valid
type: requirement

# Contract: valid
type: requirement
subtype: contract

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
kind. A Requirement carries `type: requirement` with no subtype and uses
`REQUIREMENT` in its ID. A Contract carries `type: requirement` and
`subtype: contract`. A Decision carries `type: decision` with no subtype.
Legacy Decision-parent carriers remain immutable compatibility history and
normalize to the current five-Type model without in-place retyping.

## Requirement

**Definition:** An immutable required result or obligation that the operator
has explicitly accepted as project authority. It states what the project must
provide, prevent, or keep true and compiles into mutable evergreen
specifications, plans, and rules.

An empty subtype means a residual observable obligation. Direct subtypes are
`constraint`, `contract`, `user_story`, `outcome`, `scenario`, and `invariant`.
They are siblings: links among them never create a subtype path.

| Requirement subtype | Canonical definition | Classification test | Must not represent |
|---|---|---|---|
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
subtype. A Decision separately owns material selected approaches.

## Decision

**Definition:** An immutable material selected implementation, architecture,
governance, or operating approach that the operator has explicitly accepted as
project authority.

The operator's acceptance is an act or append-only lifecycle event that grants
authority to the selected approach; it is not the approach itself. A Markdown,
TOML, database, or hosted record is only its carrier or representation. The
record may store both atom and acceptance metadata, but their semantics stay
distinct.

An external law, customer statement, DDL, API schema, platform rule, or library
policy is source material until the operator accepts a corresponding project
Requirement. The source remains linked provenance.

Decision has no subtype. Routine code detail remains implementation rather than
a Decision; record a Decision only when a selected approach must remain durable
authority or its rationale matters to future work.

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

1. Does it state a required result or obligation? Use **Requirement**, then
   choose one direct Requirement subtype or no subtype.
2. Does it state a material selected approach? Use **Decision** with no subtype.
3. Does it state missing knowledge, incompatible authority, possible future
   harm, or optional value? Use **Question**, then choose Conflict, Risk,
   Opportunity, or no subtype.
4. Does it state a currently true insufficiency? Use **Problem**, then choose
   Defect, Gap, Debt, or no subtype.
5. Does it define how to check a claim? Use **QA**, then choose Test or
   Evaluation.

If none applies, the artifact is probably a document role, lifecycle record,
implementation artifact, derived view, or optional workflow container rather
than another semantic Type.

## Artifact types are a separate axis

`artifact_type` classifies the primary job performed by a carrier.
`artifact_subtype` adds at most one direct specialization. These fields are
independent from the semantic `type` and `subtype` of an Atomic Record.

The machine-readable catalog is
the `artifact_catalog` section of
`dset_settings.toml`.
It defines eleven artifact types:

| Artifact type | Direct artifact subtypes |
|---|---|
| `atomic_record` | None; use semantic Type fields for its atom |
| `analysis_report` | `solution_landscape`, `root_cause_analysis`, `proposal`, `technical_investigation`, `external_audit_analysis` |
| `specification` | `domain_model`, `behavior`, `architecture`, `design`, `governance` |
| `procedure` | `playbook`, `runbook` |
| `plan` | `implementation_plan`, `test_plan`, `evaluation_plan` |
| `version` | `roadmap`, `version_scope`, `change`, `release_plan`, `readiness_record`, `release_record` |
| `implementation` | `source_code`, `documentation`, `configuration`, `migration`, `test_implementation`, `evaluation_implementation` |
| `evidence_record` | `test_result`, `evaluation_result`, `review_report`, `run_record` |
| `verification` | None |
| `derived_view` | `project_overview`, `health_dashboard`, `traceability_index`, `changelog` |
| `navigation` | `readme`, `hub`, `index` |

Omit an optional artifact subtype when none fits precisely. Never repeat the
artifact type as its subtype, nest artifact subtypes, or infer semantic Type
from artifact classification. Every governed artifact has one primary artifact
type, recorded directly or resolved through one unambiguous registered path
rule.

New artifact IDs and filenames use the primary artifact type token by default;
the optional subtype remains metadata. For example, Version Scope may use
`APP-VERSION-001-0-4-core.md`, and Roadmap uses the same `VERSION` sequence.
Projects may opt newly emitted artifacts into
subtype tokens with
`artifacts.subtype_in_names = true` in `.dset/dset_settings.toml`.
This independent optional capability never renames existing stable identities.

An Analysis Report interprets information without authorizing its conclusion.
A Solution Landscape compares live options; Root-Cause Analysis supports a
cause for an observed Problem; Proposal recommends one candidate; Technical
Investigation establishes facts, mechanisms, or feasibility; External Audit
Analysis interprets an external audit while the audit remains evidence. An
accepted conclusion is emitted separately as a Decision, Question, Problem, or
QA atom.

Critical boundaries are: Specification versus intended Plan; reusable
Procedure versus one enactment Plan; Plan versus bounded Version;
Implementation versus observed Evidence Record; Evidence Record versus derived
Verification; Verification versus an explicit Readiness Record gate decision;
and release readiness versus immutable Release Record publication history.
Derived View and Navigation never become authority.

The flat Release lifecycle uses the primary `version` type with direct
subtypes `roadmap`, `version_scope`, `change`, `release_plan`,
`readiness_record`, and `release_record`. All six share one project-wide
`VERSION` identity sequence. Milestones are Roadmap entries. Release Notes and
changelogs are rendered or derived from Release Records.

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
