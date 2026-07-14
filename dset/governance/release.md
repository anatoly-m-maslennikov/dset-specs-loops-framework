# Release transaction rules

## Generic authority

The adopting project configures one integration branch, one protected release
branch, one forge publisher, and one exact tag pattern in `dset/dset.yaml`.
Generic DSET skills use configured roles, never hard-coded branch or forge
names.

Each release PR has one committed release declaration in its DSET change
manifest. It is the authority for class, base, target, and readiness identity;
package metadata, release notes, PR text, tag, and forge release are validated
mirrors. The base is read exactly once from the protected branch version
manifest. Re-running preparation must be idempotent and cannot bump the target
again.

## Classification and transitions

`small` means a compatible correction or documentation/internal change with no
new public capability, migration, deprecation, or changed public contract.
`normal` means any new capability, public contract/profile/schema behavior,
deprecation, migration, or pre-1.0 compatibility break. A mixed PR takes the
highest-impact class. A material ambiguity stops release preparation.

| Base state | Class | Only valid target |
|---|---|---|
| no activated product version | `bootstrap` | `0.2.0` |
| `0.Y.Z` | `small` | `0.Y.(Z+1)` |
| `0.Y.Z` | `normal` | `0.(Y+1).0` |
| passing `0.Y.Z` with 1.0 readiness | `rc` | `1.0.0-rc.1` |
| `1.0.0-rc.N` | `rc` | `1.0.0-rc.(N+1)` |
| passing `1.0.0-rc.N` | `final` | `1.0.0` |
| stable `X.Y.Z`, `X >= 1` | `small` | `X.Y.(Z+1)` |
| stable `X.Y.Z`, `X >= 1` | `normal` | `X.(Y+1).0` |
| stable `X.Y.Z`, `X >= 1` | `breaking` | `(X+1).0.0` |

Once a public RC exists, it is immutable. An unpublished RC preparation may be
abandoned without changing the protected base. A published RC can only advance
to a higher RC or final release; abandoning the release line publishes nothing
else under that version and never returns to a lower `0.y.z` identity.

## RC readiness owner

The change's committed verification artifact is the readiness manifest. It is
anchored to the exact candidate SHA and lists declared scope, every required
test/eval/pilot/distribution gate with `applicable` or justified `not-applicable`
disposition, evidence links, and the blocker register. Final promotion permits
only release metadata and evidence-link updates; substantive code, behavior, or
scope changes require a new `rc.N+1` candidate and fresh readiness evidence.

## Identity and publication

Canonical product identity is SemVer. Python package metadata serializes
`1.0.0-rc.1` as PEP 440 `1.0.0rc1`; validation treats only this defined mapping
as equivalent. The tag is exactly `v<product-semver>` and the forge release uses
the product SemVer.

Post-merge publication is required at the exact protected-branch merge SHA. If
tag/release already exist at that SHA with matching identity, retry succeeds. If
one is missing, create only the missing object. Any existing tag or release with
a different SHA or identity stops; tags are never retargeted or reused. A bad
published release is preserved and marked withdrawn/deprecated when supported;
its correction uses a new reviewed PR and a higher version. Publication recovery
must not add a content commit to the protected branch.
