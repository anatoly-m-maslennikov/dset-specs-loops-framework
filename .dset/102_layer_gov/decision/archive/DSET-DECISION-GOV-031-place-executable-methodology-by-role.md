---
artifact_type: "implementation_decision"
artifact_id: "DSET-DECISION-GOV-031"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "replacement_of"
    targets:
      - "DSET-DECISION-GOV-030"
  - type: "child_of"
    targets:
      - "DSET-DECISION-GOV-022"
---

# Decision — Place executable methodology by semantic role

DSET uses the ordered flow `META → GOV → TOOL → SKILL → IMPL → OPS`.

TOOL owns the DSET executable product contract: CLI behavior, schemas,
templates, fixtures, validation and diagnostics, traceability, lifecycle
mechanics, and self-hosting behavior.

SKILL owns agent-facing orchestration over those executable contracts.

IMPL owns development realization: environment and dependency setup,
production code, automated Test code, Evaluation implementations, code-focused
quality gates, and concrete implementation profiles. Installed methodology
therefore materializes the repository Python package under IMPL `100_python`,
the deterministic Test package under IMPL `110_tests`, and reusable Evaluation
prompts under IMPL `120_evaluations`.

OPS owns what follows implementation: CI delivery, release and publication,
runtime operation and investigation, containment, recovery, escalation, and
hosted evidence. An operational deficiency creates or updates upstream
authority for a later implementation; OPS does not directly rewrite IMPL.

Applied QA definitions, plans, evidence, and Verification remain with their
project or layer owners. Installed reusable implementations do not become
project results or assurance.

This Decision completely replaces `DSET-DECISION-GOV-030`. The prior atom
remains immutable history; current evergreen truth compiles this separation.

## Primary claim

Installed methodology separates the DSET executable contract in TOOL from development environments and implementations in IMPL, while OPS owns only post-implementation operation and delivery.

## Rationale

Executable behavior, implementation technique, and post-implementation operation are different owners; separating them removes backward OPS-to-IMPL authority and makes recursive self-hosting inspectable.
