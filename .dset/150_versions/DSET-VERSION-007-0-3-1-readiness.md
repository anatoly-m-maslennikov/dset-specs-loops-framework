+++
artifact_type = "version"
artifact_subtype = "readiness_record"
artifact_id = "DSET-VERSION-007"
version_scope_ref = "DSET-VERSION-001"
release_plan_ref = "DSET-VERSION-006"
candidate_sha = "a6738bfed4c222f8e984d615a20be4a6e0d56767"
disposition = "blocked"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Readiness Record — DSET 0.3.1

## Candidate

- **Candidate SHA:** `a6738bfed4c222f8e984d615a20be4a6e0d56767`
- **Observed at:** 2026-07-20
- **Release Plan:** `DSET-VERSION-006`
- **Version Scope:** `DSET-VERSION-001`

## Gate disposition

| Gate | Applicability | Result | Evidence | Blocker |
|---|---|---|---|---|
| Deterministic Tests | applicable | stale | `verification.md` | yes |
| Evaluations | applicable | pending | `eval-plan.md` | yes |
| Verification | applicable | stale | `verification.md` | yes |
| Supportability and delivery | applicable | pending | `verification.md` | yes |
| Native host and platform proof | applicable | pending | `verification.md` | yes |

## Blockers

The current branch has moved beyond the pinned candidate and retains open
Evaluation, hosted delivery, native-host, platform, dependency, and governance
implementation gates. Green historical evidence cannot authorize this release.

## Conclusion

**Disposition:** `blocked`

This record, not `verification.md`, owns the release decision for the pinned
candidate. Refresh the Release Plan, declaration, evidence links, and a new
exact-candidate Readiness Record before release preparation can pass.
