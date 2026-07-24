+++
artifact_id = "DSET-ATOMIC-RECORD-277"
semantic_id = "DSET-REQUIREMENT-META-008"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "An operator-accepted DDL, file schema, API, protocol, host format, supported-platform interface, CI interface, dependency boundary, or comparable participant obligation is governed as an atomic relational Definition named Contract."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A boundary obligation must remain explicit and independently authoritative rather than becoming mutable implementation advice."

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-META-018"
+++

# Requirement — Contract boundaries

Every Contract declares its accepted source, relation kind, role-bearing
endpoints, direction, conformance, compatibility, priority, creation state, and
replaced predecessors. Implementation conforms to the Contract and cannot
rewrite it.
