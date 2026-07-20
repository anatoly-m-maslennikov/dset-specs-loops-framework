---
artifact_type: plan
artifact_subtype: release_plan
artifact_id: DSET-PLAN-002
version_scope_ref: DSET-SPECIFICATION-001
proposed_version: 0.3.1
status: preparing
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Release Plan — DSET 0.3.1

## Transition

- **Protected base:** `main` at
  `b874504c25e42329eae19ed14f2b50a3d922d64e`
- **Candidate SHA:** `a6738bfed4c222f8e984d615a20be4a6e0d56767`
- **Release class:** `bootstrap`
- **Release-owning Change:** `DSET-CHANGE-SKILL-001`
- **Participating Changes:** `DSET-CHANGE-SKILL-001`

## Included scope

Deliver the DSET 0.3 foundation represented by `DSET-SPECIFICATION-001` and
this Change. Later work on the branch is outside the pinned candidate until the
declaration and this plan are deliberately refreshed.

## Required gates

The exact candidate requires deterministic Tests, applicable Evaluations,
Verification, supportability/delivery proof, host/platform proof, and one
explicit Readiness Record disposition. Publication remains post-merge and
bound to the protected merge SHA.
