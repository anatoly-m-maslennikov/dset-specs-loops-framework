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
| **DSET-TEST-TOOL-019** | DSET-REQUIREMENT-TOOL-019, DSET-INVARIANT-TOOL-005, DSET-INVARIANT-GOV-016 | Exercise a pairwise governed-role matrix: classify normative pairs as atomic-over-stale-projection, absorbing-over-absorbed, immutable-over-mutable, unsatisfiable immutable, or selectable policy; route other role pairs deterministically; resolve only selectable conflicts by explicit precedence then higher effective priority; reject absorption cycles, age-based precedence, and mutation; allow only byte-stable fully-retired archive moves with stable lookup; emit stable records; stop where required; and invalidate results after reprioritization | Priority-conflict, atomic-lifecycle, and archive-relocation unit/fixture tests |

## Regression policy

Every accepted defect adds a deterministic regression test in its owning layer before the repair is archived.
