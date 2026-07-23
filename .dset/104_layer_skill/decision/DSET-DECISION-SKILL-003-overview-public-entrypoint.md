+++
artifact_id = "DSET-ATOMIC-RECORD-081"
semantic_id = "DSET-DECISION-SKILL-003"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:skill"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET publishes dset-overview as a supplemental read-only public skill over generated project health, while the existing sixteen lifecycle entrypoints and their routing model remain unchanged."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Operators need a discoverable helicopter view of artifacts, coverage, freshness, and open obligations without confusing observation with lifecycle routing or mutation."

[promotion]
affected_children = ["skill"]
applies_unchanged = true
local_context_required = false

[promotion.parent_scope]
kind = "project"
id = "dset-specs-loops-framework"

[[relations]]
type = "replacement_of"
target = "DSET-DECISION-SKILL-002"
+++

# Decision — Add a read-only Overview entrypoint

DSET publishes 17 public skills. Sixteen retain the lifecycle topology carried
forward from `DSET-DECISION-SKILL-002`: the catch-all `dset`, two bounded
pre-resolution exceptions, and direct wrappers for every stable lifecycle
mode. The seventeenth, `dset-overview`, is a supplemental read-only entrypoint.

`dset-overview` resolves the repository-local `overview` workflow, reads the
current generated project-health identity, and returns artifact and scope
counts, explicit coverage denominators and gaps, freshness, open obligations,
and a recommended governed handoff. It does not become a lifecycle mode, alter
mode precedence, refresh stale derived state, or perform the recommended work.

The wrapper remains thin and uses the same installed shared runtime,
repository/Work Area discovery, project-local governance, session continuity,
host distribution, integrity verification, and fail-closed boundaries as every
governed wrapper. This Decision completely replaces the public-surface claim
of `DSET-DECISION-SKILL-002` while retaining its sixteen lifecycle entrypoints.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle event.
