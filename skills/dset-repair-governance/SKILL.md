---
name: dset-repair-governance
description: Diagnose an existing but invalid repository-local DSET registry without resolving substantive rules from it. Use when DSET root discovery succeeds but schema, ownership, path, digest, applicability, or conflict validation fails; return stable diagnostics and a bounded repair handoff, then stop before any write.
---

# DSET Repair Governance

This is the diagnostic pre-resolution exception. Invalid local governance never falls back to installed templates, memory, or remote framework prose.

## Diagnose

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-repair-governance --target TARGET --objective OBJECTIVE --llm-session-id LLM_SESSION_ID`. Replace the placeholder with the current host session ID. Require `status: invalid-governance`; stop on an unavailable ID/launcher, no root, competing roots, valid governance, or command failure.
2. Report every returned stable schema, ownership, path, digest, applicability, and conflict diagnostic with its local file identity and proposed repair owner.
3. Preserve the invalid repository as evidence. Do not resolve substantive rules, copy template content, select project policy, or mutate the registry under this invocation.

## Stop

Return diagnostics, proposed local paths, available session identity, and a separately authorizable repair handoff. Stop before any write or governed project workflow.
