# Methodology SKILL specification

## Active Decision source compilation

- `DSET-DECISION-SKILL-001` compiles as the repository-local, self-hosting,
  thin-wrapper, bounded-session, integration-first DSET 0.3 operating shape.
- `DSET-DECISION-SKILL-002` compiles as the public catch-all `dset` wrapper plus
  one thin direct wrapper for every registered stable lifecycle mode.

## DSET-REQUIREMENT-SKILL-001 — Workflow skills remain focused

The framework must publish distinct portable skills for pre-spec domain clarification, evidence-first diagnosis, and disposable prototyping. Each owns one trigger/output/verification/stop boundary. It writes durable conclusions to the active DSET change only when artifact writes are authorized; otherwise it returns the same bounded handoff without modifying the repository.

**Scenario DSET-SCENARIO-SKILL-001:** A diagnosis request cannot silently authorize a fix, and prototype evidence cannot enter production without an accepted Decision/design and normal implementation proof.

## DSET-REQUIREMENT-SKILL-002 — DSET 0.3 skills are thin wrappers

A DSET 0.3 skill may own trigger metadata, root discovery, workflow identity, resolver invocation, ruleset reporting, output handoff, authorization boundaries, and stop behavior. It must not own substantive workflow, architecture, authoring, proof, threshold, safety, or supportability rules.

**Scenario DSET-SCENARIO-SKILL-002:** Static inspection finds a workflow ID and resolver handoff in a skill but no copied checklist, concrete threshold, embedded fallback procedure, or substantive normative rule.

## DSET-REQUIREMENT-SKILL-003 — DSET 0.3 wrappers follow local changes

A DSET 0.3 wrapper must be project-agnostic and consume the currently resolved
rule set from the target project's local governance layer on every invocation.
The same installed skill package and wrapper hash must work across independent
repositories and monorepo Work Areas. Starting from the requested target, it
discovers exactly one owning DSET root, validates that root's selected local
registry, and reads only the rule documents returned by that project's
resolver before governed work.

Changing a registered local rule must affect the next invocation without
changing the canonical wrapper. Switching targets must switch project root,
registry, rule paths, customization, and ruleset identity without retaining
policy from the previous project. Competing roots, invalid ownership, or an
unavailable resolver stop the invocation; installed templates, another
project's cache, agent memory, and remote framework prose never substitute for
the target project's governance.

**Scenario DSET-SCENARIO-SKILL-003:** Two adopters use byte-identical wrappers
but different registered output conventions. Consecutive invocations from a
nested target in each repository discover different roots, follow only that
adopter's convention, and report its local rule paths and ruleset identity.

## DSET-REQUIREMENT-SKILL-004 — Every lifecycle mode has a public wrapper

The release target must expose `dset` as the catch-all lifecycle and next-step orchestrator plus one thin direct-entry wrapper for every stable lifecycle mode: `dset-init`, `dset-repair-governance`, `dset-decompose`, `dset-diagnose`, `dset-clarify`, `dset-landscape`, `dset-prototype`, `dset-decisions`, `dset-plan-proof`, `dset-plan-implementation`, `dset-implement`, `dset-verify`, `dset-triage`, `dset-release`, and `dset-complete`. Governed direct wrappers resolve one registered repository-local workflow. Initialization and governance repair are the only bounded pre-resolution exceptions. The project-owned `DSET-RULE-LIFECYCLE` rule defines desired outcomes, entry and exit criteria, trigger precedence, stop boundaries, and allowed prerequisite chaining.

**Scenario DSET-SCENARIO-SKILL-004:** An operator who does not know the next action enters through `dset`; an operator or automation that already knows the applicable mode invokes its direct wrapper and receives the same governed workflow and stop boundary.

## DSET-REQUIREMENT-SKILL-005 — The primary skill orchestrates local rules

