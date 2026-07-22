+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-061"
type = "qa"
subtype = "test"
semantic_id = "DSET-TEST-GOV-040"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic tests prove byte-stable legacy package carriers, one TOML current successor, current-ID reconciliation, reader precedence, and fail-closed package cutover."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "check_of"
target = "DSET-DECISION-GOV-016"
+++

# Test — Validate native package-registry successors

The migration suite must preserve every selector-sealed legacy package YAML
digest, emit exactly one parseable sibling `package.toml`, include active
native IDs and current artifact paths, prefer TOML for current reads, and keep
legacy YAML as read-only historical input.

It must reject a missing or changed legacy carrier, an existing conflicting
TOML target, incomplete active-ID reconciliation, two writable current owners,
or readiness evidence whose preserved-input or final-output digest is stale.
A second apply is a no-op.

This Test definition is immutable. Runs and evidence are separate.
