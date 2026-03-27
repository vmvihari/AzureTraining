# Monitoring Overview

## Goals of Monitoring

The primary goal of monitoring is to ensure the availability, performance, and reliability of your infrastructure. For Virtual Machines, we focus on three key metrics:

1.  **CPU Usage**: Tracking processor load to identify bottlenecks or runaway processes.
2.  **Memory Usage**: Monitoring RAM consumption to prevent OOM (Out of Memory) errors.
3.  **Logs**: Collecting system and application logs for troubleshooting and auditing.

## VM Monitoring Setup

Monitoring is essential for both Linux and Windows environments. Enabling monitoring insights in Azure automatically installs the necessary agents (Azure Monitor Agent) on the VMs.

### Linux Monitoring
-   **Key Metrics**: Load average, CPU user/system time, free memory, disk I/O.
-   **Tools**: `top`, `htop`, `vmstat`.
-   **Stress Testing**: The `stress` utility is commonly used to artificially increase CPU load to test alert triggers.
    ```bash
    # Example: Stress 2 CPU cores for 60 seconds
    stress --cpu 2 --timeout 60
    ```

### Windows Monitoring
-   **Key Metrics**: CPU usage, Available Memory, Disk Queue Length.
-   **Tools**: Task Manager, Resource Monitor, Performance Monitor (PerfMon).
-   **Stress Testing**: Tools like `CPUStres` (from Sysinternals) can simulate high load.

## Data Collection

To effectively monitor these metrics, Azure uses **Data Collection Rules (DCR)**. These rules define:
-   **What** data to collect (Performance Counters, Event Logs, Syslog).
-   **Where** to send the data (Log Analytics Workspace).
-   **Which** resources to target (Specific VMs or Resource Groups).

> [!NOTE]
> When configuring Data Collection Rules, ensure the Resource Group and the Log Analytics Workspace are in the same region for optimal performance and compliance.
