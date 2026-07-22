# Artifact authoring rules

## Universal rules

1. Start with the answer, rule, contract, or decision; context follows only when it helps application.
2. Give each governed carrier one primary `artifact_type`, at most one allowed
   direct `artifact_subtype`, owner, and owning question. Give each atomic
   artifact a separate semantic Type, optional allowed semantic subtype, and
   authority boundary.
   Classify the smallest independently reviewable primary claim. Split
   multi-head statements into linked sibling atoms; if an irreducible claim
   remains subtype-ambiguous, use its general Type and raise a Question when
   the ambiguity matters.
3. Determine Type and subtype from semantic content—not from a workflow,
   queue, skill, tool, host, filename, folder, or intended next action. Keep
   Type separate from document and lifecycle role.
4. State scope, non-goals, applicability, and failure behavior where ambiguity would change implementation or operations.
5. Link to another owner instead of copying its rule. Summaries are navigation aids and must identify the authoritative source.
6. Keep current truth separate from proposed changes, rationale, procedures, and historical evidence.
7. Use GitHub-portable Markdown and resolving relative links. Avoid private paths, editor-specific links, and hidden context.
8. Order content for top-to-bottom comprehension. Define terms before relying on them.
9. Prefer a small table, checklist, or example only when it makes the owning rule easier to apply.
10. Prompt every Decision for a concise rationale. Other atomic artifacts may
    include rationale when it improves review, support, or later replacement.
    Rationale is recommended but optional; omission alone is never invalid.
    Keep normative claims, lifecycle state, and evidence in their canonical
    owners rather than hiding them in explanatory prose.
11. Keep the governed atom distinct from its real-world subject, operator
    acceptance or other lifecycle act, record or file carrier, performed work,
    result, evidence, gate disposition, and derived Verification. A single
    stored record may link several of these roles but must not collapse their
    meanings.
12. Name new artifact IDs and files with their primary artifact type by
    default. Keep the optional artifact subtype in metadata. Enable subtype
    tokens only through the independent
    `artifacts.subtype_in_names` setting in `.dset/dset_settings.toml`; never
    rename an immutable or already stable identity merely
    because the setting changes.

## Analysis reports

- State the exact question, reviewed inputs, revision/currentness, assumptions,
  method, limitations, and conclusion or unresolved return.
- Use Solution Landscape to compare live options without selecting one;
  Root-Cause Analysis for a supported causal conclusion about an observed
  Problem; Proposal to recommend one candidate; Technical Investigation for
  facts, mechanisms, or feasibility; and External Audit Analysis to interpret
  an external audit.
- Keep source observations in Evidence Records. Link them rather than
  laundering interpretation into evidence.
- Do not treat a recommendation as accepted authority. Emit the accepted
  conclusion separately as a Decision, Question, Problem, or QA atom.
- Omit `artifact_subtype` when no direct subtype fits; never nest subtypes.

## Specifications

- Split the specification into the **what** and the **why**. The spec owns clean observable behavior; rationale or Decisions own motivation, alternatives, and trade-offs.
- Model the service or capability as **domain entities plus per-entity lifecycle state machines** before describing code or orchestration. Classify value objects, reference vocabulary, and external actors separately; do not invent entity lifecycles for concepts the system does not own.
- Give every owned entity with transitions a lifecycle state machine. For an owned entity with no meaningful transition, state its single stable state or record why lifecycle is not applicable.
- Order sections so each entity is **defined using only entities above it**. A forward section reference is a connection, not a definition.
- Define ownership and authority for state, inputs, outputs, effects, retries, idempotency boundaries, and recovery when applicable.
- Give every Requirement Decision a stable ID and scenario or acceptance
  check.
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
- Maintain a Mermaid view at every enabled structural level. The project view
  shows immediate feature groups, or features/layers when groups are absent;
  each feature-group view shows its features; each feature or layer view shows
  its main functions, capabilities, or components. Do not create placeholders
  for disabled levels.
- Keep each diagram one level deep, link its owners, and treat it as navigation
  or compiled architecture rather than authority.
- Own every claim at the narrowest common structural ancestor of its affected
  owners and subjects. Project-level truth is for genuinely cross-child or
  whole-project concerns, including shared Contracts and semantics, end-to-end
  QA, cross-cutting Invariants/Constraints, integration architecture, release
  readiness, and cross-owner Questions or Problems. High-level wording alone
  does not move a child-owned claim upward; parents link rather than duplicate.
- Store each consequential forward edge in `relations` using the narrowest
  canonical type. Use `child_of` only for refinement/decomposition,
  `override_of` only for a narrower exception, and `replacement_of` only for
  complete replacement. Derive reverse edges; never author them. Use
  `relates_to` only when machine traceability needs an association and no
  precise relation applies; ordinary citations remain links.
- For an evergreen projection, store one `projection_of` frontier per semantic
  Type and exact scope through the latest included immutable `ATOMIC-RECORD`.
  Do not list every compiled atom individually.
- Apply the project artifact-creation strictness before emitting an immutable
  atom. At high strictness, resolve every material ambiguity through focused
  questions first. At every strictness, check the immediately broader enabled
  scope and propose an eligible promotion without performing it automatically.
- Use `dset artifact assess ROOT --candidate CANDIDATE.json` for the
  deterministic read-only gate. An eligible promotion without operator
  disposition blocks emission; `keep_local` permits the assessed local
  candidate, while `promote` requires a newly assessed broader-scope candidate.

## Rationale and Decisions

- Rationale explains forces and trade-offs behind active normative truth; it links back without restating the full rule.
- A Requirement records a required result or obligation and may use a direct
  subtype for Constraint, Contract, User Story, Outcome, Scenario, or Invariant.
- A Decision records a material selected implementation, architecture,
  governance, or operating approach and has no subtype. Rationale is strongly
  recommended but remains optional in validation.
- Never edit an emitted Decision atom. Record later state in an append-only
  lifecycle event or emit an explicit absorbing successor while preserving the
  predecessor and both directions.
- Every active applicable Requirement or Decision is an atomic
  authority source. Compile its consequences into the owning evergreen spec or
  plan; when they differ, the Decision wins and the projection is stale until
  recompiled.

## Hubs

- Keep purpose, boundaries, and start routes concise.
- Link stable child areas, atomic-artifact folders, evergreen files, settings,
  and other long-lived non-atomic owners.
- Never list individual atomic artifacts or anything below `.dset_runtime/`.
- Do not hide normative rules or long explanations in a navigation page.

## Playbooks and runbooks

- State the trigger and preconditions, then give executable ordered steps.
- Include verification, failure handling, rollback/recovery, and stop conditions.
- Reference governing rules and evidence authorities; do not duplicate them.

## Evidence and changelogs

- Record the evaluated subject, revision or runtime identity, method, bounded result, and disposition.
- Preserve failures and corrective loops when they materially affected acceptance.
- Keep secrets, sensitive payloads, transient raw logs, and unbounded command output out of committed evidence.
