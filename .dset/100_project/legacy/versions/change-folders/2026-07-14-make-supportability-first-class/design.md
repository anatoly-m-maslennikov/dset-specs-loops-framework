# Design — Supportability across spec loops

> Archive candidate in [PR #3](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/3).

## Public model

- **DSET:** Domain–Supportability–Evals–Tests.
- **Spec Loops:** the governed iteration mechanism that carries domain intent, supportability, tests, evals, implementation, verification, reconciliation, and repair.
- **Production supportability:** the ability to investigate and fix a real deployed issue using safe, bounded evidence already designed into the system.

## Supportability envelope

Each applicable production change declares:

1. Operator questions and supported incident classes.
2. Public failure, correlation, trace, job/run, entity, and incident identifiers as applicable.
3. Deployed version, commit, repository-qualified PR, and DSET-change identity.
4. Structured logs, traces, metrics/events, diagnostic bundle, status surfaces, and runbook entrypoints selected by profile.
5. Data classification, redaction, retention, access, sampling, cardinality, volume, and cost limits.
6. The traversal from incident evidence to owning requirement, deterministic test or qualitative eval, and repair evidence.

## Ownership

Runtime telemetry observes behavior; it does not become a competing business-state authority. Local files, databases, brokers, and external systems keep the owners selected by the durability topology. Support signals must reference those owners and record enough identity to reproduce or reconcile a failure.

## Applicability

Profile A/local one-shot work may need only deterministic exit status and a redacted diagnostic report. Stateful local tools add resumable progress and file/database identity. Services add centralized operational signals as needed. Distributed or asynchronous work adds cross-boundary correlation, attempt/effect identity, and end-to-end outcome evidence.
