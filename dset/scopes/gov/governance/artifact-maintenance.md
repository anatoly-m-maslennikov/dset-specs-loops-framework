# Artifact maintenance

**Rule ID:** `DSET-RULE-ARTIFACT-MAINTENANCE`

## Ownership

Every normative rule ID has one editable governing document. Hubs navigate, wrappers invoke, templates seed, generated installations distribute, and indexes summarize; none become another writable rule owner.

## Writes and cutover

- Confirm authorization before editing existing project artifacts.
- Write each conclusion to its owning accepted package, active change, decision, runbook, proof plan, or evidence artifact.
- Keep deterministic tests and qualitative/probabilistic evals separate.
- Classify each durable artifact by role: atomic authority source, evergreen
  compiled projection, transactional context/evidence, or implementation.
  Status and applicability determine whether an atomic source is active.
- Materialized rules become project-owned immediately. Later framework releases provide an explicit comparison and proposed delta, never an invisible overwrite.
- Record intentional local customization with `dset rules refresh`, retaining the source profile, version, template path, and digest as provenance.
- During migration, map every old rule/spec/plan/decision/runbook/evidence surface and make the old writer a concise pointer, read-only history, verified archive, or remove it only after cutover proof.
- Refuse an existing destination and keep the previous owner writable when validation fails.

## Transactional discharge

A resolved consequential Question produces a Decision. An accepted, active,
applicable Decision is an atomic authority source, not a parallel evergreen
specification. Compile its normative consequences into the owning evergreen
Requirements, Scenarios, Contracts, Design, proof plans, or operating rules;
emit a lifecycle event linking those projections and the resolved Question to
the Decision. Keep the Decision as the durable rationale, alternatives,
trade-offs, and consequences.
If the Decision and compiled projection differ, the Decision wins, the
projection is stale, and the relying release gate fails until recompilation.

Accepted active Requirements, Contracts, Decisions, and other registered
normative atoms follow the same source-to-projection rule. Problems,
Opportunities, Questions, evidence records, and other transactional context
route work or support those sources but do not become authority merely by
existing. Closing a transactional artifact without compiling its accepted
normative consequences leaves the work incomplete.

Atomic artifacts are immutable. Editable drafts are working documents, not
atoms. Emitting an atom fixes its ID, content, provenance, creation status, and
links. Later acceptance, rejection, reopening, correction, withdrawal, or other
state change is a new append-only lifecycle event; current status is derived.

A successor atom may declare `absorbs` links to older atoms. Absorption is
explicit, acyclic, validated, and never inferred from a timestamp, ID, or file
order. It removes the older atom from the active compilation set without
editing or deleting it. The successor carries forward or explicitly replaces
every still-applicable consequence. A partial replacement links the affected
claims and leaves all other older claims active; it does not absorb the entire
atom. Reverse `absorbed_by` links, current status, confirmation/violation state,
and the active compilation set are derived views, never edits to an atom.

When an atom has no active claims, open reliance, or unresolved lifecycle work,
it is fully retired and may move byte-for-byte into its artifact type's
`archive/` subfolder. The move preserves its ID and content digest; the
canonical ID registry updates the location so references still resolve. Partial
absorption never qualifies. Archived atoms remain immutable history and are
never deleted merely because they are inactive.

## Rationale

Every Decision should record a concise rationale for its selected option.
Rationale is also recommended for another atomic artifact when it explains why
the atom was emitted, interpreted, prioritized, related, or scoped as written
and that explanation will help review, support, absorption, replacement, or
conflict resolution. It remains optional: absence alone never invalidates an
atom or blocks a gate.

When present, rationale is explanatory context, not hidden authority. It must
not carry a Requirement, Contract, lifecycle transition, or evidence claim that
is absent from that concern's canonical owner. Keep a short rationale in the
atom or link a separate rationale artifact; keep evergreen implementation
references focused on current executable truth. Templates prompt for rationale,
and structured schemas permit a non-empty bounded value without requiring it.

## Commit and session provenance

Every commit that changes evergreen truth or implementation artifacts must name
the Decision or Decisions it implements in the commit body, for example
`Implements: DSET-DECISION-GOV-001`. If a small fix has no accepted Decision,
the commit must name the governing Problem, Opportunity, Question, or Change
that authorized it and explain why no Decision was required.

Every newly emitted atomic artifact or append-only lifecycle event has explicit
LLM session provenance. Use unique `llm_session_ids` with stable host-prefixed
IDs such as `codex:<session-id>` when an LLM produced the record; use an
explicit empty list or `none` for human-only work. A review or correction emits
another linked record rather than revising the original provenance. Missing
provenance is not equivalent to human-only work. Session provenance is not
authority by itself; it lets a reviewer find the working context that created
or assessed the atom.

Current Change manifests, intake items, Decisions, promoted proofs, local
skill-run records, and session checkpoints are atomic artifacts. Their schemas,
templates, or validators must enforce the explicit provenance shape before a
repository claims this rule is implemented.

## Proof and derived-view maintenance

