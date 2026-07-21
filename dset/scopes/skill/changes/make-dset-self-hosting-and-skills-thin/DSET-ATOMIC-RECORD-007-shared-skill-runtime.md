+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-007"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-SKILL-011"
status = "accepted"
priority = "critical"
child_of = ["DSET-REQUIREMENT-SKILL-010"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Requirement — Use one deterministic shared skill runtime

All DSET skills for one agent host use one installed shared runtime package.
For Codex, the package root is `$CODEX_HOME/packages/dset/`, with
`$CODEX_HOME` defaulting to the host's normal Codex data directory. Other
supported hosts map the same DSET distribution to an equivalent host-owned
package root. This location is a DSET distribution convention, not a source of
project governance.

The framework repository and its published distribution remain the canonical
source of the shared runtime. An installer copies a versioned runtime and
manifest into the host package root and exposes one portable `dset` launcher.
Thin skill folders contain no duplicated shared scripts or project rules.

Every governed skill invocation calls one deterministic context operation with
its public skill ID and explicit target. The operation discovers exactly one
owning repository or monorepo Work Area, validates local governance, maps the
skill to its registered workflow, resolves the ordered local rule set, and
returns stable project, workflow, rule, wrapper, conflict-coverage, and ruleset
identities. The operation also starts or resumes the bounded DSET session when
the selected workflow requires runtime state.

Project discovery, workflow mapping, rule resolution, and session setup are
mechanical runtime responsibilities. The LLM interprets the resolved project
rules and performs judgment; it does not walk parent directories, select
between competing executables, reconstruct skill-to-workflow mappings, or
silently fall back to memory, templates, another repository, or remote prose.
Missing installation, competing roots, invalid governance, a skill/workflow
mismatch, or unavailable required conflict coverage stops with stable
diagnostics.

The runtime and wrappers must be usable on macOS, Linux, native Windows, and
WSL. Core behavior must not depend on POSIX shell syntax, symlinks, executable
permission bits, hardcoded home paths, or host-private state.

## Rationale

One shared deterministic runtime removes repeated mechanical logic from every
skill, keeps byte-identical wrappers project-agnostic, and gives all hosts the
same validated boundary between installed distribution code and repository-
owned governance.

This emitted Requirement atom is immutable. Later correction, absorption, or
retirement requires a new linked atom or append-only lifecycle event.
