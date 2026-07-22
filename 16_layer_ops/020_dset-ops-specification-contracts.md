# Methodology OPS public contract

## Release compatibility surface

DSET versions use integer SemVer components. The complete transition table includes bootstrap, pre-1.0 normal/small, first/subsequent RC, final, and post-1.0 small/normal/breaking releases. Product/package identity is canonical SemVer with defined ecosystem serialization; tag and publisher release derive idempotently from the configured protected merge commit. Schema, profile, and template-format versions remain independent compatibility surfaces.

### DSET-CONTRACT-OPS-001 — CI is hosted GitHub Actions evidence

| Field | Value |
|---|---|
| Authority | DSET maintainers |
| Source | GitHub Actions workflow syntax/event/permission contracts and repository protected-branch configuration, pinned by version or digest in release evidence |
| Version or digest | `1.0` |
| Direction | Repository workflow artifacts and PR-head commits to GitHub-hosted checks and protected integration |
| Producer | `.github/workflows/` and GitHub Actions on the actual pull-request head |
| Consumer | Contributors, reviewers, required-check rules, and protected-branch integration |
| Conformance | Real workflow artifacts under `.github/workflows/` define valid syntax, events, least-required permissions, stable check names, artifact/log retention, exact-SHA correlation, failure visibility, and execution on the actual PR head |
| Compatibility | Required hosted checks integrate with protected-branch policy and retain stable GitHub check/run evidence; local scripts and specification prose are inputs, not hosted-CI proof |
| Lifecycle | `active` |
