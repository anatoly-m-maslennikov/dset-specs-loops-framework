+++
artifact_id = "DSET-ATOMIC-RECORD-059"
semantic_id = "DSET-DEFECT-GOV-006"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "repository:fpf-review"
claim = "Promoted Evidence Records are immutable but lack an executable schema for their required subject, producer, method, context, time, polarity, currentness, and reopen boundary."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Evidence cannot support a bounded claim reliably when its because-graph exists only as optional prose."
promotion = {}

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-025"
+++

# Defect — Evidence Record requirements are prose-only

Governance requires promoted proof to name one subject and intended use,
producer or performed work, method and setup, applicable context, observation
time or validity window, exact version, polarity, currentness, and reopening
trigger. No Evidence Record schema or validator enforces that contract.

## Completion condition

A TOML-frontmatter Evidence Record schema, template, and validator enforce the
bounded core fields. Risk-triggered rival-explanation and independent-producer
extensions remain optional. Existing promoted proof is preserved as immutable
legacy evidence rather than silently rewritten.
