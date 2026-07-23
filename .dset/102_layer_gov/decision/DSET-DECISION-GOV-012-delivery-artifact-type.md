+++
artifact_id = "DSET-ATOMIC-RECORD-033"
semantic_id = "DSET-DECISION-GOV-012"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Delivery is the canonical artifact type for the six release-lifecycle roles."
promotion = {}
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Decision — Use Delivery for the release lifecycle

DSET keeps semantic Type and carrier `artifact_type` as independent axes. Every
governed carrier has exactly one primary artifact type and at most one direct
artifact subtype. Semantic atoms separately use exactly one semantic Type and
at most one direct semantic subtype. Neither axis is inferred from the other,
and neither permits nested subtypes.

The canonical development artifact types are:

| Artifact type | Allowed direct artifact subtypes |
|---|---|
| `atomic_record` | None; semantic `type` and `subtype` classify its atom |
| `analysis_report` | `solution_landscape`, `root_cause_analysis`, `proposal`, `technical_investigation`, `external_audit_analysis`, or omitted |
| `specification` | `domain_model`, `behavior`, `architecture`, `design`, `governance`, or omitted |
| `procedure` | `playbook`, `runbook`, or omitted |
| `plan` | `implementation_plan`, `test_plan`, `evaluation_plan`, or omitted |
| `delivery` | `roadmap`, `version_scope`, `change`, `release_plan`, `readiness_record`, `release_record`, or omitted |
| `implementation` | `source_code`, `documentation`, `configuration`, `migration`, `test_implementation`, `evaluation_implementation`, or omitted |
| `evidence_record` | `test_result`, `evaluation_result`, `review_report`, `run_record`, or omitted |
| `verification` | None |
| `derived_view` | `project_overview`, `health_dashboard`, `traceability_index`, `changelog`, or omitted |
| `navigation` | `readme`, `hub`, `index`, or omitted |

`delivery` owns bounded delivery intent, transaction, gate, and publication
records. Roadmap orders the route toward a version line. Version Scope defines
its promise, exclusions, and exit criteria. Change groups accepted work and
evidence. Release Plan selects an exact candidate. Readiness Record owns the
ready-or-blocked disposition. Release Record immutably records publication.

All six subtypes share one project-wide `DELIVERY` identity sequence for newly
emitted carriers. Default IDs and filenames include only the primary type token,
for example `APP-DELIVERY-001-0-4-core.md`. Explicit subtype-bearing naming may
add the direct subtype token to new artifacts; it never renames an immutable
atom or another already stable identity.

Analysis Report remains non-authoritative interpretation. Specification
compiles current or required truth. Plan describes intended implementation,
Test, or Evaluation work. Procedure describes a reusable method. Implementation
realizes accepted truth or QA definitions. Evidence Record records an
observation. Verification assesses evidence without authorizing release.
Derived View and Navigation remain non-authoritative.

The catalog covers development and release handoff, not sales,
customer-success management, performed production support, or operation of
deployment infrastructure. External work may supply operator input or
evidence; developing supportability behavior or documentation remains
Implementation.

This Decision absorbs `DSET-DECISION-GOV-011` in full and, transitively, its
absorbed `DSET-DECISION-GOV-009` predecessor. It preserves the complete catalog
and all consequences of `DSET-DECISION-GOV-011` while removing the invalid
lineage edge that treated absorption as parentage. Replacement remains owned by
append-only lifecycle events.

## Rationale

The six records form one coherent delivery lifecycle but retain distinct jobs.
A plain-language shared type makes that purpose visible, while flat direct
subtypes prevent lifecycle order from becoming semantic hierarchy.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle event.
