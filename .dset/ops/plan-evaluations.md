# Methodology OPS qualitative eval plan

Applicable qualitative and probabilistic proof is layer-owned. The representative scenario set is maintained by META; each row below owns its criterion and threshold.

| Eval ID | Criterion | Threshold |
|---|---|---|
| **DSET-EVAL-OPS-001** | Diagnostic usefulness | For both supportability scenarios, an independent operator can use only synthetic redacted evidence and the runbook to diagnose the likely failure boundary, choose a safe containment/escalation/rollback action, and locate the governing requirement, change, PR, and fix record |
| **DSET-EVAL-OPS-002** | Release classification | Every reviewer selects the specified bootstrap, normal, small, RC, final, or post-1.0 class/target or stops on material ambiguity; none promotes 1.0 arithmetically |
| **DSET-EVAL-OPS-003** | Release restraint | Every reviewer refuses RC/final publication when a required gate is absent, names the owning correction surface, and does not weaken the release threshold |
| **Historical DSET-EVAL-OPS-010** | Delivery artifact boundaries | Delivery-name interpretation is superseded by cross-layer `DSET-EVALUATION-GOV-029` |

## Calibration and evidence

Use at least two independent reviewers for a baseline where interpretation matters. Record disagreements by case and criterion, and correct the earliest ambiguous owner rather than averaging incompatible results.
