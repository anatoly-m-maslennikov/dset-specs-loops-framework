# Qualitative and probabilistic eval planning

**Rule ID:** `DSET-RULE-EVAL-PLAN`

## Rules

- Use an eval only when multiple outputs may be acceptable or acceptance requires a rubric, dataset, reviewer judgment, probability, calibration, or drift analysis.
- State applicability, cases or datasets, criteria, threshold, calibration, budget, and evidence location before implementation.
- Keep deterministic correctness in the test plan even when an automated agent runs the eval harness.
- Use independent reviewers or isolated runs where interpretation matters; record disagreements and correct the earliest ambiguous governing artifact.
- Measure rule-following, navigation, diagnostic usefulness, and output quality without exposing secrets or unbounded production data.
- When no qualitative or probabilistic surface exists, record a concrete not-applicable reason rather than inventing an eval.
