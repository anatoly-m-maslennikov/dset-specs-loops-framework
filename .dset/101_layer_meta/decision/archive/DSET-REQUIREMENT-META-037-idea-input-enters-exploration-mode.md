---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-037
scope_path:
  - "layer:meta"
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-021"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-036"
---

# Requirement — Idea input enters Exploration Mode

When the operator's input primarily introduces, explores, or asks for feedback
on an idea, DSET enters Exploration Mode silently.

Idea intent includes expressions such as “another idea,” “what if,” “maybe,”
“could we,” and comparable language that presents a candidate rather than an
accepted instruction. Detection is semantic rather than a literal substring
or punctuation rule. Mentioning the word “idea” while giving an explicit
instruction does not by itself make the instruction exploratory.

Entering the mode creates no governed artifact or governance commit. DSET may
discuss, compare, critique, research, and refine the candidate under the
ordinary Exploration Mode rules.

The operator exits Exploration Mode through an explicit instruction to accept,
finalize, record, apply, implement, or end the exploration. Only accepted
conclusions may then become the minimum necessary governed artifacts.

## Rationale

Ideas are candidate inputs rather than current project truth. Treating them as
accepted requirements immediately creates short-lived authority and discourages
open exploration. A silent semantic trigger preserves a natural conversation
while keeping durable governance explicitly authorized.
