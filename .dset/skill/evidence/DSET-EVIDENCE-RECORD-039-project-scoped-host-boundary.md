+++
schema_version = "1.0"
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-039"
priority = "critical"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
context = ["repository=anatoly-m-maslennikov/dset-specs-loops-framework", "environment=codex-desktop-macos", "codex-cli=0.144.5", "claude-code=2.1.205", "public-skills=17", "installation-scope=repository"]
observed_at = "2026-07-21T07:55:00+04:00"
evidence_location = "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/proofs/DSET-EVIDENCE-RECORD-039-project-scoped-host-boundary.md"
polarity = "mixed"
currentness = "current"
reopen_when = "A real Codex process can initialize writable host state, Claude Code can authenticate through an allowed API domain, the DSET distribution changes, or either pinned host version changes."

[subject]
id = "DSET-TEST-SKILL-018"
revision = "b09cd0fe2beb7e14326c0f8bcb3693c032afada0"
intended_use = "Bound repository-scoped installation and real-process invocation claims for the seventeen-skill distribution without treating deterministic discoverability as observed host load."

[producer]
identity = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
performed_work = "Installed and verified the exact distribution in temporary documented repository-scoped host locations, invoked fresh Codex and Claude processes against those locations, recorded their pre-inference boundaries, and removed the temporary copies."

[method]
description = "Applied DSET's transactional installer to explicit repository-scoped Codex and Claude skill roots with isolated shared-runtime roots, repeated verification, then explicitly requested dset-overview from each pinned real host executable without authorizing governed repository edits."
setup = "Codex Desktop managed workspace on macOS; repository virtual environment; Codex CLI 0.144.5; Claude Code 2.1.205."

[[relations]]
type = "evidence_for"
target = "DSET-TEST-SKILL-018"
+++

# Test result — Project-scoped host boundary

Transactional repository-scoped installation and verification completed with
exit status zero for both hosts. Each installed exactly 17 copied wrappers,
reported every wrapper as discoverable with a valid invocation contract, and
verified a current copied shared-runtime manifest and portable launcher. The
temporary Codex, Claude, and runtime copies were removed after the attempts.

A fresh Codex CLI process then stopped before inference because the desktop
app's state database was read-only to the child process and the in-process app
server could not initialize. A fresh Claude Code process returned a host
session ID but stopped before inference with `403 Domain not in allowlist`.
Neither process consumed the installed skill, resolved local rules, invoked
the shared runtime, performed a handoff, or observed the stop boundary.

This evidence promotes repository-scoped transactional install and
verification only. It does not promote global installation, actual host
discovery or load, invocation, handoff, stop, or an authenticated independent
review. `DSET-TASK-SKILL-020` and `DSET-TASK-GOV-044` remain open.
