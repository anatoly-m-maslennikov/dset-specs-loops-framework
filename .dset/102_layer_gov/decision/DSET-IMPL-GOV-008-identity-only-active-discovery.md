---
artifact_type: implementation_decision
artifact_id: DSET-IMPL-GOV-008
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-DECISION-GOV-025"
      - "DSET-DECISION-GOV-028"
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-053"
---

# Implementation Decision — Discover active authority by identity

Every DSET skill begins at the target repository's `.dset` control root,
locates the unique settings carrier, and resolves requested artifact, rule,
document, and carrier identities within that bounded tree. Zero active matches
or multiple active matches stop.

Active discovery includes installed methodology, settings, active atomic
artifacts, and applicable maintained artifacts. It excludes every type-local
`archive/` subtree and never falls back to root framework source, inert legacy
material, completed migrations, a remote copy, or a global installation.

DSET-to-DSET references persist identities, not physical carrier paths. A tool
may retain a resolved path in memory for the current operation. Implementation
outside `.dset` may be located only after accepted authority identifies the
implementation subject.

## Primary claim

Skills resolve unique active identities only inside the current project's
`.dset`, exclude archives and legacy fallback, and never persist resolved
carrier paths as semantic references.

## Rationale

The merged successor preserves topology-independent discovery while aligning
current authority with type-local archives and the project-local control-plane
boundary.
