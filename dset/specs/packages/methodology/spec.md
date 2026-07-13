# Methodology specification

## METH-REQ-001 — One governed pipeline

The methodology must define one five-stage pipeline: spec; test plan plus eval plan; implementation plan; code under general rules; and executable enforcement.

**Scenario METH-SCN-001:** Given a contributor deciding where a rule belongs, the document map identifies exactly one owning stage document and treats cross-links as pointers rather than duplicate ownership.

## METH-REQ-002 — Tests and evals remain distinct

The methodology must keep deterministic tests in `test-plan.md` and probabilistic or qualitative evaluation in `eval-plan.md`.

**Scenario METH-SCN-002:** Given behavior with one exact expected output, it is routed to the test plan even when the check is automated. Given multiple acceptable outputs judged by criteria or a rubric, it is routed to the eval plan.

## METH-REQ-003 — Runtime rules are selected by independent concerns

The methodology must select recovery semantics by runtime risk and durable backing by topology, write volume, and concurrency. Event sourcing, reconciliation, durable execution, and observed-progress liveness apply only when their specific semantics are required.

**Scenario METH-SCN-003:** A stateless CRUD service keeps durable state in its database without adding an application file WAL or event store unless audit/replay requirements independently demand one.

**Scenario METH-SCN-004:** A modest-write local resumable tool keeps accepted state in declared files with one writer and atomic/durable writes; a higher-volume or concurrent local tool selects a database instead of two writable authorities.

## METH-REQ-004 — Delivery semantics are bounded

The methodology must describe retries as at-least-once delivery plus receiving-side deduplication or idempotency. It may claim effectively-once effects only inside the declared key, retention, and atomicity boundary.

**Scenario METH-SCN-005:** A retryable receiver documents its deduplication key, retention window, owner, and atomic check/write operation without claiming universal exactly-once execution.

## METH-REQ-005 — Enforcement is language-neutral and profile-applied

The methodology must define six neutral gate categories and keep concrete tools, source scopes, thresholds, exclusions, and ratchets in versioned applied profiles.

**Scenario METH-SCN-006:** A Python project selects Python v1; a JavaScript/TypeScript project does not inherit Python line limits or tools.

## METH-REQ-006 — Change history is PR-traceable without a future SHA

The methodology must use a repository-qualified PR identity as the stable implementation link, archive inside that PR after fresh verification and current-truth reconciliation, and keep the PR draft until applicable traceability and archive-readiness checks pass. Missing PR identity keeps a change active; any later implementation or specification change invalidates prior readiness.

**Scenario METH-SCN-007:** The archived change links to the PR that owns the code diff and eventual merge result without attempting to store a merge SHA before it exists.

**Scenario METH-SCN-012:** A change with a pending PR identity cannot be archived, and a later implementation or specification edit requires verification and archive readiness to be refreshed.

## METH-REQ-007 — Public Markdown is portable

Public methodology must use ordinary Markdown links and GitHub-native alerts or collapsed details sections.

**Scenario METH-SCN-008:** A GitHub reader can navigate every local link and expand every collapsed section without an Obsidian renderer.

## METH-REQ-008 — Project truth uses a visible root

Committed project truth must live under the visible `dset/` root. Hidden `.dset/` is reserved for generated, local, cached, or other machine-owned state.

**Scenario METH-SCN-009:** `dset/README.md` exposes accepted truth, active changes, archive history, templates, and schemas, while no committed project truth is owned by `.dset/`.

## METH-REQ-009 — Package structure is proportional

The project manifest must register each package exactly once and must omit or null the global-truth root until cross-package ownership exists.

**Scenario METH-SCN-010:** A one-package project resolves `methodology` to `specs/packages/methodology` and reports `global_truth_root: null`.

## METH-REQ-010 — Standard changes expose complete proof structure

A standard change must contain exactly eight top-level document artifacts—proposal, test plan, eval plan, solution landscape, design, implementation plan, tasks, and verification—plus separate `specs/` and `proofs/` directories.

**Scenario METH-SCN-011:** Structural inspection counts the eight documents separately from the requirement-delta and evidence directories.

## METH-REQ-011 — Enforcement status is honest

Public metadata must name the selected enforcement profile and canonical command and must use explicit pending values until the corresponding executable assets exist.

**Scenario METH-SCN-013:** `documentation-v1-pending` and `canonical_command: pending` cannot be presented as an active executable gate.
