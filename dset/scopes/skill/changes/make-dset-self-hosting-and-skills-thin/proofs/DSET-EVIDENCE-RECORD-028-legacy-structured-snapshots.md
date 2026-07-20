+++
schema_version = "1.0"
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-028"
priority = "critical"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
context = ["repository=anatoly-m-maslennikov/dset-specs-loops-framework", "environment=local-macos", "python=3.14.6"]
observed_at = "2026-07-21T01:55:02+04:00"
evidence_location = "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/proofs/DSET-EVIDENCE-RECORD-028-legacy-structured-snapshots.md"
polarity = "supports"
currentness = "current"
reopen_when = "A registered legacy snapshot, current TOML owner, retained historical link, classification entry, migration rule, or subject revision changes."

[subject]
id = "DSET-TEST-GOV-041"
revision = "b7d79ec08c9a446f8a5358ac44c4c26bf7486d42"
intended_use = "Support the bounded claim that exactly registered YAML snapshots remain byte-stable while current readers and writers use TOML only."

[producer]
identity = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
performed_work = "Ran digest, link-retention, classification, reader-precedence, migration, rollback, and idempotency tests over the real repository cutover."

[method]
description = "Validate every registered snapshot against its whole-file digest and current owner, then exercise drift, missing-owner, dual-owner, fallback, and repeat-run stops."
setup = "Python 3.14.6; local macOS repository checkout on branch dev; ten registered historical YAML snapshots."

[[relations]]
type = "evidence_for"
target = "DSET-TEST-GOV-041"
+++

# Test result — Legacy structured snapshots

Ten YAML files remain as exact registered historical snapshots. Current
DSET-owned mutable structured artifacts and new Markdown frontmatter use TOML;
JSON Schema remains JSON as an external contract. The complete 310-Test suite
passed, and repeat preview/apply runs planned no writes.

The 71 immutable Markdown atoms and promoted proof records with historical YAML
frontmatter remain byte-stable by design; they are not competing current
writers.
