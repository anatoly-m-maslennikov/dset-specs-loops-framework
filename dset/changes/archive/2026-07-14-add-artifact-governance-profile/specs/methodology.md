# Methodology delta — Artifact governance profiles

## ADDED — ART-REQ-001 Profile axes remain orthogonal

DSET must select implementation-language enforcement and artifact-governance enforcement independently. Runtime risk selects recovery/supportability semantics; deployment topology selects durable authority; a language profile selects code tools and thresholds; an artifact profile selects document architecture, ownership, navigation, and authoring gates.

**Scenario ART-SCN-001:** A Python repository may select `python-v1` and `documentation-v1` together; a documentation-only repository may select `documentation-v1` without inheriting Python tools; a future TypeScript repository may combine its own language profile with the same artifact profile.

## ADDED — ART-REQ-002 Governed areas have explicit architecture and hubs

Every governed public artifact area must declare one purpose, owner, root, hub, and parent relationship. The repository root hub gives the helicopter view and routes to area hubs. Hubs are thin navigation surfaces, not owners of atomic rules or exhaustive manually duplicated indexes.

**Scenario ART-SCN-002:** A new reader starts at `README.md`, reaches the documentation or methodology hub, and identifies the owning artifact without scanning unrelated files.

## ADDED — ART-REQ-003 Artifact types own different questions

DSET must define distinct types for navigation, normative rules, behavioral specification, architecture, rationale, decisions, procedures, proof plans, evidence/history, and agent workflows. Each artifact has one primary type and one owning question; secondary meaning is expressed through links rather than duplicate rule text.

**Scenario ART-SCN-003:** A design explanation moves to rationale, a repeatable sequence moves to a playbook, and the normative rule remains in one reference document linked by both.

## ADDED — ART-REQ-004 Authoring rules are type-specific

Universal rules must require answer-first writing, one primary question, explicit scope and authority, links instead of copied rules, and GitHub-portable Markdown. Specification rules must keep observable what separate from why, model domain entities and per-entity lifecycle state machines before code, and order definitions so every entity is defined only from earlier entities; a forward section reference is a connection, not a definition.

**Scenario ART-SCN-004:** A specification that uses an undefined downstream entity as part of an earlier entity's definition fails review even when it contains a forward link; the entity must be reordered or the relationship restated as a later connection.

## ADDED — ART-REQ-005 Documentation v1 is executable

The `documentation-v1` profile must provide machine-readable governed-area configuration and deterministic checks for profile identity, required hubs, unique area IDs/roots, valid owner/purpose/parent fields, reachable parent hierarchy, required hub sections, root-to-area navigation, and existing portable links. Qualitative authoring judgments remain evals rather than brittle keyword gates.

**Scenario ART-SCN-005:** Removing an area hub or pointing an area at a missing parent produces a stable diagnostic through `dset check`; debating whether rationale is sufficiently separated remains a rubric-based eval.

## ADDED — ART-REQ-006 The framework dogfoods artifact governance

This public repository must activate `documentation-v1`, expose documentation and methodology hubs, register its stable governed areas, and keep current governance separate from archived change evidence.

**Scenario ART-SCN-006:** The same canonical verification command validates Python v1 and documentation v1 without describing documentation as a programming language.
