# Provider-neutral DSET Evaluation reconciliation prompt

Use this prompt after the required independent Evaluation runs complete.
Reconciliation interprets comparable result evidence; it does not execute the
Evaluation, revise its definition, or make the final Verification disposition.

## Inputs

- Evaluation ID plus definition version or digest
- exact target revision and subject digest
- prompt, rubric, threshold, and case-set versions or digests
- declared provider/host/model matrix or comparability groups
- every independent result and execution error for those exact identities

## Prompt

Reconcile the supplied independent Evaluation results under
`llm-evaluations-v1` without rerunning the Evaluation or inventing missing
evidence.

Confirm that every result addresses the same active Evaluation ID, target
revision, subject, prompt, rubric, criterion, threshold, case set, and bounded
input set. Group only matrix cells the Evaluation explicitly declares
comparable. Exclude mismatched identities rather than silently normalizing
them. Separate evaluator disagreement, execution error, missing evidence,
ambiguous governance, and genuine threshold failure.

Produce:

1. exact reconciliation identities and declared comparability groups;
2. eligible and excluded results with reasons;
3. per-case and per-criterion agreement, disagreement, errors, and missing
   samples for every claimed matrix cell;
4. unresolved uncertainty, limitations, and defeaters;
5. threshold calculation and resulting `pass`, `fail`, or `inconclusive`
   disposition without discarding per-case findings;
6. the earliest governing, implementation, case-set, rubric, calibration, or
   execution owner requiring correction; and
7. the exact affected cases and matrix cells requiring fresh independent runs.

Do not use majority vote where the Evaluation requires unanimity or an exact
threshold. Do not average incompatible configurations, convert evidence into
authority, silently revise a QA atom, or claim Verification from an incomplete
result set. Unresolved material disagreement remains `inconclusive`.
