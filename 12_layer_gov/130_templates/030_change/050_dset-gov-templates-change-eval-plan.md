# Eval plan — {{title}}

## Applicability

State `Applicable` with the comparison question, comparator or baseline, cases,
rubric, thresholds, calibration, environment and model/tool/data versions,
freshness window, budget, and abstain/inconclusive behavior, or state `Not
applicable` with a concrete reason. Automation alone does not make a check an
eval.

## Cases and thresholds

| Eval ID | Case | Comparator | Criterion | Threshold | Abstain/inconclusive rule |
|---|---|---|---|---|---|
| `{{project_key}}-EVAL-PLAN{{id_layer}}-001` | Define a variable or qualitative case | Name the baseline | Define the rubric | Define acceptance | Define when evidence cannot decide |

Keep criterion-level results, costs, failures, and uncertainty. Do not create a
universal winner score across incompatible criteria or contexts.

## Evidence

Store bounded outputs or redacted summaries under `proofs/` and link them from
`verification.md`. Bind evidence to the evaluated commit/artifact versions and
record its freshness or expiry.
