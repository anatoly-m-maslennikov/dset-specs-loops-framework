---
artifact_type: procedure
artifact_subtype: playbook
scope_path:
  - layer:gov
priority: medium
---

# Artifact type selection

The project-local `artifact_catalog.toml` is the executable type registry.
`dset_settings.toml` enables a project whitelist. This guide explains the
selection boundary; it does not duplicate the full catalog.

## Select one primary meaning

| If the artifact primarily... | Select |
|---|---|
| requires an observable result or obligation | `requirement` |
| records an outside-imposed limitation | `constraint` |
| defines obligations between explicit endpoints | `contract` |
| selects a material realization approach | `implementation_decision` |
| records missing knowledge or choice | `question` |
| asserts a present insufficiency | `problem` |
| defines a deterministic check | `test_plan` |
| defines a judgment- or uncertainty-bearing assessment | `evaluation_plan` |
| preserves why a Definition or Method was selected | `rationale` |
| interprets named inputs without authorizing a conclusion | `analysis_report` |
| records what was observed in a bounded run or review | `evidence_record` |
| concludes what named evidence supports | `verification` |

Split independently reviewable claims. Do not select a type from the workflow
that will use it or the action expected next.

## Use direct subtypes only

- `question`: `conflict`, `risk`, or `opportunity`;
- `problem`: `defect`, `gap`, or `debt`;
- `analysis_report`: `solution_landscape`, `root_cause_analysis`, `proposal`,
  `technical_investigation`, or `external_audit_analysis`; and
- `evidence_record`: `test_result`, `evaluation_result`, `review_report`, or
  `run_record`.

Omit the subtype when the base registered type is precise enough. Never nest
subtypes or store a separate family/parent classification.

## Resolve common ambiguities

| Distinction | Rule |
|---|---|
| Requirement vs Constraint | Project-required result is Requirement; outside-imposed limitation is Constraint |
| Requirement vs Contract | One project obligation is Requirement; reciprocal or boundary obligations with explicit endpoints are Contract |
| Requirement vs Implementation Decision | Required outcome is Requirement; selected realization is Implementation Decision |
| Question vs Problem | Missing knowledge/choice is Question; currently true insufficiency is Problem |
| Conflict vs Defect | Incompatible authority is Conflict; implementation contradicting authority is Defect |
| Risk vs Problem | Possible future harm is Risk; present harm or insufficiency is Problem |
| Gap vs Debt | Required absence is Gap; known workable compromise with ongoing cost is Debt |
| Test Plan vs Evaluation Plan | Exact reproducible predicate is Test Plan; judgment or uncertainty is Evaluation Plan |
| Analysis vs Evidence | Interpretation is Analysis Report; bounded observation is Evidence Record |
| Evidence vs Verification | Evidence records what happened; Verification states what that evidence supports |

Debt never hides a Defect or Gap. An external audit remains external evidence;
the project's interpretation of it is an internal
`analysis_report/external_audit_analysis`.

## Route and carrier are derived

After selecting one enabled type/subtype:

1. resolve Revision mode, Content role, Governance locus, identity kind,
   carrier, and commit behavior from the catalog;
2. assign the narrowest structural `scope_path`;
3. add only non-derived provenance, priority, relations, endpoints, and
   type-specific properties; and
4. fail closed on unknown, disabled, or ambiguous classification.

Atomic narrative artifacts use Markdown with YAML frontmatter. Configuration
uses TOML, schemas and machine boundaries use JSON, running logs use NDJSON,
and implementation uses its native format.

## Identity

Use:

```text
<PROJECT?>-<SCOPE_PATH?>-<ARTIFACT_KIND>-<NNN>-<summary>
```

The project prefix and visible scope are settings choices. The registered type
or enabled subtype owns one project-wide number sequence. Native Git/host
entities use repository-qualified native identities. A vocabulary change is a
complete governed identity migration, not a compatibility alias.
