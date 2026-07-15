# Decision — Artifact classes, compilation, and provenance

- **Decision ID:** `DSET-DECISION-GOV-001`
- **Status:** accepted
- **Decision date:** 2026-07-16
- **Resolves Question:** direct operator requirement, no prior Question ID
- **Supersedes:** none
- **Superseded by:** none
- **Selected option:** classify DSET artifacts by authority class and require compile-down plus commit/session provenance
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Context and scope

DSET needs a clearer boundary between durable current truth, atomic historical
records, and implementation artifacts. The immediate requirement is:

- commits should name the Decision or authorizing artifact they implement;
- atomic artifacts should record the LLM session IDs that created or materially
  revised them;
- Decisions and other atomic artifacts should be compiled into current specs
  and plans before implementation treats them as governing truth;
- artifact authority classes should be explicit.

This Decision affects GOV artifact governance and the active methodology
package. It does not define a new queue beyond Problems, Opportunities, and
Questions, and it does not make session records authoritative.

## Evidence basis and rationale

The selected option preserves DSET's existing separation of accepted truth from
bounded evidence while making the missing provenance rule explicit. The
alternatives were weaker:

- leaving the behavior implicit would keep reviews dependent on session memory;
- making Decisions the current spec would duplicate authority and recreate
  canonical-source drift;
- treating code/tests/eval prompts as self-explaining would weaken traceability
  from implementation back to the operator-visible choice.

The chosen rule lets a reviewer move in both directions: from a commit to the
Decision or authorizing artifact, and from a transactional artifact to the
evergreen spec/plan/rule that now owns current truth.

## Consequences and discharge

This Decision is compiled into current truth through:

- `dset/scopes/gov/specs/packages/methodology/spec.md`
  - `DSET-REQUIREMENT-GOV-020`
  - `DSET-REQUIREMENT-GOV-021`
  - `DSET-REQUIREMENT-GOV-022`
- `dset/scopes/gov/governance/architecture.md`
- `dset/scopes/gov/governance/artifact-maintenance.md`
- `dset/scopes/gov/governance/work-items.md`
- `dset/scopes/gov/templates/change/decision.md`
- `dset/scopes/gov/templates/change/layered/change.yaml`
- `dset/scopes/gov/schemas/change.schema.json`

Future implementation commits that alter evergreen truth or implementation
surfaces must cite their implementing Decision in the commit body when a
Decision exists. Small fixes without a Decision must cite the authorizing
Problem, Opportunity, Question, or Change.

## Lifecycle evidence

- **Confirmation evidence:** this Change adds the Decision, compiles its
  consequences into GOV spec and governance, updates templates/schema, and will
  commit with `Implements: DSET-DECISION-GOV-001`.
- **Violation or counter-evidence:** none observed
- **Reopen when:** DSET changes artifact authority classes, removes
  transactional compile-down, changes commit provenance expectations, or
  changes the session-provenance field shape.
- **If reopened, retain:** the rationale for separating current truth,
  transactional history, and implementation artifacts.
- **If reopened, withdraw:** any claim that `llm_session_ids` or commit-message
  references alone create governing authority.
- **Successor or retirement:** pending; explicitly record `no successor` when
  retired.

Never silently edit accepted history. Reopen or supersede this Decision,
preserve both directions, update affected downstream owners, and name the
successor or explicit retirement without successor.
