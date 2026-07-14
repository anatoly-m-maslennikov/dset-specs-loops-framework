# Domain and specification authoring

**Rule ID:** `DSET-RULE-DOMAIN-SPEC`

## Workflow

1. Read accepted package truth, the active proposal/delta, contracts, decisions, and current evidence. Separate accepted facts, decisions, assumptions, unknowns, and solution guesses.
2. Establish ubiquitous language: actors, entities, value objects, commands, events, ownership boundaries, states, transitions, and invariants. Model a lifecycle for every owned entity with meaningful transitions.
3. Order definitions so each entity uses only vocabulary and entities defined above it. Treat a forward section reference as a connection, never as a hidden definition.
4. Stress applicable empty, boundary, concurrent, retry, partial-failure, permission, migration, rollback, and recovery cases.
5. Ask only questions whose answers can materially change observable behavior, authority, proof, security, or rollout. Stop before guessing such a branch.
6. Write each verifiable observable WHAT, outcome, or constraint as a Requirement. Put observable edge cases in Requirements/Scenarios, consequential alternative selection and rationale in Decisions, internal HOW in Design, build order in the implementation plan, and externally authoritative boundaries in Contracts.
7. Route exact proof to the deterministic test plan and variable or rubric-based proof to the eval plan.

## Output

Update only the owning proposal, domain/spec/contracts, separate proof plans, and linked decisions. Implementation begins only after unresolved material branches are closed or explicitly deferred.
