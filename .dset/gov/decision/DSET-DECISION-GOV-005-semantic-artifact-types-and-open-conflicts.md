# Decision — Semantic artifact types and open Conflicts

- **Decision ID:** `DSET-DECISION-GOV-005`
- **Status:** accepted
- **Decision date:** 2026-07-16
- **Resolves Question:** direct operator clarification of Problem, Question,
  Conflict, and workflow-independent artifact typing
- **Absorbs:** `DSET-DECISION-GOV-004` in full
- **Replaces claims:** all claims of `DSET-DECISION-GOV-004`, carried forward
  below with the added rule that workflow never defines artifact type
- **Priority:** unknown pending the registered core-v1 scale
- **Selected option:** classify artifacts by semantic condition, owning question,
  authority role, and lifecycle; never by workflow, queue, skill, tool, or path
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Context and scope

DSET needs distinct semantics for harmful states, missing knowledge or choice,
and verified incompatible claims. It also routes artifacts through intake,
review, diagnosis, resolution, compilation, and delivery workflows. Those
workflows can create, discover, link, transform, or close work, but they cannot
determine what an artifact is. Otherwise identical content would change type
when a different skill runs or when a file moves between folders.

This Decision governs every DSET artifact type. It defines Conflict semantics
but does not yet implement the conflict registry, lifecycle schema, detector,
resolver, or dashboard.

## Decision

An artifact's primary type is determined only by its semantic condition and
owning question, plus its authority and lifecycle role where needed. Creation
source, current workflow, operator queue, skill name, agent host, tool, storage
location, filename, and intended next action are routing metadata and never
type discriminators. Moving an artifact through a workflow cannot change its
type; changed semantics require a new correctly typed artifact and explicit
links.

A **Problem** is an observed current or possible harmful state: a defect, gap,
debt, risk, or nonconformance. It requires evidence and triage but does not
imply competing applicable claims or choose its repair.

A **Question** is missing knowledge, interpretation, or choice. It does not by
itself assert that anything is wrong. Evidence may answer a factual Question;
a consequential choice is resolved by a Decision whose consequences compile
into the relevant evergreen projections.

A **Conflict** is a verified incompatibility between two or more applicable
claims over the same scope, concern, and effective time such that they cannot
all govern as written. It uses `<PROJECT>-CONFLICT-<NNN>` or
`<PROJECT>-CONFLICT-<LAYER>-<NNN>` and records exact claim/artifact IDs,
incompatible propositions, roles, applicability, shared scope, evidence,
detection state, priority, and required resolution class.

These distinctions hold regardless of workflow. Diagnosis may emit a Problem,
Question, or Conflict based on what it finds. Review may emit any of them.
Conflict resolution may create a Question, Decision, Requirement, Contract,
Problem, or Change, but the resolving workflow does not retype either the open
Conflict or its outputs.

Different wording, a stale compiled projection, failing Test or Eval,
implementation nonconformance, and contradictory evidence are not
automatically Conflicts:

- an active source versus its stale projection routes recompilation;
- failing proof changes assurance;
- implementation versus authority creates a Problem;
- contradictory evidence follows its proof plan or creates a Question; and
- only verified incompatible applicable claims emit a Conflict.

Conflict is not a fourth operator-facing intake queue. Open Conflicts have a
dedicated governed register/view because they may be emitted by deterministic
analysis or a reviewer. This placement supports discovery and resolution but
does not define the Conflict type.

## Resolution and lifecycle

Every emitted Problem, Question, and Conflict atom is immutable. A Conflict is
initially open and resolves only through an append-only lifecycle event linking
durable resolving artifacts or events. Depending on class, resolution may link
a new or absorbing Requirement, Contract, Decision, explicit precedence rule,
valid exception or boundary change, recompiled evergreen projection with
proof, or external-authority update.

Deterministic role/lifecycle rules may resolve a Conflict without creating a
Question. Create a Question only when knowledge or authorized choice is
missing. Two mutually unsatisfiable immutable obligations remain an open
blocking Conflict until an authority changes a boundary or grants a valid
exception; priority may order escalation but cannot claim either obligation is
satisfied.

## Consequences and discharge

This Decision must compile into:

- universal artifact architecture and authoring rules;
- GOV domain definitions and an invariant separating the three entities while
  prohibiting workflow-defined types;
- one Requirement with deterministic Test and qualitative Eval mappings;
- ID grammar, work-item/conflict rules, and artifact-type documentation; and
- the active Change manifest, specification connections, tasks, and
  verification plan.

Implementation remains open until schemas and validators provide immutable
Conflict atoms, append-only lifecycle events, derived state, exact claim links,
resolution artifacts, traceability, and the open-conflict health view.

## Lifecycle policy at emission

- **Expected confirmation evidence:** classification fixtures that vary
  workflow while holding semantics constant, false-conflict rejection cases,
  immutable lifecycle schemas, and independent reviewer agreement
- **Known counter-evidence:** no conflict registry/lifecycle runtime exists and
  the current resolver reports conflict coverage as unavailable
- **Reopen when:** semantic classification cannot distinguish ordinary cases or
  a valid workflow must determine type rather than route already typed content
- **If reopened, retain:** exact competing-claim identity, immutable history,
  explicit resolving-artifact links, and separation of routing from semantics
- **Retirement condition:** a validated successor absorbs every active claim
  and no current schema, projection, resolver, or health view relies on this
  Decision

This emitted Decision atom is immutable. Any later status change, correction,
counter-evidence, absorption, or retirement must be a new append-only lifecycle
event or successor atom.
