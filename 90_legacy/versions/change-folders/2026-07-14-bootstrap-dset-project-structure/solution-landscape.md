# Solution landscape — Bootstrap structure

## Capability gaps

| Gap | Needed behavior |
|---|---|
| Accepted truth | One durable package-owned location |
| Bounded change | One active folder with the full artifact/evidence contract |
| Growth path | Add packages and global truth only when real boundaries appear |
| Machine discovery | One small project manifest |

## Candidates

| Candidate | Fit | Decision |
|---|---|---|
| Flat `dset/specs/*.md` | Minimal now, but package ownership becomes an incompatible migration when a second capability appears | Reject |
| `dset/specs/packages/methodology/` without `global/` | Explicit package boundary with no speculative cross-package layer | **Adopt** |
| Full `global/` plus `packages/` tree | Matches a future large project but creates empty owners and ceremony today | Defer until triggered |
| A competing OpenSpec root | Violates the canonical `dset/` decision | Reject |

## Decision

Adopt the explicit one-package tree and a small `dset/dset.toml` registry. Keep all contracts repository-native. No external framework or proof-of-fit spike is required for this filesystem-only bootstrap.
