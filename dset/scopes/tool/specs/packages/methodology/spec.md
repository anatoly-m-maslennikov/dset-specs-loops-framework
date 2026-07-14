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
