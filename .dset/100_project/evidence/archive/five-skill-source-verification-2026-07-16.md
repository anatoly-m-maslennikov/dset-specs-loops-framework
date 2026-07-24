# Five-skill source verification

- **Claim:** The repository owns five thin, registered DSET source skill packages, and governance materialization installs exactly the applicable subset without copying substantive project rules into the wrappers.
- **Evaluated commit:** `691f66da56e65c585b3b0e863f9d2b2e062dd780`.
- **Current:** Yes. This proof document is a documentation-only successor to the evaluated source and test commit.
- **Intended use:** Support the source-wrapper portion of `DSET-DECISION-SKILL-001`; it does not prove the runtime adapter, release publisher, declared agent hosts, or native operating-system matrix.
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`
- **Reopen when:** A source wrapper, wrapper metadata, workflow closure, governance profile, materializer, resolver, or wrapper/self-host test changes.

## One skill, one subagent

| Skill | Owning subagent | Source package result | `SKILL.md` SHA-256 |
|---|---|---|---|
| `dset` | `/root/skill_dset` | Skill Creator validation passed; 22-line primary wrapper | `52d0aa1298a533fa6e967fa02e9502abb091ba30d2d2a4755c105111d4b1bcfd` |
| `dset-clarify` | `/root/skill_clarify` | Skill Creator validation passed; 21-line specialist wrapper | `b2dcb6dde2349d007b0a3f8716afd0ca3a34e73620767b60abdd21756fffff45` |
| `dset-diagnose` | `/root/skill_diagnose` | Skill Creator validation passed; 21-line specialist wrapper | `edba755b23ff6729a89837c97c8e2fdf6d4658b2b8c90e1d73e52f08a8529d8f` |
| `dset-prototype` | `/root/skill_prototype` | Skill Creator validation passed; 21-line specialist wrapper | `9c23ddb14fc6e94d4e858b8dc367df2a919e9a6814d8ff9af166d1478b5aa3c4` |
| `dset-release` | `/root/skill_release` | Skill Creator validation passed; 21-line guarded wrapper | `3a33128c7ce6d444a805e989e78129f1ae9450706795e67b753509b19bb8238c` |

Each subagent changed only its assigned package. The main integration registered hashes, completed workflow dependency closures, added applicability-aware materialization, and extended deterministic and recursive coverage.

## Deterministic evidence

| Check | Result |
|---|---|
| `python -m unittest discover -s tests` | Pass: 84 tests |
| `.venv/bin/ruff format --check dset_toolchain tests` | Pass |
| `.venv/bin/ruff check .` | Pass |
| `.venv/bin/mypy dset_toolchain` | Pass |
| `python -m dset_toolchain check .` | Pass |
| `python -m dset_toolchain self-host .` | Candidate repository and temporary adopter pass; four applicable adopter workflows resolve; every installed wrapper remains unchanged after local rule customization; recursion stops; the released-validator boundary remains the declared bootstrap transition |
| Canonical `dset verify .` | Pass |
| `python -m dset_toolchain trace . --check` | Pass after trace regeneration |
| `git diff --check` | Pass |

The release-applicable materialization test installs and resolves all five wrappers. The ordinary temporary adopter declares release not applicable, so it omits the release workflow and wrapper while retaining the other four. This is profile-driven applicability, not missing capability.

## Bounded disposition

The repository-native source skill surface is implemented. `DSET-TASK-TOOL-010` remains open for the runtime adapter, run/checkpoint persistence, executable release/version mechanics, and publication automation. `DSET-TASK-SKILL-020` remains open for real installation, discovery, load, invocation, handoff, and stop proof on every declared agent host. Cross-platform execution proof remains separately open.
