+++
artifact_id = "DSET-ATOMIC-RECORD-089"
semantic_id = "DSET-DEFECT-OPS-003"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "external"
relation_shape = "standalone"
scope_path = ["layer:ops"]
status = "accepted"
priority = "high"
authority = "external:github-actions-run-29835054261"
claim = "The project-health source digest orders Path objects with host-specific path comparison, so identical checkout bytes produce different digests on Windows and POSIX hosts."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Windows path comparison is case-insensitive while POSIX path comparison is case-sensitive; hashing files in native Path order therefore makes the derived health view platform-dependent."
promotion = {}

[[relations]]
type = "child_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Defect — Project-health ordering depends on the host path flavor

GitHub Actions run `29835054261` checked the same pull-request merge tree on
Linux, macOS, and native Windows. The Windows job reported a stale generated
project-health view even after the repository pinned text worktree bytes to LF.

The source digest uses `sorted(Path)` before hashing. Python compares Windows
paths case-insensitively and POSIX paths case-sensitively, so filenames that
differ in case order are hashed in a different sequence despite identical path
text and file bytes.

This emitted Defect atom is immutable. Resolution requires one canonical path
ordering, a deterministic regression Test, and fresh hosted proof.
