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
| **METH-TEST-006** | METH-REQ-006 | Validate PR identity, fresh verification, archive path, and draft-until-ready fields before archival | Canonical validator pending |
| **METH-TEST-007** | METH-REQ-007, METH-INV-005 | Resolve all local Markdown links, balance code fences/details blocks, and reject wiki links or Obsidian callouts | Canonical validator pending; current check is ad hoc |
| **METH-TEST-008** | All | Reject whitespace errors in the proposed diff | `git diff --check` |

## Regression policy

Every documentation defect fixed after this baseline must add or extend a deterministic check when machine detection is feasible. A check first demonstrates failure against the defective revision, then passes against the correction.
