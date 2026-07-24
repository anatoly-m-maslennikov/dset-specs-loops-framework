---
artifact_type: specification
artifact_subtype: governance
scope_path:
  - layer:gov
priority: high
---

# Artifact routing rules

**Rule ID:** `DSET-RULE-ARTIFACT-CLASSIFICATION`

## Purpose

Every governed artifact has one registered `artifact_type` and at most one
direct `artifact_subtype`. The registered pair derives exactly one route:

- Revision mode: `atomic`, `append_only`, or `maintained`;
- Content role: `inquiry`, `definition`, `rationale`, `method`,
  `implementation`, or `observation`;
- Governance locus: `internal`, `external`, or `relation`.

Artifact carriers store the type pair and do not repeat the derived route
coordinates. Unknown, disabled, or ambiguous mappings fail closed.

`scope_path` is an independent project-relative structural address. The current
project is ambient, so project identity never appears in the path.

## Canonical route catalog

The installed project-local `artifact_catalog.toml` is the only executable
registry of type/subtype routes, identity kinds, carriers, and persistence
behavior. `dset_settings.toml` enables a project whitelist without repeating
route definitions. Unknown, disabled, multiply mapped, or ambiguous
classifications fail closed. Atomic sources: `DSET-REQUIREMENT-GOV-070` and
`DSET-REQUIREMENT-GOV-102`.

## Base atomic type routes

| Artifact type | Optional direct subtypes | Derived route |
|---|---|---|
| `requirement` | — | atomic / definition / internal |
| `constraint` | — | atomic / definition / external |
| `contract` | — | atomic / definition / relation |
| `implementation_decision` | — | atomic / method / internal |
| `question` | `risk`, `opportunity` | atomic / inquiry / internal |
| `question` | `conflict` | atomic / inquiry / relation |
| `problem` | `defect`, `gap`, `debt` | atomic / observation / internal |
| `test_plan` | — | atomic / method / internal |
| `evaluation_plan` | — | atomic / method / internal |
| `rationale` | — | atomic / rationale / internal |
| `analysis_report` | `solution_landscape`, `root_cause_analysis`, `proposal`, `technical_investigation`, `external_audit_analysis` | atomic / rationale / internal |
| `evidence_record` | `test_result`, `evaluation_result`, `review_report`, `run_record` | atomic / observation / internal |
| `verification` | — | atomic / observation / internal |

An `external_audit_analysis` is internal when it is the project’s interpretation
of an external report. The report itself is an external governed artifact.

Constraint is reserved for externally imposed limitations. A project-owned
result or selected restriction is a Requirement or Implementation Decision
according to meaning. Atomic source: `DSET-REQUIREMENT-GOV-057`.

## Non-atomic route boundaries

Append-only carriers preserve accepted record order and add only complete new
records. Running NDJSON logs are append-only Observation/internal artifacts.
Maintained artifacts include specifications, plans, settings, code, runners,
generated dashboards, catalogs, and derived TOON views; each registered type
still derives exactly one Content role and Governance locus.

A Release Plan derives `maintained / definition / internal`. A pull request
derives `maintained / method / relation` and declares source and target endpoint
origins. An internal Git commit derives `atomic / implementation / internal`;
an outside-owned commit uses `external_git_commit` and derives the external
locus. Native repository-qualified identities replace DSET sequences for
commits and pull requests. Atomic sources: `DSET-REQUIREMENT-GOV-078`,
`DSET-REQUIREMENT-GOV-080`, and `DSET-REQUIREMENT-GOV-103`.

Current semantic views are maintained artifacts. DSET defines no separate
currentness or freshness class. Their type-specific procedures own refresh,
generation, synchronization, and direct-authoring behavior.

Inquiry is the Content role for unresolved knowledge, choice, or clarification.
The canonical loop is Inquiry → Definition → Rationale → Method →
Implementation → Observation → Inquiry. Atomic sources:
`DSET-REQUIREMENT-GOV-087` and `DSET-REQUIREMENT-GOV-089`.

## Minimal Markdown properties

DSET Markdown uses a GitHub-compatible YAML property block. An atomic carrier
contains only non-derived properties:

```yaml
---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-038
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-094"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-035"
---
```

`artifact_subtype`, `relations`, precise external `source_refs`, provenance,
relation endpoints, and type-specific observation fields appear only when they
add non-derived meaning. Repeated relations of one kind use one `targets` list.

The following properties are invalid because they duplicate or infer meaning:
`semantic_id`, `revision_mode`, `content_role`, `governance_locus`,
`governance_origin`, `relation_shape`, `status`, generic `authority`, body-
duplicating `claim`, and ephemeral `worktree_state`.

Atomic acceptance is inherent to emission. Active versus archived state comes
from repository placement. External origin does not imply an ambient project
authority; record the actual issuer, source, or endpoint through its precise
type-specific property.

## Identity shape

IDs and filenames use:

```text
<PROJECT?>-<SCOPE_PATH?>-<ARTIFACT_KIND>-<NNN>-<summary>
```

The project prefix is controlled by settings and is omitted when disabled.
`SCOPE_PATH` is an ordered, extensible structural sequence and may contain
layers, features, or their configured nesting. The visible registered type or
enabled direct subtype owns one project-wide number sequence. Changing prefix,
scope grammar, or identity kind requires one complete governed migration
without accepted aliases. Atomic sources: `DSET-REQUIREMENT-GOV-064`,
`DSET-REQUIREMENT-GOV-071`, and `DSET-IMPL-GOV-003`.

## Governance locus and endpoints

The registered type derives Governance locus; carriers never repeat it or store
generic `governance_origin`. A relational artifact declares a stable relation
kind and at least two role-bearing endpoints, each with independent internal or
external origin. Atomic source: `DSET-REQUIREMENT-GOV-101`.

## Routing boundaries

The route is semantic and sparse. Filenames, folders, workflow stages, tools,
and requested next actions do not select it. Empty route cells are valid.

The content-role loop is:

```text
Inquiry
  -> Definition
  -> Rationale
  -> Method
  -> Implementation
  -> Observation
  -> Inquiry
```

The loop relates artifacts; it does not mutate one artifact through multiple
roles. Tests and Evaluations are Method when they define checks. Their persisted
results are Observation. Executable runners are maintained Implementation.

Relations are first-class only when the governed subject is the relation
itself. A relation declares a stable kind and explicit role-bearing endpoints.
Ordinary citations and traceability links do not change an artifact’s
Governance locus.

OPS remains a layer in `scope_path`, not another Content role. A release
condition is Definition, a deployment procedure is Method, deployable
configuration is Implementation, and a deployment result is Observation.

## Classification order

1. Identify one primary claim or job; split multi-head artifacts.
2. Select the registered type and optional direct subtype.
3. Resolve its route from the registry and fail closed on ambiguity.
4. Assign the narrowest correct `scope_path`.
5. Add only non-derived provenance, priority, applicability, endpoints,
   relations, and type-specific facts.
6. For an external artifact, identify its actual source precisely.

The schema, template, writer, and validator use this same boundary.
