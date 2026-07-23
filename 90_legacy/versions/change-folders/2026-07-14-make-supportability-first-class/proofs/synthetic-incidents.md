# Synthetic incident fixtures

- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

> Redacted synthetic fixtures carried into the dated archive candidate for [PR #3](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/3).

All names, identifiers, commands, payloads, repositories, people, and records below are fictional. The fixtures contain no production data, secrets, credentials, personal data, or working external links. Repository-qualified PR IDs are deliberately synthetic records used to evaluate traversal; they are not the implementing PR for this DSET change.

## Fixture index

| Incident | Case | Diagnostic entrypoint | Expected owning record |
|---|---|---|---|
| [SYN-INC-001](#syn-inc-001--public-service-failure) | Public service failure | `supportctl diagnose --incident SYN-INC-001 --safe` | `acme/support-demo#417` |
| [SYN-INC-002](#syn-inc-002--retried-asynchronous-effect) | Retried asynchronous effect | `supportctl trace-effect --correlation SYN-CORR-002 --safe` | `acme/support-demo#422` |
| [SYN-INC-003](#syn-inc-003--resumable-local-tool-crash) | Resumable local tool crash | `supportctl local-bundle --run SYN-RUN-003 --safe` | `acme/local-demo#38` |
| [SYN-INC-004](#syn-inc-004--sensitive-support-request) | Sensitive support request | `supportctl diagnose --incident SYN-INC-004 --safe --redaction strict` | `acme/support-demo#429` |
| [SYN-INC-005](#syn-inc-005--llm-quality-regression) | LLM quality regression | `supportctl eval-case --incident SYN-INC-005 --dataset support-quality-v3` | `acme/llm-demo#91` |

## SYN-INC-001 — Public service failure

- **Starting context:** public failure ID `SYN-INC-001`; no internal stack trace is exposed to the caller.
- **Bounded evidence:** `service=checkout`, `operation=create_order`, `correlation_id=SYN-CORR-001`, `deploy_id=checkout-syn-2026.07.14.1`, `outcome=contract_rejected`, `error_class=upstream_contract`; payload values are omitted.
- **Discovery path:** `SYN-INC-001` → deploy `checkout-syn-2026.07.14.1` → commit `syn01a7` → PR `acme/support-demo#417` → DSET change `reject-invalid-upstream-contract` → requirement `ORDER-REQUIREMENT-014` → deterministic proof `ORDER-TEST-PLAN-021` → repair `ORDER-FIX-006`.
- **Safe operator action:** confirm the upstream schema version through the read-only adapter check, stop rollout of the affected deploy, and follow runbook `RB-CHECKOUT-004`; do not log or request the order payload.

## SYN-INC-002 — Retried asynchronous effect

- **Starting context:** customer-visible job ID `SYN-JOB-002` and correlation ID `SYN-CORR-002`; the effect appears duplicated.
- **Bounded evidence:** attempt `3`, effect key `SYN-EFFECT-002`, receiver deduplication result `already_applied`, deploy `worker-syn-2026.07.14.2`, broker message content omitted.
- **Discovery path:** `SYN-CORR-002` → producer attempt → broker delivery → receiver effect/deduplication record → deploy `worker-syn-2026.07.14.2` → commit `syn02b8` → PR `acme/support-demo#422` → DSET change `bound-retried-effects` → requirement `JOB-REQUIREMENT-009` → deterministic proof `JOB-TEST-PLAN-018` → repair `JOB-FIX-004`.
- **Safe operator action:** verify the authoritative receiver state by effect key, pause only the affected consumer partition if the invariant fails, and follow runbook `RB-JOBS-007`; do not replay blindly.

## SYN-INC-003 — Resumable local tool crash

- **Starting context:** local run ID `SYN-RUN-003`; the tool stopped after partially processing a declared file manifest.
- **Bounded evidence:** manifest hash `syn-manifest-003`, checkpoint `row=418`, last durable output `row=417`, local build ID `local-syn-2026.07.14.3`; filenames and row contents omitted.
- **Discovery path:** `SYN-RUN-003` → local diagnostic bundle → build `local-syn-2026.07.14.3` → commit `syn03c4` → PR `acme/local-demo#38` → DSET change `resume-after-atomic-checkpoint` → requirement `LOCAL-REQUIREMENT-005` → deterministic proof `LOCAL-TEST-PLAN-012` → repair `LOCAL-FIX-002`.
- **Safe operator action:** copy the bounded redacted bundle, verify the manifest hash and checkpoint against the authoritative local files, then resume from row 418 using runbook `RB-LOCAL-002`; no centralized tracing service is required.

## SYN-INC-004 — Sensitive support request

- **Starting context:** incident ID `SYN-INC-004`; the report concerns a private account, but no account content is required for diagnosis.
- **Bounded evidence:** pseudonymous subject `SYN-SUBJECT-HMAC-004`, policy result `access_denied`, rule version `policy-syn-44`, deploy `auth-syn-2026.07.14.4`; raw identifier, token, request body, and personal attributes are prohibited.
- **Discovery path:** `SYN-INC-004` → audited read-only diagnostic access → deploy `auth-syn-2026.07.14.4` → commit `syn04d9` → PR `acme/support-demo#429` → DSET change `redact-auth-diagnostics` → requirement `AUTH-REQUIREMENT-022` → deterministic proofs `AUTH-TEST-PLAN-031` and `AUTH-TEST-PLAN-032` → repair `AUTH-FIX-011`.
- **Safe operator action:** use strict-redaction mode, confirm the policy rule and deploy identity, escalate through runbook `RB-AUTH-009`, and refuse requests for credentials, tokens, raw identifiers, or unrelated personal data.

## SYN-INC-005 — LLM quality regression

- **Starting context:** incident ID `SYN-INC-005`; transport, parsing, schema validation, and deterministic guardrails pass, but answer quality has degraded.
- **Bounded evidence:** model profile `support-model-syn-v5`, prompt version `support-prompt-syn-18`, dataset case `support-quality-v3/case-044`, rubric dimensions `relevance` and `safe_escalation`; the user prompt and model response are replaced by approved synthetic text.
- **Discovery path:** `SYN-INC-005` → model/prompt deploy identity → commit `syn05e2` → PR `acme/llm-demo#91` → DSET change `restore-support-answer-quality` → requirement `LLM-REQUIREMENT-017` → deterministic proof `LLM-TEST-PLAN-026` for transport/schema and qualitative proof `LLM-EVAL-PLAN-014` for response quality → repair `LLM-FIX-008`.
- **Safe operator action:** keep deterministic safety gates active, route the synthetic case through the approved eval dataset, compare the rubric result with the last accepted prompt/model profile, and follow rollback runbook `RB-LLM-006` if the threshold fails.

## Expected classification

- Field/schema validation, correlation propagation, identity presence, receiver deduplication behavior, diagnostic permissions, redaction, retention, and bounds are deterministic tests.
- Whether an unfamiliar operator can diagnose the likely boundary, choose a safe action, and follow the incident-to-fix chain is a qualitative eval.
