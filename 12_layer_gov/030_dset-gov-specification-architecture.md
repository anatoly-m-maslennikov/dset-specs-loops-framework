---
artifact_type: specification
artifact_subtype: architecture
scope_path:
  - layer:gov
priority: high
---

# Governance architecture and bootstrap

**Rule ID:** `DSET-RULE-ARCHITECTURE`

## Authority

The adopting repository's discovered project settings select a local governance
profile. Schema 1.8 owns operator settings and the enabled artifact whitelist
at `.dset/dset_settings.toml`; `.dset/artifact_catalog.toml` separately owns
the executable type/subtype route catalog. Earlier schemas are migration input,
not current authority. The discovered registry maps workflow and
rule IDs to exactly one maintained governing document and its active atomic
sources inside the target project's `.dset`. An active source atom is authority; the
materialized document is its current view only while its semantic refresh is
current. Framework template and version remain provenance only.

Resolution precedence is project-local active source atom, then its current
maintained governing document, then an explicitly selected local profile, then
failure. A source/projection mismatch selects the source, marks the projection
stale, and blocks reliance until semantic refresh. Never fall back to wrapper
prose, agent memory, a generated cache, an installed copy, or remote framework
text. Atomic sources: `DSET-REQUIREMENT-GOV-102` and
`DSET-REQUIREMENT-GOV-070`.

## Rule authority and assurance

Governance separates authority from assurance. A normative rule governs only
when the current repository-local registry resolves its accepted, active,
applicable atomic sources and one maintained governing document and validates the
dependency and precedence closure. The registered layer and scope bound its
scope; the selected profile version and customization state identify its
current edition. An atomic source/document mismatch makes the document stale;
the atom remains authoritative while the relying gate stops for semantic refresh.

`depends_on` declares prerequisites required to interpret or execute a rule.
`precedence_over` declares only how an explicit conflict between rules is
resolved. Neither relation implies the other, both graphs must be acyclic, and
every rule declares both fields even when the lists are empty. Registry order
is not precedence. If selected rules conflict and no declared precedence path
resolves the conflict, governed work stops rather than choosing implicitly.

Active Requirements, Constraints, Contracts, and Implementation Decisions may
authorize change. Provenance identifies origin but does not authorize. Test and
Evaluation results, reviews, and other evidence
assess reliance claims. None becomes rule authority merely by existing or
passing. Missing or stale assurance leaves the affected claim
pending or stale and blocks the relying gate; it does not silently erase an
otherwise valid rule. `DSET-RULE-ARTIFACT-MAINTENANCE` governs transactional
discharge and risk-proportionate proof with explicit reopen conditions.
Atomic source: `DSET-DECISION-GOV-002`.

## Bootstrap

These steps govern repository-rooted workflows. When no manifest exists, only
the distribution command `dset init` may run its minimal preview, explicit
write-authorization, no-overwrite materialization, validation, and stop
transaction. It cannot pretend that a local registry already exists or
continue into governed work. `DSET-RULE-LIFECYCLE` governs later local routing,
not the pre-root bootstrap command.

1. Walk upward from the working location until exactly one project containing the unique settings carrier `dset_settings.toml` inside `.dset` is found. Nested competing project roots fail closed.
2. Read the selected `repository_governance` profile.
3. Search only the selected `.dset` for settings, governing documents, atoms,
   maintained artifacts, evidence, and Version records; resolve each carrier by
   stable ID or globally unique name.
4. Validate local ownership, dependencies, documents, applicability, customization, and wrapper identity.
5. Resolve the requested workflow in registry order.
6. Stop before governed work when any selected owner is unresolved or incompatible.

Explicit justified non-applicability is valid. Missing or invalid selected ownership is not.

## State boundaries

Project settings select the profile and enabled whitelist; the artifact catalog
owns type/subtype routes, identity kinds, carriers, and persistence behavior;
the registry owns resolution
metadata; active atoms own normative claims; governing documents own maintained
presentation; wrappers own invocation only; generated indexes and caches are
derived. Writes that change customization status are explicit and never mutate
atoms.

Durable DSET relations and registry references never store physical carrier
paths. A resolver may derive a transient location after selecting `.dset`, but
must not expose that location as identity or use files outside `.dset` as
fallback governance. Repository and Work Area paths remain execution inputs for
implementation targeting only.

## Storage roots

Governed project state, materialized methodology, project settings, artifact
catalogs, tools, and skill instructions live in `.dset/`. Durable running
records live in `.dset_journal/` as append-only NDJSON. Disposable caches,
locks, scratch state, and process-local output live in `.dset_runtime/`.
No reader treats the journal or runtime root as a governance fallback.
Atomic source: `DSET-REQUIREMENT-GOV-100`.