After a valid local registry resolves, `dset` must use the `lifecycle-orchestration` workflow and stable modes `decompose`, `diagnose`, `clarify`, `landscape`, `prototype`, `decisions`, `plan-proof`, `plan-implementation`, `implement`, `verify`, `triage-work`, `release`, and `complete`. `DSET-RULE-LIFECYCLE` owns precedence, the exact specialist-workflow map, per-concern authority/freshness, finite entry-criteria closure, and authorization stops. A transition is allowed only when it satisfies a missing entry criterion; authoritative state is reread after each transition, and no progress, repeated state, cycles, ambiguity, failure, or a new authorization class stops the chain.

Before local resolution, the distribution owns exactly two bounded direct-entry exceptions: `dset-init` invokes the `dset init` dry-run/authorize/materialize/validate/stop transaction; `dset-repair-governance` invokes `dset rules check`, emits stable validation/ownership diagnostics and a repair handoff, then stops. Neither exception may make project decisions, use invalid local rules, or continue into governed work in the same invocation.

**Scenario DSET-SCENARIO-SKILL-005:** Byte-identical `dset` wrappers route two repositories differently because their project-owned rules and current artifacts differ, while both report the resolved local identities before acting.

## DSET-REQUIREMENT-SKILL-006 — Skill runs record bounded local evidence

The runtime adapter must follow `DSET-RULE-SKILL-RUNS` and the versioned skill-run schema. It atomically creates one immutable record per invocation, finalizes terminal status without editing another run, preserves interrupted temporary records as diagnosable evidence, enforces finite age/count/byte retention, and uses only allowlisted bounded/redacted fields. Before initialization, in read-only state, or when persistence fails, it emits the same record to the caller with `persistence: unavailable`; a risk/profile rule may require durable logging and stop a consequential action. Run records remain advisory and cannot replace accepted specs, active changes, Git/hosted state, or promoted proof.

**Scenario DSET-SCENARIO-SKILL-006:** A local log suggests verification is current, but Git shows later code changes; `dset` treats Git/change state as authoritative and recommends refreshed proof.

## DSET-REQUIREMENT-SKILL-007 — Delegation inherits the main session by default

Every subagent must request the main session's model family/version and reasoning-effort level by default. Before spawning, the runtime must discover whether it can request and attest those fields, then record requested/effective values as confirmed, runtime-default-unverified, or unsupported. A known override is reported before spawn. Unsupported or unverified inheritance stops when exact configuration is a proof/safety precondition; otherwise it may proceed only with visible uncertainty. No workflow may claim inheritance it cannot attest.

**Scenario DSET-SCENARIO-SKILL-007:** A main session at extra-high effort requests independent review; the default uses two or three extra-high reviewers on the same model. When that configuration is unavailable, DSET reports the constraint and follows an explicit project/operator decision rather than silently downgrading.

## DSET-REQUIREMENT-SKILL-008 — Budgets optimize expected outcome cost

The project-owned budget policy and `DSET-RULE-DELEGATION-BUDGET` must propagate one bounded budget through the whole delegation tree. `low` permits zero or one unique subagent, depth one, and one round; default `medium` targets two and permits at most three, depth one, and two rounds; `high` targets four and permits at most six, depth two, and three rounds. Capacity may reduce actual breadth with a recorded reason. Budget never reduces accepted scope, required proof, or safety gates; insufficiency stops for a scope/budget decision.

A model override requires dated task-relevant comparative evidence covering required quality, success/failure, tokens/prices when available, retries, steps, latency, review/rework, sample/harness, and limitations. Directly comparable measured cost may be compared; unlike metrics remain separate rather than receiving invented weights. Missing, stale, or incomparable evidence falls back to inherited model/effort. External single-agent benchmarks cannot justify multi-agent fan-out.

**Scenario DSET-SCENARIO-SKILL-008:** A lower-priced model uses more tokens and retries and completes fewer representative tasks; DSET does not classify it as cheaper for that work. A low budget reduces optional breadth, not committed scope or required proof.

## DSET-REQUIREMENT-SKILL-009 — Sessions survive chaining and context compaction

