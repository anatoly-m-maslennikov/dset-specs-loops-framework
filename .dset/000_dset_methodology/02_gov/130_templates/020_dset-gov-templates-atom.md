---
artifact_type: "{{artifact_type}}"
artifact_subtype: "{{optional_direct_subtype}}"
artifact_id: "{{semantic_artifact_id}}"
scope_path: []
priority: medium
llm_session_ids: []
relations:
  - type: relates_to
    targets:
      - "{{related_artifact_id}}"
---

# {{title}}

State exactly one independently reviewable primary claim. The registered
`artifact_type` and optional direct `artifact_subtype` derive its Revision
mode, Content role, and Governance locus; do not repeat those coordinates.

Delete optional empty properties, including `artifact_subtype` and `relations`.
Use one relation entry per relation kind and put all targets of that kind in
its `targets` list.

## Rationale (recommended, optional)

Explain why this atom is emitted, scoped, or prioritized as written when that
context will materially help review or later replacement.

After emission, seal this carrier with `dset atom seal --file PATH`. Later
semantic changes require a successor atom; never edit the atom. Move a closed,
replaced, resolved, or withdrawn atom byte-for-byte into its adjacent
`archive/`.
