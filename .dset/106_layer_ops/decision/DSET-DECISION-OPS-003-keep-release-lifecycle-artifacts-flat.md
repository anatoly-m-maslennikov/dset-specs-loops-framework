# Decision — Keep Release lifecycle artifacts flat

- **Decision ID:** `DSET-DECISION-OPS-003`
- **Status:** accepted
- **Decision date:** 2026-07-20
- **Absorbs:** `DSET-DECISION-OPS-002` in full
- **Replaces claims:** Release lifecycle artifacts do not form a parent/child
  hierarchy; Version Scope is a required scope anchor, not a base Type or root
  artifact
- **Priority:** unknown pending the registered core-v1 scale
- **Selected option:** define flat, independently addressable Release lifecycle
  roles connected by typed references
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Canonical flat model

The Release lifecycle uses these peer artifact roles:

- Version Scope;
- Roadmap;
- Milestone;
- Release Plan;
- Readiness Record;
- Release Notes; and
- Publication Record.

No role contains, owns, subclasses, or is the base Type of another. Each
artifact has its own identity, lifecycle, canonical claim, and direct links to
the authoritative Decision atoms and other records it uses.

Version Scope is the mandatory scope anchor for a declared release line such as
`0.3`, `0.4`, `0.5`, or `1.0`. Other applicable Release lifecycle artifacts
reference its identity through `version_scope_ref`. This reference does not
make them children of Version Scope.

These names are artifact roles, not additions to the four DSET semantic Types.
Their authority comes from Decision atoms and direct Decision subtypes. A role
must not be inferred from its workflow position.

## Role boundaries

- **Version Scope** defines the promises, exclusions, and exit criteria for one
  version line.
- **Roadmap** orders the mutable route from a published baseline to exactly one
  next-minor Version Scope.
- **Milestone** records an optional bounded checkpoint and its completion
  condition. It references a Roadmap when applicable.
- **Release Plan** selects one exact release transition and the Changes proposed
  for it.
- **Readiness Record** records gate applicability, results, blockers, and
  evidence for one exact release.
- **Release Notes** record user-visible change and migration information for one
  exact release.
- **Publication Record** records the protected merge, tag, package, and forge
  release identities for one published release.

Each role owns one primary claim. A document that needs to own claims from two
roles must be split into linked artifacts rather than represented as a compound
or nested subtype.

## Version and Roadmap policy

A Version Scope is evergreen while its version line is being planned. Changing
its governing claim requires a new Decision and recompilation. The exact scope
snapshot used for a published release becomes immutable evidence.

One active Roadmap targets exactly one next minor Version Scope. It links
canonical work owners instead of copying or authorizing their obligations.
Completing a Roadmap or Milestone does not itself prove an Outcome or release
readiness.

Patch releases normally reference the same minor Version Scope. A Decision is
required when a patch changes the public scope or compatibility promise.
Projects declare only meaningful version lines; missing intermediate lines do
not require placeholder Version Scopes.

## DSET project Version Scopes

The project target states retained from the absorbed Decisions are:

- `0.3`: public framework foundation, published baseline `0.3.1`, with gaps
  stated honestly and no end-user adoption-readiness claim;
- `0.4`: complete self-hosted core vertical cut on this repository;
- `0.5`: first adopter-ready, multi-language release with the Obsidian Your
  Harness pilot and cross-project proof; and
- `1.0`: fully working stable framework satisfying the existing RC/final
  readiness gate.

Intermediate pre-1.0 Version Scopes remain undeclared until accepted by a later
Decision.

## Rationale

A hierarchy incorrectly implies inherited authority and lifecycle. These
artifacts change at different rates, may be produced by different actors, and
must remain independently auditable. Flat roles with explicit references keep
their claims atomic while preserving navigation through the shared Version
Scope identity.

## Lifecycle policy at emission

- **Expected confirmation evidence:** a cold reader can identify each Release
  lifecycle artifact independently and follow explicit references without
  relying on folder nesting or document containment
- **Known counter-evidence:** schema, initializer, validator, overview, and
  release CLI enforcement remain open under `DSET-PROBLEM-OPS-002`
- **Reopen when:** typed references cannot represent a required Release
  lifecycle relationship without duplicating canonical authority
- **If reopened, retain:** one primary claim per artifact, roles remain separate
  from semantic Types, and published evidence remains immutable
- **Retirement condition:** an accepted successor absorbs every active claim

This emitted Decision atom is immutable. Any later correction, status change,
counter-evidence, absorption, or retirement must be a new atom or append-only
lifecycle event.
