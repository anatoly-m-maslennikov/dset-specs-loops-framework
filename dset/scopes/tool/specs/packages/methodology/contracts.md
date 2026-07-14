# Methodology TOOL public contract

## CLI compatibility surface

| Command | Contract |
|---|---|
| `dset new` | Create a profile-aware active change without overwrite |
| `dset check` | Read-only structural, artifact-area/hub, ID, portability, provenance, and lifecycle validation |
| `dset verify` | Run `check`, project-configured deterministic gates, and trace freshness |
| `dset trace` | Print by default; write or compare only with explicit flags |
| `dset archive` | Dry-run by default; execute only after archive readiness gates pass |

Stable diagnostic codes, command names, schema version 1.0, and trace ordering are public compatibility surfaces. Human-readable messages and non-contractual examples may improve compatibly.

### DSET-CONTRACT-TOOL-001 — Released utilities match declared platforms

| Field | Value |
|---|---|
| Authority | DSET maintainers |
| Source | Declared host/platform matrix and pinned runtime or host-format references |
| Version or digest | `1.0` |
| Direction | Released skill scripts and utilities to supported operating environments |
| Producer | DSET tool and skill release workflows |
| Consumer | Users on macOS, native Windows, WSL, and Linux |
| Conformance | Each released utility installs and runs on every declared platform with path/shell portability proof, or declares narrower applicability before release with an honest reason |
| Compatibility | Every matrix cell has executed proof or explicit honest `N/A`; generic Markdown validation is insufficient |
| Lifecycle | `active` |

### DSET-CONTRACT-TOOL-002 — Dependencies follow exact policy

| Field | Value |
|---|---|
| Authority | DSET maintainers; exception authority must also be named in the applicable policy |
| Source | Versioned dependency policy and pinned ecosystem, package, registry, license, and provenance sources |
| Version or digest | `1.0` |
| Direction | Dependency policy to implementation dependency selection and release proof |
| Producer | DSET dependency-policy owner and release workflow |
| Consumer | DSET implementations, contributors, package tooling, and release gates |
| Conformance | Policy records exact ecosystem/package/registry/license/version allowlists and denylists, sources, rationale, enforcement command, and exception authority/expiry; proof covers lockfiles, dependency resolution, licenses, and provenance |
| Compatibility | Every selected dependency is allowed and source-constrained; denied or expired-exception dependencies fail release |
| Lifecycle | `active` |

A mandated library is a Contract constraint, not a Decision. A consequential selection among alternatives that the Contract permits may be recorded as a Decision.
