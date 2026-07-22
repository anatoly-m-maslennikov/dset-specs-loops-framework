# Supportability

**Rule ID:** `DSET-RULE-SUPPORTABILITY`

## Rules

OPS accepts and operates production-bound behavior only when the implemented
surface supports profile-scaled incident triggers or objectives,
operator-usable evidence, correlation and deploy/change identity, safe
read-only diagnostics and permissions, data retention/redaction/access/deletion
controls, volume/cardinality/sampling bounds, runbook and escalation paths,
rollback or kill-switch operation, and incident-to-requirement/change/PR/fix
traceability.

Telemetry is diagnostic evidence, not a second business-state authority. Stateless services use their database or broker authorities; modest-write local tools may use declared files; higher-write or concurrent local tools select an appropriate database. Add tracing, WAL, reconciliation, durable execution, or audited access only when the runtime risk and topology require them.

Non-production behavior may mark supportability not applicable only with a concrete reason.

IMPL owns the concrete diagnostic emission, interfaces, and recovery hooks.
OPS owns runtime use, retention, access, deletion, investigation, containment,
recovery, and escalation. If the implementation surface is insufficient, OPS
records the gap through an appropriate upstream artifact and waits for a later
implementation; it never creates backward OPS-to-IMPL authority.
