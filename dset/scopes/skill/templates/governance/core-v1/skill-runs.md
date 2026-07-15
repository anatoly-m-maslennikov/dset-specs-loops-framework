# Skill-run record rules

## Authority and lifecycle

The DSET runtime adapter owns one immutable JSON record per invocation under
ignored `.dset/runs/`. The filename is
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

The runtime atomically maintains one replaceable checkpoint per session under
ignored `.dset/sessions/<session-id>.json`. A checkpoint contains the same
bounded `llm_session_ids`, a bounded objective summary, current
project/package/Change and repository-or-Work-Area target, resolved ruleset,
completed and pending stable IDs or artifact paths, authorization state, the
last authoritative-state snapshot, and the next recommended handoff. It must
not contain full prompts, source content, arbitrary tool output, credentials,
or an unbounded conversation summary. Immutable invocation evidence remains in
`.dset/runs/`; the checkpoint is only a recovery index over those runs and the
repository's authoritative artifacts.

Update the checkpoint after every workflow transition, before a known context
handoff or compaction when the host exposes that event, and on terminal exit.
Return the `session_id` with every handoff. Native host memory may cache the
same state, but it is never the only recovery mechanism.

On entry or after compaction, prefer the host-provided or explicit
`session_id`. Without one, select only a single newest active checkpoint whose
repository, workspace, and Change identity match; zero matches starts a new
session and multiple matches stop for operator selection. Before resuming,
re-read the repository, Git, active Change, proof, governance, and applicable
hosted owners. Mark stale checkpoint fields and recompute the next action; a
checkpoint never overrides newer authoritative state.

When checkpoint persistence is unavailable, return a bounded portable handoff
with `persistence: unavailable`. Low-risk read-only work may continue when its
rules allow it. A context handoff, consequential action, or compacted-session
resume that requires durable continuity must stop rather than claim it can be
resumed safely.
