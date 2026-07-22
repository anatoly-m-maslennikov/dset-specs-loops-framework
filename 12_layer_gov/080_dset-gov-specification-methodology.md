# Methodology GOV specification

## Active Decision source compilation

### DSET-DECISION-GOV-020 — Generated-only provenance boundary

Commit provenance is mandatory for every governed commit. Derived commit
relations and implementation coverage exclude commits whose changed paths are
entirely under `generated/` directories, because a generated mirror cannot be
an input to the semantic graph that generates it. Commits that change any
non-generated governed path remain relation inputs.

This evergreen GOV projection compiles the active consequences of these
general Decisions. Their immutable carriers retain rationale and history; this
specification and the registered governing rules own the current executable
presentation.

| Decision | Compiled consequence |
|---|---|
| `DSET-DECISION-GOV-001` | Separate atomic authority, evergreen projections, transactional context/evidence, implementation, commit provenance, and session provenance |
| `DSET-DECISION-GOV-002` | Use one constitutional governance root; separate dependency from precedence and authority from assurance |
| `DSET-DECISION-GOV-003` | Keep semantic atoms immutable and resolve conflicts by role and lifecycle before priority |
| `DSET-DECISION-GOV-008` | Use four application-level Types with at most one direct subtype and explicit act/content/carrier/work/evidence boundaries |
| `DSET-DECISION-GOV-010` | Use the bounded `critical`, `high`, `medium`, `low`, `deferred` priority profile with `medium` as default |
| `DSET-DECISION-GOV-019` | Use Version as the shared primary artifact type for six flat release-lifecycle roles |
| `DSET-DECISION-GOV-013` | Use ten typed forward artifact relations, derived inverses, and range-based evergreen projection frontiers |
| `DSET-DECISION-GOV-014` | Normalize explicit null to omission only for governed optional-unset TOML fields; block every other null |
| `DSET-DECISION-GOV-015` | Keep standards-compliant JSON Schema files as canonical external-format contract carriers without editable TOML duplicates |
| `DSET-DECISION-GOV-016` | Preserve selector-sealed package YAML as historical authority and use one sibling package TOML as the current editable registry |
| `DSET-DECISION-GOV-017` | Retain exactly registered, digest-bound YAML snapshots for immutable historical links while TOML alone owns current state |
| `DSET-DECISION-GOV-022` | Separate installed methodology, applied project artifacts, and reusable framework source into distinct numbered namespaces |
| `DSET-DECISION-GOV-025` | Resolve every DSET authority reference by ID or globally unique carrier name only inside the selected project control plane |
| `DSET-DECISION-GOV-026` | Number installed methodology for reading order without creating a durable path registry |
| `DSET-DECISION-GOV-027` | Atomize carrier representation transitions and exclude physical paths from current identity |
| `DSET-DECISION-GOV-028` | Keep `.dset` current and exclude inert historical aggregates and completed migrations from skill discovery and compilation |
| `DSET-DECISION-GOV-029` | Keep repository legal files outside `.dset` and resolve their unique names only within the root legal distribution surface |
| `DSET-DECISION-GOV-031` | Keep executable product contracts in TOOL, development realization and executable QA under IMPL, and post-implementation delivery and operation under OPS |

Absorbed predecessors remain immutable history and are excluded from the active
compilation set by append-only lifecycle events.

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

## DSET-DECISION-GOV-022 — Separate methodology from applied project artifacts

The project-local control plane owns installed methodology only under
`.dset/000_dset_methodology/`, applied project-wide artifacts under
`.dset/100_project/`, applied layer artifacts under
`.dset/101_layer_meta/` through `.dset/106_layer_ops/`, and applied Version
artifacts under `.dset/150_versions/`. Installed methodology never owns applied
atoms, specifications, plans, evidence, or Version records.

The DSET framework repository separately owns reusable product source under
root `10_project/`, `11_layer_meta/` through `16_layer_ops/`, and
`50_versions/`. Ordinary adopters do not receive this product-source tree.

**Scenario DSET-SCENARIO-GOV-005:** A thin skill resolves its rule from
`.dset/000_dset_methodology/04_skill/`, writes an accepted Decision only below
the applicable `.dset/100_project/` or `.dset/10x_layer_*` applied owner, and
does not mistake root framework source for project-local authority.

## DSET-DECISION-GOV-025 — Discover DSET authority by identity

Every skill first selects exactly one project control plane and searches only
that project's `.dset` tree for settings, installed methodology, evergreen
artifacts, atoms, and lifecycle events. Durable references store a stable ID or
globally unique carrier name, never a physical path. Zero or multiple matches
fail closed. Resolved filesystem locations exist only in memory while the
selected carrier is being used.

Implementation work areas remain explicit execution inputs outside the control
plane; they never become fallback DSET authority.

## DSET-DECISION-GOV-026 — Number methodology without path authority

The installed methodology uses numbered sibling names for reading order.
Numbering is presentation, not identity: skills ignore it and resolve the
requested ID or unique carrier name within `.dset`. Deterministic source
materialization computes the installed layout without persisting a
source-to-destination path registry.

## DSET-DECISION-GOV-028 — Keep the control plane current

The selected project's `.dset` tree contains only current settings, installed
methodology, applied project/layer/Version artifacts, evergreen specifications
and plans, and current evidence and verification records.

Historical aggregate registries, completed migration records, compatibility
snapshots, pre-current change folders, and retained pre-current documentation
live in an inert repository archive outside `.dset`. Skills and current
semantic compilation search only `.dset`; they never consult the archive as a
fallback authority or coverage source.

