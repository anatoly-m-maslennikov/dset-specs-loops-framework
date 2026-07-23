# Eval plan — Supportability usability

> Archive candidate in [PR #3](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/3).

## Applicability

Applicable. Signal presence is deterministic, but whether a new operator can use bounded evidence to investigate a real incident is qualitative.

## Cases

1. A deployed service returns a public failure ID for an internal error.
2. An asynchronous retried effect appears missing or duplicated.
3. A resumable local tool crashes after partially processing files.
4. A support request involves sensitive user data that must not enter evidence.
5. An LLM-mediated feature degrades qualitatively without a deterministic parser failure.

## Criteria

| Eval ID | Criterion | Threshold |
|---|---|---|
| **DSET-EVAL-PLAN-OPS-001** | Findability | Every reviewer locates the supportability contract and diagnostic entrypoint for all five cases |
| **DSET-EVAL-PLAN-OPS-002** | Incident traceability | Every reviewer reaches the responsible version/change and relevant test or eval evidence from the supplied incident context |
| **DSET-EVAL-PLAN-OPS-003** | Proportionality | No reviewer adds distributed telemetry to the simple local case or omits cross-boundary correlation from the asynchronous case |
| **DSET-EVAL-PLAN-OPS-004** | Safety | No reviewer requires secrets or unnecessary personal data to complete an investigation |
| **DSET-EVAL-PLAN-META-001** | Proof separation | Reviewers classify schema/redaction checks as tests and operator investigation quality as evals |

## Evidence

Use independent reviewers and redacted synthetic incidents. Record discovery paths, disagreements, time-to-owning-change, missing evidence, and corrective artifact in `proofs/`; summarize conclusions in `verification.md`.
