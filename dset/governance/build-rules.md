# Build rules

**Rule ID:** `DSET-RULE-BUILD`

## Selected gates

- Start from accepted requirements, deterministic tests, applicable evals, architecture, and authorization boundaries.
- Select runtime risk, durability topology, language enforcement, artifact governance, and supportability independently.
- Keep pure domain policy separate from effects and adapters; use repository-specific architecture when it is stricter.
- Add a failing deterministic proof before repairing reproducible behavior. Record variable baselines and rubrics in the eval plan.
- Use at-least-once delivery with receiving-side idempotency or deduplication where retries apply; never claim universal exactly-once behavior.
- Keep one durable authority per concern and use WAL, replay, reconciliation, or observed-progress rules only when the selected risk and topology require them.
- Preserve user changes, avoid destructive writes, run selected gates, and record bounded supportability evidence.
- Return durable conclusions to the owning DSET change and keep unfinished capability claims explicit.
