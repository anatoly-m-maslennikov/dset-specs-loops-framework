# Methodology GOV specification

## DSET-REQUIREMENT-GOV-001 — Enforcement is language-neutral and profile-applied

The methodology must define six neutral gate categories and keep concrete tools, source scopes, thresholds, exclusions, and ratchets in versioned applied profiles.

**Scenario DSET-SCENARIO-GOV-001:** A Python project selects Python v1; a JavaScript/TypeScript project does not inherit Python line limits or tools.

## DSET-REQUIREMENT-GOV-002 — Change history is PR-traceable without a future SHA

The methodology must use a repository-qualified PR identity as the stable implementation link and keep the PR draft throughout archival. After fresh baseline verification and current-truth reconciliation, the change may move to a dated, explicitly incomplete archive candidate and be pushed so remote checks can inspect the real PR head. An evidence-only commit finalizes the archive after those checks pass. Missing PR identity keeps a change active; any later implementation or specification change invalidates prior readiness.

**Scenario DSET-SCENARIO-GOV-002:** The archived change links to the PR that owns the code diff and eventual merge result without attempting to store a merge SHA before it exists.

**Scenario DSET-SCENARIO-GOV-003:** A change with a pending PR identity cannot become an archive candidate. A pushed candidate remains unaccepted until final evidence is recorded, and a later implementation or specification edit requires verification and archive readiness to be refreshed.

## DSET-REQUIREMENT-GOV-003 — Public Markdown is portable

Public methodology must use ordinary Markdown links and GitHub-native alerts or collapsed details sections.

**Scenario DSET-SCENARIO-GOV-004:** A GitHub reader can navigate every local link and expand every collapsed section without an Obsidian renderer.

## DSET-REQUIREMENT-GOV-004 — Project truth uses a visible root

Committed project truth must live under the visible `dset/` root. Hidden `.dset/` is reserved for generated, local, cached, or other machine-owned state.

**Scenario DSET-SCENARIO-GOV-005:** `dset/README.md` exposes accepted truth, active changes, archive history, templates, and schemas, while no committed project truth is owned by `.dset/`.

## DSET-REQUIREMENT-GOV-005 — Package structure is proportional

The project manifest must register each package exactly once and must omit or null the global-truth root until cross-package ownership exists.

**Scenario DSET-SCENARIO-GOV-006:** A one-package project resolves `methodology` to `specs/packages/methodology` and reports `global_truth_root: null`.

## DSET-REQUIREMENT-GOV-006 — Standard changes expose complete proof structure

A standard change must contain exactly eight top-level document artifacts—proposal, test plan, eval plan, solution landscape, design, implementation plan, tasks, and verification—plus separate `specs/` and `proofs/` directories.

**Scenario DSET-SCENARIO-GOV-007:** Structural inspection counts the eight documents separately from the requirement-delta and evidence directories.

## DSET-REQUIREMENT-GOV-007 — Enforcement status is honest

Public metadata must name the selected enforcement profile and canonical command and must use explicit pending values until the corresponding executable assets exist.

**Scenario DSET-SCENARIO-GOV-008:** `documentation-v1-pending` and `canonical_command: pending` cannot be presented as an active executable gate.

## DSET-REQUIREMENT-GOV-008 — Contracts ship with proof fixtures

Versioned schemas, profile-aware templates, and valid/invalid fixtures must cover the project manifest, package truth, active and archived changes, separate test/eval artifacts, provenance, and traceability.

**Scenario DSET-SCENARIO-GOV-009:** The fixture runner accepts small, standard, failed-active, and archived cases and rejects missing-test, merged-test/eval, and missing-PR archive cases with their expected codes.

## DSET-REQUIREMENT-GOV-009 — Governed areas have explicit architecture

Every governed public artifact area must declare one purpose, owner, root, hub, and parent relationship. The repository root hub gives the helicopter view and routes to area hubs. Hubs are thin navigation surfaces, not owners of atomic rules or exhaustive manually duplicated indexes.

**Scenario DSET-SCENARIO-GOV-010:** A cold reader starts at `README.md`, reaches the documentation or methodology hub, and identifies the owning artifact without scanning unrelated files.

## DSET-REQUIREMENT-GOV-010 — Artifact types own different questions

DSET must define distinct types for navigation, normative rules, behavioral specification, architecture, rationale, decisions, procedures, proof plans, evidence/history, and agent workflows. Each artifact has one primary type and one owning question; secondary meaning is expressed through links rather than duplicated rule text.

**Scenario DSET-SCENARIO-GOV-011:** A design explanation moves to rationale, a repeatable sequence moves to a playbook, and the normative rule remains in one reference document linked by both.

