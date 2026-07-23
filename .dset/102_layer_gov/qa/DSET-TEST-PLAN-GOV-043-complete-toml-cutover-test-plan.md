+++
artifact_id = "DSET-ATOMIC-RECORD-075"
semantic_id = "DSET-TEST-PLAN-GOV-043"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic tests prove complete lossless TOML cutover of every DSET-owned YAML artifact and Markdown YAML-frontmatter carrier with reference closure, rollback parity, and second-run idempotency."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A zero-YAML claim is valid only when every historical edition, link, seal, and normalized value is preserved in the new representation."
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-040"

[[relations]]
type = "replacement_of"
target = "DSET-TEST-PLAN-GOV-038"

[[relations]]
type = "replacement_of"
target = "DSET-TEST-PLAN-GOV-040"

[[relations]]
type = "replacement_of"
target = "DSET-TEST-PLAN-GOV-041"
+++

# Test Plan — Complete the all-TOML artifact cutover

The repository and migration suites require zero `.yaml` or `.yml` files under
`dset/` and zero DSET Markdown YAML-frontmatter carriers. Every former
standalone YAML edition has one distinct adjacent `<stem>.legacy.toml` envelope
unless parsed equality permits the current owner to serve both roles.

The transition ledger covers every changed carrier exactly once. Normalized
values, selector fragments, Markdown bodies, physical links, classifications,
current owners, generated views, and the bootstrap bundle remain valid. The
transaction rejects collisions, incomplete mappings, stale input, partial
resealing, semantic drift, loss, broken references, and rollback mismatch.
Preview and apply are both no-ops after cutover.

JSON Schema and other externally prescribed formats remain outside this Test.
This Test definition is immutable; runs and Evidence Records are separate.
