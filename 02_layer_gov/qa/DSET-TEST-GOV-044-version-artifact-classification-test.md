+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-079"
type = "qa"
subtype = "test"
semantic_id = "DSET-TEST-GOV-044"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic validation requires Version and its six exact direct subtypes across current authority, registries, templates, active carriers, generated views, settings examples, and release behavior, while rejecting Delivery as a current artifact Type."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "layer"
id = "gov"

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

# Test — Enforce the Version artifact classification

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
