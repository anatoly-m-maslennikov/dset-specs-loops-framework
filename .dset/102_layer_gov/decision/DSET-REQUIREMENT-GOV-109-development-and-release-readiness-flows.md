---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-109
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-066"
---

# Requirement — Separate development and release-readiness flows

Development is the default flow:

```text
active atomic authority
→ Test and Evaluation Plans
→ implementation
→ executable Tests and Evaluations
→ factual Observations and Evidence
→ development Verification
```

Development consumes active atomic authority plus any enabled current
maintained views. It does not require every enabled view to refresh after every
new atom unless that view's own gate requires currentness.

Release readiness is mandatory before a Version can be declared ready:

```text
all active atomic authority
→ optional atomic refactoring when overlap warrants it
→ refresh every required maintained view
→ detect conflicts
→ resolve conflicts through new atomic authority
→ repeat to a fixed point
→ reconcile implementation and assurance
→ execute Tests and Evaluations at the exact candidate head
→ fresh Evidence and Verification
→ Readiness Record
```

Conflict resolution never edits an accepted atom. Any applicable code,
configuration, Test, Evaluation, or maintained-view change after an assurance
run makes the affected release evidence stale.

`.dset/dset_settings.toml` records `development` as the default workflow mode
and `release_readiness` as the mandatory pre-release mode.

## Primary claim

Development may proceed atomic-first, while release readiness must reconcile
all active authority, required maintained views, implementation, and fresh
assurance to one exact-head fixed point.

## Rationale

The successor removes retired compilation and Evergreen terminology while
preserving the different currentness needs of ordinary development and
release.
