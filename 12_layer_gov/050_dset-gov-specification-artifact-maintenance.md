---
artifact_type: specification
artifact_subtype: governance
scope_path:
  - layer:gov
priority: high
---

# Artifact maintenance

**Rule ID:** `DSET-RULE-ARTIFACT-MAINTENANCE`

## Ownership

Every normative rule ID has one editable governing document. Hubs navigate, wrappers invoke, templates seed, generated installations distribute, and indexes summarize; none become another writable rule owner.

## Writes and cutover

- Treat every operator input in a governed project as intake. Exploration input
  creates no artifacts until a durable conclusion is accepted. Then classify
  and emit one or more immutable atoms before implementing their consequences;
  split independent claims and never derive type from the workflow.
- Select one canonical carrier by job: Markdown with YAML frontmatter for
  human-governed narrative artifacts; TOML for directly executed human-edited
  configuration; JSON for external contracts, standardized schemas, wire data,
  and generated machine data; JSONL/NDJSON for append-only runtime records; and
  native formats for source code, CI, lockfiles, and host manifests.
- Every governed Markdown artifact begins with valid YAML frontmatter and stays
  legible and navigable in GitHub preview. Sources:
  `DSET-CONSTRAINT-GOV-002` and `DSET-REQUIREMENT-GOV-095`.
- Keep standards-compliant JSON Schema files as canonical JSON. Never keep
  competing editable representations of one concern.
- Confirm authorization before editing existing project artifacts.
- Write each conclusion to its owning accepted package, active change, decision, runbook, proof plan, or evidence artifact.
- Keep deterministic tests and qualitative/probabilistic evals separate.
- Classify each durable artifact by exactly one Revision mode: `atomic`,
  `append_only`, or `maintained`. Artifact type separately derives Content role
  and Governance locus. Placement and applicability determine whether an
  atomic source participates in current authority.
- Materialized rules become project-owned immediately. Later framework releases provide an explicit comparison and proposed delta, never an invisible overwrite.
- Author reusable methodology only in the repository-root source. Refresh the
  installed `.dset/000_dset_methodology/` snapshot only through an explicit
  one-way operator synchronization command; never mirror ordinary edits or
  copy installed files back into the source.
- Record intentional local customization with `dset rules refresh`, retaining the source profile, version, unique template carrier name, and digest as provenance.
- During migration, map every old rule/spec/plan/decision/runbook/evidence surface and make the old writer a concise pointer, read-only history, verified archive, or remove it only after cutover proof.
- Perform multi-carrier mechanical migrations with bounded deterministic Python
  scripts that validate all expected source shapes before writing and stop
  without partial mutation on unexpected structure. Source:
  `DSET-IMPL-GOV-001`.
- Refuse an existing destination and keep the previous owner writable when validation fails.

## Revision-mode behavior

| Revision mode | Permitted write behavior |
|---|---|
| `atomic` | Emit one immutable governed unit; changed meaning creates a linked successor |
| `append_only` | Preserve accepted records and order; append only complete new records |
| `maintained` | Revise existing content through the registered artifact procedure |

Running logs use canonical NDJSON and `append_only`. Each append writes one
complete UTF-8 JSON record; readers fail closed on malformed or incomplete
records. Rotation seals the completed segment and opens a new sequence without
rewriting accepted records.

A persisted TOON rendering of a running log is a non-authoritative maintained
Observation view. It records the NDJSON source identity and frontier and is
regenerated or replaced through its registered procedure. It is never appended
as if it were the source log.

Current specifications, plans, catalogs, and generated projections are
maintained artifacts. Their registered procedures define currentness,
staleness, refresh, synchronization, and generation; DSET defines no additional
currentness class.

## Transactional discharge

A resolved consequential Question produces the applicable Requirement,
Constraint, Contract, or Implementation Decision. Every accepted, active,
applicable authority atom is a source, not a parallel maintained
specification. Refresh its normative consequences
into the owning maintained specifications, Design, proof plans, or operating
rules. Link the resolver to the Question with `resolution_of`; move
the Question to its type-local `archive/` after resolution. Keep the resolver
as durable authority plus its
linked context, alternatives, rationale, trade-offs, and consequences where
applicable.
If atomic authority and a maintained view differ, the atom wins, the view is
stale, and the relying release gate fails until semantic refresh.

