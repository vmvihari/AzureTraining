# Alerting Basics

## Alert Rules

Alert rules define the conditions that trigger a notification. A tiered approach helps distinguish between minor issues and critical failures.

### Recommended Thresholds

| Severity | Threshold | Description | Action |
| :--- | :--- | :--- | :--- |
| **Warning** | 60% CPU | Elevated load, potential issue developing. | Monitor closely, check for planned tasks. |
| **Warning** | 80% CPU | High load, performance impact likely. | Investigate active processes. |
| **Critical** | 90% CPU | Severe congestion, service degradation imminent. | Immediate intervention required. |

> [!IMPORTANT]
> Azure charges for each alert rule you create. Be strategic about what you monitor to control costs.

## Action Groups

An **Action Group** is a reusable collection of notification preferences. When an alert triggers, it notifies the associated Action Group.

### Notification Types
-   **Email/SMS/Push/Voice**: Direct notifications to engineers.
-   **Azure Function/Logic App**: Trigger automated remediation scripts.
-   **Webhook**: Integrate with third-party tools.
-   **ITSM**: Create tickets in tools like ServiceNow or Jira.

## Integrations

### PagerDuty
PagerDuty is a popular incident response platform.
-   **On-Call Schedules**: Rotates responsibility among team members.
-   **Escalation Policies**: Automatically escalates unacknowledged alerts (e.g., if on-call engineer doesn't respond in 15 mins, notify manager).
-   **Integration**: Connects via Webhook from Azure Monitor.

### Ticketing Systems (Jira / Remedy Force)
-   **Automation**: Alerts can automatically create tickets.
-   **Tracking**: Provides an audit trail of incidents and resolutions.
-   **Reduction of Email Noise**: Moves alerts from inboxes to structured workflows.

## Multi-VM Behavior

When a single alert rule is applied to multiple VMs (e.g., a dynamic scope based on Resource Group):
-   The rule monitors all VMs in the scope.
-   If **VM-A** spikes to 95%, the alert notification will specifically identify **VM-A** as the source.
-   You do not need separate rules for each VM, which simplifies management and reduces costs.
