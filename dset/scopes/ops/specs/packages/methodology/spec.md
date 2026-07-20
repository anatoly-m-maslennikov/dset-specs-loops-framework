# Methodology OPS specification

## Active Decision source compilation

### DSET-DECISION-OPS-006 — Flat Delivery lifecycle roles

The Decision compiles as six flat peer roles under the primary Delivery
artifact type: Roadmap, Version Scope, Change, Release Plan, Readiness Record,
and Release Record. Milestone remains a Roadmap entry. Release Record combines
delivered summary and publication identity. The absorbed OPS Decisions remain
immutable history and do not participate in active compilation.

## DSET-REQUIREMENT-OPS-001 — Production supportability is explicit and risk-scaled

Every production-bound tool must define a supportability contract appropriate to its runtime risk profile and deployment topology. The contract covers incident triggers or objectives; operator-usable evidence; end-to-end correlation and deploy/change identity; safe read-only diagnostics and permissions; retention, redaction, access, deletion, volume, cardinality, and sampling bounds; runbook, escalation, rollback or kill-switch paths; and traceability from an incident to governing requirements, changes, PRs, and fixes. Telemetry is diagnostic evidence, not a competing business-state authority. A non-production tool may mark the contract not applicable only with a reason.

**Scenario DSET-SCENARIO-OPS-001:** A production-bound local tool uses bounded structured local diagnostic records and run/build identity appropriate to its risk without being forced to deploy a tracing backend; a non-production one-shot tool records a justified not-applicable disposition.

**Scenario DSET-SCENARIO-OPS-002:** A distributed, stateful, retryable, or high-risk service propagates correlation and deploy/change identity across relevant effect boundaries, provides safe bounded diagnostics and incident runbooks, and adds tracing, audited access, rollback, or stronger redaction when its topology and profile require them.

## DSET-REQUIREMENT-OPS-002 — Repository delivery is supportable

The GitHub-hosted delivery path must document incident triggers, authoritative PR/check/run/ruleset/commit evidence, safe diagnostics, data controls, containment, recovery, escalation, and change-to-fix traceability. Hosted state remains authoritative; local files do not add a competing delivery-state store.

**Scenario DSET-SCENARIO-OPS-003:** An operator can diagnose a blocked or incorrect `dev → main` delivery, contain it by preserving the draft/PR evidence, and recover without bypassing protected `main` or rewriting history.

## DSET-REQUIREMENT-OPS-003 — DSET 0.3 release is framework-first

A DSET 0.3 capability must not be released until this repository adopts it under every applicable selected profile. When a profile-specific capability is not applicable to this repository, a versioned in-repository adopter fixture must pass before an external pilot may depend on it.

**Scenario DSET-SCENARIO-OPS-004:** A TypeScript-only gate is not applied to Python sources, but its versioned adopter fixture passes before the gate is presented to Your Harness as released DSET behavior.

## DSET-REQUIREMENT-OPS-004 — Every protected release PR has one deterministic transition

After policy activation, every configured integration-to-protected release-branch PR must contain exactly one committed release declaration in one release-owning Change; any other participating Changes contain only a reference to that owner. Omission, multiple declarations, and dangling/cyclic references fail preparation and cannot classify the PR as non-release. The declaration records protected base ref/SHA/version, candidate SHA, target, readiness owner, and exactly one class. `DSET-RULE-RELEASE` owns the complete bootstrap/pre-1.0/RC/final/post-1.0 table, highest-impact aggregation, ambiguity stop, integer arithmetic, and immutable published-RC progression.

**Scenario DSET-SCENARIO-OPS-005:** `0.2.4` becomes `0.3.0` for a normal PR or `0.2.5` for a small PR; `0.9.0` becomes `0.10.0`, never `1.0.0`.

## DSET-REQUIREMENT-OPS-005 — Release authority is configured and idempotent

Each applicable project must configure an integration branch, protected release branch, publisher, and tag pattern containing one `{product_version}` placeholder. One committed declaration is authoritative for class, protected-base ref/SHA/version, candidate SHA, target, and readiness artifact; version files, package metadata, notes, PR text, rendered tag, and publisher release are mirrors. Preparation reads the protected base once, rejects drift, and is idempotent. Interactive `dset-release` prepares/verifies; authorized post-merge automation publishes at the exact merge SHA. Retry creates only missing objects, accepts exact matches, and stops on collision. Published tags are immutable; bad releases are preserved/withdrawn and corrected by a higher-version PR without a post-merge content commit.

**Scenario DSET-SCENARIO-OPS-006:** A PR with mismatched product/package targets fails before merge; a passing merge is tagged at its exact merge commit without modifying `main` files afterward.

## DSET-REQUIREMENT-OPS-006 — RC and final releases are fully working gates

`1.0.0-rc.N` may begin only when the declared 1.0 scope is feature-complete, self-hosted, documented, supportable, migration-ready, green under every deterministic test and applicable eval, verified in required adopters or pilots, and free of known release-blocking defects. The change's committed Readiness Record, anchored to the exact candidate SHA, owns applicable/not-applicable gate dispositions, evidence links, the blocker register, and the explicit ready-or-blocked conclusion. `verification.md` is linked assurance evidence and cannot authorize release. Final promotion allows only release metadata/evidence-link updates; any substantive change requires `rc.N+1` and fresh proof. Time or accumulated increments cannot replace readiness.

**Scenario DSET-SCENARIO-OPS-007:** A green candidate with one required pilot unfinished remains `0.y.z`; a fully working `1.0.0-rc.2` may promote to `1.0.0` only after final evidence passes and without adding features.

## DSET-REQUIREMENT-OPS-007 — Product/package identity is coordinated

The framework product version, CLI package version, release notes, rendered Git tag, and publisher release must carry equivalent release identity. Product identity is canonical SemVer; Python maps every `MAJOR.MINOR.PATCH-rc.N` to PEP 440 `MAJOR.MINOR.PATCHrcN`, and no other mismatch is accepted. Committed files express prepared identity; live tag/release state at the protected merge SHA proves publication. Schema, governance-profile, language-profile, artifact-profile, and template-format versions remain independent compatibility surfaces.

**Scenario DSET-SCENARIO-OPS-008:** Product/package `0.3.0` may validly use schema `1.0` and governance profile `core-v1@0.2`; neither compatibility version implies DSET 1.0 readiness.

## DSET-REQUIREMENT-OPS-013 — Release lifecycle artifacts are flat and typed

Every release-applicable project must represent release planning, bounded work,
gates, and history with six peer roles under the primary Delivery artifact
type: Roadmap, Version Scope, Change, Release Plan, Readiness Record, and
Release Record. Roadmap targets one next-minor Version Scope and owns milestone
entries; Version Scope defines one version line; Change groups one bounded
delivery; Release Plan selects one exact transition and its Changes; Readiness
Record owns the explicit ready-or-blocked disposition for one exact candidate;
and Release Record immutably owns both the delivered summary and publication
identity. Applicable artifacts use typed references rather than containment or
copied obligations. Verification may support a Readiness Record but cannot
authorize release. Forge notes and changelogs are mirrors or derived views of
Release Records.

**Scenario DSET-SCENARIO-OPS-014:** A `0.4.0` candidate references its `0.4`
Version Scope and exact Release Plan. Passing Tests, Evals, and Verification are
linked evidence, but the candidate remains blocked until its Readiness Record
explicitly says ready. After publication, one immutable Release Record binds
the scope, plan, readiness record, protected merge SHA, tag, packages, forge
identity, migration notes, and user-visible summary.
