# Monitoring and Alerting

## Overview

Effective monitoring and alerting are crucial for maintaining the health, performance, and security of your Azure infrastructure. This module covers the setup of monitoring for Virtual Machines (Linux and Windows), configuring alerts, managing logs with Log Analytics, and incident response workflows.

## Table of Contents

### Concepts

1. [Monitoring Overview](./Concepts/01-MonitoringOverview.md) - Goals, VM monitoring, and stress testing
2. [Alerting Basics](./Concepts/02-AlertingBasics.md) - Alert rules, action groups, and integrations
3. [Log Analytics](./Concepts/03-LogAnalytics.md) - Workspace setup, Data Collection Rules (DCR), and KQL
4. [Incident Response](./Concepts/04-IncidentResponse.md) - Alert lifecycle, triage, and escalation
5. [Tools and Cost](./Concepts/05-ToolsAndCost.md) - Cost management and third-party tools
6. [Azure Alerts Deep Dive](./Concepts/06-AzureAlertsDeepDive.md) - Detailed breakdown of Alert Rules, Signals, and Action Groups

### Labs

1. [Lab 1: Create a Basic CPU Alert](./Labs/Lab01-BasicCPUAlert.md) - Hands-on practice with Azure Monitor Alerts

## Key Takeaways

- **Centralized Logging**: Log Analytics Workspace serves as the single source of truth for logs.
- **Alerting Strategy**: Use tiered thresholds (Warning vs. Critical) to manage noise.
- **Cost Awareness**: Azure alerts cost money per rule; open-source tools like Grafana are popular alternatives.
- **Incident Workflow**: Define clear escalation paths from L1 to L2/L3 support.
- **Role Clarity**: Understand the difference between Cloud Ops (manual) and DevOps (automated) recovery.
