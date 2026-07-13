# Change archive

On the accepted target branch, archived changes are immutable historical evidence. Each directory is named `YYYY-MM-DD-<change-id>` and records the repository-qualified implementing PR identity.

Archival is a two-phase transaction inside the implementing draft PR. After baseline verification and current-truth reconciliation, commit and push an explicitly incomplete dated candidate so remote checks can inspect the real PR head. After those checks pass, an evidence-only commit records the results and final archived status. Any later implementation or specification change invalidates archive readiness and requires verification and applicable traceability evidence to be refreshed before merge.

When the selected enforcement profile or canonical command is pending, the archived verification must record a manual PR/link/archive audit and the exact read-only checks. It must not claim that unavailable CI, validation, or traceability generation passed.

## Candidates

- [2026-07-14 — Bootstrap the DSET project structure](2026-07-14-bootstrap-dset-project-structure/proposal.md) — incomplete candidate in draft PR [anatoly-m-maslennikov/dset-loops-framework#2](https://github.com/anatoly-m-maslennikov/dset-loops-framework/pull/2); final remote-head evidence pending
