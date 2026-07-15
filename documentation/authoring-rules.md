# Artifact authoring rules

## Universal rules

1. Start with the answer, rule, contract, or decision; context follows only when it helps application.
2. Give each file one primary question, type, owner, and authority boundary.
3. State scope, non-goals, applicability, and failure behavior where ambiguity would change implementation or operations.
4. Link to another owner instead of copying its rule. Summaries are navigation aids and must identify the authoritative source.
5. Keep current truth separate from proposed changes, rationale, procedures, and historical evidence.
6. Use GitHub-portable Markdown and resolving relative links. Avoid private paths, editor-specific links, and hidden context.
7. Order content for top-to-bottom comprehension. Define terms before relying on them.
8. Prefer a small table, checklist, or example only when it makes the owning rule easier to apply.

## Specifications

- Split the specification into the **what** and the **why**. The spec owns clean observable behavior; rationale or Decisions own motivation, alternatives, and trade-offs.
- Model the service or capability as **domain entities plus per-entity lifecycle state machines** before describing code or orchestration. Classify value objects, reference vocabulary, and external actors separately; do not invent entity lifecycles for concepts the system does not own.
- Give every owned entity with transitions a lifecycle state machine. For an owned entity with no meaningful transition, state its single stable state or record why lifecycle is not applicable.
- Order sections so each entity is **defined using only entities above it**. A forward section reference is a connection, not a definition.
- Define ownership and authority for state, inputs, outputs, effects, retries, idempotency boundaries, and recovery when applicable.
- Give every requirement a stable ID and scenario or acceptance check.
- Keep implementation mechanisms out unless they constrain observable behavior, compatibility, safety, ownership, or operations.
- Design deterministic tests and applicable qualitative/probabilistic evals in separate artifacts before implementation.

When two entities are mutually related, define each independently first using shared earlier vocabulary, then describe the bidirectional connection in a later relationship section. Do not make either definition depend on an undefined future entity. As a review test, remove the forward sentence: if the current entity's identity or invariant becomes incomprehensible, the sentence was a disguised definition rather than a connection.

## Normative methodology and reference docs

- State the governing rule and its applicability before examples or citations.
- Name the owner of adjacent concerns and link to it instead of re-cataloging its rules.
- Keep reusable conventions in the normative file; move extended justification to rationale and repeatable steps to a playbook.
- Distinguish mandatory requirements, recommended defaults, optional patterns, and examples.
- Preserve stable document responsibilities when renaming or splitting files; provide migration links when authority moves.

## Architecture

- State goals, boundaries, components, ownership, dependency direction, and prohibited coupling.
- Separate accepted structural constraints from candidate designs and implementation batches.
- Link material choices to Decisions and behavioral constraints to specifications.
- Use diagrams only when relationships are harder to understand linearly.

## Rationale and Decisions

- Rationale explains forces and trade-offs behind active normative truth; it links back without restating the full rule.
- A Decision records a material choice in context, including rejected alternatives and consequences.
- Never edit an emitted Decision atom. Record later state in an append-only
  lifecycle event or emit an explicit absorbing successor while preserving the
  predecessor and both directions.
- An active applicable Decision is an atomic authority source. Compile its
  behavioral consequences into the owning evergreen spec; when they differ,
  the Decision wins and the projection is stale until recompiled.

## Hubs

- Keep purpose, boundaries, and start routes concise.
- Link stable child areas and owning documents, not every file generated below them.
- Do not hide normative rules or long explanations in a navigation page.

## Playbooks and runbooks

- State the trigger and preconditions, then give executable ordered steps.
- Include verification, failure handling, rollback/recovery, and stop conditions.
- Reference governing rules and evidence authorities; do not duplicate them.

## Evidence and changelogs

- Record the evaluated subject, revision or runtime identity, method, bounded result, and disposition.
- Preserve failures and corrective loops when they materially affected acceptance.
- Keep secrets, sensitive payloads, transient raw logs, and unbounded command output out of committed evidence.
