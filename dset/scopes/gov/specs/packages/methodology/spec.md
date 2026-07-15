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

DSET must define distinct types for navigation, normative rules, behavioral specification, architecture, rationale, decisions, procedures, proof plans, evidence/history, and agent workflows. Each artifact has one primary type determined by its semantic content, owning question, and authority/lifecycle role where needed; workflow, queue, skill, tool, host, filename, and path never determine type. Secondary meaning is expressed through links rather than duplicated rule text.

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

`DSET-RULE-WORK-ITEMS` must expose only `problems`, `opportunities`, and `questions` through one project-owned `dset/scopes/gov/intake.yaml` registry in schema 1.2. Problems cover bugs, gaps, debt, and risks; opportunities describe improvements when nothing is wrong; consequential questions close through Decisions. Open Conflicts use their own governed register/view because they may be emitted by deterministic analysis and are not a fourth intake queue. Decision is both the entity and durable artifact and uses the full `DECISION` type. Accepted problems, opportunities, and Decisions enter a DSET Change, whose executable steps live in `tasks.md`. Decisions and Changes are artifacts, while GitHub Issues and Jira/support tickets are external tracker representations rather than additional semantic types.

**Scenario DSET-SCENARIO-GOV-019:** A production defect and a delivery risk become problems, optional release-note automation becomes an opportunity, and an unresolved API choice becomes a question linked to a Decision. Their accepted implementation steps appear only after a DSET Change creates tasks.

## DSET-REQUIREMENT-GOV-019 — IDs use project and optional layer grammar

The project prefix is `DSET`. Project-wide IDs use `DSET-<FULL-TYPE>-<NNN>`; layer-owned IDs use `DSET-<FULL-TYPE>-<LAYER>-<NNN>`, where `<LAYER>` is `META`, `GOV`, `TOOL`, `SKILL`, or `OPS`. Accepted methodology uses the full types `STORY`, `OUTCOME`, `REQUIREMENT`, `SCENARIO`, `INVARIANT`, `TEST`, and `EVAL`; intake, conflict, resolution, and authoritative-boundary artifacts use `PROBLEM`, `OPPORTUNITY`, `QUESTION`, `CONFLICT`, `DECISION`, and `CONTRACT`. Numbering is independent per full type within the project-wide sequence or semantic layer. No alternate global prefix is used, and directory moves do not rename IDs.

**Scenario DSET-SCENARIO-GOV-020:** A project-wide question uses `DSET-QUESTION-001`; an open layer-owned conflict uses `DSET-CONFLICT-GOV-001`; layer-owned accepted truth uses IDs such as `DSET-STORY-SKILL-001`, `DSET-OUTCOME-OPS-001`, `DSET-REQUIREMENT-GOV-001`, and `DSET-TEST-GOV-001`; a durable resolution uses `DSET-DECISION-001`. Directory-only refactors do not rename these identities.

## DSET-REQUIREMENT-GOV-020 — Artifacts declare authority and lifecycle roles

DSET must distinguish atomic authority sources, evergreen compiled projections,
transactional context/evidence, and implementation-layer artifacts. Accepted,
active, applicable Requirements, Contracts, Decisions, and other registered
normative atoms are authority sources. Evergreen specs, implementation plans,
test plans, eval plans, runbooks, and governing rules are updatable projections
compiled from those sources. Problems, Opportunities, Questions, Conflicts, proofs,
Changes, releases, sessions, and runs preserve work history or evidence without
becoming authority merely by existing. Implementation artifacts are code,
tests, eval prompts/datasets, CI workflows, scripts, generated runtime assets,
and configuration examples.

**Scenario DSET-SCENARIO-GOV-021:** An accepted Decision changes behavior, the
compiled spec and proof plans expose its current consequences, and code/tests/
eval prompts implement those sources without becoming competing authority. If
the Decision and compiled spec differ, the Decision wins and the spec is stale.

## DSET-REQUIREMENT-GOV-021 — Atomic authority compiles into evergreen projections

