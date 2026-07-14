# Third-party notices and provenance

DSET Spec Loops is original work released under the repository [Apache License 2.0](LICENSE). The projects below influenced terminology or workflow choices. DSET does not install them, depend on them at runtime, or treat them as governing methodology.

## OpenSpec

- **Upstream:** [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)
- **Revision reviewed:** [`0a99f410457271aa773d8b106f03f637f7c6b3c0`](https://github.com/Fission-AI/OpenSpec/commit/0a99f410457271aa773d8b106f03f637f7c6b3c0)
- **License:** MIT; retained at [`third_party/licenses/openspec-MIT.txt`](third_party/licenses/openspec-MIT.txt)
- **DSET surfaces:** methodology roadmap, change-package lifecycle, solution-landscape comparison, migration guidance
- **Use:** Concepts such as repository-local specs, changes, and archival were evaluated and independently re-expressed in DSET terminology. No OpenSpec source code, templates, command text, or generated files are distributed in DSET v1.

OpenSpec names and marks belong to their respective owners. References describe provenance and comparison only and do not imply endorsement.

## Matt Pocock skills

- **Upstream:** [mattpocock/skills](https://github.com/mattpocock/skills)
- **Revision reviewed:** [`66898f60e8c744e269f8ce06c2b2b99ce7660d5f`](https://github.com/mattpocock/skills/commit/66898f60e8c744e269f8ce06c2b2b99ce7660d5f)
- **License:** MIT; retained at [`third_party/licenses/mattpocock-skills-MIT.txt`](third_party/licenses/mattpocock-skills-MIT.txt)
- **DSET surfaces:** `dset-grill`, `dset-diagnose`, and `dset-prototype` workflow boundaries
- **Use:** The public skill collection informed the choice of three focused workflow categories. DSET instructions, outputs, safety boundaries, and implementation are independently written; no upstream skill file is copied.

Matt Pocock's name and marks belong to their owner. References describe provenance only and do not imply endorsement.

## Contribution rule

Before copied or substantially adapted third-party material enters this repository, record its exact source and revision, license, affected files, modifications, required notices, and trademark boundary here and in [`dset/provenance.yaml`](dset/provenance.yaml). Add the applicable license text under `third_party/licenses/`. Independently re-expressed ideas must still cite their source when it materially shaped the design.
