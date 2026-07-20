+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-050"
type = "qa"
subtype = "evaluation"
semantic_id = "DSET-EVALUATION-GOV-028"
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "Cold readers can configure DSET from dset_settings.toml and correctly distinguish selectable behavior from project truth and governing definitions."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-037"

[[relations]]
type = "replacement_of"
target = "DSET-EVALUATION-GOV-027"
+++

# Evaluation — Judge settings discoverability

Without implementation knowledge, cold readers must find every active setting,
accepted value, default, effect, and practical example in
`dset_settings.toml`. They must correctly predict where to change an operator
preference and where to inspect project identity, topology, contracts, release
targets, or verification commands.

At least 90% of representative questions must be answered correctly, with no
authority-source error, no assumption that omitted settings are unavailable,
and no treatment of legacy `dset.toml` compatibility as a writable second
source.

This emitted Evaluation definition is immutable. Execution and evidence are
separate.
