+++
schema_version = "1.0"
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-027"
priority = "critical"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
context = ["repository=anatoly-m-maslennikov/dset-specs-loops-framework", "environment=local-macos", "python=3.14.6"]
observed_at = "2026-07-21T01:55:01+04:00"
evidence_location = "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/proofs/DSET-EVIDENCE-RECORD-027-native-package-successors.md"
polarity = "supports"
currentness = "current"
reopen_when = "A package registry, selector seal, package reader, migration transaction, or subject revision changes."

[subject]
id = "DSET-TEST-GOV-040"
revision = "b7d79ec08c9a446f8a5358ac44c4c26bf7486d42"
intended_use = "Support the bounded claim that each shared package has one native TOML current owner while selector-sealed YAML remains byte-stable history."

[producer]
identity = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
performed_work = "Ran package-reader, legacy-authority, migration, governance, self-host, and complete repository tests after the cutover."

[method]
description = "Compare registered legacy digests, native successor parsing and precedence, transaction rollback behavior, and second-run idempotency."
setup = "Python 3.14.6; local macOS repository checkout on branch dev; exact committed migration input and output carriers."

[[relations]]
type = "evidence_for"
target = "DSET-TEST-GOV-040"
+++

# Test result — Native package successors

All five shared packages retain their registered historical YAML carriers and
have one current `package.toml` successor. The complete 310-Test suite passed,
and repeat preview/apply runs were no-ops with zero planned writes or reference
updates.

This record proves repository behavior, not semantic equivalence beyond the
registered values or hosted release readiness.
