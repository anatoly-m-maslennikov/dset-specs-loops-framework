# Methodology SKILL domain

This is one layer-owned fragment of the logical methodology package. Use the sibling layer hubs for connected definitions; this file owns only the entities and invariants below.

## Entities

| Entity | Definition |
|---|---|
| **Workflow wrapper** | A thin skill or runtime adapter that discovers the repository, invokes one registered workflow, reports the resolved ruleset, and hands off output without owning substantive rules |
| **Lifecycle orchestrator** | The primary `dset` workflow wrapper that inspects authoritative project/change state, selects a bounded next action, and chains registered workflows without owning their rules |
| **Skill-run record** | Bounded structured machine-local evidence of one invocation, stored under ignored `.dset/runs/` for investigation and heuristics without becoming project truth |
| **Session checkpoint** | Bounded replaceable machine-local recovery state for one operator-visible DSET session, stored under ignored `.dset/sessions/` and reconciled with authoritative state before reuse |
| **Delegation budget** | Project-owned policy for inherited model/effort, useful subagent fan-out, roles, rounds, context/evidence depth, tool/live-eval allowance, and stopping thresholds |
| **Expected outcome cost** | Predicted completed-task cost across token price/volume, retries, agent/tool steps, latency, failure probability, review burden, and rework rather than token price alone |

## Invariants

- **DSET-INVARIANT-SKILL-001:** Repository skills have distinct triggers and stop conditions and cannot replace the owning DSET specification, diagnosis authorization boundary, or implementation plan.
- **DSET-INVARIANT-SKILL-002:** Workflow wrappers own discovery, invocation, reporting, handoff, authorization, and stop behavior but no substantive workflow, architecture, authoring, proof, threshold, safety, or supportability rules.
- **DSET-INVARIANT-SKILL-003:** Changing a registered local rule changes the next governed invocation without changing the canonical workflow wrapper.
- **DSET-INVARIANT-SKILL-004:** The release-target user-facing skill surface contains one primary `dset` orchestrator plus the narrow `dset-clarify`, `dset-diagnose`, `dset-prototype`, and `dset-release` specialists; helper lifecycle actions remain modes or chained workflows.
- **DSET-INVARIANT-SKILL-005:** Skill-run records are schema-bounded, redacted, immutable local operational evidence with finite retention; unavailable persistence is explicit, and records never override accepted artifacts, active changes, Git history, hosted state, or promoted proof.
- **DSET-INVARIANT-SKILL-006:** Subagents request the main session's model and reasoning effort by default; capability and effective configuration are attested when possible, and every uncertainty or deviation is explicit.
- **DSET-INVARIANT-SKILL-007:** One tree-wide low/medium/high budget preserves requested scope, required proof, and safety while bounding unique agents, depth, and rounds; nominal token price alone never proves a cheaper plan.
- **DSET-INVARIANT-SKILL-008:** One operator-visible session links its public entrypoint, automatically chained skills, governed model-only workflows, and delegated runs; bounded checkpoint recovery survives context compaction without overriding newer repository, Git, proof, or hosted state.
