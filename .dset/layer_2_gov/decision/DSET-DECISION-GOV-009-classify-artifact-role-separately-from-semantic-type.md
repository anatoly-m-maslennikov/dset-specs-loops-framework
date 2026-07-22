# Decision — Classify artifact role separately from semantic Type

- **Decision ID:** `DSET-DECISION-GOV-009`
- **Status:** accepted
- **Decision date:** 2026-07-20
- **Selected option:** add one independent `artifact_type` and optional direct
  `artifact_subtype` axis while retaining the four semantic Types unchanged
- **Priority:** unknown pending the registered core-v1 scale
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Classification axes

`artifact_type` answers what primary job a carrier performs in the development
system. The existing semantic `type` and `subtype` answer what an atomic claim
or directive means. Neither axis is inferred from the other.

An atomic carrier therefore uses both axes:

```yaml
artifact_type: atomic_record
type: decision
subtype: requirement
```

A non-atomic document uses only the artifact axis unless it embeds separately
identified atoms:

```yaml
artifact_type: analysis_report
artifact_subtype: solution_landscape
```

Every governed artifact has exactly one primary `artifact_type` and at most one
allowed direct `artifact_subtype`. Artifact subtypes do not contain other
artifact subtypes. A physical carrier may expose linked records or projections,
but proximity does not merge their roles or transfer authority.

## Canonical artifact types

| Artifact type | Allowed direct artifact subtypes |
|---|---|
| `atomic_record` | None; semantic `type` and `subtype` classify its atom |
| `analysis_report` | `solution_landscape`, `root_cause_analysis`, `proposal`, `technical_investigation`, `external_audit_analysis`, or omitted for a general analysis |
| `specification` | `domain_model`, `behavior`, `architecture`, `design`, `governance`, `version_scope`, or omitted for a general specification |
| `procedure` | `playbook`, `runbook`, or omitted for a general reusable procedure |
| `plan` | `roadmap`, `implementation_plan`, `test_plan`, `evaluation_plan`, `release_plan`, or omitted for a general plan |
| `change` | None |
| `implementation` | `source_code`, `documentation`, `configuration`, `migration`, `test_implementation`, `evaluation_implementation`, or omitted for a mixed implementation |
| `evidence_record` | `test_result`, `evaluation_result`, `review_report`, `run_record`, or omitted for general evidence |
| `verification` | None |
| `readiness_record` | None |
| `release_record` | None |
| `derived_view` | `project_overview`, `health_dashboard`, `traceability_index`, `changelog`, or omitted for another declared derived view |
| `navigation` | `readme`, `hub`, `index`, or omitted for another navigation surface |

The catalog is complete for DSET's development scope. Sales, customer-success
management, performed production support, and operation of deployment
infrastructure are outside it. Their outputs may enter as operator input or
external evidence. Developing supportability behavior and documentation remains
implementation work when accepted project authority requires it.

## Analysis Report boundaries

Analysis Report is the newly admitted artifact type. It interprets information
without becoming authority merely by existing:

- Solution Landscape compares multiple live approaches without selecting one;
- Root-Cause Analysis supports a cause for an observed Problem;
- Proposal recommends one candidate without accepting it;
- Technical Investigation establishes technical facts, mechanisms, or
  feasibility without requiring a causal conclusion; and
- External Audit Analysis interprets and triages an external audit while the
  source audit remains external evidence.

An accepted conclusion is emitted separately as a Decision, Question, Problem,
or QA atom. An observation remains an Evidence Record. When no subtype owns the
analysis precisely, omit `artifact_subtype` rather than guessing or nesting.

## Development boundaries

- Specification describes current or required truth; Plan describes intended
  work.
- Procedure describes a reusable way of working; Plan describes one intended
  enactment.
- A proposed Design is an Analysis Report/Proposal; accepted current Design is
  a Specification/Design.
- Implementation realizes accepted truth; Evidence Record records an observed
  result.
- Verification assesses what evidence supports without authorizing release.
- Readiness Record contains the explicit ready-or-blocked gate disposition for
  an exact candidate; a checklist or green display is not that disposition.
- Release Record immutably records what exact version was published and where.
- Derived View and Navigation never become authority.

## Release lifecycle projection

The five final Release lifecycle artifacts remain flat and independently
addressable:

- Version Scope is `specification/version_scope`;
- Roadmap is `plan/roadmap` and contains milestone entries;
- Release Plan is `plan/release_plan`;
- Readiness Record is `readiness_record`; and
- Release Record is `release_record` and owns both the release summary and
  publication identity.

This artifact classification creates no parent/child lifecycle hierarchy.
Applicable records use explicit references such as `version_scope_ref`.
Forge-facing release notes and changelogs are rendered mirrors or derived views
of Release Records, not competing canonical artifacts.

## Registration and enforcement

DSET must publish one machine-readable artifact-type registry, schema, and
project-local materialized template. The registry owns type/subtype vocabulary,
fallback behavior, primary questions, and classification boundaries without
restating semantic Type definitions.

The selected artifact profile must validate registry structure, unknown types,
unknown or nested subtypes, and subtype/type mismatches with stable diagnostics.
Repository-owned canonical artifacts must be classified directly or through one
unambiguous registered path rule. Generated output exposes the effective
classification and its source without becoming authority.

Existing carriers keep their identities. Classification adds metadata and
does not edit immutable atom content, reinterpret history, or turn a document
role into a semantic Type.

## Rationale

The previous four-role model—atomic authority, evergreen projection,
transactional context/evidence, and implementation—was useful for authority but
too coarse for a collectively exhaustive development description. It collapsed
analysis with evidence, procedure with plan, verification with gates, and
publication with history.

Two orthogonal axes avoid the opposite error. The four semantic Types remain a
small stable claim taxonomy, while artifact types describe the distinct jobs
performed by specifications, plans, implementation, evidence, gates,
publication, derived views, and navigation. One primary question per artifact
keeps the catalog mutually exclusive; the catalog and fallback rules make the
development scope collectively exhaustive.

## Lifecycle policy at emission

- **Expected confirmation evidence:** schema and fixture tests reject unknown,
  mismatched, or multiply classified artifacts; cold reviewers consistently
  separate Analysis Report, Evidence Record, Verification, and Readiness Record
- **Known counter-evidence:** full semantic atom migration remains separately
  open under `DSET-PROBLEM-GOV-007` and `DSET-TASK-GOV-049`
- **Reopen when:** a development artifact cannot be assigned one primary type
  without merging distinct authority, work, evidence, gate, or publication
  claims
- **If reopened, retain:** semantic and artifact axes remain separate, one
  primary claim/role per artifact, no subtype nesting, and workflow never
  determines classification
- **Retirement condition:** an accepted successor absorbs every active claim

This emitted Decision atom is immutable. Any later correction, status change,
counter-evidence, absorption, or retirement must be a new atom or append-only
lifecycle event.
