# Lifecycle orchestration rules

## Scope

These rules own deterministic next-action routing for the primary `dset`
workflow. They recommend the next useful action from current evidence; they do
not impose one universal end-to-end project order, authorize the selected
action, or restate the rules of the workflow selected next.

## Registered modes and recommendation precedence

Evaluate authoritative repository and hosted state in this order and recommend
the first applicable mode. The ordering resolves competing next-action signals;
it is not a requirement that every Change execute every mode in sequence:

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
8. `decide`: a consequential resolved question lacks its Decision.
9. `plan-proof`: accepted behavior lacks a complete test or applicable eval
   plan.
10. `plan-implementation`: accepted behavior and proof exist but the build plan
   is incomplete.
11. `implement`: approved tasks remain and their prerequisites are satisfied.
12. `verify`: implementation or governing artifacts changed after the latest
    applicable proof.
13. `triage-work`: a durable problem, opportunity, or question is
    unclassified or lacks its owning change/tracker link.
14. `release`: a verified change is ready for its guarded release transaction.
15. `complete`: no earlier mode applies.

An explicit operator-selected mode may override the recommendation only when
that mode is applicable and the override is recorded. Conflicting or
insufficient state stops with the unresolved evidence instead of guessing.

Return the first useful result as soon as the selected mode reaches its declared
output boundary. Report the recommended handoff separately; do not continue
merely to advance through the mode list.

## Specialist boundaries

| Entrypoint | Trigger and first useful result | Stop/return boundary |
|---|---|---|
| `dset` | Catch-all lifecycle request; returns one mode, its evidence, and the next authorized handoff | Does not perform a specialist workflow merely because it can name one |
| `dset-clarify` | Explicit clarification request or blocking open question; returns decision-ready alternatives and remaining unknowns | Stops before choosing a consequential answer or implementing it |
| `dset-diagnose` | Explicit investigation request, current problem, or failed proof; returns evidence, cause confidence, and repair options | Stops before modifying the system unless repair receives separate authorization |
| `dset-prototype` | Explicit bounded experiment where solution uncertainty blocks a decision; returns comparable disposable evidence | Stops before production adoption or promotion |
| `dset-release` | Explicit release request or verified release-ready change; returns prepared/verified release state and, only with release authority, publication result | Stops on any mismatch, missing gate, collision, or new authorization boundary |

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

## Chaining and authorization

One invocation selects one bounded mode by default. It may invoke one
registered specialist workflow and then must re-read authoritative state before
selecting anything else. Automatic chaining stops after two workflow
transitions, on any failure or ambiguity, before any new authorization class,
or when the selected workflow reaches its own stop condition. Writes, external
messages, publication, and other consequential effects require the same
authorization they would require if invoked directly.

The primary `dset` entrypoint owns session start, checkpoint, and resume for
the whole chain. A direct specialist invocation joins a matching explicit
session or starts one; an automatically invoked specialist or governed
model-only workflow is a child run in the current session. Every transition
updates `DSET-RULE-SKILL-RUNS` continuity state. After host context compaction,
resume from that bounded checkpoint, re-read authoritative state, and recompute
the next mode before acting. Session continuity is an internal capability, not
another user-facing skill.

The exact specialist map is `clarify` → `domain-clarification`, `diagnose` →
`diagnosis`, `prototype` → `prototyping`, `triage-work` → `work-triage`, and
`release` → `release`. Other modes resolve the project-owned rules registered
for that mode; a skill name is not synthesized for them.

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
