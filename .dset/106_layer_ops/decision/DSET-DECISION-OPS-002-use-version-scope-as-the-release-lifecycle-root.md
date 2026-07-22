# Decision — Use Version Scope as the Release lifecycle root

- **Decision ID:** `DSET-DECISION-OPS-002`
- **Status:** accepted
- **Decision date:** 2026-07-20
- **Resolves Question:** follow-up operator clarification of
  `DSET-QUESTION-GOV-003`
- **Absorbs:** `DSET-DECISION-OPS-001` in full
- **Replaces claims:** “Version Target” is replaced by **Version Scope** as the
  canonical root artifact role; Milestone becomes a bounded Roadmap checkpoint
  rather than the definition of a version line
- **Priority:** unknown pending the registered core-v1 scale
- **Selected option:** organize Release lifecycle artifacts beneath one Version
  Scope per declared version line, with Roadmap and Release Plan as its primary
  children and Milestones, Readiness Record, Release Notes, and Publication
  Record in their bounded roles
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Canonical hierarchy

```text
Version Scope
├── Roadmap
│   └── Milestones
└── Release Plan
    ├── Readiness Record
    ├── Release Notes
    └── Publication Record
```

These names are artifact roles/kinds, not additions to the four DSET semantic
Types. Their authoritative inputs remain Decision atoms and direct subtypes;
their work and evidence remain separate.

## Version Scope

Version Scope is the mandatory root for a declared release line such as `0.3`,
`0.4`, `0.5`, or `1.0`. It answers what the line promises and excludes, not
when it will ship. It records:

- version line and intended initial release;
- purpose and promised target state;
- required Outcomes, capabilities, compatibility, and exit criteria;
- explicit non-goals and deferred scope;
- proof, supportability, migration, and adoption obligations; and
- links to the active Decisions, Requirements, Contracts, Questions, Problems,
  and evidence that own each claim.

Version Scope is an evergreen compiled projection before publication. A new
Decision is required to change its governing claims. The exact scope/readiness
snapshot attached to a published release becomes immutable release evidence.
Patch releases remain inside the current minor Version Scope unless a new
Decision explicitly changes the public scope and the release policy classifies
that change accordingly.

Projects declare only meaningful version lines. They must not invent empty
`0.6`, `0.7`, and similar scopes merely to fill a sequence. Dates are optional
and never replace exit criteria.

## Roadmap and Milestones

One active Roadmap connects the current published baseline to exactly one next
minor Version Scope. It is a mutable, dependency-aware projection of current
work and links canonical owners instead of copying their obligations.

A Milestone is an optional bounded checkpoint inside that Roadmap. It has a
completion condition and applicable proof, but it neither defines the meaning
of the version nor authorizes work. Completing a Milestone does not by itself
prove an Outcome or release readiness.

After the target minor release is published, its Roadmap and achieved
Milestone state are snapshotted as release evidence and a new Roadmap is
created for the next declared minor Version Scope.

## Exact-release artifacts

A Release Plan selects the exact version transition and participating Changes
for one release instance such as `0.4.0` or `0.4.1`. Its children remain
separate:

- Readiness Record owns gates, blockers, applicability, and evidence;
- Release Notes own user-visible changes and migration information; and
- Publication Record owns the protected merge SHA, tag, package, and forge
  release identity.

An exact release references one Version Scope. These artifacts cannot widen
that scope without a new governing Decision and recompiled Version Scope.

## DSET project scopes

This Decision retains the project target states accepted in
`DSET-DECISION-OPS-001`, now as Version Scopes:

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

“Version Target” describes intent but does not expose the controlling boundary.
“Version Scope” is clearer: it defines what belongs to a version line and what
does not. It also distinguishes the stable meaning of `0.4` from Roadmap
sequencing, Milestone checkpoints, and one exact `0.4.x` release transaction.

## Lifecycle policy at emission

- **Expected confirmation evidence:** a cold reader starts from one Version
  Scope and can distinguish its Roadmap, Milestones, exact Release Plan,
  readiness, notes, and publication identity
- **Known counter-evidence:** schema, initializer, validator, overview, and
  release CLI enforcement remain open under `DSET-PROBLEM-OPS-002`
- **Reopen when:** a project cannot represent a minor line and its patch
  releases without duplicating scope authority or confusing Roadmap checkpoints
  with release readiness
- **If reopened, retain:** Release lifecycle roles do not become semantic Types,
  published evidence is immutable, and `1.0` remains readiness-gated
- **Retirement condition:** an accepted successor absorbs every active claim

This emitted Decision atom is immutable. Any later correction, status change,
counter-evidence, absorption, or retirement must be a new atom or append-only
lifecycle event.
