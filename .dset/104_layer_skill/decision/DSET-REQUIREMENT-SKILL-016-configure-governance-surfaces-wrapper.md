+++
artifact_id = "DSET-ATOMIC-RECORD-269"
semantic_id = "DSET-REQUIREMENT-SKILL-016"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:skill"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET publishes one thin dset-configure skill for status, activation, deactivation, and recommendations instead of separate enable and disable skills."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "One configuration entrypoint keeps the public skill surface small and lets the deterministic tool own mechanical settings changes."

[promotion]
affected_children = ["implementation", "operations"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-TOOL-023"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-SKILL-002"
+++

# Requirement — Publish one dset-configure wrapper

`dset-configure` is one supplemental public skill with four operator intents:
status, activate, deactivate, and recommend. Separate `dset-enable` and
`dset-disable` skills are forbidden.

The wrapper resolves the target project's local governance, reports current
surface state, and invokes the deterministic `dset configure` command. It owns
no surface catalog, heuristic, threshold, settings-editing logic, or fallback
methodology.

Activation and deactivation require explicit write authorization and use the
tool's preview before execution. Recommendation remains read-only and advisory.
The wrapper stops after reporting the result; it does not create a selected
surface or perform another workflow automatically.
