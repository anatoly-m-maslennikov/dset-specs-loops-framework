# Delivery automation supportability runbook

## Scope and objective

This runbook covers the GitHub-hosted automation that accepts owner pushes to `dev`, validates owner-authored same-repository `dev → main` pull requests, runs DSET gates, enables merge-commit auto-merge, updates protected `main`, and, when the coordinated version contract changes, creates or verifies the immutable tag and GitHub Release at the exact merge SHA. It does not govern application runtime behavior in adopting repositories.

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
| DSET relationship view | `dset/scopes/gov/generated/traceability.toml` | change ID and PR URL; GitHub remains authoritative |

Local files are source for workflow definitions and DSET contracts, not authoritative runtime state for GitHub checks, queues, or merges.

## Safe diagnostic sequence

1. Confirm the PR is in `anatoly-m-maslennikov/dset-specs-loops-framework`, authored by `anatoly-m-maslennikov`, with base `main`, head `dev`, and the same head repository.
2. Record the PR number, current head SHA, draft state, mergeability, and check conclusions. Do not expose tokens or raw environment data.
3. Open the `Enforce dev-to-main PR policy` run and verify the `PR policy` job evaluated the same PR/head identity.
4. Open the `DSET` run and inspect the first failed bounded gate: format, lint, typing, unit tests, DSET validation, trace freshness, or diff hygiene.
5. If checks pass but merge is blocked, inspect the [`main` ruleset](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/rules/18897046), permitted merge method, required check names, and auto-merge state.
6. After merge, verify the PR merge commit contains the exact accepted `dev` head as a parent. A green check on a different SHA is not completion evidence.
7. Open the `Publish DSET release` run and verify its local `dset release check` evaluated the exact checked-out merge SHA and the tag is exactly `v<product-semver>`, resolves to that SHA, and has not been reused or retargeted.
8. Verify the GitHub Release targets that tag, reports the canonical product SemVer, and was created by the publication run for the same merge SHA. A tag without a Release or a Release without the correct tag is partial publication.

Use `gh pr view`, `gh pr checks`, `gh run view`, and read-only ruleset/API queries when available. Keep diagnostic output to IDs, conclusions, durations, and concise failure excerpts.

## Containment and recovery

- Convert the PR to draft or close it to stop publication while preserving evidence.
- Rerun a failed job only when evidence indicates a transient GitHub/platform failure. Correct repository failures in a new commit and let checks run against the new SHA.
- Never bypass protected `main`, force-push either protected branch, or weaken the author/head/base policy to unblock one delivery.
- If auto-merge logic is defective, keep the PR draft, correct the workflow through the active DSET change, and require the policy and DSET checks on the corrected head.
- If a ruleset is misconfigured, capture its ID and current JSON, apply the smallest owner-authorized correction, then validate with a draft `dev → main` PR before publication.
- If wrong content reaches `main`, preserve the merge commit and deliver inverse content changes through a reviewed `dev → main` corrective PR with a newly higher version. Do not restore an older version surface, rewrite history, or create a tag collision.
- Publication retry is idempotent: accept an already-correct tag/Release pair, create only the missing object after partial failure, and make no content commit to `main`.
- Stop on an existing tag or Release with a different identity or SHA. Never retarget, delete-and-reuse, or force-update a public release tag.
- Preserve an incorrect published release as evidence and mark it withdrawn/deprecated when GitHub supports the required signal. Deliver a correction through a new `dev → main` PR with a higher version.

## Release publication activation

The repository now contains the guarded `Publish DSET release` workflow and deterministic local `dset release plan`, `check`, and explicit `prepare --execute` transaction. The publisher runs only after a protected `main` push that changed `dset/scopes/meta/version.toml`; it checks the committed declaration, verifies the checkout SHA, creates only missing GitHub objects, and stops on tag identity or SHA collisions without a post-merge content write.

This source implementation is not hosted proof. Until an actual version-changing `dev → main` PR demonstrates the workflow at its merge SHA—including already-correct retry, tag-only and release-only recovery, and collision stops—the hosted publication gate remains pending and no local check may claim that GitHub published a release.

## Data controls

Workflow logs and PR metadata are public repository evidence. Do not print credentials, GitHub tokens, local paths containing private data, or unredacted external payloads. GitHub owns access, retention, deletion, and availability for hosted run logs; DSET stores only bounded links, IDs, conclusions, and synthetic proof. Keep check names and diagnostic cardinality bounded and stable.

## Escalation and traceability

Escalate platform outages to GitHub Status/Support and repository-policy defects to the repository owner. Link every correction to its requirement, DSET change, regression test or eval, PR, and final merge/revert result. Update this runbook when the authoritative workflow, ruleset, check name, or recovery path changes.