All active authority atoms follow the same source-to-projection rule. Problems,
Questions and their direct subtypes, check results, evidence records, and other
transactional context route work or support those sources but do not become
authority merely by existing. Closing a transactional artifact without
refreshing its accepted normative consequences into applicable maintained
views leaves the work incomplete.

Atomic artifacts are immutable in governed meaning. Editable drafts are working
documents, not atoms. Emission fixes the primary claim or proof intent,
rationale, accepted authority and creation state, provenance, scope, priority
at creation, and relation meanings; a Test Plan or Evaluation Plan also fixes its conditions,
criteria, thresholds, and expected disposition. Later semantic or lifecycle
change requires a successor atom. Storage state is only active or archived.

An ID, filename, path, classification-label spelling, heading label, carrier
encoding, seal, or reference spelling is representation, not the atom's
governed meaning. A governed migration may change those fields only through a
complete collision-free mapping that preserves the referenced artifacts and
relation semantics, records equivalence and Git return evidence, and removes
old aliases from accepted lookup after cutover. A claim, rationale,
authority, provenance fact, scope meaning, relation meaning, or check-criterion
change requires a successor atom. Aggregate mutable transition ledgers and
unproved resealing are invalid.

A successor atom declares `replacement_of` relations to completely replaced
older atoms. Replacement is explicit, acyclic, validated, and never inferred
from a timestamp, ID, or file order. Each predecessor has at most one complete
replacement successor. The successor carries forward or explicitly replaces
every still-applicable consequence, and each replaced predecessor moves
byte-for-byte to its type-local `archive/`. A partial change uses narrower
linked claims and leaves the older atom active; it is not `replacement_of`.
Reverse `replaced_by` links and the active compilation set are derived views.

Resolution uses `resolution_of` from the resolving authority or outcome to the
Question, Conflict, or Problem, then archives the resolved atom. Withdrawal
archives the atom without a semantic successor; any future intent belongs in a
Version Roadmap. Reopening is forbidden. A new Question or Problem that repeats
an archived concern is a new atom with `recurrence_of` to the archived
predecessor. `recurrence_of` requires the same registered artifact type and never
reactivates the predecessor.

Archive relocation is the only atom state transition. It preserves bytes,
carrier name, semantic identity, and stable identity-based lookup. An atom with
an active `child_of` or `override_of` dependant cannot be archived. Archived
atoms remain immutable history and do not participate in active compilation,
unresolved-parent, self-link, or cycle gates.

Every commit that archives atoms records:

```text
Archives: <artifact-id>
Archive-Reason: replaced|resolved|withdrawn
Archive-Reference: <successor-resolver-or-version-id>
Session: <host-prefixed-session-id>
```

Repeat `Archives:` for every moved atom. Use separate commits when reasons or
references differ. `Archive-Reference` may be omitted only for terminal
withdrawal whose commit body explains why no successor or future intent exists.
Source: `DSET-DECISION-GOV-035` and `DSET-REQUIREMENT-GOV-096`.

The executable boundary is explicit:

```text
dset atom seal ROOT --file ATOM.md
dset atom archive ROOT --id SEMANTIC-ID
dset conflict ROOT --candidate CONFLICT.json --emit CONFLICT.md
dset conflict ROOT --candidate CONFLICT.json --check-result RESULT.json
dset compile ROOT --write
```

Sealing refuses an already registered semantic ID and records the carrier's
content digest. Validation fails after content, semantic classification, or
registered location drift. Relation validation rejects unresolved targets,
replacement or recurrence cycles, multiple replacement successors, active
replacement predecessors, and invalid recurrence Types. Conflict resolution
classifies role
and applicability before consulting explicit precedence or effective priority;
it reports whether a first-class open Conflict atom and later resolution artifact
are required, but never edits an atom. Explicit emission creates and seals one
`question/conflict` atom whose `relates_to` edges name both incompatible
parties; the Conflict claim owns the incompatibility semantics. A resolving
artifact uses `resolution_of`, then the Conflict moves to `archive/`.
Recorded dispositions bind the effective priority values and sources, context,
precedence, and profile scale; check mode rejects them when that basis changes.
An active atom with no structural dependant may move to its adjacent `archive/`
folder through a lossless carrier transition while canonical lookup retains its
identity and original seal.

