# Lifecycle orchestration rules

## Scope

These rules own deterministic next-action routing for the primary `dset`
workflow. They recommend the next useful action from current evidence; they do
not impose one universal end-to-end project order, authorize the selected
action, or restate the rules of the workflow selected next.

## Registered modes and recommendation precedence

Evaluate authoritative repository and hosted state, compute the applicable
mode set, then recommend one mode with its evidence and rationale. The order
below resolves direct conflicts, but admissible modes and genuine partial or
unordered dependencies remain visible; applicability alone is not a
recommendation and every Change need not execute every mode in sequence:

1. `initialize`: no valid DSET root exists.
2. `repair-governance`: a DSET root exists but selected ownership is invalid.
3. `decompose`: package, feature, or service boundaries are materially
   unresolved.
4. `diagnose`: an observed problem or failing proof requires cause-finding.
5. `clarify`: an open domain or specification question blocks a decision.
6. `landscape`: a consequential solution, dependency, framework, or language
   choice lacks comparable evidence.
7. `prototype`: an explicitly requested bounded experiment is needed to compare
   solution evidence.
8. `decisions`: accepted operator/session directives are not reconciled into
   current atomic records.
9. `compile`: an affected evergreen specification or plan must be current for
   the requested downstream workflow and accepted atoms remain beyond its
   recorded frontier.
10. `plan-proof`: accepted behavior lacks a complete test or applicable eval
   plan.
11. `plan-implementation`: accepted behavior and proof exist but the build plan
   is incomplete.
12. `implement`: an implementation outcome is requested or approved tasks
    remain; missing entry criteria activate its allowed prerequisite closure.
13. `verify`: implementation or governing artifacts changed after the latest
    applicable proof.
14. `triage-work`: a durable problem, opportunity, or question is
    unclassified or lacks its owning change/tracker link.
15. `release`: a verified change is ready for its guarded release transaction.
16. `complete`: no earlier mode applies.

An explicit operator-selected mode may override the recommendation only when
that mode is applicable and the override is recorded. Conflicting or
insufficient state stops with the unresolved evidence instead of guessing.

Return the first useful result as soon as the selected mode reaches its declared
exit criteria. Report the recommended handoff separately; do not continue
merely to advance through the mode list.

Public skills are entered by desired outcome. The operator need not manually
satisfy their entry criteria or know the prerequisite workflow graph. Each
entrypoint below may traverse only its registered prerequisite closure; the
requested outcome remains the root run and every child remains in the same DSET
session.

## Public entrypoint boundaries

| Entrypoint | Desired outcome and entry criteria | Exit/stop criteria |
|---|---|---|
| `dset` | Catch-all lifecycle request; returns one mode, its evidence, and the next authorized handoff | Does not perform a specialist workflow merely because it can name one |
| `dset-init` | No valid DSET root exists; returns an exact initialization preview and, only after write authorization, materialization plus validation result | Stops after preview when unauthorized and after validation when authorized; never continues into governed work |
| `dset-repair-governance` | A DSET root exists but selected ownership is invalid; returns stable diagnostics and proposed local repair paths | Stops before substantive rule resolution or any repair write without separate authorization |
| `dset-decompose` | Package, feature, service, or Work Area boundaries are materially unresolved; returns a bounded ownership/dependency decomposition | Stops before specification or implementation of a selected unit |
| `dset-clarify` | Explicit clarification request or blocking open question; returns decision-ready alternatives and remaining unknowns | Stops before choosing a consequential answer or implementing it |
| `dset-diagnose` | Explicit investigation request, current problem, or failed proof; returns evidence, cause confidence, and repair options | Stops before modifying the system unless repair receives separate authorization |
| `dset-landscape` | A consequential solution, dependency, framework, or language choice lacks comparable evidence; returns eligible candidates and comparison state | Stops before selection or implementation |
| `dset-prototype` | Explicit bounded experiment where solution uncertainty blocks a decision; returns comparable disposable evidence | Stops before production adoption or promotion |
| `dset-decisions` | Reconcile accepted directives from available current input/session and repository evidence into missing atomic records; acceptance and owning scope must be clear | Returns emitted IDs and affected evergreen owners; stops on uncertain acceptance, unresolved meaning, missing authority, semantic compilation, or implementation |
| `dset-compile` | An explicit compilation request or a downstream entry gate requires affected evergreen truth to include accepted atoms beyond its recorded frontier | Returns semantically synthesized owner updates, unchanged owners, pending atoms, conflicts, and frontier state; stops before implementation, testing, evaluation, or release |
| `dset-plan-proof` | Accepted behavior lacks complete deterministic tests or applicable qualitative evals; returns separate current test and eval plans | Stops before implementation or proof execution |
| `dset-plan-implementation` | Accepted behavior and proof obligations exist but executable work is incomplete; returns a dependency-ordered build plan and Change tasks | Stops before implementation |
| `dset-implement` | A bounded implementation outcome is requested; the chain first reconciles Decisions, then requires complete separate proof plans, an executable implementation plan, and implementation authorization | Returns bounded implementation plus test/eval assets and provenance; stops before claiming verification or release readiness |
| `dset-verify` | Implementation or governing artifacts changed after applicable proof; returns deterministic test results, eval evidence where applicable, and conformance status | Stops before repairing failures or releasing |
| `dset-overview` | Explicit read-only project-health request; returns current artifact/scope counts, coverage, freshness, open obligations, and a recommended handoff | Stops before refreshing stale derived state or performing the recommended workflow; it is not a lifecycle mode |
| `dset-triage` | A Decision, Question, Problem, or QA atom lacks semantic classification, ownership, priority, or Change/tracker linkage; returns Type/subtype routing and priority state | Stops before diagnosis, decision, proof planning, or implementation |
| `dset-release` | Explicit release request or verified release-ready change; returns prepared/verified release state and, only with release authority, publication result | Stops on any mismatch, missing gate, collision, or new authorization boundary |
| `dset-complete` | No earlier mode applies; returns terminal Change/session status and any residual open obligations | Stops without creating work solely to keep the workflow active |

