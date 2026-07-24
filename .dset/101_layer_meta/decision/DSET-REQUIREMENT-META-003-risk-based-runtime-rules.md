---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-META-003"
scope_path:
  - "layer:meta"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Requirement — Risk-based runtime rules

Event sourcing, reconciliation, durable execution, and observed-progress
liveness apply only when their semantics are required. A project declares one
durable authority appropriate to its topology instead of adding duplicate
writable truth.

## Primary claim

DSET selects recovery semantics by runtime risk and durable authority by topology, write volume, and concurrency rather than imposing one durability mechanism on every project.

## Rationale

Stateless services, modest-write local tools, and concurrent durable systems have different authoritative state and recovery needs.
