# Design — {{title}}

## Boundaries

Define domain ownership, interfaces, dependencies, non-goals, and internal HOW.
Do not restate observable Requirements or externally authoritative Contracts.

## State and durability

| Concern | Authority | Writer model | Refresh boundary | Failure/recovery proof |
|---|---|---|---|---|
| Define each durable concern | One owner | Single/concurrent | When readers refresh | Test/evidence ID |

## Supportability

Define risk-scaled evidence, correlation/deploy identity, safe diagnostics, data controls, runbook, escalation, and rollback or justify not applicable.

## Decisions

Link only consequential accepted choices among valid alternatives, including
their rationale, trade-offs, and consequences. Do not create a Decision for
every implementation detail or observable edge case.
