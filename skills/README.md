# DSET workflow skills

## Purpose

This is the hub for thin DSET workflow wrappers. These repository-native sources are portable release artifacts; installed copies are distributions and must match their registered source identity.

## Boundaries

Skills own discovery, workflow identity, resolver invocation, rule-set reporting, authorization handoff, and fail-closed behavior. Repository-local governing documents own the substantive procedure and project rules. A skill never falls back to embedded prose or remote framework text.

The reusable `SKILL.md` core is LLM-provider agnostic. Codex metadata,
host-native discovery, installation, and invocation are adapters with separate
compatibility claims. The current distribution implements Codex and Claude
adapters only; Grok, Chinese model providers, and other hosts are neither
excluded by the core nor claimed without their own adapter and Evaluation
evidence.

The same installed skill packages serve every DSET project. Each invocation
starts from its explicit target, discovers exactly one owning DSET root, and
resolves that project's local governance layer. Moving to another project
changes the registry, rules, and ruleset identity—not the skill package—and no
project policy is retained or copied across that boundary.

## Navigation

### Base operator surface

- [`dset`](dset/SKILL.md) — route a general or uncertain request to one governed mode and specialist handoff.
- [`dset-init`](dset-init/SKILL.md) — preview and, only when authorized, initialize a repository or monorepo Work Area.
- [`dset-implement`](dset-implement/SKILL.md) — follows the repository's documented `workflows.implement.mode`: lazy preparation closes only governed missing criteria, while strict is implementation-only and stops on insufficient inputs.
- [`dset-verify`](dset-verify/SKILL.md) — check implementation and governance against accepted truth and proof plans.
- [`dset-overview`](dset-overview/SKILL.md) — show current artifacts, coverage, freshness, and open obligations without changing the repository.
- [`dset-release`](dset-release/SKILL.md) — prepare or verify a release and publish only under separate explicit authority.

### Direct and advanced entries

- [`dset-repair-governance`](dset-repair-governance/SKILL.md) — diagnose invalid local governance and stop with a repair handoff.
- [`dset-decompose`](dset-decompose/SKILL.md) — establish bounded Work Area and Change seams.
- [`dset-clarify`](dset-clarify/SKILL.md) — resolve domain ambiguity and proof obligations before specification acceptance.
- [`dset-diagnose`](dset-diagnose/SKILL.md) — investigate defects and incidents through evidence and Back-to-Left provenance without silently authorizing a fix.
- [`dset-landscape`](dset-landscape/SKILL.md) — compare solution, library, framework, architecture, and language alternatives.
- [`dset-prototype`](dset-prototype/SKILL.md) — run bounded disposable design experiments and feed evidence into the Solution Landscape and Decision.
- [`dset-decisions`](dset-decisions/SKILL.md) — reconcile accepted session intent into immutable atomic records and compiled handoffs.
- [`dset-compile`](dset-compile/SKILL.md) — semantically synthesize pending accepted atoms into only the affected evergreen specifications and plans when compilation is requested or required by an entry gate.
- [`dset-plan-proof`](dset-plan-proof/SKILL.md) — maintain separate deterministic test and qualitative eval plans.
- [`dset-plan-implementation`](dset-plan-implementation/SKILL.md) — create dependency-ordered implementation work and Change tasks.
- [`dset-triage`](dset-triage/SKILL.md) — classify and route Questions, including Conflicts and Opportunities, and Problems.
- [`dset-complete`](dset-complete/SKILL.md) — confirm terminal state and report residual obligations without inventing work.

The base skills accept desired outcomes. `dset` routes an uncertain request to
one next mode and handoff; it does not execute the selected specialist.
Specialist entrypoints may traverse only their registered prerequisite closure,
notably the lazy `dset-implement` workflow. These 18 folders are the exact
implemented source catalog. Sixteen wrappers
resolve repository-local workflows; `dset-init` and
`dset-repair-governance` are the only bounded pre-resolution exceptions. The
primary router owns the shared session checkpoint/resume boundary; there
is no separate session-management skill. Source availability does not prove a
real host invocation, release publication, or cross-platform execution until
those separate gates pass.

Each folder contains a concise `SKILL.md` and generated `agents/openai.yaml`.
Governed wrappers resolve their registered workflow before acting; the two
exceptions use only their declared bootstrap/diagnostic transaction. No skill
depends on private memory, machine-specific paths, shell-only behavior, or a
parallel specification format.

Every created or updated skill must pass `agent-skills-v1` before installation
or distribution:

```text
python -m dset_toolchain skills audit --source skills
```

The gate validates all 18 package shapes and the 54-case minimum trigger,
non-trigger, and ambiguous-routing catalog. Provider/host/model execution
remains a separate qualitative Evaluation; a clean static audit is not host
invocation proof.

Use the [host-distribution workflow](host-distribution.md) to preview or apply
copy-based Codex and Claude installations. One transaction installs all thin
wrappers plus the shared runtime under the host's `packages/dset` root, verifies
their identities, and can validate a bounded receipt from a representative
host invocation.
