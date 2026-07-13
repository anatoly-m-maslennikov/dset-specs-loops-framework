# DSET templates

Version 1.0 templates are inputs to `dset new`. Placeholders use `{{snake_case_name}}`; the CLI replaces only documented placeholders and refuses an existing destination.

- [`profiles.yaml`](profiles.yaml) defines required artifacts for small, standard, large, defect, and adoption changes.
- [`change/`](change/) contains the common change artifacts plus profile supplements.
- [`package/`](package/) contains accepted package-truth templates.

Every change profile keeps `proposal.md`, `specs/`, `test-plan.md`, `eval-plan.md`, `proofs/`, `tasks.md`, and `verification.md`. A small deterministic change may declare evals not applicable with a reason; it may not merge tests and evals into one artifact.
