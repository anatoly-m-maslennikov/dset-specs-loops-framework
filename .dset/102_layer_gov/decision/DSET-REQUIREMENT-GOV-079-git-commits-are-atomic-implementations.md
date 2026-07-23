+++
artifact_id = "DSET-ATOMIC-RECORD-237"
semantic_id = "DSET-REQUIREMENT-GOV-079"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "A Git commit is classified as atomic + implementation, uses its native commit SHA as identity instead of a DSET artifact sequence, and has internal or external origin according to the repository authority that produced it."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A Git commit is already an immutable, content-addressed implementation snapshot; duplicating it as a Markdown Atomic Artifact would create competing identities and provenance."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-076"
+++

# Requirement — Git commits are Atomic Implementations

A project-owned Git commit is classified as:

```toml
artifact_type = "atomic"
content_role = "implementation"
authority_origin = "internal"
```

An upstream commit from an externally governed repository is:

```toml
artifact_type = "atomic"
content_role = "implementation"
authority_origin = "external"
```

The commit SHA is the artifact's canonical identity. DSET does not duplicate
the commit as a Markdown Atomic Artifact and does not allocate it a DSET
sequence number.

DSET semantic artifacts link to commits through `implementation_of`, and
commit messages name the Requirements, Decisions, Problems, or other atomic
artifacts they implement.

Other content-addressed implementation snapshots, such as immutable package,
binary, or container-image digests, may use the same classification while
retaining their native digest identities.
