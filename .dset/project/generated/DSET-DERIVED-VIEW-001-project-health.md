+++
artifact_type = "derived_view"
artifact_subtype = "health_dashboard"
artifact_id = "DSET-DERIVED-VIEW-001"
priority = "low"
llm_session_ids = []
+++

# DSET project health

> [!NOTE]
> This generated view is not authority. Follow each link to its canonical
> owner and refresh explicitly after source changes.

- **Source digest:** `c9b092ef9c11ede6a42322e6a86c13ec36296368bc28b6c7df94a251c734c8bc`
- **Renderer:** `dset health` schema 1.0

## Coverage

| Closure | Numerator | Denominator | Excluded | N/A | Unknown | Stale |
|---|---:|---:|---:|---:|---:|---:|
| Decision authority compiled into evergreen truth | 29 | 29 | 0 | 0 | 0 | 0 |
| Decision authority linked from implementation commits | 20 | 25 | 4 | 0 | 5 | 0 |
| Applicable authority connected to Test or Evaluation | 17 | 29 | 0 | 0 | 12 | 0 |
| QA definitions connected to current evidence | 12 | 26 | 0 | 0 | 14 | 0 |

### Coverage gaps

- **Decision authority compiled into evergreen truth:** none
- **Decision authority linked from implementation commits:** `DSET-DECISION-OPS-009`, `DSET-DECISION-OPS-011`, `DSET-DECISION-SKILL-003`, `DSET-INVARIANT-GOV-027`, `DSET-REQUIREMENT-GOV-040`
- **Applicable authority connected to Test or Evaluation:** `DSET-DECISION-GOV-001`, `DSET-DECISION-GOV-002`, `DSET-DECISION-GOV-008`, `DSET-DECISION-GOV-010`, `DSET-DECISION-GOV-014`, `DSET-DECISION-GOV-015`, `DSET-DECISION-SKILL-001`, `DSET-INVARIANT-GOV-027`, `DSET-REQUIREMENT-GOV-031`, `DSET-REQUIREMENT-GOV-032`, `DSET-REQUIREMENT-TOOL-021`, `DSET-REQUIREMENT-TOOL-022`
- **QA definitions connected to current evidence:** `DSET-EVALUATION-GOV-026`, `DSET-EVALUATION-GOV-028`, `DSET-EVALUATION-GOV-029`, `DSET-EVALUATION-GOV-031`, `DSET-EVALUATION-SKILL-012`, `DSET-EVALUATION-TOOL-003`, `DSET-EVALUATION-TOOL-004`, `DSET-TEST-GOV-045`, `DSET-TEST-OPS-018`, `DSET-TEST-OPS-019`, `DSET-TEST-OPS-020`, `DSET-TEST-SKILL-014`, `DSET-TEST-TOOL-021`, `DSET-TEST-TOOL-022`

## Artifact inventory

- **Governed artifacts:** 607
- **By role:** atomic=131, derived_or_navigation=75, evergreen=170, implementation=172, transactional=59
- **By type:** analysis_report=23, atomic_record=131, derived_view=1, evidence_record=47, implementation=172, navigation=43, plan=44, procedure=31, specification=86, verification=8, version=21
- **By subtype:** architecture=4, behavior=6, change=9, configuration=79, design=6, domain_model=1, evaluation_plan=14, evaluation_result=6, external_audit_analysis=2, governance=69, health_dashboard=1, hub=43, implementation_plan=10, migration=3, playbook=28, proposal=8, readiness_record=2, release_plan=2, release_record=1, review_report=2, roadmap=2, root_cause_analysis=1, run_record=9, runbook=3, solution_landscape=6, source_code=43, technical_investigation=2, test_implementation=47, test_plan=14, test_result=30, version_scope=5
- **By layer:** gov=149, meta=34, ops=46, repository=137, skill=87, tool=154
- **By effective priority:** critical=44, high=48, medium=509, unknown=6
- **By status:** absorbed=25, accepted=57, open=19, resolved=39

