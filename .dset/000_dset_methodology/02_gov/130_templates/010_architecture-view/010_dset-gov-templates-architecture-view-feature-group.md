+++
artifact_type = "specification"
artifact_subtype = "architecture"
artifact_id = "{{project_key}}-SPECIFICATION-{{sequence}}"
llm_session_ids = []
+++

# Feature-group architecture — {{feature_group}}

Show the features immediately owned by this group and their responsibility
boundaries. Do not expand into feature internals here.

```mermaid
flowchart LR
    GROUP["{{feature_group}}"]
    FEATURE_A["{{feature_a}}"]
    FEATURE_B["{{feature_b}}"]

    GROUP --> FEATURE_A
    GROUP --> FEATURE_B
```

Link each feature to its owning hub below the diagram.
