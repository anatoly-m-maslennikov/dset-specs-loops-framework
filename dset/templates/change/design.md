# Design — {{title}}

## Boundaries

Define domain ownership, interfaces, dependencies, and non-goals.

## State and durability

| Concern | Authority | Writer model | Refresh boundary | Failure/recovery proof |
|---|---|---|---|---|
| Define each durable concern | One owner | Single/concurrent | When readers refresh | Test/evidence ID |

## Supportability

Define risk-scaled evidence, correlation/deploy identity, safe diagnostics, data controls, runbook, escalation, and rollback or justify not applicable.

## Decisions

Link accepted ADRs and rejected alternatives.
