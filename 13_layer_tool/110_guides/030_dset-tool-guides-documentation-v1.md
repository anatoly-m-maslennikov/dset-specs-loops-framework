# Documentation v1 applied profile

## Applicability

Select `documentation-v1` when a repository contains public or operational knowledge artifacts whose ownership and navigation must survive multiple contributors, agents, or sessions. It may be selected with any implementation-language profile or by itself.

The profile governs declared areas, not every incidental Markdown file. Change packages, fixtures, generated output, and archived evidence retain their own lifecycle contracts unless explicitly registered as governed areas.

## Deterministic gates

| Gate | Required proof |
|---|---|
| Profile/configuration | Project configuration names `documentation-v1`; the artifact registry and JSON Schema exist and parse |
| Artifact classification | The artifact-type registry and schema exist; type IDs, direct subtypes, primary questions, direct metadata, and path rules are valid and unambiguous |
| Area identity | Area IDs and roots are unique; owner and purpose are non-empty; roots and hubs exist |
| Parent hierarchy | Exactly one root hub exists; each area parent resolves; parent chains terminate without cycles |
| Hub shape | Each area hub contains Purpose, Boundaries, and Start here/Navigation sections |
| Root navigation | The repository root hub links every registered top-level area hub |
| Portability | Local Markdown links resolve; GitHub alert syntax is supported; wiki links are rejected |

The canonical `dset check` reports stable path-oriented diagnostics and does not write. `dset verify` runs these gates together with the selected implementation-language profile and repository checks.

## Qualitative gates

Deterministic parsing cannot prove that a rule is understandable or that a section truly defines an entity before using it. Evaluate:

- helicopter navigation by a cold reader;
- artifact-type and subtype selection, Analysis/Evidence separation, and duplicate-authority avoidance;
- what/why/how/history separation;
- domain entity and lifecycle completeness;
- definition-before-use and connection-vs-definition clarity;
- proportionality of hub depth and document splitting.

Record prompts, reviewer routes, disagreements, and corrective loops. Do not encode semantic judgments as fragile keyword bans merely to make them automated.

## Adoption

1. Choose the repository root hub.
2. Inventory stable public areas and existing sources of truth.
3. Create only the missing area hubs that satisfy the navigation criteria.
4. Classify authoritative documents and move duplicated why/how/history content only through a reviewed change.
5. Add the artifact registry and select `documentation-v1` independently from the code profile.
6. Run deterministic checks and cold-reader evals before making the profile required.

Existing repositories may adopt incrementally, but one concern cannot retain two writable normative owners during migration.
