---
artifact_type: specification
artifact_subtype: domain_model
scope_path:
  - layer:gov
priority: high
---

# Governance domain model

This model defines GOV entities in dependency order. A definition uses only
entities defined above it; later sections add relations without changing an
earlier definition.

## Entities

| Entity | Definition |
|---|---|
| **Project** | The current repository or monorepo work area selected for one DSET governance context |
| **Structural scope** | A project-relative owner address composed from enabled layers, features, feature groups, or future registered structural dimensions |
| **Governed artifact** | One persisted project item with one primary registered artifact type, at most one direct registered subtype, and one structural scope |
| **Artifact route** | The tuple of Revision mode, Content role, and Governance locus derived from a governed artifact's registered type/subtype |
| **Revision mode** | Exactly one write behavior: `atomic`, `append_only`, or `maintained` |
| **Content role** | Exactly one contribution to the development loop: `inquiry`, `definition`, `rationale`, `method`, `implementation`, or `observation` |
| **Governance locus** | Exactly one ownership position: `internal`, `external`, or `relation` |
| **Atomic artifact** | A governed artifact whose accepted meaning is immutable after emission |
| **Append-only artifact** | A governed artifact whose accepted records and order are immutable and that accepts only complete new records |
| **Maintained artifact** | A governed artifact whose registered procedure may revise existing content |
| **Active atom** | An Atomic artifact located in its active type folder and eligible for current routing, authority, work, or assurance according to its type |
| **Archived atom** | The same immutable Atomic artifact relocated byte-for-byte to its type-local `archive/` and excluded from the active set |
| **Artifact relation** | One registered directional semantic edge from a source artifact to one or more stable target identities |
| **Artifact catalog** | The single project-local executable registry mapping each allowed type/subtype to one route, identity kind, carrier, and persistence behavior |
| **Project settings** | The single project-local operator configuration selecting enabled artifact types/subtypes, workflow behavior, optional surfaces, and other policy choices without restating catalog mappings |
| **Maintained semantic view** | A thin current model synthesized from applicable active atoms, containing a domain flow, dependency-ordered entity definitions, lifecycle criteria, and links to its atomic sources |
| **Governance registry** | The project-local mapping from workflow and rule IDs to one maintained governing document, its prerequisites, applicability, and profile identity |
| **Governing document** | The single Maintained artifact that owns the current application of one or more normative rule IDs |
| **Hub** | A thin Maintained navigation artifact linking stable folders and long-lived owners without listing every atom or owning normative truth |
| **Framework source** | The repository-root reusable DSET methodology from which released methodology packages are produced |
| **Installed methodology** | A materialized project-local copy of selected released framework source under `.dset/000_dset_methodology/` |
| **Applied project artifact** | A project-owned Governed artifact outside installed methodology that records the current project's requirements, work, implementation, assurance, or history |
| **Journal** | Durable Append-only NDJSON records under `.dset_journal/` |
| **Runtime state** | Disposable locks, caches, scratch data, and process-local output under `.dset_runtime/` |
| **Priority** | The stored `high`, `medium`, or `low` rank, with `highest` available only as a virtual capped comparison result |
| **Ruleset identity** | The selected profile/version provenance plus whether installed local rules remain equivalent or form an explicitly custom project ruleset |

## Core invariants

- **DSET-INVARIANT-GOV-001:** Framework source, installed methodology, and
  applied project artifacts never share a writable owner. Installation
  materializes ordinary files; governed execution never follows a live
  reference back to framework source. Sources:
  `DSET-DECISION-GOV-022`, `DSET-IMPL-GOV-002`, and
  `DSET-REQUIREMENT-GOV-052`.
- **DSET-INVARIANT-GOV-002:** Every governed artifact has one registered
  type/subtype and derives exactly one Artifact route. No parent semantic-Type
  hierarchy, workflow name, carrier, folder, or requested next action supplies
  a second classification. Sources: `DSET-REQUIREMENT-META-035`,
  `DSET-IMPL-GOV-003`, and `DSET-REQUIREMENT-GOV-101`.
