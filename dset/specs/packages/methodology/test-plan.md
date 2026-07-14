# Methodology deterministic test plan

## Scope

This plan proves exact structural and terminology claims. Qualitative comprehensibility and routing accuracy belong to [eval-plan.md](eval-plan.md).

| Test ID | Requirement/invariant | Deterministic proof | Current command/status |
|---|---|---|---|
| **METH-TEST-001** | METH-REQ-001 | Assert that README and document 00 link exactly one live file for each numbered methodology owner | Canonical validator pending; current local-link check is ad hoc |
| **METH-TEST-002** | METH-REQ-002, METH-INV-002 | Reject merged test/eval artifact names and universal claims that automation changes proof category | Canonical validator pending |
| **METH-TEST-003** | METH-REQ-003, METH-INV-003/004 | Reject unconditional application WAL/event-store/reconciliation language and duplicate durable owners | Canonical validator pending |
| **METH-TEST-004** | METH-REQ-004 | Reject `exactly-once` claims; require an explicit receiver-side boundary for effectively-once claims | `rg -n -i 'exactly[- ]once' README.md methodology` must return no normative claim |
| **METH-TEST-005** | METH-REQ-005 | Assert six neutral gate rows and isolate Python tool/threshold terms inside the Python profile | Canonical validator pending |
| **METH-TEST-006** | METH-REQ-006 | Validate PR identity, baseline verification, reconciliation, dated candidate status, pushed PR head, final evidence, later-change invalidation, and draft-until-ready state | Canonical validator pending; manual two-phase archive audit required under the pending profile |
| **METH-TEST-007** | METH-REQ-007, METH-INV-005 | Resolve all local Markdown links, balance code fences/details blocks, and reject wiki links or Obsidian callouts | Canonical validator pending; current check is ad hoc |
| **METH-TEST-008** | All | Reject whitespace errors in the proposed diff | `git diff --check` |
| **METH-TEST-009** | METH-REQ-008 | Assert committed project truth uses visible `dset/` and no competing `.dset/` truth exists | Canonical validator pending; current tree check is ad hoc |
| **METH-TEST-010** | METH-REQ-009 | Parse the manifest; assert every package is unique and the global root matches current cross-package ownership | Canonical validator pending; current `yq` check is ad hoc |
| **METH-TEST-011** | METH-REQ-010 | Assert a standard change has the eight named documents plus separate `specs/` and `proofs/` directories | Canonical validator pending; current tree check is ad hoc |
| **METH-TEST-012** | METH-REQ-011 | Reject executable-enforcement claims while the selected profile or canonical command is pending | Canonical validator pending; current metadata review is manual |
| **METH-TEST-013** | METH-REQ-012 | Assert the exact public display name, title, DSET expansion, repository slug, and active metadata identity | Canonical validator pending; current exact-string and remote checks are ad hoc |
| **METH-TEST-014** | METH-REQ-013, METH-INV-007 | Validate representative supportability contracts for required evidence fields, correlation propagation, deploy/change identity, diagnostic permissions, redaction/access/retention/deletion behavior, volume/cardinality/sampling bounds, and resolvable runbook/incident links | Canonical validator pending; current scenario fixtures and review are manual |
| **METH-TEST-015** | METH-REQ-014, METH-INV-008/009 | Assert the five CLI commands, read-only validation, stable diagnostics, explicit writes, and no-overwrite behavior | `python -m unittest tests.test_cli tests.test_scaffold_archive` |
| **METH-TEST-016** | METH-REQ-015 | Materialize every fixture case and compare pass/fail results with expected diagnostic codes | `python -m unittest tests.test_fixtures` |
| **METH-TEST-017** | METH-REQ-016 | Generate traceability twice, assert byte stability, verify freshness, and resolve the real archived/current change IDs and PR #7 | `python -m unittest tests.test_traceability` |
| **METH-TEST-018** | METH-REQ-017 | Prove archive dry-run, readiness/PR/reconciliation gates, atomic move, and destination refusal | `python -m unittest tests.test_scaffold_archive` |
| **METH-TEST-019** | METH-REQ-018, METH-INV-010 | Validate three skill packages, UI metadata, distinct trigger descriptions, and static cross-platform portability | Skill Creator `quick_validate.py` plus the repository skill audit |
| **METH-TEST-020** | METH-REQ-019 | Parse the delivery workflow and runbook; prove stable policy/DSET check names and required authority/recovery fields | `python -m dset_toolchain check .` plus workflow assertions in CI |
| **METH-TEST-021** | METH-REQ-020 | Project configuration and schema accept separate implementation-language and artifact-profile fields without substitution | `python -m dset_toolchain check .` plus schema parsing |
| **METH-TEST-022** | METH-REQ-021/024 | Accept unique valid governed areas and reject missing hubs, duplicate roots, unresolved parents, and parent cycles with stable diagnostics | `python -m unittest tests.test_artifact_profile` |
| **METH-TEST-023** | METH-REQ-021/025 | Assert the root README links every registered top-level area hub and every hub contains Purpose, Boundaries, and Start here/Navigation | `python -m unittest tests.test_artifact_profile` |
| **METH-TEST-024** | METH-REQ-022/023 | Assert the released artifact-type catalog and universal plus specification-specific authoring rules exist and remain linked from the documentation hub | `python -m dset_toolchain check .` plus artifact review |
| **METH-TEST-025** | METH-REQ-024 | Parse `dset/artifacts.yaml` and its schema; prove diagnostics DSET-E120–123 through valid and invalid registry cases | `python -m unittest tests.test_artifact_profile` |
| **METH-TEST-026** | METH-REQ-020–025, METH-INV-011/012 | Run the selected Python and documentation profiles together with portability, trace freshness, and diff hygiene | `uv run dset verify .` |
| **METH-TEST-027** | METH-REQ-026, METH-INV-013 | Reject a DSET 0.2 release candidate lacking repository adoption for an applicable selected profile or a passing versioned in-repository adopter fixture for a non-applicable profile-specific capability | Planned 0.2 self-hosting fixture gate |
| **METH-TEST-028** | METH-REQ-027, METH-INV-014 | Assert the released → candidate → repository/temporary-adopter graph has the declared depth and that the temporary adopter cannot create another adopter or traverse unrelated DSET roots | Planned 0.2 recursive-runner tests |
| **METH-TEST-029** | METH-REQ-028, METH-INV-015 | Prove materialized local rules resolve without consulting a changed source template and reject normative paths outside the adopter root | Planned 0.2 resolver/materializer tests |
| **METH-TEST-030** | METH-REQ-029, METH-INV-016 | Statically reject substantive normative rules, concrete thresholds, copied workflow steps, or embedded fallback procedures in canonical workflow wrappers | Planned 0.2 wrapper audit |
| **METH-TEST-031** | METH-REQ-030, METH-INV-017 | Hold the wrapper hash constant, change a registered local rule, and assert the resolved identity and next invocation input change | Planned 0.2 wrapper mutation test |
| **METH-TEST-032** | METH-REQ-031, METH-INV-018 | Assert stable diagnostics for missing, duplicate, cyclic, outside-root, and profile-incompatible selected owners while accepting justified non-applicability | Planned 0.2 invalid-fixture matrix |
| **METH-TEST-033** | METH-REQ-032, METH-INV-019 | Assert a local normative edit changes ruleset status to custom while preserving source profile/version provenance | Planned 0.2 ruleset identity tests |
| **METH-TEST-034** | METH-REQ-033, METH-INV-020 | Validate that exact governance checks are registered as tests while qualitative criteria remain in a separate eval plan and evidence stream | `python -m dset_toolchain check .` plus planned 0.2 manifest assertions |
| **METH-TEST-035** | METH-REQ-034, METH-INV-021 | Reject zero or multiple editable owners for a selected normative rule ID and reject normative rule bodies in declared derived surfaces | Planned 0.2 ownership fixtures and wrapper audit |

## Regression policy

Every documentation defect fixed after this baseline must add or extend a deterministic check when machine detection is feasible. A check first demonstrates failure against the defective revision, then passes against the correction.
