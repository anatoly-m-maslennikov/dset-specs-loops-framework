---
artifact_type: implementation_decision
artifact_id: DSET-DECISION-GOV-003
scope_path: ["layer:gov"]
priority: high
decided_at: 2026-07-16
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Decision — Immutable atoms and role-aware conflict handling

- **Resolves Question:** direct operator requirements for universal priority,
  conflict handling, source compilation, and atomic lifecycle
- **Replaces claims:** the `DSET-DECISION-GOV-001` claim that evergreen files
  own current truth and the `DSET-DECISION-GOV-002` claim that governing
  documents remain the sole project authority after bootstrap; all unaffected
  claims in both Decisions remain active
- **Selected option:** use one priority rank for every governed artifact,
  classify every conflict by role and lifecycle before priority, and make every
  emitted atomic artifact immutable

## Context and scope

DSET needs one consistent model for Requirements, Contracts, Decisions,
evergreen specs and plans, Tests, Evals, evidence, and implementation. A single
priority attribute should support project health, work ordering, and safe
automatic conflict handling without turning every disagreement into a
priority contest or reporting false compliance.

The operator established two additional source-of-truth constraints: evergreen
artifacts are compiled projections of accepted atomic sources, so an active
Decision wins when its projection is stale; and emitted atomic artifacts are
immutable. Replacement occurs only through a new atom that explicitly absorbs
older atoms. Fully retired atoms may move byte-for-byte to a type-local archive.

This Decision governs repository and Work Area artifacts across every DSET
layer. It does not choose the concrete priority scale or implement the schemas,
resolver, compiler, health renderer, or archive runtime.

## Evidence basis and rationale

One generic priority avoids overlapping importance/severity/priority metadata.
Impact, likelihood, severity, value, obligation, and gate status remain typed
evidence for the one rank. Priority can order handling for every artifact while
artifact role and lifecycle prevent category errors:

- immutable external authority beats mutable project truth;
- two incompatible immutable obligations are unsatisfiable, not resolved by
  claiming the lower-priority obligation passed;
- explicit absorption beats absorbed predecessors without age-based
  precedence;
- active atomic sources beat stale evergreen projections;
- evidence changes assurance rather than authority;
- implementation mismatches create conformance Problems;
- generated drift marks the view stale; and
- explicit precedence then priority selects a normative claim only when the
  governing profile permits selection.

An append-only atomic history retains provenance and makes absorption auditable.
Derived current status and reverse links avoid rewriting old records. A bounded
byte-stable archive keeps inactive history out of the active surface without
deleting it or breaking ID lookup.

## Consequences and discharge

This Decision is compiled into:

- `DSET-REQUIREMENT-GOV-020..021` and `DSET-INVARIANT-GOV-016` for atomic
  sources, compiled projections, immutability, absorption, and retirement;
- `DSET-REQUIREMENT-GOV-024..026` and `DSET-INVARIANT-GOV-013..015` for health,
  external review, universal priority, and conflict governance;
- `DSET-REQUIREMENT-TOOL-018..019` and
  `DSET-INVARIANT-TOOL-004..005` for planned deterministic rendering and
  pairwise conflict disposition;
- the accepted GOV/TOOL test and eval plans;
- `DSET-RULE-ARCHITECTURE` and `DSET-RULE-ARTIFACT-MAINTENANCE`; and
- the active Change's specification connections, tasks, implementation plan,
  verification matrix, and intake gaps.

Every governed artifact has one explicit or traceably inherited priority.
Priority orders remediation across all conflict classes but selects a claim
only for a declared comparable policy conflict whose profile permits
selection. The resolver records the artifact roles, lifecycle state, priority
sources, context, conflict class, disposition, selected claim when applicable,
profile edition, and invalidation trigger.

Every emitted atom is immutable. Later state is an append-only lifecycle event.
An absorbing successor points backward and must preserve or explicitly replace
all still-applicable consequences. Partial replacement leaves unaffected older
claims active. Only an atom with no active claims, open reliance, or unresolved
lifecycle work may move byte-for-byte to `archive/`, retaining ID, digest, and
canonical lookup.

## Lifecycle policy at emission

- **Expected confirmation evidence:** atomic/lifecycle schemas, immutable
  baseline digests, pairwise conflict fixtures, projection compilation checks,
  archive relocation tests, generated health output, and independent evals
- **Known counter-evidence:** current repository schemas and validators do not
  yet enforce the selected model
- **Reopen when:** one priority cannot represent project ordering, an artifact
  pair has no safe deterministic disposition, source compilation loses an
  accepted consequence, or append-only atoms cannot support a required
  lifecycle
- **If reopened, retain:** role-before-priority classification, no false
  compliance, evidence/authority separation, stable provenance, and explicit
  lifecycle relations
- **If reopened, withdraw:** only the smallest disproven conflict, priority, or
  lifecycle rule
- **Retirement condition:** every consequence is absorbed by a validated
  successor and no current projection, implementation, proof, or release relies
  on this Decision

This emitted Decision atom is immutable. Any later status change, correction,
counter-evidence, reopening, absorption, or retirement must be a new append-only
lifecycle event or successor atom.
