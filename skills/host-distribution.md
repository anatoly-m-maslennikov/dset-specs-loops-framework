# DSET skill host distribution

The 16 folders listed in the [skills hub](README.md) and the repository's
`dset_toolchain` package are canonical source artifacts. A host installation
copies the thin wrappers and one shared runtime package. Installed copies do
not become editable rule owners.

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

The same transaction previews or installs the shared runtime under
`CODEX_HOME/packages/dset` or `CLAUDE_CONFIG_DIR/packages/dset`; without an
environment override it uses `.codex/packages/dset` or
`.claude/packages/dset` below the current home directory. An explicit skill
destination derives a sibling `packages/dset` root unless
`--package-destination PATH` is supplied. The package contains copied Python
sources, a versioned manifest, the portable `dset.py` launcher, and native
`dset`/`dset.cmd` adapters. It has no project governance: every invocation
resolves the explicit target's repository-local authority.

During installation, each copied wrapper is rendered with the exact current
Python interpreter and package-local `dset.py` path from the same preview. The
installed wrapper therefore does not depend on a global `dset` command or a
mutable `PATH`; a changed source, destination, interpreter, or launcher path
changes the planned digest and stops an unreviewed replacement.

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
frontmatter, Codex UI metadata when applicable, deterministic tree digest, the
registered shared-context invocation in every wrapper, and the runtime
manifest and launchers. Use `--package-destination PATH` when verifying a
non-default runtime root.

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
