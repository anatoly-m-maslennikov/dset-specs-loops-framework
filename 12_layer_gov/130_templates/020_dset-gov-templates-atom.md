+++
artifact_id = "{{project_key}}-ATOMIC-RECORD-{{carrier_sequence}}"
semantic_id = "{{semantic_id}}"
revision_mode = "atomic"
content_role = "{{content_role}}"
governance_origin = "{{governance_origin}}"
relation_shape = "standalone"
scope_path = []
status = "proposed"
priority = "medium"
authority = "operator:{{operator_id}}"
claim = "{{one_primary_claim}}"
promotion = {}
llm_session_ids = []

+++

# {{title}}

State exactly one independently reviewable primary claim. Route it explicitly;
do not infer routing from its filename, display name, folder, workflow, or
requested next action.

## Rationale (recommended, optional)

Explain why this atom is emitted, scoped, or prioritized as written when that
context will materially help review or later replacement.

After emission, seal this carrier with `dset atom seal --file PATH`. Later
semantic changes require a successor atom; never edit the atom. Move a closed,
replaced, or withdrawn atom byte-for-byte into its adjacent `archive/`.
