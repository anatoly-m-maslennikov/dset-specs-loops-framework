# Delegation budget rules

## Quality and scope floor

Budget changes resource breadth, not the accepted outcome, safety boundary, or
required proof. If a profile cannot complete the requested scope at the
required quality, stop and report the shortfall; do not silently reduce scope.

## Model and effort inheritance

Subagents request the main session's model family/version and reasoning effort
by default. Before spawning, discover whether the runtime can request and
attest those fields. Record requested and effective values with one of
`confirmed`, `runtime-default-unverified`, or `unsupported`. A known mismatch is
an override and must be reported before spawning. When exact configuration is a
declared proof or safety precondition, unsupported or unverified inheritance
stops for an operator/project decision; otherwise it may continue only with the
uncertainty visible in the run record.

## Profiles

| Profile | Unique subagents in the whole tree | Maximum depth | Rounds | Breadth and stop rule |
|---|---:|---:|---:|---|
| `low` | 0–1 | 1 | 1 | One necessary role and minimum sufficient optional exploration; all required tests/evals remain |
| `medium` (default) | Target 2, maximum 3 | 1 | 2 | Independent useful roles plus one reconciliation/re-review round; use zero or one only when no second independent role adds value |
| `high` | 4–6 | 2 | 3 | Distinct implementation/review/eval or adversarial roles, broader task-relevant context, and up to two challenge rounds |

Runtime capacity may reduce actual fan-out but never changes the profile's
quality floor. Every planned/actual difference is recorded. Agents with
duplicate roles or no independently useful output do not count toward fan-out.
One root budget is propagated through the delegation tree; a child cannot reset
the remaining-agent, depth, or round counters. Operator instruction overrides
the selected project profile. The discovered project manifest selects the
profile from schema 1.2 `dset/scopes/skill/budget.yaml` or legacy
`dset/budget.yaml`; `budget.yaml.default_profile` applies only when a legacy
manifest has no selection, and the framework template is provenance only after
materialization. No override may lower a required quality or safety gate
without an explicit scope decision.

## Model-selection evidence

Lower unit token price is not evidence of lower task cost. A model override
requires a dated, task-relevant comparison that records required quality,
success/failure rate, token volume and price when available, retries, agent/tool
steps, latency, review/rework, sample size, harness, and important limitations.
Use directly comparable measured cost when available; otherwise keep metrics
separate and state confidence rather than inventing weights or a synthetic
currency. Stale, incomparable, or absent evidence falls back to inherited
model/effort. External benchmarks are candidate evidence, not universal model
rankings or evidence for multi-agent fan-out.
