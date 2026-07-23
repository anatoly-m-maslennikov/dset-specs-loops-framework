# Applied IMPL qualitative Evaluation plan

The accepted QA atom owns the criterion and threshold. Implementation prompts,
case sets, runs, evidence, and Verification remain separate carriers.

| Evaluation ID | Governed claims | Definition and case set | Required execution |
|---|---|---|---|
| **DSET-EVALUATION-IMPL-001** | `DSET-REQ-IMPL-005`, `DSET-REQ-001` | `DSET-EVALUATION-IMPL-001-agent-skills-profile.md`; `030_dset-implementation-evaluations-skill-cases.toml` | Run every affected skill's trigger, non-trigger, ambiguous-routing, and applicable adversarial cases independently for each provider/host/model matrix cell actually claimed; reconcile only matching identities and preserve unsupported or inconclusive cells. |

The current case catalog defines 54 minimum routing cases for 18 public skills.
It is definition input, not execution evidence. No provider, host, or model cell
is considered evaluated until independent result evidence and Verification are
fresh for the exact skill, adapter, configuration, and target revision.
