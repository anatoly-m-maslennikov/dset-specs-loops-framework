# DSET templates

Artifact templates remain schema/toolchain v1 inputs to `dset new`. The separately versioned `core-v1` governance profile is a DSET 0.2 framework input to `dset rules materialize`. Both commands replace only documented placeholders and refuse an existing destination.

- [`profiles.yaml`](profiles.yaml) defines required artifacts for small, standard, large, defect, and adoption changes.
- [`budget.yaml`](budget.yaml) seeds the project-owned delegation budget without changing scope, proof, or safety requirements.
- [`intake.yaml`](intake.yaml) registers the stable `META`, `GOV`, `TOOL`, `SKILL`, and `OPS` layers used by optional ID layer segments.
- [`change/`](change/) contains the common change artifacts plus profile supplements.
- [`package/`](package/) contains accepted package-truth templates, including optional User Story and measurable Outcome records.
- [`governance/core-v1/`](governance/core-v1/README.md) contains repository-governed architecture, build, authoring, proof, diagnosis, prototype, supportability, lifecycle, run-record, budget, release, intake, and artifact-maintenance defaults plus their workflow map.

Every change profile keeps `proposal.md`, `specs/`, `test-plan.md`, `eval-plan.md`, `proofs/`, `tasks.md`, and `verification.md`. A small deterministic change may declare evals not applicable with a reason; it may not merge tests and evals into one artifact.

Materialized governance documents become editable project truth immediately. The profile/template version and digest remain provenance; later framework releases are compared with `dset rules diff --source <framework-root>` and never overwrite local documents.
