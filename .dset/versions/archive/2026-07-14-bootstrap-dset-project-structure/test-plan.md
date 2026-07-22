# Test plan — Bootstrap the DSET project structure

## Deterministic checks

| Test ID | Requirement | Proof |
|---|---|---|
| **DSET-TEST-GOV-001** | DSET-REQUIREMENT-GOV-001 | Assert `dset/{README.md,dset.toml,specs,changes,templates,schemas}` exists and no competing project-truth root is introduced |
| **DSET-TEST-GOV-002** | DSET-REQUIREMENT-GOV-002 | Parse `dset/dset.toml`; assert one package named `methodology`, its path exists, mode is `single-package`, and global root is null |
| **DSET-TEST-META-001** | DSET-REQUIREMENT-META-001 | Assert this change contains the eight named Markdown documents plus `specs/` and `proofs/` |
| **DSET-TEST-OPS-001** | DSET-REQUIREMENT-OPS-001 | Assert PR is non-pending before archive; assert archive path/date and fresh verification after the last content change |
| **DSET-TEST-GOV-003** | DSET-REQUIREMENT-GOV-003 | Assert manifest values remain `documentation-v1-pending` and `canonical_command: pending` until executable assets land |
| **DSET-TEST-GOV-004** | All | Resolve local Markdown links, parse YAML, check balanced fences/details, and run `git diff --check` |

## Regression rule

A future structural defect adds a failing fixture to the canonical validator once that validator exists. Until then, verification records the exact read-only commands and exit status used for this bootstrap.
