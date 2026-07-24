---
artifact_type: procedure
scope_path: []
priority: medium
artifact_subtype: playbook
---

# Domain and specification authoring

**Rule ID:** `DSET-RULE-DOMAIN-SPEC`

## Workflow

1. Read applicable active atomic authority, the current thin maintained view,
   maintained artifacts, and current assurance. Separate accepted truth,
   observations, assumptions, unknowns, and solution guesses.
2. Establish ubiquitous language: actors, entities, value objects, commands, events, ownership boundaries, states, transitions, and invariants. Model a lifecycle for every owned entity with meaningful transitions.
3. Order definitions so each entity uses only vocabulary and entities defined above it. Treat a forward section reference as a connection, never as a hidden definition.
4. Stress applicable empty, boundary, concurrent, retry, partial-failure, permission, migration, rollback, and recovery cases.
5. Ask only questions whose answers can materially change observable behavior, authority, proof, security, or rollout. Stop before guessing such a branch.
6. Write each independently enforceable accepted Definition as one atomic
   Requirement, Constraint, or Contract according to its governance locus.
   Write a material internal HOW choice as an Implementation Decision. Keep
   rationale explicit when it materially improves interpretation, but do not
   hide another normative claim inside it.
7. Route exact proof to the deterministic test plan and variable or rubric-based proof to the eval plan.
8. After accepted atomic change, refresh the owning thin maintained view only
   when requested or required by a downstream gate. Summarize current meaning
   without duplicating atomic authority, and link every semantic location
   directly to its atomic sources. Mark affected downstream state potentially
   stale and continue through the canonical layer handoffs.

## Output

Create or update only the owning atomic records, thin maintained views, and
applicable maintained artifacts. Questions resolved for current work link to
their accepted resolution. Future intentions remain in a named Version Roadmap
until accepted into current atomic authority. Implementation begins only after
material current branches are resolved or removed from current scope.
