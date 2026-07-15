# DSET templates

Artifact templates remain schema/toolchain v1 inputs to `dset new`. The separately versioned `core-v1` governance profile is a DSET 0.2 framework input to `dset rules materialize`. Both commands replace only documented placeholders and refuse an existing destination.

- [`profiles.yaml`](profiles.yaml) defines required artifacts for small, standard, large, defect, and adoption changes.
- [`change/`](change/) contains the common change artifacts plus profile supplements.
- [`package/`](package/) contains accepted package-truth templates.
- [`governance/core-v1/`](governance/core-v1/README.md) contains repository-governed architecture, build, authoring, proof, diagnosis, prototype, supportability, and artifact-maintenance defaults plus their workflow map.

Every change profile keeps `proposal.md`, `specs/`, `test-plan.md`, `eval-plan.md`, `proofs/`, `tasks.md`, and `verification.md`. A small deterministic change may declare evals not applicable with a reason; it may not merge tests and evals into one artifact.

Materialized governance documents become editable project truth immediately. The profile/template version and digest remain provenance; later framework releases are compared with `dset rules diff --source <framework-root>` and never overwrite local documents.
