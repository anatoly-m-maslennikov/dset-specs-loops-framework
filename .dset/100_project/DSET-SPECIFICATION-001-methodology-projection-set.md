+++
artifact_type = "specification"
artifact_subtype = "governance"
artifact_id = "DSET-SPECIFICATION-001"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[[relations]]
type = "projection_of"

[relations.range]
semantic_type = "decision"
layer = "gov"
through = "DSET-ATOMIC-RECORD-162"

[relations.range.scope]
kind = "project"
id = "dset-specs-loops-framework"

[[relations]]
type = "projection_of"

[relations.range]
semantic_type = "qa"
subtype = "test"
layer = "gov"
through = "DSET-ATOMIC-RECORD-114"

[relations.range.scope]
kind = "project"
id = "dset-specs-loops-framework"

[[relations]]
type = "projection_of"

[relations.range]
semantic_type = "qa"
subtype = "evaluation"
layer = "gov"
through = "DSET-ATOMIC-RECORD-115"

[relations.range.scope]
kind = "project"
id = "dset-specs-loops-framework"

[[relations]]
type = "projection_of"

[relations.range]
semantic_type = "decision"
layer = "gov"
through = "DSET-ATOMIC-RECORD-078"

[relations.range.scope]
kind = "layer"
id = "gov"

[[relations]]
type = "projection_of"

[relations.range]
semantic_type = "qa"
subtype = "test"
layer = "gov"
through = "DSET-ATOMIC-RECORD-079"

[relations.range.scope]
kind = "layer"
id = "gov"

[[relations]]
type = "projection_of"

[relations.range]
semantic_type = "qa"
subtype = "evaluation"
layer = "gov"
through = "DSET-ATOMIC-RECORD-080"

[relations.range.scope]
kind = "layer"
id = "gov"
+++

# Methodology projection set

This evergreen carrier binds the current GOV semantic frontiers to the package
fragments that compile them:

- Behavior specification: `080_dset-gov-specification-methodology.md`
- Deterministic Test plan: `DSET-GOV-plan-tests.md`
- Qualitative Evaluation plan: `DSET-GOV-plan-evaluations.md`

It owns projection metadata only. The linked fragments own their respective
compiled content, and the immutable atoms own authority and QA definitions.