The public skills must share one internal session-continuity capability rather than expose a separate session-management skill. `dset` starts, checkpoints, and resumes its workflow chain; a directly invoked lifecycle skill starts or joins a compatible session; automatically chained skills, governed model-only workflows, and delegated work remain child runs. Every run carries DSET session/root/parent identity plus unique host-prefixed `llm_session_ids` for contributing LLM sessions, using an explicit empty list for human-only work. The runtime atomically updates a bounded ignored `.dset/sessions/<session-id>.json` checkpoint with the same provenance after workflow transitions, before an observable context handoff or compaction, and on terminal exit.

A checkpoint contains only a bounded objective, scope and artifact/run pointers, authorization state, authority snapshot, and next handoff. It excludes full prompts, source content, arbitrary tool output, and secrets. Resume prefers an explicit or host-provided session ID; otherwise it may select only one compatible newest active checkpoint and must stop on ambiguity. It re-reads repository, Git, Change, proof, governance, and applicable hosted state before recomputing the next action. Conversation memory and checkpoints remain advisory and cannot override those owners.

**Scenario DSET-SCENARIO-SKILL-009:** An operator invokes `dset`, which chains clarification and planning before the host compacts context. The next invocation reloads the same checkpoint, detects a newer Git change, invalidates the stale next-action hint, and recommends fresh verification without asking the operator to reconstruct the session or invoke a sixth skill.

## DSET-REQUIREMENT-SKILL-010 — Skills enter through outcome criteria

A public DSET skill accepts the desired outcome even when prerequisite artifacts
are incomplete. The repository-local lifecycle rule owns its entry criteria,
allowed prerequisite workflows, exit criteria, and stops. Missing criteria may
be satisfied through a finite registered workflow closure in one DSET session;
every transition must make observable progress and re-read authority.

`dset-implement` must first invoke `decisions` to reconcile available host
session history, bounded DSET continuity records, Git, and repository artifacts
into missing accepted atomic records. It then invokes `plan-proof` when the
separate Test or Evaluation plans are incomplete and `plan-implementation` when
the executable plan is incomplete. Only then may implementation begin.

Session and run history are candidate evidence rather than authority. The
decisions workflow never invents acceptance, silently resolves uncertainty, or
edits an emitted atom. Missing context is returned explicitly. Repeated state,
cycles, no progress, ambiguity, failure, and new authorization boundaries stop
the closure.

**Scenario DSET-SCENARIO-SKILL-010:** An operator asks `dset-implement` to build
a feature described only in the current session. The same DSET session records
accepted atomic directives, creates separate Test and Evaluation plans plus an
implementation plan where missing, then implements. If acceptance is unclear,
the chain stops with the exact Question instead of fabricating a Decision.

## DSET-REQUIREMENT-SKILL-011 — Skills use one deterministic shared runtime

Every DSET skill for one host must use one versioned shared runtime package. A
Codex installation places it under `$CODEX_HOME/packages/dset/`; other hosts
map the same distribution to an equivalent host-owned package root. Canonical
runtime source remains in the framework distribution, and thin skill folders
must not duplicate shared scripts or project rules.

The runtime must accept the public skill ID and explicit target, discover one
owning repository or monorepo Work Area, validate its local governance, enforce
the registered skill/workflow mapping, resolve ordered rules and stable
identities, and start or resume bounded session state where applicable. The LLM
interprets returned rules but must not perform mechanical root discovery,
entrypoint selection, workflow reconstruction, or fallback. Missing
installation, competing roots, invalid governance, mapping mismatch, or
required unavailable conflict coverage stops with stable diagnostics.

**Scenario DSET-SCENARIO-SKILL-011:** The same installed `dset-implement`
wrapper is invoked from nested paths in two repositories. One shared runtime
resolves different project roots and rule digests from the explicit targets,
rejects a mismatched workflow, and records both invocations without scripts or
governance copied into either skill folder.
