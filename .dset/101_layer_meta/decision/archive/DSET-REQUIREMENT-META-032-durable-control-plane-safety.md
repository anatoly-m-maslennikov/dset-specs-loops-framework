---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-META-032"
scope_path:
  - "layer:meta"
priority: "high"
promotion:
  affected_children:
    - "governance"
    - "tool"
    - "skill"
    - "implementation"
    - "operations"
  applies_unchanged: true
  local_context_required: false
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "relates_to"
    targets:
      - "DSET-REQUIREMENT-META-021"
      - "DSET-REQUIREMENT-META-022"
---

# Requirement — Protect the durable control plane

The durable DSET control plane contains accepted current project truth only.

- Passwords, API keys, tokens, private keys, and comparable secrets never enter
  DSET artifacts, settings, logs, evidence, generated views, or commits.
  Durable artifacts may name runtime lookup keys without storing their values.
- Methodology semantics and project authority remain independent of Codex,
  Claude, Grok, or any other LLM provider. Provider adapters are downstream
  mechanisms.
- Requirements and Decisions describe current work. Future intentions remain
  in Version Roadmaps until accepted into current atomic authority.
- Exploration Mode emits no governed artifact until explicit operator
  acceptance.

GOV, TOOL, SKILL, IMPL, and OPS own the concrete storage, lookup, adapter,
redaction, and enforcement mechanisms without weakening this boundary.

## Primary claim

The durable DSET control plane admits only accepted current project truth, excludes secrets, remains LLM-provider agnostic, and keeps future intentions and unaccepted exploration outside current authority.

## Rationale

One universal admissibility boundary prevents security leakage, provider lock-in, roadmap confusion, and exploratory candidates from contaminating current governed truth.
