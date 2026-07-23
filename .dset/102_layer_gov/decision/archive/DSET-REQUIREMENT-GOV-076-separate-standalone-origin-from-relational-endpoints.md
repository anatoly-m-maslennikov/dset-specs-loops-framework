+++
artifact_id = "DSET-ATOMIC-RECORD-234"
semantic_id = "DSET-REQUIREMENT-GOV-076"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET classifies all governed artifacts by artifact type and content role; standalone artifacts additionally use internal or external authority origin, while relational artifacts omit authority origin, declare two or more typed endpoints, and appear only in the relational matrix. Contract is always relational."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A Contract is defined by the scopes or parties it binds rather than by one internal or external owner, so forcing it into an ownership cell destroys the distinction between artifact origin and endpoint structure."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-074"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-075"
+++

# Requirement — Separate standalone origin from relational endpoints

Every governed artifact declares:

```toml
artifact_type = "atomic"    # atomic | evergreen | maintained
content_role = "definition" # definition | rationale | method | implementation | observation
relation_shape = "standalone" # standalone | relational
```

Standalone artifacts additionally declare:

```toml
authority_origin = "internal" # internal | external
```

Relational artifacts do not declare `authority_origin`. They declare at least
two typed endpoints:

```toml
relation_shape = "relational"

[[endpoints]]
role = "consumer"
target = "APP-FEATURE-A"
origin = "internal"

[[endpoints]]
role = "provider"
target = "EXTERNAL-SYSTEM-B"
origin = "external"
```

Endpoint origins describe the participating subjects. They do not collapse
the relational artifact into one ownership value.

The primary matrix contains only standalone artifacts and shows
`internal | external` inside each artifact-type and content-role cell.

The relational matrix contains only relational artifacts and shows their
required endpoint roles. Shared, between, or mixed ownership never appears in
the primary matrix.

Contract is always relational. It appears only in the relational matrix under
its artifact type and `definition` content role.