Failed verification routes to `diagnose` when the cause is unknown and to
`implement` when a known accepted correction exists. Ambiguity routes to
`clarify`; solution comparison routes to `landscape` or an explicitly requested
prototype. Release readiness routes to `release`, but publication remains a
separate consequential effect.

## Authority and freshness

Authority is per concern, not a global ranking:

| Concern | Owner |
|---|---|
| Accepted behavior and public contract | Accepted package specs |
| Proposed, unaccepted intent | Active DSET change |
| Current file and commit content | Git working tree/index/commits |
| Proof result | Promoted proof plus the exact input commit/artifact identities it evaluated |
| Hosted PR, check, merge, tag, and release state | Configured forge |
| Selected workflow and rule ownership | Repository governance registry and governing documents |
| Operational hints | Local skill-run records, advisory only |

Derived proof becomes stale when any identified input changes. Hosted state is
queried live when it controls a decision. When owners disagree across concerns,
report the mismatch and refresh the derived surface; never let a cache or run
record override its source authority.

## Entry-criteria closure and authorization

One invocation owns one requested outcome and may invoke only registered
prerequisite workflows needed to satisfy that outcome's missing entry criteria.
After each transition, re-read authoritative state and record which criterion
became satisfied. Stop on unchanged or repeated state, a workflow cycle, no
progress, failure, ambiguity, the selected workflow's exit condition, or before
crossing a new authorization class. There is no fixed transition count; the
closure is finite because every transition must remove a missing criterion.
Writes, external messages, publication, and other consequential effects require
the same authorization they would require if invoked directly.

`.dset/dset_settings.toml` selects `workflows.implement.mode = "lazy"` or `"strict"`.
Missing configuration uses `lazy`.

## Installed command carrier

Governance uses `dset` as the logical command token because a repository
template cannot know a host installation path. An installed wrapper owns one
exact package-local Python-and-`dset.py` launcher prefix and must reuse that
same prefix for every later governed DSET instruction in the session. Bare
ambient `dset` execution and launcher substitution are forbidden. Installer
rendering uses argument-safe POSIX syntax on macOS, Linux, and WSL, and a
PowerShell call operator with single-quoted literals on native Windows.

In lazy mode, the following sequence applies.

The `implement` closure is ordered:

1. invoke `decisions` and reconcile available current host-session history,
   the DSET checkpoint and run records, Git, and current artifacts;
2. invoke `compile` only when an affected evergreen owner must be current for
   this implementation and accepted atoms remain beyond its frontier;
3. invoke `plan-proof` when separate Test or applicable Evaluation plans are
   incomplete;
4. invoke `plan-implementation` when the executable plan is incomplete; and
5. invoke `implement` only when all resolved entry criteria and authorization
   are satisfied.

