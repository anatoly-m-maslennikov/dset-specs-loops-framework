---
artifact_type: "evidence_record"
artifact_subtype: "test_result"
artifact_id: "DSET-EVIDENCE-RECORD-035"
scope_path:
  - "layer:gov"
priority: "high"
schema_version: "1.0"
context:
  - "repository=anatoly-m-maslennikov/dset-specs-loops-framework"
  - "environment=local-macos"
  - "python=3.14"
  - "artifact_type=version"
  - "version_subtypes=6"
  - "active_version_ids=7"
observed_at: "2026-07-21T05:50:23+04:00"
polarity: "supports"
currentness: "current"
reopen_when: "Artifact classification, Version lifecycle authority, registries, templates, active Version carriers or IDs, settings examples, release/runtime behavior, projection scopes, generated views, or the subject revision changes."
subject:
  id: "DSET-TEST-PLAN-GOV-044"
  revision: "86cad6406c56124813d6208dd546efe2e3a731a4"
  intended_use: "Support the bounded claim that Version is the only current release-lifecycle artifact Type and its six flat subtypes work consistently across authority and implementation."
producer:
  identity: "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
  performed_work: "Sealed sibling GOV and OPS Decisions plus Test and Evaluation definitions, absorbed predecessor authority and QA, migrated current artifact classification and IDs, corrected projection scope, and ran deterministic gates."
method:
  description: "Validated exact current registry/templates/carriers, ran focused artifact-type, health, release, semantic-atom, compilation, governance, and traceability tests, then ran Ruff formatting and lint, strict mypy, canonical DSET validation, diff hygiene, and all 312 Tests."
  setup: "Commit 86cad6406c56124813d6208dd546efe2e3a731a4; project .venv; local macOS. The complete suite used the normal macOS temporary directory because sandbox-denied system temp access otherwise caused post-assertion repository-local cleanup races."
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "evidence_for"
    targets:
      - "DSET-TEST-PLAN-GOV-044"
---

# Test result — Version artifact Type

The current artifact registry contains exactly eleven primary artifact Types,
including `version` and excluding `delivery`. Version owns exactly six direct
subtypes: Roadmap, Version Scope, Change, Release Plan, Readiness Record, and
Release Record. Current templates, settings examples, release behavior, and
the seven self-hosted lifecycle carriers use `VERSION` identities.

The migration preserves the former Decision/Test/Evaluation atoms through
append-only absorption and maintains separate project- and GOV-layer projection
frontiers. The exact subject revision passes the focused 89-test migration
matrix, traceability regression tests, Ruff formatting and lint, strict mypy,
canonical DSET validation, diff hygiene, and all 312 repository Tests.

`DSET-EVAL-PLAN-GOV-029` remains pending because reader interpretation is a
qualitative claim, not a deterministic Test result.
