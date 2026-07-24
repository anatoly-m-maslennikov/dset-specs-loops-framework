---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-065"
scope_path:
  - "layer:gov"
priority: "high"
promotion:
  affected_children:
    - "governance"
    - "tool"
    - "skill"
    - "implementation"
    - "ops"
  applies_unchanged: false
  local_context_required: true
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Requirement — Require Git and commit coverage

Git is mandatory for every DSET-managed project.

`dset-init` must:

1. fail clearly when Git is unavailable;
2. use an enclosing Git repository when the selected project is a monorepo
   work area rather than creating a nested repository;
3. initialize Git when no enclosing repository exists and initialization is
   authorized;
4. stage only files created or intentionally changed by the DSET transaction;
5. create a commit for the executed initialization; and
6. stop with recovery instructions when author identity or another Git
   prerequisite prevents the commit.

Implementation has commit-coverage invariants:

- every implemented Decision has at least one commit naming it with
  `Implements:`;
- every fixed Problem has at least one commit naming it with `Resolves:`;
- a correction that changes governed behavior also names its authorizing
  Decision;
- every such commit carries the required `Session:` provenance; and
- a workflow cannot report implementation or resolution complete while the
  relevant changes remain uncommitted.

One commit may cover multiple Decisions or Problems only when the delivered
change is technically indivisible and names every covered artifact. The
coverage rule does not require empty or artificial commits and does not permit
one unrelated catch-all commit.

## Primary claim

Every DSET-managed project uses Git, dset-init requires an existing enclosing repository or initializes one, and every implemented Decision or resolved Problem has at least one committed change that names the governed artifact.

## Rationale

Development without versioned history makes rollback, review, provenance, bisecting, and support investigation unreliable. Commit coverage connects each delivered behavior or correction to its governing reason without forcing unrelated work into one commit.
