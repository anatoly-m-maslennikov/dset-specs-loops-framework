from __future__ import annotations

PUBLIC_SKILL_WORKFLOWS = {
    "dset": "lifecycle-orchestration",
    "dset-init": "initialize",
    "dset-repair-governance": "repair-governance",
    "dset-decompose": "decompose",
    "dset-diagnose": "diagnosis",
    "dset-clarify": "domain-clarification",
    "dset-landscape": "landscape",
    "dset-prototype": "prototyping",
    "dset-decisions": "decisions",
    "dset-plan-proof": "plan-proof",
    "dset-plan-implementation": "plan-implementation",
    "dset-implement": "implement",
    "dset-verify": "verify",
    "dset-triage": "work-triage",
    "dset-release": "release",
    "dset-complete": "complete",
}

PRE_RESOLUTION_SKILLS = frozenset({"dset-init", "dset-repair-governance"})

SKILL_INVOCATION_MARKERS = {
    skill_id: f"rules resolve {workflow_id} --format json"
    for skill_id, workflow_id in PUBLIC_SKILL_WORKFLOWS.items()
    if skill_id not in PRE_RESOLUTION_SKILLS
}
SKILL_INVOCATION_MARKERS.update(
    {
        "dset-init": "init TARGET --project-key KEY",
        "dset-repair-governance": "rules check --root ROOT --format json",
    }
)

REGISTERED_SKILL_WORKFLOWS = {
    skill_id: workflow_id
    for skill_id, workflow_id in PUBLIC_SKILL_WORKFLOWS.items()
    if skill_id not in PRE_RESOLUTION_SKILLS
}
