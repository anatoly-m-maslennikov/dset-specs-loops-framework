+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-195"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQ-IMPL-005"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET provides and applies a provider-neutral Agent Skills implementation profile whenever a skill is created or updated, including thin instructions, progressive disclosure, portable deterministic helpers, host adapters, security review, and skill-specific evaluation gates."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A mandatory reusable profile preserves the proven skill-refactor contract while preventing vendor-specific, token-heavy, unsafe, or untested skill changes from bypassing the same quality bar."

[scope]
kind = "layer"
id = "implementation"

[promotion]
affected_children = ["implementation"]
applies_unchanged = false
local_context_required = true

[promotion.parent_scope]
kind = "project"
id = "dset-specs-loops-framework"

[[relations]]
type = "child_of"
target = "DSET-REQ-001"
+++

# Requirement — Apply the Agent Skills profile

Every new or changed DSET skill must pass the selected Agent Skills profile
before its source is accepted, installed, distributed, or used as current
framework methodology.

The profile keeps `SKILL.md` focused on discovery, judgment, sequencing,
authorization, and stop conditions. Deterministic mechanics move to portable
scripts; static bulk moves to focused on-demand resources. The skill preserves
its behavioral contract, declares host-specific differences explicitly, and
does not rely on private memory, absolute machine paths, ambient packages, one
provider, or one operating system.

Each changed skill has representative evaluations for correct triggering,
non-triggering, ambiguous routing, isolation, coexistence, instruction
following, stop behavior, and output quality across every claimed host/model
configuration. Missing required profile or Evaluation coverage blocks the
skill change.