- **DSET-INVARIANT-GOV-003:** The Artifact catalog owns route and identity
  mappings. Project settings own only the enabled whitelist and operator
  choices. Unknown, disabled, duplicate, or ambiguous mappings fail closed.
  Source: `DSET-REQUIREMENT-GOV-102`.
- **DSET-INVARIANT-GOV-004:** The only Revision modes are `atomic`,
  `append_only`, and `maintained`; no freshness class is a fourth mode.
  Sources: `DSET-REQUIREMENT-META-041` and
  `DSET-REQUIREMENT-META-042`.
- **DSET-INVARIANT-GOV-005:** An Atomic artifact's accepted meaning is
  immutable. Complete semantic correction emits a successor. A proven
  one-to-one identity or carrier migration may recode representation without
  changing the atom. Sources: `DSET-REQUIREMENT-GOV-060` and
  `DSET-REQUIREMENT-GOV-061`.
- **DSET-INVARIANT-GOV-006:** Active and archived are the only Atomic-artifact
  storage states. Replacement, resolution, withdrawal, and recurrence use
  typed relations, archive placement, Version planning, and Git history; DSET
  has no lifecycle-event artifact type. Source: `DSET-DECISION-GOV-035`.
- **DSET-INVARIANT-GOV-007:** Every Markdown artifact has valid YAML
  frontmatter and remains GitHub-preview compatible. Derived route coordinates,
  status, generic authority, and ephemeral worktree state are not duplicated
  in the property block. Sources: `DSET-CONSTRAINT-GOV-002`,
  `DSET-REQUIREMENT-GOV-095`, and `DSET-REQUIREMENT-META-038`.
- **DSET-INVARIANT-GOV-008:** Carrier choice follows job: Markdown with YAML
  frontmatter for human-governed narrative artifacts; TOML for directly
  executed human-edited configuration; JSON for schemas, contracts, wire data,
  or generated machine data; NDJSON for append-only logs; and native formats
  for code, CI, lockfiles, and host manifests. Sources:
  `DSET-DECISION-GOV-015` and `DSET-REQUIREMENT-GOV-097`.
- **DSET-INVARIANT-GOV-009:** Git is mandatory. Every implemented authority or
  resolved Problem has a committed change naming the governed artifact and one
  Session trailer. Source: `DSET-REQUIREMENT-GOV-065`.
- **DSET-INVARIANT-GOV-010:** Stored priority is exactly `high`, `medium`, or
  `low`; `highest` is virtual and future-version work belongs in a Version
  Roadmap rather than a deferred priority. Source:
  `DSET-REQUIREMENT-GOV-063`.
- **DSET-INVARIANT-GOV-011:** `.dset/` owns governed state,
  `.dset_journal/` owns durable append-only running records, and
  `.dset_runtime/` owns disposable state. Source:
  `DSET-REQUIREMENT-GOV-100`.
- **DSET-INVARIANT-GOV-012:** Features are horizontal peers joined by
  Contracts. Layers are ordered `META → GOV → TOOL → SKILL → IMPL → OPS`;
  authority moves only forward, preferably one layer at a time.
- **DSET-INVARIANT-GOV-013:** Every claim belongs to the narrowest structural
  scope containing all affected owners and subjects. A project-level artifact
  owns only genuinely cross-child or whole-project concerns. Source:
  `DSET-REQUIREMENT-GOV-032`.
- **DSET-INVARIANT-GOV-014:** Authority and assurance remain distinct.
  Requirements, Constraints, Contracts, and Implementation Decisions may
  authorize; plans define checks; executions create observations; Verification
  derives a bounded reliance statement.
- **DSET-INVARIANT-GOV-015:** Rules resolve locally to one maintained governing
  document and its active atomic sources. Invalid ownership, dependency,
  precedence, applicability, or customization identity fails closed.
