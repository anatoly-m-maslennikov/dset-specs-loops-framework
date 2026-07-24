---
artifact_type: "evaluation_plan"
artifact_id: "DSET-EVAL-PLAN-GOV-034"
scope_path:
  - "layer:gov"
priority: "medium"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "check_of"
    targets:
      - "DSET-REQUIREMENT-GOV-045"
---

# Evaluation Plan — Distinguish features from layers

Given a project with two interacting features and the five DSET layers, a cold
reviewer should explain that:

- features are peer capabilities connected by horizontal Contracts;
- layers refine authority only in the META → GOV → TOOL → SKILL → OPS
  direction;
- an adjacent-layer connection is preferred; and
- a downstream reference to upstream truth is consumption, not backward
  governance; and
- irreducible backward coupling is a signal to propose feature reclassification,
  not to normalize a dirty layer graph.

Record confusion between call direction, delivery order, dependency edges,
feature ownership, and layer authority. This Evaluation atom is immutable;
later correction requires a successor Evaluation and append-only lifecycle
event.

## Primary claim

A reviewer can distinguish horizontal feature Contracts from forward-only layer authority and recognize adjacent layer influence as the preferred design.
