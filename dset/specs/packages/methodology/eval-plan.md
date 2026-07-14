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
12. A mixed Python/TypeScript repository with methodology, architecture, runbooks, Decisions, and generated evidence.
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
24. A mixed backlog containing defects, debt, unresolved choices, executable work, Decisions, Changes, GitHub Issues, and Jira tickets.
25. Ambiguous and incompatible authoritative boundaries covering a host-native skill format, platform claim, dependency mandate, and hosted-CI claim.
26. Mixed statements that could be User Stories, Requirements, Scenarios, Decisions, Design, implementation-plan steps, or Contracts, plus a package with no meaningful User Story.
27. Mixed feature/output and measurable-state-change claims with complete, missing, weak, or mismatched baselines, targets, observation sources, and evaluation windows.

## Criteria and thresholds

| Eval ID | Criterion | Threshold |
|---|---|---|
| **DSET-EVAL-META-001** | Stage routing | Independent reviewers select the same owning stage/document for all eight scenarios |
| **DSET-EVAL-META-002** | Test/eval separation | No reviewer classifies deterministic correctness as an eval merely because it is automated |
| **DSET-EVAL-META-003** | Runtime applicability | Reviewers select only the recovery, effect-safety, and durability mechanisms triggered by each scenario |
| **DSET-EVAL-META-004** | Implementation readiness | No scenario leaves a critical ownership, proof, or recovery decision implicit |
| **DSET-EVAL-GOV-001** | Public usability | A new reader can locate current truth, active changes, archive history, templates, schemas, and the governing methodology document without Obsidian or private context |
| **DSET-EVAL-OPS-001** | Diagnostic usefulness | For both supportability scenarios, an independent operator can use only synthetic redacted evidence and the runbook to diagnose the likely failure boundary, choose a safe containment/escalation/rollback action, and locate the governing requirement, change, PR, and fix record |
| **DSET-EVAL-GOV-002** | File-only resumability | A fresh evaluator locates active status, next task, proof obligations, PR identity, and archive gates without session context |
| **DSET-EVAL-TOOL-001** | CLI diagnostic usefulness | A contributor can correct a malformed fixture from the stable code, path, and message without reading validator source |
| **DSET-EVAL-SKILL-001** | Skill routing | Ambiguous-domain, defect-investigation, and disposable-experiment prompts select the intended distinct skill and respect its stop condition |
| **DSET-EVAL-GOV-003** | Migration clarity | A repository with separate existing spec/test/eval/implementation roots reaches one writable `dset/` root without losing test/eval separation or current-truth ownership |
| **DSET-EVAL-GOV-004** | Helicopter navigation | A cold reader reaches the owner for methodology, artifact rules, project truth, and agent workflows from the root and area hubs without a filesystem scan |
| **DSET-EVAL-GOV-005** | Artifact ownership | Reviewers assign each sample document one primary type and owning question without creating duplicate normative authority |
| **DSET-EVAL-GOV-006** | Specification semantics | Reviewers identify what/why mixing, incomplete entity lifecycles, and definition-before-use violations while treating forward references only as connections |
| **DSET-EVAL-META-005** | Profile independence | Reviewers configure documentation-only, Python-plus-documentation, and future TypeScript-plus-documentation cases without treating documentation as a programming language |
| **DSET-EVAL-SKILL-002** | Local-rule following | For both adopters, every independent run follows the registered local rule, reports its rule ID/path and ruleset identity, and never substitutes the source framework template while the wrapper hash remains unchanged |
| **DSET-EVAL-GOV-007** | Governance navigation | Every reviewer reaches the registry and single local governing owner and identifies custom/source provenance without treating a wrapper, template, generated installation, index, summary, or cache as normative |
| **DSET-EVAL-GOV-008** | Governance diagnostic usefulness | For every invalid-ownership case, reviewers identify the blocking defect and a safe local correction without reading resolver source or inventing a fallback rule |
| **DSET-EVAL-GOV-009** | Fail-closed wrapper restraint | Every independent run stops before governed work when ownership cannot resolve, reports the unresolved state, and does not continue from embedded knowledge or remote framework prose |
| **DSET-EVAL-SKILL-003** | Primary orchestration usefulness | Every reviewer selects the same stable mode for each lifecycle/authority-conflict state, respects specialist and authorization stops, and does not invent a helper skill |
| **DSET-EVAL-SKILL-004** | Heuristic restraint | Every reviewer treats local run records as advisory, follows newer authoritative state, and recommends the correct refreshed proof or workflow |
| **DSET-EVAL-OPS-002** | Release classification | Every reviewer selects the specified bootstrap, normal, small, RC, final, or post-1.0 class/target or stops on material ambiguity; none promotes 1.0 arithmetically |
| **DSET-EVAL-OPS-003** | Release restraint | Every reviewer refuses RC/final publication when a required gate is absent, names the owning correction surface, and does not weaken the release threshold |
| **DSET-EVAL-SKILL-005** | Outcome-cost judgment | Every reviewer compares expected completed-task cost and required quality rather than nominal token price alone and reports uncertainty instead of inventing precision |
| **DSET-EVAL-SKILL-006** | Proportional delegation | Every reviewer varies useful fan-out, roles, rounds, and evidence depth proportionally, preserves main model/effort by default, and selects zero subagents when delegation adds no material value |
| **DSET-EVAL-GOV-010** | Intake clarity | Every reviewer classifies intake consistently using only problems, opportunities, and questions, while placing tasks inside Changes, treating Decision as both the entity and durable artifact, and treating hosted tickets as representations |
| **DSET-EVAL-GOV-011** | ID grammar | Reviewers use the `DSET` project prefix and full type, omit the layer for project-wide IDs, include the semantic layer for layer-owned IDs, use full `DECISION`, and never derive identity from directories |
| **DSET-EVAL-META-006** | Contract restraint | Every reviewer preserves the authoritative boundary, routes ambiguity to a Question and demonstrated incompatibility to a Problem, refuses Decision-based overrides, distinguishes a mandated dependency from a Decision while permitting consequential choices among allowed alternatives, identifies the authority required for supersession, and rejects prose-only host/platform/CI assurance as proof |
| **DSET-EVAL-META-007** | User Story and specification boundaries | Every reviewer consistently distinguishes optional actor/value context from normative verifiable behavior, observable edge cases, consequential choices, internal logic, build sequence, and non-choosable boundaries; no reviewer creates a User Story intake queue, substitutes a User Story for a Requirement, labels every implementation detail a Decision, or invents a User Story where no meaningful actor perspective exists |
| **DSET-EVAL-META-008** | Outcome validity | Every reviewer distinguishes a delivered output or feature from a measurable user/business/operational/system state change, rejects Outcome claims with an unusable baseline, target, observation method/source, or evaluation window, and keeps Requirement-delivery evidence separate from evidence of intended effect |

## Calibration and evidence

Use at least two independent reviewers for a baseline. Record disagreements by scenario and criterion; resolve them by correcting the earliest ambiguous artifact rather than averaging scores. Store redacted results in the implementing change's `verification.md` or linked proof evidence.