Accepted, active, applicable normative atoms must compile their current
behavioral consequences into the owning evergreen specs, plans, runbooks, or
governing rules. A compiled projection never outranks an active source atom. If
they differ, the source atom governs, the projection is stale, and its relying
release gate fails until deterministic recompilation succeeds. Transactional
context and evidence can motivate or assess a source but cannot replace one;
generated traceability shows the relationship without becoming authority.

Atomic artifacts are immutable. Editable drafts are not atoms. Emission fixes
the atom's ID, content, provenance, creation status, and links. Acceptance,
rejection, reopening, correction, withdrawal, or any other later change is a
new append-only lifecycle event from which current status is derived.

A replacement is a new atom with an explicit `absorbs` relation to older atoms.
Absorption is acyclic, validated, never inferred from time or numbering, and
removes the older atoms from the active authority set without deleting or
editing their history. The absorbing atom must carry forward or explicitly
replace every still-applicable consequence. Partial replacement leaves
unaffected older claims active and does not absorb the whole atom. Reverse
links and the active compilation set are derived views.

An atom with no active claims, open reliance, or unresolved lifecycle work is
fully retired and may move byte-for-byte into its artifact type's `archive/`
subfolder. Its ID and content digest remain unchanged, and the canonical ID
registry updates its location. Partial absorption does not qualify. Archived
atoms remain immutable history and are not deleted.

**Scenario DSET-SCENARIO-GOV-022:** A resolved Question produces a Decision, the
Decision compiles into the relevant spec and proof plans, and review rejects a
code-only change that leaves the evergreen projection stale. A later Decision
absorbs the earlier one explicitly; the original remains immutable provenance,
while only the successor participates in the active compilation set. After all
reliance closes, the original moves byte-for-byte to `archive/` and remains
resolvable by ID.

## DSET-REQUIREMENT-GOV-022 — Commits and atomic artifacts retain provenance

Every commit that changes an evergreen projection or implementation artifact must name the Decision or Decisions it implements in its commit message body. If no Decision is required, the commit must name the authorizing Problem, Opportunity, Question, or Change. Each newly emitted atomic artifact or append-only lifecycle event has an explicit session-provenance field: unique stable host-prefixed `llm_session_ids` when an LLM helped produce it, or an explicit empty list/`none` for human-only work. Missing provenance is invalid. A review, correction, or status change emits another linked record rather than revising the atom. This applies to Changes, intake items, Decisions, promoted proofs, skill-run records, and session checkpoints without making provenance authoritative.

**Scenario DSET-SCENARIO-GOV-023:** A commit body contains `Implements: DSET-DECISION-GOV-001`; the emitted Decision, Change, intake item, proof, run, checkpoint, and later lifecycle-event shapes record the Codex session IDs that produced them; a correction is a new linked event; and a human-only fixture passes only with explicit empty provenance.

## DSET-REQUIREMENT-GOV-023 — Rule authority and assurance are explicit

`DSET-RULE-ARCHITECTURE` must remain the dependency-free constitutional root
for repository governance. Every registered normative rule must resolve to one
accepted, active, applicable atomic source set and one repository-local compiled
governing document in the current profile edition and declare separate
`depends_on` and `precedence_over` relations. A source/document mismatch selects
the source, marks the document stale, and blocks reliance until recompilation.
Both graphs must be acyclic; registry order must not imply precedence; missing
precedence targets or unresolved conflicts must fail closed.

Active Decisions authorize and explain rule changes; provenance identifies
origin but does not authorize. Tests, evals, reviews, and evidence assess
reliance claims. None becomes rule
authority by existing or passing. Missing or stale assurance must leave only
the affected claim pending or stale and block its relying gate according to
risk; it must not silently erase an otherwise valid rule. Transactional
consequences must still compile into the evergreen governing artifact.

**Scenario DSET-SCENARIO-GOV-024:** An adopter rejects a precedence cycle and a
precedence target without a registered owner. A separate review keeps an
applicable rule authoritative when one proof becomes stale, marks only the
affected assurance claim stale, and blocks the release gate that relies on it.

