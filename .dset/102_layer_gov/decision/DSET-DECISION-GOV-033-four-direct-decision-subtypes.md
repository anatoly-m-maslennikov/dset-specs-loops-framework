+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-186"
type = "decision"
semantic_id = "DSET-DECISION-GOV-033"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Decision has four direct subtypes: requirement, constraint, contract, and implementation_decision, using the canonical new ID tokens REQ, CONSTR, CONTR, and IMPDEC respectively."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "All four artifacts are accepted directives but own different questions: required result, allowed-solution restriction, boundary obligation, or selected implementation approach. The compact tokens keep subtype-bearing atomic filenames readable."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "replacement_of"
target = "DSET-DECISION-GOV-032"

[[relations]]
type = "resolution_of"
target = "DSET-QUESTION-GOV-009"
+++

# Decision — Four direct Decision subtypes

DSET returns to one parent Decision Type for accepted project authority. It
permits exactly four direct subtypes:

| Subtype | Owns | New ID token |
|---|---|---|
| `requirement` | Required observable result, behavior, capability, quality, prevention condition, or obligation | `REQ` |
| `constraint` | Restriction on acceptable technologies, dependencies, environments, resources, formats, or operating limits | `CONSTR` |
| `contract` | Provider/consumer and compatibility obligations across a boundary | `CONTR` |
| `implementation_decision` | Material selected architecture, design, algorithm, data, tooling, or operating approach | `IMPDEC` |

An empty-subtype Decision remains the fallback for accepted authority that does
not fit one of these four precise kinds. Routine code detail remains
implementation and does not require an Implementation Decision atom.

Older immutable long-form Requirement, Constraint, Contract, Story, Outcome,
Scenario, and Invariant carriers are compatibility input. Their payloads and
IDs are never rewritten. New atoms use only the four subtype tokens above.

This Decision completely replaces `DSET-DECISION-GOV-032`; the predecessor is
removed from active authority by a separate append-only absorption event.
