# Decision — Select the DSET 0.3 operating shape

- **Decision ID:** `DSET-DECISION-SKILL-001`
- **Status:** accepted
- **Decision date:** 2026-07-15
- **Resolves Question:** `DSET-QUESTION-SKILL-001`
- **Supersedes:** none
- **Superseded by:** none
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`
- **Selected option:** Repository-owned rules, thin five-skill topology,
  bounded self-hosting, SemVer-compatible release classes, and evidence-based
  delegation budgets

## Context and scope

This Decision covers the coherent operating shape specified by
`DSET-CHANGE-SKILL-001` across the repository. Fixed Contracts include local
rule ownership, fail-closed resolution, separate tests/evals, protected
delivery, bounded recursion, and readiness-gated 1.0 promotion. The comparison
frame and candidate-specific currentness are in the
[Solution Landscape](solution-landscape.md).

## Evidence basis and rationale

The selected shape is favorable on local authority, offline customization,
bounded discovery, deterministic transition semantics, and resistance to
price-only model downgrades. Evidence is sufficient for implemented §§0–§4
local behavior and degraded or insufficient for hosted state, two missing
skills, runtime session records, release automation, TypeScript, pilots, and
distribution. The Decision accepts the target design without claiming those
pending capabilities are implemented.

Embedded rules, remote live authority, hidden fallback, and automatic decimal
promotion violate fixed constraints. Per-step versus five-skill usability and
delegation fan-out remain runtime-eval questions rather than forced comparison
winners.

## Consequences and discharge

Normative consequences are discharged to the layer-owned
[Requirements](specs/methodology.md), [Contracts](specs/contracts.md),
[test plan](test-plan.md), [eval plan](eval-plan.md), [Design](design.md),
repository governance, and release policy. The Decision retains rationale only.
Implementation remains bounded by the active [tasks](tasks.md) and
[verification](verification.md).

Trade-offs include registry and materialization maintenance, an intentionally
small public skill surface, coordinated product/package versions, and possible
higher nominal model cost when cheaper-token alternatives use more work.

## Lifecycle evidence

- **Confirmation evidence:** Current local gate, wrapper inventory, schema/rule
  validation, and bounded self-host proof linked from `verification.md`.
- **Violation or counter-evidence:** Current hosted proof is stale; the released
  validator cannot parse schema 1.2; runtime and pilots remain incomplete. These
  limit implementation/readiness claims but do not yet refute the selected
  target shape.
- **Reopen when:** A fixed Contract changes, host-native evals favor another
  skill topology, a compatible released validator disproves the bootstrap
  design, task-relevant evidence disproves the delegation policy, or pilot
  evidence shows the repository-owned rule model is not portable.
- **If reopened, retain:** prior evidence, rationale, external Contracts, and
  unaffected accepted Requirements.
- **If reopened, withdraw:** invalid assumptions and only the downstream
  authority that depended on them.
- **Successor or retirement:** none; any supersession must name the successor or
  explicitly record retirement with `no successor`.
