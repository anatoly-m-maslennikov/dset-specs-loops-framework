---
artifact_type: specification
artifact_subtype: architecture
artifact_id: "{{project_key}}-SPECIFICATION-{{sequence}}"
llm_session_ids: []
---

# Project architecture — {{project_name}}

Show only the immediate enabled structural children. Prefer feature groups when
present; otherwise show features and/or layers. Do not invent empty levels.

```mermaid
flowchart LR
    PROJECT["{{project_name}}"]
    CHILD_A["{{child_a}}"]
    CHILD_B["{{child_b}}"]

    PROJECT --> CHILD_A
    PROJECT --> CHILD_B
```

Link each node to its owning hub below the diagram.
