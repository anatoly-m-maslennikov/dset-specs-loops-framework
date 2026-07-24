# Methodology IMPL specification

## DSET-DECISION-IMPL-001 — Model IMPL as selectable profile features

IMPL is the development-realization layer between SKILL and OPS. It owns
environment and dependency setup, production code, automated Test code,
Evaluation implementations, code-focused gates, and any diagnostics or hooks
implemented in code. It contains peer selectable Implementation Profile
features rather than nested layers.

A project may select more than one compatible profile for explicit work areas.
A host-specific profile may extend a broader profile without copying it.

## DSET-REQUIREMENT-IMPL-001 — Provide the Local Python Tools profile

DSET provides `local-python-tools-v1` for small local Python tools. The profile
owns concrete environment, source-structure, size, reuse, data-modeling,
schema, settings, naming, documentation, failure, Test, Evaluation,
portability, and conditional NDJSON rules. The machine-readable profile owns
its thresholds and switches.

## DSET-REQUIREMENT-IMPL-002 — Require portable, simulatable, diagnosable tools

Every governed executable accepts a no-mutation `--dry-run` mode and begins
with usage and effect documentation appropriate to its role. Errors remain
actionable and redacted without debug mode. Non-trivial tools should offer a
safe `--debug` mode. Implementations are readily transferable across macOS,
native Windows, WSL, and Linux and isolate unavoidable host-specific behavior.

## DSET-REQUIREMENT-IMPL-003 — Place and explain settings and constants

A separate settings file is optional. Every module nevertheless groups all
module-level settings, defaults, thresholds, and constants immediately after
its module docstring and imports, before classes, functions, or runtime
statements. Every constant explains its responsibility, unit or interpretation
where relevant, and authority or override boundary. Profile thresholds,
including the exclusive 40-line function limit, remain explicit profile TOML
settings rather than hidden checker literals.

## DSET-DECISION-IMPL-002 — Canonical project-health path ordering

Derived project-health source digests order included files by case-sensitive
POSIX relative-path text before hashing that path text and current working-tree
bytes. This replaces `DSET-DECISION-OPS-009`; TOOL continues to own the
observable health contract.

## DSET-DECISION-IMPL-003 — Platform-native verification placeholders

Verification templates are tokenized before exact-token replacement. An
argument equal to `{python}` becomes the current Python executable as one
direct subprocess argument and is never reparsed as shell text. This replaces
`DSET-DECISION-OPS-010`.

## DSET-DECISION-IMPL-004 — Canonical filesystem path boundaries

Filesystem paths are compared by resolved identity. Relative `Path` inputs are
serialized with POSIX separators before repository-relative validation, while
serialized string inputs must already use canonical POSIX separators. This
replaces `DSET-DECISION-OPS-011`.

## DSET-DECISION-IMPL-005 — Deterministic temporary Git bytes

Temporary Git repositories used by deterministic Tests disable autocrlf and
select LF through repository-local configuration before staging.
Byte-sensitive fixtures write explicit LF or observe materialized bytes before
asserting preservation. This replaces `DSET-DECISION-OPS-012`.

## Layer boundary

TOOL owns what the DSET executable must do. IMPL owns how selected profiles
realize upstream truth in an environment and implementation. OPS consumes the
finished surface for delivery, release, runtime operation, investigation, and
recovery. An operational deficiency is routed upstream through a new artifact;
OPS never governs IMPL backwards.
