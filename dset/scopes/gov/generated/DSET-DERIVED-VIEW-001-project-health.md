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

- **Source digest:** `64af964a7700d9caefa8991719a2c043386463ab8ae7b04ef7abadc8d75b3082`
- **Renderer:** `dset health` schema 1.0

## Coverage

| Closure | Numerator | Denominator | Excluded | N/A | Unknown | Stale |
|---|---:|---:|---:|---:|---:|---:|
| Decision authority compiled into evergreen truth | 92 | 92 | 0 | 0 | 0 | 0 |
| Decision authority linked from implementation commits | 17 | 17 | 75 | 0 | 0 | 0 |
| Applicable authority connected to Test or Evaluation | 9 | 92 | 0 | 0 | 83 | 0 |
| QA definitions connected to current evidence | 2 | 130 | 0 | 0 | 128 | 0 |

### Coverage gaps

- **Decision authority compiled into evergreen truth:** none
- **Decision authority linked from implementation commits:** none
- **Applicable authority connected to Test or Evaluation:** `DSET-CONTRACT-META-001`, `DSET-CONTRACT-OPS-001`, `DSET-CONTRACT-SKILL-001`, `DSET-CONTRACT-SKILL-002`, `DSET-CONTRACT-TOOL-001`, `DSET-CONTRACT-TOOL-002`, `DSET-DECISION-GOV-001`, `DSET-DECISION-GOV-002`, `DSET-DECISION-GOV-003`, `DSET-DECISION-GOV-008`, `DSET-DECISION-GOV-010`, `DSET-DECISION-GOV-012`, `DSET-DECISION-GOV-014`, `DSET-DECISION-GOV-015`, `DSET-DECISION-OPS-006`, `DSET-DECISION-SKILL-001`, `DSET-DECISION-SKILL-002`, `DSET-REQUIREMENT-GOV-001`, `DSET-REQUIREMENT-GOV-002`, `DSET-REQUIREMENT-GOV-003`, `DSET-REQUIREMENT-GOV-004`, `DSET-REQUIREMENT-GOV-005`, `DSET-REQUIREMENT-GOV-006`, `DSET-REQUIREMENT-GOV-007`, `DSET-REQUIREMENT-GOV-008`, `DSET-REQUIREMENT-GOV-009`, `DSET-REQUIREMENT-GOV-010`, `DSET-REQUIREMENT-GOV-011`, `DSET-REQUIREMENT-GOV-012`, `DSET-REQUIREMENT-GOV-013`, `DSET-REQUIREMENT-GOV-014`, `DSET-REQUIREMENT-GOV-015`, `DSET-REQUIREMENT-GOV-016`, `DSET-REQUIREMENT-GOV-017`, `DSET-REQUIREMENT-GOV-018`, `DSET-REQUIREMENT-GOV-019`, `DSET-REQUIREMENT-GOV-020`, `DSET-REQUIREMENT-GOV-021`, `DSET-REQUIREMENT-GOV-022`, `DSET-REQUIREMENT-GOV-023`, `DSET-REQUIREMENT-GOV-024`, `DSET-REQUIREMENT-GOV-025`, `DSET-REQUIREMENT-GOV-026`, `DSET-REQUIREMENT-GOV-027`, `DSET-REQUIREMENT-GOV-028`, `DSET-REQUIREMENT-GOV-029`, `DSET-REQUIREMENT-GOV-031`, `DSET-REQUIREMENT-GOV-032`, `DSET-REQUIREMENT-META-001`, `DSET-REQUIREMENT-META-002`, `DSET-REQUIREMENT-META-003`, `DSET-REQUIREMENT-META-004`, `DSET-REQUIREMENT-META-005`, `DSET-REQUIREMENT-META-006`, `DSET-REQUIREMENT-META-007`, `DSET-REQUIREMENT-META-008`, `DSET-REQUIREMENT-META-009`, `DSET-REQUIREMENT-META-010`, `DSET-REQUIREMENT-META-011`, `DSET-REQUIREMENT-OPS-001`, `DSET-REQUIREMENT-OPS-002`, `DSET-REQUIREMENT-OPS-003`, `DSET-REQUIREMENT-OPS-004`, `DSET-REQUIREMENT-OPS-005`, `DSET-REQUIREMENT-OPS-006`, `DSET-REQUIREMENT-OPS-007`, `DSET-REQUIREMENT-OPS-013`, `DSET-REQUIREMENT-SKILL-001`, `DSET-REQUIREMENT-SKILL-002`, `DSET-REQUIREMENT-SKILL-003`, `DSET-REQUIREMENT-SKILL-004`, `DSET-REQUIREMENT-SKILL-005`, `DSET-REQUIREMENT-SKILL-006`, `DSET-REQUIREMENT-SKILL-007`, `DSET-REQUIREMENT-SKILL-008`, `DSET-REQUIREMENT-TOOL-001`, `DSET-REQUIREMENT-TOOL-002`, `DSET-REQUIREMENT-TOOL-003`, `DSET-REQUIREMENT-TOOL-004`, `DSET-REQUIREMENT-TOOL-018`, `DSET-REQUIREMENT-TOOL-019`, `DSET-REQUIREMENT-TOOL-021`, `DSET-REQUIREMENT-TOOL-022`
- **QA definitions connected to current evidence:** `DSET-EVAL-GOV-001`, `DSET-EVAL-GOV-002`, `DSET-EVAL-GOV-003`, `DSET-EVAL-GOV-004`, `DSET-EVAL-GOV-005`, `DSET-EVAL-GOV-006`, `DSET-EVAL-GOV-007`, `DSET-EVAL-GOV-008`, `DSET-EVAL-GOV-009`, `DSET-EVAL-GOV-010`, `DSET-EVAL-GOV-011`, `DSET-EVAL-GOV-012`, `DSET-EVAL-GOV-013`, `DSET-EVAL-GOV-014`, `DSET-EVAL-GOV-015`, `DSET-EVAL-GOV-016`, `DSET-EVAL-GOV-017`, `DSET-EVAL-GOV-018`, `DSET-EVAL-GOV-019`, `DSET-EVAL-GOV-020`, `DSET-EVAL-GOV-021`, `DSET-EVAL-GOV-022`, `DSET-EVAL-GOV-023`, `DSET-EVAL-META-001`, `DSET-EVAL-META-002`, `DSET-EVAL-META-003`, `DSET-EVAL-META-004`, `DSET-EVAL-META-005`, `DSET-EVAL-META-006`, `DSET-EVAL-META-007`, `DSET-EVAL-META-008`, `DSET-EVAL-META-009`, `DSET-EVAL-OPS-001`, `DSET-EVAL-OPS-002`, `DSET-EVAL-OPS-003`, `DSET-EVAL-OPS-010`, `DSET-EVAL-SKILL-001`, `DSET-EVAL-SKILL-002`, `DSET-EVAL-SKILL-003`, `DSET-EVAL-SKILL-004`, `DSET-EVAL-SKILL-005`, `DSET-EVAL-SKILL-006`, `DSET-EVAL-SKILL-007`, `DSET-EVAL-SKILL-008`, `DSET-EVAL-TOOL-001`, `DSET-EVALUATION-GOV-026`, `DSET-EVALUATION-GOV-028`, `DSET-EVALUATION-SKILL-012`, `DSET-EVALUATION-TOOL-003`, `DSET-EVALUATION-TOOL-004`, `DSET-TEST-GOV-001`, `DSET-TEST-GOV-002`, `DSET-TEST-GOV-003`, `DSET-TEST-GOV-004`, `DSET-TEST-GOV-005`, `DSET-TEST-GOV-006`, `DSET-TEST-GOV-007`, `DSET-TEST-GOV-008`, `DSET-TEST-GOV-009`, `DSET-TEST-GOV-010`, `DSET-TEST-GOV-011`, `DSET-TEST-GOV-012`, `DSET-TEST-GOV-013`, `DSET-TEST-GOV-014`, `DSET-TEST-GOV-015`, `DSET-TEST-GOV-016`, `DSET-TEST-GOV-017`, `DSET-TEST-GOV-018`, `DSET-TEST-GOV-019`, `DSET-TEST-GOV-020`, `DSET-TEST-GOV-021`, `DSET-TEST-GOV-022`, `DSET-TEST-GOV-023`, `DSET-TEST-GOV-024`, `DSET-TEST-GOV-025`, `DSET-TEST-GOV-026`, `DSET-TEST-GOV-027`, `DSET-TEST-GOV-028`, `DSET-TEST-GOV-029`, `DSET-TEST-GOV-030`, `DSET-TEST-GOV-031`, `DSET-TEST-GOV-032`, `DSET-TEST-GOV-033`, `DSET-TEST-GOV-039`, `DSET-TEST-GOV-040`, `DSET-TEST-GOV-041`, `DSET-TEST-META-001`, `DSET-TEST-META-002`, `DSET-TEST-META-003`, `DSET-TEST-META-004`, `DSET-TEST-META-005`, `DSET-TEST-META-006`, `DSET-TEST-META-007`, `DSET-TEST-META-008`, `DSET-TEST-META-009`, `DSET-TEST-META-010`, `DSET-TEST-META-011`, `DSET-TEST-OPS-001`, `DSET-TEST-OPS-002`, `DSET-TEST-OPS-003`, `DSET-TEST-OPS-004`, `DSET-TEST-OPS-005`, `DSET-TEST-OPS-006`, `DSET-TEST-OPS-007`, `DSET-TEST-OPS-016`, `DSET-TEST-SKILL-001`, `DSET-TEST-SKILL-002`, `DSET-TEST-SKILL-003`, `DSET-TEST-SKILL-004`, `DSET-TEST-SKILL-005`, `DSET-TEST-SKILL-006`, `DSET-TEST-SKILL-007`, `DSET-TEST-SKILL-008`, `DSET-TEST-SKILL-009`, `DSET-TEST-SKILL-010`, `DSET-TEST-SKILL-014`, `DSET-TEST-SKILL-015`, `DSET-TEST-SKILL-016`, `DSET-TEST-SKILL-017`, `DSET-TEST-TOOL-001`, `DSET-TEST-TOOL-002`, `DSET-TEST-TOOL-003`, `DSET-TEST-TOOL-004`, `DSET-TEST-TOOL-005`, `DSET-TEST-TOOL-018`, `DSET-TEST-TOOL-019`, `DSET-TEST-TOOL-021`, `DSET-TEST-TOOL-022`

