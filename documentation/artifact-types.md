# Artifact types and ownership

## Rule

Every governed artifact has one primary type and one owning question. Type is
determined by semantic content and authority/lifecycle role, never by workflow,
queue, skill, tool, host, filename, folder, or intended next action. A workflow
may create, discover, link, or resolve artifacts, but cannot retype them. Split
a file when it must answer two independently maintained questions.

| Type | Owning question | Required content | Must not own |
|---|---|---|---|
| Hub/README | Where do readers start and which stable areas or owners exist? | Purpose, boundaries, start routes, short descriptions | Atomic rules, exhaustive leaf inventory, long rationale |
| Normative reference/methodology | What reusable rule or convention applies, and when? | Rule, scope, applicability, invariants, examples needed to apply it | Historical narrative, repeated procedure, extensive design rationale |
| Behavioral specification | What observable behavior, entities, states, constraints, and non-goals are accepted? | Domain vocabulary, requirements, scenarios, lifecycle state machines, authority boundaries | Implementation sequence, tool preference, unaccepted rationale |
| Architecture | How are stable components/artifacts arranged, owned, and constrained? | Goals, boundaries, components, dependencies, authority, constraints, decision links | Product requirements, step-by-step operations, decision history copies |
| Rationale | Why does an active rule or structure exist? | Forces, trade-offs, rejected shapes, consequences, link to normative owner | New normative requirements or procedures hidden in explanatory prose |
| Problem | What harmful state, gap, defect, debt, risk, or nonconformance was observed? | Evidence, affected scope, impact, priority, and triage links | Competing-claim resolution or an implied repair |
| Question | What knowledge, interpretation, or authorized choice is missing? | Context, unknown or alternatives, evidence, priority, and resolution link | An assertion that something is wrong or the consequential choice itself |
| Conflict | Which applicable claims are verified incompatible over the same scope, concern, and effective time? | Exact claim IDs/propositions, roles, applicability, shared scope, evidence, priority, resolution class, and lifecycle links | Ordinary wording drift, failed assurance, implementation nonconformance, or an edited-in-place resolution |
| Decision | Which material decision was accepted in a specific context? | Context, decision, alternatives, consequences, status, implementation links, and recommended optional rationale | Accepted behavioral truth or an implementation file ledger |
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
4. Is it an observed harmful state? Use a Problem. Is knowledge or choice
   missing? Use a Question. Are identified applicable claims verified
   incompatible? Use a Conflict.
5. Is it explaining why? Use rationale or a Decision when a specific choice is being recorded.
6. Is it telling an operator or contributor how to act? Use a playbook/runbook.
7. Is it defining proof before implementation? Use a test or eval plan.
8. Is it recording an observation or past change? Use evidence/changelog.
9. Is it a reusable agent invocation? Use a thin skill that resolves the repository-governed procedure and writes conclusions back to the owning project artifacts.

Examples may appear in normative artifacts when needed to apply a rule. They remain illustrative and cannot introduce a second rule that exists nowhere in the normative text.

Every atomic artifact may carry a concise rationale when the explanation helps
review, investigation, absorption, replacement, or conflict resolution.
Decision templates always prompt for it. The field or section is recommended,
not required: missing rationale alone does not invalidate an artifact. A
rationale explains the atom; it cannot silently own normative behavior,
lifecycle state, or evidence assigned to another artifact type.
