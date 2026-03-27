# Azure Alerts Deep Dive

## Introduction

Azure Alerts are a critical component of Azure Monitor, allowing you to stay informed about the state of your infrastructure and applications. Instead of constantly watching dashboards, you can configure alerts to proactively notify you when issues arise.

In this document, we explore the core concepts required to set up a basic CPU alert, explaining how the different components of Azure Monitor work together.

## The Alerting Workflow

The process of triggering an alert involves several logical steps:

1.  **Resource**: The target Azure resource (e.g., a Virtual Machine) generates data.
2.  **Signal**: The specific data being monitored (e.g., CPU Percentage, Disk IO, or a specific Log entry).
3.  **Alert Rule**: A logical rule that constantly checks the signal against a **Threshold**.
4.  **Action Group**: A defined collection of notification preferences (e.g., "Email the IT Admin") that triggers when the rule is met.
5.  **Notification**: The actual email, SMS, or webhook call sent to the user.

## Component Breakdown

### 1. Monitoring Agents (Insights)

To monitor the guest operating system of a Virtual Machine (e.g., memory usage, internal process CPU), you often need to install a monitoring agent.
*   **Azure Monitor Agent (AMA)**: The modern agent that collects monitoring data from the guest OS and delivers it to Azure Monitor.
*   **VM Insights**: A feature that streamlines the installation and configuration of agents to provide a pre-defined set of performance metrics and logs.

### 2. Metrics

Metrics are numerical values that describe some aspect of a system at a particular time. They are lightweight and capable of near-real-time scenarios.
*   **CPU Percentage**: A common metric indicating how busy the processor is.
*   **Aggregation**: Since metrics are collected frequently (e.g., every second), we "aggregate" them over a time window (e.g., "Average over the last minute") to make sense of the data.

### 3. Alert Logic

When defining an Alert Rule, you configure the logic that determines "Bad" behavior.
*   **Operator**: Defines the comparison (e.g., "Greater than").
*   **Threshold**: The limit value (e.g., "50%").
*   **Granularity**: How often the data is sampled and averaged (e.g., "1 minute").
*   **Frequency**: How often the alert system runs the check (e.g., "Every 1 minute").

**Example Logic**: "Trigger if the **Average** CPU Percentage is **Greater than 50** over the last **5 minutes**, checking every **1 minute**."

### 4. Action Groups

An Action Group is a reusable object. You define it once (e.g., "Operations Team") and attach it to multiple alert rules.
*   **Types**: Email/SMS, Push Notifications, Voice calls.
*   **Automation**: Trigger Azure Functions, Logic Apps, or Webhooks to auto-remediate issues (e.g., restart a service if CPU is high).

## Use Case: CPU Stress Alerting

In the associated lab, we simulate a high-load scenario. By artificially "stressing" the CPU, we force the metric to cross the defined threshold. This validates that:
1.  The Agent is reporting data.
2.  The Alert Rule is evaluating correctly.
3.  The Action Group is successfully delivering mail.

This "Fire Drill" approach is essential for verifying that your monitoring strategy works *before* a real incident occurs.
