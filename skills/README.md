# DSET workflow skills

## Purpose

This is the hub for thin DSET workflow wrappers. These repository-native sources are portable release artifacts; installed copies are distributions and must match their registered source identity.

## Boundaries

Skills own discovery, workflow identity, resolver invocation, rule-set reporting, authorization handoff, and fail-closed behavior. Repository-local governing documents own the substantive procedure and project rules. A skill never falls back to embedded prose or remote framework text.

## Start here

- [`dset-clarify`](dset-clarify/SKILL.md) — resolve domain ambiguity and proof obligations before specification acceptance.
- [`dset-diagnose`](dset-diagnose/SKILL.md) — investigate defects and incidents through evidence and Back-to-Left provenance without silently authorizing a fix.
- [`dset-prototype`](dset-prototype/SKILL.md) — run bounded disposable design experiments and feed evidence into the Solution Landscape and Decision.

These three specialists are the currently implemented skill surface. The active
DSET 0.3 Change specifies, but does not yet release, the primary `dset`
orchestrator and guarded `dset-release` specialist. The primary orchestrator
also owns the internal session checkpoint/resume capability; it is not a sixth
public skill. No README or accepted
contract should present those two source directories as implemented before
their wrappers, registry entries, tests, and evals pass.

Each folder contains a concise `SKILL.md` and generated `agents/openai.yaml`. Resolve its workflow with `dset rules resolve <workflow-id>` before acting. No skill depends on private memory, machine-specific paths, shell-only behavior, or a parallel specification format.
