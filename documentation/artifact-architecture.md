# Artifact architecture

## Rule

DSET uses independent profile axes for runtime behavior, durable authority, code enforcement, and knowledge artifacts. Documentation is not a programming language, and its structural rules must not inherit Python or TypeScript tools and thresholds.

## Orthogonal selections

| Axis | Governing question | Example selections |
|---|---|---|
| Runtime risk | Which recovery, safety, and supportability semantics are required? | transient/local, stateful/retryable, distributed/high-risk |
| Durability topology | Which system owns persistent state? | local files, local database, external backing service/platform |
| Implementation language | Which code tools, scopes, and thresholds enforce the build? | `python-v1`, future `typescript-v1`, not applicable |
| Artifact governance | Which document types, ownership rules, hubs, and authoring gates apply? | `documentation-v1`, future domain-specific artifact profiles |

A project selects each applicable axis explicitly. Selecting `documentation-v1` does not imply that the project is documentation-only; selecting `python-v1` does not govern prose.

## Artifact classification and navigation

Every governed carrier has one primary artifact type from the project-local
MECE registry. Atomic Record, Analysis Report, Specification, Procedure, Plan,
Change, Implementation, Evidence Record, Verification, Readiness Record,
Release Record, Derived View, and Navigation cover the development lifecycle
without changing the four semantic Types—Decision, Question, Problem, and QA.

Artifact type answers what job the carrier performs. Semantic Type answers what
an Atomic Record means. Workflow, queue, skill, tool, host, filename, folder,
and intended next action determine neither axis. Direct metadata or exactly one
registered path rule supplies artifact classification; ambiguity fails closed.

Base artifact IDs and filenames expose the primary artifact type, not its
optional subtype. The subtype remains direct metadata. Root `dset.toml` exposes
independent optional capabilities; setting
`artifact_subtype_in_names = true` opts only newly emitted artifacts into
subtype-bearing names and never rewrites stable history.

An active applicable source atom wins when its compiled Specification,
Procedure, or Plan is stale.
The drift must be routed for recompilation; implementation and evidence cannot
silently redefine either authority.

Navigation remains hierarchical:

```text
repository root hub
└── governed area hub
    └── classified owning artifact
        ├── linked rationale or Decision
        ├── linked playbook/runbook
        └── linked proof/evidence
```

- The root hub answers which stable public areas exist.
- An area hub answers what the area owns, excludes, and where a reader starts.
- An owning artifact answers one primary question and declares its type and
  authority boundary.
- Rationale, procedures, and evidence link to the owner; they do not copy its
  rule. Decisions are atomic sources whose consequences compile into their
  owning evergreen projections.

Every governed area declares one root, owner, purpose, hub, and parent. A child may have many semantic links but one structural parent. Cycles and missing parents are invalid.

Each enabled structural level also owns one one-level-down Mermaid view. A
project hub shows feature groups when present, otherwise its immediate features
and/or layers. A feature-group hub shows its features. A feature or layer hub
shows its main functions, capabilities, or components. Disabled optional levels
need no placeholder. These views provide the helicopter view at the reader's
current scale and link canonical owners without replacing them.

## Current truth and history

Active source atoms authorize current rules or accepted behavior.
Specifications, Procedures, and Plans present compiled views. DSET Change
folders hold proposed deltas and Verification. Archived Changes and Release
Records preserve what happened; changelogs are Derived Views. Evidence may
support current truth, but it is not another authority for that truth.

## Artifact lifecycle

1. Classify the intended artifact by its owning question.
2. Locate the existing owner and area hub before writing.
3. Use a bounded DSET change when authority, public behavior, structure, or reusable rules change.
4. Recompile affected evergreen projections. Emit a new source atom,
   append-only lifecycle event, or explicit absorbing successor when atomic
   authority changes; never edit an emitted atom.
5. Validate configuration, hierarchy, hubs, links, and applicable semantic evals.
6. Reconcile accepted truth and archive through the implementing PR.

Folder layout helps navigation but does not replace ownership. If two files claim the same normative concern, fix the authority boundary rather than adding cross-links between duplicates.
