# Eval plan — Add artifact governance profiles

## Applicability

Applicable. Navigation usefulness, artifact classification, semantic dependency order, and profile selection require human/agent judgment.

## Cases and thresholds

| Eval ID | Case | Threshold |
|---|---|---|
| **DSET-EVAL-PLAN-GOV-007** | Cold-start helicopter navigation | A reviewer locates the framework purpose, methodology stages, artifact-type owner, authoring rule, rationale, and maintenance procedure from hubs within three minutes without using repository search |
| **DSET-EVAL-PLAN-META-002** | Artifact classification | Given six mixed requests, a reviewer selects hub, normative reference, rationale, Decision record, playbook/runbook, or evidence without assigning the same rule to two artifacts |
| **DSET-EVAL-PLAN-META-003** | Specification dependency order | A reviewer detects undefined forward dependencies, distinguishes connections from definitions, and produces a domain-entity/lifecycle ordering that can be read top-to-bottom |
| **DSET-EVAL-PLAN-GOV-008** | Orthogonal profile selection | Python code, TypeScript code, documentation-only governance, and mixed repositories select implementation-language and artifact profiles independently with no inherited Python thresholds for documents |

## Evidence

Store prompts, reviewer routes, disagreements, timing, and corrective loops under `proofs/`. Run at least two independent reviewers across the four cases. Do not label deterministic link or schema checks as evals.
