# Proposal — Add artifact governance profiles

- **Change ID:** `add-artifact-governance-profile`
- **Profile:** `standard`
- **Target package:** `methodology`
- **Implementing PR:** [anatoly-m-maslennikov/dset-specs-loops-framework#8](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/8)
- **Status:** archived with final readiness evidence; PR remains draft until this evidence-only head passes

## Problem

Python and the planned JavaScript/TypeScript profiles govern implementation-language tooling. They do not govern the repository's other production surfaces: methodology, specifications, architecture, hubs, rationale, Decision records, playbooks, runbooks, skills, and evidence. Treating documentation as another language profile would collapse two independent concerns.

The repository also lacks one artifact architecture that tells a reader which document types exist, what each type owns, where rationale and procedures belong, and which hub provides the helicopter view. The root README currently compensates by linking many leaf documents directly. Structural Markdown validation proves links exist, but not that documentation has one owner, one purpose, a navigable hierarchy, or the correct artifact type.

## Outcome

Add an orthogonal artifact-governance profile system and make `documentation-v1` active for this repository. Publish a thin documentation hub plus separate architecture, type, authoring, navigation, maintenance, and rationale documents. Register governed public areas in machine-readable configuration and validate their hubs, ownership, parent hierarchy, portability, and type contracts through the canonical DSET command.

## Scope

- Define runtime-risk, durability-topology, implementation-language, and artifact-governance selections as independent axes.
- Define artifact types and their owning questions: hub, normative reference, specification, architecture, rationale, Decision record, playbook/runbook, proof plan, evidence/changelog, and skill.
- Define universal and type-specific authoring rules, including what/why separation, domain entities and lifecycles before code, and definition-before-use ordering.
- Add public documentation and methodology hubs for helicopter navigation.
- Add a `documentation-v1` configuration, schema, validator diagnostics, fixtures/tests, and repository adoption.
- Reconcile durable requirements and proof contracts into the methodology package.

## Non-goals

- Rewriting every legacy methodology document into atomic files in this change.
- Guessing a JavaScript/TypeScript code profile before evidence from `obsidian-your-harness`.
- Requiring Obsidian frontmatter, wiki links, backlinks, or Dataview in a GitHub distribution.
- Turning hubs into exhaustive file inventories or copying the private vault's physical taxonomy.
- Building a general-purpose documentation site generator or CMS.

## Risk

Governance risk is moderate because new ownership rules can create navigation churn or duplicate authority. Runtime and data risk are low: the implementation extends read-only repository validation and committed schemas. Rollout remains additive until existing public links, tests, and independent navigation evals pass.
