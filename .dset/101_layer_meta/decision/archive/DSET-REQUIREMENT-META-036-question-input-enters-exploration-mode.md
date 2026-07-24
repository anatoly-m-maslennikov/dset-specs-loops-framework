---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-036
scope_path:
  - "layer:meta"
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-021"
---

# Requirement — Question input enters Exploration Mode

When the operator's input primarily asks for information, explanation,
comparison, critique, alternatives, or a recommendation, DSET enters
Exploration Mode silently.

Entering the mode requires no announcement, confirmation, command, or durable
artifact. While it remains active, the ordinary Exploration Mode prohibition
on creating or changing governed artifacts and governance commits applies.

Question intent is semantic rather than punctuation-based. A direct instruction
to record, accept, apply, implement, fix, or otherwise change governed state
does not become exploratory merely because it is phrased as a question. When
one input mixes genuine questions with an explicit change instruction, DSET
may answer and explore the questions, but it applies only the explicitly
authorized change.

The operator exits Exploration Mode through an explicit instruction to accept,
finalize, record, apply, implement, or end the exploration. Only accepted
conclusions may then become the minimum necessary governed artifacts.

This conversational trigger is distinct from the durable `question` artifact
type. Entering Exploration Mode does not itself create a Question artifact.

## Rationale

Operators commonly express brainstorming and design work as ordinary
questions. Treating those questions as immediate governed intake creates
short-lived artifacts before the candidate space is understood. Silent
Exploration Mode keeps the interaction natural while preserving explicit
authorization for durable project truth.
