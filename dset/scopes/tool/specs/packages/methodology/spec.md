# Methodology TOOL specification

## DSET-REQUIREMENT-TOOL-001 — The canonical workflow is executable

The framework must provide one cross-platform CLI with `new`, `check`, `verify`, `trace`, and guarded `archive` commands. `check` is dependency-light and read-only; every write is explicit and refuses an existing destination.

**Scenario DSET-SCENARIO-TOOL-001:** A contributor can run `python -m dset_toolchain check .` without installing OpenSpec or a second methodology and receives stable diagnostic codes for malformed artifacts.

## DSET-REQUIREMENT-TOOL-002 — Traceability is generated from durable identities

`dset/scopes/gov/generated/traceability.yaml` must be generated in stable order from committed change manifests and repository-qualified PR references. It may cache evidence relationships but must not replace GitHub as owner of PR state, checks, diffs, or merge results.

**Scenario DSET-SCENARIO-TOOL-002:** Regeneration without source changes produces no diff, and every archived change resolves to the PR that owns its implementation history.

## DSET-REQUIREMENT-TOOL-003 — Archive writes are guarded

Archive execution must require complete profile artifacts, fresh verification, accepted-truth reconciliation, an archive-ready status, a real PR identity, and a free dated destination. Dry-run is the default.

**Scenario DSET-SCENARIO-TOOL-003:** A proposed, failed, incomplete, PR-less, or colliding change remains active and no archive path is overwritten.

## DSET-REQUIREMENT-TOOL-004 — DSET 0.3 self-hosting is bounded

The DSET 0.3 self-hosting gate must have exactly three bounded levels: the last
released validator checks the candidate change; the candidate checks this
repository; and the candidate materializes and checks one temporary adopter.
During a declared bootstrap transition, an incompatible pre-transition
validator records its exact rejection as degraded assurance rather than a pass;
the candidate and temporary adopter still must pass. The temporary adopter must
not create another adopter or traverse unrelated nested DSET roots.

**Scenario DSET-SCENARIO-TOOL-004:** One release run records released-to-candidate
as pass or an explicitly declared bootstrap-transition rejection, requires
candidate-to-repository and candidate-to-temporary-adopter to pass, then
terminates at the declared fixed point.

## DSET-REQUIREMENT-TOOL-018 — Project health has a portable deterministic renderer

The toolchain must compute the project-health model from discovered canonical
artifacts, registry ownership, traceability, Git identities, and current proof
metadata, then render a GitHub-portable Markdown view. Default inspection is
read-only; an explicit write refreshes only the declared generated destination
and a check mode detects staleness. Repository, layer, package, and Work Area
drill-downs use the same source model. A later local or hosted dashboard may
render that model but cannot introduce private health state or new authority.

**Scenario DSET-SCENARIO-TOOL-018:** Two runs over unchanged inputs produce the
same Markdown bytes. A changed Requirement makes check mode report the view
stale, explicit refresh updates only the generated health destination, and
every row links back to a canonical artifact or an explicit unknown.

## DSET-REQUIREMENT-TOOL-019 — Priority conflict resolution is deterministic

The toolchain must evaluate candidate incompatibilities between any governed
artifacts. It first resolves each atom's semantic Type and direct subtype plus
each document's role independently from the workflow that discovered it, then distinguishes genuine
Conflicts from drift, assurance changes, nonconformance, and evidence
adjudication. Only verified incompatible applicable claims over the same scope,
concern, and effective time emit a first-class immutable Conflict atom.
Immutable external authority wins over mutable project truth. Mutually
unsatisfiable immutable obligations stop with an explicit non-compliance state;
priority may order remediation but cannot make either obligation satisfied.

For a comparable policy conflict whose governing profile permits selection,
the resolver applies explicit artifact-specific precedence, then the selected
profile's effective priority order. A strictly higher comparable priority
selects the effective conflicting claim without invalidating the other artifact
outside that context.

Other classes produce deterministic dispositions rather than artificial
winners: an active atomic source beats its stale compiled projection and routes
recompilation; an absorbing atom beats absorbed predecessors; authority/
evidence conflicts update assurance and affected gates; implementation/
authority conflicts create a conformance Problem; evidence/evidence conflicts
apply the registered proof plan and quality/freshness rules or stop for
adjudication; generated/canonical conflicts mark generated output stale; and
implementation conflicts follow the traceable owner or stop when ownership is
missing. Priority orders handling for every class but cannot convert evidence
into authority or a failing obligation into compliance.

An archive relocation is valid only for a fully retired atom with no active
claim, reliance, or unresolved lifecycle work. The toolchain verifies the
content digest is unchanged, moves it only to the artifact type's `archive/`
subfolder, updates canonical ID lookup, and rejects partial-absorption moves,
content edits, broken references, or deletion.

Every emitted Conflict begins open. A deterministic disposition appends a
lifecycle event linking its resolution record and durable resolving artifacts;
an unresolved or unsatisfiable Conflict remains open and blocking. Neither the
Conflict nor its source claims are edited. Non-Conflict dispositions keep their
own typed evidence or Problem/Question paths and do not emit a false Conflict.

Equal, unknown, cyclically inherited, or incomparable priorities must stop with
the artifact IDs, values, sources, context, and safe next action. Every automatic
resolution is a derived transactional record and Conflict lifecycle event
containing those same inputs, both artifact roles, the conflict class,
disposition or selected claim, governing profile edition, and invalidation
trigger. Atomic sources are never rewritten;
an authorized compiler may update only declared evergreen projections.
Reprioritization or input changes invalidate the affected resolution and health
projection.

**Scenario DSET-SCENARIO-TOOL-019:** A Requirement and project-owned Contract
conflict over one selectable output field. With no explicit-precedence result,
the higher-priority Contract governs that field and a resolution record is
emitted. Changing either priority makes check mode mark the record stale; equal
priority stops for a Decision instead of choosing by scan order. A fixture with
two incompatible immutable Contracts stops as unsatisfiable regardless of
priority. An active Decision/spec fixture selects the Decision and emits a
stale-projection/recompile disposition; a Test/spec fixture emits an
assurance-change disposition rather than selecting the Test. A successor atom
beats an absorbed predecessor by lifecycle relation rather than age.
