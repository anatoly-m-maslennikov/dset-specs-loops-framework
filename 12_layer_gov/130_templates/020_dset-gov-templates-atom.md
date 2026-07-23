+++
artifact_type = "atomic_record"
artifact_id = "{{project_key}}-ATOMIC-RECORD-{{carrier_sequence}}"
type = "{{type}}"
semantic_id = "{{semantic_id}}"
status = "proposed"
priority = "medium"
authority = "operator:{{operator_id}}"
claim = "{{one_primary_claim}}"
promotion = {}
llm_session_ids = []

[scope]
kind = "project"
id = "{{project_id}}"
+++

# {{title}}

State exactly one independently reviewable primary claim. QA requires the
direct `test_plan` or `evaluation_plan` subtype. Do not infer Type from this filename,
folder, workflow, or requested next action.

## Rationale (recommended, optional)

Explain why this atom is emitted, scoped, or prioritized as written when that
context will materially help review or later replacement.

After emission, seal this carrier with `dset atom seal --file PATH`. Later
state and priority changes use `dset atom event`; never edit the atom.
