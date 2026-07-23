+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-236"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-078"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "A Release Plan is a maintained, internal Definition artifact because it directly states the intended release scope, conditions, sequence, and completion state rather than implementing or observing the release."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A Release Plan governs what the release is intended to contain and satisfy; release tooling is Method, delivered release assets are Implementation, and readiness or publication records are Observation."

[scope]
kind = "layer"
id = "governance"

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-076"
+++

# Requirement — Release Plan is a maintained Definition

A Release Plan declares:

```toml
artifact_type = "maintained"
content_role = "definition"
authority_origin = "internal"
```

It defines the intended release scope, entry conditions, ordered release work,
completion conditions, and release target.

Related artifacts remain distinct:

- release scripts and procedures are maintained Methods;
- packaged or published release assets are maintained Implementations;
- readiness evidence and the Release Record are Observations.
