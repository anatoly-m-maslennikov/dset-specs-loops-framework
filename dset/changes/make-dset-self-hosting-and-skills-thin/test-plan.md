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
| `MDSHAST-TEST-010` | `MDSHAST-REQ-010` | Assert the release-target registry declares exactly the five accepted user-facing skills, no helper wrappers, and one trigger/output/stop boundary per specialist | Skill registry/package inventory test |
| `MDSHAST-TEST-011` | `MDSHAST-REQ-011` | Exercise stable modes, precedence/authority collisions, two-transition cap, specialist/authorization stops, and the rootless preview-authorize-materialize-validate-stop transaction | Governance workflow/bootstrap fixtures plus Skill Creator validation |
| `MDSHAST-TEST-012` | `MDSHAST-REQ-012` | Validate the run-record schema, atomic/terminal/interrupted lifecycle, finite retention, 64-KiB and field bounds, read-only/unavailable behavior, redaction, and advisory status | Run-record fixtures and ignore check |
| `MDSHAST-TEST-013` | `MDSHAST-REQ-013` | Exercise the complete bootstrap/pre-1.0/RC/final/post-1.0 transition table and reject ambiguous/multiple classes, decimal arithmetic, RC rollback, and automatic 1.0 promotion | Release-policy unit fixtures |
| `MDSHAST-TEST-014` | `MDSHAST-REQ-014` | Validate project release configuration and one change declaration; prove idempotent preparation, exact-merge publication, partial retry, collision stop, immutable tag, and no protected-branch content commit | Release manifest/CI fixtures and hosted workflow assertion |
| `MDSHAST-TEST-015` | `MDSHAST-REQ-015` | Reject RC/final transitions whose exact-SHA readiness artifact has incomplete scope, failed/applicability proof, missing pilot/distribution evidence, blockers, or substantive promotion changes | Release-readiness fixture matrix |
| `MDSHAST-TEST-016` | `MDSHAST-REQ-016` | Require canonical product identity and exact SemVer/PEP-440 RC mapping while allowing independent schema/profile/template compatibility versions | Version-surface consistency fixtures |
| `MDSHAST-TEST-017` | `MDSHAST-REQ-017` | Assert model/effort request and effective attestation, known-mismatch reporting, required-gate stop, and visible unverified continuation only where allowed | Orchestration/delegation capability fixtures |
| `MDSHAST-TEST-018` | `MDSHAST-REQ-018` | Validate low/medium/high tree agent/depth/round bounds, quality/scope floor, evidence fields, no price-only downgrade, and plan/actual/deviation records | Budget schema/policy and run-record fixtures |
| `MDSHAST-TEST-019` | `MDSHAST-REQ-019` | Classify defects, debt, risks, optional improvements, uncertainty, tasks, ADRs, changes, GitHub Issues, and Jira tickets as problems/opportunities/questions or non-intake artifacts/representations | Work-routing fixture matrix |

## Regression rule

Add a failing deterministic proof before fixing every reproducible defect.
