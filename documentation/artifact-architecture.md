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

## Artifact roles and navigation

Durable content has one of four roles:

- an **atomic authority source** is an immutable accepted Requirement,
  Contract, Decision, or other normative atom;
- an **evergreen compiled projection** is an editable current spec, plan,
  runbook, or governing document compiled from active sources;
- **transactional context or evidence** records proposed work, rationale,
  review, proof, or history without becoming authority by itself; and
- an **implementation artifact** is code, configuration, tests, eval prompts,
  or another delivered executable surface.

Role and primary type come from semantic content, the owning question, and
authority/lifecycle position. Workflow, queue, skill, tool, host, filename,
folder, and intended next action are routing metadata and never define type.

An active applicable source atom wins when its evergreen projection is stale.
The drift must be routed for recompilation; implementation and evidence cannot
silently redefine either authority.

Navigation remains hierarchical:

```text
repository root hub
└── governed area hub
    └── owning artifact
        ├── linked rationale or Decision
        ├── linked playbook/runbook
        └── linked proof/evidence
```

- The root hub answers which stable public areas exist.
- An area hub answers what the area owns, excludes, and where a reader starts.
- An owning artifact answers one primary question and declares its role and
  authority boundary.
- Rationale, procedures, and evidence link to the owner; they do not copy its
  rule. Decisions are atomic sources whose consequences compile into their
  owning evergreen projections.

Every governed area declares one root, owner, purpose, hub, and parent. A child may have many semantic links but one structural parent. Cycles and missing parents are invalid.

## Current truth and history

Active source atoms authorize current rules or accepted behavior. Evergreen
artifacts present the current compiled view. DSET Change folders hold proposed
deltas and verification. Archived Changes and changelogs preserve what
happened. Evidence may prove current truth, but it is not another authority for
that truth.

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
