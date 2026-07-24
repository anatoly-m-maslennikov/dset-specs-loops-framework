---
artifact_type: navigation
artifact_subtype: hub
scope_path:
  - layer:gov
priority: medium
---

# Hub and navigation rules

## Rule

Create a hub for a stable area people revisit directly, not merely because a folder exists. A hub is a thin front door; it does not replace the documents it routes to.

## Hub levels

| Level | Owns | Example |
|---|---|---|
| Repository root hub | Framework purpose, major public areas, primary run path | `README.md` |
| Area hub | Area purpose, boundaries, stable owning documents or child areas | `documentation/README.md`, `methodology/README.md` |
| Child hub | A stable nested area with its own audience or lifecycle | Add only when the parent area would otherwise mix real subareas |

Review navigation when a reader must traverse more than three hubs before reaching an owner. Depth is a review signal, not a reason to flatten meaningful ownership boundaries.

## Required hub sections

Every governed area hub contains:

- **Purpose** — what the area is for and who starts here;
- **Boundaries** — what it owns and explicitly does not own;
- **Start here** or **Navigation** — stable routes with one-line descriptions.

An operating area may additionally link its validation command, maintenance playbook, or support runbook.

## Link rules

- The root hub links each registered top-level area hub.
- Each registered area declares one parent hub; the parent chain must terminate at the root hub without cycles.
- Link stable child areas, maintained specifications and plans, settings, and
  other long-lived non-atomic owners directly.
- Represent atomic artifacts only by their containing folders. Never enumerate
  or link individual atomic carriers from a hub.
- Never list or link anything below `.dset_runtime/`. A hub may name the runtime
  root only to explain that it is excluded from durable navigation.
- Generated, archived, fixture, and evidence directories do not receive hubs unless they are stable reader-facing areas with their own navigation need.
- Use relative Markdown links that resolve on GitHub. Do not use Obsidian wiki links, local absolute paths, or private application state.

## When not to create a hub

Do not create a hub for a thin folder, one-off change, dated archive, generated package, test fixture, or storage-only directory. Use its nearest owning area hub or a generated index when exhaustive discovery is required.

## Maintenance invariant

Adding or removing a governed area updates its registry entry, its hub, its
parent hub route, and verification in the same change. Adding or removing an
individual atom never changes a hub. Update navigation only when an
atomic-artifact folder or a stable long-lived non-atomic owner is added,
removed, or renamed.
