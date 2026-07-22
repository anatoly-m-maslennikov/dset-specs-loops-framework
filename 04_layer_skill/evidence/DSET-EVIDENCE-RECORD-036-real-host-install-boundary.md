+++
schema_version = "1.0"
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-036"
priority = "critical"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
context = ["repository=anatoly-m-maslennikov/dset-specs-loops-framework", "environment=codex-desktop-macos", "codex-cli=0.144.5", "claude-code=2.1.205", "public-skills=17"]
observed_at = "2026-07-21T06:30:00+04:00"
evidence_location = "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/proofs/DSET-EVIDENCE-RECORD-036-real-host-install-boundary.md"
polarity = "mixed"
currentness = "current"
reopen_when = "A host process can write its supported global skill and runtime roots, the DSET distribution changes, or the Codex/Claude host versions change."

[subject]
id = "DSET-TEST-SKILL-018"
revision = "3dbd3c42bfa9003718bf415322407241a1cb6ec2"
intended_use = "Bound the current real-host installation claim for the seventeen-skill DSET distribution without promoting discovery or invocation evidence that was not observed."

[producer]
identity = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
performed_work = "Previewed exact Codex and Claude host transactions, identified host versions and destinations, then attempted the default and alternate Codex installs plus the default Claude install under the app's approved escalation boundary."

[method]
description = "Rendered the exact 17-wrapper and shared-runtime manifests from the subject revision, checked that all destinations were absent, and invoked transactional apply for each real host location without bypassing installer collision or integrity guards."
setup = "Codex Desktop managed workspace on macOS; repository virtual environment; Codex CLI 0.144.5; Claude Code 2.1.205."

[[relations]]
type = "evidence_for"
target = "DSET-TEST-SKILL-018"
+++

# Test result — Real host installation boundary

Both previews passed at the exact subject revision. Codex planned all 17
wrappers under `~/.agents/skills` and one shared runtime under
`~/.codex/packages/dset`. Claude planned all 17 wrappers under
`~/.claude/skills` and one shared runtime under `~/.claude/packages/dset`.
Every planned destination was absent, and the manifests included
`dset-overview`.

Transactional apply was attempted for the default Codex locations, the
alternate personal Codex skill root `~/.codex/skills`, and the default Claude
locations. The app process received `Operation not permitted` while creating
each destination's transaction staging directory. No destination was created,
no partial rollback was required, and no installation, discovery, load,
invocation, handoff, or stop receipt is promoted.

This supports source completeness, deterministic host layout, and safe
fail-before-write behavior for the 17-skill distribution. It contradicts any
claim that real global installation or host invocation has completed in this
environment. `DSET-TASK-SKILL-020` therefore remains open.