The traceability compiler generates a digest-bound index from every active
authority source to one or more explicit maintained-view claim fragments. A
fragment must be a
canonical ID-owned section, table row, or labeled block; a loose ID mention is
not a projection. The index binds both the complete projection carrier and the
identified fragment. `dset compile ROOT --check` fails when the active source
set, source digest, projection digest, fragment location, or fragment digest
changes. This deterministic gate proves structured linkage and byte freshness,
not semantic equivalence. Review or Evaluation judges whether the fragment
faithfully carries the source consequence. The index is evidence of
traceability, not another authority source.

## Rationale

Every Implementation Decision should record a concise rationale for its
selected option.
Rationale is also recommended for another atomic artifact when it explains why
the atom was emitted, interpreted, prioritized, related, or scoped as written
and that explanation will help review, support, replacement, or
conflict resolution. It remains optional: absence alone never invalidates an
atom or blocks a gate.

When present, rationale is explanatory context, not hidden authority. It must
not carry a Decision or subtype, state transition, or evidence claim that
is absent from that concern's canonical owner. Keep a short rationale in the
atom or link a separate rationale artifact; keep maintained implementation
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

Every commit that changes maintained views or implementation artifacts must name
the authority IDs it implements in the commit body, for example
`Implements: DSET-REQUIREMENT-IMPL-004`. A linked Problem may explain why a
correction is needed, but only active applicable authority authorizes the
resulting behavior.

The repository manifest activates deterministic commit validation from an
explicit commit or from the commit that first added the manifest. Every later
non-merge commit uses exactly one provenance mode: implementation has one or
more authority `Implements:` IDs; evidence has both authority `Decision:` IDs
and known `Verifies:` IDs. Both modes require exactly one valid
`Session:` trailer. Optional `Resolves:` IDs must identify Problems. Unknown
IDs, invalid implementation authority, mixed modes, and missing provenance
fail the repository check.

Immutable historical commits are never rewritten or exempted. When an older
commit in the validated range cannot satisfy the current trailer grammar, the
project manifest may append one correction bound to its full commit SHA and
exact original-message digest. The correction declares the ordinary provenance
mode, canonical authority and applicable Verification/Problem IDs, exactly one
Session ID, and a rationale. The original must be invalid, the corrected view
must pass the same rules as a current commit, and correction entries are unique
and append-only.

Every newly emitted atomic artifact has explicit LLM session provenance. Use
unique `llm_session_ids` with stable host-prefixed
IDs such as `codex:<session-id>` when an LLM produced the record; use an
explicit empty list or `none` for human-only work. A review or correction emits
another linked record rather than revising the original provenance. Missing
provenance is not equivalent to human-only work. Session provenance is not
authority by itself; it lets a reviewer find the working context that created
or assessed the atom.

Atomic status comes from the catalog's Revision mode, not from belonging to a
family hierarchy. Change manifests, intake queues, skill-run records, and
session checkpoints follow their registered Revision mode; none becomes atomic
merely because a workflow uses it. Every supported carrier enforces explicit
provenance appropriate to its role. Git and commit coverage are mandatory.
Source: `DSET-REQUIREMENT-GOV-065`.

## Proof and derived-view maintenance

Promoted proof supports one named claim for one intended use. It records the
producer or performed work, method and setup, applicable repository/version/
environment/assumption context, observation time or validity window, exact
commit or artifact version, evidence location and polarity, and reopen trigger.
Evidence currentness is derived against the current subject, method, and
context; it is never a mutable status stored in an immutable Evidence Record.
An attempted use that the evidence cannot support remains `uncertain` or
`pending`; it is not converted into a positive conclusion.
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
a maintained owner, or a proof obligation. Review does
not authorize repair. Refresh accepted consequences into current views and
reopen only affected proof before implementation or release relies on them.

## Priority

