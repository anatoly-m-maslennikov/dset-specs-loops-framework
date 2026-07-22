---
name: dset-compile
description: Semantically reconcile accepted atomic DSET artifacts into affected evergreen specifications and plans under the target repository's local governance. Use when the operator requests compilation, pending atoms must become current project truth, or implementation, verification, or release entry criteria require current evergreen artifacts; do not run merely because one new atom exists.
---

# DSET Compile

This is the thin wrapper for semantic compilation. Repository-local governance
owns the substantive compilation and authoring rules.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context
   --skill dset-compile --target TARGET --objective OBJECTIVE
   --llm-session-id LLM_SESSION_ID [--session-id SESSION_ID]`. Reuse an active
   DSET session ID. Stop if the runtime, target, identity, or governed workflow
   is unavailable.
2. Verify the returned repository/Work Area, `compile` workflow, ordered rule
   identities and digests, ruleset identity, conflict coverage, and run/session
   identity.
3. Read the returned project-owned rules in order. Stop on an identity mismatch,
   unresolved governing conflict, or a returned stop status.

## Compile

1. Inventory accepted atomic artifacts beyond each affected evergreen owner's
   recorded frontier. Do not treat a new atom as an automatic compilation
   trigger.
2. Resolve `replacement_of`, `override_of`, `child_of`, conflict resolution,
   and lifecycle state before synthesis. Never edit an atomic artifact.
3. Update only affected evergreen specifications or plans. Synthesize current
   consequences in the target document's vocabulary and structure; do not
   concatenate atom text or expose a chronological decision log.
4. If a project reference still exactly matches distributable framework truth,
   retain its portable TOML reference. If the project consequence diverges,
   replace the reference with a project-owned evergreen document.
5. Record the considered atomic frontier by scope and semantic type. A frontier
   marks considered inputs, not proof that the synthesis is correct.
6. Report updated owners, unchanged owners, pending atoms, conflicts, material
   unknowns, and session provenance. Stop before implementation, testing,
   evaluation, or release work unless the caller separately requested it.

## Continuity

For a chained workflow, hand off the active run with `dset runtime handoff
RUN_ID REPOSITORY_ROOT --next-signal WORKFLOW` and preserve the same session ID.
Only terminal completion or a governed stop invokes `dset runtime finish`.
