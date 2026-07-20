---
artifact_type: delivery
artifact_subtype: release_plan
artifact_id: "{{project_key}}-DELIVERY-{{sequence}}"
version_scope_ref: "{{project_key}}-DELIVERY-{{version_scope_sequence}}"
proposed_version: "{{proposed_version}}"
status: preparing
llm_session_ids: []
---

# Release Plan — {{proposed_version}}

## Transition

- **Protected base ref/SHA/version:** pending
- **Candidate SHA:** pending
- **Release class:** pending
- **Release-owning Change:** pending
- **Participating Changes:** pending

## Included scope

Link the exact accepted Changes and any justified exclusions. This plan cannot
widen the referenced Version Scope.

## Execution and recovery

Record preparation, integration, migration, rollback, publisher, tag pattern,
and retry/collision handling.

## Required gates

Link applicable Test, Evaluation, Verification, supportability, pilot,
distribution, and policy gates. The later Readiness Record owns their results
and the explicit release disposition.