## Methodology materialization

The repository-root methodology is the reusable authoring source. Installation
materializes the selected released methodology into
`.dset/000_dset_methodology/` as ordinary project-local files. Skills resolve
only the installed `.dset` copy during governed work; they do not follow
symlinks, file pointers, or live references back to the framework repository.
Refreshing the installed copy is an explicit one-way operation with provenance,
comparison, and no implicit overwrite. Atomic sources:
`DSET-IMPL-GOV-002` and `DSET-REQUIREMENT-GOV-052`.

## Semantic boundaries

A typed atom is the smallest independently reviewable primary project claim or
directive. It is not the real-world subject, condition, operator act, file,
record carrier, performed work, result, evidence, gate disposition, or derived
view connected to it. One stored record may link several of those roles but
must keep their meanings and identifiers distinct.

In particular, an operator acceptance act grants authority to applicable
Requirement, Constraint, Contract, or Implementation Decision content; a Test
Plan or Evaluation Plan defines a checking Method; execution performs work;
results and logs provide evidence; and Verification derives a current bounded
reliance statement. A carrier does none of those merely by containing readable
text. Multi-head claims split into linked sibling atoms. Material
classification ambiguity stays in Exploration Mode or becomes a Question.

## Revision behavior and artifact function

DSET separates Revision mode from artifact meaning and Content role:

- **Atomic authority sources** are accepted, active, applicable Requirements,
  Constraints, Contracts, and Implementation Decisions. Atoms are immutable.
  Complete replacement is a successor atom with an
  explicit acyclic `replacement_of` relation, followed by byte-stable archive
  relocation of the predecessor.
- **Append-only record sequences** include NDJSON running logs and event
  ledgers. Accepted records remain ordered and immutable; readers may derive
  maintained catalogs or TOON views without changing the source sequence.
- **Maintained semantic views** are updatable current views such as specs,
  implementation plans, deterministic test plans, eval plans, architecture,
  runbooks, and governing rules. They are reasoned from active source atoms and
  become stale when they disagree with one.
- **Context and evidence atoms** record Questions and their Conflict,
  Risk, and Opportunity subtypes; Problems and their Defect, Gap, and Debt
  subtypes; QA executions and results; proofs; sessions/runs; and optional
  Version records.
  They route work or assess claims without becoming normative authority merely
  by existing.
- **Implementation artifacts** are code, Test code, Evaluation prompts or
  datasets, CI
  workflows, scripts, generated runtime assets, and configuration examples.
  They implement atomic sources through maintained semantic views when those
  views are enabled.

This separation preserves distinct atomic authority, append-only records,
maintained views, implementation, commit provenance, and session provenance.
Atomic source: `DSET-DECISION-GOV-001`.

An active atom wins over a stale maintained view. A replacement successor
wins over its archived predecessor by explicit `replacement_of`, never by age.
Resolution uses `resolution_of`; a repeated archived Question or Problem uses
`recurrence_of`; reopening is forbidden. Archive relocation keeps semantic ID,
bytes, original seal, source-return identity, and lookup. Generated views may
summarize these relationships but never become authority.

## Public workflow contract

Every public workflow declares three operator-visible boundaries: the trigger
that makes it applicable, the first useful result it can return, and the
stop/return condition beyond which it needs another workflow or new authority.
Wrappers may expose these boundaries for discovery, but the registered local
governing document owns their meaning.

## Derived navigation

Thin hubs and generated ID, relation, and term indexes may improve navigation.
They are reproducible views over canonical artifacts, carry no independent
authority, and must link back to stable IDs and owning sources. A stale or
missing generated view cannot override or invalidate otherwise valid canonical
truth.

## One-level architecture views

Every project hub includes a Mermaid view of its immediate enabled structural
children: feature groups when present, otherwise features and/or layers. Every
feature-group hub shows its features. Every feature or layer hub shows the main
functions, capabilities, or components it immediately owns. A project does not
create empty diagrams for structural levels it has not enabled.

Each view stays one level deep, links its owning hubs, atomic-artifact folders,
or long-lived non-atomic owners, and remains consistent with current accepted
truth. It never links individual atoms or `.dset_runtime` descendants. It is
Navigation or compiled Specification/Architecture, never independent
authority. Cross-level details belong in the child view rather than expanding
one whole-project diagram until it becomes unreadable.
Atomic source: `DSET-REQUIREMENT-GOV-031`.

