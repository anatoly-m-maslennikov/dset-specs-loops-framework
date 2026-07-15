# Methodology GOV deterministic test plan

This fragment owns exact deterministic proof for its listed IDs. Shared package behavior is connected by stable IDs, not duplicated plans.

| Test ID | Requirement or invariant | Assertion | Current automation |
|---|---|---|---|
| **DSET-TEST-GOV-001** | DSET-REQUIREMENT-GOV-001 | Assert six neutral gate rows and isolate Python tool/threshold terms inside the Python profile | Canonical validator pending |
| **DSET-TEST-GOV-002** | DSET-REQUIREMENT-GOV-002 | Validate PR identity, baseline verification, reconciliation, dated candidate status, pushed PR head, final evidence, later-change invalidation, and draft-until-ready state | Canonical validator pending; manual two-phase archive audit required under the pending profile |
| **DSET-TEST-GOV-003** | DSET-REQUIREMENT-GOV-003, DSET-INVARIANT-GOV-002 | Resolve all local Markdown links, balance code fences/details blocks, and reject wiki links or Obsidian callouts | Canonical validator pending; current check is ad hoc |
| **DSET-TEST-GOV-004** | DSET-REQUIREMENT-GOV-004 | Assert committed project truth uses visible `dset/` and no competing `.dset/` truth exists | Canonical validator pending; current tree check is ad hoc |
| **DSET-TEST-GOV-005** | DSET-REQUIREMENT-GOV-005 | Parse the manifest; assert every package is unique and the global root matches current cross-package ownership | Canonical validator pending; current `yq` check is ad hoc |
| **DSET-TEST-GOV-006** | DSET-REQUIREMENT-GOV-006 | Assert a standard change has the eight named documents plus separate `specs/` and `proofs/` directories | Canonical validator pending; current tree check is ad hoc |
| **DSET-TEST-GOV-007** | DSET-REQUIREMENT-GOV-007 | Reject executable-enforcement claims while the selected profile or canonical command is pending | Canonical validator pending; current metadata review is manual |
| **DSET-TEST-GOV-008** | DSET-REQUIREMENT-GOV-008 | Materialize every fixture case and compare pass/fail results with expected diagnostic codes | `python -m unittest tests.test_fixtures` |
| **DSET-TEST-GOV-009** | DSET-REQUIREMENT-GOV-009, DSET-REQUIREMENT-GOV-012 | Accept unique valid governed areas and reject missing hubs, duplicate roots, unresolved parents, and parent cycles with stable diagnostics | `python -m unittest tests.test_artifact_profile` |
| **DSET-TEST-GOV-010** | DSET-REQUIREMENT-GOV-009, DSET-REQUIREMENT-GOV-013 | Assert the root README links every registered top-level area hub and every hub contains Purpose, Boundaries, and Start here/Navigation | `python -m unittest tests.test_artifact_profile` |
| **DSET-TEST-GOV-011** | DSET-REQUIREMENT-GOV-010, DSET-REQUIREMENT-GOV-011 | Assert the released artifact-type catalog and universal plus specification-specific authoring rules exist and remain linked from the documentation hub | `python -m dset_toolchain check .` plus artifact review |
| **DSET-TEST-GOV-012** | DSET-REQUIREMENT-GOV-012 | Parse `dset/scopes/gov/artifacts.yaml` and its schema; prove diagnostics DSET-E120–123 through valid and invalid registry cases | `python -m unittest tests.test_artifact_profile` |
| **DSET-TEST-GOV-013** | DSET-REQUIREMENT-META-006, DSET-REQUIREMENT-GOV-009, DSET-REQUIREMENT-GOV-010, DSET-REQUIREMENT-GOV-011, DSET-REQUIREMENT-GOV-012, DSET-REQUIREMENT-GOV-013, DSET-INVARIANT-GOV-004, DSET-INVARIANT-GOV-005 | Run the selected Python and documentation profiles together with portability, trace freshness, and diff hygiene | `uv run dset verify .` |
| **DSET-TEST-GOV-014** | DSET-REQUIREMENT-GOV-014, DSET-INVARIANT-GOV-006 | Prove materialized local rules resolve without consulting a changed source template and reject normative paths outside the adopter root | `python -m unittest tests.test_governance` |
| **DSET-TEST-GOV-015** | DSET-REQUIREMENT-GOV-015, DSET-INVARIANT-GOV-007 | Assert stable diagnostics for missing, duplicate, cyclic, outside-root, and profile-incompatible selected owners while accepting justified non-applicability | Governance failure-matrix and non-applicability tests |
| **DSET-TEST-GOV-016** | DSET-REQUIREMENT-GOV-016, DSET-INVARIANT-GOV-008 | Assert a local normative edit changes ruleset status to custom while preserving source profile/version provenance | Governance customization test |
| **DSET-TEST-GOV-017** | DSET-REQUIREMENT-GOV-017, DSET-INVARIANT-GOV-009 | Reject zero or multiple editable owners for a selected normative rule ID and reject normative rule bodies in declared derived surfaces | Governance ownership fixtures, thin-wrapper audit, and change rule inventory |
| **DSET-TEST-GOV-018** | DSET-REQUIREMENT-GOV-018, DSET-INVARIANT-GOV-010 | Classify representative defects, gaps, debt, risks, optional improvements, uncertainties, tasks, Decisions, Changes, GitHub Issues, and Jira tickets as problems/opportunities/questions or non-intake artifacts/representations | Work-routing fixture matrix |
| **DSET-TEST-GOV-019** | DSET-REQUIREMENT-GOV-019, DSET-INVARIANT-GOV-011 | Validate the one-owner intake registry, the `DSET` project prefix, full types, optional semantic layer, project-wide layer omission, full `DECISION` IDs, and independent per-type/layer numbering | Intake schema and ID-grammar fixture matrix |
| **DSET-TEST-GOV-020** | DSET-REQUIREMENT-GOV-020 | Verify artifact-governance docs define evergreen, transactional, and implementation-layer authority classes without making generated views authoritative | Documentation/gov link and text audit |
| **DSET-TEST-GOV-021** | DSET-REQUIREMENT-GOV-021 | Verify every accepted Decision added by this Change names the evergreen artifacts that compile its normative consequences | Change artifact audit |
| **DSET-TEST-GOV-022** | DSET-REQUIREMENT-GOV-022 | Verify the active Change and new atomic artifacts carry `llm_session_ids`, and the implementing commit body names the Decision it implements | Change manifest/schema audit plus commit-message review |
| **DSET-TEST-GOV-023** | DSET-REQUIREMENT-GOV-023, DSET-INVARIANT-GOV-012 | Materialize governance registry schema 1.1, require separate `depends_on` and `precedence_over` lists, and reject missing precedence owners or precedence cycles with stable `DSET-E150` diagnostics | `python -m unittest tests.test_governance` |

## Regression policy

Every accepted defect adds a deterministic regression test in its owning layer before the repair is archived.
