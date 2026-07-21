+++
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-012"
priority = "high"
child_of = ["DSET-TEST-TOOL-021"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Test result — OYOHA local DSET adoption

**LLM session ID:**
`codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Subject and intended use

The owned TypeScript pilot
`anatoly-m-maslennikov/obsidian-your-harness` at local `dev` commit
`b960772` and DSET's candidate runtime through `0ea9bc3`. This record proves
that OYOHA has begun real, repository-local DSET adoption. It resolves the
narrow historical claim that the pilot had no DSET control plane; it does not
claim complete pilot readiness or promotion of `typescript-v1-candidate`.

## Result

The pilot has one visible schema 1.2 `dset/` root, repository-local
governance and provenance registries, five layer-owned `harness` package
fragments, project-owned rules, generated compilation/trace/health views, an
active adoption Change, and project-local thin skill wrappers. A bounded
inventory classifies every legacy spec/plan family, root and scoped agent-rule
surface, architecture hub, Test owner, workflow, and generated output without
prematurely cutting over its current owner.

The project-local candidate profile passes structural inspection. TypeScript
and ESLint hard errors are zero, the warning ratchet shrank from 203 to 202,
and 5,876 Jest tests pass without a product assertion failure. Nine
loopback-HTTP Tests remain inconclusive in the Codex host. Candidate CI is now
active for remote `dev` and pull requests to `main`, with read-only
Ubuntu/macOS/Windows jobs, full-history secret scanning, isolated build/output
comparison, and a revision-bound plugin artifact. Configuration is not hosted
Evidence: no run result is promoted by this record.

## Fresh deterministic checks

At OYOHA `b960772`, these commands exited `0`:

```text
python -m dset_toolchain check /path/to/obsidian-your-harness
python -m dset_toolchain trace /path/to/obsidian-your-harness --check
python -m dset_toolchain profile check /path/to/obsidian-your-harness \
  --profile typescript-v1-candidate \
  --target /path/to/obsidian-your-harness --format json
npm run typecheck
npm run lint -- --quiet
```

The OYOHA repository owns the detailed evidence in
`dset/scopes/gov/changes/adopt-dset/proofs/`. Its active Change remains open.

## Unresolved uses and reopen conditions

This result does not close the complete Jest Test, hosted matrix, secret scan,
qualitative Evaluation, native Codex/Claude invocation, production
supportability, legacy-owner cutover, real feature delivery, PR, release, or
clean upstream Claudian obligations. Reopen it when the cited OYOHA revision,
control-plane ownership, layer/package structure, profile, wrapper set, or
legacy-owner classification changes.
