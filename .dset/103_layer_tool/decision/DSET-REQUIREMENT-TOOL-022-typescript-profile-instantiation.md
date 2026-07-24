+++
artifact_id = "DSET-ATOMIC-RECORD-017"
semantic_id = "DSET-REQUIREMENT-TOOL-022"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:tool"]
status = "accepted"
priority = "high"
child_of = ["DSET-REQUIREMENT-TOOL-021"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Requirement — Separate profile references from applied instances

DSET must distinguish an evidence-derived framework reference from an applied
project-owned enforcement profile. A reference records the pinned pilot and
reusable six-gate schema for comparison; it is not executable authority in an
adopter. An applied instance lives under the target repository's local TOOL
profile root, declares its reference origin, and owns that project's commands,
paths, thresholds, file populations, warning debt, blockers, promotion gates,
and evidence revisions.

Profile resolution must prefer a local applied instance and fail closed in an
adopter when only a distributed framework reference exists. The framework
source repository may resolve its own reference for bounded read-only
comparison. Neither role promotes OYOHA product, Obsidian, delivery, debt, or
supportability settings into TypeScript defaults.

## Rationale

The clean-upstream comparison proved that the six gate categories and
inspection mechanics generalize, while concrete commands, owners, counts,
thresholds, blockers, and delivery topology remain project-local. Encoding the
role boundary prevents a useful pilot snapshot from becoming accidental
cross-project authority.

This emitted Requirement is immutable. Later correction or replacement
requires a linked atom or append-only lifecycle event.
