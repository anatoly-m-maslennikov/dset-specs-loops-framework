# DSET workflow skills

These repository-native skill sources are portable release artifacts. Installed copies are distributions; this repository remains the editable source.

- [`dset-grill`](dset-grill/SKILL.md) — resolve domain ambiguity and proof obligations before specification acceptance.
- [`dset-diagnose`](dset-diagnose/SKILL.md) — investigate defects and incidents through evidence and Back-to-Left provenance without silently authorizing a fix.
- [`dset-prototype`](dset-prototype/SKILL.md) — run bounded disposable design experiments and feed evidence into the Solution Landscape and ADR.

Each folder contains a concise `SKILL.md` and generated `agents/openai.yaml`. No skill depends on private memory, machine-specific paths, shell-only behavior, or a parallel specification format.
