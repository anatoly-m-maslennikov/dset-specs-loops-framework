+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-085"
type = "qa"
subtype = "test_plan"
semantic_id = "DSET-TEST-PLAN-OPS-017"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic verification checks that representative source, governance, and generated text paths resolve to the repository's LF worktree policy."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A source-level assertion catches accidental removal or narrowing of the checkout policy before hosted native-Windows proof is attempted."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "check_of"
target = "DSET-DECISION-OPS-008"

[[relations]]
type = "check_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Test Plan — Enforce portable text bytes

Use Git's attribute resolver for representative Python source, Markdown
governance, TOML migration authority, and generated trace paths. Every path
must resolve to `eol: lf` from repository-owned attributes, including when the
caller requests automatic CRLF conversion.

Run the carrier-transition suite and the complete DSET validation suite after
the repository policy is installed. Fresh hosted Linux, macOS, and native
Windows execution remains required before the platform gate closes.

This emitted Test atom is immutable. Later correction requires a successor Test
and append-only lifecycle event.
