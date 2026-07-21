+++
schema_version = "1.0"
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-033"
priority = "critical"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
context = ["repository=anatoly-m-maslennikov/dset-specs-loops-framework", "environment=local-macos", "python=3.14", "dset_yaml_files=0", "dset_yaml_frontmatter=0"]
observed_at = "2026-07-21T04:13:20+04:00"
evidence_location = "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/proofs/DSET-EVIDENCE-RECORD-033-complete-toml-cutover.md"
polarity = "supports"
currentness = "current"
reopen_when = "A DSET-owned YAML carrier or YAML frontmatter is added, a migrated carrier/reference/generated view changes, the migration implementation changes, or the subject revision changes."

[subject]
id = "DSET-TEST-GOV-043"
revision = "483ea2af321505f40713a73a51b3b68f327ba7f3"
intended_use = "Support the bounded claim that all DSET-owned artifact carriers use TOML and the completed migration is idempotent and repository-valid."

[producer]
identity = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
performed_work = "Migrated ten standalone YAML snapshots and seventy-one Markdown YAML-frontmatter carriers, refreshed links/seals/generated outputs/bootstrap, and ran the complete deterministic repository gate."

[method]
description = "Counted DSET YAML paths/frontmatter, repeated migration preview and apply, checked compilation/traceability/health/diff hygiene, and ran canonical dset verify plus the 312-Test suite, Ruff formatting/lint, and strict mypy."
setup = "Commit 483ea2af321505f40713a73a51b3b68f327ba7f3; project .venv; local macOS; uv synchronization disabled against the existing locked environment; execution temp/cache state outside the governed repository."

[[relations]]
type = "evidence_for"
target = "DSET-TEST-GOV-043"
+++

# Test result — Complete TOML cutover

The repository contains zero `.yaml`/`.yml` files under `dset/` and zero DSET
Markdown YAML-frontmatter carriers. Ten standalone snapshots now use adjacent
`.legacy.toml` envelopes and seventy-one immutable Markdown records use TOML
frontmatter. A repeated migration preview reports zero blockers and zero
changes; the repeated apply is also a no-op.

All 312 Tests, Ruff formatting and lint, strict mypy, `dset check`, compilation,
traceability, project health, bootstrap regeneration, diff hygiene, and the
canonical aggregate `dset verify` gate pass. Externally prescribed GitHub and
host-skill YAML remains outside the DSET artifact-carrier claim.
