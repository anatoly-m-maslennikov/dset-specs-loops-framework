# LLM Evaluations profile v1

## Scope

`llm-evaluations-v1` applies to Evaluation definitions, scenario sets, prompts,
harnesses, graders, reconciliation procedures, and result carriers where
judgment, probability, or model behavior prevents a deterministic Test from
owning the claim. It does not convert deterministic assertions into
Evaluations and does not treat an Evaluation result as authority.

The profile is provider agnostic. Provider/model/host details are run
configuration and evidence. They never become hidden semantics of the
Evaluation definition.

## Definition

Before execution, every Evaluation states:

1. stable Evaluation ID and governed claim IDs;
2. objective and why deterministic Test coverage is insufficient;
3. exact subject, target revision, bounded inputs, and exclusions;
4. representative task distribution plus normal, edge, adversarial, failure,
   and ambiguous cases that apply;
5. criterion-level rubric with observable anchors;
6. pass/fail/inconclusive threshold and aggregation rule;
7. grader type, calibration method, reconciliation rule, and stopping rule;
8. permitted tools, data, writes, budget, retries, and safety boundary; and
9. evidence schema and freshness policy.

Split independent criteria instead of hiding several judgments behind one
overall score. Keep test data and production-derived cases representative,
bounded, redacted, and versioned. Held-out cases remain separate from prompt or
grader tuning.

## Grading

1. Use code-based grading for deterministic facts. Do not spend model judgment
   on exact structure, identifiers, counts, or other assertions a Test can own.
2. Use model or human grading only for criteria that require judgment. Rubrics
   use precise labels, anchored scales, examples, and automatic-fail conditions
   where applicable.
3. Prefer classification, pairwise comparison, or criterion-level scoring over
   unconstrained open-ended grading. A scalar score never substitutes for the
   criterion findings that produced it.
4. Calibrate model graders against independently reviewed examples. Record
   agreement and known disagreement modes; rerun calibration when the grader,
   rubric, task distribution, or relevant model changes.
5. Do not let the author be the only evaluator for consequential acceptance.
   Blind reviewers to intended answers, prior results, and misleading carrier
   names when those inputs are unnecessary.

## Execution and evidence

1. Each run records Evaluation ID, exact target revision, prompt/rubric/case-set
   versions or digests, provider, model, effective parameters, tools,
   permissions, budget, evaluator identity, timestamp, and inspected inputs.
2. Independent runs do not share prior outputs. Randomness, retries, and sample
   counts are explicit. Use enough repetitions for the declared threshold and
   report variance where nondeterminism matters.
3. Preserve per-case findings, failures, errors, exclusions, uncertainty,
   latency, usage, and cost when applicable. Never report only the aggregate.
4. Evaluation definitions, execution work, result evidence, and Verification
   remain separate. A result cannot rewrite its own rubric or threshold.
5. Logs are bounded and redacted. Production cases containing sensitive data
   use approved handling and retention rather than entering committed fixtures.

## Reconciliation and lifecycle

1. Reconcile only results for the same Evaluation version, target revision,
   case-set identity, rubric, and threshold. Exclude mismatched runs explicitly.
2. Separate evaluator disagreement, execution error, missing evidence,
   ambiguous governance, and genuine threshold failure.
3. Do not average incompatible findings or use majority vote when the authored
   threshold requires unanimity or criterion-level success. Unresolved material
   disagreement is inconclusive.
4. Correct the earliest ambiguous owner, then rerun affected cases against the
   corrected version. Preserve earlier failures as evidence.
5. Run Evaluations early and after relevant changes. Add production-discovered
   failures and edge cases to the maintained regression set without leaking
   held-out answers into the system under evaluation.

## Sources

- [OpenAI — Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [OpenAI — Working with evals](https://developers.openai.com/api/docs/guides/evals)
- [Anthropic — Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)
- [Anthropic — Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