## DSET-REQUIREMENT-GOV-024 — Project health is a transparent derived view

DSET must expose a generated project-health projection without making it a new
authority. It reports artifact counts by authority class, type, layer, status,
priority, and applicable Work Area; unresolved and automatically resolved
conflicts; unresolved Problems, Opportunities, and Questions; proof freshness;
and traceability coverage for Decisions compiled into
evergreen owners, Requirements connected to implementation and applicable
Tests/Evals, implementation commits connected to their authorizing artifact,
and proof plans connected to current evidence.

Every coverage result states its numerator, denominator, exclusions,
not-applicable, unknown, and stale counts and links back to canonical owners.
The view must not require a Decision for every Requirement, code for a
documentation-only Requirement, or an Eval where the eval plan declares one
not applicable. A portable Markdown renderer is the baseline public surface;
interactive renderers may consume the same derived model later.

**Scenario DSET-SCENARIO-GOV-025:** A repository reports 18 of 20 applicable
Requirements with current deterministic Test coverage, one justified
not-applicable Requirement, and one uncovered Requirement. The dashboard links
the uncovered row to its spec owner and does not inflate the score by creating
irrelevant Decisions, code, or Evals.

## DSET-REQUIREMENT-GOV-025 — External reviews are portable transactional evidence

DSET must support independent review across humans and agent hosts through a
portable review packet and report. The packet identifies exact commits and
artifacts, resolved rules, review criteria, requested scope, and allowed
effects. The report uses a mandatory envelope for reviewer/host identity,
available model/tool version, `llm_session_ids`, exact reviewed inputs, method,
observation time, priority, limitations, and stable finding IDs with effective
priority; the findings body may be free-form.

Every finding records evidence, confidence, impact, and proposed disposition.
Import or reconciliation must explicitly reject it with rationale, defer it,
or route it to an existing or new Problem, Opportunity, Question, Decision,
Change, evergreen owner, or proof obligation. Accepted consequences compile
into current truth and reopen the smallest affected proof closure. Neither the
report nor the reviewer may silently edit or authorize implementation.

**Scenario DSET-SCENARIO-GOV-026:** Codex produces a candidate commit and review
packet; Claude reviews that exact commit and returns a partly free-form report.
DSET preserves its provenance, routes one defect to a Problem, one ambiguity to
a Question, rejects one unsupported finding with rationale, updates accepted
truth for the accepted findings, and reruns only affected proof.

## DSET-REQUIREMENT-GOV-026 — Every governed artifact has one priority

DSET must use `priority` as its only generic ordered rank across atomic
authority, evergreen projection, transactional context/evidence, and
implementation artifacts. Every governed artifact declares priority directly
or inherits it through one visible canonical relation.
Implementation files may inherit from their owning Requirement, Decision,
Change, Test, or Eval instead of carrying duplicated inline metadata.

Problems, Opportunities, Questions, Changes, and tasks use priority as one
input to execution order. Dependencies, authorization boundaries, release
gates, and resource constraints may still require a different next action.
Impact, severity, likelihood, expected value, Contract obligations, Outcome
value, and gate status remain evidence that explains priority rather than
separate universal ranking fields.

Priority is also the default deterministic tie-breaker for declared resolvable
policy conflicts. The resolver first classifies the conflict. Immutable
external authority wins over mutable project truth. If two immutable
obligations cannot both be satisfied, priority may order remediation or
escalation but cannot report the lower-priority obligation as satisfied; the
conflict stops for an exception, boundary change, or external resolution.

For a comparable conflict whose governing profile permits selection, the
resolver applies any explicit specific precedence relation, then the higher
effective priority. The selected artifact governs only the conflicting claim
in the declared context; the other artifact remains valid elsewhere. Equal,
unknown, cyclically inherited, or incomparable priorities stop with the
unresolved artifacts and require a Decision or explicit precedence. Every
automatic resolution records the artifact IDs, effective priorities, priority
sources, conflict class, context, selected claim, and governing profile edition.

