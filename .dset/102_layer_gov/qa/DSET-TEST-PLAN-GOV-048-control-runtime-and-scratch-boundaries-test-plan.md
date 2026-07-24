+++
artifact_id = "DSET-ATOMIC-RECORD-108"
semantic_id = "DSET-TEST-PLAN-GOV-048"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic tests prove distinct control, runtime, scratch, and atomic-publication boundaries without repository scratch leakage."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-043"

[[relations]]
type = "replacement_of"
target = "DSET-TEST-PLAN-GOV-047"
+++

# Test Plan — Verify control, runtime, and scratch boundaries

Run layout, settings, bootstrap, runtime, session, migration, distribution,
self-host, cross-platform, and full repository tests. Prove that:

1. current governed state resolves only below `.dset/`;
2. resumable run, session, readiness, cache, and recovery state resolves below
   ignored `.dset_runtime/` and never becomes project authority;
3. POSIX scratch workspaces use `/tmp` even when ambient `TMPDIR` points at the
   repository;
4. native Windows scratch workspaces use the native system temporary root;
5. normal and handled-failure paths delete their scratch workspaces;
6. self-hosting and bootstrap leave no `dset-*` scratch directory in the
   repository; and
7. same-directory atomic-publication staging is bounded to the transaction and
   cannot survive its return path.

The complete recursive verifier must pass after bootstrap and generated views
are refreshed. This Test atom is immutable; later correction requires a
successor Test and append-only lifecycle event.
