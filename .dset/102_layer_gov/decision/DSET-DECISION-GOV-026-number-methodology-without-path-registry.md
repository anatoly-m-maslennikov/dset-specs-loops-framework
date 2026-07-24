+++
artifact_id = "DSET-ATOMIC-RECORD-161"
semantic_id = "DSET-DECISION-GOV-026"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Every committed file and directory below .dset/000_dset_methodology uses a stable numeric prefix within its parent, and deterministic materialization derives those names without a durable source-to-carrier path registry."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "replacement_of"
target = "DSET-DECISION-GOV-024"

[[relations]]
type = "child_of"
target = "DSET-DECISION-GOV-025"
+++

# Decision — Number methodology without a path registry

The installed methodology keeps the accepted `00_project` through `05_ops`
layer roots. Every descendant entry uses a zero-padded numeric prefix unique
among its siblings. The materializer applies the governed numbering algorithm
directly and does not publish a source-path-to-installed-path registry.

Skills ignore the numbering when resolving an identity. They search the
project's `.dset` tree and require exactly one matching identity or unique
carrier name.

## Rationale

Numbering improves local reading order, while identity-based lookup prevents
that presentation choice from becoming a second authority or a persistent
coupling in settings.
