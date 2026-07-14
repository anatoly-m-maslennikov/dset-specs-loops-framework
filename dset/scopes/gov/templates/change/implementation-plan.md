# Implementation plan — {{title}}

- **Implementing PR:** pending

## Delivery topology

- **Workspace mode (`integration-branch` default or optional `branch-worktree`):** pending
- **Integration branch:** pending
- **Release branch:** pending

Default to one Change and one review PR. The same Change may cross layers
atomically; split only independently reviewable, verifiable, and mergeable
parts. Do not create permanent layer branches.

## Batch 1 — Tracer slice

- Map tasks to requirement, test, and applicable eval IDs.
- Produce one independently verifiable vertical outcome.
- Keep build sequence and dependency ordering here rather than in Requirements
  or Decisions.

## Rollout and recovery

Define ordering, migration, feature controls, rollback, and proof refresh triggers.

For a cross-Change dependency, hand off stable IDs, exact commits or versions,
Contracts, evidence locations, currentness, and reopen triggers.
