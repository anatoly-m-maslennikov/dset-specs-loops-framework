# Methodology GOV domain

This is one layer-owned fragment of the logical methodology package. Use the sibling layer hubs for connected definitions; this file owns only the entities and invariants below.

## Entities

| Entity | Definition |
|---|---|
| **Framework truth** | Released DSET methodology and framework-owned assets in this public repository |
| **Package** | A cohesive capability with one vocabulary, specification, public contract, deterministic test plan, and applicable eval plan |
| **Change** | One bounded unit of unaccepted intent and evidence under `dset/scopes/<primary-layer>/changes/<change-slug>/`, identified independently by `DSET-CHANGE-<LAYER>-<NNN>` |
| **Language profile** | Versioned mapping from the six neutral gate categories to language-native tools, scopes, thresholds, and exclusions |
| **Artifact governance profile** | Versioned mapping from artifact architecture and authoring rules to machine-checkable ownership, hierarchy, hub, navigation, and portability gates; it is selected independently from an implementation-language profile |
| **Governed artifact area** | A stable public knowledge boundary with one purpose, owner, root, hub, and structural parent |
| **Semantic Type** | Exactly one of Decision, Question, Problem, or QA; it is determined by an atom's meaning rather than workflow, document role, queue, skill, tool, host, path, or next action |
| **Subtype** | At most one direct specialization of a semantic Type; subtype nesting and a subtype that repeats its Type are invalid |
| **Hub** | A thin navigation surface that identifies an area's purpose, boundaries, and stable owning documents without becoming an exhaustive index or a second normative owner |
| **Project health view** | A generated non-authoritative projection of artifact inventory, traceability coverage, proof freshness, and unresolved work that returns every result to its canonical owner |
| **External review report** | Transactional evidence from an independent human or agent review, bound to exact inputs and provenance, whose findings require explicit triage and never authorize repair by themselves |
| **Atomic artifact** | An immutable emitted record; later status, correction, or authority changes are new append-only lifecycle events or successor atoms, never edits |
| **Atomic authority source** | An accepted, active, applicable Decision atom, including any direct Decision subtype, that is compiled into evergreen projections and wins if that projection is stale |
| **Absorption** | An explicit acyclic new-atom-to-old-atom relation that replaces the older atom in the active authority set without deleting history or inferring precedence from age |
| **Fully retired atom** | An atom with no active claim, open reliance, or lifecycle work that may move byte-for-byte to its type's `archive/` subfolder while retaining its ID, digest, and lookup |
| **Priority** | The single project-wide ordered rank for a governed artifact; it orders handling across all conflict classes, selects a claim only in declared resolvable policy conflicts, and is one execution-order input for actionable work |
| **Governance registry** | Repository-local machine-readable mapping from workflow and normative rule IDs to their editable governing documents, dependencies, applicability, and profile/customization identity; it points to rules without restating them |
| **Governing document** | The single editable repository-local owner of one or more normative rule IDs selected by the governance registry |
| **Decision** | Immutable project authority explicitly supplied or accepted by the operator; an empty subtype represents general authority |
| **Requirement** | A direct Decision subtype for an observable result, behavior, capability, quality, or outcome the project must provide or prevent |
| **Constraint** | A direct Decision subtype restricting acceptable technologies, dependencies, environments, resources, formats, or operating limits |
| **Contract** | A direct Decision subtype defining provider/consumer, interface, compatibility, and failure obligations across a project boundary |
| **User Story** | A direct Decision subtype stating which actor or stakeholder wants which capability or outcome and why it has value |
| **Outcome** | A direct Decision subtype stating a measurable change in user, business, operational, or system state |
| **Scenario** | A direct Decision subtype stating a concrete accepted behavior through preconditions, interaction or event, and observable result |
| **Invariant** | A direct Decision subtype stating a condition that must always hold in its declared scope |
| **Question** | Missing knowledge, interpretation, or choice; an empty subtype represents general uncertainty |
| **Conflict** | A direct Question subtype for verified incompatible active applicable authority over the same scope, concern, and effective time |
| **Risk** | A direct Question subtype for an uncertain future harmful condition |
| **Opportunity** | A direct Question subtype for possible beneficial improvement when no current obligation is unmet |
| **Problem** | A presently true, evidence-backed insufficiency that does not imply or authorize its repair |
| **Defect** | A direct Problem subtype for current behavior or implementation that contradicts active authority or its current projection |
| **Gap** | A direct Problem subtype for a required capability, artifact, proof, or obligation that is absent now |
| **Debt** | A direct Problem subtype for a knowingly accepted compromise that works sufficiently now but creates continuing or future cost |
| **QA** | An immutable definition of how accepted authority is checked; every emitted QA atom has a Test or Evaluation subtype |
| **Test** | A direct QA subtype for deterministic proof with declared conditions and an exact reproducible pass/fail result |
| **Evaluation** | A direct QA subtype for qualitative, probabilistic, statistical, or model-judged assessment with method, criterion, and threshold |
| **Layer** | An optional stable semantic owner for accepted IDs: `META`, `GOV`, `TOOL`, `SKILL`, or `OPS`; it is independent of directory layout |
| **Ruleset identity** | Stable declaration of selected profile/version provenance and whether the materialized local rules remain equivalent or have become a valid custom project profile |

