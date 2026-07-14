# Methodology SKILL deterministic test plan

This fragment owns exact deterministic proof for its listed IDs. Shared package behavior is connected by stable IDs, not duplicated plans.

| Test ID | Requirement or invariant | Assertion | Current automation |
|---|---|---|---|
| **DSET-TEST-SKILL-001** | DSET-REQUIREMENT-SKILL-001, DSET-INVARIANT-SKILL-001 | Validate three skill packages, UI metadata, distinct trigger descriptions, and static cross-platform portability | Skill Creator `quick_validate.py` plus the repository skill audit |
| **DSET-TEST-SKILL-002** | DSET-REQUIREMENT-SKILL-002, DSET-INVARIANT-SKILL-002 | Statically reject substantive normative rules, concrete thresholds, copied workflow steps, or embedded fallback procedures in canonical workflow wrappers | Governance thin-wrapper test plus Skill Creator validation |
| **DSET-TEST-SKILL-003** | DSET-REQUIREMENT-SKILL-003, DSET-INVARIANT-SKILL-003 | Hold the wrapper hash constant, change a registered local rule, and assert the resolved identity and next invocation input change | Governance customization and generated-wrapper identity tests |
| **DSET-TEST-SKILL-004** | DSET-REQUIREMENT-SKILL-004, DSET-INVARIANT-SKILL-004 | Assert the release-target registry declares exactly `dset`, `dset-clarify`, `dset-diagnose`, `dset-prototype`, and `dset-release`, with no helper wrappers, and that each specialist has one trigger/output/stop boundary | Skill registry/package inventory test |
| **DSET-TEST-SKILL-005** | DSET-REQUIREMENT-SKILL-005, DSET-INVARIANT-SKILL-002, DSET-INVARIANT-SKILL-004 | Exercise every stable mode, precedence collision, authority/freshness case, two-transition cap, authorization stop, and rootless preview/authorize/materialize/validate/stop transaction | Governance orchestration and bootstrap fixtures plus Skill Creator validation |
| **DSET-TEST-SKILL-006** | DSET-REQUIREMENT-SKILL-006, DSET-INVARIANT-SKILL-005 | Validate the published run-record schema, atomic unique creation, terminal/interrupted lifecycle, 64-KiB/field/retention bounds, read-only/unavailable persistence, redaction allowlist, and non-authoritative status | Run-record fixtures and repository ignore check |
| **DSET-TEST-SKILL-007** | DSET-REQUIREMENT-SKILL-007, DSET-INVARIANT-SKILL-006 | Assert request/effective model-effort capability discovery and attestation, pre-spawn mismatch reporting, required-gate stop, and visible unverified continuation only where permitted | Orchestration/delegation capability fixtures |
| **DSET-TEST-SKILL-008** | DSET-REQUIREMENT-SKILL-008, DSET-INVARIANT-SKILL-007 | Validate low/medium/high tree-wide agent/depth/round bounds, override precedence, quality/scope floor, task-evidence fields, no price-only downgrade, and plan/actual/deviation records | Budget schema/policy and run-record fixtures |
| **DSET-TEST-SKILL-009** | DSET-REQUIREMENT-SKILL-009, DSET-INVARIANT-SKILL-008 | Validate session/root/parent run identity, atomic bounded checkpoint replacement, redaction, explicit/compatible resume selection, ambiguity stop, compaction handoff, authoritative-state reconciliation, and unavailable-persistence behavior | Session/run schema fixtures and orchestration resume cases |

## Regression policy

Every accepted defect adds a deterministic regression test in its owning layer before the repair is archived.
