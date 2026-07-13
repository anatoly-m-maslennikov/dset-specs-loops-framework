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

The eight document artifacts are proposal, test plan, eval plan, solution landscape, design, implementation plan, tasks, and verification. `specs/` owns requirement deltas; `proofs/` owns disposable evidence rather than another narrative artifact.

Active changes may contain implementation evidence but do not own accepted project truth. Failed or incomplete changes stay here. Do not move a change to `archive/` until its deltas are reconciled, verification is fresh, the implementing PR is recorded, and archive-readiness checks pass.