Every governed artifact pair is classifiable even when it is not a selectable
normative conflict. An accepted, active, applicable atomic source governs over
its stale evergreen projection and routes recompilation. An explicit absorption
relation selects the absorbing atom over absorbed predecessors before priority.
Test/Eval/review/proof evidence changes assurance and the relying gate instead
of overriding authority. Implementation that contradicts authority creates a
conformance Problem. Conflicting evidence follows its registered proof plan and
quality/freshness rules or stops for adjudication. A generated view that
contradicts its canonical source is stale. An implementation-only conflict
follows its traceable owner or stops when no owner or applicable rule exists.
Priority orders remediation across these classes but selects a normative claim
only when the profile permits selection.

The selected project governance profile owns one bounded priority scale, its
legend, inheritance rules, override rules, and escalation behavior and exposes
them to generated views. Missing effective priority remains `unknown` and is a
visible governance gap; type, file order, age, or a dashboard score must not
infer it. Reprioritization may change future conflict or queue outcomes, so it
records provenance and invalidates affected derived resolutions, but it does
not silently rewrite accepted artifacts.

**Scenario DSET-SCENARIO-GOV-027:** A project-owned output Contract permits one
of two formats and has higher priority than a preferred-format Requirement. The
Contract wins the declared field automatically and both artifacts remain valid
outside that conflict. Two immutable customer Contracts demanding mutually
exclusive values stop as unsatisfiable; priority orders remediation but does
not falsely mark either Contract satisfied. An active Decision that differs
from its compiled evergreen spec wins and makes that projection stale; a
failing Test changes assurance instead of competing by priority. An absorbing
Decision wins over its absorbed predecessor by explicit lifecycle relation,
not because it is newer. Equal selectable priorities stop for a Decision; no
outcome is inferred from document order.

## DSET-REQUIREMENT-GOV-027 — Problems, Questions, and Conflicts are distinct

DSET must classify an observed current or possible harmful state as a Problem,
missing knowledge, interpretation, or choice as a Question, and verified
incompatible applicable claims as a Conflict. A Conflict exists only when two
or more identified claims cover the same scope, concern, and effective time and
cannot all govern as written. Different wording alone is insufficient.

Classification depends on semantic content and authority/lifecycle role, never
on the workflow, queue, skill, tool, agent host, filename, or path that created,
discovered, routed, or resolves the artifact. A workflow may emit or link any
applicable type, but moving an artifact through a workflow cannot retype it.
Changed semantics require a new correctly typed artifact and explicit links.

An active atomic source versus its stale compiled projection routes
recompilation. A failing Test, Eval, or review changes assurance. Implementation
that contradicts authority creates a Problem. Contradictory evidence follows
its proof plan or creates a Question. None becomes a Conflict unless the
applicable claims themselves are verified incompatible.

Conflict is an immutable transactional entity using
`<PROJECT>-CONFLICT-<NNN>` or
`<PROJECT>-CONFLICT-<LAYER>-<NNN>`. It records exact claim/artifact IDs,
incompatible propositions, roles, applicability, shared scope, evidence,
detection state, priority, and required resolution class. Open Conflicts use a
dedicated governed register/view rather than the three operator-facing intake
queues.

A Conflict resolves only through an append-only lifecycle event linking the
durable resolving artifacts or events. Depending on class, those may include a
new or absorbing Requirement, Contract, Decision, explicit precedence rule,
valid exception or boundary change, recompiled evergreen projection with
proof, or external-authority update. Deterministic role/lifecycle rules may
resolve it without a Question; create a Question only when knowledge or an
authorized choice is missing. Unsatisfiable immutable obligations remain open
and blocking until an authority changes the boundary or grants a valid
exception.

**Scenario DSET-SCENARIO-GOV-028:** A failing Test against an active Requirement
creates an assurance failure, not a Conflict. Two active customer Contracts
demanding mutually exclusive values emit one blocking Conflict. Investigation
creates a linked Question only when the governing scope is unclear; resolution
links the authority's new absorbing Contract and an append-only Conflict event
without editing either original atom.
