---
artifact_type: "evidence_record"
artifact_subtype: "test_result"
artifact_id: "DSET-EVIDENCE-RECORD-046"
scope_path:
  - "layer:gov"
priority: "high"
schema_version: "1.0"
context:
  - "candidate_commit=57dd0a1a17f0c85118e10e628180c2222834df22"
  - "platform=macos"
  - "python=3.14.3"
  - "tests=326"
  - "ruff_files=94"
  - "mypy_modules=44"
  - "schema=1.3"
observed_at: "2026-07-22T21:19:36+04:00"
polarity: "supports"
currentness: "current"
reopen_when: "The .dset control boundary, .dset_runtime storage boundary, temporary-directory helper, bootstrap/self-host lifecycle, atomic-publication mechanism, migration, ignore rules, or configured verification commands change."
subject:
  id: "DSET-TEST-PLAN-GOV-048"
  revision: "57dd0a1a17f0c85118e10e628180c2222834df22"
  intended_use: "Verify separate committed-control, ignored-runtime, disposable-scratch, and bounded atomic-publication boundaries at one exact implementation commit."
producer:
  identity: "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
  performed_work: "Moved resumable machine-local state to repository-root .dset_runtime, routed disposable POSIX scratch to /tmp and Windows scratch to its native temporary root, made cleanup fail loud, migrated compatibility state without discarding it, prevented repository fixture leaks, rebuilt the bootstrap bundle, and executed the complete deterministic verifier."
method:
  description: "Ran the complete unit/integration suite, focused runtime and cleanup tests, Ruff formatting and lint checks, strict mypy, recursive DSET validation, compilation/traceability/health freshness checks, bootstrap freshness, and Git diff hygiene against the implementation commit."
  setup: "Codex Desktop managed workspace on macOS; repository virtual environment. The managed sandbox denies direct /tmp writes, so integration fixtures used a removed DSET_TESTING-only scratch root outside the repository; an override-disabled policy test separately proved that production POSIX resolution is /tmp regardless of ambient TMPDIR."
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "evidence_for"
    targets:
      - "DSET-TEST-PLAN-GOV-048"
---

# Test result — runtime and scratch boundaries

Commit `57dd0a1a17f0c85118e10e628180c2222834df22` implements four
non-overlapping state boundaries:

- committed governance and control truth under `.dset/`;
- ignored resumable machine-local state under `.dset_runtime/`;
- disposable process scratch under `/tmp` on POSIX or the native Windows
  temporary root; and
- same-directory atomic-publication staging only where replacement semantics
  require it, with cleanup or replacement before return.

The complete deterministic verifier passed:

- 326 unit and integration Tests;
- Ruff format check across 94 files and Ruff lint;
- strict mypy across 44 source modules;
- fresh active-authority compilation, traceability, and project health;
- recursive `dset check` and bootstrap-bundle freshness; and
- `git diff --check`.

Focused coverage proves runtime/checkpoint placement, native-platform scratch
selection, cleanup after successful and handled-failure paths, bootstrap and
self-host isolation, migration compatibility, transactional rollback, and no
new `dset-init-*`, `dset-source-*`, or `dset-self-host-*` directory under the
repository. The dedicated integration scratch root was empty after the suite
and was removed.

The managed Codex sandbox did not permit a direct filesystem write to `/tmp`;
therefore this record proves the production POSIX path choice deterministically
but does not claim a native-host `/tmp` creation receipt. Qualitative boundary
interpretation remains separate under `DSET-EVAL-PLAN-GOV-032`.
