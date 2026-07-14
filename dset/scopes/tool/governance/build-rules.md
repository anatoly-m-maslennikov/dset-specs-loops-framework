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

## Review profiles

Every Change passes the baseline gates: scope and authority review, Contract and
Requirement trace review, focused diff review, applicable tests and evals,
supportability review, and repository hygiene. The Change records the selected
risk profile and adds triggered gates for security or permissions, sensitive
data, migrations, concurrency, external effects, irreversible writes,
cross-platform behavior, or release/publication. Risk increases evidence and
review depth; low risk does not erase the baseline.

## Change isolation and delivery

Default to local work on the configured integration branch, push that branch to
its remote counterpart, then open the integration-to-protected release PR. A
Change may instead select `branch-worktree` when parallelism, risk, or
conflicting work needs an isolated branch-backed workspace/worktree; that branch
reviews into the integration branch before release. Do not create permanent
branches for DSET layers.

Sharing the integration branch or release PR never merges Change identities,
proof, scope, or authorization. One Change may cross multiple layers atomically;
split it only when the parts are independently reviewable, verifiable, and
mergeable without an invalid intermediate state.