## DSET-DECISION-GOV-029 — Keep legal files outside the control plane

The repository's own legal instrument remains the root `LICENSE` carrier.
Retained third-party license texts and no-license notices live under the root
`LICENSES` distribution surface. They are not methodology, applied artifacts,
settings, runtime state, or historical DSET data and never live in `.dset`.

Source provenance stores each legal carrier's globally unique filename. Legal
validation resolves that name only within `LICENSES`; this bounded legal check
does not widen skill discovery, artifact identity lookup, or semantic
compilation beyond `.dset`.

## DSET-DECISION-GOV-031 — Place executable methodology by semantic role

Installed methodology keeps the DSET executable contract, schemas, templates,
fixtures, and algorithms under TOOL. It places development realization under
IMPL: the synchronized Python package and portable launcher under `100_python`,
deterministic Test implementations and runner under `110_tests`, and
independent-review/reconciliation Evaluation implementations under
`120_evaluations`. OPS owns delivery, release, publication, runtime operation,
investigation, containment, recovery, and hosted evidence after implementation.

Applied QA atoms and plans continue to own what must be checked. Evidence and
Verification continue to own what happened and what the results support. The
methodology owns only reusable execution mechanisms. Repository Python/Test
sources materialize byte-for-byte without symlinks; generated caches are
excluded. Ecosystem-required package and module names may remain unnumbered
inside their numbered IMPL owners. This Decision replaces
`DSET-DECISION-GOV-030`.

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

## DSET-REQUIREMENT-GOV-010 — Semantic Types and document roles stay separate

DSET must define exactly four semantic Types—Decision, Question, Problem, and
QA—and at most one allowed direct subtype per emitted atom. Navigation,
specification, architecture, rationale, procedure, plan, evidence/history,
implementation, derived view, agent workflow, Change, and Release are document,
lifecycle, implementation, or optional-container roles rather than additional
semantic Types. Workflow, queue, skill, tool, host, filename, path, and next
action never determine Type or subtype.

**Scenario DSET-SCENARIO-GOV-011:** A User Story and Requirement are sibling
Decision subtypes linked from one specification; the specification is their
evergreen document role rather than a fifth Type. A design explanation moves to
rationale and a repeatable sequence to a playbook without retyping either as an
atom.

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

## DSET-REQUIREMENT-GOV-018 — Routing applies the flat semantic Type model

`DSET-RULE-WORK-ITEMS` must route operator-accepted authority to Decision;
unresolved knowledge, Conflict, Risk, and Opportunity to Question; current
insufficiency, Defect, Gap, and Debt to Problem; and deterministic Test or
qualitative, probabilistic, statistical, or model-judged Evaluation definitions
to QA. Every named subtype is direct; no subtype may contain another subtype.

Problems and Questions do not authorize implementation. A Problem may return
directly to implementation only when an active Decision already defines the
correction; otherwise it raises a Question whose consequential answer becomes a
Decision. GitHub Issues, Jira/support tickets, tasks, Changes, and releases are
representations, steps, or optional containers rather than semantic Types.

**Scenario DSET-SCENARIO-GOV-019:** A production failure is a Problem/Defect, a
missing required platform is a Problem/Gap, future delivery harm is a
Question/Risk, optional release-note automation is a Question/Opportunity, and
incompatible active API obligations form a Question/Conflict. An operator
answer becomes a Decision or direct Decision subtype before implementation.

## DSET-REQUIREMENT-GOV-019 — IDs expose the concrete Type or subtype

The project prefix is `DSET`. Project-wide IDs use
`DSET-<FULL-KIND>-<NNN>`; layer-owned compatibility IDs use
`DSET-<FULL-KIND>-<LAYER>-<NNN>`, where `<LAYER>` is `META`, `GOV`, `TOOL`,
`SKILL`, `IMPL`, or `OPS`. `<FULL-KIND>` is the subtype when present and the Type when
subtype is empty. No ID encodes a subtype path.

Decision kinds are `DECISION`, `REQUIREMENT`, `CONSTRAINT`, `CONTRACT`,
`STORY`, `OUTCOME`, `SCENARIO`, and `INVARIANT`; Question kinds are `QUESTION`,
`CONFLICT`, `RISK`, and `OPPORTUNITY`; Problem kinds are `PROBLEM`, `DEFECT`,
`GAP`, and `DEBT`; QA kinds are `TEST` and `EVALUATION`. Existing stable
`EVAL` and other legacy IDs remain resolvable compatibility history and are not
renamed in place. No alternate global prefix is used, and directory moves do
not rename identities.

**Scenario DSET-SCENARIO-GOV-020:** A general Decision uses
`DSET-DECISION-001`; a User Story uses `DSET-STORY-002` with
`type: decision` and `subtype: user_story`; a Risk uses `DSET-RISK-003` with
`type: question`; and a Test uses `DSET-TEST-004` with `type: qa`. None carries
a nested subtype in its ID or metadata.

## DSET-REQUIREMENT-GOV-020 — Artifacts declare authority and lifecycle roles

