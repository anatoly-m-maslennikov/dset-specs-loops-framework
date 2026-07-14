# Eval plan — DSET v1

## Applicability

Applicable. The CLI is deterministic, but resumability, diagnostic usefulness, migration clarity, and skill routing require qualitative evaluation.

## Cases and thresholds

| Eval ID | Case | Threshold |
|---|---|---|
| **DSET-V1-EVAL-001** | Resume `operationalize-dset-v1` using repository files only | An evaluator locates current status, next task, proof obligations, and PR identity without chat context |
| **DSET-V1-EVAL-002** | Diagnose a failed `dset verify` and a blocked `dev → main` delivery | The evaluator identifies the failing boundary, authoritative evidence, and safe recovery action without guessing or mutating production state |
| **DSET-V1-EVAL-003** | Route ambiguous-domain, defect-diagnosis, and disposable-experiment prompts | All prompts select the intended distinct skill and stop at its authorization boundary |
| **DSET-V1-EVAL-004** | Migrate a repository with separate spec, test-plan, eval-plan, and implementation-plan roots | The evaluator produces one writable `dset/` root and an explicit map for retained read-only history without losing test/eval separation |

## Evidence

Store prompts, evaluator outputs, disagreements, and corrective loops under `proofs/`. Do not label deterministic fixture execution as an eval.
