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

## DSET-REQ-IMPL-007 — Promote runtime configuration deliberately

Every Implementation Profile defines explicit heuristics for keeping invariants
as code constants and promoting runtime policy to a typed settings carrier.
Keep a value in code when it is universal across supported environments,
changes only with the implementation, and expresses an algorithm, schema,
protocol, or safety invariant. Promote it when an operator must change it
without a code release, it varies by host or integration, multiple consumers
share it as runtime policy, or it needs typed validation, documented precedence,
or an auditable override boundary. A Test variant alone does not justify a
settings file, and a settings file is not a dumping ground for literals.

## DSET-REQ-IMPL-008 — Implement project-wide secret exclusion

Every applicable Implementation Profile excludes secret values from DSET,
source, non-secret settings, command lines, builds, logs, diagnostics, Tests,
Evaluations, prompts, evidence, and generated files. Local development injects
secrets from an ignored `.env` outside `.dset`; CI and production use platform
or dedicated secret injection. Implementations validate at the outer boundary,
redact before serialization or agent ingestion, scan shared surfaces, use
least-privileged and preferably short-lived credentials, fail closed without
printing a value, and revoke or rotate immediately after suspected exposure.

Email addresses, usernames, and account IDs are not authenticators. They may
appear in DSET when necessary and authorized, but remain minimized personal
data and are sourced from the environment when used as mutable runtime values.

## DSET-REQ-IMPL-009 — Resolve runtime identities and secrets by key

Source code and DSET store only stable environment-variable key names for
runtime logins, emails, account IDs, API keys, passwords, tokens, and other
secrets. Scripts resolve and validate the corresponding values at their outer
runtime boundary, then inject them into the smallest consumer scope. Local
development backs the keys with ignored `.env`; managed hosts may supply the
same keys through environment or secret injection. Help, diagnostics, logs,
prompts, evidence, and errors never render resolved values.

## DSET-REQ-IMPL-005 — Apply the Agent Skills profile

Every created or updated reusable agent skill must pass
`agent-skills-v1` before acceptance, installation, distribution, or use as
current DSET methodology. The provider-neutral skill core owns routing,
judgment, workflow, authorization, safety, verification, and stop behavior.
Deterministic mechanics move to portable scripts; static bulk moves to focused
on-demand resources; host-specific discovery and metadata remain explicit
adapters.

Each changed skill retains its load-bearing behavior and has representative
trigger, non-trigger, and ambiguous-routing cases plus applicable isolation,
coexistence, instruction-following, stop, and output-quality coverage. A claim
for one provider, host, or model requires evidence for that exact matrix cell
and never implies compatibility with another.

## DSET-REQ-IMPL-006 — Apply the LLM Evaluations profile

Every created or updated Evaluation definition, case set, prompt, harness,
grader, reconciliation procedure, and result carrier must pass
`llm-evaluations-v1`. The definition names its governed claims, why a
deterministic Test is insufficient, exact subject and revision, bounded inputs,
case distribution, rubric, threshold, grading and calibration method, tools,
budget, evidence schema, and freshness rule before execution.

Deterministic facts remain Tests or code graders. Judgment-based grading uses
anchored criteria and calibrated human or model review. Definitions,
execution, result evidence, and Verification remain distinct. Reconciliation
compares only matching Evaluation versions and configurations, preserves
per-case findings and failures, and treats unresolved material disagreement as
inconclusive. Provider/model/host identity is run configuration, not hidden
Evaluation semantics.

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
