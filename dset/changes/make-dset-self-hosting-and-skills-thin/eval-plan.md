# Eval plan — Make DSET self-hosting and skills thin

## Applicability

Applicable. The invariant contract governs how agents discover, interpret, and follow repository-local natural-language rules. Exact resolver and wrapper mechanics stay in [test-plan.md](test-plan.md); these evals measure whether the resulting workflow is understandable and correctly applied.

## Cases and thresholds

| Eval ID | Case | Criterion | Threshold |
|---|---|---|---|
| `MDSHAST-EVAL-001` | Two adopters use one unchanged wrapper but deliberately different local output rules | Local-rule following | Every independent run follows the adopter's registered local rule, identifies its rule ID/path, and never substitutes the framework template |
| `MDSHAST-EVAL-002` | A cold agent starts from a workflow request in a customized adopter | Navigation and ownership | Every reviewer reaches the registry, resolved local owner, and custom/source identity without treating a skill, template, summary, or cache as normative |
| `MDSHAST-EVAL-003` | Each invalid-ownership fixture emits only its stable code, path, and actionable message | Diagnostic usefulness | Every reviewer identifies the blocking ownership defect and a safe correction without reading resolver source or inventing a fallback rule |
| `MDSHAST-EVAL-004` | A wrapper cannot resolve its workflow because ownership is missing or incompatible | Fail-closed restraint | Every independent run stops before governed work, reports the unresolved state, and does not continue from embedded knowledge or remote framework prose |

## Calibration and budget

Use at least two independent reviewers or isolated agent runs per case. Preserve the wrapper hash, registry/ruleset identity, bounded prompts, decisions, and disagreements. Correct the earliest ambiguous governing artifact and rerun the failed case; do not average a blocking failure into a passing score.

## Evidence

Store bounded outputs or redacted summaries under `proofs/` and link them from `verification.md`.
