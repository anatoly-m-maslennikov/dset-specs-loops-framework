---
artifact_type: derived_view
artifact_subtype: health_dashboard
artifact_id: DSET-DERIVED-VIEW-001
priority: low
llm_session_ids: []
---

# DSET project health

> [!NOTE]
> This generated view is not authority. Follow each link to its canonical
> owner and refresh explicitly after source changes.

- **Source digest:** `0eaab361036f2fcaa8fe816cd918c988da56aedd8895f0ac90d388c4dd59da12`
- **Renderer:** `dset health` schema 1.0

## Coverage

| Closure | Numerator | Denominator | Excluded | N/A | Unknown | Stale |
|---|---:|---:|---:|---:|---:|---:|
| Decision authority compiled into evergreen truth | 86 | 86 | 0 | 0 | 0 | 0 |
| Decision authority linked from implementation commits | 9 | 9 | 77 | 0 | 0 | 0 |
| Applicable authority connected to Test or Evaluation | 86 | 86 | 0 | 0 | 0 | 0 |
| QA definitions connected to current evidence | 49 | 116 | 0 | 0 | 66 | 1 |

### Coverage gaps

- **Decision authority compiled into evergreen truth:** none
- **Decision authority linked from implementation commits:** none
- **Applicable authority connected to Test or Evaluation:** none
- **QA definitions connected to current evidence:** `DSET-EVAL-GOV-010`, `DSET-EVAL-GOV-011`, `DSET-EVAL-GOV-012`, `DSET-EVAL-GOV-013`, `DSET-EVAL-GOV-014`, `DSET-EVAL-GOV-015`, `DSET-EVAL-GOV-016`, `DSET-EVAL-GOV-018`, `DSET-EVAL-GOV-020`, `DSET-EVAL-GOV-021`, `DSET-EVAL-GOV-023`, `DSET-EVAL-META-004`, `DSET-EVAL-META-005`, `DSET-EVAL-META-006`, `DSET-EVAL-META-007`, `DSET-EVAL-META-008`, `DSET-EVAL-META-009`, `DSET-EVAL-SKILL-003`, `DSET-EVAL-SKILL-004`, `DSET-EVAL-SKILL-005`, `DSET-EVAL-SKILL-006`, `DSET-EVAL-SKILL-007`, `DSET-EVAL-SKILL-008`, `DSET-TEST-GOV-001`, `DSET-TEST-GOV-002`, `DSET-TEST-GOV-003`, `DSET-TEST-GOV-004`, `DSET-TEST-GOV-010`, `DSET-TEST-GOV-011`, `DSET-TEST-GOV-012`, `DSET-TEST-GOV-013`, `DSET-TEST-GOV-014`, `DSET-TEST-GOV-015`, `DSET-TEST-GOV-016`, `DSET-TEST-GOV-017`, `DSET-TEST-GOV-018`, `DSET-TEST-GOV-019`, `DSET-TEST-GOV-020`, `DSET-TEST-GOV-021`, `DSET-TEST-GOV-023`, `DSET-TEST-GOV-024`, `DSET-TEST-GOV-025`, `DSET-TEST-GOV-028`, `DSET-TEST-GOV-029`, `DSET-TEST-GOV-030`, `DSET-TEST-GOV-031`, `DSET-TEST-GOV-033`, `DSET-TEST-META-001`, `DSET-TEST-META-005`, `DSET-TEST-META-006`, `DSET-TEST-META-007`, `DSET-TEST-META-008`, `DSET-TEST-META-009`, `DSET-TEST-META-010`, `DSET-TEST-META-011`, `DSET-TEST-OPS-001`, `DSET-TEST-OPS-016`, `DSET-TEST-SKILL-003`, `DSET-TEST-SKILL-004`, `DSET-TEST-SKILL-005`, `DSET-TEST-SKILL-006`, `DSET-TEST-SKILL-007`, `DSET-TEST-SKILL-008`, `DSET-TEST-SKILL-009`, `DSET-TEST-SKILL-010`, `DSET-TEST-TOOL-018`

## Artifact inventory

