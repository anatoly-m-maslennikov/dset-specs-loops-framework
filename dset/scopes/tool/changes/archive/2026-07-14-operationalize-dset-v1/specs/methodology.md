# Methodology delta specification

## ADDED — DSET-REQUIREMENT-TOOL-001 Executable canonical workflow

The framework must provide one dependency-light, cross-platform canonical command with `new`, `check`, `verify`, `trace`, and `archive` workflows. Read-only validation is the default; writes must be explicit and must not overwrite existing work.

**Scenario DSET-SCENARIO-TOOL-001:** A contributor with a supported Python runtime can validate an adopting repository from its root without installing OpenSpec or another methodology.

## ADDED — DSET-REQUIREMENT-TOOL-002 Machine-readable contracts and fixtures

The framework must release versioned schemas, templates, and fixtures for the project manifest, accepted package truth, change manifest, artifact set, archive readiness, and traceability graph. Fixtures must include valid small, standard, failed-active, and archived changes plus representative invalid cases.

**Scenario DSET-SCENARIO-TOOL-002:** The validator accepts every released valid fixture and rejects each invalid fixture with a stable diagnostic code.

## ADDED — DSET-REQUIREMENT-TOOL-003 Deterministic PR traceability

The toolchain must generate a stably ordered `dset/traceability.yaml` from committed change metadata and repository-qualified PR references. The index may cache PR number, URL, state, merge commit, requirements, tests, evals, Decisions, and evidence paths, but GitHub remains authoritative for PR state and code diffs.

**Scenario DSET-SCENARIO-TOOL-003:** Regenerating traceability without source changes produces no diff, and archived changes resolve to the PRs that own their implementation history.

## ADDED — DSET-REQUIREMENT-TOOL-004 Safe archive transaction

The archive command must reject a change without complete artifacts, fresh verification, accepted-truth reconciliation, a repository-qualified PR identity, and an archive-ready status. It must refuse overwrites and move the change only after all local gates pass.

**Scenario DSET-SCENARIO-TOOL-004:** A failed or merely proposed change remains active; a verified change with an existing archive destination is rejected without modifying either path.

## ADDED — DSET-REQUIREMENT-SKILL-001 Focused portable skills

The framework must publish three distinct repository-native skills: pre-spec domain grilling, evidence-first diagnosis, and disposable prototyping. Each skill must have a distinct trigger, output, verification step, stop condition, and portable installation contract.

**Scenario DSET-SCENARIO-SKILL-001:** An agent can select one skill for an ambiguous domain, a different skill for a defect investigation, and a third for a disposable design experiment without invoking a competing spec or implementation methodology.

## ADDED — DSET-REQUIREMENT-OPS-007 Delivery automation is supportable

Repository production supportability must include the GitHub-hosted PR policy and auto-merge workflow. GitHub PRs, checks, rulesets, workflow logs, and commit identities are authoritative operational evidence; the repository must document bounded diagnostics and recovery without treating local files as a competing runtime authority.

**Scenario DSET-SCENARIO-OPS-007:** Given a blocked or incorrect delivery, an operator can locate the PR, policy check, workflow run, ruleset, head commit, and safe recovery action from public repository documentation.