DSET must distinguish atomic authority sources, evergreen compiled projections,
transactional context/evidence, and implementation-layer artifacts. A typed
atom owns one primary claim or directive rather than its real-world subject,
operator acceptance act, file or record carrier, performed work, result,
evidence, gate disposition, or derived Verification. Accepted,
active, applicable Decision atoms and their direct subtypes are authority
sources. Evergreen specs, implementation plans, Test plans, Evaluation plans,
runbooks, and governing rules are updatable projections compiled from those
sources. Problems, Questions and their direct subtypes, acceptance and other
lifecycle events, QA executions/results, proofs, optional Changes/releases,
sessions, and runs preserve work history or evidence
without becoming authority merely by existing. Implementation artifacts are
code, Test code, Evaluation prompts/datasets, CI workflows, scripts, generated
runtime assets, and configuration examples.

**Scenario DSET-SCENARIO-GOV-021:** An operator acceptance event grants
authority to a Decision directive carried in a Markdown record. The directive
changes behavior, the
compiled spec and proof plans expose its current consequences, and code, Test
code, and Evaluation prompts implement those sources. Later QA execution
produces evidence and Verification without any act, carrier, work occurrence,
or result becoming competing authority. If
the Decision and compiled spec differ, the Decision wins and the spec is stale.

## DSET-REQUIREMENT-GOV-021 — Atomic authority compiles into evergreen projections

Accepted, active, applicable Decision atoms and direct subtypes must compile their current
behavioral consequences into the owning evergreen specs, plans, runbooks, or
governing rules. A compiled projection never outranks an active source atom. If
they differ, the source atom governs, the projection is stale, and its relying
release gate fails until deterministic recompilation succeeds. Transactional
context and evidence can motivate or assess a source but cannot replace one;
generated traceability shows the relationship without becoming authority.

The deterministic compilation gate accepts only an explicit ID-owned heading
section, table row, or labeled block as a projection fragment; a loose ID
mention provides no coverage. It binds source, full projection, fragment kind,
location, and fragment digests. This proves declared structure and freshness,
not semantic equivalence. Review or Evaluation separately judges whether the
fragment faithfully carries the source consequence.

Atomic semantic records are immutable. Editable drafts are not atoms. Emission
fixes the atom's ID, semantic payload, provenance, creation status, and links.
Acceptance, rejection, reopening, correction, withdrawal, or any other later
semantic change is a new append-only lifecycle event or successor atom.
Atomic semantic content never changes. Directory placement may change while
the globally unique carrier name remains stable. A carrier-name or
representation migration is a separate immutable transition record with
old/new carrier names, digests, semantic-equivalence proof, and Git return
identity. A semantic change requires a successor atom and lifecycle event.

Compatibility migration must not leave older Decision authority mutable.
Dedicated legacy Decision carriers are sealed by whole-file digest; Decision
identifiers held in shared package registries are sealed as independent
selector fragments so unrelated registry additions remain possible. A missing
or changed sealed fragment fails validation. New or replacement authority must
use a native atom and append-only lifecycle transition rather than refreshing
the legacy ledger.

A replacement is a new atom with an explicit `absorbs` relation to older atoms.
Absorption is acyclic, validated, never inferred from time or numbering, and
removes the older atoms from the active authority set without deleting or
editing their history. The absorbing atom must carry forward or explicitly
replace every still-applicable consequence. Partial replacement leaves
unaffected older claims active and does not absorb the whole atom. Reverse
links and the active compilation set are derived views.

An atom with no active claims, open reliance, or unresolved lifecycle work is
fully retired and may move into its artifact type's `archive/` subfolder
through a registered carrier transition. Its semantic ID and payload remain
unchanged, the original and current carrier digests remain linked, and the
canonical ID registry updates its location. Partial absorption does not
qualify. Archived atoms remain immutable history and are not deleted.

**Scenario DSET-SCENARIO-GOV-022:** A resolved Question produces a Decision, the
Decision compiles into the relevant spec and proof plans, and review rejects a
code-only change that leaves the evergreen projection stale. A later Decision
absorbs the earlier one explicitly; the original remains immutable provenance,
while only the successor participates in the active compilation set. After all
reliance closes, the original moves to `archive/` through a lossless registered
carrier transition and remains resolvable by ID and source return address.

## DSET-REQUIREMENT-GOV-022 — Commits and atomic artifacts retain provenance

Every commit that changes an evergreen projection or implementation artifact
must name the Decision or Decisions it implements in its commit message body.
A linked Problem may explain the need for correction, but does not replace
Decision authority. Each newly emitted atomic artifact or append-only lifecycle
event has an explicit session-provenance field: unique stable host-prefixed
`llm_session_ids` when an LLM helped produce it, or an explicit empty
list/`none` for human-only work. Missing provenance is invalid. A review,
correction, or status change emits another linked record rather than revising
the atom. This applies to supported Decision, Question, Problem, and QA atoms,
optional containers, promoted proofs, skill-run records, and session
checkpoints without making provenance authoritative.

The project manifest declares the commit at which enforcement begins. Every
later non-merge commit must use exactly one validated mode: `Implements:` with
one or more known Decision-family IDs, or the evidence pair `Decision:` and
`Verifies:`. Both require exactly one valid `Session:` trailer; `Resolves:` may
name only known Problems. Unknown IDs, QA/Problem IDs used as implementation
authority, mixed modes, and missing trailers fail validation.

An immutable historical commit in the validated range may have one append-only
manifest correction instead of rewritten history. The correction binds the
full commit SHA and exact original-message digest, declares the ordinary
provenance mode and canonical IDs, carries exactly one Session ID and a
rationale, and is valid only when the original fails and the corrected view
passes the same rules as a current commit. It is not an exemption mechanism.

