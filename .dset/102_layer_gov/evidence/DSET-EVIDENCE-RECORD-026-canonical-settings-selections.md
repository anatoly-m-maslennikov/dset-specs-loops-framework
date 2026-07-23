+++
schema_version = "1.0"
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-026"
priority = "high"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
context = ["repository=anatoly-m-maslennikov/dset-specs-loops-framework", "environment=local-macos", "python=3.14.6"]
observed_at = "2026-07-21T01:55:00+04:00"
evidence_location = "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/proofs/DSET-EVIDENCE-RECORD-026-canonical-settings-selections.md"
polarity = "supports"
currentness = "current"
reopen_when = "The settings schema, defaults, reader precedence, bootstrap writer, selected workflow behavior, or subject revision changes."

[subject]
id = "DSET-TEST-PLAN-GOV-039"
revision = "b7d79ec08c9a446f8a5358ac44c4c26bf7486d42"
intended_use = "Support the bounded claim that canonical settings select naming, creation strictness, and implementation preparation without a legacy write path."

[producer]
identity = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
performed_work = "Ran the complete repository suite and static gates after applying the canonical TOML cutover."

[method]
description = "Execute the settings, bootstrap, migration, and full self-host regression paths, then repeat the migration in preview and apply modes."
setup = "Python 3.14.6; Ruff 0.15.21; mypy 2.3.0; local macOS repository checkout on branch dev."

[[relations]]
type = "evidence_for"
target = "DSET-TEST-PLAN-GOV-039"
+++

# Test result — Canonical settings selections

The complete suite passed: 310 Tests in 114.795 seconds. Ruff format and lint,
strict mypy, DSET compilation, traceability, health, recursive validation, and
diff hygiene passed. A second TOML preview and apply both reported
`changes=0` and `references=0`.

This record does not satisfy the separate qualitative settings Evaluation or
hosted operating-system proof.
