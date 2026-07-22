# Artifact maintenance

**Rule ID:** `DSET-RULE-ARTIFACT-MAINTENANCE`

## Ownership

Every normative rule ID has one editable governing document. Hubs navigate, wrappers invoke, templates seed, generated installations distribute, and indexes summarize; none become another writable rule owner.

## Writes and cutover

- Treat every operator input in a governed project as intake. Classify and emit
  one or more immutable semantic atoms before implementing its consequences;
  split independent claims and never derive Type from the workflow.
- Use TOML for DSET-owned structured artifacts and TOML frontmatter for DSET
  Markdown. Keep host/ecosystem/wire/runtime formats and generated compatibility
  adapters explicit and non-authoritative. Never keep editable YAML/JSON and
  TOML copies of the same claim.
- Keep standards-compliant JSON Schema files as canonical external contract
  carriers. Validate and retain them as JSON; do not create an editable TOML
  duplicate or call them generated without a governed source and freshness map.
- Confirm authorization before editing existing project artifacts.
- Write each conclusion to its owning accepted package, active change, decision, runbook, proof plan, or evidence artifact.
- Keep deterministic tests and qualitative/probabilistic evals separate.
- Classify each durable artifact by role: atomic authority source, evergreen
  compiled projection, transactional context/evidence, or implementation.
  Status and applicability determine whether an atomic source is active.
- Materialized rules become project-owned immediately. Later framework releases provide an explicit comparison and proposed delta, never an invisible overwrite.
- Author reusable methodology only in the repository-root source. Refresh the
  installed `.dset/000_dset_methodology/` snapshot only through an explicit
  one-way operator synchronization command; never mirror ordinary edits or
  copy installed files back into the source.
- Record intentional local customization with `dset rules refresh`, retaining the source profile, version, unique template carrier name, and digest as provenance.
- During migration, map every old rule/spec/plan/decision/runbook/evidence surface and make the old writer a concise pointer, read-only history, verified archive, or remove it only after cutover proof.
- Refuse an existing destination and keep the previous owner writable when validation fails.

## Transactional discharge

A resolved consequential Question produces a Decision. Every accepted, active,
applicable Decision—including any direct subtype—is an atomic authority source,
not a parallel evergreen specification. Compile its normative consequences
into the owning evergreen specifications, Design, proof plans, or operating
rules; emit a lifecycle event linking those projections and the resolved
Question to the Decision. Keep the Decision as durable authority plus its
linked context, alternatives, rationale, trade-offs, and consequences where
applicable.
If the Decision and compiled projection differ, the Decision wins, the
projection is stale, and the relying release gate fails until recompilation.

All active Decision atoms follow the same source-to-projection rule. Problems,
Questions and their direct subtypes, QA results, evidence records, and other
transactional context route work or support those sources but do not become
authority merely by existing. Closing a transactional artifact without
compiling its accepted normative consequences leaves the work incomplete.

Atomic artifacts are immutable in their semantic records. Editable drafts are working documents,
not atoms. Emitting an atom fixes its ID, semantic payload, provenance,
creation status, and links. Later semantic or lifecycle change is a new
append-only event or successor atom; current status is derived.

Atomic semantic content never changes. A directory move preserves the carrier
name and bytes; identity-based discovery therefore needs no durable path
mapping or relocation ledger. A carrier-name or representation migration emits
one immutable transition record containing the old and new unique carrier
names, digests, semantic-equivalence proof, and Git return identity. A semantic
change requires a successor atom. Aggregate path-transition ledgers and direct
resealing are invalid.

A successor atom declares `replacement_of` relations to older atoms. Matching
append-only lifecycle events mark the predecessors `absorbed`. Replacement is
explicit, acyclic, validated, and never inferred from a timestamp, ID, or file
order. Absorption removes the older atom from the active compilation set without
editing or deleting it. The successor carries forward or explicitly replaces
every still-applicable consequence. A partial replacement links the affected
claims and leaves all other older claims active; it does not absorb the entire
atom. Reverse `absorbed_by` links, current status, confirmation/violation state,
and the active compilation set are derived views, never edits to an atom.

When an atom has no active claims, open reliance, or unresolved lifecycle work,
it is fully retired and may move into its artifact type's `archive` subfolder.
The move preserves bytes, carrier name, semantic identity, and stable
identity-based lookup.
Partial absorption never qualifies. Archived atoms remain immutable history
and are never deleted merely because they are inactive.

Lifecycle absorption is also the repair mechanism when a sealed atom contains
an invalid relationship that cannot be edited. The absorbing successor must
pass the complete current-lineage gate. The inactive predecessor retains its
authored relationship as historical data, but that relationship no longer
participates in active unresolved-parent, self-link, or cycle gates.