**Scenario DSET-SCENARIO-GOV-023:** A commit body contains `Implements: DSET-DECISION-GOV-001`; the emitted Decision, Change, intake item, proof, run, checkpoint, and later lifecycle-event shapes record the Codex session IDs that produced them; an atomic correction is a new linked event; an exact historical commit correction is append-only, digest-bound, and revalidated; and a human-only fixture passes only with explicit empty provenance.

## DSET-REQUIREMENT-GOV-023 — Rule authority and assurance are explicit

`DSET-RULE-ARCHITECTURE` must remain the dependency-free constitutional root
for repository governance. Every registered normative rule must resolve to one
accepted, active, applicable atomic source set and one repository-local compiled
governing document in the current profile edition and declare separate
`depends_on` and `precedence_over` relations. A source/document mismatch selects
the source, marks the document stale, and blocks reliance until recompilation.
Both graphs must be acyclic; registry order must not imply precedence; missing
precedence targets or unresolved conflicts must fail closed.

Active Decisions and their direct subtypes authorize and explain rule changes;
provenance identifies origin but does not authorize. QA/Test and
QA/Evaluation results, reviews, and evidence assess
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
authority. It reports artifact counts by role, Type, subtype, layer, status,
priority, and applicable Work Area; unresolved and automatically resolved
Question/Conflict subtypes; unresolved Problems and Questions with their
subtypes; proof freshness; and traceability coverage for Decision atoms
compiled into evergreen owners, applicable authority connected to
implementation and QA/Test or QA/Evaluation, implementation commits connected
to their authorizing Decision, and proof plans connected to current evidence.

Every coverage result states its numerator, denominator, exclusions,
not-applicable, unknown, and stale counts and links back to canonical owners.
The view must not require a second empty-subtype Decision for every direct
Decision subtype, code for a documentation-only Requirement, or an Evaluation
where the Evaluation plan declares one not applicable. A portable Markdown renderer is the baseline public surface;
interactive renderers may consume the same derived model later.

**Scenario DSET-SCENARIO-GOV-025:** A repository reports 18 of 20 applicable
Requirements with current deterministic Test coverage, one justified
not-applicable Requirement, and one uncovered Requirement. The dashboard links
the uncovered row to its authority and evergreen owners and does not inflate
the score by creating irrelevant Decisions, code, or Evaluations.

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
or route it to an existing or new Problem or Question and direct subtype,
Decision and direct subtype, optional Change, evergreen owner, or proof
obligation. Accepted consequences compile
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
Implementation files may inherit from their owning Decision or QA atom, or an
optional Change, instead of carrying duplicated inline metadata.

Problems, Questions and their direct subtypes, optional Changes, and tasks use priority as one
input to execution order. Dependencies, authorization boundaries, release
gates, and resource constraints may still require a different next action.
Impact, severity, likelihood, expected value, Decision/Contract obligations, Outcome
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
QA/Test, QA/Evaluation, review, and proof evidence change assurance and the relying gate instead
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

## DSET-REQUIREMENT-GOV-027 — Four Types use one flat subtype level

DSET must represent each semantic atom with exactly one of four Types and at
most one direct allowed subtype:

- Decision: Requirement, Constraint, Contract, User Story, Outcome, Scenario,
  or Invariant;
- Question: Conflict, Risk, or Opportunity;
- Problem: Defect, Gap, or Debt; and
- QA: Test or Evaluation, with subtype required.

A general Decision, Question, or Problem omits subtype. A subtype never repeats
its Type and never contains another subtype. User Story and Requirement are
sibling Decision subtypes; links between them do not create
Decision/Requirement/User Story nesting.

Classification depends on semantic content, never workflow, queue, skill,
tool, host, filename, path, or next action. Changed semantics require a new
linked atom. All emitted atoms are immutable.

Types are application-level routing classifications for durable project claims
and directives, not universal classifications of people, systems, real-world
conditions, performed work, or files. Classify the smallest independently
reviewable primary claim. Split multi-head statements into linked sibling
atoms. When an irreducible claim remains plausible under several subtypes, use
the empty subtype of its Type and raise a Question when ambiguity affects work;
never guess or assign several subtypes.

The operator's acceptance is an act or lifecycle event distinct from Decision
directive content and its carrier. QA atoms define checks; Test/Evaluation
execution is work; results and logs are evidence; gate decisions and
Verification are derived. Storage may colocate linked roles without collapsing
their semantics or identities.

Direct Decision subtypes are recognized by the acceptance condition that owns
the claim. Contract owns named boundary obligations. Constraint narrows
otherwise acceptable solutions when no boundary participant relies on it as a
Contract. User Story owns actor/want/value framing but not acceptance criteria.
Outcome owns intended measurable state change, not observed evidence. Scenario
owns one accepted example, not its run. Invariant owns an always-hold
condition, not evidence that it currently holds. Requirement owns the remaining
observable obligation that no more precise Decision subtype owns.

Problem means presently true insufficiency. Wrong now is Defect; missing now is
Gap; a working known compromise with continuing cost is Debt. Question means
uncertainty. Possible future harm is Risk; optional possible value is
Opportunity; verified incompatible active applicable authority is Conflict.
Different wording, stale compilation, failed QA, implementation nonconformance,
and contradictory evidence alone are not Conflicts.

Debt cannot hide a Defect or Gap. If a compromise also violates active
authority or leaves an obligation absent, record linked Defect or Gap atoms or
emit a Decision that changes the applicable authority.

