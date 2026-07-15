# Artifact maintenance

**Rule ID:** `DSET-RULE-ARTIFACT-MAINTENANCE`

## Ownership

Every normative rule ID has one editable governing document. Hubs navigate, wrappers invoke, templates seed, generated installations distribute, and indexes summarize; none become another writable rule owner.

## Writes and cutover

- Confirm authorization before editing existing project artifacts.
- Write each conclusion to its owning accepted package, active change, decision, runbook, proof plan, or evidence artifact.
- Keep deterministic tests and qualitative/probabilistic evals separate.
- Materialized rules become project-owned immediately. Later framework releases provide an explicit comparison and proposed delta, never an invisible overwrite.
- Record intentional local customization with `dset rules refresh`, retaining the source profile, version, template path, and digest as provenance.
- During migration, map every old rule/spec/plan/decision/runbook/evidence surface and make the old writer a concise pointer, read-only history, verified archive, or remove it only after cutover proof.
- Refuse an existing destination and keep the previous owner writable when validation fails.

## Decision discharge

A resolved consequential Question produces a Decision, but the Decision is not
a second specification. Discharge its normative consequences into the owning
canonical Requirements, Scenarios, Contracts, Design, proof plans, or operating
rules; link those edits and the closed Question back to the Decision. Keep the
Decision as the durable rationale, alternatives, trade-offs, and consequences.

A Decision records status and decision date, its evidence basis, superseded and
successor Decisions, confirmation or violation evidence, and the condition that
reopens it. Counter-evidence may withdraw a Decision's current authority without
deleting its history or the evidence that once supported it. Supersession creates
an explicit successor link; it never silently rewrites the earlier Decision.

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
