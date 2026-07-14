# Test plan — Make DSET self-hosting and skills thin

Deterministic tests prove exact behavior. Probabilistic or qualitative proof belongs in [eval-plan.md](eval-plan.md).

| Test ID | Requirement ID | Deterministic proof | Command or seam |
|---|---|---|---|
| `MDSHAST-TEST-001` | `MDSHAST-REQ-001` | Reject a release fixture lacking either repository adoption for an applicable profile or an in-repository adopter fixture for a non-applicable profile | Planned self-hosting fixture gate |
| `MDSHAST-TEST-002` | `MDSHAST-REQ-002` | Assert the released → candidate → repository/temporary-adopter graph has the declared depth and never recurses from the temporary adopter | Planned recursive-runner unit test |
| `MDSHAST-TEST-003` | `MDSHAST-REQ-003` | Prove materialized local rules resolve without consulting a changed source template and reject any normative path outside the adopter root | Planned resolver/materializer tests |
| `MDSHAST-TEST-004` | `MDSHAST-REQ-004` | Statically reject normative rule bodies, concrete thresholds, copied workflow steps, or an embedded fallback procedure in canonical wrappers | Planned wrapper audit |
| `MDSHAST-TEST-005` | `MDSHAST-REQ-005` | Hold the wrapper hash constant, change a local registered rule, and assert the resolved rule identity and invocation input change | Planned wrapper mutation test |
| `MDSHAST-TEST-006` | `MDSHAST-REQ-006` | Assert stable codes for missing, duplicate, cyclic, outside-root, and incompatible selected owners while accepting justified non-applicability | Planned invalid-fixture matrix |
| `MDSHAST-TEST-007` | `MDSHAST-REQ-007` | Assert a local normative edit changes profile status to custom while preserving source profile/version provenance | Planned ruleset identity test |
| `MDSHAST-TEST-008` | `MDSHAST-REQ-008` | Validate that exact checks are registered as tests and qualitative criteria remain in a separate eval plan and evidence stream | `python -m dset_toolchain check .` plus manifest assertions |
| `MDSHAST-TEST-009` | `MDSHAST-REQ-009` | Reject zero or multiple editable owners for a selected rule ID and reject normative prose in declared derived surfaces | Planned ownership fixtures and wrapper audit |

## Regression rule

Add a failing deterministic proof before fixing every reproducible defect.
