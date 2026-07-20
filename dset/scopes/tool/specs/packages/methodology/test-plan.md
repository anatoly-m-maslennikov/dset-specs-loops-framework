# Methodology TOOL deterministic test plan

This fragment owns exact deterministic proof for its listed IDs. Shared package behavior is connected by stable IDs, not duplicated plans.

| Test ID | Requirement or invariant | Assertion | Current automation |
|---|---|---|---|
| **DSET-TEST-TOOL-001** | All | Reject whitespace errors in the proposed diff | `git diff --check` |
| **DSET-TEST-TOOL-002** | DSET-REQUIREMENT-TOOL-001, DSET-INVARIANT-TOOL-001, DSET-INVARIANT-TOOL-002 | Assert the five CLI commands, read-only validation, stable diagnostics, explicit writes, and no-overwrite behavior | `python -m unittest tests.test_cli tests.test_scaffold_archive` |
| **DSET-TEST-TOOL-003** | DSET-REQUIREMENT-TOOL-002 | Generate traceability twice, assert byte stability, verify freshness, and resolve the real archived/current change IDs and PR #7 | `python -m unittest tests.test_traceability` |
| **DSET-TEST-TOOL-004** | DSET-REQUIREMENT-TOOL-003 | Prove archive dry-run, readiness/PR/reconciliation gates, atomic move, and destination refusal | `python -m unittest tests.test_scaffold_archive` |
| **DSET-TEST-TOOL-005** | DSET-REQUIREMENT-TOOL-004, DSET-INVARIANT-TOOL-003 | Assert the released → candidate → repository/temporary-adopter graph has the declared depth and that the temporary adopter cannot create another adopter or traverse unrelated DSET roots | `python -m unittest tests.test_self_host` and `python -m dset_toolchain self-host .` |
| **DSET-TEST-TOOL-018** | DSET-REQUIREMENT-TOOL-018, DSET-INVARIANT-TOOL-004 | Render unchanged health inputs twice for byte stability, detect stale output in check mode, refresh only the declared generated destination, preserve repository/layer/package/Work Area drill-downs, and reject private or authoritative dashboard state | Project-health unit and fixture tests |
| **DSET-TEST-TOOL-019** | DSET-REQUIREMENT-TOOL-019, DSET-INVARIANT-TOOL-005, DSET-INVARIANT-GOV-016..017 | Exercise a pairwise governed-role matrix; classify semantic type independently from workflow; reject false Conflicts for drift, assurance, nonconformance, and evidence adjudication; emit immutable Conflict atoms only for verified incompatible applicable claims; resolve only selectable policy Conflicts by explicit precedence then higher effective priority; append linked resolution lifecycle events; leave unsatisfiable Conflicts open; reject absorption cycles, age-based precedence, and mutation; allow only byte-stable fully-retired archive moves with stable lookup; stop where required; and invalidate results after reprioritization | Priority-conflict, semantic-classification, atomic-lifecycle, and archive-relocation unit/fixture tests |
| **DSET-TEST-TOOL-021** | DSET-REQUIREMENT-TOOL-021 | Validate the candidate profile schema, exact six gates, pinned evidence, safe paths, canonical command closure, warning-only ratchet, zero-error baseline, blocker/status rules, and read-only target drift detection; reject a missing gate, unpinned source, unsafe path, inconsistent baseline, active blocker, or mismatched target revision/script/lockfile/file population | `python -m unittest tests.test_enforcement_profiles` and `python -m dset_toolchain profile check --profile typescript-v1-candidate --target <pinned-pilot>` |
| **DSET-TEST-TOOL-022** | DSET-REQUIREMENT-TOOL-022 | Require explicit reference/applied role semantics and applied origin; reject malformed roles and adopter fallback to a framework reference; accept a project-local applied instance; expose the selected role without executing target commands | `python -m unittest tests.test_enforcement_profiles` plus framework/OYOHA profile inspection |

## Regression policy

Every accepted defect adds a deterministic regression test in its owning layer before the repair is archived.
