+++
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-022"
priority = "high"
child_of = ["DSET-REQUIREMENT-SKILL-011"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Test result — documented-path Codex host invocation attempt

**LLM session IDs:**

- `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Subject and intended use

DSET commit `87a9a8c6f7098c9c1231d0949fbcdbffd799830d` and Codex CLI
`0.144.5`. This record reopens the Codex host boundary after aligning the
default skill destination with the host's documented `.agents/skills`
location. It may prove the exact-head install layout and verifier result only;
it does not prove host discovery, load, invocation, local-rule handoff, or stop
behavior.

## Performed work and result

The default dry run planned all 16 thin wrappers under
`~/.agents/skills` and the shared runtime under `~/.codex/packages/dset`.
Every destination was absent. A separate repository-local transaction then
installed the same exact-head wrappers under `.agents/skills` and the shared
runtime under `.codex/packages/dset`. Installation verification passed for all
16 copied wrappers and the package manifest, launchers, and digest. The runtime
digest was
`2d53cf9fa427d6264b9c8c753f6cb3a48caa17055bed782549657922e0cd2232`.

The authenticated Codex CLI was then invoked from that repository-local host
root with explicit `$dset`, target repository, objective, and workspace-write
boundaries. Both normal and authorized outer execution reached the same
pre-discovery stop: the app-managed process could not write
`~/.codex/state_5.sqlite`, then failed to initialize its in-process app-server
client with `Operation not permitted`. The skill was not loaded and no
invocation receipt was created.

```text
codex login status
  Logged in using ChatGPT

python -m dset_toolchain skills install --host codex --source .
  preview: pass; 16 wrappers under ~/.agents/skills plus packages/dset planned

python -m dset_toolchain skills install --host codex --source . \
  --destination HOST_ROOT/.agents/skills \
  --package-destination HOST_ROOT/.codex/packages/dset --apply
  result: pass

python -m dset_toolchain skills verify --host codex \
  --destination HOST_ROOT/.agents/skills \
  --package-destination HOST_ROOT/.codex/packages/dset
  result: pass

codex exec ... 'Use $dset explicitly ...'
  blocked before discovery: read-only state database; app-server EPERM
```

## Boundaries and reopen conditions

Reopen from an authenticated Codex host process allowed to write its own state
and initialize its app-server client. Repeat the install and invocation when a
later DSET commit changes any distributed wrapper, shared-runtime byte, host
location rule, or supported Codex version. Do not promote a receipt until the
real host observes discovery, load, invocation, local governance resolution,
handoff, and a terminal stop record.
