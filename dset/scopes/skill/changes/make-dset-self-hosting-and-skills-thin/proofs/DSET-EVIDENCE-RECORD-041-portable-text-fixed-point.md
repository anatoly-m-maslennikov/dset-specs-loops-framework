+++
schema_version = "1.0"
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-041"
priority = "critical"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
context = ["commit=a473c29073a9660b35f2a7f78d3d715609b063fe", "platform=macos", "python=3.14.6", "github_actions_failure_run=29799045908", "tests=314"]
observed_at = "2026-07-21T16:45:37+04:00"
evidence_location = "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/proofs/DSET-EVIDENCE-RECORD-041-portable-text-fixed-point.md"
polarity = "supports"
currentness = "current"
reopen_when = "The repository text-attribute policy, carrier hashing, commit-relation path filter, bootstrap template/bundle, or covered validation commands change; hosted platform proof remains independently open."

[subject]
id = "DSET-TEST-OPS-017"
revision = "a473c29073a9660b35f2a7f78d3d715609b063fe"
intended_use = "Prove the local portable-text repair and the generated-view fixed point without claiming fresh hosted Windows or WSL execution."

[producer]
identity = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
performed_work = "Reproduced the hosted failure boundary, added the LF checkout contract and regression Test, removed generated-only commits from derived implementation relations, rebuilt the bootstrap bundle, and ran the complete local deterministic suite."

[method]
description = "Compared GitHub Actions run 29799045908 across Linux, macOS, and native Windows; enforced repository-owned LF text bytes; exercised a temporary Git history containing substantive, generated-only, and mixed commits; then ran all configured deterministic commands directly from the locked environment plus DSET freshness checks."
setup = "macOS Codex workspace; existing locked .venv; direct .venv executables used because the sandbox denied uv's user cache and network tunnel."

[[relations]]
type = "evidence_for"
target = "DSET-TEST-OPS-017"
+++

# Test result — Portable text and generated-view fixed point

At commit `a473c29073a9660b35f2a7f78d3d715609b063fe`:

- `.gitattributes` resolves representative source, governance, migration, and
  generated text paths to `eol: lf` even with `core.autocrlf=true`;
- substantive and mixed commits form `implementation_of` relations, while a
  generated-only refresh commit does not;
- the shipped bootstrap bundle matches its current templates and digest;
- Ruff formatting and lint pass for 86 Python files;
- strict mypy passes for 86 Python files;
- all 314 unit and fixture Tests pass;
- DSET repository validation, traceability freshness, project-health freshness,
  and `git diff --check` pass from a clean worktree.

The aggregate `dset verify` launcher itself could not complete in this sandbox:
its configured `uv run` commands first encountered the read-only user cache and
then a blocked PyPI tunnel when redirected to a new empty cache. The exact
configured Ruff, mypy, unittest, and diff commands were therefore run directly
from the existing locked environment, followed by explicit DSET checks.

This result resolves the local defect and proves a stable generated-view fixed
point. It does not close `DSET-TASK-TOOL-036`: fresh hosted Linux, macOS, native
Windows, and WSL evidence is still required.
