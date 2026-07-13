# Test plan — Bootstrap the DSET project structure

## Deterministic checks

| Test ID | Requirement | Proof |
|---|---|---|
| **BOOT-TEST-001** | BOOT-REQ-001 | Assert `dset/{README.md,dset.yaml,specs,changes,templates,schemas}` exists and no competing project-truth root is introduced |
| **BOOT-TEST-002** | BOOT-REQ-002 | Parse `dset/dset.yaml`; assert one package named `methodology`, its path exists, mode is `single-package`, and global root is null |
| **BOOT-TEST-003** | BOOT-REQ-003 | Assert this change contains the eight named Markdown documents plus `specs/` and `proofs/` |
| **BOOT-TEST-004** | BOOT-REQ-004 | Assert PR is non-pending before archive; assert archive path/date and fresh verification after the last content change |
| **BOOT-TEST-005** | BOOT-REQ-005 | Assert manifest values remain `documentation-v1-pending` and `canonical_command: pending` until executable assets land |
| **BOOT-TEST-006** | All | Resolve local Markdown links, parse YAML, check balanced fences/details, and run `git diff --check` |

## Regression rule

A future structural defect adds a failing fixture to the canonical validator once that validator exists. Until then, verification records the exact read-only commands and exit status used for this bootstrap.