## Artifact inventory

- **Governed artifacts:** 544
- **By role:** atomic=95, derived_or_navigation=84, evergreen=164, implementation=162, transactional=39
- **By type:** analysis_report=23, atomic_record=95, delivery=21, derived_view=1, evidence_record=27, implementation=162, navigation=52, plan=39, procedure=21, specification=95, verification=8
- **By subtype:** architecture=7, behavior=29, change=9, configuration=76, design=7, domain_model=6, evaluation_plan=14, evaluation_result=2, external_audit_analysis=2, governance=46, health_dashboard=1, hub=52, implementation_plan=9, migration=1, playbook=18, proposal=8, readiness_record=2, release_plan=2, release_record=1, review_report=2, roadmap=2, root_cause_analysis=1, run_record=9, runbook=3, solution_landscape=7, source_code=42, technical_investigation=3, test_implementation=43, test_plan=14, test_result=14, version_scope=5
- **By layer:** gov=108, meta=36, ops=44, repository=27, skill=190, tool=139
- **By effective priority:** critical=15, high=43, medium=480, unknown=6
- **By status:** absorbed=14, accepted=41, open=20, resolved=28

## Semantic inventory

- **Semantic claims:** 302
- **By Type:** decision=111, problem=37, qa=136, question=18
- **By direct subtype:** contract=6, defect=17, evaluation=53, gap=4, opportunity=3, requirement=80, test=83
- **Native immutable atoms:** 69
- **Compatibility-classified legacy IDs:** 233

