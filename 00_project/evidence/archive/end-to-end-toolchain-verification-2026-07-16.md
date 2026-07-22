# End-to-end toolchain verification

- **Claim:** At implementation commit
  `c7c0038a19ee2b95bd9d51d2d903f130aca3166e`, the DSET Python distribution
  builds as a wheel, initializes and validates a schema 1.2 adopter without
  access to the source repository, persists a governed runtime invocation,
  installs all five source skills into isolated Codex and Claude layouts, and
  passes the complete local repository gate.
- **Current:** Yes for the local macOS, wheel, isolated-layout, deterministic
  runtime, and source-workflow claims. Native authenticated Codex/Claude
  invocation, hosted Linux/native-Windows execution, WSL execution, and real
  GitHub publication remain explicitly unproved.
- **Intended use:** Support `DSET-DECISION-SKILL-001`, close the local
  implementation portion of `DSET-TASK-TOOL-010`, and bound the remaining
  evidence work under `DSET-TASK-SKILL-020`, `DSET-TASK-TOOL-036`, and
  `DSET-TASK-OPS-025`.
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`
- **Reopen when:** Bootstrap inputs, the embedded bundle, CLI routing, runtime
  schemas, host distribution, release preparation/publication, supported
  Python versions, or any declared host/operating-system boundary changes.

## Delegated implementation review

Three independent subagents audited the accepted contracts and implemented
bounded slices before main-thread integration:

| Slice | Result |
|---|---|
| Contract/consistency audit | Located initialization, runtime, host, portability, and release obligations and identified the shared CLI integration boundary |
| Codex/Claude distribution | Added dry-run-first copy installation, digest verification, no-overwrite stops, and bounded invocation-receipt validation |
| Release integration | Added deterministic plan/check/prepare behavior plus an idempotent exact-merge-SHA GitHub publisher with collision stops |

The main integration added the packaged bootstrap transaction, persistent CLI
runtime bridge, OS matrix, WSL proof hook, clean-install wheel proof, and fixes
for Unicode repository paths, JSON gate isolation, generated bundle freshness,
and machine-local host-state isolation.

## Deterministic evidence

| Check | Result |
|---|---|
| `python -m unittest discover -s tests -v` | Pass: 129 tests |
| `ruff format --check dset_toolchain tests scripts` | Pass: 47 files |
| `ruff check dset_toolchain tests scripts` | Pass |
| `mypy dset_toolchain tests scripts` | Pass: 47 source files |
| `python -m dset_toolchain verify .` | Pass at the evaluated commit; canonical validation, configured gates, trace freshness, and diff hygiene passed |
| Wheel build | Pass with bundled setuptools 82.0.1; `dset_spec_loops-0.3.1-py3-none-any.whl` SHA-256 `187ec740d93d53414d656d39d307427d9342405674613eb44613854dc70e0945` |
| Wheel contents | Pass: embedded bootstrap bundle, CLI, runtime bridge, skill distribution, and release modules present |
| Clean wheel initialization | Pass in a repository path containing a space and Unicode; packaged source digest `efe8511ca1b15f68790c26f44ff25f6021961c3061e3b52d3c1a83653329eda8`; `dset verify --format json` returned `[]` |
| Runtime bridge from installed wheel | Pass: `diagnosis` resolved `core-v1:0.3:unmodified`; run `run-a6c28008359548e49bb6f56d14894ccc` persisted and finished `succeeded` |
| Isolated Codex distribution | Pass: five copied non-symlink skill folders with valid Codex metadata and invocation contracts |
| Isolated Claude distribution | Pass: five copied non-symlink skill folders with valid skill and invocation contracts |
| Release transaction | Pass: coordinated `0.3.1` surfaces, bootstrap declaration, and `v0.3.1` plan agree; local publisher collision/idempotency tests pass |
| Workflow syntax | Pass: Linux/macOS/native-Windows matrix, explicit self-hosted WSL hook, and post-merge publisher YAML parse locally |

PyPI access was unavailable through the app proxy, so the wheel used the
already bundled workspace build runtime rather than downloading a build
dependency. This does not alter the wheel payload or clean-install check.

## Native and hosted evidence boundary

The installed host executables were Codex CLI `0.144.4` and Claude Code
`2.1.202`. Fresh-process attempts were made without fabricating receipts:

- Codex created thread `019f6846-6d08-7933-810c-c16087847b74`, then both its
  WebSocket and HTTPS inference transports failed at the app proxy with 403.
- Claude created session `0e6ac89d-c839-4eda-aed4-294545e0ace6`, then stopped
  before inference with `403 Domain not in allowlist`.
- The Codex desktop sandbox also denied writes to the real `~/.codex/skills`
  and `~/.claude/skills` destinations, and its Computer Use policy denied both
  Terminal and Ghostty control.

Therefore no native invocation receipt was promoted. The isolated layouts
prove the distributable artifact and installer; an authenticated operator or
hosted run must still prove discovery, load, invocation, local-rule
resolution, handoff, and stop behavior on each real host.

The repository now defines GitHub-hosted Linux, macOS, and native-Windows
validation plus a labeled self-hosted WSL proof workflow. Only local macOS
execution is evidence in this record. Likewise, the post-merge publisher is
implemented and deterministically tested, but exact-SHA publication/retry/
collision evidence requires a real version-changing `dev` to `main` delivery.

## Bounded disposition

The CLI/runtime bridge, initialization transaction, portable host distributor,
coordinated release preparation, publisher source, and local wheel boundary are
implemented. Remaining distribution readiness is evidence work, not hidden
completion: native authenticated host proof, hosted OS/WSL runs, and real
GitHub release publication stay open in the owning tasks and verification
matrix.
