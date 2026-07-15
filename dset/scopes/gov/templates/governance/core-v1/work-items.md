# Work-item routing rules

DSET exposes only three operator-facing intake queues:

| Queue | Meaning | Required fields |
|---|---|---|
| `problems` | Something is wrong or may harm the project: bug, gap, debt, or risk | Subtype/concern, evidence, state, and owning change when accepted |
| `opportunities` | Nothing is wrong, but a bounded improvement may create value | Expected value, evidence, state, and owning change when accepted |
| `questions` | An unresolved choice or uncertainty | Decision needed, context, options/evidence, and Decision link when resolved |

Type follows the semantic condition and owning question, never the workflow,
queue, skill, tool, host, filename, or path. Open Conflicts use a separate
governed register/view, not a fourth intake queue. Emit a Conflict only when two
or more identified applicable claims cover the same scope, concern, and
effective time and cannot all govern as written. Record the exact claims and
propositions, roles/applicability, shared scope, evidence, priority, and
resolution class.

Ordinary wording differences, stale projections, failed proof, contradictory
evidence, and implementation nonconformance follow their own dispositions and
are not automatically Conflicts. A workflow may discover or link any artifact
type, but cannot retype an artifact.

Debt is a problem subtype, not a synonym for a question. Use concern labels such
as product, implementation, supportability, documentation, test, or eval.
Keep the Problem form thin and scale it by risk. Every Problem atom needs an ID,
concise statement, evidence or observation, impact, owner, and creation state. Add
reproduction and severity for an observed defect; add likelihood, trigger, and
mitigation for a possible future harm; add deeper analysis only when the
selected risk profile or handoff requires it.

Consequential questions close through a Decision and an append-only lifecycle
event; the Question atom is not edited. Decision is both the entity and durable
artifact type. Accepted problems, opportunities, and Decisions enter a DSET
Change. Their executable steps are tasks inside that change's `tasks.md`, not a
fourth top-level queue.

Resolving a Question is not complete when the Decision file alone is written.
Compile the Decision's normative consequences into evergreen Requirements,
Scenarios, Contracts, Design, proof plans, or operating rules, then emit a
lifecycle event linking the resolved Question, Decision, and projections.

Problems, Opportunities, Questions, and Conflicts are immutable transactional atoms. They
may motivate work but do not become normative authority. Accepted, active,
applicable Requirements, Contracts, and Decisions are atomic authority sources
compiled into evergreen specs, plans, and rules. Implementation may link to a
Problem or Opportunity for context, but it must still cite the Change or
Decision that authorized the behavior it adds.

A Requirement owns a verifiable observable WHAT, delivered result, or constraint;
observable edge cases belong in Requirements and Scenarios. A Decision owns a
consequential choice among valid alternatives plus rationale, trade-offs, and
consequences. It may constrain HOW, but it is not a ledger for every internal
detail or edge case. Internal details belong in Design, build order belongs in
the implementation plan, and an externally authoritative boundary remains a
Contract rather than a Decision.

A User Story records who wants what and why: a meaningful actor or stakeholder, the
desired capability or outcome, its value or purpose, and links to owning
Requirements and Scenarios. User Stories are optional, traceable entities; they are
not a fourth intake queue and never substitute for a Requirement.

An Outcome records a measurable change in user, business, operational, or
system state, never merely an output, deliverable, or feature. Each Outcome
states a baseline, target, observation method and source, evaluation window,
and links to motivating Problems or Opportunities, relevant User Stories, and the
Evals that determine attainment.

Schema 1.2 `dset/scopes/gov/intake.yaml` is the one project-owned append-only
intake-atom registry; lifecycle events and derived current state never mutate
an emitted entry. Legacy schema 1.0/1.1 uses central `dset/intake.yaml`. `project.key` in
the discovered project manifest owns the stable project prefix. The registry owns the stable
`META`, `GOV`, `TOOL`, `SKILL`, and `OPS` layer segments. Numeric trace IDs use
`<PROJECT>-<FULL-TYPE>-<NNN>` or
`<PROJECT>-<FULL-TYPE>-<LAYER>-<NNN>`. The full intake types are `PROBLEM`,
`OPPORTUNITY`, and `QUESTION`; the separate conflict type is `CONFLICT`;
`GLOBAL` is never an ID segment. Numbering is
independent per full type within the project-wide sequence or semantic layer,
and a layer segment never changes merely because directories move.

Decision and DSET Change are durable artifacts, not additional queues. Decision
IDs use `<PROJECT>-DECISION-<NNN>` or
`<PROJECT>-DECISION-<LAYER>-<NNN>`. GitHub
Issues and Jira/support tickets are external tracker representations of a problem,
opportunity, question, conflict, or task, not additional semantic types.
Discovery or triage does not authorize the solution.

A Conflict atom is never edited to record its outcome. Resolution emits an
append-only lifecycle event linking durable resolving artifacts or events,
such as a new or absorbing Requirement, Contract, Decision, explicit
precedence rule, valid exception or boundary change, recompiled projection with
proof, or external-authority update. Create a linked Question only when
knowledge or an authorized choice is actually missing.