## Typed relation inventory

- **Forward relations:** 357
- **By type:** analysis_of=1, check_of=16, child_of=41, evidence_for=3, implementation_of=264, projection_of=3, relates_to=15, replacement_of=11, resolution_of=3
- **By origin:** authored=62, commit_trailer=264, legacy_child_of=31
- **By source kind:** artifact=93, commit=264

## Unresolved work

- [`DSET-PROBLEM-TOOL-001`](../intake.toml) — problem: Released validator cannot parse schema 1.2
- [`DSET-QUESTION-GOV-001`](../intake.toml) — question: Should Action become a first-class entity?
- [`DSET-QUESTION-META-001`](../intake.toml) — question: Should DSET standardize Journey?
- [`DSET-QUESTION-META-002`](../intake.toml) — question: Should DSET standardize Actor and Persona?
- [`DSET-QUESTION-META-003`](../intake.toml) — question: Should DSET standardize Hypothesis and Experiment?
- [`DSET-QUESTION-OPS-001`](../intake.toml) — question: Should DSET standardize feedback and analytics evidence?
- [`DSET-QUESTION-GOV-003`](../intake.toml) — question: Should DSET generate roadmap and release views?
- [`DSET-PROBLEM-TOOL-002`](../intake.toml) — problem: Generated adopter does not exercise current schema 1.2
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

- None

## Drill-downs

- **Packages:** methodology=46
- **Work Areas:** delivery=5, documentation=8, methodology=10, project-control=443, skills=34, tests=42, toolchain=43

## Canonical return paths

- [manifest](../../meta/dset.toml)
- [governance](../governance.toml)
- [intake](../intake.toml)
- [traceability](traceability.toml)

## Boundaries

Counts are descriptive, not targets. Missing links remain gaps; the
renderer never creates Decisions, implementation, Tests, Evaluations, or
evidence to improve a ratio. `unknown`, `not applicable`, exclusions, and
staleness remain separate dispositions.
