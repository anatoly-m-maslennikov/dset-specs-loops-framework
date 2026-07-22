+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-180"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-SKILL-015"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "Every operator input in a DSET-governed project is classified and emitted as one or more typed atomic artifacts before its requested consequences are implemented."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Immediate atomization prevents accepted operator intent from remaining only in volatile conversation history and makes later implementation, compilation, and provenance complete."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-050"
+++

# Requirement — Atomize every operator input before implementation

Each operator input is intake. Before implementing its consequences, DSET
classifies the input by semantic meaning and emits one or more immutable
Decision, Question, Problem, or QA atoms. Multiple independent claims become
linked sibling atoms; the workflow or requested next action never determines
their Type.

The current artifact-creation strictness still applies. When an immutable
claim is not precise enough to emit, DSET asks focused questions and stops the
requested consequence until the input can be recorded safely.
