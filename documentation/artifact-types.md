# Artifact types and ownership

## Rule

Every governed artifact has one primary type and one owning question. Split a file when it must answer two independently maintained questions.

| Type | Owning question | Required content | Must not own |
|---|---|---|---|
| Hub/README | Where do readers start and which stable areas or owners exist? | Purpose, boundaries, start routes, short descriptions | Atomic rules, exhaustive leaf inventory, long rationale |
| Normative reference/methodology | What reusable rule or convention applies, and when? | Rule, scope, applicability, invariants, examples needed to apply it | Historical narrative, repeated procedure, extensive design rationale |
| Behavioral specification | What observable behavior, entities, states, constraints, and non-goals are accepted? | Domain vocabulary, requirements, scenarios, lifecycle state machines, authority boundaries | Implementation sequence, tool preference, unaccepted rationale |
| Architecture | How are stable components/artifacts arranged, owned, and constrained? | Goals, boundaries, components, dependencies, authority, constraints, decision links | Product requirements, step-by-step operations, decision history copies |
| Rationale | Why does an active rule or structure exist? | Forces, trade-offs, rejected shapes, consequences, link to normative owner | New normative requirements or procedures hidden in explanatory prose |
| ADR | Which material decision was accepted in a specific context? | Context, decision, alternatives, consequences, status, implementation links | Accepted behavioral truth or an implementation file ledger |
| Playbook/runbook | How is a repeatable change or operational response performed? | Trigger, preconditions, ordered steps, checks, failure/rollback path, stop conditions | General rationale, duplicated normative rules, historical audit output |
| Test plan | Which deterministic claims must be proven exactly? | Test IDs, requirement mapping, seams, cases, commands, pass criteria | Probabilistic rubrics or implementation results |
| Eval plan | Which variable or qualitative behavior must be judged? | Dataset/cases, rubric, thresholds, calibration, budgets, drift policy | Deterministic checks relabeled as evals |
| Evidence/changelog | What was observed or changed at an identified revision/time? | Subject identity, bounded result, source/evidence pointers, disposition | Current rules, mutable runtime authority, secrets or unnecessary raw logs |
| Skill | Which registered repository-governed workflow should run for a specific trigger? | Trigger, root/manifest/registry discovery, workflow ID, resolver invocation, resolved-rule reporting, authorization handoff, and fail-closed behavior | Substantive workflow steps, architecture or authoring rules, proof thresholds, supportability rules, fallback methodology, or broad permanent project truth |

## Classification order

Ask these questions in order:

1. Is the file a navigation front door? Use a hub.
2. Is it current reusable truth or accepted behavior? Use a normative reference or specification.
3. Is it stable structural design? Use architecture and link material decisions.
4. Is it explaining why? Use rationale or an ADR when a specific decision is being recorded.
5. Is it telling an operator or contributor how to act? Use a playbook/runbook.
6. Is it defining proof before implementation? Use a test or eval plan.
7. Is it recording an observation or past change? Use evidence/changelog.
8. Is it a reusable agent invocation? Use a thin skill that resolves the repository-governed procedure and writes conclusions back to the owning project artifacts.

Examples may appear in normative artifacts when needed to apply a rule. They remain illustrative and cannot introduce a second rule that exists nowhere in the normative text.
