# Methodology OPS domain

This is one layer-owned fragment of the logical methodology package. Use the sibling layer hubs for connected definitions; this file owns only the entities and invariants below.

## Entities

| Entity | Definition |
|---|---|
| **Production supportability contract** | Risk- and topology-scaled agreement for the evidence, correlation and deploy/change identity, safe diagnostics, data controls, runbook, recovery/escalation paths, and incident-to-fix traceability needed to investigate and repair production behavior |
| **Product release** | One coordinated DSET framework and distributable CLI-package identity prepared through the configured integration-to-protected release PR and published from its protected merge commit |
| **Release candidate** | A fully working `1.0.0-rc.N` build whose declared scope and required proof are complete and whose remaining work is release-blocker correction or final validation only |
| **Hosted delivery automation** | GitHub workflows and rulesets that govern the repository's production publication path and use GitHub PR/check/run/commit identities as authoritative operational evidence |
| **Version Scope** | Evergreen specification of the promises, exclusions, and exit criteria for one declared version line |
| **Roadmap** | Evergreen dependency-aware plan from one published baseline to exactly one next-minor Version Scope; milestones are local checkpoint entries, not artifacts |
| **Release Plan** | Evergreen plan for one exact proposed release transition and its participating Changes |
| **Readiness Record** | Exact-candidate gate disposition that records applicability, results, blockers, and evidence and explicitly concludes ready or blocked |
| **Release Record** | Immutable post-publication record of what one exact release delivered and where it was published |

## Invariants

- **DSET-INVARIANT-OPS-001:** Every production-bound tool has an explicit supportability contract scaled to its risk profile and topology; a non-production tool may mark it not applicable only with a reason.
- **DSET-INVARIANT-OPS-002:** Before release, this repository adopts every new capability applicable to its selected profiles; a non-applicable profile-specific capability passes through a versioned in-repository adopter fixture before any external pilot depends on it.
- **DSET-INVARIANT-OPS-003:** Every release PR has one committed bootstrap, normal, small, RC, final, or post-1.0 breaking transition selected by the complete state table; integer-component progression never promotes `0.y.z` to `1.0.0` automatically.
- **DSET-INVARIANT-OPS-004:** Release artifacts are prepared and reviewed before merge; immutable tag and publisher-release identity derive from the configured protected merge commit without a post-merge content mutation.
- **DSET-INVARIANT-OPS-005:** `1.0.0-rc.N` and `1.0.0` represent fully working, evidence-complete gates; schedules, accumulated version increments, or partial scope cannot substitute for readiness.
- **DSET-INVARIANT-OPS-006:** Product, CLI package, release notes, tag, and publisher release share one canonical/equivalent release identity, while schemas, profiles, and template formats retain independent compatibility versions.
- **DSET-INVARIANT-OPS-007:** The Release lifecycle uses exactly five flat peer artifacts—Version Scope, Roadmap, Release Plan, Readiness Record, and Release Record—connected by typed references. Verification never substitutes for Readiness, milestones remain Roadmap entries, and rendered release notes never compete with the immutable Release Record.
