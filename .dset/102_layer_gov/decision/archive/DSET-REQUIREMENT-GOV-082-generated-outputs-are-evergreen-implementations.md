---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-082"
scope_path:
  - "layer:gov"
priority: "high"
promotion:
  affected_children:
    - "governance"
    - "tool"
    - "skill"
    - "implementation"
    - "ops"
  applies_unchanged: true
  local_context_required: false
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-GOV-077"
  - type: "override_of"
    targets:
      - "DSET-REQUIREMENT-GOV-081"
---

# Requirement — Generated outputs are Evergreen Implementations

The standalone matrix cell is:

| Artifact type | Content role | Internal Type | External Type |
|---|---|---|---|
| Evergreen | Implementation | Generated Implementation | — |

A Generated Implementation is an executable or operative project artifact
compiled from current governed inputs. Examples include:

- generated HTML, JavaScript, or TSX dashboards;
- generated source code;
- generated configuration;
- generated schemas;
- other replaceable executable outputs.

The generator itself remains `Maintained + Implementation`. Its generated
output is `Evergreen + Implementation` when the output is reproducible from
the current governed inputs and is replaced rather than directly maintained.

If people directly maintain the output as a primary project asset, it is
`Maintained + Implementation` instead.

## Primary claim

Evergreen + Implementation uses the internal Type Generated Implementation for executable or operative outputs compiled from governed project inputs; examples include generated HTML, JavaScript, TSX, dashboards, source code, configuration, and schemas.

## Rationale

The maintained generator and its generated output have different revision semantics: the generator is directly maintained implementation, while the replaceable output is an evergreen implementation compiled from current governed inputs.