QA/Test is an exact reproducible predicate under declared conditions.
QA/Evaluation is qualitative, probabilistic, statistical, or model-judged and
declares its
method, criterion, threshold, and uncertainty handling where applicable. QA
remains Evaluation when deterministic code executes the method but the
conclusion depends on judgment, sampling, calibration, probability, statistics,
or a model. QA results affect assurance and never override Decision authority.

New atoms use this explicit envelope and direct-subtype ID kind. Existing
stable IDs and carriers are never rewritten merely to adopt it. A deterministic
compatibility classifier maps each legacy ID-kind/carrier pair to the same four
Types, including legacy `EVAL` to QA/Evaluation and standalone Opportunity to
Question/Opportunity, and fails closed when the pair disagrees. Traceability,
project health, validation, lifecycle lookup, and skill context consume that
single mapping so compatibility does not become a second taxonomy.

A Question/Conflict records exact incompatible authority and resolves through
an append-only lifecycle event linked to the answering or absorbing Decision,
precedence, exception, boundary change, or external-authority update. A
Problem returns directly to implementation only when an active Decision already
defines the correction; otherwise it raises a Question.

**Scenario DSET-SCENARIO-GOV-028:** A failing QA/Test against an active
Requirement creates assurance failure and a Problem/Defect when current
behavior is wrong, not a Conflict. Two active Contract subtypes demanding
mutually exclusive values create one Question/Conflict. An operator-accepted
absorbing Contract resolves it through an append-only event without editing the
original atoms.

## DSET-REQUIREMENT-GOV-028 — Atomic rationale is recommended and optional

Every Decision representation must prompt for a concise rationale explaining
why its option was selected. Every other atomic artifact representation must
permit rationale when it helps review, production investigation, priority or
scope interpretation, absorption, replacement, or conflict resolution.
Rationale remains optional for every atomic type: omission alone must never
invalidate an artifact or block a proof or release gate.

When a structured rationale is supplied, its schema must require a non-empty,
bounded value. Rationale is explanatory context, not an alternate authority;
it cannot hide a Decision or direct subtype, lifecycle transition, or evidence claim
that is absent from the canonical owner for that concern. Templates should
prompt useful reasoning without encouraging placeholder prose. Evergreen
implementation references remain focused on current executable truth and link
out when the rationale is substantial.

**Scenario DSET-SCENARIO-GOV-029:** Two otherwise identical Decisions, one with
a concise rationale and one without it, both pass structural validation; the
template makes the rationale opportunity visible. A Change, intake atom, proof,
skill run, or checkpoint may add a bounded rationale when its non-obvious scope,
interpretation, or handoff needs explanation. An empty supplied structured
value fails, and no rationale is allowed to introduce an unowned behavioral
rule or lifecycle transition.

## DSET-REQUIREMENT-GOV-029 — Artifact classification is MECE and independent

DSET must classify every governed carrier with exactly one primary
`artifact_type` and at most one allowed direct `artifact_subtype`, independently
from the semantic `type` and `subtype` used by Atomic Records. The registered
types are Atomic Record, Analysis Report, Specification, Procedure, Plan,
Version, Implementation, Evidence Record, Verification, Derived View, and
Navigation. Version directly permits Roadmap, Version Scope, Change, Release
Plan, Readiness Record, and Release Record. The project-local
machine-readable registry owns their IDs, primary questions, direct subtypes,
fallback behavior, and path rules.

Analysis Report permits Solution Landscape, Root-Cause Analysis, Proposal,
Technical Investigation, and External Audit Analysis. It interprets named
inputs but does not authorize its conclusion; accepted conclusions are emitted
as separate Decision, Question, Problem, or QA atoms. Evidence records
observations, Verification derives assurance, Readiness Record owns the
explicit release gate disposition, and Release Record owns immutable
publication history. Unknown types, missing classifications, mismatched or
nested subtypes, and multiple applicable path rules fail closed.

Roadmap, Version Scope, Change, Release Plan, Readiness Record, and Release
Record are flat peers under the primary Version type. They share one
project-wide `VERSION` identity sequence. Milestones are Roadmap entries;
Release Notes and changelogs are mirrors or Derived Views of Release Records.

**Scenario DSET-SCENARIO-GOV-030:** A Solution Landscape compares three options
without choosing one; a later Decision accepts one option and compiles it into
Specification/Design and Plan/Implementation Plan. Test execution emits an
Evidence Record, Verification assesses its support, and a Readiness Record
records an explicit blocked gate until the required evidence passes. No
workflow position changes any semantic or artifact classification.

## DSET-REQUIREMENT-GOV-038 — Artifact names default to primary type

New artifact IDs and filenames must include the primary artifact type token by
default. The optional direct artifact subtype remains metadata and cannot force
identity churn. A project may opt only newly emitted artifacts into subtype
tokens with `artifacts.subtype_in_names = true` in root
`dset_settings.toml`. Optional capabilities are independently selectable; DSET has no
single bundled advanced mode. A settings change never renames immutable atoms
or already stable artifact identities.

**Scenario DSET-SCENARIO-GOV-031:** A Version Scope is emitted as
`APP-VERSION-001-0-4-core.md` with `artifact_subtype: version_scope`, and a
Roadmap uses the same `VERSION` sequence with `artifact_subtype: roadmap`. An
adopter that explicitly enables subtype-bearing names may include those subtype
tokens in new artifacts, while every existing stable identity remains
unchanged.

`DSET-REQUIREMENT-GOV-030` is absorbed by
`DSET-REQUIREMENT-GOV-038` and remains immutable history.

## DSET-REQUIREMENT-GOV-031 — Architecture views descend one level

