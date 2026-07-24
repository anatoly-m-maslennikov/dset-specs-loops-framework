+++
artifact_id = "DSET-ATOMIC-RECORD-067"
semantic_id = "DSET-TEST-PLAN-SKILL-016"
revision_mode = "atomic"
content_role = "method"
governance_origin = "external"
relation_shape = "standalone"
scope_path = ["layer:skill"]
status = "accepted"
priority = "high"
authority = "external:skill-refactor-audit"
claim = "Deterministic installation tests require one package-local launcher identity for every executable DSET instruction and prove shell-safe macOS, Linux, native Windows, and WSL rendering without ambient PATH."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-SKILL-011"
+++

# Test Plan — Prove one portable installed launcher

Rendered wrapper and governance instructions must contain no bare executable
fallback. Exact argv or host-native launcher forms must remain correct for
paths with spaces and shell metacharacters on every declared platform.

This Test definition is immutable. Runs and evidence are separate.
