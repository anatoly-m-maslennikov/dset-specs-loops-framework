# Governance architecture and bootstrap

**Rule ID:** `DSET-RULE-ARCHITECTURE`

## Authority

The adopting repository's discovered project manifest selects a local governance
profile. Schema 1.2 owns that manifest at `dset/scopes/meta/dset.yaml` and the
governance registry at `dset/scopes/gov/governance.yaml`; legacy schema 1.0/1.1
owns the compatible central paths. The discovered registry maps workflow and
rule IDs to exactly one editable governing document inside the repository. A
materialized document is project truth immediately; its source template and
version remain provenance only.

Resolution precedence is project-local registered rule, then an explicitly selected local profile, then failure. Never fall back to wrapper prose, agent memory, a generated cache, an installed copy, or remote framework text.

## Rule authority and assurance

Governance separates authority from assurance. A normative rule governs only
when the current repository-local registry resolves it to one applicable,
editable governing document and validates its dependency and precedence
closure. The registered layer and path bound its scope; the selected profile
version and customization state identify its current edition.

`depends_on` declares prerequisites required to interpret or execute a rule.
`precedence_over` declares only how an explicit conflict between rules is
resolved. Neither relation implies the other, both graphs must be acyclic, and
every rule declares both fields even when the lists are empty. Registry order
is not precedence. If selected rules conflict and no declared precedence path
resolves the conflict, governed work stops rather than choosing implicitly.

Decisions and provenance authorize and explain change. Tests, evals, reviews,
and evidence assess reliance claims. None becomes rule authority merely by
existing or passing. Missing or stale assurance leaves the affected claim
pending or stale and blocks the relying gate; it does not silently erase an
otherwise valid rule. `DSET-RULE-ARTIFACT-MAINTENANCE` governs transactional
discharge and risk-proportionate proof with explicit reopen conditions.

## Bootstrap

These steps govern repository-rooted workflows. When no manifest exists, only
the distribution command `dset init` may run its minimal preview, explicit
write-authorization, no-overwrite materialization, validation, and stop
transaction. It cannot pretend that a local registry already exists or
continue into governed work. `DSET-RULE-LIFECYCLE` governs later local routing,
not the pre-root bootstrap command.

1. Walk upward from the working path until exactly one supported manifest is found: schema 1.2 `dset/scopes/meta/dset.yaml` or legacy `dset/dset.yaml`. Duplicate authorities fail.
2. Read the selected `repository_governance` profile.
3. Discover and validate the layout-owned governance registry, local ownership, dependencies, documents, applicability, customization, and wrapper identity.
4. Resolve the requested workflow in registry order.
5. Stop before governed work when any selected owner is unresolved or incompatible.

Explicit justified non-applicability is valid. Missing or invalid selected ownership is not.

## State boundaries

The project manifest selects the profile; the registry owns resolution metadata; governing documents own rules; wrappers own invocation only; generated indexes and caches are derived. Writes that change customization status are explicit and never overwrite governing documents.

## Artifact classes

DSET separates three authority classes:

- **Evergreen artifacts** are updatable current truth. Specs, implementation
  plans, deterministic test plans, eval plans, architecture, contracts,
  runbooks, and governing rules may change in place through a bounded Change.
  They state the current accepted version.
- **Transactional artifacts** record bounded facts, choices, observations, or
  questions in time. Decisions, Problems, Opportunities, Questions, proof
  records, session/run records, release evidence, and Change records are not
  edited into a new truth shape silently; they are resolved, superseded,
  archived, or linked forward.
- **Implementation artifacts** are the executable or concrete delivery layer:
  code, tests, eval prompts/datasets, CI workflows, scripts, generated runtime
  assets, and configuration examples. They implement evergreen truth and cite
  the transactional artifacts that authorized or constrained the work.

Transactional artifacts influence current behavior only after their accepted
consequences are compiled into the owning evergreen artifact. A generated view
may summarize that relationship, but the evergreen owner remains the current
truth and the transactional artifact remains provenance.

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
