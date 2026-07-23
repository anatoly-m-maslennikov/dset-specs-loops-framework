+++
artifact_id = "DSET-ATOMIC-RECORD-239"
semantic_id = "DSET-REQUIREMENT-GOV-081"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Each occupied internal and external position in the standalone artifact matrix uses a distinct canonical Type name; Atomic + Implementation is represented by Commit for internal repositories and External Commit for externally governed repositories."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Distinct Type names make the matrix readable without requiring the authority-origin label to disambiguate two otherwise identical names, while Commit preserves the native Git concept for immutable implementation states."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-076"

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-079"
+++

# Requirement — Unique internal and external Type names

The standalone matrix contains only canonical Types. Concrete distinctions
remain direct subtypes and do not appear in the matrix.

Each cell contains at most one internal Type and at most one external Type.
When both positions are occupied, their canonical Type names must differ.

| Artifact type | Content role | Internal Type | External Type |
|---|---|---|---|
| Atomic | Definition | Decision | Constraint |
| Atomic | Rationale | Rationale | External Rationale |
| Atomic | Method | Implementation Decision | Mandate |
| Atomic | Implementation | Commit | External Commit |
| Atomic | Observation | Feedback | External Finding |
| Evergreen | Definition | Specification | — |
| Evergreen | Rationale | Rationale Synthesis | — |
| Evergreen | Method | Guidance | — |
| Evergreen | Implementation | — | — |
| Evergreen | Observation | View | — |
| Maintained | Definition | Version | Requirement Source |
| Maintained | Rationale | Note | Reference |
| Maintained | Method | Tool | Dependency |
| Maintained | Implementation | Implementation | Imported Asset |
| Maintained | Observation | Report | External Report |

Evergreen has no external Types because the project authors its compiled
projections. External inputs retain their own provenance and are represented
by Atomic or Maintained artifacts.

`Commit` and `External Commit` are Git commits. Their repository-qualified
SHAs are their canonical identities. They are not duplicated as Markdown
Atomic Artifacts and do not receive DSET sequence numbers.
