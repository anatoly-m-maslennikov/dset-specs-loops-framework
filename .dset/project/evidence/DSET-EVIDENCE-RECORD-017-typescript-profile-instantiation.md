+++
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-017"
priority = "high"
child_of = ["DSET-TEST-TOOL-022"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Test result — TypeScript profile instantiation boundary

**LLM session IDs:**

- `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Subject and intended use

DSET commit `9d9a209832a7b205790245c59a0d193c218b8762`. This record
verifies the deterministic distinction between an evidence-derived framework
profile reference and a project-owned applied instance. It does not pass the
separate qualitative profile-role Evaluation or promote `typescript-v1`.

## Result

The enforcement-profile schema requires `profile_role: reference|applied`.
Applied instances require a non-empty `derived_from`; references reject that
field. Read-only inspection reports the selected role. Resolution still
prefers `dset/scopes/tool/profiles/<id>.yaml`, but a non-framework adopter now
fails closed when only the distributed reference exists. The framework source
can resolve its own reference for pinned comparison.

The focused schema/bootstrap suite passed 12 tests. The complete framework gate
set then passed:

```text
ruff format --check .                    75 files formatted
ruff check .                             no findings
mypy dset_toolchain                      35 source files, no issues
python -m unittest                       223 tests
dset check .                             pass
dset rules check .                       pass
dset compile . --check                   fresh
dset trace . --check                     fresh
dset health . --check                    fresh
git diff --cached --check                pass
```

The generated bootstrap bundle was rebuilt and its freshness/digest test passed.

## Boundaries and reopen conditions

OYOHA must add `profile_role: applied` and its reference origin before consuming
this runtime commit. The profile remains a candidate, with hosted and
independent qualitative gates open. Reopen when role semantics, resolver
precedence, repository-role detection, schema, bootstrap bundle, applied origin,
or promotion rules change.
