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
