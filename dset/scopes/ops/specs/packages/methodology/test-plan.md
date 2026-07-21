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
| **Historical DSET-TEST-OPS-016** | DSET-DECISION-OPS-006 | Delivery-name release-role proof is superseded by cross-layer `DSET-TEST-GOV-044` | Historical release-role fixtures |
| **DSET-TEST-OPS-017** | DSET-DECISION-OPS-008, DSET-CONTRACT-TOOL-001 | Require representative source, governance, migration, and generated paths to resolve to the repository-owned LF worktree policy | `python -m unittest tests.test_cross_platform_contract` plus hosted platform matrix |
| **DSET-TEST-OPS-018** | DSET-DECISION-OPS-009, DSET-CONTRACT-TOOL-001 | Require case-sensitive POSIX relative-path text to own project-health source traversal instead of host-native Path ordering | `python -m unittest tests.test_health` plus hosted platform matrix |
| **DSET-TEST-OPS-019** | DSET-DECISION-OPS-010, DSET-CONTRACT-TOOL-001 | Require a Windows Python path with backslashes and spaces to remain one exact subprocess argument after verification-template expansion | `python -m unittest tests.test_verification` plus hosted platform matrix |
| **DSET-TEST-OPS-020** | DSET-DECISION-OPS-011, DSET-CONTRACT-TOOL-001 | Require aliased repository paths to compare by resolved identity and Windows relative Path values to serialize as canonical POSIX repository text | Layout, archive, evidence, and hosted platform regressions |
| **DSET-TEST-OPS-021** | DSET-DECISION-OPS-012, DSET-CONTRACT-TOOL-001 | Require temporary Git repositories and byte-sensitive fixtures to preserve exact worktree/blob identity independent of Windows newline defaults | Carrier-transition, semantic-atom, migration, bootstrap, artifact-type, and hosted platform regressions |

## Regression policy

Every accepted defect adds a deterministic regression test in its owning layer before the repair is archived.
