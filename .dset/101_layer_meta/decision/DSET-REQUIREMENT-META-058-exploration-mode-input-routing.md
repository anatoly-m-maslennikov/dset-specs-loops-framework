---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-058
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-021"
      - "DSET-REQUIREMENT-META-036"
      - "DSET-REQUIREMENT-META-037"
---

# Requirement — Route uncertain input through Exploration Mode

Exploration Mode permits brainstorming, discussion, research, analysis,
comparison, terminology work, and structural modeling without creating or
changing governed artifacts.

DSET enters Exploration Mode when the operator's input primarily:

- asks for information, explanation, comparison, critique, alternatives, or a
  recommendation; or
- introduces an idea, explores it, or asks for feedback on it.

An explicit operator request to create or change governed state takes
precedence over question-shaped wording. Otherwise, Exploration Mode ends only
when the operator explicitly accepts a conclusion or requests its promotion.
DSET then emits only the minimum artifacts required to preserve the accepted
meaning. Any maintained view may refresh only after its atomic sources exist.

Whether a mode transition is announced is a downstream interaction-reporting
choice and does not change this routing.

## Primary claim

Question and idea input stays non-persistent in Exploration Mode until explicit
operator acceptance authorizes the minimum durable artifacts.

## Rationale

One rule now owns the mode boundary and its two automatic input routes without
conflicting with configurable silent or verbose reporting.