## Features versus layers

Features are peer capabilities. Their interactions are horizontal and are
governed by explicit Contracts at their narrowest common structural owner.
Neither feature becomes an architectural authority over the other merely
because it calls, supplies data to, or is delivered before the other.

Layers are an ordered refinement chain:
`META → GOV → TOOL → SKILL → IMPL → OPS`.
Layer authority may affect the same layer or move only forward to later layers;
it never governs, overrides, or takes precedence over an earlier layer. Direct
influence on the immediately following layer is preferred because it keeps
boundaries local and legible. An explicit longer forward jump is valid when an
intermediate layer has no meaningful ownership to add.

When an otherwise eligible normative conflict reaches priority comparison, the
artifact owned by the earlier layer receives one virtual effective-priority
step over the later-layer artifact. The bonus applies once regardless of layer
distance and never changes stored priority. It is a comparison consequence of
the forward-only authority chain, not a new backward dependency or a permanent
precedence relation.

A downstream artifact may cite, depend on, implement, check, or provide
evidence for upstream authority. Those relations consume earlier authority;
they do not reverse it. In the rule registry, a rule may depend only on a rule
in the same or an earlier layer, and `precedence_over` may target only the same
or a later layer. Backward authority fails validation instead of being inferred
from workflow order, carrier location, or a cross-layer reference.

If a backward dependency cannot be deleted, re-homed, or resolved without
misrepresenting the system, DSET proposes reclassifying the coupled owners as
features and replacing layer authority with horizontal Contracts. It reports
the proposal and waits for operator acceptance; it never silently changes the
project structure.

## Project-level and child-level ownership

Every claim and compiled artifact belongs to the narrowest common structural
ancestor that contains all affected owners and subjects. A concern spanning
features inside one feature group belongs to that group; a concern spanning
groups or layers belongs to the project. Abstract, important, or reusable does
not by itself mean project-level.

During an eligible conflict comparison, a strict structural-scope ancestor
receives one virtual effective-priority step over its applicable descendant.
Thus a project Contract gains one step over a conflicting feature, group, or
layer Requirement. Peer features and unrelated scopes gain no structural
bonus, and the comparison never changes either artifact's canonical owner.

The project-level set owns genuinely project-wide outcomes, user journeys, and
requirements; cross-child Contracts and dependency rules; shared API, data,
and event semantics; end-to-end Tests and Evaluations; cross-cutting
Invariants and Constraints; system architecture and integration topology;
whole-project version, release, readiness, and publication artifacts; and
cross-owner Decisions, Questions, Problems, and Analysis Reports. Parent
artifacts link child-owned detail and never duplicate it as parallel truth.

## Typed artifact relations

New artifacts store consequential forward edges in `relations` using exactly
one of `child_of`, `analysis_of`, `projection_of`, `implementation_of`,
`check_of`, `evidence_for`, `resolution_of`, `solution_for`, `override_of`,
`replacement_of`, `recurrence_of`, or `relates_to`. Reverse edges are derived and never
authored. One source-target pair has one primary relation.

`child_of` narrows or decomposes a claim and keeps both active. `analysis_of`
owns investigation. `implementation_of` owns realization. `check_of` owns a
Test Plan or Evaluation Plan definition. `evidence_for` owns observed support.
`resolution_of` closes a Question, Conflict, or Problem. `override_of` changes
authority only in a narrower scope. `replacement_of` completely replaces an
atom and requires the predecessor to be archived. `recurrence_of` links a new
Question or Problem to an archived predecessor of the same registered type without
reactivating it. These structural, replacement, and recurrence meanings never
overlap for one pair.

`relates_to` is a symmetric trace fallback only. It carries no authority,
dependency, assurance, precedence, or lifecycle meaning and satisfies no
implementation or QA coverage. Ordinary citations and shared subject matter
remain Markdown links. `depends_on` and `precedence_over` remain specialized
rule-registry controls rather than general artifact relations.

`projection_of` normally stores a range with one registered atomic type, one
exact structural scope, and a `through` boundary naming the latest included
artifact identity in that type/scope sequence. Archive placement selects
applicable active atoms
through that frontier. A newer applicable atom makes the projection stale;
individual targets are for explicit exceptions only.

Deterministic validation checks relation vocabulary, shape, direction, target
resolution, uniqueness, source suitability, range frontiers, incompatible
combinations, and applicable cycles. It never infers semantic truth from an
edge.
Atomic sources: `DSET-IMPL-GOV-004` and
`DSET-DECISION-GOV-035`.
