# Lab: Create a Basic CPU Alert for an Azure Virtual Machine

## Lab Overview

In this lab, you will learn how to configure a basic alert rule in Azure Monitor. You will create a Virtual Machine, enable monitoring, configure an alert to trigger when CPU usage exceeds a threshold, and verify the alert by artificially increasing the CPU load.

## Learning Objectives

By the end of this lab, you will be able to:
- Enable Insights (monitoring) for an Azure Virtual Machine
- Create an Action Group for email notifications
- Configure a metric-based Alert Rule for CPU usage
- Trigger an alert using a stress test tool
- Verify alert notifications

## Prerequisites

- Active Azure subscription
- Basic understanding of Azure Portal navigation

## Estimated Time to Complete

⏱️ **30-45 minutes**

---

## Part 1: Create a Virtual Machine

**Objective**: Deploy a VM to monitor. If you already have a VM, you can skip this part.

### Steps

1.  Log in to the [Azure Portal](https://portal.azure.com).
2.  Search for **"Virtual Machines"** and click **"Create"**.
3.  Configure the following settings:
    -   **Image**: Ubuntu Server 20.04/22.04 LTS or Windows Server 2019/2022 (your choice).
    -   **Size**: **Standard_B1s** (recommended for low cost).
    -   **Authentication**:
        -   **Linux**: SSH public key or Password.
        -   **Windows**: Password.
4.  **Disks** and **Networking**: Leave default options.
5.  Click **"Review + Create"** and then **"Create"**.
6.  Wait for the VM to deploy successfully.

---

## Part 2: Enable Monitoring (Insights)

**Objective**: Install the monitoring agent to collect metrics.

### Steps

1.  Navigate to your VM in the Azure Portal.
2.  In the left menu, under **Monitoring**, select **Insights**.
3.  Click **Enable** (if not already enabled).
4.  Wait **1–2 minutes** for Azure to install the monitoring agent in the background.

---

## Part 3: Create an Action Group

**Objective**: Define *who* gets notified when an alert triggers.

### Steps

1.  Go to your VM's menu.
2.  Under **Monitoring**, click **Alerts**.
3.  Click **Action groups** (top menu) > **Create**.
4.  **Basic Details**:
    -   **Action group name**: `basic-ag`
    -   **Display name**: `basicAG`
    -   **Subscription** and **Resource group**: Select your VM’s resource group.
5.  **Notifications**:
    -   **Notification type**: Email/SMS message/Push/Voice.
    -   **Name**: `emailAlert`
    -   **Email**: Enter your email address.
6.  Click **Review + Create** and then **Create**.

---

## Part 4: Create an Alert Rule (CPU Percentage)

**Objective**: Define *what* condition triggers the alert.

### Steps

1.  Go back to the VM’s **Alerts** page.
2.  Click **Create** > **Alert rule**.
3.  **Scope**: Should already show your VM. If not, select your VM manually.
4.  **Condition**:
    -   Click the **Condition** tab (or "Add condition").
    -   **Signal name**: Select **Percentage CPU**.
    -   **Alert Logic**:
        -   **Operator**: Greater than
        -   **Threshold value**: `50`
        -   **Aggregation granularity**: Average
        -   **Frequency of evaluation**: 1 minute (or 5 minutes)
5.  **Actions**:
    -   Select **Use existing action group**.
    -   Select the group you created: `basic-ag`.
6.  **Details**:
    -   **Alert rule name**: `vm-cpu-alert`
    -   **Severity**: `3 - Warning`
7.  Click **Review + Create** and then **Create**.

---

## Part 5: Trigger the Alert

**Objective**: Artificially increase CPU load to test the alert.

### Option A: Linux VM

1.  **SSH** into your VM.
2.  Update package lists and install the stress tool:
    ```bash
    sudo apt-get update
    sudo apt-get install stress -y
    ```
3.  Run a CPU load test for 60 seconds:
    ```bash
    stress --cpu 2 --timeout 60
    ```

### Option B: Windows VM

1.  **RDP** into your VM.
2.  Download a simple CPU stress tool (e.g., `CPUStres` from Sysinternals or any lightweight alternative).
3.  Start the tool and generate a high CPU load for at least **1 minute**.

> [!NOTE]
> Wait **3–5 minutes** after starting the stress test for Azure Monitor to detect the high CPU usage and trigger the alert.

---

## Part 6: Verify Alert

**Objective**: Confirm the alert system works as expected.

### Expected Results

1.  **Email Notification**: You should receive an email from Azure Monitor stating that the CPU is above 50%.
2.  **Portal Status**: In the **Alerts** section of your VM, you should see a new alert with severity "Warning".
3.  **Recovery**: After the stress test stops, the CPU usage will drop. Depending on configuration, you might receive a resolution email, or the alert state in the portal will change to "Resolved".

---

## Lab Cleanup

> [!IMPORTANT]
> To avoid unnecessary costs, delete the resources if you are done with the lab.

1.  Delete the **Alert Rule**.
2.  Delete the **Action Group**.
3.  Delete the **Virtual Machine** and its associated resources (Disk, NIC, IP) or the entire **Resource Group** if created specifically for this lab.

---

## Submission Requirements (Self-Check)

If you were submitting this as an assignment, you would capture:
1.  VM Overview page.
2.  Action Group configuration.
3.  Alert Rule settings.
4.  The received Email notification.
5.  The command/tool running the CPU load.