Promoted proof supports one named claim for one intended use. It records the
producer or performed work, method and setup, applicable repository/version/
environment/assumption context, observation time or validity window, exact
commit or artifact version, evidence location and polarity, currentness status,
and reopen trigger. An attempted use that the evidence cannot support remains
`uncertain` or `pending`; it is not converted into a positive conclusion.
Contrary evidence or a changed input is a defeater that makes only the affected
claim closure stale. Refresh that smallest closure; do not rerun unrelated proof
merely because it shares a repository.

When reliance or risk is high, also separate evidence producer from source
maintainer, distinguish the planned method from performed work and deviations,
and record credible rival explanations plus the evidence that supports or
weakens them. These fields are triggered extensions, not mandatory ceremony for
every bounded proof.

Generated hubs and ID, relation, or term indexes are thin non-authoritative
views. A reliance-bearing view states the structure it captures, what it omits,
its permitted and prohibited uses, its canonical return path, and its
currentness. Regenerate only the affected closure, retain stable links to
canonical owners, and report staleness rather than treating a generated view as
truth.

A generated project-health view follows the same boundary. Report artifact
counts by declared class/type/layer/status and applicable Work Area, unresolved
work, proof freshness, and traceability coverage without turning counts into a
target. Every ratio exposes numerator, denominator, exclusions,
not-applicable, unknown, and stale counts. Link each gap to its canonical owner;
never invent a Decision, code artifact, Test, or Eval merely to improve a
percentage. Markdown is the portable baseline. An interactive renderer may use
the same derived model but cannot own private health state.

## Independent review flow

Cross-host or external review uses a bounded packet and transactional report.
The packet names exact commits/artifacts, resolved rules, criteria, scope, and
allowed effects. The report has a mandatory envelope for reviewer/host and
available model/tool version, `llm_session_ids`, exact inputs, method, time,
limitations, and stable finding IDs; its findings body may be free-form.

For each finding, record evidence, confidence, impact, and one explicit
disposition: reject with rationale, defer, or route to a Problem, Opportunity,
Question, Decision, Change, evergreen owner, or proof obligation. Review does
not authorize repair. Compile accepted consequences into current truth and
reopen only affected proof before implementation or release relies on them.

## Priority

Priority is the single generic ordered rank. Every governed atomic authority,
evergreen projection, transactional context/evidence, and implementation
artifact declares it directly or inherits it through one visible canonical
relation.
Implementation files may inherit from their owning Requirement, Decision,
Change, Test, or Eval rather than duplicating metadata inside every file.

Actionable work uses priority as one execution-order input; dependencies,
authorization, gates, and resources may still determine the next action.
Impact, severity, likelihood, expected value, obligations, and Outcome value
stay in their owning semantics as priority evidence, not a second universal
rank. The selected project profile owns one bounded scale, legend, inheritance,
override, and escalation rules.

Classify each conflict before resolving it. Immutable external authority wins
over mutable project truth. If two immutable obligations cannot both be
satisfied, priority orders remediation or escalation but cannot claim
compliance; stop for an exception, boundary change, or external resolution.
For a declared comparable and resolvable policy conflict, apply explicit
specific precedence first; otherwise, higher effective priority wins the
conflicting claim. Equal, unknown, cyclically inherited, or incomparable
priority stops for a Decision or explicit precedence.

The resolver accepts every governed artifact pairing and uses artifact role
before priority:

- an active atomic authority source versus its evergreen projection selects the
  atomic source, marks the projection stale, and routes recompilation;
- an absorbed atom is inactive where the absorption applies; the explicit
  absorbing successor wins without consulting age or priority;
- authority versus Test, Eval, review, or proof updates assurance and the
  relying gate; evidence never rewrites authority;
- implementation versus authority creates a conformance Problem;
- conflicting assurance evidence follows the registered proof plan and
  evidence-quality/freshness rules or stops for adjudication;
- generated views versus canonical sources mark the view stale; and
- conflicts inside implementation follow the owning authority or stop when no
  owner or applicable rule exists.

Priority orders remediation for every conflict class, but selects a normative
claim only where the governing profile permits selection. Record both artifact
IDs, roles, effective priority values and sources, conflict class, context,
disposition or selected claim, and profile edition. Never infer resolution from
filename, list order, or age. Reprioritization invalidates affected derived
resolutions. Conflict handling never edits an atom; recompilation updates only
the declared evergreen projection.

## Artifact threshold

Ordinary reversible work may return a bounded result without opening a committed
Change. Work becomes reliance-bearing and requires durable DSET artifacts when
it changes accepted truth, crosses authorization or ownership boundaries,
requires coordination, audit, delayed reuse, rollback, or release evidence, or
would be unsafe to reconstruct from a session. Ignored run records may support
investigation but never replace those artifacts.

## Cross-Change handoff

Handoff between Changes names stable artifact IDs, exact commits or versions,
applicable Contracts, evidence locations, currentness, and reopen triggers. A
summary without those anchors is context, not authoritative delivery evidence.
