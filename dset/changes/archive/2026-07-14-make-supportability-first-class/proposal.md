# Proposal — Make supportability first-class

- **Change ID:** `make-supportability-first-class`
- **Target package:** `methodology`
- **Implementing branch:** `dev`
- **Implementing PR:** [anatoly-m-maslennikov/dset-specs-loops-framework#3](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/3)
- **Status:** archive candidate; incomplete until the pushed PR head and dated layout pass final audit

## Problem

The public name expands DSET through “Spec,” while production supportability is scattered across generic observability, secret-hygiene, and verification rules. A real incident cannot yet rely on one framework contract for moving from a production symptom through safe runtime evidence to the deployed version, DSET change, requirement, test/eval proof, and corrective work.

## Outcome

Rename the framework to **DSET Spec Loops: A Production Vibecoding Framework**, expand DSET as **Domain–Supportability–Evals–Tests**, and make supportability a risk-scaled obligation across every spec loop. A production-facing change must declare the minimum safe evidence needed to investigate and fix real failures without treating “log everything” as a design.

## Scope

- Public name, expansion, project ID, and repository slug.
- Supportability requirements across domain/spec, proof planning, implementation planning, code rules, and gates.
- Correlation and incident IDs; deployed version, PR, and DSET-change identity; structured logs, traces, metrics/events, diagnostics, and runbooks where applicable.
- Retention, redaction, access, sampling, cardinality, and cost boundaries.
- Incident-to-requirement/test/eval/fix traceability.
- Local-tool, service, and long-running-workflow profiles without a universal telemetry vendor.

## Non-goals

- Requiring distributed tracing for every local script.
- Treating logs, traces, or metrics as new business-state authorities.
- Persisting secrets, raw personal data, or unlimited diagnostic output.
- Adding a ninth standard change document.
- Archiving this change without a repository-qualified implementing PR.

## Risk

Medium governance and operational risk. Too little evidence blocks incident repair; indiscriminate telemetry leaks sensitive data, creates unbounded cost/cardinality, and obscures the signal operators need.
