+++
artifact_id = "DSET-ATOMIC-RECORD-006"
semantic_id = "DSET-REQUIREMENT-SKILL-010"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:skill"]
status = "accepted"
priority = "unknown"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Requirement — Enter skills by desired outcome

Public DSET skills are invoked for the result the operator wants, not only
after the operator has manually satisfied their prerequisites. The
repository-local lifecycle rule owns each workflow's entry criteria, allowed
prerequisite workflows, exit criteria, and stop conditions.

When an entry criterion is missing, a skill may invoke only the registered
prerequisite workflows needed to satisfy it. After every child workflow it
must re-read authoritative project state. Every transition must satisfy at
least one previously missing criterion; repeated state, a cycle, no progress,
ambiguity, failure, or a new authorization boundary stops the chain.

`dset-implement` first invokes `dset-decisions` to reconcile available current
host-session history, the DSET session checkpoint and run records, Git, and
current project artifacts into any missing accepted atomic records. It then
invokes `dset-plan-proof` when separate Test or Evaluation plans are incomplete
and `dset-plan-implementation` when executable planning is incomplete. It
implements only after the resolved implementation entry criteria are met.

Session history, checkpoints, and run records are candidate evidence, never
authority. `dset-decisions` must not invent an operator acceptance, silently
resolve an uncertainty, or edit an existing atom. After compaction or when
history is unavailable, it reconciles the bounded checkpoint and repository
owners and returns every material unknown that still needs operator input.
Every child run preserves the common DSET session and contributing
host-prefixed LLM-session provenance.

This Requirement replaces the `dset-decide` name and fixed two-transition
limit from `DSET-DECISION-SKILL-002` with `dset-decisions` and a finite
progress-bounded closure. All other topology, thin-wrapper, local-authority,
proof-separation, and exception claims of that parent remain active.

## Rationale

Operators should be able to ask for implementation without memorizing the
framework's internal workflow graph. Explicit entry and exit criteria keep the
convenience deterministic and auditable while project-local governance, not a
generic wrapper or conversation memory, continues to own the behavior.

This emitted Requirement atom is immutable. Later correction, absorption, or
retirement requires a new linked atom or append-only lifecycle event.
