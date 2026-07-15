# Methodology delta specification — Supportability

> Archive candidate in [PR #3](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/3); accepted truth is reconciled under `dset/specs/packages/methodology/`.

## MODIFIED — METH-REQ-001 One governed spec-loop pipeline

The methodology must define one five-stage spec-loop pipeline while treating supportability as a cross-cutting production obligation from domain/spec through verification and repair. “Spec” names the governing loop artifact; “Supportability” is the `S` in DSET.

**Scenario DSET-SCENARIO-META-002:** A contributor can distinguish the DSET expansion from the spec-loop artifact without dropping specifications or treating supportability as an optional post-release add-on.

## ADDED — DSET-REQUIREMENT-META-002 Public identity is exact

The public display name must be **DSET Spec Loops**, the subtitle must be **A Production Vibecoding Framework**, DSET must expand to **Domain–Supportability–Evals–Tests**, and the project/repository ID must be `dset-specs-loops-framework`.

**Scenario DSET-SCENARIO-META-003:** Active public metadata contains the new identity and no active, non-historical document claims that DSET expands through “Spec.”

## ADDED — DSET-REQUIREMENT-OPS-002 Production changes declare a supportability contract

Every production-facing spec must state the operator questions it must answer, applicable signals, correlation/incident identity, deployed-version/change identity, diagnostic and runbook surface, data classification, redaction, retention, access, sampling/cardinality, and cost boundaries. A non-production or transient local tool may mark items not applicable with a reason.

**Scenario DSET-SCENARIO-OPS-002:** A service incident can be investigated from its public failure or correlation ID without first adding ad hoc logging in production.

## ADDED — DSET-REQUIREMENT-OPS-003 Runtime evidence is traceable to corrective intent

Applicable runtime evidence must identify the deployed version and allow an investigator to traverse incident → runtime evidence → version/commit → PR → DSET change → requirement → deterministic test or qualitative eval → repair evidence.

**Scenario DSET-SCENARIO-OPS-003:** Given one reported production incident ID, an operator can identify the owning version and change and locate the proof that should reproduce or prevent recurrence.

## ADDED — DSET-REQUIREMENT-OPS-004 Telemetry is safe and bounded

Logs, traces, metrics, events, diagnostic bundles, and prompts must exclude secrets and unnecessary sensitive data; declare retention and access; bound metric cardinality, sampling, and diagnostic volume; and keep business state authoritative in its declared store.

**Scenario DSET-SCENARIO-OPS-004:** A support bundle is useful for diagnosis but contains no credentials, raw tokens, or unapproved personal data and cannot grow without a declared bound.

## ADDED — DSET-REQUIREMENT-OPS-005 Supportability is profile- and topology-scaled

Local tools may use structured local files and a reproducible diagnostic bundle; services may use centralized logs/metrics/traces; long-running or distributed workflows must preserve cross-boundary correlation and effect evidence. Mechanisms apply only where runtime risk and deployment topology require them.

**Scenario DSET-SCENARIO-OPS-005:** A one-shot local transform does not inherit distributed tracing, while an asynchronous multi-service workflow preserves correlation across retry and effect boundaries.

## ADDED — DSET-REQUIREMENT-OPS-006 Support proof keeps tests and evals separate

Deterministic telemetry schemas, redaction, correlation propagation, retention configuration, and diagnostic commands belong to test plans. Whether an unfamiliar operator can diagnose representative incidents with the evidence belongs to eval plans.

**Scenario DSET-SCENARIO-OPS-006:** An automated redaction assertion remains a test, while a timed incident-investigation exercise with a rubric remains an eval.