## DSET-REQUIREMENT-GOV-011 — Authoring rules are type-specific

Universal rules must require answer-first writing, one primary question, explicit scope and authority, links instead of copied rules, and GitHub-portable Markdown. Specification rules must keep observable what separate from why, model domain entities and per-entity lifecycle state machines before code, and order definitions so every entity is defined only from earlier entities; a forward section reference is a connection, not a definition.

**Scenario DSET-SCENARIO-GOV-012:** A specification that uses an undefined downstream entity as part of an earlier entity's definition fails review even when it contains a forward link; the entity is reordered or the relationship is stated as a later connection.

## DSET-REQUIREMENT-GOV-012 — Documentation v1 is executable

The `documentation-v1` profile must provide a machine-readable governed-area registry and deterministic checks for profile identity, required hubs, unique area IDs/roots, valid owner/purpose/parent fields, reachable parent hierarchy, required hub sections, root-to-area navigation, and existing portable links. Qualitative authoring judgments remain evals rather than brittle keyword gates.

**Scenario DSET-SCENARIO-GOV-013:** Removing an area hub or pointing an area at a missing parent produces a stable diagnostic through `dset check`; debating whether rationale is sufficiently separated remains a rubric-based eval.

## DSET-REQUIREMENT-GOV-013 — The framework dogfoods artifact governance

This public repository must activate `documentation-v1`, expose documentation and methodology hubs, register its stable governed areas, and keep current governance separate from archived change evidence.

**Scenario DSET-SCENARIO-GOV-014:** The same canonical verification command validates Python v1 and documentation v1 without describing documentation as a programming language.

## DSET-REQUIREMENT-GOV-014 — DSET 0.3 rules are repository-owned

Every selected normative rule must resolve to one editable governing document inside the adopting repository. A framework template may seed the document, but after materialization the local document is authoritative and the template remains provenance rather than a live fallback.

**Scenario DSET-SCENARIO-GOV-015:** Editing the framework template after materialization does not change the adopter's resolved rules; editing its registered local governing document does.

## DSET-REQUIREMENT-GOV-015 — DSET 0.3 fails closed on invalid selected ownership

Missing, duplicate, cyclic, outside-root, or profile-incompatible selected rule ownership must stop before governed work and emit a stable diagnostic. A rule or profile explicitly marked not applicable with a valid reason must remain a successful disposition.

**Scenario DSET-SCENARIO-GOV-016:** A selected rule outside the repository stops with its stable code and path, while an unselected TypeScript profile in a documentation-only adopter passes as justified not applicable.

## DSET-REQUIREMENT-GOV-016 — DSET 0.3 identifies customization honestly

A locally changed materialized ruleset remains valid project truth but must identify itself as local/custom and preserve source profile/version provenance. It must not claim equivalence to the unchanged framework profile.

**Scenario DSET-SCENARIO-GOV-017:** Changing one normative local rule changes the resolved ruleset identity to custom while retaining the originating profile and version as provenance.

## DSET-REQUIREMENT-GOV-017 — DSET 0.3 gives every rule one owner

Every normative rule ID must resolve to exactly one editable governing document. Agent guidance, skills, templates, generated installations, indexes, summaries, and caches may link to that owner or reproduce derived metadata but must not become additional writable rule authorities.

**Scenario DSET-SCENARIO-GOV-018:** The registry rejects two governing documents claiming the same rule ID and accepts multiple navigation or generated surfaces that point to the single owner without restating its normative text.

## DSET-REQUIREMENT-GOV-018 — Intake routing uses three queues

`DSET-RULE-WORK-ITEMS` must expose only `problems`, `opportunities`, and `questions` through one project-owned `dset/scopes/gov/intake.yaml` registry in schema 1.2. Problems cover bugs, gaps, debt, and risks; opportunities describe improvements when nothing is wrong; consequential questions close through Decisions. Decision is both the entity and durable artifact and uses the full `DECISION` type. Accepted problems, opportunities, and Decisions enter a DSET Change, whose executable steps live in `tasks.md`. Decisions and Changes are artifacts, while GitHub Issues and Jira/support tickets are external tracker representations rather than additional semantic types.

**Scenario DSET-SCENARIO-GOV-019:** A production defect and a delivery risk become problems, optional release-note automation becomes an opportunity, and an unresolved API choice becomes a question linked to a Decision. Their accepted implementation steps appear only after a DSET Change creates tasks.

## DSET-REQUIREMENT-GOV-019 — IDs use project and optional layer grammar

