# DSET workflow skills

## Purpose

This is the hub for thin DSET workflow wrappers. These repository-native sources are portable release artifacts; installed copies are distributions and must match their registered source identity.

## Boundaries

Skills own discovery, workflow identity, resolver invocation, rule-set reporting, authorization handoff, and fail-closed behavior. Repository-local governing documents own the substantive procedure and project rules. A skill never falls back to embedded prose or remote framework text.

## Start here

- [`dset`](dset/SKILL.md) — inspect repository state, recommend one governed lifecycle mode, and hand off at the next authorization boundary.
- [`dset-clarify`](dset-clarify/SKILL.md) — resolve domain ambiguity and proof obligations before specification acceptance.
- [`dset-diagnose`](dset-diagnose/SKILL.md) — investigate defects and incidents through evidence and Back-to-Left provenance without silently authorizing a fix.
- [`dset-prototype`](dset-prototype/SKILL.md) — run bounded disposable design experiments and feed evidence into the Solution Landscape and Decision.
- [`dset-release`](dset-release/SKILL.md) — prepare or verify a release and publish only under separate explicit authority.

These five repository-native wrappers are the implemented source skill surface.
The primary orchestrator owns the internal session checkpoint/resume boundary;
it is not a sixth public skill. Wrapper availability does not claim the still
separately gated runtime adapter, release publisher, declared-host installation
proof, or cross-platform execution proof is complete.

Each folder contains a concise `SKILL.md` and generated `agents/openai.yaml`. Resolve its workflow with `dset rules resolve <workflow-id>` before acting. No skill depends on private memory, machine-specific paths, shell-only behavior, or a parallel specification format.
