# Semantic Type and routing rules

**Rule ID:** `DSET-RULE-WORK-ITEMS`

## Canonical Types

DSET has exactly four core semantic Types. Type is determined by meaning, not
workflow, queue, skill, host, tool, status, filename, path, or next action.

| Type | Empty subtype | Allowed subtypes |
|---|---|---|
| `decision` | General operator-accepted authority | `requirement`, `constraint`, `contract`, `user_story`, `outcome`, `scenario`, `invariant` |
| `question` | General missing knowledge, interpretation, or choice | `conflict`, `risk`, `opportunity` |
| `problem` | General current insufficiency | `defect`, `gap`, `debt` |
| `qa` | Invalid for an emitted QA atom | `test`, `evaluation` |

Omit an empty subtype. Never repeat the Type as its own subtype. Every emitted
atom has one Type and at most one direct subtype; QA always has one of its two
subtypes. Subtypes never contain subtypes. Type and subtype are immutable after
emission.

When a subtype exists, its full name is the external artifact and ID kind. A
Requirement uses `type: decision`, `subtype: requirement`, and a `REQUIREMENT`
ID. A general Decision omits subtype and uses a `DECISION` ID.

## Atom boundary

Types classify durable project claims and directives for DSET routing, not
real-world objects, conditions, performed work, or files. Classify the smallest
independently reviewable primary claim. Split statements with several
independently enforceable or verifiable heads into linked sibling atoms. If an
irreducible claim remains plausible under several subtypes, use the empty
subtype of its Type and raise a Question when the ambiguity matters. Never
guess from a carrier, path, workflow, or intended next action.

The operator's acceptance is a lifecycle act that grants authority to a
Decision directive; the act and directive are distinct even when one record
stores both. Markdown, YAML, database, and hosted records are carriers.
Implementation, investigation, acceptance, and QA execution are work. Results
and logs are evidence. Gate dispositions and Verification are derived. None
inherits a Type merely because it is stored beside a typed atom.

## Decision routing

A Decision is immutable directive content explicitly accepted as project
authority by the operator. External material is provenance until the operator
accepts its directive content through an explicit lifecycle act.
Active Decisions compile into evergreen specifications, plans, runbooks, or
governing rules and win when a projection is stale.

- A **Requirement** states the remaining observable result, behavior,
  capability, quality, or prevention condition that no more precise Decision
  subtype owns.
- A **Constraint** restricts acceptable solutions, including required or
  forbidden technologies, dependencies, environments, resources, formats, or
  limits when no boundary participant relies on the restriction as a Contract.
- A **Contract** states an obligation across a project/external or internal
  component boundary, including provider, consumer, interface, schema,
  protocol, compatibility, and failure obligations.
- A **User Story** states which actor or stakeholder wants which capability or
  outcome and why it has value; linked acceptance criteria remain sibling
  atoms.
- An **Outcome** states an intended measurable change in user, business,
  operational, or system state; an observed result is evidence.
- A **Scenario** states a concrete accepted behavioral example through
  preconditions, interaction or event, and expected observable result; an
  executed run is work and evidence.
- An **Invariant** states a condition that must always hold within its declared
  scope; an observation that it currently holds is evidence.
- An empty-subtype **Decision** owns any other accepted authoritative choice.

Requirements own what must result, Constraints narrow the solution space, and
Contracts own boundary obligations. User Stories, Outcomes, Scenarios, and
Invariants are sibling Decision subtypes, not children of Requirement or each
other. They may link but never create a subtype path. A general Decision may
own material governance, logic, design, implementation, or edge-case choices.

## Question routing

A Question records unresolved knowledge, interpretation, or choice and does
not authorize implementation merely by existing.

- A **Conflict** is verified incompatible active and applicable authority over
  the same scope, concern, and effective time. It is spec-level uncertainty,
  not a runtime failure.
- A **Risk** is an uncertain future harmful condition. Record likelihood,
  impact, trigger, and mitigation when useful.
- An **Opportunity** is a possible beneficial improvement when no current
  obligation is unmet.
- An empty-subtype **Question** owns any other uncertainty.

Different wording, stale projections, failed proof, implementation
nonconformance, and contradictory evidence are not automatically Conflicts.
Identify the exact incompatible authority claims before using that subtype.

Evidence may answer a factual Question. A consequential choice resolves
through a Decision. Resolution emits an append-only lifecycle event linking
the answer or Decision; it never edits the Question atom. An accepted
Opportunity becomes authority only through a new Requirement or other
Decision.

## Problem routing

A Problem records a presently true, evidence-backed insufficiency. It does not
choose or authorize its correction.

- A **Defect** is current behavior or implementation that contradicts active
  authority or its current evergreen projection.
- A **Gap** is a required capability, artifact, proof, or obligation that is
  absent now.
- **Debt** is a knowingly accepted compromise that works sufficiently now but
  creates continuing or future cost.
- An empty-subtype **Problem** owns any other current insufficiency.

Use: wrong now → Defect; missing now → Gap; works through a known costly
compromise → Debt; might harm later → Risk; could add optional value →
Opportunity. Select one primary subtype and link causes or related atoms rather
than duplicating a condition.

Debt must not conceal a Defect or Gap. When a compromise also violates active
authority or leaves a required item absent, link separate Defect or Gap atoms
or emit a Decision that changes the applicable authority.

A Problem returns directly to implementation when existing Decisions already
define the correction. If knowledge or a new choice is missing, create a linked
Question first.

## QA routing

QA defines how accepted claims are checked and changes assurance, not
authority.

- A **Test** is deterministic under declared conditions and has an exact,
  reproducible pass/fail result.
- An **Evaluation** uses qualitative, probabilistic, statistical, or
  model-judged assessment with an explicit method, rubric or metric, threshold,
  and uncertainty treatment where applicable. It remains an Evaluation when
  deterministic code executes the method but the conclusion depends on
  judgment, sampling, calibration, probability, statistics, or a model.

QA atoms define checks. Test code, Evaluation prompts, datasets, fixtures, and
harnesses are implementation artifacts. Execution results are evidence for
derived Verification and never rewrite Decisions.

## Lifecycle and authority

All emitted Decision, Question, Problem, and QA atoms are immutable. Editable
drafts are not atoms. Later acceptance, answer, correction, replacement,
absorption, or retirement is a new linked atom or append-only lifecycle event.

Problems and Questions route work but do not authorize implementation. Active
Decisions own authority. QA owns assurance definitions. Evergreen specs and
plans are mutable compiled projections; implementation realizes them;
Verification and project-health views are derived.

Commits changing evergreen truth or implementation cite their governing
Decision or Decisions. A correction under existing authority may additionally
link its Problem. A workflow, GitHub Issue, Jira/support ticket, task, Change,
or Release is a route, representation, step, or optional container rather than
another semantic Type.

## Representation migration

Existing emitted atoms remain immutable. Legacy top-level Opportunity and
Conflict records, Problem/Risk classifications, separate Requirement/Contract
authority records, and `EVAL` identities must not be silently retyped or
renamed. A successor schema must preserve their IDs, content digests,
provenance, and explicit successor or absorption relations.

Until that migration is implemented, the accepted Type model governs and the
older schema/validator projection is stale. Workflows must report the mismatch
rather than claiming end-to-end Type/subtype enforcement.
