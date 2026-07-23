+++
artifact_id = "DSET-ATOMIC-RECORD-057"
semantic_id = "DSET-DEFECT-GOV-005"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "repository:fpf-review"
claim = "Governed files without direct metadata or a matching path rule can bypass the mandatory exactly-one artifact classification gate."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A MECE catalog is not complete when unclassified carriers silently disappear from validation and health."
promotion = {}

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-029"
+++

# Defect — Missing artifact classifications are skipped

Validation and health currently continue past governed files that have neither
direct classification metadata nor one applicable registry rule. Procedure
also lacks practical playbook/runbook path coverage.

## Completion condition

Every governed file resolves to exactly one classification or an explicit
registered exclusion. Missing, conflicting, nested, or invalid classification
fails closed, and health reports the complete governed inventory.
