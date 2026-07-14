# Methodology qualitative eval plan

## Applicability

Applicable. The methodology is natural-language guidance, so routing clarity, ambiguity, and usability require qualitative evaluation even when structural correctness is deterministic.

## Evaluation set

Use representative project scenarios covering:

1. A one-shot local transform with no durable work.
2. A modest-write resumable local tool using files.
3. A high-write concurrent local tool selecting a database.
4. A stateless CRUD service using an external database.
5. A long-running workflow with retry and human approval.
6. A deterministic parser defect.
7. A variable LLM-output quality regression.
8. A Python project and a JavaScript/TypeScript project selecting enforcement profiles.
9. A production-bound local tool whose incident evidence stays in bounded local files.
10. A distributed retryable service whose operator must trace a synthetic incident across effect boundaries and a deployment.
11. A documentation-only repository selecting artifact governance without code enforcement.
12. A mixed Python/TypeScript repository with methodology, architecture, runbooks, ADRs, and generated evidence.
13. A mature repository whose root contains many files but only four stable governed areas.
14. Two adopters using one unchanged workflow wrapper but deliberately different registered local output rules.
15. A customized adopter in which a cold agent must distinguish the governing document from the wrapper, template, generated installation, summary, and cache.
16. Invalid ownership fixtures that expose only a stable code, path, and actionable message to the evaluator.
17. A wrapper invocation whose selected workflow cannot resolve because rule ownership is missing or profile-incompatible.
18. A cold operator invoking `dset` during initialization, ambiguous design, active implementation, failed verification, and release readiness.
19. Local skill-run history that conflicts with newer authoritative Git/change state.
20. Representative normal, small, RC, and final PRs with mixed code, documentation, migrations, blockers, and proof state.
21. A superficially green candidate that lacks one required pilot or retains a known release blocker.
22. One representative engineering task with candidate models that differ in token price, token use, retries, agent/tool steps, pass rate, and latency.
23. Low, medium, and high budget requests for trivial, parallelizable, high-risk, and evaluator-sensitive work.
24. A mixed backlog containing defects, debt, unresolved choices, executable work, ADRs, changes, GitHub Issues, and Jira tickets.

## Criteria and thresholds

| Eval ID | Criterion | Threshold |
|---|---|---|
| **METH-EVAL-001** | Stage routing | Independent reviewers select the same owning stage/document for all eight scenarios |
| **METH-EVAL-002** | Test/eval separation | No reviewer classifies deterministic correctness as an eval merely because it is automated |
| **METH-EVAL-003** | Runtime applicability | Reviewers select only the recovery, effect-safety, and durability mechanisms triggered by each scenario |
| **METH-EVAL-004** | Implementation readiness | No scenario leaves a critical ownership, proof, or recovery decision implicit |
| **METH-EVAL-005** | Public usability | A new reader can locate current truth, active changes, archive history, templates, schemas, and the governing methodology document without Obsidian or private context |
| **METH-EVAL-006** | Diagnostic usefulness | For both supportability scenarios, an independent operator can use only synthetic redacted evidence and the runbook to diagnose the likely failure boundary, choose a safe containment/escalation/rollback action, and locate the governing requirement, change, PR, and fix record |
| **METH-EVAL-007** | File-only resumability | A fresh evaluator locates active status, next task, proof obligations, PR identity, and archive gates without session context |
| **METH-EVAL-008** | CLI diagnostic usefulness | A contributor can correct a malformed fixture from the stable code, path, and message without reading validator source |
| **METH-EVAL-009** | Skill routing | Ambiguous-domain, defect-investigation, and disposable-experiment prompts select the intended distinct skill and respect its stop condition |
| **METH-EVAL-010** | Migration clarity | A repository with separate existing spec/test/eval/implementation roots reaches one writable `dset/` root without losing test/eval separation or current-truth ownership |
| **METH-EVAL-011** | Helicopter navigation | A cold reader reaches the owner for methodology, artifact rules, project truth, and agent workflows from the root and area hubs without a filesystem scan |
| **METH-EVAL-012** | Artifact ownership | Reviewers assign each sample document one primary type and owning question without creating duplicate normative authority |
| **METH-EVAL-013** | Specification semantics | Reviewers identify what/why mixing, incomplete entity lifecycles, and definition-before-use violations while treating forward references only as connections |
| **METH-EVAL-014** | Profile independence | Reviewers configure documentation-only, Python-plus-documentation, and future TypeScript-plus-documentation cases without treating documentation as a programming language |
| **METH-EVAL-015** | Local-rule following | For both adopters, every independent run follows the registered local rule, reports its rule ID/path and ruleset identity, and never substitutes the source framework template while the wrapper hash remains unchanged |
| **METH-EVAL-016** | Governance navigation | Every reviewer reaches the registry and single local governing owner and identifies custom/source provenance without treating a wrapper, template, generated installation, index, summary, or cache as normative |
| **METH-EVAL-017** | Governance diagnostic usefulness | For every invalid-ownership case, reviewers identify the blocking defect and a safe local correction without reading resolver source or inventing a fallback rule |
| **METH-EVAL-018** | Fail-closed wrapper restraint | Every independent run stops before governed work when ownership cannot resolve, reports the unresolved state, and does not continue from embedded knowledge or remote framework prose |
| **METH-EVAL-019** | Primary orchestration usefulness | Every reviewer selects the same stable mode for each lifecycle/authority-conflict state, respects specialist and authorization stops, and does not invent a helper skill |
| **METH-EVAL-020** | Heuristic restraint | Every reviewer treats local run records as advisory, follows newer authoritative state, and recommends the correct refreshed proof or workflow |
| **METH-EVAL-021** | Release classification | Every reviewer selects the specified bootstrap, normal, small, RC, final, or post-1.0 class/target or stops on material ambiguity; none promotes 1.0 arithmetically |
| **METH-EVAL-022** | Release restraint | Every reviewer refuses RC/final publication when a required gate is absent, names the owning correction surface, and does not weaken the release threshold |
| **METH-EVAL-023** | Outcome-cost judgment | Every reviewer compares expected completed-task cost and required quality rather than nominal token price alone and reports uncertainty instead of inventing precision |
| **METH-EVAL-024** | Proportional delegation | Every reviewer varies useful fan-out, roles, rounds, and evidence depth proportionally, preserves main model/effort by default, and selects zero subagents when delegation adds no material value |
| **METH-EVAL-025** | Intake clarity | Every reviewer classifies intake consistently using only problems, opportunities, and questions, while placing tasks inside changes and treating ADRs/changes as artifacts and hosted tickets as representations |

## Calibration and evidence

Use at least two independent reviewers for a baseline. Record disagreements by scenario and criterion; resolve them by correcting the earliest ambiguous artifact rather than averaging scores. Store redacted results in the implementing change's `verification.md` or linked proof evidence.
