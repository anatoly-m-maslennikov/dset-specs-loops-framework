+++
artifact_id = "DSET-ATOMIC-RECORD-245"
semantic_id = "DSET-REQUIREMENT-GOV-087"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET content_role includes inquiry for persisted artifacts whose primary contribution is an unresolved request for knowledge, choice, or clarification."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A Question is mandatory in DSET but is not honestly a Definition, Rationale, Method, Implementation, or Observation. FPF strict distinction requires inquiry to remain separate from both observed claims and accepted definitions."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-086"
+++

# Requirement — Inquiry Content Role

The allowed Content Roles are:

```toml
content_role = "definition"
# definition | inquiry | rationale | method | implementation | observation
```

`inquiry` means that the persisted artifact's primary contribution is an
unresolved request for knowledge, choice, or clarification.

An inquiry may concern any Entity of Concern and any lifecycle stage. Its
unresolved status does not make it an Observation, and the workflow used to
answer it does not make it a Method.

When an answer is accepted, the answer is represented by a new artifact with
its own appropriate Content Role. The original immutable inquiry may then move
to its archive.
