# Skill-run record rules

## Authority and lifecycle

The DSET runtime adapter owns one immutable JSON record per invocation under
ignored `.dset_runtime/runs/`. The filename is
`<UTC-basic-time>-<random-run-id>.json`; creation must be atomic and must not
overwrite another record. A started record has `status: running`. Normal exit
atomically replaces only that run's temporary file with a terminal
`succeeded`, `failed`, or `stopped` record. A stale temporary file is diagnostic
evidence of an interrupted run and may be finalized as `interrupted` by a later
maintenance pass.

The collection is immutable-record, not append-only-storage: completed records
are never edited, but project retention may delete the oldest completed records
to satisfy all three default bounds of 30 days, 200 records, and 20 MiB. A
retention override belongs in project governance and must remain finite.

## Allowlisted fields

A record contains only schema version, run ID, parent run ID when present,
timestamps, status, repository-relative scope IDs, skill/workflow/mode IDs,
resolved ruleset identity, budget profile, requested and effective
model/effort attestation, planned and actual fan-out/rounds, named output paths,
stable result/diagnostic codes, next-step signals, and available aggregate
usage/cost metrics. Parameters are represented by allowlisted names plus
redacted categorical values or hashes; arbitrary values, full prompts, source
content, credentials, environment dumps, and raw tool logs are forbidden.
The published schema limits every string, collection, path count, diagnostic
count, and record to a maximum serialized size of 64 KiB.

A run or checkpoint may include a bounded non-empty `rationale` when a
non-obvious workflow, scope, budget, disposition, or next-handoff choice needs
explanation. The field is recommended only when it adds support or review value
and is never required. It cannot contain hidden instructions, source content,
or authority that is absent from the repository's canonical artifacts.

## Unavailable persistence

Before initialization, in a read-only workspace, or when local persistence
fails, the runtime emits the same bounded terminal record to the caller and
reports `persistence: unavailable`; it must not create a hidden project root or
claim a persisted record. Logging failure does not invalidate otherwise
read-only low-risk guidance. A selected risk/profile rule may require durable
audit evidence for a consequential action; in that case unavailable persistence
stops before the action.

Run records are advisory supportability evidence. Accepted specs, active
changes, Git/PR/check state, and promoted proof remain authoritative.

## Session continuity

One operator-visible DSET invocation starts or joins one bounded session. The
public entrypoint is recorded once; automatically chained skills, governed
workflows invoked directly by the model, and delegated runs remain children of
that session. They share a DSET `session_id`, identify their parent/root runs,
and record the host-prefixed `llm_session_ids` that materially contributed. An
empty list means no LLM contributed; it does not mean provenance is unknown.
Internal chaining therefore does not create extra user-facing skills or lose
either DSET session continuity or host-session provenance.

Every public or internally chained LLM wrapper passes its current host session
ID explicitly at context start and stops when the host cannot expose one. The
runtime rejects empty provenance for public-skill, chained-skill,
governed-model, and delegated-run sources; only an explicit operator source may
represent human-only execution with an empty list.

Every command in one installed skill run uses the exact launcher prefix
rendered into that wrapper. A logical `dset` token in resolved governance means
that same prefix; it never authorizes an ambient executable, a different Python
runtime, or a shell-dependent fallback.

The runtime atomically maintains one replaceable checkpoint per session under
ignored `.dset_runtime/sessions/<session-id>.json`. A checkpoint contains the same
bounded `llm_session_ids`, a bounded objective summary, current
project/package/Change and repository-or-Work-Area target, resolved ruleset,
completed and pending stable IDs or artifact paths, authorization state, the
last authoritative-state snapshot, and the next recommended handoff. It must
not contain full prompts, source content, arbitrary tool output, credentials,
or an unbounded conversation summary. Immutable invocation evidence remains in
`.dset_runtime/runs/`; the checkpoint is only a recovery index over those runs and the
repository's authoritative artifacts.

The checkpoint also carries a bounded `active_run_ids` stack. Starting a child
adds only that child; finalizing it removes only that child, so a still-running
parent remains finishable. `latest_run_id` identifies the newest invocation and
never grants exclusive ownership of the session. `dset runtime handoff`
finalizes one successful run while keeping the session `active`; it requires a
next signal and returns the same `session_id` for the next explicit context
call. `dset runtime finish` is terminal-only: success completes the session and
failure, interruption, or stop marks it stopped. A session cannot become
terminal while another run remains active.

Update the checkpoint after every workflow transition, before a known context
handoff or compaction when the host exposes that event, and on terminal exit.
Return the `session_id` with every handoff. Native host memory may cache the
same state, but it is never the only recovery mechanism.

On entry or after compaction, use the host-provided explicit `session_id`.
Only an initial governed wrapper entry with zero compatible active checkpoints
may omit it and start a new session. A wrapper entry with one or more compatible
active checkpoints but no explicit ID stops and reports the continuity gap; it
never joins or creates a chain implicitly. A read-only resume query may select
one compatible checkpoint and stops on multiple matches. Before resuming,
re-read the repository, Git, active Change, proof, governance, and applicable
hosted owners. Mark stale checkpoint fields and recompute the next action; a
checkpoint never overrides newer authoritative state.

When `decisions` reconciles current intent, it may inspect only host history
that the current invocation can actually access plus the bounded checkpoint,
run records, Git, and current artifacts. Those inputs propose candidate atomic
directives; they do not prove acceptance. Every emitted atom records the
available contributing `llm_session_ids`. Missing history after compaction is
reported as unknown when repository and checkpoint evidence cannot establish
the directive without invention.

Every fresh operator input is itself a required intake candidate. Before a
requested consequence continues, `decisions` must classify and emit all clear
primary claims as separate semantic atoms. It asks focused questions and stops
when strictness, authority, meaning, or acceptance prevents safe immutable
emission.

When checkpoint persistence is unavailable, return a bounded portable handoff
with `persistence: unavailable`. Low-risk read-only work may continue when its
rules allow it. A context handoff, consequential action, or compacted-session
resume that requires durable continuity must stop rather than claim it can be
resumed safely.
