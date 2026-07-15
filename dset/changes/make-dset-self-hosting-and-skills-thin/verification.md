# Verification — Make DSET self-hosting and skills thin

- **Implementing PR:** [anatoly-m-maslennikov/dset-specs-loops-framework#9](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/9)
- **Status:** roadmap §§0–§4 pass; qualitative evals and roadmap §§5–§10 remain pending

| Gate | Command or method | Result | Evidence |
|---|---|---|---|
| Invariant contract | IDs, scenarios, proof-category separation, and accepted methodology mapping | Pass | [Invariant contract verification](proofs/invariant-contract-verification-2026-07-14.md) |
| Rule migration | Pre-refactor skill bodies mapped to one registered owner; current wrappers retain only allowed fields | Pass | [Wrapper rule inventory](proofs/wrapper-rule-inventory-2026-07-14.md) |
| MDSHAST-TEST-001–009 | Ruff, mypy, 37 unit/fixture tests, governance failure matrix, generated-wrapper identity, local fixed point, `dset check`, canonical `dset verify`, and diff hygiene | Pass locally | [Local fixed-point proof](proofs/local-fixed-point-2026-07-14.md) and [clarify rename verification](proofs/clarify-rename-verification-2026-07-14.md) |
| Hosted fixed point | Same pushed `dev`/PR head through GitHub checks | Pass after a recorded shallow-checkout corrective loop | [Hosted fixed-point proof](proofs/hosted-fixed-point-2026-07-14.md) |
| MDSHAST-EVAL-001–004 | Independent local-rule following, navigation, diagnostic-usefulness, and fail-closed restraint reviews | Pending; remains separate from tests | [Eval plan](eval-plan.md) |
| Supportability | Existing repository delivery contract | Applicable; no adopter runtime or production data changed | [Delivery runbook](../../supportability/delivery-runbook.md) |
| Reconciliation/archive | Accepted invariant/test mappings updated; current change remains active | Not archive-ready until later roadmap, eval, hosted, reconciliation, and release gates pass | [Tasks](tasks.md) |

Record fresh commands, exit status, bounded summaries, unresolved failures, and the completion disposition. Never persist secrets or sensitive raw output.
