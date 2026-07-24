"""Provide DSET skill catalog behavior."""

from __future__ import annotations

# PUBLIC_SKILL_WORKFLOWS defines public skill workflows; this module owns the default.
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
    "dset-compile": "compile",
    "dset-plan-proof": "plan-proof",
    "dset-plan-implementation": "plan-implementation",
    "dset-implement": "implement",
    "dset-verify": "verify",
    "dset-configure": "configure",
    "dset-overview": "overview",
    "dset-triage": "work-triage",
    "dset-release": "release",
    "dset-complete": "complete",
}

# PUBLIC_SKILL_MODES defines public skill modes; this module owns the default.
PUBLIC_SKILL_MODES = {
    "dset": None,
    "dset-init": "initialize",
    "dset-repair-governance": "repair-governance",
    "dset-decompose": "decompose",
    "dset-diagnose": "diagnose",
    "dset-clarify": "clarify",
    "dset-landscape": "landscape",
    "dset-prototype": "prototype",
    "dset-decisions": "decisions",
    "dset-compile": "compile",
    "dset-plan-proof": "plan-proof",
    "dset-plan-implementation": "plan-implementation",
    "dset-implement": "implement",
    "dset-verify": "verify",
    "dset-configure": "configure",
    "dset-overview": "overview",
    "dset-triage": "triage-work",
    "dset-release": "release",
    "dset-complete": "complete",
}

# PRE_RESOLUTION_SKILLS defines pre resolution skills; this module owns the default.
PRE_RESOLUTION_SKILLS = frozenset({"dset-init", "dset-repair-governance"})

# SKILL_INVOCATION_MARKERS defines skill invocation markers; this module owns the default.
SKILL_INVOCATION_MARKERS = {
    skill_id: f"skills context --skill {skill_id} --target TARGET"
    for skill_id in PUBLIC_SKILL_WORKFLOWS
}

# REGISTERED_SKILL_WORKFLOWS defines registered skill workflows; this module owns the default.
REGISTERED_SKILL_WORKFLOWS = {
    skill_id: workflow_id
    for skill_id, workflow_id in PUBLIC_SKILL_WORKFLOWS.items()
    if skill_id not in PRE_RESOLUTION_SKILLS
}
