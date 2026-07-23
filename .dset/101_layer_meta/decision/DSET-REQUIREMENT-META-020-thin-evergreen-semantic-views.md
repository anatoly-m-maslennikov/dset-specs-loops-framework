+++
artifact_id = "DSET-ATOMIC-RECORD-253"
semantic_id = "DSET-REQUIREMENT-META-020"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["project:dset-specs-loops-framework", "layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Evergreen documents are thin, reasoned semantic views over authoritative atomic records rather than compiled restatements; domain specifications contain a flow view, topologically ordered entity definitions, explicit entity lifecycle models, separated forward relations, and direct atomic provenance."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Thin views preserve a readable current model without duplicating atomic authority. Ordered definitions prevent circular meaning, lifecycle tables make behavior operational, and direct atomic links keep every summarized claim traceable."

[promotion]
affected_children = ["governance", "tool", "skill"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-048"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-072"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-019"
+++

# Requirement — Thin evergreen semantic views

An evergreen document is a mutable current view over authoritative atomic
records. Refreshing it requires semantic reasoning; DSET must not produce it by
concatenating, copying, or mechanically compiling atomic prose.

A domain specification view contains:

1. a Mermaid diagram of the domain flow;
2. domain entities defined in dependency order;
3. one lifecycle model for every stateful entity;
4. cross-entity relations separated from entity definitions; and
5. direct atomic-source IDs at each summarized claim, diagram element, and
   lifecycle row.

An entity definition may use only entities defined above it. A later entity may
be referenced only as a connection in the relations section, never as part of
the earlier entity's definition.

Each stateful entity records:

- identity and uniqueness;
- lifecycle invariants;
- the authority allowed to change status;
- statuses and their meanings;
- entry and exit criteria for every status;
- allowed and forbidden transitions;
- required evidence for transitions; and
- failure and recovery behavior when applicable.

Semantic provenance in an evergreen document targets atomic records only.
Navigation links may target hubs or other evergreen documents, but they do not
support a semantic claim.

Evergreen views refresh on demand after accepted atomic changes and before a
downstream gate requires current truth. Related active atoms may first be
refactored into immutable successors when overlap obscures the current model;
refactoring is optional and never edits an atom in place.
