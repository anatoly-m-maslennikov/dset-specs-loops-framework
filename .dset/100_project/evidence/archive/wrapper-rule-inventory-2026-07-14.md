# Wrapper rule inventory — 2026-07-14

- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Subject

- Pre-refactor wrapper tree: `3b47daffca4c4cfae51d0bf9eb0509cd95280eb7`
- Thin-wrapper commit: `e9ebe845f8d9659104a2851e54b3641b0106ca85`
- Canonical local registry: `dset/governance.yaml`
- Source profile: `core-v1@0.2`

The inventory groups semantically equivalent statements so every normative
statement in the three former skill bodies has one registered owner. Trigger
metadata remains in the wrapper; substantive rules moved to the owners below.

## Former `dset-grill` (`dset-clarify` in the 0.2 candidate)

| Former statement group | Governing owner |
|---|---|
| Repository/change discovery, selected authority, and fail-closed bootstrap | `DSET-RULE-ARCHITECTURE` |
| Facts/decisions/assumptions/unknowns; vocabulary; actors; entities; value objects; ownership; lifecycle state machines; invariants; boundary cases; material questions; what/why separation; requirement/scenario IDs; stop before unresolved domain choices | `DSET-RULE-DOMAIN-SPEC` |
| Exact proof belongs to deterministic tests | `DSET-RULE-TEST-PLAN` |
| Variable or rubric-based proof belongs to evals | `DSET-RULE-EVAL-PLAN` |
| Authorized artifact writes, Decision routing, single-owner output, and implementation handoff | `DSET-RULE-ARTIFACT-MAINTENANCE` |
| Run the selected validation gate after authorized writes | `DSET-RULE-BUILD` |

## `dset-diagnose`

| Former statement group | Governing owner |
|---|---|
| Accepted/current authority discovery and state-owner boundaries | `DSET-RULE-ARCHITECTURE` |
| Reproduce, minimize, separate environment failures, form competing hypotheses, gather discriminating evidence, find the first bad change, trace Back-to-Left provenance, classify upstream artifacts, report inference honestly, contain, and stop at an evidence/authorization boundary | `DSET-RULE-DIAGNOSIS` |
| Exact regression proof | `DSET-RULE-TEST-PLAN` |
| Variable baseline and threshold proof | `DSET-RULE-EVAL-PLAN` |
| Bounded/redacted diagnostics, build/deploy identity, access, retention, volume, and production-effect safety | `DSET-RULE-SUPPORTABILITY` |
| Write authorization, owning defect artifacts, and fix handoff | `DSET-RULE-ARTIFACT-MAINTENANCE` |

## `dset-prototype`

| Former statement group | Governing owner |
|---|---|
| Selected requirements, constraints, candidates, and repository authority | `DSET-RULE-ARCHITECTURE` |
| Falsifiable hypothesis, timebox, representative cases, comparable candidate evidence, provenance/license, cost/lock-in, adopt/adapt/build/defer decision, disposal, promotion, and stop conditions | `DSET-RULE-PROTOTYPING` |
| Exact candidate thresholds and cases | `DSET-RULE-TEST-PLAN` |
| Variable or rubric-based candidate thresholds | `DSET-RULE-EVAL-PLAN` |
| External access, data class, security/privacy, and operational evidence bounds | `DSET-RULE-SUPPORTABILITY` |
| Bounded proof placement, solution/Decision links, quarantine/removal, and production handoff | `DSET-RULE-ARTIFACT-MAINTENANCE` |

## Retained wrapper-owned fields

Each current wrapper owns only its name/trigger, repository-root discovery,
workflow ID, resolver invocation, resolved-ruleset reporting, authorization
handoff, output handoff, and fail-closed stop behavior. The registered wrapper
digests and deterministic tests reject drift from those canonical sources.

## Disposition

Complete for roadmap tasks `DSET-TASK-SKILL-005`–`DSET-TASK-SKILL-012`. No former
substantive workflow statement remains authoritative in a skill, installed
copy, template, or generated adopter wrapper.
