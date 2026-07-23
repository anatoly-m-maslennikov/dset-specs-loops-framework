+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-203"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQ-GOV-059"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Each project selects ask_always or auto_by_effective_priority conflict handling, defaults to ask_always, and automatic mode asks whenever structural comparison does not produce one unique eligible winner."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Operator confirmation is the safest general default, while an explicit project opt-in can remove routine structural conflicts without guessing through ties, incomparable scopes, or unsatisfiable authority."

[scope]
kind = "layer"
id = "governance"

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = false
local_context_required = true

[[relations]]
type = "child_of"
target = "DSET-REQ-GOV-058"
+++

# Requirement — Configure conflict selection mode

`.dset/dset_settings.toml` exposes exactly two conflict-selection modes:

- `ask_always` is the default. DSET classifies the conflict, explains the
  applicable authority and effective-priority calculation, and asks the
  operator before selecting a conflicting normative claim.
- `auto_by_effective_priority` may select automatically only when the conflict
  class permits selection and scope/layer-adjusted effective priority produces
  exactly one winner. Equal effective priority, the same structural level,
  unknown or incomparable scope, uncertainty, or multiple winners asks the
  operator.

The mode governs only selectable normative conflicts. Deterministic lifecycle
and role dispositions—such as absorption, an explicit applicable override,
stale projection routing, evidence affecting assurance, or implementation
drift creating a Problem—continue without pretending they are operator choices.
Mutually unsatisfiable external obligations always stop for operator or
external resolution; automatic mode cannot report false compliance.
