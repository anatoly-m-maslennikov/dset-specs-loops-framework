# Decision — Use five flat Release lifecycle artifacts

- **Decision ID:** `DSET-DECISION-OPS-004`
- **Status:** accepted
- **Decision date:** 2026-07-20
- **Absorbs:** `DSET-DECISION-OPS-003` in full
- **Replaces claims:** Milestone is a Roadmap entry rather than an artifact;
  Release Notes and Publication Record are combined as Release Record
- **Priority:** unknown pending the registered core-v1 scale
- **Selected option:** use five flat Release lifecycle artifact roles connected
  by typed references
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Canonical artifact roles

The Release lifecycle uses five peer artifact roles:

- **Version Scope** defines the promises, exclusions, and exit criteria for one
  declared version line such as `0.4`.
- **Roadmap** orders the mutable route from a published baseline to exactly one
  next-minor Version Scope. Milestones are structured checkpoint entries inside
  the Roadmap, not separate artifacts.
- **Release Plan** selects one exact release transition, such as `0.4.0`, and
  the Changes proposed for it.
- **Readiness Record** records gate applicability, results, blockers, and
  evidence for one exact release candidate.
- **Release Record** immutably records what an exact release delivered and
  where it was published, including its user-visible summary, migration notes,
  protected merge SHA, tag, packages, and forge release identity.

No role contains, owns, subclasses, or is the base Type of another. Version
Scope is the shared scope anchor, not a root or base artifact. Other applicable
Release lifecycle artifacts reference its stable identity through
`version_scope_ref`.

These roles are not additions to the four DSET semantic Types. Their authority
comes from Decision atoms and direct Decision subtypes, and their workflow
position never determines their semantic Type.

## Reference boundaries

- A Roadmap references one next-minor Version Scope.
- A milestone entry belongs to one Roadmap and carries a local identifier,
  completion condition, dependencies, and evidence links when achieved.
- A Release Plan references one Version Scope and one exact proposed version.
- A Readiness Record references one Release Plan, its Version Scope, and the
  exact candidate commit.
- A Release Record references the accepted Readiness Record, Release Plan,
  Version Scope, and exact protected merge commit.

Each artifact owns one primary claim and links canonical work owners rather
than copying their obligations. Release Notes rendered on a forge or package
registry are mirrors of the Release Record, not another canonical artifact.

## Lifecycle policy

A Version Scope is evergreen while its line is being planned. Changing a
governing claim requires a new Decision and recompilation. The exact scope
snapshot used by a published release becomes immutable evidence.

One active Roadmap targets exactly one next minor. Completing its work or a
milestone entry does not itself prove an Outcome or release readiness.

A Release Plan and Readiness Record are evergreen during preparation, subject
to their governing Decisions and candidate rules. The Release Record is emitted
only after publication and is immutable. A correction is a new release and a
new Release Record.

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

A milestone has no independent authority outside the Roadmap that defines its
sequence and completion condition, so a separate artifact adds identity without
adding a primary claim. Release Notes and publication identity describe two
facets of one historical fact: what exact version was published. Keeping them
in one Release Record reduces drift between public explanation and operational
evidence while preserving a single immutable release history.

## Lifecycle policy at emission

- **Expected confirmation evidence:** a cold reader can distinguish the five
  roles, find milestone entries within a Roadmap, and recover both release
  content and publication identity from one Release Record
- **Known counter-evidence:** schema, initializer, validator, overview, and
  release CLI enforcement remain open under `DSET-PROBLEM-OPS-002`
- **Reopen when:** a Release Record cannot remain one coherent historical claim
  across supported publishers or a milestone requires authority outside its
  Roadmap
- **If reopened, retain:** flat roles, one primary claim per artifact, explicit
  references, and immutable published evidence
- **Retirement condition:** an accepted successor absorbs every active claim

This emitted Decision atom is immutable. Any later correction, status change,
counter-evidence, absorption, or retirement must be a new atom or append-only
lifecycle event.
