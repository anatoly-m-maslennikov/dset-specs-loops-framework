+++
schema_version = "1.0"
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-038"
priority = "high"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
context = ["repository=anatoly-m-maslennikov/dset-specs-loops-framework", "environment=local-macos", "python=3.14", "public-skills=17", "governed-wrappers=15", "pre-resolution-exceptions=2", "tests=312"]
observed_at = "2026-07-21T07:30:00+04:00"
evidence_location = "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/proofs/DSET-EVIDENCE-RECORD-038-overview-skill.md"
polarity = "supports"
currentness = "current"
reopen_when = "The public skill catalog, Overview workflow or stop boundary, project-health renderer, runtime/session schema, bootstrap bundle, distribution payload, or subject revision changes."

[subject]
id = "DSET-TEST-PLAN-SKILL-018"
revision = "74f4c90d82b5fc76a9c292d4ff41ec88626e42bd"
intended_use = "Support the bounded claim that DSET exposes one read-only Overview skill alongside an unchanged sixteen-entry lifecycle topology and distributes all seventeen packages consistently."

[producer]
identity = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
performed_work = "Created and validated the thin wrapper, registered its supplemental workflow and runtime mode, updated current authority and schemas, regenerated the bootstrap bundle and health view, and exercised source, adopter, distribution, runtime, and fixed-point behavior."

[method]
description = "Ran the official Skill Creator validator, focused wrapper/lifecycle/runtime/bootstrap cases, all 312 repository Tests, Ruff formatting and lint, strict mypy, canonical DSET validation, and diff hygiene."
setup = "Commit 74f4c90d82b5fc76a9c292d4ff41ec88626e42bd; project .venv; local macOS; TMPDIR=/tmp for the complete suite."

[[relations]]
type = "evidence_for"
target = "DSET-TEST-PLAN-SKILL-018"
+++

# Test result — Read-only Overview skill

The canonical catalog contains exactly 17 public packages: the existing
sixteen-entry lifecycle surface plus `dset-overview`. Fifteen governed wrappers
resolve project-local workflows; initialization and governance repair remain
the only pre-resolution exceptions. The lifecycle still contains exactly 15
modes, and Overview is not one of them.

`dset-overview` resolves the supplemental `overview` workflow through the
shared runtime and local governance, reports generated-health identity,
artifact/scope counts, coverage, freshness, and open obligations, and stops
before refreshing stale state or performing a recommended handoff. Codex and
Claude previews include all 17 wrappers and one host-local shared runtime.

The exact subject revision passed the official package-shape validator, focused
integration gates, all 312 Tests in 165.210 seconds, Ruff format/lint, strict
mypy, canonical DSET validation, and `git diff --check`. Real global host
installation and invocation remain separately open under evidence record 036.
