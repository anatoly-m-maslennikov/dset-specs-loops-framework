+++
schema_version = "1.0"
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-029"
priority = "critical"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
context = ["repository=anatoly-m-maslennikov/dset-specs-loops-framework", "environment=isolated-host-fixtures", "python=3.14.6"]
observed_at = "2026-07-21T01:55:03+04:00"
evidence_location = "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/proofs/DSET-EVIDENCE-RECORD-029-installed-skill-integrity.md"
polarity = "supports"
currentness = "current"
reopen_when = "Wrapper rendering, installation manifests, runtime payloads, receipt verification, or the subject revision changes."

[subject]
id = "DSET-TEST-SKILL-015"
revision = "b7d79ec08c9a446f8a5358ac44c4c26bf7486d42"
intended_use = "Support the bounded claim that installed wrapper and runtime mutation is detected against source-bound expected identities."

[producer]
identity = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
performed_work = "Ran isolated installation, rendered-wrapper, runtime-payload, manifest, receipt, mutation, and full repository regressions."

[method]
description = "Install into isolated host layouts, verify sealed source/render identities, mutate each protected surface, and require deterministic rejection."
setup = "Python 3.14.6; local macOS execution with isolated cross-host filesystem fixtures."

[[relations]]
type = "evidence_for"
target = "DSET-TEST-SKILL-015"
+++

# Test result — Installed skill integrity

Expected wrapper-tree and shared-runtime identities are sealed into the
installation result. Added, removed, changed, or substituted installed files,
manifests, and receipts are rejected. The complete 310-Test suite passed.

This deterministic record does not claim real Codex or Claude host invocation;
that external proof remains open.
