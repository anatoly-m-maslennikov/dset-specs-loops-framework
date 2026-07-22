# Expanded skill-surface verification — 2026-07-16

- **Claim:** The source and host-distribution catalog contains exactly 16
  public skills, every stable governed lifecycle mode has one thin direct
  wrapper, and initialization plus governance repair remain the only bounded
  pre-resolution exceptions.
- **Current:** Yes for source, registry, bootstrap, copy-distribution, and local
  deterministic proof at the evaluated commit. Real authenticated host
  invocation and hosted cross-platform proof remain separate open gates.
- **Evaluated commit:**
  `f42fe8736645833e3c709b17b799e991e45ee9a0`
- **Decision:** `DSET-DECISION-SKILL-002`
- **Task:** `DSET-TASK-SKILL-022`
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Evaluated surface

The machine-owned catalog declares 16 public source packages. Fourteen map to
registered repository-local workflows. `dset-init` maps only to the rootless
preview/authorize/materialize/validate transaction, and
`dset-repair-governance` maps only to fail-closed registry diagnostics and a
repair handoff.

The ordinary generated adopter declares release not applicable and therefore
materializes 13 governed wrappers. The release-applicable fixture materializes
all 14 governed wrappers. Both host-copy distributions contain all 16 public
packages because distribution capability is independent of one adopter's
workflow applicability.

## Deterministic evidence

| Check | Result |
|---|---|
| Skill Creator `quick_validate.py` shape algorithm over every `SKILL.md` | 16/16 valid. Available Python runtimes lacked PyYAML, so the unchanged validator was supplied a temporary `safe_load` compatibility shim backed by DSET's YAML-subset parser; the shim and failed uv cache were removed after the run. |
| Exact source catalog and invocation markers | Pass; missing, extra, stale, symlinked, or marker-mismatched packages fail closed. |
| Codex and Claude copy distribution fixtures | Pass for all 16 packages with real folders, UI metadata, deterministic digests, collision stops, and invocation-contract receipts. |
| Governance profile and live registry parity | Pass for 14 registered workflows/wrappers; every direct workflow includes session/run support dependencies in valid order. |
| Rootless/invalid-governance exception tests | Pass; initialization is dry-run-first and no-overwrite, while repair cannot resolve invalid substantive rules or write without separate authorization. |
| Bootstrap bundle regeneration and source-mode end-to-end initialization | Pass; a generated ordinary adopter receives the 13 applicable wrappers and validates. |
| `python -m unittest discover -s tests` | Pass: 131 tests. |
| `.venv/bin/ruff check dset_toolchain tests scripts/build_bootstrap_bundle.py` | Pass. |
| `.venv/bin/mypy dset_toolchain tests` | Pass: 46 source files. |
| Candidate `dset check` | Pass with empty diagnostics. |
| `git diff --check` | Pass. |

The aggregate `dset verify` command was also attempted and did not receive a
pass: its configured `uv run ruff format --check ...` subprocess could not
initialize the user uv cache or fetch the build-time `setuptools>=68`
dependency through the Codex app sandbox. The exact configured Ruff format,
Ruff lint, mypy, unit, candidate-check, and diff gates were run directly and
passed as listed above. The aggregate wrapper failure is retained as an
environment/tooling limitation rather than converted into a false pass.

## Ownership and portability review

All new `SKILL.md` files stay below 24 lines, contain no machine-specific
paths, shell-specific procedure, copied project threshold, or alternate
normative fallback. Governed wrappers resolve local rule documents before
acting. Every package includes Codex `agents/openai.yaml`; the same folder is a
valid Claude skill source. The centralized catalog drives source validation,
bootstrap inclusion, host installation, receipt workflow identity, and tests.

## Limits and reopening

This proof does not claim a successful authenticated Codex or Claude inference,
host-native invocation receipt, hosted Linux/macOS/native-Windows/WSL run, or
release publication. Those remain governed by `DSET-TASK-SKILL-020`,
`DSET-TASK-TOOL-036`, and `DSET-TASK-OPS-025`.

Reopen this proof when any public skill, workflow registration, invocation
marker, bootstrap bundle, distribution logic, governance applicability, host
format, or evaluated implementation input changes. The prior five-skill proof
remains immutable historical evidence for its own commit and no longer proves
the current public topology.
