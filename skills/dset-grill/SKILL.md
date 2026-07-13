---
name: dset-grill
description: Turn ambiguous product or domain intent into explicit DSET vocabulary, boundaries, invariants, requirements, scenarios, proof obligations, and decision records. Use before specification acceptance when a feature request has unresolved branches, overloaded terms, hidden actors or states, unclear ownership, conflicting edge cases, or premature solution choices.
---

# DSET Grill

Clarify the domain before implementation planning. With explicit write authorization, write durable conclusions into the active DSET change; otherwise return a proposed artifact update and do not mutate the repository.

## Workflow

1. Locate the repository's visible `dset/` root and current change. Read `proposal.md`, delta specs, package domain/spec/contracts, and linked ADRs. Confirm write authorization before changing an existing artifact. If no change exists, propose a change ID; create it only when the user authorizes writes.
2. Separate accepted facts, explicit decisions, assumptions, unknowns, and solution guesses. Do not turn existing code behavior into a requirement without product evidence.
3. Establish ubiquitous language: actors, entities, value objects, states, transitions, invariants, commands, events, ownership boundaries, and terms that must not be conflated.
4. Stress each rule with empty, boundary, concurrent, retry, partial-failure, permission, migration, rollback, and recovery cases that apply. Ask the smallest high-leverage question that resolves each real branch.
5. Convert accepted decisions into stable requirement and scenario IDs under `specs/`. Route exact proof to `test-plan.md`; route variable or rubric-based proof to `eval-plan.md`. Keep the two artifacts separate.
6. Record material architectural or external-component choices as ADR candidates. Keep implementation details out of the domain unless they constrain observable behavior or ownership.
7. Run `dset check` or the portable equivalent `python -m dset_toolchain check` from the project root. Report unresolved branches explicitly.

## Output contract

When writes are authorized, produce or update only the owning artifacts:

- `proposal.md`: problem, outcome, scope, non-goals, risk, unresolved decisions;
- delta spec or package domain/spec: vocabulary, invariants, requirements, scenarios;
- test/eval plans: proof obligations designed before implementation;
- ADR links: accepted material decisions and alternatives.

Do not duplicate accepted rules across artifacts. Link to their owner.

## Stop conditions

Stop before solution selection or code when a domain branch can materially change the behavior, data owner, proof, security boundary, or rollout. Stop after the spec and proof obligations are explicit; implementation belongs to the accepted DSET plan, not this skill.