The project prefix is `DSET`. Project-wide IDs use `DSET-<FULL-TYPE>-<NNN>`; layer-owned IDs use `DSET-<FULL-TYPE>-<LAYER>-<NNN>`, where `<LAYER>` is `META`, `GOV`, `TOOL`, `SKILL`, or `OPS`. Accepted methodology uses the full types `STORY`, `OUTCOME`, `REQUIREMENT`, `SCENARIO`, `INVARIANT`, `TEST`, and `EVAL`; intake, resolution, and authoritative-boundary artifacts use `PROBLEM`, `OPPORTUNITY`, `QUESTION`, `DECISION`, and `CONTRACT`. Numbering is independent per full type within the project-wide sequence or semantic layer. No alternate global prefix is used, and directory moves do not rename IDs.

**Scenario DSET-SCENARIO-GOV-020:** A project-wide question uses `DSET-QUESTION-001`; layer-owned accepted truth uses IDs such as `DSET-STORY-SKILL-001`, `DSET-OUTCOME-OPS-001`, `DSET-REQUIREMENT-GOV-001`, and `DSET-TEST-GOV-001`; a durable resolution uses `DSET-DECISION-001`. Directory-only refactors do not rename these identities.

## DSET-REQUIREMENT-GOV-020 — Artifacts declare evergreen, transactional, or implementation authority

DSET must distinguish evergreen current-truth artifacts, transactional atomic artifacts, and implementation-layer artifacts. Evergreen artifacts are updatable accepted truth such as specs, implementation plans, test plans, eval plans, contracts, runbooks, and governing rules. Transactional artifacts preserve bounded choices, questions, observations, evidence, and work history such as Decisions, Problems, Opportunities, Questions, proofs, Changes, releases, sessions, and runs. Implementation artifacts are code, tests, eval prompts/datasets, CI workflows, scripts, generated runtime assets, and configuration examples.

**Scenario DSET-SCENARIO-GOV-021:** A Decision and a Problem explain why behavior changes, the spec and plans own the current behavior and proof obligations, and the code/tests/eval prompts implement those owners without becoming a competing specification.

## DSET-REQUIREMENT-GOV-021 — Transactional artifacts compile into evergreen truth

Accepted Decisions, Problems, Opportunities, Questions, proofs, and other transactional artifacts must discharge their current behavioral consequences into the owning evergreen specs, plans, contracts, runbooks, or governing rules before they authorize implementation. Transactional artifacts remain provenance and rationale; generated traceability may show the relationship but cannot replace the evergreen owner.

**Scenario DSET-SCENARIO-GOV-022:** A resolved Question produces a Decision, the Decision updates the relevant spec and proof plans, the implementation cites that Decision, and review rejects a code-only change that leaves the evergreen spec stale.

## DSET-REQUIREMENT-GOV-022 — Commits and atomic artifacts retain provenance

Every commit that changes evergreen truth or implementation artifacts must name the Decision or Decisions it implements in its commit message body. If no Decision is required, the commit must name the authorizing Problem, Opportunity, Question, or Change. Each newly created or materially changed atomic artifact has an explicit session-provenance field: unique stable host-prefixed `llm_session_ids` when an LLM helped produce it, or an explicit empty list/`none` for human-only work. Missing provenance is invalid. This applies to Changes, intake items, Decisions, promoted proofs, skill-run records, and session checkpoints without making provenance authoritative.

**Scenario DSET-SCENARIO-GOV-023:** A commit body contains `Implements: DSET-DECISION-GOV-001`; the created Decision, Change, intake item, proof, run, and checkpoint shapes record the Codex session IDs that produced or materially revised them; and a human-only fixture passes only with explicit empty provenance.

## DSET-REQUIREMENT-GOV-023 — Rule authority and assurance are explicit

`DSET-RULE-ARCHITECTURE` must remain the dependency-free constitutional root
for repository governance. Every registered normative rule must resolve to one
applicable repository-local owner in the current profile edition and declare
separate `depends_on` and `precedence_over` relations. Both graphs must be
acyclic; registry order must not imply precedence; missing precedence targets
or unresolved conflicts must fail closed.

Decisions and provenance authorize and explain rule changes, while tests,
evals, reviews, and evidence assess reliance claims. None becomes rule
authority by existing or passing. Missing or stale assurance must leave only
the affected claim pending or stale and block its relying gate according to
risk; it must not silently erase an otherwise valid rule. Transactional
consequences must still compile into the evergreen governing artifact.

**Scenario DSET-SCENARIO-GOV-024:** An adopter rejects a precedence cycle and a
precedence target without a registered owner. A separate review keeps an
applicable rule authoritative when one proof becomes stale, marks only the
affected assurance claim stale, and blocks the release gate that relies on it.
