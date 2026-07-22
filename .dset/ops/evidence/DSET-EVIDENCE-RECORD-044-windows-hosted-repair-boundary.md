+++
schema_version = "1.0"
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-044"
priority = "critical"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
context = ["candidate_commit=92fd2a8df05ff37eecc3c45a0143466b36ba1be9", "remote_commit=0ed3ccb8a0dcef377a5870d0f3d14fddb158fac6", "platform=macos", "python=3.14.6", "tests=321", "push_run=29848351686", "pull_request_run=29848356251"]
observed_at = "2026-07-21T20:48:14+04:00"
evidence_location = "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/proofs/DSET-EVIDENCE-RECORD-044-windows-hosted-repair-boundary.md"
polarity = "inconclusive"
currentness = "current"
reopen_when = "The repaired candidate is published and receives a completed hosted matrix, or its path/newline policy, migration byte handling, fixture policy, or configured verification commands change."

[subject]
id = "DSET-TEST-OPS-021"
revision = "92fd2a8df05ff37eecc3c45a0143466b36ba1be9"
intended_use = "Bind the locally passing Windows repair candidate and the failing hosted predecessor without claiming exact-head hosted success."

[producer]
identity = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
performed_work = "Inspected both GitHub Actions matrices for remote commit 0ed3ccb, extracted the two remaining native-Windows errors, repaired host-neutral work-area validation and byte-exact preserved-package planning, added deterministic regressions, and ran the complete local verifier at candidate 92fd2a8."

[method]
description = "Compared push run 29848351686 and pull-request run 29848356251 for the exact remote SHA, then ran focused bootstrap/migration regressions and the configured canonical verifier on the repaired local candidate."
setup = "GitHub-hosted Ubuntu, macOS, and native Windows for the remote predecessor; Codex Desktop managed workspace on macOS for the unpushed repair candidate."

[[relations]]
type = "evidence_for"
target = "DSET-TEST-OPS-021"
+++

# Test result — Windows hosted repair boundary

Remote commit `0ed3ccb8a0dcef377a5870d0f3d14fddb158fac6` was evaluated by
both GitHub Actions entry paths:

- push run [`29848351686`](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29848351686): Ubuntu and macOS passed; native Windows failed;
- pull-request run [`29848356251`](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29848356251): Ubuntu and macOS passed; native Windows failed.

Both Windows jobs completed all 320 Tests and exposed two remaining
platform-boundary errors: POSIX `/absolute` work-area text was interpreted
through host-native `Path`, and preserved-package planning normalized CRLF
before comparing its digest with raw bytes.

Local candidate `92fd2a8df05ff37eecc3c45a0143466b36ba1be9` contains both
repairs, an explicit Windows-semantics regression, and correct implementation
provenance. The complete configured verifier passes locally with 321 Tests,
Ruff format/lint, strict mypy, recursive validation, fresh compilation,
traceability and health views, and diff hygiene.

The candidate is four commits ahead of `origin/dev` and has no hosted run.
Therefore this evidence is intentionally inconclusive for cross-platform
closure: it supports the local repair but does not establish that Ubuntu,
macOS, and native Windows are green on the repaired SHA.

`DSET-PROBLEM-OPS-001` remains open. It may be resolved only after a published
commit containing the repair completes all three hosted jobs successfully.
