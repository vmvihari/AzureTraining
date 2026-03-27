# Homework: Create a Basic CPU Alert for an Azure Virtual Machine

## Objective

To help you understand how Azure Alerts work by creating a single basic alert rule for CPU usage on one Virtual Machine and sending a notification to your email.

## Prerequisites

*   Active Azure Subscription.
*   Access to Azure Portal.

---

## Part 1: Create a Virtual Machine

*(If you already have a VM, you may use it and skip to Part 2.)*

### Steps

1.  Login to [Azure Portal](https://portal.azure.com).
2.  Search for **"Virtual Machines"** and click **"Create"**.
3.  Choose:
    *   **Image**: Ubuntu or Windows (your choice)
    *   **Size**: Any small size (**B1s** recommended for low cost)
    *   **Authentication**:
        *   **Linux**: SSH key or password
        *   **Windows**: Password
4.  Leave default options for **Disk** and **Networking**.
5.  Click **"Review + Create"** and then **"Create"**.
6.  Wait for the VM to deploy successfully.

---

## Part 2: Enable Monitoring (Insights)

### Steps

1.  Open your VM from the Azure Portal.
2.  In the left menu, find **Monitoring** > **Insights**.
3.  Click **Enable** (if not already enabled).
4.  Wait **1–2 minutes** for Azure to install the monitoring agent in the background.

---

## Part 3: Create an Action Group

This defines *how* alerts will notify you.

### Steps

1.  Go to the VM.
2.  Under **Monitoring**, click **Alerts**.
3.  Click **Action groups** > **Create**.
4.  **Basic Details**:
    *   **Action group name**: `basic-ag`
    *   **Display name**: `basicAG`
    *   **Subscription and Resource group**: Select your VM’s resource group
5.  **Actions**:
    *   **Action type**: Email/SMS
    *   **Name**: `emailAlert`
    *   **Email**: Enter your email address
6.  Click **Review + Create** and then **Create**.

---

## Part 4: Create an Alert Rule (CPU Percentage)

### Steps

1.  Go back to the VM’s **Alerts** page.
2.  Click **Create Alert Rule**.
3.  **Scope**: Should already show your VM. If not, add your VM manually.
4.  **Condition**:
    *   Click **Add Condition**.
    *   Select metric: **Percentage CPU**.
    *   **Configure the condition**:
        *   **Operator**: Greater than
        *   **Threshold**: `50`
        *   **Aggregation**: Average
        *   **Check frequency**: 1 or 5 minutes
5.  **Actions**:
    *   Select your Action Group: `basic-ag`
6.  **Details**:
    *   **Alert rule name**: `vm-cpu-alert`
    *   **Severity**: `3` (Warning)
7.  Click **Review + Create** and then **Create**.

---

## Part 5: Trigger the Alert

Triggering the alert helps verify that it works. You may choose Linux or Windows:

### Linux VM

1.  **SSH** into your VM.
2.  Install stress tool:
    ```bash
    sudo apt-get update
    sudo apt-get install stress -y
    ```
3.  Run CPU load:
    ```bash
    stress --cpu 2 --timeout 60 
    ```
    *(This will run for 1 minute)*

### Windows VM

1.  **RDP** into your VM.
2.  Download a simple CPU stress tool (any lightweight one).
3.  Start CPU load for **1 minute**.

> [!NOTE]
> Wait **3–5 minutes** for Azure to detect the high CPU and send an alert email.

---

## Part 6: Verify Alert

### Expected Results

*   You will receive an email from Azure Monitor saying the CPU is above 50 percent.
*   After the stress test stops, the CPU will drop and a recovery email may arrive.

---

## Submission Requirements

Take screenshots of the following:

1.  **Your VM Overview page**
2.  **Action Group created**
3.  **Alert Rule settings**
4.  **Email received** for the CPU alert
5.  **Command or tool used** to generate CPU load

**Submit these screenshots in your individual WhatsApp group.**
