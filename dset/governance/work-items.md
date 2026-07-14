# Work-item routing rules

DSET exposes only three operator-facing queues:

| Queue | Meaning | Required fields |
|---|---|---|
| `problems` | Something is wrong or may harm the project: bug, gap, debt, or risk | Subtype/concern, evidence, state, and owning change when accepted |
| `opportunities` | Nothing is wrong, but a bounded improvement may create value | Expected value, evidence, state, and owning change when accepted |
| `questions` | An unresolved choice or uncertainty | Decision needed, context, options/evidence, and ADR link when resolved |

Debt is a problem subtype, not a synonym for a question. Use concern labels such
as product, implementation, supportability, documentation, test, or eval.
Consequential questions close through an ADR. Accepted problems, opportunities,
and decisions enter a DSET change. Their executable steps are tasks inside that
change's `tasks.md`, not a fourth top-level queue.

ADR/decision and DSET change are durable artifacts, not additional queues.
GitHub Issues and Jira/support tickets are external tracker representations of
a problem, opportunity, question, or task, not additional semantic types.
Discovery or triage does not authorize the solution.
