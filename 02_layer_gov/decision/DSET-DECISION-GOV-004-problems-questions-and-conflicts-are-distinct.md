# Decision — Problems, Questions, and Conflicts are distinct

- **Decision ID:** `DSET-DECISION-GOV-004`
- **Status:** accepted
- **Decision date:** 2026-07-16
- **Resolves Question:** direct operator clarification of whether an open
  conflict is only a Question or a distinct entity
- **Absorbs:** none
- **Replaces claims:** the conflict-record portion of
  `DSET-DECISION-GOV-003`; its role-aware disposition, priority, authority,
  immutability, and absorption rules remain active
- **Priority:** unknown pending the registered core-v1 scale
- **Selected option:** distinguish observed bad states, missing knowledge, and
  verified incompatible claims as Problem, Question, and Conflict
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Context and scope

DSET already distinguishes Problems from Questions, but its conflict rules use
“conflict” both for genuine incompatible authority and for ordinary drift,
failed proof, or implementation nonconformance. Treating every conflict as a
Question would incorrectly require human choice when deterministic governance
already supplies the disposition. Treating every conflict as a Problem would
lose the competing-claim structure needed for resolution, audit, and health
views.

This Decision defines the semantic entities. It does not yet implement the
conflict registry, lifecycle-event schema, detector, resolver, or dashboard.

## Decision

A **Problem** is an observed current or possible harmful state: a defect, gap,
debt, risk, or nonconformance. It requires evidence and triage but does not
imply competing applicable claims or choose its repair.

A **Question** is missing knowledge, interpretation, or choice. It does not by
itself assert that anything is wrong. Evidence may answer a factual Question;
a consequential choice is resolved by a Decision whose consequences compile
into the relevant evergreen projections.

A **Conflict** is a verified incompatibility between two or more applicable
claims over the same scope, concern, and effective time such that they cannot
all govern as written. It is an immutable transactional entity with ID grammar
`<PROJECT>-CONFLICT-<NNN>` or
`<PROJECT>-CONFLICT-<LAYER>-<NNN>`. It records the exact claim/artifact IDs,
incompatible propositions, roles, applicability, scope, evidence, detected
state, priority, and required resolution class.

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
analysis or a reviewer. If resolution requires investigation, choice, or
executable remediation, the Conflict links a Problem, Question, Decision, or
Change rather than duplicating those entities.

## Resolution and lifecycle

The emitted Conflict atom is immutable and initially open. It is resolved only
by an append-only lifecycle event that links the durable resolving artifacts or
events. Depending on its class, resolution may link a new or absorbing
Requirement, Contract, Decision, precedence rule, exception/boundary change,
recompiled evergreen projection with proof, or external-authority update.

Deterministic role/lifecycle rules may resolve a Conflict without creating a
Question. A Question is required only when knowledge or an authorized choice is
missing. Two mutually unsatisfiable immutable Contracts remain an open blocking
Conflict until an authority changes a boundary or grants an explicit valid
exception; priority may order escalation but cannot pretend either obligation
is satisfied.

## Consequences and discharge

This Decision must compile into:

- GOV domain definitions and an invariant separating the three entities;
- one accepted Requirement with deterministic Test and qualitative Eval maps;
- ID grammar and artifact-type documentation;
- the project-owned work-item/conflict governing rules; and
- the active Change manifest, specification connections, tasks, and
  verification plan.

Implementation remains open until schemas and validators provide immutable
Conflict atoms, append-only lifecycle events, derived state, exact claim links,
resolution artifacts, traceability, and the open-conflict health view.

## Lifecycle policy at emission

- **Expected confirmation evidence:** classification fixtures, false-conflict
  rejection cases, immutable conflict/lifecycle schemas, resolution-link
  validation, and independent reviewer agreement
- **Known counter-evidence:** no conflict registry or lifecycle runtime exists,
  and the current resolver reports conflict coverage as unavailable
- **Reopen when:** the three categories overlap in ordinary cases, deterministic
  dispositions require unnecessary Questions, or a verified incompatible claim
  cannot be represented without losing authority or scope
- **If reopened, retain:** exact competing-claim identity, immutable history,
  and explicit resolving-artifact links
- **Retirement condition:** a validated successor absorbs every active claim
  from this Decision and no current schema, projection, resolver, or health view
  relies on it

This emitted Decision atom is immutable. Any later status change, correction,
counter-evidence, absorption, or retirement must be a new append-only lifecycle
event or successor atom.
