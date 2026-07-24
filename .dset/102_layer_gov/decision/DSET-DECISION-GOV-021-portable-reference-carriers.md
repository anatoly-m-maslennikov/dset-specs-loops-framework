+++
artifact_id = "DSET-ATOMIC-RECORD-118"
semantic_id = "DSET-DECISION-GOV-021"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "When recursive project truth is exactly the distributable framework truth, DSET records a repository-relative TOML reference carrier instead of duplicating bytes or relying on filesystem symlinks."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}
+++

# Decision — Use portable reference carriers

A reference carrier contains one repository-relative target, the target's
expected artifact role, and the reason the project reuses it. Readers resolve
the target within the same repository and fail closed on escape, absence,
cycles, or a role mismatch.

If project truth later diverges from framework truth, semantic compilation
replaces the reference with a project-owned evergreen specification or plan.

## Rationale

Git tracks symbolic links, but Windows checkouts may materialize them as plain
files or require elevated configuration. A small TOML reference is explicit,
portable, reviewable, and deterministic on macOS, Linux, Windows, and WSL.
