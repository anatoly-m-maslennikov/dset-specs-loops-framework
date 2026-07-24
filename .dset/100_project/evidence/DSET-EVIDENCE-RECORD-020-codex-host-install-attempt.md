+++
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-020"
priority = "high"
child_of = ["DSET-REQUIREMENT-SKILL-011"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Test result — exact-head Codex host installation attempt

**LLM session IDs:**

- `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Subject and intended use

DSET commit `1645e263682ffc76eee5f7c9c2084b92a5225121`. This record
reopens the real Codex installation boundary after the launcher, runtime,
session-provenance, and transactional-rollback corrections. It may support
only the current blocked disposition; it does not prove host discovery, load,
invocation, local-rule handoff, or stop behavior.

## Performed work and result

The exact-head dry-run resolved the current Codex host root and planned all 16
thin wrappers under `~/.codex/skills` plus one shared runtime under
`~/.codex/packages/dset`. Every destination was absent. The rendered launcher
used the repository's exact virtual-environment interpreter and the installed
runtime entry point. The planned runtime digest was
`b688e21986d6b50d7d0d1d81a98409e7bb4b8cbdea0f9ec5bb9d1d1344d5491d`.

The authorized apply transaction stopped before writing any destination. The
Codex app process could not create the atomic staging directory under
`~/.codex/skills` and returned `EPERM` (`Operation not permitted`). The
transaction therefore preserved the no-partial-write boundary.

```text
python -m dset_toolchain skills install --host codex --source .
  preview: pass; 16 wrappers plus packages/dset planned

python -m dset_toolchain skills install --host codex --source . --apply
  blocked: EPERM creating the atomic staging directory under ~/.codex/skills
```

## Boundaries and reopen conditions

Reopen when an operator runs the same exact-source transaction from a process
authorized to write the Codex host root, when the install destination or
installer changes, or when a later DSET commit changes any distributed wrapper
or shared-runtime byte. After installation, separate authenticated host
discovery, load, invocation, handoff, and stop observations are still required.
