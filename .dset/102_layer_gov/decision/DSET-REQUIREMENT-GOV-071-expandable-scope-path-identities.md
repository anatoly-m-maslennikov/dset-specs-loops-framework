+++
artifact_id = "DSET-ATOMIC-RECORD-227"
semantic_id = "DSET-REQUIREMENT-GOV-071"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Governed artifact IDs and filenames use <PROJECT>-<SCOPE_PATH>-<ARTIFACT_TYPE>-<NNN>-<summary>, where SCOPE_PATH is an optional, registered, ordered, and extensible sequence that may represent layers, features, layers nested inside features, features nested inside layers, or future project-defined scope axes."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A single ordered scope path preserves readable identities without hard-coding the framework to only layers or features, while keeping future structural axes extensible."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "relates_to"
target = "DSET-DECISION-GOV-034"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-064"
+++

# Requirement — Use expandable scope paths in artifact identities

The canonical governed-artifact identity and filename shape is:

```text
<PROJECT>-<SCOPE_PATH>-<ARTIFACT_TYPE>-<NNN>-<summary>.md
```

`SCOPE_PATH` is optional. When present, it contains one or more registered
scope segments ordered from the broader parent scope to the narrower child
scope.

Supported scope paths include:

- one layer;
- one feature;
- a layer nested inside a feature;
- a feature nested inside a layer; and
- future project-defined scope axes and deeper registered scope paths.

Project-level artifacts omit `SCOPE_PATH`. Projects that disable the optional
project prefix also omit `PROJECT`.

The scope path never changes the numbering axis. Numeric sequences remain
project-wide for each concrete artifact type or subtype selected by the
project naming policy. Layers, features, nesting depth, folders, and scope
paths never restart a sequence.

Every scope segment and parent-child scope relationship is registered in
`dset_settings.toml`. A scope path must match that registry exactly. Artifact
type tokens and other reserved identity tokens cannot be reused as scope
segments.

The first implementation of this Requirement must perform one complete
governed identity migration. It updates active and archived IDs, filenames,
relations, evergreen references, settings, implementation references,
evidence, and commit provenance together. The project must not retain the
previous identity order as a second accepted naming vocabulary.
