+++
artifact_type = "analysis_report"
artifact_subtype = "proposal"
llm_session_ids = []
+++

# Proposal — {{title}}

- **Change ID:** `{{change_id}}`
- **Profile:** `{{profile}}`
- **Target package:** `{{package_id}}`
- **Implementing PR:** pending
- **Status:** proposed

## Problem

- **Problem ID:** pending
- **Statement:** Describe what is wrong or may cause harm.
- **Evidence/observation:** Link the smallest useful evidence.
- **Impact:** State who or what is affected.
- **Owner and state:** pending

For an observed defect, add reproduction and severity. For a possible future
harm, add likelihood, trigger, and mitigation. Add further analysis only when
the selected risk profile requires it.

## Outcome

Describe the accepted end state.

## Scope

- List included behavior and artifacts.

## Non-goals

- List deliberate exclusions.

## Risk

Select and justify the review profile. State applicable runtime, data, security,
rollout, and governance triggers; do not expand a low-risk Problem into a large
form without a triggered need.
