# Methodology OPS deterministic test plan

This fragment owns exact deterministic proof for its listed IDs. Shared package behavior is connected by stable IDs, not duplicated plans.

| Test ID | Requirement or invariant | Assertion | Current automation |
|---|---|---|---|
| **DSET-TEST-OPS-001** | DSET-REQUIREMENT-OPS-001, DSET-INVARIANT-OPS-001 | Validate representative supportability contracts for required evidence fields, correlation propagation, deploy/change identity, diagnostic permissions, redaction/access/retention/deletion behavior, volume/cardinality/sampling bounds, and resolvable runbook/incident links | Canonical validator pending; current scenario fixtures and review are manual |
| **DSET-TEST-OPS-002** | DSET-REQUIREMENT-OPS-002 | Parse the delivery workflow and runbook; prove stable policy/DSET check names and required authority/recovery fields | `python -m dset_toolchain check .` plus workflow assertions in CI |
| **DSET-TEST-OPS-003** | DSET-REQUIREMENT-OPS-003, DSET-INVARIANT-OPS-002 | Require selected framework profiles to pass and materialize a complete temporary adopter before an external pilot | `python -m unittest tests.test_self_host tests.test_governance` |
| **DSET-TEST-OPS-004** | DSET-REQUIREMENT-OPS-004, DSET-INVARIANT-OPS-003 | Exercise every allowed bootstrap/pre-1.0/RC/final/post-1.0 transition and reject ambiguous class, wrong arithmetic, invalid RC rollback, missing/multiple class, and automatic 1.0 promotion | Release-policy fixture matrix |
| **DSET-TEST-OPS-005** | DSET-REQUIREMENT-OPS-005, DSET-INVARIANT-OPS-004 | Validate project delivery configuration and one release declaration; prove idempotent preparation, exact-merge publication, already-correct retry, partial recovery, collision stop, immutable tag, and no protected-branch content mutation | Release manifest/CI fixtures and hosted workflow assertion |
| **DSET-TEST-OPS-006** | DSET-REQUIREMENT-OPS-006, DSET-INVARIANT-OPS-005 | Reject RC/final transitions whose exact-SHA readiness artifact has incomplete scope, failed/applicability proof, missing pilot/distribution evidence, blockers, or a substantive final-promotion diff | Release-readiness fixture matrix |
| **DSET-TEST-OPS-007** | DSET-REQUIREMENT-OPS-007, DSET-INVARIANT-OPS-006 | Require canonical product identity and exact SemVer-to-PEP-440 RC equivalence while accepting independent schema/profile/template compatibility versions | Version-surface consistency fixtures |
| **DSET-TEST-OPS-016** | DSET-DECISION-OPS-006, DSET-REQUIREMENT-OPS-013, DSET-INVARIANT-OPS-007 | Require the six exact flat Delivery subtypes, one shared Delivery identity sequence for new carriers, typed reference chain, milestone entries inside Roadmap, explicit ready-or-blocked gate disposition, and immutable combined delivery/publication history; reject former split types, hierarchy, Verification-as-Readiness, standalone Milestone, and competing Release Notes or Publication Record artifacts | `python -m unittest tests.test_release_artifacts tests.test_release_integration` plus `python -m dset_toolchain check .` |

## Regression policy

Every accepted defect adds a deterministic regression test in its owning layer before the repair is archived.
