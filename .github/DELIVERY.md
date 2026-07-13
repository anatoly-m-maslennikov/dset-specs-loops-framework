# Repository delivery policy

This operational document defines how the repository moves changes from `dev` to `main`. The framework overview and documentation map live in the root [README](../README.md).

## Rules

- [`dev` ruleset](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/rules/18896762): only `anatoly-m-maslennikov` may create, update, or delete `dev`.
- [`main` ruleset](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/rules/18897046): `main` has no bypass actors; every update requires a pull request, the `PR policy` check, and the merge-commit method.
- [Policy workflow](workflows/auto-merge-owner-prs.yml): `PR policy` passes only for a same-repository `dev → main` pull request authored by the repository owner. A passing non-draft PR is merged automatically.
- [DSET workflow](workflows/dset.yml): `DSET / validate` runs the locked Python profile, unit and fixture tests, DSET contract validation, trace freshness, and diff hygiene on `dev` and `main` pull requests.

Merge commits are deliberate: `dev` is long-lived, so preserving its commits as parents of `main` prevents the history divergence caused by repeated squash or rebase merges.

## Delivery sequence

1. The owner commits and pushes a bounded change to `dev`.
2. The owner opens a ready pull request from `dev` to `main`.
3. `PR policy` validates the author, repository, head, and base.
4. `DSET / validate` proves the tested head satisfies the executable framework contract.
5. GitHub Actions enables merge-commit auto-merge.
6. GitHub updates `main` only after the required checks pass.

Pull requests to `main` from any other branch, repository, or author are expected to fail `PR policy` and cannot merge.
