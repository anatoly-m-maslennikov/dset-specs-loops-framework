+++
artifact_id = "DSET-ATOMIC-RECORD-107"
semantic_id = "DSET-REQUIREMENT-GOV-043"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "A DSET project separates committed control state under .dset, ignored resumable runtime state under .dset_runtime, and disposable scratch workspaces under the host temporary root."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Control truth, resumable operational state, and disposable process scratch have different authority, retention, and cleanup semantics and therefore require visibly distinct roots."
promotion = {}

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-042"
+++

# Requirement — Separate control, runtime, and scratch state

The canonical repository-local boundaries are:

- `.dset/` — committed DSET settings, governance, evergreen artifacts, atomic
  artifacts, Version records, schemas, templates, and generated views;
- `.dset_runtime/` — ignored, bounded, resumable project runtime state,
  including runs, session checkpoints, caches, readiness records, and recovery
  backups; and
- `/tmp/` on POSIX — disposable DSET process scratch and test workspaces that
  must be removed when their owning operation exits. Native Windows uses its
  operating-system temporary root because `/tmp` is not a portable Windows
  location.

Ambient POSIX `TMPDIR`, `TEMP`, or `TMP` values must not redirect DSET scratch
workspaces into the repository. Cleanup errors are failures, not ignored
success. A test or subprocess must leave no `dset-*` scratch directory in the
repository after normal completion or a handled failure.

Short-lived same-directory files or directories used exclusively to preserve
atomic publication may live beside their destination. They are transactional
swap state rather than resumable runtime or scratch workspaces, and must be
replaced or removed before the operation returns.

Persisted control and runtime paths are repository-root-relative. Markdown
links may remain relative to their owning file. Schema 1.0–1.2 layouts and the
schema 1.3 `.dset/runtime/` location remain read-only compatibility inputs;
current initialization and writes use `.dset_runtime/`.

This Requirement atom is immutable. Later correction requires a successor and
an append-only lifecycle event.
