+++
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-011"
child_of = ["DSET-TEST-PLAN-TOOL-021"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Test result — TypeScript candidate profile

**LLM session IDs:**
`codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Subject

DSET commit `de05bf282e603edff9459afc95680d05aa2ef69c` and the
read-only target `anatoly-m-maslennikov/obsidian-your-harness` at commit
`1c3ede2653245412d4d03067d5b20d9dd228298d`, branch
`codex/gpt-5-6-models`. The recorded upstream Claudian revision is
`783df1ceb149ac9cd9a00a3444c3dadf83bbacf4`; the repository license is MIT.

## Result

The executable `typescript-v1-candidate` profile passes its schema and
boundary tests. A read-only target inspection found the pinned revision,
package scripts, required files, and 348 source plus 254 test TypeScript files
without drift. It executed no target-owned command.

The profile maps all six neutral gate categories, records the canonical
typecheck/lint/test/build/DSET/trace/diff sequence, keeps the 203-warning ESLint
baseline shrink-only, and keeps every hard-error baseline at zero. The target
has no active GitHub Actions workflow: six definitions, including the
candidate CI workflow, are parked under `.github/workflows-disabled/`.

The candidate is intentionally not promotion-eligible. It records six live
blockers: one typecheck error, three lint errors, three product-test failures,
no project-local DSET control plane, no dedicated secret gate, and no current
hosted proof. Production build proof remains unclaimed because the local build
can copy output into a live vault; it requires an isolated target.

## Commands and evidence

```text
.venv/bin/ruff check dset_toolchain/enforcement_profiles.py dset_toolchain/cli.py tests/test_enforcement_profiles.py
.venv/bin/mypy dset_toolchain/enforcement_profiles.py dset_toolchain/cli.py tests/test_enforcement_profiles.py
.venv/bin/python -m unittest tests.test_artifact_lineage tests.test_enforcement_profiles -v
.venv/bin/python scripts/build_bootstrap_bundle.py
.venv/bin/python -m dset_toolchain profile check . --profile typescript-v1-candidate --target /Users/am/Documents/My_Repos/obsidian-your-harness --format json
.venv/bin/python -m dset_toolchain check .
.venv/bin/python -m dset_toolchain trace . --check
git diff --check
```

The focused suite passed 9 tests; the live inspection returned no structural
diagnostics, `commands_executed: false`, and `promotion_eligible: false`.
Canonical repository validation, trace freshness, and diff hygiene passed.

This evidence completes the inventory, neutral-gate mapping, canonical
sequence, syntax-aware boundary mapping, and warning-ratchet tasks. Secret,
generated-output, lockfile, and test-to-source enforcement remain open, as do
pilot adoption, hosted execution, independent Evaluation, and promotion to
`typescript-v1`.

## Reopen conditions

Reopen this result when either pinned repository revision changes, the profile
schema or commands change, the observed file population or warning baseline
changes, a blocker closes, or the candidate is considered for promotion.