The executable boundary is explicit:

```text
dset atom seal ROOT --file ATOM.md
dset atom event ROOT --candidate EVENT.json
dset atom archive ROOT --id SEMANTIC-ID
dset conflict ROOT --candidate CONFLICT.json --emit CONFLICT.md
dset conflict ROOT --candidate CONFLICT.json --check-result RESULT.json
dset compile ROOT --write
```

Sealing refuses an already registered semantic ID and records the carrier's
content digest. Validation fails after content, semantic classification, or
registered location drift. Lifecycle writes append unique events and reject
unresolved targets or absorption cycles. Conflict resolution classifies role
and applicability before consulting explicit precedence or effective priority;
it reports whether a first-class open Conflict atom and later resolution event
are required, but never edits an atom. Explicit emission creates and seals one
`question/conflict` atom whose `relates_to` edges name both incompatible
parties; the Conflict claim owns the incompatibility semantics. A separate
append-only lifecycle event records its later resolution.
Recorded dispositions bind the effective priority values and sources, context,
precedence, and profile scale; check mode rejects them when that basis changes.
An explicitly retired atom with no active child reliance may move to its
adjacent `archive/` folder only through a lossless carrier transition while the
canonical registry updates current lookup and retains the original seal.

Compilation generates a digest-bound index from every active authority source
to one or more explicit evergreen claim fragments. A fragment must be a
canonical ID-owned section, table row, or labeled block; a loose ID mention is
not a projection. The index binds both the complete projection carrier and the
identified fragment. `dset compile ROOT --check` fails when the active source
set, source digest, projection digest, fragment location, or fragment digest
changes. This deterministic gate proves structured projection and freshness,
not semantic equivalence. Review or Evaluation judges whether the fragment
faithfully carries the source consequence. The index is evidence of
compilation, not another authority source.

## Rationale

Every Decision should record a concise rationale for its selected option.
Rationale is also recommended for another atomic artifact when it explains why
the atom was emitted, interpreted, prioritized, related, or scoped as written
and that explanation will help review, support, absorption, replacement, or
conflict resolution. It remains optional: absence alone never invalidates an
atom or blocks a gate.

When present, rationale is explanatory context, not hidden authority. It must
not carry a Decision or subtype, lifecycle transition, or evidence claim that
is absent from that concern's canonical owner. Keep a short rationale in the
atom or link a separate rationale artifact; keep evergreen implementation
references focused on current executable truth. Templates prompt for rationale,
and structured schemas permit a non-empty bounded value without requiring it.

## Artifact-creation strictness and promotion eligibility

`.dset/dset_settings.toml` selects `artifacts.creation_strictness` independently from
other optional capabilities. The default is `medium`; `high` is opt-in.

The same file must explain every operator setting, accepted value, behavioral
effect, and default with concise comments. Defaults are executable behavior,
not undocumented parser fallbacks.

At medium strictness, emit an accepted atom only when its authority, one primary
claim, Type, owning structural scope, provenance, material links, priority, and
acceptance state are clear. Optional non-authoritative detail may remain
explicitly unknown. A material unknown that could change the claim becomes a
separate Question or blocks the emission.

At high strictness, do not emit while authority, meaning, boundary, Type,
scope, lineage, conflict state, or proof obligation is materially ambiguous.
Ask focused questions until the atom can safely remain immutable, or stop
without writing it.

Before emission, assess whether the unchanged claim belongs at the immediately
broader enabled scope under narrowest-common-scope ownership. Propose eligible
feature-to-group, feature/group-to-project, or layer-to-project promotion one
step at a time. Promotion requires operator acceptance and is never automatic.
Local evidence, implementation, exceptions, and vocabulary remain local. A
later promotion emits a new linked broader-scope atom; it never moves or edits
the original.

The deterministic pre-emission check accepts a JSON candidate and never writes:

```text
dset artifact assess ROOT --candidate CANDIDATE.json
```

Every candidate explicitly supplies authority, one claim, semantic `type`,
structural `scope`, `llm_session_ids`, material links, priority, acceptance,
and a promotion assessment. High strictness additionally requires boundary,
lineage, conflict state, and verification obligation. `unknowns` identifies
each unresolved field, whether it is material, and the focused question to ask.
Promotion names only the immediate `parent_scope`, affected children, whether
the claim applies unchanged, whether local context is required, and an optional
operator `disposition` of `keep_local` or `promote`. Eligibility without a
disposition stops with a proposal; `promote` stops local emission so a new
candidate can be assessed at the broader scope. The assessor resolves scopes,
immediate parents, affected children, material links, priority values, and
session syntax against repository authority. `dset atom seal` repeats this
assessment and refuses the immutable write when it is not allowed.

