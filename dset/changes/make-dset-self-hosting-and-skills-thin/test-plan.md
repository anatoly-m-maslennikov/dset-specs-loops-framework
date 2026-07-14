# Test plan — Make DSET self-hosting and skills thin

Deterministic tests prove exact behavior. Probabilistic or qualitative proof belongs in [eval-plan.md](eval-plan.md).

| Test ID | Requirement ID | Deterministic proof | Command or seam |
|---|---|---|---|
| `MDSHAST-TEST-001` | `MDSHAST-REQ-001` | Require the selected framework profiles to pass and materialize a complete in-repository-style adopter before an external pilot | `python -m unittest tests.test_self_host tests.test_governance` |
| `MDSHAST-TEST-002` | `MDSHAST-REQ-002` | Assert the released → candidate → repository/temporary-adopter graph has the declared depth and never recurses from the temporary adopter | `python -m unittest tests.test_self_host` and `python -m dset_toolchain self-host .` |
| `MDSHAST-TEST-003` | `MDSHAST-REQ-003` | Prove materialized local rules resolve without consulting a changed source template and reject any normative path outside the adopter root | `python -m unittest tests.test_governance` |
| `MDSHAST-TEST-004` | `MDSHAST-REQ-004` | Statically reject normative rule bodies, concrete thresholds, copied workflow steps, or an embedded fallback procedure in canonical wrappers | `GovernanceTests.test_wrappers_are_thin_and_registered` plus Skill Creator validation |
| `MDSHAST-TEST-005` | `MDSHAST-REQ-005` | Hold wrapper hashes constant, change a local registered rule, and assert the resolved local identity changes | `GovernanceTests.test_customization_changes_rules_not_wrapper` and generated-wrapper identity test |
| `MDSHAST-TEST-006` | `MDSHAST-REQ-006` | Assert stable codes for missing, duplicate, cyclic, outside-root, and incompatible selected owners while accepting justified non-applicability | `GovernanceTests.test_registry_failure_codes_are_stable` and non-applicability test |
| `MDSHAST-TEST-007` | `MDSHAST-REQ-007` | Assert a local normative edit changes profile status to custom while preserving source profile/version provenance | `GovernanceTests.test_customization_changes_rules_not_wrapper` |
| `MDSHAST-TEST-008` | `MDSHAST-REQ-008` | Validate that exact checks are registered as tests and qualitative criteria remain in a separate eval plan and evidence stream | `python -m dset_toolchain check .` plus change-manifest assertions |
| `MDSHAST-TEST-009` | `MDSHAST-REQ-009` | Reject zero or multiple editable owners for a selected rule ID and reject normative prose in declared derived surfaces | Governance ownership fixtures, thin-wrapper audit, and [rule inventory](proofs/wrapper-rule-inventory-2026-07-14.md) |
| `MDSHAST-TEST-010` | `MDSHAST-REQ-010` | Assert the core distribution declares exactly the five accepted user-facing skills and no separate init, landscape, planning, implementation, ticket, or next-step wrappers | Skill registry/package inventory test |
| `MDSHAST-TEST-011` | `MDSHAST-REQ-011` | Prove `dset` resolves orchestration locally, chains only registered workflows, remains thin, and preserves authorization boundaries | Governance workflow fixtures plus Skill Creator validation |
| `MDSHAST-TEST-012` | `MDSHAST-REQ-012` | Validate the local run-record schema, append-only behavior, ignored location, redaction exclusions, bounded fields, and non-authoritative status | Run-record fixtures and repository ignore check |
| `MDSHAST-TEST-013` | `MDSHAST-REQ-013` | Exercise bootstrap, normal, small, RC, and final transition tables; reject missing/multiple classes, decimal arithmetic, skipped bumps, and automatic `0.9.0` to `1.0.0` promotion | Release-policy unit fixtures |
| `MDSHAST-TEST-014` | `MDSHAST-REQ-014` | Reject inconsistent pre-merge version surfaces and prove post-merge publication targets the protected merge commit without adding content to `main` | Release manifest/CI fixtures and hosted workflow assertion |
| `MDSHAST-TEST-015` | `MDSHAST-REQ-015` | Reject RC/final transitions with incomplete scope, failed tests/evals, missing pilot/distribution evidence, known blockers, or feature additions during RC | Release-readiness fixture matrix |
| `MDSHAST-TEST-016` | `MDSHAST-REQ-016` | Require one product/package/release identity while allowing independent schema/profile/template compatibility versions | Version-surface consistency fixtures |

## Regression rule

Add a failing deterministic proof before fixing every reproducible defect.
