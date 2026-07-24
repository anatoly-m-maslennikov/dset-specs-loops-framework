+++
artifact_id = "DSET-ATOMIC-RECORD-031"
semantic_id = "DSET-DECISION-GOV-011"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Delivery is the canonical artifact type for the six release-lifecycle roles."
promotion = {}
child_of = ["DSET-DECISION-GOV-009"]
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

`delivery` answers: what bounded delivery intent, transaction, gate, or
publication record does this artifact own? Its six direct subtypes have these
boundaries:

- `roadmap` orders the mutable route toward a version line;
- `version_scope` defines the promise, exclusions, and exit criteria of a
  version line;
- `change` groups accepted work and evidence for one bounded delivery;
- `release_plan` selects one exact candidate and its participating Changes;
- `readiness_record` owns the explicit ready-or-blocked disposition for one
  exact candidate; and
- `release_record` immutably records what exact version was published and
  where.

All six subtypes share one project-wide `DELIVERY` identity sequence. Default
IDs and filenames include only the primary type token, for example
`APP-DELIVERY-001-0-4-core.md`. Projects that explicitly enable subtype-bearing
names may add the direct subtype token to newly emitted artifacts. The setting
never renames an immutable atom or an already stable artifact identity.

The other artifact-role boundaries remain unchanged. Analysis Report interprets
information without authorizing a choice. Specification compiles current or
required truth. Plan describes intended implementation, Test, or Evaluation
work. Procedure describes a reusable method. Implementation realizes accepted
truth or QA definitions. Evidence Record records an observation. Verification
assesses evidence without authorizing release. Derived View and Navigation are
non-authoritative projections or routing surfaces.

The catalog covers development and release handoff. Sales, customer-success
management, performed production support, and operation of deployment
infrastructure remain outside it. External work may supply operator input or
evidence; developing required supportability behavior or documentation remains
Implementation.

This Decision absorbs `DSET-DECISION-GOV-009`. It carries forward that
Decision's independent-axis model, one-role rule, Analysis Report boundaries,
development boundary, registration and enforcement requirements, and naming
policy. It replaces only the catalog structure and release-lifecycle
classification: the former top-level `change`, `readiness_record`, and
`release_record` roles and the former `specification/version_scope`,
`plan/roadmap`, and `plan/release_plan` roles become the six direct `delivery`
subtypes above.

## Rationale

The six records form one coherent delivery lifecycle but were previously split
across unrelated carrier types. A single plain-language type makes their shared
purpose visible while direct subtypes retain precise roles. It also gives the
project one readable sequence for release-lifecycle artifacts without turning
the lifecycle into a semantic hierarchy.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle event.
