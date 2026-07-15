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

## Regression rule

Add a failing deterministic proof before fixing every reproducible defect.
