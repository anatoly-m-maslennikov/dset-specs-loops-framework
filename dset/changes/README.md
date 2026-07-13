# Changes

Each direct child except `archive/` is one bounded, active change. A standard change contains eight document artifacts plus requirement deltas and optional proof-of-fit evidence:

```text
<change-id>/
├── proposal.md
├── specs/
├── test-plan.md
├── eval-plan.md
├── solution-landscape.md
├── proofs/
├── design.md
├── implementation-plan.md
├── tasks.md
└── verification.md
```

The eight document artifacts are proposal, test plan, eval plan, solution landscape, design, implementation plan, tasks, and verification. `specs/` owns requirement deltas; `proofs/` owns bounded, redacted evidence; `verification.md` owns conclusions and links to that evidence. Raw generated output remains ephemeral unless a concise excerpt is required to diagnose a failure.

Active changes may contain implementation evidence but do not own accepted project truth. Failed or incomplete changes stay here. After deltas are reconciled and baseline verification is fresh, a change may move to a dated archive candidate on its still-draft PR branch so remote checks can inspect the real path and head. The candidate remains unaccepted and explicitly incomplete until final evidence and archive readiness are recorded.
