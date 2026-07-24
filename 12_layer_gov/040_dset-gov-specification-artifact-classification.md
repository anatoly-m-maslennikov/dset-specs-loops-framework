# Artifact routing rules

**Rule ID:** `DSET-RULE-ARTIFACT-CLASSIFICATION`

## Purpose

Every governed artifact has one registered `artifact_type` and at most one
direct `artifact_subtype`. The registered pair derives exactly one route:

- Revision mode: `atomic`, `evergreen`, or `maintained`;
- Content role: `inquiry`, `definition`, `rationale`, `method`,
  `implementation`, or `observation`;
- Governance locus: `internal`, `external`, or `relation`.

Artifact carriers store the type pair and do not repeat the derived route
coordinates. Unknown, disabled, or ambiguous mappings fail closed.

`scope_path` is an independent project-relative structural address. The current
project is ambient, so project identity never appears in the path.

## Base atomic type routes

The executable registry is the `x-dset-type-routes` table in
`010_dset-gov-schemas-atom.schema.toml`.

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

An `external_audit_analysis` is internal when it is the project’s interpretation
of an external report. The report itself is an external governed artifact.

## Minimal Markdown properties

DSET Markdown uses a GitHub-compatible YAML property block. An atomic carrier
contains only non-derived properties:

```yaml
---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-094
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: analysis_of
    targets:
      - "DSET-REQUIREMENT-META-018"
      - "DSET-REQUIREMENT-META-020"
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
