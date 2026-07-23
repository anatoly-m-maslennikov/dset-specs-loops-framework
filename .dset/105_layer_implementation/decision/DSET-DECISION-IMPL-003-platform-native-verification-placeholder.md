+++
artifact_id = "DSET-ATOMIC-RECORD-172"
semantic_id = "DSET-DECISION-IMPL-003"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:implementation"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Verification command implementations replace exact argument tokens with platform-native executable paths without shell reparsing."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Placeholder expansion is an implementation technique required to realize TOOL portability, not post-implementation operational authority."
promotion = {}

[[relations]]
type = "replacement_of"
target = "DSET-DECISION-OPS-010"

[[relations]]
type = "child_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Decision — Platform-native verification placeholders

Verification command templates are tokenized before exact-token placeholders
are replaced. An argument equal to `{python}` becomes the current Python
executable as one direct subprocess argument, so Windows backslashes, spaces,
and other platform-native path syntax are never reparsed as shell text.

This Decision completely replaces `DSET-DECISION-OPS-010`.
