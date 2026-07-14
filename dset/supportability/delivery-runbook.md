# Delivery automation supportability runbook

## Scope and objective

This runbook covers the GitHub-hosted automation that accepts owner pushes to `dev`, validates owner-authored same-repository `dev → main` pull requests, runs DSET gates, enables merge-commit auto-merge, updates protected `main`, and—after the pending release publisher is implemented—creates the immutable tag and GitHub Release. It does not govern application runtime behavior in adopting repositories.

Investigate when a valid delivery remains blocked after its checks should finish, an invalid PR appears mergeable, a required check is missing or unexpectedly green/red, auto-merge fails, `main` does not contain the accepted `dev` head, or an activated publication run is absent, partial, colliding, or points at the wrong SHA.

## Authority and correlation

| Concern | Authoritative evidence | Correlation identity |
|---|---|---|
| Proposed change and code diff | GitHub pull request | repository-qualified PR number and URL |
| Exact implementation | Git commit on `dev` | full head SHA |
| Policy decision | `PR policy` check and workflow run | PR number, run ID, job ID |
| DSET enforcement | `DSET / validate` check | PR number, run ID, head SHA |
| Branch update rules | GitHub rulesets | ruleset ID and protected ref |
| Final publication | `main` merge commit | merge SHA with the accepted `dev` SHA as a parent |
| Product release declaration | Active DSET change manifest | change ID, class, protected base, and target version |
| Release tag | GitHub Git ref `refs/tags/v<product-semver>` | exact product version and protected merge SHA |
| Release object | GitHub Release | tag name, release ID, target SHA, and workflow run ID |
| DSET relationship view | `dset/traceability.yaml` | change ID and PR URL; GitHub remains authoritative |

Local files are source for workflow definitions and DSET contracts, not authoritative runtime state for GitHub checks, queues, or merges.

## Safe diagnostic sequence

1. Confirm the PR is in `anatoly-m-maslennikov/dset-specs-loops-framework`, authored by `anatoly-m-maslennikov`, with base `main`, head `dev`, and the same head repository.
2. Record the PR number, current head SHA, draft state, mergeability, and check conclusions. Do not expose tokens or raw environment data.
3. Open the `Enforce dev-to-main PR policy` run and verify the `PR policy` job evaluated the same PR/head identity.
4. Open the `DSET` run and inspect the first failed bounded gate: format, lint, typing, unit tests, DSET validation, trace freshness, or diff hygiene.
5. If checks pass but merge is blocked, inspect the [`main` ruleset](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/rules/18897046), permitted merge method, required check names, and auto-merge state.
6. After merge, verify the PR merge commit contains the exact accepted `dev` head as a parent. A green check on a different SHA is not completion evidence.
7. When publication automation is activated, verify the tag is exactly `v<product-semver>`, resolves to that merge SHA, and has not been reused or retargeted.
8. Verify the GitHub Release targets that tag, reports the canonical product SemVer, and was created by the publication run for the same merge SHA. A tag without a Release or a Release without the correct tag is partial publication.

Use `gh pr view`, `gh pr checks`, `gh run view`, and read-only ruleset/API queries when available. Keep diagnostic output to IDs, conclusions, durations, and concise failure excerpts.

## Containment and recovery

- Convert the PR to draft or close it to stop publication while preserving evidence.
- Rerun a failed job only when evidence indicates a transient GitHub/platform failure. Correct repository failures in a new commit and let checks run against the new SHA.
- Never bypass protected `main`, force-push either protected branch, or weaken the author/head/base policy to unblock one delivery.
- If auto-merge logic is defective, keep the PR draft, correct the workflow through the active DSET change, and require the policy and DSET checks on the corrected head.
- If a ruleset is misconfigured, capture its ID and current JSON, apply the smallest owner-authorized correction, then validate with a draft `dev → main` PR before publication.
- If a wrong merge reaches `main`, preserve the merge commit and use a reviewed revert PR. Do not rewrite public history.
- Publication retry is idempotent: accept an already-correct tag/Release pair, create only the missing object after partial failure, and make no content commit to `main`.
- Stop on an existing tag or Release with a different identity or SHA. Never retarget, delete-and-reuse, or force-update a public release tag.
- Preserve an incorrect published release as evidence and mark it withdrawn/deprecated when GitHub supports the required signal. Deliver a correction through a new `dev → main` PR with a higher version.

## Release publication activation

Post-merge tag/GitHub Release publication is specified but not yet implemented in this candidate. Until its workflow and hosted tests pass, a merged PR is not a published DSET product release and the release transaction remains incomplete. Activation must add the stable publication check/run identity to this runbook and prove exact-SHA, retry, partial-failure, and collision cases on the draft delivery path.

## Data controls

Workflow logs and PR metadata are public repository evidence. Do not print credentials, GitHub tokens, local paths containing private data, or unredacted external payloads. GitHub owns access, retention, deletion, and availability for hosted run logs; DSET stores only bounded links, IDs, conclusions, and synthetic proof. Keep check names and diagnostic cardinality bounded and stable.

## Escalation and traceability

Escalate platform outages to GitHub Status/Support and repository-policy defects to the repository owner. Link every correction to its requirement, DSET change, regression test or eval, PR, and final merge/revert result. Update this runbook when the authoritative workflow, ruleset, check name, or recovery path changes.
