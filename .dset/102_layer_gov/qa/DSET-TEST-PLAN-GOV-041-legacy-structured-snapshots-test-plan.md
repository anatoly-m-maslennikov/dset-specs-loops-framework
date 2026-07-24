+++
artifact_id = "DSET-ATOMIC-RECORD-063"
semantic_id = "DSET-TEST-PLAN-GOV-041"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic tests prove exact legacy-structured registration, preserved snapshot digests and links, TOML-only current reads, mutable-link rewrites, fail-closed drift and dual ownership, and idempotent cutover."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-DECISION-GOV-017"
+++

# Test Plan — Validate exact legacy structured snapshots

The migration and repository suites must keep every registered YAML byte and
historical Markdown link unchanged, emit and prefer its TOML current owner,
rewrite mutable references, and reject digest drift, missing owners, duplicate
or wildcard entries, unregistered pairs, legacy read fallback, mutable old
links, and unregistered new immutable links. A second migration is a no-op.

This Test definition is immutable. Runs and evidence are separate.
