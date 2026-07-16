# Decision — Expose every DSET lifecycle mode as a public skill

- **Decision ID:** `DSET-DECISION-SKILL-002`
- **Status:** accepted
- **Decision date:** 2026-07-16
- **Resolves Question:** direct operator request to create all remaining DSET
  lifecycle skills
- **Absorbs:** none
- **Replaces claims:** the `DSET-DECISION-SKILL-001` claim that the public
  surface contains exactly five skills and that other lifecycle actions cannot
  have public wrappers; all other claims of that Decision remain active
- **Priority:** unknown pending the registered core-v1 scale
- **Selected option:** keep `dset` as the catch-all orchestrator and publish one
  thin direct-entry wrapper for every stable lifecycle mode
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Context and scope

The five-skill topology proved the thin-wrapper and local-rule model, but it
made direct lifecycle work depend on remembering which request must be phrased
through the general orchestrator. The operator has selected an explicit public
entrypoint for every stable mode. This is a usability and discoverability
change, not a transfer of governing behavior into skill files.

This Decision covers source packages, host distribution, adopter
materialization, lifecycle routing, documentation, and proof for the public
skill surface. It does not rename current artifact entities or split tests and
evals into competing workflows.

## Decision

DSET publishes these 16 public skills:

- `dset`, the catch-all lifecycle and next-action orchestrator;
- `dset-init` and `dset-repair-governance`, the two bounded pre-resolution
  exceptions;
- `dset-decompose`, `dset-diagnose`, `dset-clarify`, `dset-landscape`,
  `dset-prototype`, and `dset-decide`;
- `dset-plan-proof` and `dset-plan-implementation`;
- `dset-implement`, `dset-verify`, `dset-triage`, `dset-release`, and
  `dset-complete`.

Every governed direct-entry skill resolves exactly one registered local
workflow and remains a thin wrapper. `dset-init` owns only the rootless
dry-run/authorize/materialize/validate/stop transaction.
`dset-repair-governance` owns only fail-closed governance diagnostics and a
repair handoff. Neither exception may substitute embedded project rules.

`dset` remains the cheapest default entrypoint for operators who do not know
the next mode. Direct skills are optional shortcuts and explicit automation
boundaries. The orchestrator may chain them under the same transition,
authorization, session, and authoritative-state reread limits as before.

Tests and applicable evals remain separate proof plans behind
`dset-plan-proof`; Problems, Questions, Opportunities, and Conflicts keep their
current semantic types and are routed through `dset-triage`, diagnosis,
clarification, decision, implementation, or verification as their state
requires.

## Consequences and discharge

The current skill specification, lifecycle rules, governance registry,
bootstrap bundle, distribution manifest, source hub, host guide, tests, evals,
and active Change must compile this topology. Host and project materialization
must reject omissions, unexpected public skill folders, stale digests, and
wrapper/workflow mismatches.

Historical proof for the five-skill surface remains valid only for the commit
and topology it evaluated. New proof must cover all 16 source packages and all
14 repository-resolved wrappers; rootless initialization and invalid-registry
repair require their separate exception cases.

## Lifecycle policy at emission

- **Expected confirmation evidence:** static package validation, exact source
  inventory, profile registration, bootstrap regeneration, clean host-copy
  installation, adopter materialization, and representative routing cases
- **Known counter-evidence:** no current proof covers the expanded public
  surface and real host invocation remains separately pending
- **Reopen when:** operators cannot reliably distinguish the direct triggers,
  host discovery becomes materially worse, or maintaining explicit wrappers
  causes verified drift despite generated registry checks
- **If reopened, retain:** thin wrappers, repository-local rule ownership,
  `dset` as the catch-all entrypoint, stop boundaries, and the two bounded
  pre-resolution exceptions
- **Retirement condition:** a validated successor explicitly replaces every
  active topology claim and all current projections stop relying on this
  Decision

This emitted Decision atom is immutable. Any later status change, correction,
counter-evidence, absorption, or retirement must be a new append-only lifecycle
event or successor atom.
