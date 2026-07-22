# Third-party notices and provenance

DSET Spec Loops is original work released under the repository [Apache License 2.0](LICENSE). The projects below influenced terminology or workflow choices. DSET does not install them, depend on them at runtime, or treat them as governing methodology.

## OpenSpec

- **Upstream:** [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)
- **Revision reviewed:** [`0a99f410457271aa773d8b106f03f637f7c6b3c0`](https://github.com/Fission-AI/OpenSpec/commit/0a99f410457271aa773d8b106f03f637f7c6b3c0)
- **License:** MIT; retained at [`020_dset-project-licenses-openspec-mit.txt`](LICENSES/020_dset-project-licenses-openspec-mit.txt)
- **DSET surfaces:** methodology roadmap, change-package lifecycle, solution-landscape comparison, migration guidance
- **Use:** Concepts such as repository-local specs, changes, and archival were evaluated and independently re-expressed in DSET terminology. No OpenSpec source code, templates, command text, or generated files are distributed in DSET v1.

OpenSpec names and marks belong to their respective owners. References describe provenance and comparison only and do not imply endorsement.

## Matt Pocock skills

- **Upstream:** [mattpocock/skills](https://github.com/mattpocock/skills)
- **Revision reviewed:** [`66898f60e8c744e269f8ce06c2b2b99ce7660d5f`](https://github.com/mattpocock/skills/commit/66898f60e8c744e269f8ce06c2b2b99ce7660d5f)
- **License:** MIT; retained at [`010_dset-project-licenses-mattpocock-skills-mit.txt`](LICENSES/010_dset-project-licenses-mattpocock-skills-mit.txt)
- **DSET surfaces:** `dset-clarify`, `dset-diagnose`, and `dset-prototype` workflow boundaries
- **Use:** The public skill collection informed the choice of three focused workflow categories. DSET instructions, outputs, safety boundaries, and implementation are independently written; no upstream skill file is copied.

Matt Pocock's name and marks belong to their owner. References describe provenance only and do not imply endorsement.

## First Principles Framework

- **Upstream:** [ailev/FPF](https://github.com/ailev/FPF)
- **Revision reviewed:** [`afa4936541774021c92adb97c3cbf787bf126062`](https://github.com/ailev/FPF/commit/afa4936541774021c92adb97c3cbf787bf126062)
- **License:** No license was declared in the reviewed repository tree; this is recorded at [`000_dset-project-licenses-fpf-no-license.txt`](LICENSES/000_dset-project-licenses-fpf-no-license.txt).
- **DSET surfaces:** workflow return boundaries, Decision discharge, risk-scaled review, comparison evidence, proof currentness, and derived navigation.
- **Use:** DSET independently re-expresses and attributes a small set of public concepts and short technical terms. No substantial expressive passage, template, code, ontology, index, or Obsidian mechanic from FPF is copied or distributed.

## Conductor

- **Sources reviewed:** [Git worktrees](https://www.conductor.build/docs/concepts/git-worktrees), [workspaces and branches](https://www.conductor.build/docs/concepts/workspaces-and-branches), and [parallel agents](https://www.conductor.build/docs/concepts/parallel-agents), observed 2026-07-15.
- **DSET surface:** the optional one Change to one isolated branch-backed workspace/worktree mode.
- **Use:** DSET independently defines its own Change identity, proof, dependency handoff, default integration-branch flow, optional worktree isolation, and release semantics. No Conductor text, code, or product artifact is copied.

## Contribution rule

Before copied or substantially adapted third-party material enters this repository, record its exact source and revision, license, affected files, modifications, required notices, and trademark boundary here and in [`dset_settings.toml`](.dset/dset_settings.toml). Add the applicable license text under `LICENSES/`. Independently re-expressed ideas must still cite their source when it materially shaped the design; web-only references may be recorded here with their observation date when no versioned source artifact is imported.
