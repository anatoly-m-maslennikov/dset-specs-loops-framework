+++
artifact_type = "version"
artifact_subtype = "readiness_record"
artifact_id = "{{project_key}}-VERSION-{{sequence}}"
version_scope_ref = "{{project_key}}-VERSION-{{version_scope_sequence}}"
release_plan_ref = "{{project_key}}-VERSION-{{release_plan_sequence}}"
candidate_sha = "pending"
disposition = "blocked"
llm_session_ids = []
+++

# Readiness Record — {{proposed_version}}

## Candidate

- **Candidate SHA:** pending
- **Observed at:** pending
- **Release Plan:** pending
- **Version Scope:** pending

## Gate disposition

| Gate | Applicability | Result | Evidence | Blocker |
|---|---|---|---|---|
| Deterministic Tests | applicable | pending | pending | yes |
| Evaluations | pending | pending | pending | pending |
| Verification | applicable | pending | pending | yes |
| Supportability and delivery | pending | pending | pending | pending |

## Blockers

List every open release blocker and owner. Green evidence never removes the
need for this explicit disposition.

## Conclusion

**Disposition:** `blocked`

Use exactly `ready` or `blocked`. Any candidate, scope, gate, or substantive
implementation change invalidates this record and requires fresh evidence.
