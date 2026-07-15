# Methodology GOV domain

This is one layer-owned fragment of the logical methodology package. Use the sibling layer hubs for connected definitions; this file owns only the entities and invariants below.

## Entities

| Entity | Definition |
|---|---|
| **Framework truth** | Released DSET methodology and framework-owned assets in this public repository |
| **Package** | A cohesive capability with one vocabulary, specification, public contract, deterministic test plan, and applicable eval plan |
| **Change** | One bounded unit of unaccepted intent and evidence under `dset/scopes/<primary-layer>/changes/<change-slug>/`, identified independently by `DSET-CHANGE-<LAYER>-<NNN>` |
| **Language profile** | Versioned mapping from the six neutral gate categories to language-native tools, scopes, thresholds, and exclusions |
| **Artifact governance profile** | Versioned mapping from artifact architecture and authoring rules to machine-checkable ownership, hierarchy, hub, navigation, and portability gates; it is selected independently from an implementation-language profile |
| **Governed artifact area** | A stable public knowledge boundary with one purpose, owner, root, hub, and structural parent |
| **Artifact type** | A document family defined by one primary owning question, such as navigation, normative rules, behavior, architecture, rationale, decision, procedure, proof plan, evidence, or agent workflow |
| **Hub** | A thin navigation surface that identifies an area's purpose, boundaries, and stable owning documents without becoming an exhaustive index or a second normative owner |
| **Governance registry** | Repository-local machine-readable mapping from workflow and normative rule IDs to their editable governing documents, dependencies, applicability, and profile/customization identity; it points to rules without restating them |
| **Governing document** | The single editable repository-local owner of one or more normative rule IDs selected by the governance registry |
| **Problem** | An observed bug, gap, or debt item that requires triage without implying its solution |
| **Question** | An unresolved choice or uncertainty whose consequential resolution is a Decision |
| **Decision** | A durable consequential choice among alternatives that records rationale, tradeoffs, and consequences; it is both the entity and artifact, uses the full `DECISION` type, and does not represent every implementation detail |
| **Layer** | An optional stable semantic owner for accepted IDs: `META`, `GOV`, `TOOL`, `SKILL`, or `OPS`; it is independent of directory layout |
| **Opportunity** | A bounded improvement with expected value when no current problem exists |
| **Ruleset identity** | Stable declaration of selected profile/version provenance and whether the materialized local rules remain equivalent or have become a valid custom project profile |

## Invariants

- **DSET-INVARIANT-GOV-001:** Framework truth and project truth never share a writable owner.
- **DSET-INVARIANT-GOV-002:** Public methodology renders and navigates on GitHub without Obsidian-only links or callouts.
- **DSET-INVARIANT-GOV-003:** A change cannot alter accepted truth until its proof is fresh and the change is archived through its implementing PR.
- **DSET-INVARIANT-GOV-004:** Each governed artifact has one primary type and owning question; links connect authorities without duplicating their rules.
- **DSET-INVARIANT-GOV-005:** Hubs own navigation and boundaries, while atomic documents own rules, rationale, procedures, decisions, proof, and history.
- **DSET-INVARIANT-GOV-006:** Every selected normative rule resolves to one editable governing document inside the adopting repository; a source template remains provenance rather than a live authority after materialization.
- **DSET-INVARIANT-GOV-007:** Invalid or incompatible selected rule ownership fails closed with a stable diagnostic, while explicitly justified non-applicability remains valid.
- **DSET-INVARIANT-GOV-008:** A locally changed ruleset remains valid project truth only under an explicit custom identity that retains its source profile/version provenance.
- **DSET-INVARIANT-GOV-009:** Every normative rule ID has exactly one editable governing document; skills, agent guidance, templates, generated installations, indexes, summaries, and caches never become parallel writable rule stores.
- **DSET-INVARIANT-GOV-010:** Intake routes only to problems, opportunities, or questions; Decisions and Changes are artifacts, Decision is both the entity and durable artifact, tasks live inside Changes, and external tickets are representations rather than semantic types.
- **DSET-INVARIANT-GOV-011:** All accepted IDs use the `DSET` project prefix and a full type; project-wide IDs omit the layer, layer-owned IDs include `META`, `GOV`, `TOOL`, `SKILL`, or `OPS`, and numbering is independent per type within each project-wide or layer sequence.
- **DSET-INVARIANT-GOV-012:** Rule authority and assurance remain distinct. Dependency and precedence are separate acyclic relations; invalid authority or unresolved conflict fails closed, while missing or stale assurance affects only the relying claim or gate.
