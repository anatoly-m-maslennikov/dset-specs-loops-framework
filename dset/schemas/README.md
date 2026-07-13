# DSET schemas

Version 1.0 publishes machine-readable JSON Schemas for external tooling while the repository-owned validator enforces filesystem and Markdown semantics without a runtime dependency.

| Schema | Contract |
|---|---|
| [`project.schema.json`](project.schema.json) | `dset/dset.yaml` project identity, topology, supportability, profiles, and lifecycle |
| [`package.schema.json`](package.schema.json) | Accepted package manifest and owned requirement/test/eval IDs |
| [`change.schema.json`](change.schema.json) | Active or archived change identity, status, PR, proof IDs, and archive metadata |
| [`provenance.schema.json`](provenance.schema.json) | Third-party source, revision, license, and use boundary |
| [`pull-request-history.schema.json`](pull-request-history.schema.json) | GitHub-authoritative PR snapshot used as traceability evidence |
| [`traceability.schema.json`](traceability.schema.json) | Deterministically generated change-to-proof-to-PR index |

JSON Schema validates data shape. The canonical `dset check` command additionally validates required directories/documents, Markdown links and portability, ID references, archive gates, provenance files, competing roots, and generated-index freshness.
