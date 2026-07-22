# Decision — Govern releases through Version Targets and a next-minor Roadmap

- **Decision ID:** `DSET-DECISION-OPS-001`
- **Status:** accepted
- **Decision date:** 2026-07-20
- **Resolves Question:** `DSET-QUESTION-GOV-003`
- **Absorbs:** none
- **Priority:** unknown pending the registered core-v1 scale
- **Selected option:** use Release lifecycle as the umbrella; define Version
  Target, Roadmap, Release Plan, Readiness Record, Release Notes, and
  Publication Record as distinct artifact roles; require a version-target
  catalog and a roadmap to the next minor version for release-applicable
  projects
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Context

DSET already governs release transitions and publication, but it does not
separate the long-range meaning of version lines from the executable plan to
the next minor release. The current `0.3` TODO combines target definition,
backlog, implementation sequence, and historical progress. That makes it hard
to answer two simple questions independently:

1. What must `0.3`, `0.4`, `0.5`, or `1.0` mean?
2. What work should happen now to reach the next minor release?

“Release artifacts” is not an adequate umbrella because software ecosystems
commonly use that phrase for distributable packages, binaries, images, and
archives.

## Canonical Release lifecycle roles

| Role | Owning question |
|---|---|
| **Version Target** | What state and exit criteria does this version line promise? |
| **Roadmap** | What is the current dependency-aware route from the published baseline to the next minor version? |
| **Release Plan** | Which exact Changes and version transition belong to one release transaction? |
| **Readiness Record** | Which gates, blockers, and evidence determine whether that release may proceed? |
| **Release Notes** | What user-visible behavior, compatibility, migration, or correction changed? |
| **Publication Record** | Which protected merge SHA, tag, package, and forge release prove publication? |

These are artifact and lifecycle roles, not semantic Types. They compile and
connect Decision, Question, Problem, QA, Change, implementation, evidence, and
hosted state without replacing any canonical owner.

“Milestone” remains an accepted conversational alias for Version Target, but
the canonical term is **Version Target** because it states that a version has a
defined target state rather than merely a date or issue-tracker bucket.

## Version Target contract

A release-applicable project maintains one evergreen catalog of declared
Version Targets. Each declared target records:

- version line and intended first release identity;
- concise theme and promised target state;
- required Outcomes, capabilities, compatibility, and proof/exit criteria;
- explicit exclusions or deferred scope;
- dependencies and current planning status; and
- links to the active Decisions, Requirements, Contracts, Questions, Problems,
  and evidence that own its claims.

The catalog is a compiled planning view, not authority. A target changes only
because a new Decision changes its owning claims. Before publication the
catalog may be recompiled. At publication, the exact target/readiness snapshot
becomes immutable release evidence; later corrections use a higher version and
retain the historical snapshot.

Projects must not invent placeholder targets for every intermediate number.
Undeclared version lines remain undeclared until operator authority gives them
meaning. Dates are optional and never substitute for exit criteria.

## Roadmap contract

A release-applicable project maintains one evergreen Roadmap for exactly one
next minor version. It records:

- current published baseline and next-minor target;
- target Version Target link;
- dependency-ordered workstreams and completion conditions;
- links to owning Problems, Questions, Decisions, Requirements, QA, Changes,
  and tasks rather than copied obligations;
- proof, migration, supportability, and release-readiness obligations; and
- explicit exclusions and replan triggers.

The Roadmap is a mutable projection of current truth and does not authorize
work or redefine a Version Target. Small patch releases may deliver corrections
or internal progress toward the same next minor target. After the target minor
is published, the project snapshots the completed Roadmap as release evidence
and creates a new Roadmap for the next declared minor target.

## DSET project Version Targets

| Version line | Target state |
|---|---|
| **0.3** | Public framework foundation: repository-local governance, layered self-hosting structure, executable Python toolchain, thin skill distribution, and explicit gaps without an end-user adoption-readiness claim. The published baseline is `0.3.1`. |
| **0.4** | Complete self-hosted core vertical cut: the accepted flat Type model, lifecycle/provenance, project overview, external-review flow, host/runtime bridge, cross-platform gates, and protected release path work end to end on this repository with current proof. |
| **0.5** | First adopter-ready release: language/profile extension including JavaScript/TypeScript, a real Obsidian Your Harness pilot, reusable migration/distribution guidance, and cross-project proof that local governance remains isolated. |
| **1.0** | Fully working stable framework: declared public scope is feature-complete, self-hosted, documented, supportable, migration-ready, tested, evaluated, piloted, distributable, and free of known release blockers before RC/final promotion. |

Version lines between `0.5` and `1.0` are intentionally undeclared. They must
not be filled with speculative promises merely to make a continuous list.

## Consequences

- `DSET-RULE-RELEASE` must own these role boundaries and stop when a
  release-applicable project has no target catalog, has more than one active
  next-minor Roadmap, or lets either view contradict its canonical owners.
- DSET templates must seed a Version Target catalog and next-minor Roadmap
  without hard-coding this repository's product targets into adopters.
- This repository must publish its own catalog and a Roadmap from `0.3.1` to
  `0.4.0` under the OPS scope.
- The existing DSET 0.3 TODO remains historical/current work detail until its
  still-applicable items are linked into the new Roadmap; it is not the
  canonical owner of what future version lines mean.
- Generation and runtime enforcement may be added later. The first vertical
  implementation is repository-owned documents, templates, specifications,
  deterministic structural checks, and qualitative usefulness criteria.

## Rationale

Version Target and Roadmap have different change cadences and questions. A
stable target prevents scope meaning from drifting with task order; a mutable
next-minor Roadmap permits replanning without silently redefining the release.
Keeping release planning as roles instead of Types preserves the four-Type
semantic model and lets every plan line return to its real authority, work, or
evidence owner.

## Lifecycle policy at emission

- **Expected confirmation evidence:** a cold reader can distinguish target
  meaning, current route, exact release scope, readiness, notes, and publication
  identity and can return every claim to its canonical owner
- **Known counter-evidence:** no schema or CLI currently enforces one target
  catalog and one active next-minor Roadmap
- **Reopen when:** adopters cannot plan patch work toward a minor target without
  duplicating authority, or Version Target and Roadmap repeatedly fail to
  separate stable intent from mutable sequencing
- **If reopened, retain:** targets do not become deadlines by default, Roadmaps
  do not authorize work, published snapshots remain immutable evidence, and
  `1.0` remains readiness-gated rather than arithmetic
- **Retirement condition:** an accepted successor absorbs every active claim

This emitted Decision atom is immutable. Any later correction, status change,
counter-evidence, absorption, or retirement must be a new atom or append-only
lifecycle event.
