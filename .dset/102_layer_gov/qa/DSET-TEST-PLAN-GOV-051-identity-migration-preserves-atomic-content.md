+++
artifact_id = "DSET-ATOMIC-RECORD-207"
semantic_id = "DSET-TEST-PLAN-GOV-051"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "A deterministic migration check proves canonical identity closure while preserving every atomic artifact's non-identity governed content."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-DECISION-GOV-034"

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-060"
+++

# Test Plan — Preserve atomic content during identity migration

For each migrated atomic artifact, compare the pre-migration and post-migration
carriers after normalizing only:

1. the artifact's canonical semantic ID;
2. its carrier filename and identity-bearing heading label;
3. relation and lifecycle target identifiers;
4. canonical identifier references in governed text; and
5. generated or compiled references derived from those identifiers.

The normalized carriers must be equal. The migrated repository must contain no
identifier using a retired short kind, no alias lookup for one, no duplicate
canonical identity, and no unresolved relation or lifecycle target.
