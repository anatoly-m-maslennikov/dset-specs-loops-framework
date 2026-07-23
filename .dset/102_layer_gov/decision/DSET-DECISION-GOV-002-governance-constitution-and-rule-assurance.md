# Decision — Governance constitution and rule assurance

- **Decision ID:** `DSET-DECISION-GOV-002`
- **Status:** accepted
- **Decision date:** 2026-07-16
- **Resolves Question:** direct operator requirement following bounded FPF review
- **Supersedes:** none
- **Superseded by:** none
- **Selected option:** strengthen `DSET-RULE-ARCHITECTURE` as the sole governance constitution and separate rule authority, dependency, precedence, and assurance
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Context and scope

DSET needs a governance rule that governs how other normative rules become
authoritative without creating an infinite chain of new rule authorities. The
candidate review considered a new `DSET-RULE-RULE-AUTHORITY`, a new
`DSET-RULE-GOVERNANCE-OF-GOVERNANCE`, and an extension of the existing
dependency-free Architecture rule.

This Decision affects the GOV governance registry, profile templates, schema,
validator, accepted methodology package, and active self-hosting Change. It
does not define product-domain precedence and does not make proof or provenance
an alternative source of rule authority.

## Evidence basis and rationale

Three independent read-only reviews compared the candidates with the pinned FPF
revision recorded in `dset/scopes/gov/provenance.yaml` and with DSET's current
governance graph. They agreed that:

- authority, applicability/currentness, provenance, transactional discharge,
  and assurance are different questions;
- dependency and precedence are separate relations and both must remain
  acyclic;
- proof depth should be risk-proportionate;
- a new sibling root would duplicate `DSET-RULE-ARCHITECTURE` and complicate
  bootstrap without adding a distinct owner question.

Strengthening the existing Architecture rule preserves one root owner. The
bootstrap transaction structurally materializes and validates the local
manifest, registry, and rule documents; after admission, the local registry and
governing documents are project authority. Later changes use the ordinary
Decision, Change, compile-down, and proof lifecycle.

## Consequences and discharge

This Decision is compiled into current truth through:

- `DSET-REQUIREMENT-GOV-023` and `DSET-INVARIANT-GOV-012`;
- `DSET-TEST-PLAN-GOV-023` and `DSET-EVAL-PLAN-GOV-013`;
- `dset/scopes/gov/governance/architecture.md`;
- governance registry schema 1.1 and profile `core-v1` version 0.3;
- executable precedence validation and deterministic regressions;
- synchronized Architecture, Artifact Maintenance, and Work Items templates.

Every rule declares both `depends_on` and `precedence_over`, including empty
lists. Declared precedence targets must exist and the precedence graph must be
acyclic. Registry order never creates precedence. Missing or stale assurance
blocks only the relying claim or gate; it does not silently erase valid rule
authority.

## Lifecycle evidence

- **Confirmation evidence:** the bounded review proof, synchronized governance
  templates, validator tests, canonical DSET checks, and implementing commit
  that cites this Decision.
- **Violation or counter-evidence:** none observed.
- **Reopen when:** DSET introduces another constitutional root, merges
  dependency with precedence, lets proof create authority, changes registry
  schema compatibility, or cannot represent a real rule conflict safely.
- **If reopened, retain:** one repository-local owner, fail-closed resolution,
  authority/assurance separation, and bounded proof currentness.
- **If reopened, withdraw:** the assumption that per-rule
  `precedence_over` is sufficient for every future conflict model.
- **Successor or retirement:** pending; explicitly record `no successor` when
  retired.

Never silently edit accepted history. Reopen or supersede this Decision, retain
both directions, and compile the successor into every affected evergreen owner.
