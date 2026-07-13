# Test plan — Supportability contract

> Archive candidate in [PR #3](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/3).

## Deterministic checks

| Test ID | Requirement | Proof |
|---|---|---|
| **SUP-TEST-001** | SUP-REQ-001 | Assert exact active display name, subtitle, expansion, project ID, and repository slug; reject stale active identity outside archived history |
| **SUP-TEST-002** | SUP-REQ-002 | Assert spec, implementation-plan, code-rule, and gate documents expose the required supportability-contract fields |
| **SUP-TEST-003** | SUP-REQ-003 | Assert the documented incident chain reaches version, PR, DSET change, requirement, test/eval, and repair evidence |
| **SUP-TEST-004** | SUP-REQ-004 | Assert secret/PII redaction, retention/access, cardinality/sampling, volume/cost, and authority boundaries are explicit |
| **SUP-TEST-005** | SUP-REQ-005 | Assert local-tool, service, and distributed-workflow examples choose different applicable mechanisms without a vendor mandate |
| **SUP-TEST-006** | SUP-REQ-006 | Assert deterministic support checks remain in test plans and operator-usability judgments remain in eval plans |
| **SUP-TEST-007** | All | Resolve Markdown links, parse YAML, balance fences/details, reject unsupported Markdown, and run `git diff --check` |

## Regression rule

Every supportability defect that is mechanically detectable must add a failing deterministic check. Incident evidence must be redacted before it is committed under `proofs/`.