## Semantic inventory

- **Semantic claims:** 332
- **By Type:** decision=125, problem=44, qa=144, question=19
- **By direct subtype:** conflict=1, contract=6, defect=24, evaluation=53, gap=4, invariant=1, opportunity=3, requirement=83, test=91
- **Native immutable atoms:** 106
- **Compatibility-classified legacy IDs:** 226

## Typed relation inventory

- **Forward relations:** 476
- **By type:** analysis_of=1, check_of=38, child_of=56, evidence_for=24, implementation_of=298, projection_of=6, relates_to=19, replacement_of=24, resolution_of=10
- **By origin:** authored=147, commit_trailer=298, legacy_child_of=31
- **By source kind:** artifact=178, commit=298

## Unresolved work

- [`DSET-PROBLEM-TOOL-001`](../intake.toml) — problem: Released validator cannot parse schema 1.2
- [`DSET-QUESTION-GOV-001`](../intake.toml) — question: Should Action become a first-class entity?
- [`DSET-QUESTION-META-001`](../intake.toml) — question: Should DSET standardize Journey?
- [`DSET-QUESTION-META-002`](../intake.toml) — question: Should DSET standardize Actor and Persona?
- [`DSET-QUESTION-META-003`](../intake.toml) — question: Should DSET standardize Hypothesis and Experiment?
- [`DSET-QUESTION-OPS-001`](../intake.toml) — question: Should DSET standardize feedback and analytics evidence?
- [`DSET-QUESTION-GOV-003`](../intake.toml) — question: Should DSET generate roadmap and release views?
- [`DSET-PROBLEM-SKILL-001`](../intake.toml) — problem: Core skill runtime is incomplete
- [`DSET-PROBLEM-OPS-001`](../intake.toml) — problem: Current exact-head hosted proof is missing
- [`DSET-PROBLEM-OPS-002`](../intake.toml) — problem: Release-planning enforcement is not implemented
- [`DSET-QUESTION-META-004`](../intake.toml) — question: Should evidence context be separate from Work Area?
- [`DSET-QUESTION-META-005`](../intake.toml) — question: Should Work Areas expose optional descriptive tags?
- [`DSET-QUESTION-GOV-005`](../intake.toml) — question: Should Decision lifecycle be schema-enforced?
- [`DSET-QUESTION-GOV-006`](../intake.toml) — question: Should proof dependency closures become machine-readable?
- [`DSET-OPPORTUNITY-GOV-001`](../intake.toml) — question/opportunity: Generate a proof-currentness review view
- [`DSET-OPPORTUNITY-TOOL-001`](../intake.toml) — question/opportunity: Expand schema template validation into a compatibility matrix
- [`DSET-OPPORTUNITY-OPS-001`](../intake.toml) — question/opportunity: Generate a cross-repository adoption status view
- [`DSET-QUESTION-TOOL-001`](../intake.toml) — question: When should project health gain an interactive renderer?
- [`DSET-QUESTION-GOV-007`](../intake.toml) — question: How strictly should external review reports be schema-enforced?

## Open Conflicts

- None

## Conflict outcomes

- `DSET-CONFLICT-GOV-001` resolved by `DSET-LIFECYCLE-EVENT-061`; related: `DSET-DECISION-GOV-018`

## Drill-downs

- **Packages:** methodology=0
- **Work Areas:** delivery=5, documentation=8, methodology=10, project-control=456, skills=36, tests=46, toolchain=44

## Canonical return paths

- [manifest](../../dset_settings.toml)
- [governance](../governance.toml)
- [intake](../intake.toml)
- [traceability](traceability.toml)

## Boundaries

Counts are descriptive, not targets. Missing links remain gaps; the
renderer never creates Decisions, implementation, Tests, Evaluations, or
evidence to improve a ratio. `unknown`, `not applicable`, exclusions, and
staleness remain separate dispositions.
