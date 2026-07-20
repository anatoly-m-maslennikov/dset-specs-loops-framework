---
artifact_type: release_record
artifact_id: "{{project_key}}-RELEASE-RECORD-{{sequence}}"
version_scope_ref: "{{project_key}}-SPECIFICATION-{{version_scope_sequence}}"
release_plan_ref: "{{project_key}}-PLAN-{{release_plan_sequence}}"
readiness_record_ref: "{{project_key}}-READINESS-{{readiness_sequence}}"
released_version: "{{released_version}}"
published_at: pending
llm_session_ids: []
---

# Release Record — {{released_version}}

## Delivered summary

Describe the user-visible result and link the exact Changes, Decisions,
Requirements, Outcomes, and resolved Problems delivered by this version.

## Migration and compatibility

Record required actions, deprecations, compatibility boundaries, and known
limitations. State `none` explicitly when no migration is required.

## Publication identity

- **Protected merge SHA:** pending
- **Tag:** pending
- **Packages and digests:** pending
- **Publisher/forge release:** pending
- **Release workflow/run:** pending

## Evidence chain

Link the accepted Readiness Record, Release Plan, Version Scope, and bounded
publication evidence. This record is immutable after emission; corrections use
a higher release and a new Release Record.
