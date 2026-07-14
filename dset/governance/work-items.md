# Work-item routing rules

DSET exposes only three operator-facing queues:

| Queue | Meaning | Required fields |
|---|---|---|
| `problems` | Something is wrong or may harm the project: bug, gap, debt, or risk | Subtype/concern, evidence, state, and owning change when accepted |
| `opportunities` | Nothing is wrong, but a bounded improvement may create value | Expected value, evidence, state, and owning change when accepted |
| `questions` | An unresolved choice or uncertainty | Decision needed, context, options/evidence, and Decision link when resolved |

Debt is a problem subtype, not a synonym for a question. Use concern labels such
as product, implementation, supportability, documentation, test, or eval.
Consequential questions close through a Decision. Decision is both the entity
and durable artifact type. Accepted problems, opportunities, and Decisions
enter a DSET Change. Their executable steps are tasks inside that change's
`tasks.md`, not a fourth top-level queue.

A Requirement owns a verifiable observable WHAT, outcome, or constraint;
observable edge cases belong in Requirements and Scenarios. A Decision owns a
consequential choice among valid alternatives plus rationale, trade-offs, and
consequences. It may constrain HOW, but it is not a ledger for every internal
detail or edge case. Internal details belong in Design, build order belongs in
the implementation plan, and an externally authoritative boundary remains a
Contract rather than a Decision.

A Story records who wants what and why: a meaningful actor or stakeholder, the
desired capability or outcome, its value or purpose, and links to owning
Requirements and Scenarios. Stories are optional, traceable entities; they are
not a fourth intake queue and never substitute for a Requirement.

An Outcome records a measurable change in user, business, operational, or
system state, never merely an output, deliverable, or feature. Each Outcome
states a baseline, target, observation method and source, evaluation window,
and links to motivating Problems or Opportunities, relevant Stories, and the
Evals that determine attainment.

`dset/intake.yaml` is the one project-owned intake registry. `project.key` in
`dset/dset.yaml` owns the stable project prefix. The registry owns the stable
`META`, `GOV`, `TOOL`, `SKILL`, and `OPS` layer segments. Numeric trace IDs use
`<PROJECT>-<FULL-TYPE>-<NNN>` or
`<PROJECT>-<FULL-TYPE>-<LAYER>-<NNN>`. The full work-item types are `PROBLEM`,
`OPPORTUNITY`, and `QUESTION`; `GLOBAL` is never an ID segment. Numbering is
independent per full type within the project-wide sequence or semantic layer,
and a layer segment never changes merely because directories move.

Decision and DSET Change are durable artifacts, not additional queues. Decision
IDs use `<PROJECT>-DECISION-<NNN>` or
`<PROJECT>-DECISION-<LAYER>-<NNN>`. GitHub
Issues and Jira/support tickets are external tracker representations of a problem,
opportunity, question, or task, not additional semantic types.
Discovery or triage does not authorize the solution.
