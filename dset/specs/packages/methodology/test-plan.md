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
| **METH-TEST-006** | METH-REQ-006 | Validate PR identity, fresh verification, reconciliation, archive path, later-change invalidation, and draft-until-ready state before archival | Canonical validator pending; manual archive audit required under the pending profile |
| **METH-TEST-007** | METH-REQ-007, METH-INV-005 | Resolve all local Markdown links, balance code fences/details blocks, and reject wiki links or Obsidian callouts | Canonical validator pending; current check is ad hoc |
| **METH-TEST-008** | All | Reject whitespace errors in the proposed diff | `git diff --check` |
| **METH-TEST-009** | METH-REQ-008 | Assert committed project truth uses visible `dset/` and no competing `.dset/` truth exists | Canonical validator pending; current tree check is ad hoc |
| **METH-TEST-010** | METH-REQ-009 | Parse the manifest; assert every package is unique and the global root matches current cross-package ownership | Canonical validator pending; current `yq` check is ad hoc |
| **METH-TEST-011** | METH-REQ-010 | Assert a standard change has the eight named documents plus separate `specs/` and `proofs/` directories | Canonical validator pending; current tree check is ad hoc |
| **METH-TEST-012** | METH-REQ-011 | Reject executable-enforcement claims while the selected profile or canonical command is pending | Canonical validator pending; current metadata review is manual |

## Regression policy

Every documentation defect fixed after this baseline must add or extend a deterministic check when machine detection is feasible. A check first demonstrates failure against the defective revision, then passes against the correction.
