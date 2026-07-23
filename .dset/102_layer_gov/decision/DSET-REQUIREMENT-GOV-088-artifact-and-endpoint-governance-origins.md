+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-246"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-088"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Every governed artifact declares its own governance_origin relative to the project boundary; relational artifacts additionally declare the independent origin of each typed endpoint."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The governor of a relational record and the origins of its participants answer different questions. Omitting artifact-level origin from relational records collapses governance of the relation with the provenance of its endpoints."

[scope]
kind = "layer"
id = "governance"

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-076"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-086"
+++

# Requirement — Artifact and endpoint governance origins

Every governed artifact declares:

```toml
governance_origin = "internal" # internal | external
```

Governance Origin identifies who controls the semantic content and currentness
of this artifact relative to the project boundary. It does not establish
truth, authority, authorship, storage, or provenance.

A Relational artifact also declares `relation_kind` and at least two typed,
role-bearing endpoints. Each endpoint independently declares its origin:

```toml
relation_shape = "relational"
relation_kind = "pull_request"
governance_origin = "internal"

[[endpoints]]
role = "source"
target = "EXTERNAL-CONTRIBUTOR-BRANCH"
origin = "external"

[[endpoints]]
role = "target"
target = "PROJECT-MAIN-BRANCH"
origin = "internal"
```

Direction follows from Relation Kind and endpoint roles. Relational structures
may be n-ary; they are not restricted to exactly two endpoints.

Artifact origin and endpoint origins never substitute for each other.
