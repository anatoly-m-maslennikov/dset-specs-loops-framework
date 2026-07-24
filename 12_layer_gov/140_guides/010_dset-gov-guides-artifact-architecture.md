---
artifact_type: procedure
artifact_subtype: playbook
scope_path:
  - layer:gov
priority: medium
---

# Artifact architecture

## Separate semantic routing from project structure

Each governed artifact has one catalog-derived route:

```text
revision_mode × content_role × governance_locus
```

`scope_path` is structural, not a fourth semantic axis. It may represent
layers, features, feature groups, layers inside features, features inside
layers, or future registered dimensions. The current project is ambient and is
not repeated in the path.

The catalog derives route and identity kind from one registered
`artifact_type` plus at most one direct `artifact_subtype`. The carrier never
repeats route coordinates. Workflow, queue, skill, tool, host, filename,
folder, and intended next action determine neither type nor route.

## Keep other selections orthogonal

Runtime risk, durability topology, implementation profile, and artifact
governance are independent selections:

| Selection | Governing question |
|---|---|
| Runtime risk | Which recovery, safety, and supportability semantics apply? |
| Durability topology | Which local or external system owns persistent state? |
| Implementation profile | Which language/runtime coding and proof rules apply? |
| Artifact governance | Which artifact types, structures, carriers, and authoring rules apply? |

Documentation does not inherit Python or TypeScript thresholds merely because
the repository also contains code.

## Own artifacts at the narrowest scope

Features are horizontal peer capabilities connected by Contracts at their
narrowest common owner. Layers are ordered authority refinements:

```text
META → GOV → TOOL → SKILL → IMPL → OPS
```

Layer authority moves only forward. A downstream artifact may implement,
check, analyze, or provide evidence for upstream authority without reversing
the dependency. If irreducible backward authority remains, propose
reclassifying the coupled owners as features rather than hiding the cycle.

Place every claim at the narrowest structural ancestor containing all affected
owners and subjects. Project-level artifacts own genuinely cross-child
requirements, contracts, shared semantics, integration architecture, end-to-end
assurance, release history, and cross-owner inquiry or observation. They link
to child detail instead of duplicating it.

## Navigate one level at a time

```text
repository hub
└── immediate feature groups, features, or layers
    └── immediate capabilities or components
```

Every enabled structural level has one current Mermaid view of itself and the
level immediately below. Hubs link stable folders, maintained files, settings,
and other long-lived owners; they do not list every atomic artifact or anything
inside `.dset_runtime/`.
Sources: `DSET-REQUIREMENT-GOV-031` and
`DSET-REQUIREMENT-GOV-053`.

## Connect artifacts with precise relations

Use the narrowest registered forward relation. Derive reverse edges.

- `child_of` narrows or decomposes;
- `analysis_of` interprets;
- `projection_of` states a maintained-view frontier;
- `implementation_of` realizes;
- `check_of` defines assurance;
- `evidence_for` supports a run or conclusion;
- `resolution_of` closes inquiry or observation;
- `solution_for` supplies a conflict solution;
- `override_of` creates a narrower exception;
- `replacement_of` completely replaces;
- `recurrence_of` links a new occurrence to an archived predecessor; and
- `relates_to` is a fallback with no semantic or coverage force.

Relational artifact types declare stable kinds and explicit role-bearing
endpoints. Ordinary links and citations do not make an artifact relational.

## Separate current views from atomic authority

An active atomic authority source wins over a stale maintained semantic view.
Refresh the affected view on demand or before a relying gate. A view records
precise `projection_of` frontiers and source links; it does not copy every atom
or become an independent authority.

## Lifecycle

1. Explore without artifact creation until a durable conclusion is accepted.
2. Classify the smallest primary claim by direct type/subtype.
3. Assign the narrowest scope and precise relations.
4. Emit atomically and commit with provenance.
5. Refresh enabled maintained views when required.
6. Implement, check, observe, and verify through distinct artifacts.
7. Resolve or replace with a new atom, then archive the predecessor with
   explicit commit trailers.

Folder layout supports discovery but never substitutes for ownership.
