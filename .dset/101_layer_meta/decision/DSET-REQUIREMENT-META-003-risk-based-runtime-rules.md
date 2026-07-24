+++
artifact_id = "DSET-ATOMIC-RECORD-272"
semantic_id = "DSET-REQUIREMENT-META-003"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET selects recovery semantics by runtime risk and durable authority by topology, write volume, and concurrency rather than imposing one durability mechanism on every project."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Stateless services, modest-write local tools, and concurrent durable systems have different authoritative state and recovery needs."
+++

# Requirement — Risk-based runtime rules

Event sourcing, reconciliation, durable execution, and observed-progress
liveness apply only when their semantics are required. A project declares one
durable authority appropriate to its topology instead of adding duplicate
writable truth.
