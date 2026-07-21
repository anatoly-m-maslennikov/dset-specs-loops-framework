+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-093"
type = "decision"
semantic_id = "DSET-DECISION-OPS-010"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "Verification command templates are tokenized before exact-token placeholders are replaced, so the current Python executable remains one platform-native subprocess argument."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The manifest owns portable command syntax while Python owns executable discovery; keeping those boundaries separate avoids reparsing an operating-system path as shell syntax."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "resolution_of"
target = "DSET-DEFECT-TOOL-008"

[[relations]]
type = "child_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Decision — Preserve platform-native verification placeholders

The aggregate verifier parses each repository-owned portable command template
into arguments first. It then replaces an argument equal to `{python}` with
the current `sys.executable` value. The executable path is passed directly to
`subprocess` and is never converted back into shell text.

The placeholder is deliberately token-shaped. Embedded interpolation remains
unsupported because it would make executable identity part of another
argument and reintroduce platform-specific quoting behavior.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle event.