- **Governed artifacts:** 333
- **By role:** atomic=28, derived_or_navigation=84, evergreen=88, implementation=113, transactional=20
- **By type:** analysis_report=20, atomic_record=28, change=9, derived_view=1, evidence_record=11, implementation=113, navigation=52, plan=40, readiness_record=2, release_record=1, specification=48, verification=8
- **By subtype:** architecture=5, behavior=10, configuration=9, design=7, documentation=33, domain_model=6, evaluation_plan=14, external_audit_analysis=1, governance=15, health_dashboard=1, hub=52, implementation_plan=7, proposal=8, release_plan=2, review_report=1, roadmap=2, root_cause_analysis=1, run_record=9, solution_landscape=7, source_code=34, technical_investigation=2, test_implementation=37, test_plan=14, test_result=1, version_scope=5
- **By layer:** gov=68, meta=24, ops=33, repository=4, skill=95, tool=109
- **By effective priority:** critical=1, high=2, medium=324, unknown=6
- **By status:** accepted=9, archived=4, in-progress=1, open=22, resolved=11

## Semantic inventory

- **Semantic claims:** 242
- **By Type:** decision=93, problem=15, qa=116, question=18
- **By direct subtype:** contract=6, evaluation=46, opportunity=3, requirement=71, test=70
- **Native immutable atoms:** 9
- **Compatibility-classified legacy IDs:** 233

## Unresolved work

- [`DSET-PROBLEM-TOOL-001`](../intake.yaml) — problem: Released validator cannot parse schema 1.2
- [`DSET-QUESTION-GOV-001`](../intake.yaml) — question: Should Action become a first-class entity?
- [`DSET-QUESTION-META-001`](../intake.yaml) — question: Should DSET standardize Journey?
- [`DSET-QUESTION-META-002`](../intake.yaml) — question: Should DSET standardize Actor and Persona?
- [`DSET-QUESTION-META-003`](../intake.yaml) — question: Should DSET standardize Hypothesis and Experiment?
- [`DSET-QUESTION-OPS-001`](../intake.yaml) — question: Should DSET standardize feedback and analytics evidence?
- [`DSET-QUESTION-GOV-003`](../intake.yaml) — question: Should DSET generate roadmap and release views?
- [`DSET-PROBLEM-TOOL-002`](../intake.yaml) — problem: Generated adopter does not exercise current schema 1.2
- [`DSET-PROBLEM-SKILL-001`](../intake.yaml) — problem: Core skill runtime is incomplete
- [`DSET-PROBLEM-OPS-001`](../intake.yaml) — problem: Current exact-head hosted proof is missing
- [`DSET-PROBLEM-OPS-002`](../intake.yaml) — problem: Release-planning enforcement is not implemented
- [`DSET-QUESTION-META-004`](../intake.yaml) — question: Should evidence context be separate from Work Area?
- [`DSET-QUESTION-META-005`](../intake.yaml) — question: Should Work Areas expose optional descriptive tags?
- [`DSET-QUESTION-GOV-004`](../intake.yaml) — question: Should traceability use typed relation edges?
- [`DSET-QUESTION-GOV-005`](../intake.yaml) — question: Should Decision lifecycle be schema-enforced?
- [`DSET-PROBLEM-GOV-004`](../intake.yaml) — problem: The declared Your Harness pilot has not adopted DSET
- [`DSET-QUESTION-GOV-006`](../intake.yaml) — question: Should proof dependency closures become machine-readable?
- [`DSET-OPPORTUNITY-GOV-001`](../intake.yaml) — question/opportunity: Generate a proof-currentness review view
- [`DSET-OPPORTUNITY-TOOL-001`](../intake.yaml) — question/opportunity: Expand schema template validation into a compatibility matrix
- [`DSET-OPPORTUNITY-OPS-001`](../intake.yaml) — question/opportunity: Generate a cross-repository adoption status view
- [`DSET-QUESTION-TOOL-001`](../intake.yaml) — question: When should project health gain an interactive renderer?
- [`DSET-QUESTION-GOV-007`](../intake.yaml) — question: How strictly should external review reports be schema-enforced?

## Open Conflicts

- None

## Conflict outcomes

- None

## Drill-downs

- **Packages:** methodology=25
- **Work Areas:** delivery=0, documentation=1, methodology=1, project-control=259, skills=34, tests=37, toolchain=34

## Canonical return paths

- [manifest](../../meta/dset.yaml)
- [governance](../governance.yaml)
- [intake](../intake.yaml)
- [traceability](traceability.yaml)

## Boundaries

Counts are descriptive, not targets. Missing links remain gaps; the
renderer never creates Decisions, implementation, Tests, Evaluations, or
evidence to improve a ratio. `unknown`, `not applicable`, exclusions, and
staleness remain separate dispositions.
