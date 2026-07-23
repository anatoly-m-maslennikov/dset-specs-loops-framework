+++
artifact_id = "DSET-ATOMIC-RECORD-157"
semantic_id = "DSET-DECISION-GOV-022"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET stores the installed project-local methodology only under .dset/000_dset_methodology, stores applied project artifacts only under .dset/100_project through .dset/150_versions, and keeps the reusable framework source in the repository root's 10_project through 50_versions product structure."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-051"
+++

# Decision — Separate methodology from applied project artifacts

The project-local DSET control plane uses three visibly distinct carriers:

```text
.dset/000_dset_methodology/   installed project-local DSET methodology
.dset/100_project/            applied project-wide artifacts
.dset/101_layer_meta/         applied META artifacts
.dset/102_layer_gov/          applied GOV artifacts
.dset/103_layer_tool/         applied TOOL artifacts
.dset/104_layer_skill/        applied SKILL artifacts
.dset/105_layer_ops/          applied OPS artifacts
.dset/150_versions/           applied Version artifacts
```

The reusable DSET framework source remains a separate governed product surface
at the repository root:

```text
10_project/
11_layer_meta/
12_layer_gov/
13_layer_tool/
14_layer_skill/
15_layer_ops/
50_versions/
```

`000_dset_methodology` contains governing rules, procedures, schemas,
templates, and workflow definitions. It never owns this project's Decisions,
Questions, Problems, QA atoms, evidence, or applied specifications and plans.

## Rationale

Methodology defines how the project works; applied artifacts record what this
project decides, plans, checks, and observes. Keeping those carriers in
separate numbered namespaces prevents framework rules from being mistaken for
project state while preserving deterministic local rule resolution for thin
skills.
