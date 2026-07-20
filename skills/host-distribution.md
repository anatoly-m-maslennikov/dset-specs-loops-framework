# DSET skill host distribution

The 16 folders listed in the [skills hub](README.md) are canonical source artifacts. Host
installations are copied distributions: they do not become editable rule
owners, and installation never adds another public skill.

## Install

Preview is the default and writes nothing:

```text
python -m dset_toolchain.skill_distribution install --host codex --source .
python -m dset_toolchain.skill_distribution install --host claude --source .
```

Add `--apply` to perform the exact previewed copy. Existing byte-identical
folders are accepted; differing destinations stop without overwrite. Use
`--destination PATH` for a project-local or other explicit host skill root.
Without it, Codex uses `CODEX_HOME/skills` or the current user's
`.codex/skills`, and Claude uses `CLAUDE_CONFIG_DIR/skills` or the current
user's `.claude/skills`. These paths are derived at runtime through portable
path APIs on Linux, macOS, native Windows, and WSL.

The installer rejects symlinked source content and creates real copied skill
folders. It requires the exact 16-skill catalog: `dset`, `dset-init`,
`dset-repair-governance`, `dset-decompose`, `dset-diagnose`, `dset-clarify`,
`dset-landscape`, `dset-prototype`, `dset-decisions`, `dset-plan-proof`,
`dset-plan-implementation`, `dset-implement`, `dset-verify`, `dset-triage`,
`dset-release`, and `dset-complete`.

## Verify discovery

```text
python -m dset_toolchain.skill_distribution verify --host codex
python -m dset_toolchain.skill_distribution verify --host claude
```

Verification checks the host directory shape, copied-folder status, skill
frontmatter, Codex UI metadata when applicable, deterministic tree digest, and
the registered resolver invocation in every wrapper.

## Verify representative invocation

Generate a receipt template only after installation verification:

```text
python -m dset_toolchain.skill_distribution receipt-template --host codex --skill dset
```

After a real host session invokes the installed skill, fill the bounded receipt
with the host version, repository and session identities, and observed
discovery, load, invocation, local-rule resolution, handoff, and stop-boundary
results. Validate the saved JSON receipt with:

```text
python -m dset_toolchain.skill_distribution verify-invocation --host codex --skill dset --receipt RECEIPT.json
```

The verifier rejects a stale installed digest or any missing observation. A
receipt is an evidence envelope, not proof that the verifier itself launched
Codex or Claude. Release proof still requires a representative invocation in
each declared real host and pinned host-version evidence.

## Host references

The implementation was checked on 2026-07-16 against the official
[OpenAI Skills overview](https://help.openai.com/en/articles/20001066-skills-in-chatgpt),
[Claude Code skill locations](https://code.claude.com/docs/en/skills), and
[Claude configuration-directory contract](https://code.claude.com/docs/en/claude-directory).
Release evidence must still pin the exact host versions actually exercised.
