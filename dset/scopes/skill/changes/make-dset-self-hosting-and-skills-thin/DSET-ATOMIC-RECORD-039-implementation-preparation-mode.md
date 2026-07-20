---
artifact_type: atomic_record
artifact_id: DSET-ATOMIC-RECORD-039
type: decision
subtype: requirement
semantic_id: DSET-REQUIREMENT-SKILL-012
status: accepted
priority: high
authority: "operator:anatoly-m-maslennikov"
claim: "Each project selects lazy or strict dset-implement preparation, with lazy as the documented default."
scope:
  kind: project
  id: dset-specs-loops-framework
promotion:
  parent_scope: null
relations:
  - type: replacement_of
    target: DSET-REQUIREMENT-SKILL-010
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
rationale: "One entrypoint should serve operators who want automatic prerequisite closure and automations that require a preparation-free implementation boundary."
---

# Requirement — Select implementation preparation mode

Root `dset.toml` must select `lazy` or `strict` behavior for
`dset-implement`. The default is `lazy`.

In `lazy` mode, `dset-implement` must reconcile accepted session intent into
any missing atomic artifacts, complete separate Test and applicable Evaluation
definitions/plans, complete the implementation plan when needed, and only then
implement. Every prerequisite transition remains progress-bounded and governed
by normal authority and authorization rules.

In `strict` mode, `dset-implement` must not invoke prerequisite workflows or
create, repair, or compile missing authority, QA, or plan artifacts. It may
implement only from the already sufficient accepted inputs. Missing or
ambiguous inputs produce an exact stop rather than an automatic handoff.

Both modes must resolve repository-local governance, preserve run/session and
commit provenance, obey authorization, and stop before claiming Verification
or release readiness.

This Requirement completely replaces `DSET-REQUIREMENT-SKILL-010`.

## Rationale

Lazy preparation keeps the end-user surface simple. Strict preparation gives
automation and expert operators a predictable implementation-only boundary
without creating a second skill or embedding project rules in the wrapper.

This emitted Requirement atom is immutable. Later correction requires a
successor and append-only lifecycle event.
