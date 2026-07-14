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

## Calibration and evidence

Use at least two independent reviewers for a baseline. Record disagreements by scenario and criterion; resolve them by correcting the earliest ambiguous artifact rather than averaging scores. Store redacted results in the implementing change's `verification.md` or linked proof evidence.
