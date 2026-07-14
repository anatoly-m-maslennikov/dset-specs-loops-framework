# Deterministic test planning

**Rule ID:** `DSET-RULE-TEST-PLAN`

## Rules

- Derive tests from requirements, invariants, lifecycle transitions, contracts, stable diagnostics, safety boundaries, and regressions before implementation.
- Use a test when one input and state have an exact expected result, regardless of whether execution is automated.
- Cover happy, boundary, invalid, retry, recovery, persistence, migration, concurrency, authorization, and supportability contracts when applicable.
- Prove a reproducible defect fails before its fix and passes after it.
- Name the command or seam, fixture, expected outcome, and requirement/invariant ID.
- Do not move qualitative judgment, variable model quality, navigation usefulness, or diagnostic usefulness into this artifact.
