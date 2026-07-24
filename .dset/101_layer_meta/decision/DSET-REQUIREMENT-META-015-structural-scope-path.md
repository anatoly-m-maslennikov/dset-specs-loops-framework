+++
artifact_id = "DSET-ATOMIC-RECORD-284"
semantic_id = "DSET-REQUIREMENT-META-015"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Scope path is a project-relative extensible structural coordinate for layer, feature, feature group, Work Area, or configured compositions and is not a semantic routing axis; the current project is ambient and never repeated inside scope_path."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The repository already identifies the current project. Repeating that identity in every artifact adds no scope information and implies a cross-project address that DSET does not support."

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-META-018"
+++

# Requirement — Structural scope path

Artifacts with different scope paths may share the same semantic route. The
current project is ambient: a project-level artifact uses an empty scope path,
while a layer artifact begins with a coordinate such as `layer:meta`. Scope
composition remains extensible without expanding the routing matrix.