Every project hub must include a Mermaid view of its immediate enabled
structural children: feature groups when present, otherwise features and/or
layers. Every feature-group hub must show its features. Every feature or layer
hub must show the main functions, capabilities, or components immediately
under it. A structural level that is not enabled requires no placeholder.
Views must state how responsibility descends one level, remain consistent with
linked canonical owners, and never become authority merely by being visual.

**Scenario DSET-SCENARIO-GOV-032:** A layered repository root shows META, GOV,
TOOL, SKILL, and OPS. Each layer hub shows only its own main functions. A
product repository with enabled feature groups instead shows groups at the
root, features in each group hub, and main functions inside each feature hub;
it creates no empty layer or feature-group diagram for disabled structures.

## DSET-REQUIREMENT-GOV-032 — Global truth owns only cross-child concerns

When features, feature groups, or layers are enabled, every atomic claim and
compiled artifact must be owned by the narrowest structural scope that fully
contains every affected owner and subject. A claim must not move to project
scope merely because it is abstract, important, reused, or described at a high
level.

The project-level artifact set owns project-wide outcomes, user journeys, and
requirements; Contracts and dependency rules between immediate children;
shared API, data, and event semantics; end-to-end Tests and Evaluations;
cross-cutting Invariants and Constraints such as security, privacy,
compatibility, supportability, performance budgets, and licensing; whole-
project architecture, integration topology, version scope, release planning,
readiness, and publication history; and cross-owner Decisions, Questions,
Problems, Conflicts, Risks, Opportunities, and Analysis Reports.

The rule applies recursively. A concern spanning features inside one feature
group belongs to that group; a concern spanning feature groups or layers
belongs to the project. Parent specifications and atoms link child-owned detail
without copying or becoming a competing authority.

**Scenario DSET-SCENARIO-GOV-033:** Two features in one group share an API
Contract and one end-to-end Test, so the group owns those artifacts. A privacy
Invariant and release-readiness gate apply across multiple groups, so the
project owns them. A high-level requirement affecting only one feature remains
with that feature despite its abstraction.

## DSET-DECISION-GOV-013 — Artifact relations are typed and directional

Every authored artifact relation uses exactly one of `child_of`, `analysis_of`,
`projection_of`, `implementation_of`, `check_of`, `evidence_for`,
`resolution_of`, `override_of`, `replacement_of`, or `relates_to`. The source
stores one forward `type` and canonical `target`; reverse relations are derived
and never authored. A source-target pair has one primary relation.

`child_of` is claim refinement or decomposition and keeps both claims active.
`analysis_of` owns non-authoritative investigation. `implementation_of` owns
realization by code, configuration, documentation, migration, or commit.
`check_of` owns Test/Evaluation definitions. `evidence_for` owns observed
support for an explicit result, finding, or Verification. `resolution_of`
closes a Question, Conflict, or Problem. `override_of` changes inherited
authority only inside a narrower declared scope. `replacement_of` completely
replaces an older atom and requires append-only absorption. `relates_to` is a
symmetric fallback with no authority, assurance, dependency, precedence, or
lifecycle meaning and satisfies no implementation or QA coverage.

`projection_of` normally stores a range containing one semantic Type, one
exact structural scope, and a `through` boundary naming a globally ordered
immutable `ATOMIC-RECORD` carrier. The range includes all applicable active
atoms of that Type and scope through the boundary after lifecycle resolution.
A newer applicable atom makes the projection stale. Individual targets are
valid only for explicit exceptions.

The specialized governance-registry fields `depends_on` and
`precedence_over` are not general artifact relations. Ordinary citations,
folder or scope membership, shared subject matter, and chronology remain
metadata or Markdown links. Historical sealed `child_of` fields remain
compatibility input and project as typed `child_of` edges; new artifacts use
the `relations` list.

**Scenario DSET-SCENARIO-GOV-034:** A feature Requirement refining a project
Requirement is `child_of`; a scoped exception is `override_of`; and a complete
successor is `replacement_of`. None stores an additional `child_of` edge.

**Scenario DSET-SCENARIO-GOV-035:** A specification records one
`projection_of` Decision range through its current carrier frontier. A Test is
`check_of` the Requirement, its result is `evidence_for` the Verification, and
the implementation commit produces `implementation_of` edges. No reverse edge
is stored.

`DSET-REQUIREMENT-GOV-033` remains a sealed package-registry compatibility ID.
Its authority is absorbed and fully replaced by `DSET-DECISION-GOV-013`; it is
not part of the active compilation set.

## DSET-REQUIREMENT-GOV-039 — Atom creation has configurable strictness

`.dset/dset_settings.toml` must expose independent
`artifacts.creation_strictness` with `medium` as the
default and `high` as the stricter alternative. At `medium`, DSET may emit one
accepted atom when authority, primary claim, Type, owning structural scope,
provenance, material links, priority, and acceptance state are clear; optional
non-authoritative detail may remain explicitly unknown. At `high`, every
material authority, meaning, boundary, Type, scope, lineage, conflict, and
proof question must be resolved before emission. Otherwise DSET asks focused
questions or stops without writing an atom.

The deterministic assessment must resolve the candidate's scope, immediate
parent, affected children, material links, priority, and session identifiers
against repository authority. Sealing an immutable atom must consume the same
assessment and refuse a blocked candidate; a caller cannot bypass the gate by
writing a carrier directly.

