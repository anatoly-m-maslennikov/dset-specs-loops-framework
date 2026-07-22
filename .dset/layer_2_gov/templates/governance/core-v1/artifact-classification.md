# Artifact classification rules

**Rule ID:** `DSET-RULE-ARTIFACT-CLASSIFICATION`

## Two independent axes

Every governed artifact has exactly one primary `artifact_type` and at most one
allowed direct `artifact_subtype`. Atomic records separately use semantic
`type` and `subtype`. Artifact classification never creates a fifth semantic
Type or derives semantic meaning from a filename, folder, workflow, or tool.

The project-local `.dset/project/artifact-types.toml` registry owns the
machine-readable artifact vocabulary for schema 1.3. Older equivalents remain
compatibility inputs. The selected artifact profile must validate the
registry before relying on classification.

## Classification order

1. Identify the carrier's one primary owning question.
2. Select the registered `artifact_type` that owns that question.
3. Select at most one allowed direct `artifact_subtype`; omit it when the type's
   general form is the honest classification.
4. Record classification directly on an editable carrier or resolve it through
   exactly one registered path rule.
5. Stop on unknown types, mismatched subtypes, nested subtypes, missing
   classification, or multiple applicable path rules.

Direct metadata uses `artifact_type` and `artifact_subtype`. The fields `type`
and `subtype` remain reserved for semantic atom classification. Existing
immutable atoms are classified externally; classification never edits their
emitted content.

## Naming

The base naming convention uses the primary artifact type token in a new
artifact ID and filename. Optional artifact subtypes live in direct metadata
and do not enter the structural name. For example, a Version Scope is
`APP-VERSION-001-0-4-core.md` with `artifact_subtype: version_scope`; a
Roadmap uses the same `VERSION` sequence with `artifact_subtype: roadmap`.

Projects may opt into subtype tokens for newly emitted artifacts with
`artifacts.subtype_in_names = true` in `.dset/dset_settings.toml`.
This is an independent optional capability, not a bundled “advanced mode.” A
setting change never renames an immutable atom or an already stable artifact
identity.

## Role boundaries

- Analysis Report interprets information; Evidence Record records an
  observation.
- Specification compiles current or required truth; Plan describes intended
  work.
- Procedure describes a reusable method; Plan describes one intended
  enactment.
- Version owns bounded version intent, transaction, gate, and publication
  records; Plan owns intended implementation or proof work.
- Implementation realizes accepted truth or QA definitions; Verification
  assesses what evidence supports.
- Readiness Record contains the explicit release gate disposition; green checks
  alone do not authorize release.
- Release Record immutably records the publication occurrence.
- Derived View and Navigation never become authority.

An accepted analysis conclusion becomes a separate Decision, Question,
Problem, or QA atom. A proposed Design is an Analysis Report/Proposal; accepted
current Design is a Specification/Design. An external audit is evidence;
External Audit Analysis is the project's interpretation and triage of it.

## Release lifecycle

Release lifecycle artifacts remain flat peers under one primary `version`
type. Its direct subtypes are `roadmap`, `version_scope`, `change`,
`release_plan`, `readiness_record`, and `release_record`. They share one
project-wide `VERSION` identity sequence. Milestones are Roadmap entries.
Release Notes and changelogs are rendered or derived from immutable Release
Records.

## Scope

The catalog covers development and release handoff. Sales, customer-success
management, performed production support, and operation of deployment
infrastructure are outside it. External work may supply operator input or
evidence. Developing required supportability behavior or documentation remains
Implementation.
