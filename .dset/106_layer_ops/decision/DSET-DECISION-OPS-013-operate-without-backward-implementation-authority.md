+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-175"
type = "decision"
semantic_id = "DSET-DECISION-OPS-013"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "OPS consumes and evaluates implemented supportability surfaces after implementation and routes deficiencies upstream without directly governing implementation technique."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Keeping OPS terminal prevents release and runtime concerns from creating backward authority into IMPL while preserving an explicit incident-to-fix loop through new artifacts."

[scope]
kind = "layer"
id = "ops"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-DECISION-GOV-031"
+++

# Decision — Operate without backward implementation authority

OPS owns acceptance and use of the supportability surface after implementation:
CI delivery, release, publication, runtime evidence, investigation, retention,
access, deletion, containment, recovery, escalation, and hosted proof.

IMPL owns how code emits diagnostic data, exposes safe diagnostics, implements
rollback hooks, or otherwise realizes upstream supportability requirements.
When OPS finds the realized surface missing or insufficient, it emits a
Problem, Question, Requirement, or Decision for the appropriate upstream owner
and waits for a later implementation. OPS never directly prescribes or mutates
implementation technique.