Before emission, DSET must assess eligibility for the immediately broader
enabled scope under narrowest-common-scope ownership. Eligible feature claims
may be proposed for their feature group, feature-group or feature claims for
the project, and layer claims for the project. Promotion is proposed one step
at a time, requires operator acceptance, and never generalizes claims that
depend on local evidence, implementation, exceptions, or vocabulary. A later
promotion of an immutable atom emits a new linked broader-scope atom rather
than moving or editing the old one.

**Scenario DSET-SCENARIO-GOV-036:** With strictness `high`, an accepted feature
claim with an ambiguous exception is not emitted until the operator resolves
the exception. Once precise, DSET notices that the claim applies unchanged to
every feature in its group and proposes one feature-to-group promotion; it
does not write at group scope or jump to project scope without acceptance.

`DSET-REQUIREMENT-GOV-035` is absorbed by
`DSET-REQUIREMENT-GOV-039` and remains immutable history.

## DSET-REQUIREMENT-GOV-040 — Project settings are verbose and all DSET artifacts use TOML

The canonical settings and project-manifest carrier is
`.dset/dset_settings.toml`. It must explain its boundary with governing documents, every setting,
every accepted value, the behavior each value selects, the default, and
practical examples. New writers and bootstraps emit only this path. Retired
root settings and split manifests are read-only migration inputs; if competing
carriers exist, validation stops.

Settings own operator-selectable behavior: artifact subtype naming,
medium/high artifact-creation strictness, lazy/strict implementation
preparation, integration-branch/branch-worktree Change workspace selection,
low/medium/high delegation budget selection, and the priority scale/default.
The manifest section owns identity, repository and Work Area structure,
runtime-risk and durability topology, external contracts, release targets,
verification commands, and commit-provenance boundaries. Governing documents
own definitions and policy; settings select registered behavior only.

DSET-owned structured artifact files and DSET Markdown frontmatter must use
TOML. One canonical source must not coexist with an editable YAML or JSON copy.
Previously sealed atomic carriers, promoted evidence, legacy Decision
carriers, and historical structured editions migrate through the authorized
lossless carrier-transition protocol; they are not format exceptions.

Externally prescribed carriers may retain their required format: host skill
metadata, GitHub Actions, ecosystem manifests and lockfiles, wire/CLI output,
machine-local runtime journals, and standards-compliant JSON Schema files.

Migration must inventory every source and reference, preview without writing,
preserve normalized values, stable IDs, provenance, relations, selector
fragments, and Markdown bodies, emit old/new and semantic digests plus Git
source-return addresses, refuse collisions and unsupported values, rewrite
repository references, update current-carrier seals transactionally, validate
the complete migrated tree before cutover, and leave no DSET-owned YAML
artifact or Markdown YAML frontmatter. Any adopter compatibility reader is
explicit, finite, and never a legacy write path.

**Scenario DSET-SCENARIO-GOV-037:** A cold reader opens
`.dset/dset_settings.toml`, finds every operator choice and predicts its effect,
and reads the same carrier for runtime topology and release truth. Bootstrap
emits only the canonical path; a repository containing competing carriers
fails.

**Scenario DSET-SCENARIO-GOV-038:** A dry run reports every DSET-owned YAML
source, TOML destination, reference rewrite, carrier transition, source-return
address, and semantic digest. Apply produces a valid repository with no DSET
YAML artifact or Markdown YAML frontmatter; a second apply is a no-op, and JSON
Schema remains standard canonical JSON without an editable TOML duplicate.

`DSET-REQUIREMENT-GOV-036` and `DSET-REQUIREMENT-GOV-037` remain historical
compatibility IDs. Their authority is absorbed and fully replaced by
`DSET-REQUIREMENT-GOV-040`; neither is part of the active compilation set.

## DSET-DECISION-GOV-014 — TOML null normalization is allowlisted

TOML migration preserves governed semantic values. Because TOML has no null,
an explicit null may become an omitted field only when the owning schema and
runtime define absence as exactly optional and unset. The initial allowlist is
`promotion.parent_scope`, intake `items[].decision`, and pull-request-history
`pull_requests[].merge_commit`. The migration report records every omission by
source and key path. Every other null blocks conversion, and expanding the
allowlist requires new accepted authority and deterministic equivalence proof.

## DSET-DECISION-GOV-015 — JSON Schema remains at its standard boundary

Files whose primary contract is JSON Schema remain canonical JSON as an
externally prescribed interoperability boundary. Generic TOML migration
classifies and retains them, creates no editable TOML duplicate, and continues
validating them as JSON Schema. Replacing this boundary with a DSET schema DSL
and generated adapter requires separate accepted authority, a lossless mapping,
and a freshness gate.

## Historical DSET-DECISION-GOV-016 — Native package registries succeed sealed YAML

When a package YAML contains selector-sealed legacy Decision fragments, DSET
preserves that YAML byte-for-byte as historical compatibility authority. The
migration emits one sibling `package.toml` as the current editable registry,
initializes it from the preserved semantic values, and reconciles it with active
native atoms and current evergreen artifact paths.

Readers prefer `package.toml` after cutover. New package IDs and paths are
written only to TOML. YAML remains finite read-only input for its registered
historical fragments, so the two carriers never become competing writable
owners. Readiness binds the preserved YAML digest and exact successor output;
missing, changed, incomplete, ambiguous, or competing successors stop cutover.

This Decision is absorbed by `DSET-DECISION-GOV-018`; retained YAML is no
longer active policy.

## Historical DSET-DECISION-GOV-017 — Legacy structured snapshots preserve history only

