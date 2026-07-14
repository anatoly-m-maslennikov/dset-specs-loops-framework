# Verification — Make DSET self-hosting and skills thin

- **Implementing PR:** pending
- **Status:** invariant contract in progress; 0.2 mechanics not implemented

| Gate | Command or method | Result | Evidence |
|---|---|---|---|
| Deterministic contract checks | `python -m dset_toolchain check .` and `git diff --check` | Pending after accepted-truth reconciliation | `proofs/` |
| Planned 0.2 mechanics | MDSHAST-TEST-001–007/009 | Not implemented; must remain planned | [Test plan](test-plan.md) |
| Applicable evals | MDSHAST-EVAL-001–004 | Planned for implemented wrappers/resolver | [Eval plan](eval-plan.md) |
| Supportability | Existing repository delivery contract | Applicable; no runtime surface added | [Delivery runbook](../../supportability/delivery-runbook.md) |
| Reconciliation/archive | Accepted invariant/package diff and later `dset verify` | In progress; archive not eligible | This file and future proof evidence |

Record fresh commands, exit status, bounded summaries, unresolved failures, and the completion disposition. Never persist secrets or sensitive raw output.