Priority is the single generic ordered rank. Every governed atomic authority,
append-only sequence, maintained artifact, context/evidence atom, and
implementation artifact declares it directly or inherits it through one
visible canonical relation.
Implementation files may inherit from their owning authority or check-plan atom, or an
optional Change, rather than duplicating metadata inside every file.

Actionable work uses priority as one execution-order input; dependencies,
authorization, gates, and resources may still determine the next action.
Impact, severity, likelihood, expected value, obligations, and Outcome value
stay in their owning semantics as priority evidence, not a second universal
rank. New writers use the stored scale `high`, `medium`, `low`. Creation
defaults are Constraint `high`; Contract, Requirement, and Decision `medium`;
and implementation carrier `low`. Other roles inherit through their owning
atom or Change, then use the project `medium` default. `highest` is
virtual-only. No other stored value is valid. Source:
`DSET-REQUIREMENT-GOV-063`. The former `critical` label is
recoded to `high` by a governed meaning-preserving migration. `deferred` is not
a priority: current low-urgency work uses `low`, while non-current work belongs
in a named future Version Roadmap.

For an eligible comparison, add one effective-priority step to a strict
structural-scope ancestor and one step to an earlier owning layer. Apply each
axis once, add the bonuses, and cap at `highest` on
`low → medium → high → highest`. A project Contract therefore outranks an
otherwise-equal child Requirement; an earlier-layer artifact outranks an
otherwise-equal later-layer artifact. Peer features, same-level artifacts, and
unrelated scopes receive no bonus.

Classify each conflict before resolving it. Immutable external authority wins
over mutable project truth. If two immutable obligations cannot both be
satisfied, priority orders remediation or escalation but cannot claim
compliance; stop for an exception, boundary change, or external resolution.
For a declared comparable and resolvable policy conflict, apply explicit
applicable lifecycle and override relations first. The default `ask_always`
mode explains the result and asks before claim selection. Opt-in
`auto_by_effective_priority` selects only one unique higher effective priority;
equal, same-level, unknown, cyclically inherited, uncertain, or incomparable
results ask.

The resolver accepts every governed artifact pairing and uses artifact role
before priority:

- an active atomic authority source versus its maintained view selects the
  atomic source, marks the view stale, and routes semantic refresh;
- an archived predecessor is inactive; its explicit replacement successor wins
  without consulting age or priority;
- authority versus QA/Test, QA/Evaluation, review, or proof updates assurance and the
  relying gate; evidence never rewrites authority;
- implementation versus authority creates a conformance Problem;
- conflicting assurance evidence follows the registered proof plan and
  evidence-quality/freshness rules or stops for adjudication;
- generated views versus canonical sources mark the view stale; and
- conflicts inside implementation follow the owning authority or stop when no
  owner or applicable rule exists.

Priority orders remediation for every conflict class, but selects a normative
claim only where the governing profile and selected mode permit it. Record both
artifact IDs, roles, stored priorities, applied scope/layer bonuses, effective
priorities and sources, conflict class, context, mode, disposition or selected
claim, and profile edition. Never infer resolution from filename, list order,
age, or layer distance. Reprioritization invalidates affected derived
resolutions. Conflict handling never edits an atom; refresh updates only the
declared maintained view.

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

## Progressive governance surfaces

DSET starts atomic-first. The registered optional governance surfaces are
`maintained-specification`, `test-plan`, `evaluation-plan`,
`implementation-plan`, `project-overview`, and `architecture-view`.
`.dset/dset_settings.toml` records an explicit Boolean for every registered
surface; a missing table or key reads as inactive, and an unknown surface fails
closed.

Activating a surface adds only that surface's currentness and entry-gate
obligations. Deactivating it removes those obligations without deleting or
rewriting its carrier or Git history. Reactivation must reconcile a retained
carrier against current atomic authority before calling the surface current.
Activation never disables or enables an entire revision mode.

`dset configure ROOT status` and `recommend` are read-only. `activate` and
`deactivate` preview by default and write only with `--execute`. The writer
changes only the selected Boolean, materializes missing registered defaults,
and preserves unrelated TOML text and comments. Recommendations are advisory
and cite repository evidence; they never mutate configuration.
