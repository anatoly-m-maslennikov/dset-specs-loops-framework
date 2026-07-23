+++
artifact_id = "DSET-ATOMIC-RECORD-196"
semantic_id = "DSET-REQUIREMENT-IMPL-006"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:implementation"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET provides and applies a provider-neutral LLM Evaluation implementation profile to every Evaluation definition, prompt, harness, grader, reconciliation procedure, and result carrier it creates or updates."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Evaluation conclusions are trustworthy only when their objective, cases, rubric, threshold, run configuration, independence, calibration, evidence, and limitations are explicit and reproducible across the providers actually claimed."

[promotion]
affected_children = ["implementation"]
applies_unchanged = false
local_context_required = true

[promotion.parent_scope]
kind = "project"
id = "dset-specs-loops-framework"

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-001"
+++

# Requirement — Apply the LLM Evaluation profile

Every Evaluation states the governed claim, objective, exact subject and
revision, representative distribution, edge and failure cases, rubric,
threshold, grading and reconciliation method, tools, permissions, budget, and
required evidence before execution.

Use deterministic grading for deterministic facts. Use human or model judgment
only for criteria that genuinely require it, with a precise rubric and
calibration against reviewed examples. Independent runs do not share prior
answers. Each result records effective provider, model, configuration, prompt
and dataset identity, exclusions, disagreement, uncertainty, and possible
defeaters. Definitions, executions, evidence, and Verification remain separate.

The profile is host-neutral. Evaluation matrices cover only provider/model/host
configurations the project actually claims, and one provider's passing result
cannot establish universal behavior.