## Commit and session provenance

Every commit that changes evergreen truth or implementation artifacts must name
the Requirement or Decision IDs it implements in the commit body, for example
`Implements: DSET-REQUIREMENT-IMPL-004`. A linked Problem may explain why a
correction is needed, but only an active Requirement or Decision authorizes the
resulting behavior.

The repository manifest activates deterministic commit validation from an
explicit commit or from the commit that first added the manifest. Every later
non-merge commit uses exactly one provenance mode: implementation has one or
more authority `Implements:` IDs; evidence has both authority `Decision:` IDs
and known `Verifies:` IDs. Both modes require exactly one valid
`Session:` trailer. Optional `Resolves:` IDs must identify Problems. Unknown
IDs, non-Decision implementation authority, mixed modes, and missing provenance
fail the repository check.

Immutable historical commits are never rewritten or exempted. When an older
commit in the validated range cannot satisfy the current trailer grammar, the
project manifest may append one correction bound to its full commit SHA and
exact original-message digest. The correction declares the ordinary provenance
mode, canonical Decision and applicable Verification/Problem IDs, exactly one
Session ID, and a rationale. The original must be invalid, the corrected view
must pass the same rules as a current commit, and correction entries are unique
and append-only.

Every newly emitted atomic artifact or append-only lifecycle event has explicit
LLM session provenance. Use unique `llm_session_ids` with stable host-prefixed
IDs such as `codex:<session-id>` when an LLM produced the record; use an
explicit empty list or `none` for human-only work. A review or correction emits
another linked record rather than revising the original provenance. Missing
provenance is not equivalent to human-only work. Session provenance is not
authority by itself; it lets a reviewer find the working context that created
or assessed the atom.

Only emitted Decision, Question, Problem, and QA claims are semantic atoms.
Change manifests, intake queues, skill-run records, and session checkpoints are
mutable transactional or execution-state carriers; they may contain or point
to atoms but do not become atoms because a workflow uses them. Promoted proof
is immutable evidence, not a semantic atom. Every supported carrier still
enforces explicit provenance appropriate to its role.

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
its permitted and prohibited uses, its canonical return identity or unique
carrier name, and its currentness. Regenerate only the affected closure, retain
stable identity references to canonical owners, and report staleness rather
than treating a generated view as truth.

A generated project-health view follows the same boundary. Report artifact
counts by declared class/type/layer/status and applicable Work Area, unresolved
work, proof freshness, and traceability coverage without turning counts into a
target. Every ratio exposes numerator, denominator, exclusions,
not-applicable, unknown, and stale counts. Link each gap to its canonical owner;
never invent a Decision, code artifact, Test, or Evaluation merely to improve a
percentage. Markdown is the portable baseline. An interactive renderer may use
the same derived model but cannot own private health state.

## Independent review flow

Cross-host or external review uses a bounded packet and transactional report.
The packet names exact commits/artifacts, resolved rules, criteria, scope, and
allowed effects. The report has a mandatory envelope for reviewer/host and
available model/tool version, `llm_session_ids`, exact inputs, method, time,
limitations, and stable finding IDs; its findings body may be free-form.

For each finding, record evidence, confidence, impact, and one explicit
disposition: reject with rationale, defer, or route to a Problem or Question
and applicable subtype, a Decision and applicable subtype, an optional Change,
an evergreen owner, or a proof obligation. Review does
not authorize repair. Compile accepted consequences into current truth and
reopen only affected proof before implementation or release relies on them.

## Priority

Priority is the single generic ordered rank. Every governed atomic authority,
evergreen projection, transactional context/evidence, and implementation
artifact declares it directly or inherits it through one visible canonical
relation.
Implementation files may inherit from their owning Decision or QA atom, or an
optional Change, rather than duplicating metadata inside every file.

Actionable work uses priority as one execution-order input; dependencies,
authorization, gates, and resources may still determine the next action.
Impact, severity, likelihood, expected value, obligations, and Outcome value
stay in their owning semantics as priority evidence, not a second universal
rank. The selected project profile owns one bounded scale, legend, inheritance,
override, and escalation rules. `core-v1` orders `critical`, `high`, `medium`,
`low`, then `deferred`; lower list position means lower current execution
priority. `.dset/dset_settings.toml` publishes the ordered scale and its default. An
artifact without a direct priority inherits through its owning atom or Change,
then the project default. An explicit historical `unknown` remains unknown
until an append-only priority event supplies a value; it never silently falls
back.

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
- authority versus QA/Test, QA/Evaluation, review, or proof updates assurance and the
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
