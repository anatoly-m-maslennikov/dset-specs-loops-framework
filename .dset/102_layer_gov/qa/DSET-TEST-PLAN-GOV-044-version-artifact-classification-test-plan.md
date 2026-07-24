+++
artifact_id = "DSET-ATOMIC-RECORD-079"
semantic_id = "DSET-TEST-PLAN-GOV-044"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic validation requires Version and its six exact direct subtypes across current authority, registries, templates, active carriers, generated views, settings examples, and release behavior, while rejecting Delivery as a current artifact Type."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[promotion]
affected_children = ["gov", "tool", "ops"]
applies_unchanged = false
local_context_required = true

[promotion.parent_scope]
kind = "project"
id = "dset-specs-loops-framework"

[[relations]]
type = "check_of"
target = "DSET-DECISION-GOV-019"

[[relations]]
type = "check_of"
target = "DSET-DECISION-OPS-007"
+++

# Test Plan — Enforce the Version artifact classification

Parse the current registry, schemas, templates, active Version artifacts,
settings examples, and release-tool fixtures. Require the primary Type
`version`, the direct subtypes `roadmap`, `version_scope`, `change`,
`release_plan`, `readiness_record`, and `release_record`, and one shared
type-bearing `VERSION` identity sequence. Reject `delivery` as a current
artifact Type, mismatched or nested subtypes, stale active `DELIVERY` IDs, and
partial migrations. Preserved historical records may retain the former term
only when their currentness is explicitly historical.

Run artifact-type, project-health, release-artifact, release-integration,
bootstrap, recursive validation, and generated-view freshness checks.

This emitted Test atom is immutable. Later correction requires a successor
Test and append-only lifecycle event.
