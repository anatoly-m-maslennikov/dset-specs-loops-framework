# Eval plan — Bootstrap the DSET project structure

## Applicability

Applicable. Folder discoverability and ownership clarity are qualitative even though tree shape and links are deterministic.

## Cases

1. A new contributor seeks accepted methodology requirements.
2. A contributor starts one bounded methodology change.
3. A reviewer distinguishes current truth from unaccepted deltas.
4. A maintainer determines whether a global spec layer is needed.
5. An agent resumes the bootstrap without chat history.

## Criteria

| Eval ID | Criterion | Threshold |
|---|---|---|
| **BOOT-EVAL-001** | Findability | Every reviewer locates the correct path for all five cases without private instructions |
| **BOOT-EVAL-002** | Ownership | No reviewer treats `changes/` as accepted truth or `methodology/` as duplicated project truth |
| **BOOT-EVAL-003** | Proportionality | Reviewers find the one-package tree sufficient and do not require an empty global layer |
| **BOOT-EVAL-004** | Resumability | An agent can identify completed work, pending PR/archive gates, and the next task from repository files alone |

## Evidence

Record independent reviewer results and disagreements in `verification.md`. Do not substitute a successful link check for this qualitative evaluation.
