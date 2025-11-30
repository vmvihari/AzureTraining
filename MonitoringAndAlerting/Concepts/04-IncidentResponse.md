# Incident Response

## Alert Lifecycle

1.  **Trigger**: Metric exceeds threshold (e.g., CPU > 90%).
2.  **Notification**: Action Group sends email/SMS/Webhook.
3.  **New State**: Alert appears in the Azure Portal dashboard with status "New".
4.  **Acknowledgment**: Engineer reviews the alert and changes status to "Acknowledged".
5.  **Resolution**:
    -   **Auto-Resolve**: If the metric returns to normal, Azure automatically changes status to "Resolved".
    -   **Manual Resolve**: If the issue persists or requires manual intervention, the engineer resolves it after fixing the root cause.

## Triage Process

When an alert is received, the monitoring engineer must perform triage to determine the root cause and appropriate action.

### Workflow
1.  **Verify**: Check if the alert is a false positive or a real issue.
2.  **Diagnose**: Log into the VM to identify the resource hog.
    -   **OS Level**: Is it a system process (e.g., Windows Update, backup agent)?
    -   **App Level**: Is it a specific application (e.g., Java, SQL Server)?
3.  **Remediate**:
    -   **Restart**: Restart the service or process.
    -   **Scale**: If load is legitimate and persistent, consider upsizing the VM.
    -   **Escalate**: If the issue is complex, assign to the relevant team.

## Roles and Responsibilities

### Monitoring Team / L1 Support
-   Receives all initial alerts.
-   Performs basic triage and categorization.
-   Assigns tickets to specialized teams (Linux, Windows, Database, Application).

### Cloud Operations vs. DevOps
-   **Cloud Operations**: Focuses on manual recovery tasks, patching, and infrastructure maintenance.
-   **DevOps**: Focuses on automation. If a VM fails, a DevOps approach might be to automatically redeploy it via a pipeline rather than manually fixing it.

### Escalation Matrix
-   **Level 1**: Initial triage (15 mins).
-   **Level 2**: Deep dive troubleshooting (1 hour).
-   **Level 3**: Vendor support (Microsoft) or Senior Architects.
