+++
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-018"
priority = "high"
child_of = ["DSET-REQUIREMENT-SKILL-011"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Test result — Codex host installation attempt

**LLM session IDs:**

- `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Subject and intended use

DSET commit `ca3faa2c99099ca708c5be5f0f0e685926132240`. This record
tests the real Codex installation boundary for `DSET-CONTRACT-SKILL-001` and
`DSET-TEST-PLAN-SKILL-011`. It may support only the current blocked disposition; it
does not prove host discovery, load, invocation, local-rule handoff, or stop
behavior.

## Performed work and result

The canonical dry-run installer resolved the current user's Codex host root,
planned all 16 thin wrappers under `~/.codex/skills`, and planned one shared
runtime package under `~/.codex/packages/dset`. Every destination was absent,
and the runtime source digest was
`32a771af68dd44f12b3fef58b36856591bce94cbc437334714d1eabe1c44aa07`.

The apply transaction then stopped before writing any skill or runtime package.
The Codex app process could not create the installer's atomic staging directory
under `~/.codex/skills` and returned `EPERM` (`Operation not permitted`). The
no-partial-write boundary therefore held, but no host-native installation
receipt can be promoted.

```text
python -m dset_toolchain.skill_distribution install --host codex --source .
  preview: pass; 16 wrappers plus packages/dset planned

python -m dset_toolchain.skill_distribution install --host codex --source . --apply
  blocked: EPERM creating the atomic staging directory under ~/.codex/skills
```

## Boundaries and reopen conditions

Reopen when an operator runs the same exact-source transaction from a process
authorized to write the Codex host root, when the install destination or
installer changes, or when a later DSET commit changes any distributed wrapper
or shared-runtime byte. After installation, separate authenticated host
discovery, load, invocation, handoff, and stop observations are still required.