Strict mode has no prerequisite closure. It invokes only `implement` from
already sufficient accepted artifacts and authorization. It must not create,
repair, or compile missing Decisions, Questions, Problems, QA, proof plans, or
implementation plans and must not fall back to lazy mode. Missing or ambiguous
input stops with the exact insufficiency.

`dset skills context --skill dset-implement ...` returns the selected
preparation mode. In lazy mode it starts or resumes the closure and returns its
persisted criterion state and exact `next_workflow`. Start a returned
prerequisite as a child with
`dset runtime child SESSION WORKFLOW ROOT --objective OBJECTIVE`, finish that
child with the session left `active`, then report the authoritative reread with
`dset runtime closure SESSION ROOT --workflow WORKFLOW --criterion NAME=VALUE`.
Criteria use `true`, `false`, or `unknown`. An observation-only closure update
omits `--workflow`; it is the only way to resume after missing evidence or
newly granted implementation authority.

The runtime marks successful lazy-mode `decisions`, `compile`, `plan-proof`,
`plan-implementation`, and `implement` transitions as satisfying their owned
criterion. It rejects an unexpected workflow, records parent/root run links,
and persists visited criterion states through compaction. Failed, stopped, or
ambiguous children; unchanged/repeated states; unknown required criteria; and
missing repository-write authorization stop or block with stable reason codes.
The runtime chooses the next registered workflow but never judges proof-plan
completeness, implementation-plan completeness, or operator authorization; the
caller supplies those observations from the governing repository and host.

In strict mode the runtime records a direct implementation closure, never
accepts a prerequisite child workflow, and retains the same run/session,
authorization, provenance, terminal-finish, Verification, and release
boundaries as lazy mode.

The `decisions` workflow treats session/checkpoint/run content as candidate
evidence, never authority. It emits only accepted atomic directives, preserves
session and LLM-session provenance, identifies affected evergreen owners, and
never edits an existing atom or compiles projections implicitly. Unclear acceptance or meaning produces an exact
Question or handoff; it is not silently decided. After compaction or unavailable
history, repository owners and the bounded checkpoint are reconciled and every
material unknown remains visible.

The primary `dset` entrypoint owns session start, checkpoint, and resume for
the whole chain. Only initial DSET entry may omit a DSET `session_id`. An active
handoff finalizes the current run with `dset runtime handoff`, leaves its
checkpoint active, returns that same explicit `session_id`, and requires the
next specialist context call to pass it. A workflow exit or return of control
is not terminal by itself. Only true completion or stop uses
`dset runtime finish`, which closes the session and must fail while another run
remains active. An automatically invoked specialist or governed model-only
workflow is a child run in the same session. Every transition updates
`DSET-RULE-SKILL-RUNS` continuity state. After host context compaction, resume
from that bounded checkpoint, re-read authoritative state, and recompute the
next mode before acting. Session continuity is an internal capability, not
another user-facing skill.

The governed direct-entry map is `decompose` → `dset-decompose`, `diagnose` →
`dset-diagnose`, `clarify` → `dset-clarify`, `landscape` → `dset-landscape`,
`prototype` → `dset-prototype`, `decisions` → `dset-decisions`, `compile` →
`dset-compile`, `plan-proof` →
`dset-plan-proof`, `plan-implementation` → `dset-plan-implementation`,
`implement` → `dset-implement`, `verify` → `dset-verify`, `triage-work` →
`dset-triage`, `release` → `dset-release`, and `complete` → `dset-complete`.
Each wrapper resolves the registered workflow shown by the mode. `dset-init`
and `dset-repair-governance` are the two pre-resolution exceptions below.

## Rootless initialization exception

Before a local DSET root exists, no repository-local rule can be resolved.
`initialize` is therefore a minimal distribution-owned bootstrap transaction,
not governed project work: select an explicit source/profile, preview the exact
paths and provenance, require write authorization, refuse every existing
destination, materialize the local manifest/registry/governing documents,
validate them, and stop. The next invocation must use the new local authority.
The bootstrap transaction cannot make product decisions or continue into a
second lifecycle mode.

When a root exists but governance validation fails, the distribution command
`dset rules check` may select `repair-governance` before local workflow
resolution. This is a diagnostic-only exception: emit stable schema/ownership
diagnostics and proposed local paths, then stop. It cannot resolve substantive
rules from the invalid registry or write a repair without separate explicit
authorization.
