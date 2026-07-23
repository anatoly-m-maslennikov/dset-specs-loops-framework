+++
schema_version = "1.0"
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-034"
priority = "high"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
context = ["repository=anatoly-m-maslennikov/dset-specs-loops-framework", "environment=local-macos", "python=3.14", "generated_schema=1.2", "workspace_modes=integration-branch,branch-worktree"]
observed_at = "2026-07-21T05:11:11+04:00"
evidence_location = "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/proofs/DSET-EVIDENCE-RECORD-034-current-generated-adopter.md"
polarity = "supports"
currentness = "current"
reopen_when = "Bootstrap inputs, schema 1.2 layout or Work Area rules, release branch configuration, Change workspace selection, generated-adopter validation, or the subject revision changes."

[subject]
id = "DSET-TEST-PLAN-META-011"
revision = "347df79ba1d1310476ff587e55489b8d723576dd"
intended_use = "Support the bounded claim that a newly generated schema 1.2 adopter validates Work Areas and both configured Change workspace modes."

[producer]
identity = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
performed_work = "Added explicit release branches to generated adopters, exercised integration-branch and optional branch-worktree Change creation, refreshed derived outputs, and ran deterministic repository gates."

[method]
description = "Initialized a nonempty temporary adopter from the current bundle, asserted schema 1.2 and Work Area ownership, created and validated Changes in both workspace modes, ran focused bootstrap/self-host checks, then ran Ruff formatting and lint, strict mypy, and all 312 Tests."
setup = "Commit 347df79ba1d1310476ff587e55489b8d723576dd; project .venv; local macOS; temporary adopters outside the governed repository."

[[relations]]
type = "evidence_for"
target = "DSET-TEST-PLAN-META-011"

[[relations]]
type = "evidence_for"
target = "DSET-TEST-PLAN-OPS-005"
+++

# Test result — Current generated adopter

A newly generated adopter now owns schema `1.2`, declared Work Areas, and
explicit `dev` integration and `main` protected branches. Its default Change
uses the integration branch; its optional isolated Change uses a
`dset/<slug>` worktree branch based on `dev`. Both states pass repository
validation.

The exact subject revision passes Ruff formatting and lint, strict mypy, the
focused bootstrap, CLI, and self-host tests, and all 312 repository Tests. One
prior complete run encountered a post-assertion temporary-directory cleanup
race; the isolated test and the immediately repeated complete suite passed.
