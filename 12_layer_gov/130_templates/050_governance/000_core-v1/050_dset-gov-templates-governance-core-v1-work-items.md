---
artifact_type: specification
scope_path: []
priority: medium
artifact_subtype: governance
---

# Semantic Type and routing rules

**Rule ID:** `DSET-RULE-WORK-ITEMS`

## Canonical Types

DSET has exactly four core semantic Types. Type is determined by meaning, not
workflow, queue, skill, host, tool, status, filename, path, or next action.

| Type | Empty subtype | Allowed subtypes |
|---|---|---|
| `decision` | General accepted directive | `requirement`, `constraint`, `contract`, `implementation_decision` |
| `question` | General missing knowledge, interpretation, or choice | `conflict`, `risk`, `opportunity` |
| `problem` | General current insufficiency | `defect`, `gap`, `debt` |
| `qa` | Invalid for an emitted QA atom | `test_plan`, `evaluation_plan` |

Omit an empty subtype. Never repeat the Type as its own subtype. Every emitted
atom has one Type and at most one direct subtype; QA always has one of its two
subtypes. Subtypes never contain subtypes. Type and subtype are immutable after
emission.

When subtype-bearing names are enabled, a Requirement, Constraint, Contract,
or Implementation Decision uses `REQUIREMENT`, `CONSTRAINT`, `CONTRACT`, or `IMPL` as its
external ID kind. An empty-subtype Decision uses `DECISION`. Type-only naming
uses the Type token while keeping the subtype in atom metadata.

## Canonical identity migration

All current and historical project identities use the same canonical
vocabulary. A naming change is a complete governed migration of IDs, carrier
names, relations, maintained views, settings, code,
proof references, and generated views. Short aliases are rejected after the
migration; they do not remain as a second compatibility vocabulary. One
recognized ID-kind token and the carrier's semantic role must agree on one
Type and at most one direct subtype.

`dset check` fails with `DSET-E166` when an ID kind and carrier classification
disagree or a carrier cannot resolve to the flat model. Traceability publishes
the canonical ID, normalized Type/subtype, carrier identity, relations, and
active/archive state. Project health reports the same population by Type and subtype. Skill
context exposes the four-Type routing identity and
counts from the current repository; wrappers never infer a Type from the skill
that happened to run.

## Atom boundary

Types classify durable project claims and directives for DSET routing, not
real-world objects, conditions, performed work, or files. Classify the smallest
independently reviewable primary claim. Split statements with several
independently enforceable or verifiable heads into linked sibling atoms. If an
irreducible claim remains plausible under several subtypes, use the empty
subtype of its Type and raise a Question when the ambiguity matters. Never
guess from a carrier, path, workflow, or intended next action.

The operator's acceptance is a lifecycle act that grants authority to a
Decision; the act and accepted content are distinct even when
one record stores both. Markdown, TOML, database, and hosted records are
carriers.
Implementation, investigation, acceptance, and QA execution are work. Results
and logs are evidence. Gate dispositions and Verification are derived. None
inherits a Type merely because it is stored beside a typed atom.

## Decision routing

A Decision is an immutable directive explicitly accepted as project authority
by the operator. External material is provenance until the operator accepts its
content through an explicit lifecycle act. Active Decisions are reflected in
maintained specifications, plans, runbooks, or governing rules and win when a
view is stale.

- A **Requirement** states a required observable result, behavior, capability,
  quality, prevention condition, or obligation.
- A **Constraint** records an externally imposed limitation on acceptable
  technologies, dependencies, environments, resources, formats, or operating
  limits when no boundary participant relies on the restriction as a Contract.
- A **Contract** states provider, consumer, interface, schema, protocol,
  compatibility, or failure obligations across a boundary.
- An **Implementation Decision** records a material selected architecture,
  design, algorithm, data, tooling, or operating approach.
- An empty-subtype **Decision** is the fallback for accepted directives that no
  more precise Decision subtype owns.

Routine code-level detail remains implementation rather than an Implementation
Decision. User Story, Outcome, Scenario, and Invariant are useful requirement
forms in prose and compatibility history, but they are not current semantic
subtypes; split their independently enforceable claims into Requirement atoms.

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
through a Decision with `resolution_of`; the resolved Question moves
byte-for-byte to its Type-local `archive/`. An accepted
Opportunity becomes authority only through a new Decision.

## Problem routing

A Problem records a presently true, evidence-backed insufficiency. It does not
choose or authorize its correction.

- A **Defect** is current behavior or implementation that contradicts active
  authority or its current maintained view.
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

A Problem returns directly to implementation when existing Requirements or
Decisions already define the correction. If knowledge or a new choice is
missing, create a linked Question first.

## QA routing

QA defines how accepted claims are checked and changes assurance, not
authority.

- A **Test Plan** defines deterministic proof under declared conditions with an exact,
  reproducible pass/fail result.
- An **Evaluation Plan** defines qualitative, probabilistic, statistical, or
  model-judged assessment with an explicit method, rubric or metric, threshold,
  and uncertainty treatment where applicable. It remains an Evaluation Plan when
  deterministic code executes the method but the conclusion depends on
  judgment, sampling, calibration, probability, statistics, or a model.

QA atoms define Test Plans or Evaluation Plans. Test code, Evaluation prompts,
datasets, fixtures, and harnesses are implementation artifacts. Execution results are evidence for
derived Verification and never rewrite Requirements or Decisions.

## Atom state and authority

All emitted Decision, Question, Problem, and QA atoms are immutable. Editable
drafts are not atoms. Later semantic correction requires a successor atom.
Complete replacement uses `replacement_of`; resolution uses `resolution_of`;
withdrawal archives the atom and routes future intent to a Version Roadmap.
Reopening is forbidden. A repeated Question or Problem is a new atom using
`recurrence_of` to its archived predecessor.

Problems and Questions route work but do not authorize implementation. Active
Decisions own authority. QA owns assurance definitions.
Maintained specs and plans are mutable semantic views; implementation realizes
them;
Verification and project-health views are derived.

Commits changing maintained views or implementation cite their governing
Decision IDs. A correction under existing authority may
additionally link its Problem. A workflow, GitHub Issue, Jira/support ticket,
task, Change,
or Release is a route, representation, step, or optional container rather than
another semantic Type.

## Complete identity migration

Payloads and provenance remain attributable, but a naming-policy change
migrates the complete current and historical identity graph in one governed
transaction. IDs, carrier names, relations, compiled
projections, settings, implementations, proof references, and generated views
must agree before the migration is accepted. Short aliases are rejected after
cutover rather than retained as compatibility identities.

The canonical projection is implemented across validation, traceability,
project health, and skill routing. Every migrated atom resolves through its
original seal plus any validated current-
carrier transition chain. Any immutability claim must distinguish semantic
immutability from carrier representation.
