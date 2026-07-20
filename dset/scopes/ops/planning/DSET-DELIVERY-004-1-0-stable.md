+++
artifact_type = "delivery"
artifact_subtype = "version_scope"
artifact_id = "DSET-DELIVERY-004"
version_line = "1.0"
status = "planned"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Version Scope — DSET 1.0 stable

## Promise

Publish a fully working stable DSET framework whose public behavior,
distribution, migration, supportability, and compatibility claims are complete
and proven through the RC/final gate.

## Included outcomes and capabilities

- The complete adopter-ready framework surface accepted before RC entry.
- Evidence-complete self-hosting, required adopters/pilots, supported hosts and
  platforms, recovery paths, and public distribution.
- Stable public contracts and documented compatibility/migration policy.

## Exclusions

- New feature scope after RC entry.
- Time-based, version-count-based, or partially complete promotion.

## Exit criteria

- A fully working `1.0.0-rc.N` satisfies every required deterministic Test,
  applicable Evaluation, pilot, distribution, supportability, and migration
  gate with no release-blocking defect.
- Final promotion contains no substantive behavior or scope change and has a
  fresh explicit ready disposition for the exact candidate.
- One immutable Release Record binds the published `1.0.0` identity.

## Governing provenance

Compiled from `DSET-DECISION-OPS-006` and the accepted RC/final release rules.
