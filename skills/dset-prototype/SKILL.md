---
name: dset-prototype
description: Run a bounded disposable experiment to answer a specific design, framework, library, protocol, performance, recovery, or integration question with comparable evidence. Use when uncertainty blocks a DSET Solution Landscape or ADR decision and production-quality implementation would be premature; never use the prototype as an unreviewed path into production.
---

# DSET Prototype

Answer one decision question with disposable evidence. Keep prototype code outside production surfaces until a later accepted design deliberately reimplements or promotes it.

## Workflow

1. Read the governing requirements, test plan, applicable eval plan, solution landscape, constraints, and candidate versions. Refuse a prototype whose question or acceptance threshold is undefined.
2. State one falsifiable hypothesis, time/effort bound, representative scenarios, hard constraints, success/failure thresholds, and disposal rule.
3. Create evidence only under `dset/changes/<change-id>/proofs/<candidate>-fit/`. Record the exact source, version/commit, license, setup, data class, and external access. Update third-party notices before copying or substantially adapting material.
4. Exercise the same accepted test and eval thresholds used for alternatives: happy path, boundary, failure, retry/recovery, concurrency, upgrade/migration, diagnostics, and exit behavior as applicable.
5. Record observed evidence separately from vendor claims. Measure uncovered requirements, adapter/policy glue, persistence, migrations, operational burden, security/privacy, lock-in, maintenance, and replacement cost.
6. Conclude adopt, adapt, build, or defer. Link evidence from `solution-landscape.md`; create or update an ADR for a material decision.
7. Delete or clearly quarantine disposable runtime artifacts. Run `dset check` and retain only bounded reproducible evidence needed for the decision.

## Output contract

Produce a small proof directory containing setup, cases, results, and disposal status; update the comparison matrix and ADR link. Do not modify accepted package truth or production code directly from prototype evidence.

## Stop conditions

Stop when licensing, security, data residency, platform, or architecture violates a hard constraint; when the timebox expires; or when evidence is insufficient. Do not weaken thresholds for a preferred candidate. Promotion requires an accepted ADR/design and normal implementation/test/eval plan.
