+++
artifact_type = "specification"
artifact_subtype = "architecture"
artifact_id = "{{project_key}}-SPECIFICATION-{{sequence}}"
llm_session_ids = []
+++

# {{structure_kind}} architecture — {{name}}

Show the main functions, capabilities, or components immediately owned by this
feature or layer. Link behavior and implementation owners instead of copying
their rules.

```mermaid
flowchart TB
    OWNER["{{name}}"]
    FUNCTION_A["{{function_a}}"]
    FUNCTION_B["{{function_b}}"]

    OWNER --> FUNCTION_A
    OWNER --> FUNCTION_B
```

Record cross-boundary connections after every node is defined.
