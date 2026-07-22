+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-077"
type = "decision"
semantic_id = "DSET-DECISION-OPS-007"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "The release lifecycle uses the primary Version artifact Type, never Delivery, with six flat direct subtypes and unchanged reference and gate boundaries."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Version names the governed object directly and is easier to interpret without extra framework context; Delivery can be mistaken for deployment, logistics, execution, or a workflow phase."

[scope]
kind = "layer"
id = "ops"

[promotion]
affected_children = ["meta", "gov", "tool", "skill", "ops"]
applies_unchanged = false
local_context_required = true

[promotion.parent_scope]
kind = "project"
id = "dset-specs-loops-framework"

[[relations]]
type = "replacement_of"
target = "DSET-DECISION-OPS-006"
+++

# Decision — Name the release lifecycle Type Version

The artifact classification for the release lifecycle uses the primary
`version` Type. Its six direct subtypes remain:

- `roadmap`;
- `version_scope`;
- `change`;
- `release_plan`;
- `readiness_record`; and
- `release_record`.

The six roles remain flat peers. Their existing authority, mutability,
reference chain, readiness boundary, release-record immutability, milestone
placement, and release-cycle semantics do not change. Only their primary Type
name changes from `delivery` to `version`.

Current registries, schemas, templates, toolchain behavior, generated views,
tests, settings examples, and active artifact carriers use `version`. Default
type-bearing IDs and filenames use `VERSION`. Preserved historical evidence
may continue to quote the former name when it describes an exact earlier
revision; it must not be presented as current truth.

This Decision completely replaces `DSET-DECISION-OPS-006`. The predecessor
remains immutable and discoverable through its lifecycle and replacement
relation.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle event.
