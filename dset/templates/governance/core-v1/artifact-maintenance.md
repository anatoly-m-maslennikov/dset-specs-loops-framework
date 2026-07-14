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

## Proof and derived-view maintenance

Promoted proof records the claim proved, intended use, exact commit or artifact
version, currentness status, evidence location, and reopen trigger. When an
input changes, refresh the smallest dependency closure that can make the claim
current; do not rerun unrelated proof merely because it shares a repository.

Generated hubs and ID, relation, or term indexes are thin non-authoritative
views. Regenerate only the affected closure, retain stable links to canonical
owners, and report staleness rather than treating a generated view as truth.

## Cross-Change handoff

Handoff between Changes names stable artifact IDs, exact commits or versions,
applicable Contracts, evidence locations, currentness, and reopen triggers. A
summary without those anchors is context, not authoritative delivery evidence.
