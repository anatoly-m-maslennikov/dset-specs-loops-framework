# Deterministic supportability checks — 2026-07-14

- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

> Baseline evidence carried into the dated archive candidate for [PR #3](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/3).

## Scope

Checks ran on `dev` after the identity, methodology, accepted-truth, and synthetic-fixture commits. The repository still declares `documentation-v1-pending`, so these are explicit ad hoc checks rather than a claim that the canonical validator exists.

## Results

| Test | Result | Evidence |
|---|---|---|
| DSET-TEST-META-002 identity | Pass | README title is `DSET Spec Loops: A Production Vibecoding Framework`; expansion is `Domain–Supportability–Evals–Tests`; `dset/dset.yaml` uses project ID and repository slug `dset-specs-loops-framework`; origin uses the personal-account SSH alias and renamed slug; active truth contains no stale old slug or old expansion outside historical/problem context |
| DSET-TEST-OPS-002 contract fields | Pass | Methodology 01 specifies incident objectives, signals, correlation/deploy identity, safe diagnostics, governance/bounds, runbooks, and incident traceability; documents 02–05 assign proof, implementation, runtime, and supplemental-gate ownership |
| DSET-TEST-OPS-003 incident chain | Pass | Each case in [synthetic-incidents.md](synthetic-incidents.md) traverses incident/run identity → runtime/build identity → commit → repository-qualified synthetic PR → DSET change → requirement → test/eval → repair |
| DSET-TEST-OPS-004 safe bounded evidence | Pass | Public contract and fixtures exclude secrets/unnecessary personal data, require read-only diagnostics and redaction/access/retention/deletion controls, bound volume/cardinality/sampling, and keep telemetry derived from business authorities |
| DSET-TEST-OPS-005 proportional mechanisms | Pass | Profile A/local, Profile B stateful/retryable, and Profile C high-risk rules differ; local fixture SYN-INC-003 explicitly avoids centralized tracing while asynchronous SYN-INC-002 carries cross-boundary correlation |
| DSET-TEST-OPS-006 proof separation | Pass | Schema, identity, propagation, permission, redaction, retention, and bounds checks remain deterministic tests; independent operator diagnosis and LLM response quality remain evals |
| DSET-TEST-GOV-005 structure | Pass | 45 Markdown files inspected, 126 local links resolved, 29 `<details>` blocks balanced, code fences balanced, YAML parsed, no wiki links, no unsupported GitHub alerts, and `git diff --check` passed |

## Commands and observations

```text
node /tmp/check_dset_markdown.mjs
PASS: 45 Markdown files, 126 local links, 29 details blocks

yq -e '<identity, supportability disposition, and manifest assertions>' dset/dset.yaml
true

git diff --check
exit 0

gh repo view anatoly-m-maslennikov/dset-specs-loops-framework --json nameWithOwner,description,url,defaultBranchRef
nameWithOwner: anatoly-m-maslennikov/dset-specs-loops-framework
description: DSET Spec Loops: A Production Vibecoding Framework
default branch: main

git ls-remote origin refs/heads/dev
545be8970b447f3c20da51c739bd63b20f0ef888 refs/heads/dev
```

The Markdown checker was an ad hoc read-only script outside the repository. A repository-owned validator remains pending and is not implied by this evidence.