## Invariants

- **DSET-INVARIANT-GOV-001:** Framework truth and project truth never share a writable owner.
- **DSET-INVARIANT-GOV-002:** Public methodology renders and navigates on GitHub without Obsidian-only links or callouts.
- **DSET-INVARIANT-GOV-003:** A Change may reconcile candidate evergreen projections before archival, but those projections cannot be released or treated as accepted truth until applicable proof is fresh and the Change is archived through its implementing PR.
- **DSET-INVARIANT-GOV-004:** Each emitted atom has exactly one semantic Type and at most one allowed direct subtype determined by meaning, never by workflow, document/lifecycle role, queue, skill, tool, host, filename, path, or next action; links connect siblings without creating subtype nesting.
- **DSET-INVARIANT-GOV-005:** Hubs own navigation and boundaries, while atomic documents own rules, rationale, procedures, decisions, proof, and history.
- **DSET-INVARIANT-GOV-006:** Every selected normative rule resolves to one editable governing document inside the adopting repository; a source template remains provenance rather than a live authority after materialization.
- **DSET-INVARIANT-GOV-007:** Invalid or incompatible selected rule ownership fails closed with a stable diagnostic, while explicitly justified non-applicability remains valid.
- **DSET-INVARIANT-GOV-008:** A locally changed ruleset remains valid project truth only under an explicit custom identity that retains its source profile/version provenance.
- **DSET-INVARIANT-GOV-009:** Every normative rule ID has exactly one editable governing document; skills, agent guidance, templates, generated installations, indexes, summaries, and caches never become parallel writable rule stores.
- **DSET-INVARIANT-GOV-010:** DSET has exactly four semantic Types—Decision, Question, Problem, and QA. Decision permits Requirement, Constraint, Contract, User Story, Outcome, Scenario, and Invariant; Question permits Conflict, Risk, and Opportunity; Problem permits Defect, Gap, and Debt; QA requires Test or Evaluation. No subtype contains another subtype. Workflows, tasks, tickets, document roles, Changes, and releases are not semantic Types.
- **DSET-INVARIANT-GOV-011:** All accepted IDs use the `DSET` project prefix and a full type; project-wide IDs omit the layer, layer-owned IDs include `META`, `GOV`, `TOOL`, `SKILL`, or `OPS`, and numbering is independent per type within each project-wide or layer sequence.
- **DSET-INVARIANT-GOV-012:** Rule authority and assurance remain distinct. Dependency and precedence are separate acyclic relations; invalid authority or unresolved conflict fails closed, while missing or stale assurance affects only the relying claim or gate.
- **DSET-INVARIANT-GOV-013:** A health percentage is valid only with an explicit numerator, denominator, excluded/not-applicable/unknown/stale counts, and canonical return links; it never creates authority or rewards unnecessary artifacts.
- **DSET-INVARIANT-GOV-014:** External review findings remain transactional evidence until each finding is explicitly rejected, deferred, or routed to a Problem, Opportunity, Question, Decision, Change, or evergreen owner; review never silently authorizes a fix.
- **DSET-INVARIANT-GOV-015:** Every governed artifact has one explicit or traceably inherited priority, and every conflict pairing receives a deterministic classification and disposition. Artifact role and lifecycle govern before priority: active atomic sources beat stale compiled projections, absorbing atoms beat absorbed predecessors, evidence changes assurance, implementation mismatches create Problems, generated drift becomes stale, and mutually unsatisfiable immutable obligations stop. Explicit precedence and then higher priority select a claim only for declared comparable policy conflicts whose governing profile permits selection. Equal, unknown, or incomparable priority stops for resolution. Filename, list order, or age never silently determines the result.
- **DSET-INVARIANT-GOV-016:** Atomic artifacts are immutable. Every later lifecycle transition, correction, withdrawal, or replacement is an append-only event or successor atom; absorption points backward from the successor, and current status plus reverse links are derived. A fully retired atom may only move byte-for-byte to its type's `archive/` subfolder with stable ID, digest, and lookup.
- **DSET-INVARIANT-GOV-017:** A Problem records a current insufficiency, a Question records uncertainty, and Conflict is a direct Question subtype for verified incompatible applicable authority. Risk and Opportunity are also Question subtypes; Defect, Gap, and Debt are Problem subtypes. Workflow never changes those meanings. Drift, failed proof, implementation nonconformance, and contradictory evidence follow their own dispositions and do not become Conflicts merely because two artifacts differ. Every atom is immutable and resolves only through linked successor atoms or append-only lifecycle events.
- **DSET-INVARIANT-GOV-018:** Every Decision is prompted for rationale, and every other atomic artifact may carry it when useful; rationale is recommended but optional, so omission alone never invalidates an atom, while supplied rationale never becomes a hidden owner of normative behavior, lifecycle state, or evidence.
