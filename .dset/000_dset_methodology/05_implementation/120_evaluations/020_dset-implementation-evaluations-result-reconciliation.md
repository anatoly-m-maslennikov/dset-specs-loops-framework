# DSET Evaluation reconciliation prompt

Use this prompt after the required independent Evaluation runs complete.

## Inputs

- Evaluation ID and authored threshold
- exact target revision
- every independent result for that revision

## Prompt

Reconcile the supplied independent Evaluation results without rerunning the
Evaluation or inventing missing evidence.

Confirm that every result addresses the same active Evaluation ID, target
revision, criterion, threshold, and bounded input set. Separate evaluator
disagreement, execution error, missing evidence, ambiguous governance, and a
genuine threshold failure.

Produce:

1. eligible and excluded results with reasons;
2. agreement and disagreement by criterion and case;
3. unresolved uncertainty and defeaters;
4. the resulting pass, fail, or inconclusive disposition;
5. the earliest artifact or implementation owner requiring correction; and
6. whether a fresh independent rerun is required after correction.

Do not use majority vote where the Evaluation requires unanimity or an exact
threshold. Do not convert evidence into authority, silently revise a QA atom,
or claim Verification from an incomplete result set.
