# Solution landscape — Supportability

> Archive candidate in [PR #3](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/3).

## Candidates

| Candidate | Fit | Decision |
|---|---|---|
| Rename only | Memorable identity but no operational behavior | Reject |
| “Log everything” | Easy to state; unsafe, noisy, and unbounded | Reject |
| Vendor-specific telemetry stack | Executable for one deployment but violates framework portability | Reject as framework truth; allow in applied project profiles |
| Language- and vendor-neutral supportability contract with profile-applied adapters | Stable questions, identity, safety, and proof requirements with proportional implementations | **Adopt** |
| Ninth standard `support-plan.md` artifact | Makes support visible but breaks the eight-document change contract and duplicates spec/implementation/verification ownership | Reject; add explicit supportability sections to existing owners |

## Decision

Adopt one cross-cutting supportability contract. Domain/spec owns operator questions, identifiers, and data policy; the test/eval plans own separate proof; the implementation plan owns instrumentation sequence and rollout; general rules own runtime patterns; gates own enforcement; verification links redacted evidence.