A YAML carrier required by immutable historical links or selector-sealed
authority remains byte-stable only as an exact `legacy_structured` registry
entry. The entry binds its path and whole-file digest to one TOML current owner,
artifact classification, exact retaining carrier IDs, and retention reason.

Readers use TOML only. Missing or changed snapshots or owners, unregistered
YAML/TOML pairs, duplicate or wildcard registration, mutable links to legacy
paths, and new immutable links to unregistered carriers fail. Migration creates
the owner and registration transactionally, rewrites only mutable references,
keeps historical links physically navigable on GitHub, and becomes a no-op on
a second run.

This Decision is absorbed by `DSET-DECISION-GOV-018`; retained YAML is no
longer active policy.

## Historical DSET-DECISION-GOV-018 — Immutable semantics permitted aggregate carrier transitions

Atomic immutability attaches to the artifact's semantic identity and payload,
not permanently to one byte encoding. DSET may replace a governed carrier
representation with canonical TOML only through a deterministic, lossless,
append-only transition that preserves IDs, normalized values, claims,
relations, provenance, intended use, selector fragments, and Markdown bodies.

The historical aggregate carrier `carrier-transitions.toml` bound the
authorizing Decision, carrier and semantic IDs, old location, format,
digest and Git blob return address, new location, format and digest, semantic-
equivalence digest, declared loss, implementation commit, and session
provenance. Original seals remain historical; current-carrier fields follow the
validated transition chain. Unregistered mutation, semantic loss, missing
return address, broken chain, partial resealing, or ambiguous ownership fails.

Markdown keeps its carrier name and body while TOML replaces YAML frontmatter. A
standalone historical YAML edition moves to adjacent `<stem>.legacy.toml` when
`<stem>.toml` already owns current truth. Readers never treat the historical
envelope as current authority. After cutover, `dset/` contains no YAML artifact
files and no Markdown YAML frontmatter. JSON Schema and other externally
prescribed formats remain governed by `DSET-DECISION-GOV-015` and their owning
host or ecosystem contracts.

This Decision is absorbed by `DSET-DECISION-GOV-027`; representation migration
remains governed, but each transition is now an immutable atomic record keyed
by carrier names and digests rather than an aggregate path ledger.

This Decision replaces `DSET-DECISION-GOV-003`, `016`, and `017` while carrying
forward semantic immutability, append-only lifecycle, explicit acyclic
replacement and absorption, role-before-priority conflict handling, universal
priority, retirement, and stable lookup.

## DSET-REQUIREMENT-GOV-043 — Separate control, runtime, and scratch state

A current DSET project has one writable settings and project-manifest carrier
at `.dset/dset_settings.toml`. Installed methodology lives exclusively under
`.dset/000_dset_methodology/`. Current project-wide evergreen artifacts,
atomic records, analysis, evidence, and verification live under
`.dset/100_project/`; current Version lifecycle artifacts and Changes live
under `.dset/150_versions/`; and layer-owned applied
truth lives under `.dset/101_layer_meta/`, `.dset/102_layer_gov/`,
`.dset/103_layer_tool/`, `.dset/104_layer_skill/`, and
`.dset/105_layer_implementation/`, and `.dset/106_layer_ops/`. Generated views remain runtime state under
`.dset_runtime/generated/` unless a separate artifact explicitly promotes an
observation into the applied evidence owner.
Historical aggregates, completed migrations, compatibility snapshots,
pre-current change folders, and retained delivery history live outside `.dset`
and are not current discovery or compilation inputs.
Resumable run, session, cache, readiness, and migration-recovery state lives
under the ignored sibling `.dset_runtime/` root and cannot become project
authority. Disposable DSET scratch and test workspaces live under `/tmp` on
POSIX, or the native operating-system temporary root on Windows, and must be
deleted when their operation exits. Ambient POSIX temporary-directory
variables cannot redirect them into the repository.

Persisted DSET settings, registries, relations, reports, and generated views
refer to project authority by stable ID or globally unique carrier name. They
never store a physical carrier path. Historical immutable records may retain a
former location as inert evidence, but current resolution never consults it.

Enabled feature and feature-group structure may add segments below its owning
project or layer scope, but it does not restore a generic `scopes` carrier.
Schema 1.0–1.4 layouts and root settings are migration inputs only. New
initialization emits schema 1.5 directly. Migration must preserve semantic
identity through atomized transition records while rewriting mutable current
references and generated views to IDs or globally unique carrier names.
Competing current and legacy configuration carriers fail closed.
Same-directory staging needed for atomic publication is bounded to its
transaction and must be replaced or removed before return. This Requirement
replaces `DSET-REQUIREMENT-GOV-042`.

## DSET-REQUIREMENT-GOV-045 — Keep layer authority forward-only

Features are peer capabilities connected horizontally through Contracts at
their narrowest common owner. Call direction, data flow, and delivery order do
not make one feature authoritative over another.

Layers are ordered `META → GOV → TOOL → SKILL → IMPL → OPS`. A layer may govern itself
or any later layer but never an earlier layer. Direct influence on the next
layer is preferred; a longer forward jump is valid only when explicit and when
an intermediate layer has no meaningful ownership to add. A downstream
artifact may consume, implement, check, or evidence upstream authority without
reversing it.

Rule dependencies therefore point to the same or an earlier layer, while rule
precedence targets only the same or a later layer. Backward authority fails
deterministic validation.

If a backward dependency cannot be removed or re-homed without falsifying the
architecture, DSET proposes reclassifying the coupled owners as features with
horizontal Contracts and waits for operator acceptance.
