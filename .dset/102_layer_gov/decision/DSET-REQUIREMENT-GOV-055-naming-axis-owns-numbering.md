+++
artifact_id = "DSET-ATOMIC-RECORD-188"
semantic_id = "DSET-REQUIREMENT-GOV-055"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Atomic artifact numbering follows the configured filename classification axis: type-only names use one project-wide sequence per Type, while subtype-bearing names use one project-wide sequence per direct subtype and one separate sequence for the Type's empty-subtype form."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The visible classification token and its sequence must describe the same population; restarting numbers by layer or feature would make the file list ambiguous and defeat project-wide lookup."
promotion = {}

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-030"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-054"
+++

# Requirement — The naming axis owns numbering

When atomic filenames expose only the semantic Type, allocate one monotonic
project-wide number sequence for that Type.

When atomic filenames expose the semantic subtype, allocate one monotonic
project-wide sequence for each subtype. The empty-subtype form has its own
sequence under the Type token. For Decision authority in this repository, the
independent sequences are `REQUIREMENT`, `CONSTRAINT`, `CONTRACT`, `IMPL`, and `DECISION`.

Layers, features, feature groups, folders, and lifecycle state do not restart a
sequence. Existing immutable IDs retain their original numbers; allocation
uses the current naming mode only for newly emitted atoms.
