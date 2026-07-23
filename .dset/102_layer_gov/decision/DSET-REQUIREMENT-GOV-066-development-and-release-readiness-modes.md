+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-214"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-066"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET defines a development mode that moves accepted Atomic Artifacts through Test and Evaluation planning, implementation, execution, and evidence, plus a mandatory release-readiness mode that first compiles active Atomic Artifacts into evergreen specifications, resolves conflicts to a fixed point, and then refreshes implementation and assurance evidence at the exact release head."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Compiling every accepted atom immediately creates avoidable churn during development, while releasing without a full authority-to-specification reconciliation risks shipping implementation and evidence against stale current truth."

[scope]
kind = "layer"
id = "governance"

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = false
local_context_required = true

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-048"
+++

# Requirement — Separate development and release-readiness modes

DSET exposes two governed workflow modes.

## Development mode

Development mode is the default:

```text
accepted Atomic Artifacts
→ Test Plan and Evaluation Plan
→ implementation
→ executable Tests and Evaluations
→ Evidence Records
→ development Verification
```

Development mode consumes the latest compiled specifications plus every active
accepted Atomic Artifact not yet included in those specifications. It does not
require evergreen specifications to be recompiled after every new atom.

## Release-readiness mode

Release-readiness mode is mandatory before a Version can be declared ready:

```text
all active Atomic Artifacts
→ evergreen specifications
→ conflict detection
→ conflict resolution through new Atomic Artifacts
→ recompilation until conflict-free
→ implementation reconciliation
→ Test and Evaluation execution
→ fresh Evidence Records
→ release Verification
→ Readiness Record
```

Conflict resolution never edits an existing Atomic Artifact. It emits the
required successor, resolution, override, replacement, or other applicable
atom and repeats compilation until the authority set and evergreen projections
reach a fixed point.

Any specification, implementation, Test implementation, Evaluation
implementation, or applicable configuration change after an assurance run
makes the affected development evidence stale for release. Release-readiness
assurance runs against the exact candidate head.

## Settings and invocation

`dset_settings.toml` records `development` as the default workflow mode and
`release_readiness` as the required pre-release mode. `dset-init` materializes
these defaults. `dset release` selects release-readiness behavior without
silently rewriting the project's configured development default.
