---
artifact_type: procedure
artifact_subtype: playbook
scope_path:
  - layer:gov
priority: medium
---

# Maintain governed artifacts

## Trigger

Use this playbook when adding, splitting, moving, renaming, or changing the authority of a governed public artifact or hub.

## Steps

1. Start from the repository root hub and the affected area hub.
2. Identify the one current owner and classify the requested content using the `artifact-types.md`.
3. Open a bounded DSET change when public behavior, reusable rules, authority, artifact structure, or validation changes.
4. Keep normative what, rationale why, procedural how, decision history, and observed evidence in their owning artifacts.
5. If a file mixes independent questions, split it and leave migration links from the old public path when compatibility requires them.
6. Update the `artifact_structure` section of `.dset/dset_settings.toml` when a governed area, hub, owner, purpose, or parent changes.
7. Apply the `hub-rules.md` and update the parent hub only when the stable navigation route changes; do not add every leaf file.
8. Run `python -m dset_toolchain check .`, inspect diagnostics, and correct the earliest ownership or hierarchy defect.
9. Run the selected qualitative navigation/authoring evals when semantics or reader routes changed.
10. Run `python -m dset_toolchain verify .`, record bounded evidence, reconcile accepted truth, and archive through the implementing PR.

## Checks

- One root hub and an acyclic parent hierarchy.
- Every governed area has one existing hub, owner, purpose, and root.
- Root navigation reaches each top-level area hub.
- No rule is duplicated across normative, rationale, playbook, or evidence surfaces.
- Specifications define entities and lifecycle states before code and avoid forward definitions.
- Markdown links resolve on GitHub and no private machine paths entered public artifacts.
- Historical evidence remains history rather than current authority.

## Stop conditions

Stop before deleting or moving current normative content when the owner is ambiguous, public compatibility is unknown, or two areas claim the same concern. Keep the change active, record the conflict, and resolve authority before continuing.
