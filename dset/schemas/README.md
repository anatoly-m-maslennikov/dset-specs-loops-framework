# DSET schemas

Version 1.1 publishes machine-readable JSON Schemas for external tooling while preserving legacy v1.0 manifest shapes. The repository-owned validator enforces current filesystem and Markdown semantics without a runtime dependency.

| Schema | Contract |
|---|---|
| [`project.schema.json`](project.schema.json) | `dset/dset.yaml` project identity, topology, supportability, profiles, and lifecycle |
| [`artifacts.schema.json`](artifacts.schema.json) | `dset/artifacts.yaml` governed areas, hubs, owners, purposes, and parent hierarchy |
| [`package.schema.json`](package.schema.json) | Accepted package manifest and owned Requirement/Test/Eval/Contract plus optional Story/Outcome IDs |
| [`change.schema.json`](change.schema.json) | Active or archived change identity, status, PR, trace IDs including optional Stories and Outcomes, and archive metadata |
| [`provenance.schema.json`](provenance.schema.json) | Third-party source, revision, license, and use boundary |
| [`pull-request-history.schema.json`](pull-request-history.schema.json) | GitHub-authoritative PR snapshot used as traceability evidence |
| [`traceability.schema.json`](traceability.schema.json) | Deterministically generated change-to-Story/Outcome/Contract-to-proof-to-PR index |
| [`governance.schema.json`](governance.schema.json) | Repository-local workflow/rule ownership, dependencies, applicability, provenance, customization, and wrapper identity |
| [`version.schema.json`](version.schema.json) | Coordinated product/package identity, independent schema version, and released/candidate validator identities |
| [`budget.schema.json`](budget.schema.json) | Tree-wide low/medium/high delegation bounds, inheritance policy, and quality floor |
| [`skill-run.schema.json`](skill-run.schema.json) | Bounded redacted machine-local invocation evidence and model/budget attestation |
| [`intake.schema.json`](intake.schema.json) | Project-owned Problem/Opportunity/Question registry, stable layers, and Decision links |

JSON Schema validates data shape. The canonical `dset check` command additionally validates required directories/documents, governed artifact areas and hubs, repository-local rule ownership and wrapper identity, Markdown links and portability, project/type/layer ID consistency, Contract references, archive gates, provenance files, competing roots, and generated-index freshness.
