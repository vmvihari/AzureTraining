# Lab: Azure Backup and File-Level Recovery

## Lab Overview

In this lab, you will learn how to configure Azure VM backup and file-level backup using the Microsoft Azure Recovery Services (MARS) Agent. You'll create a Recovery Services Vault, perform full VM backups, install and configure the MARS Agent for file-level backups, and practice data recovery operations.

> [!IMPORTANT]
> This lab is designed for **easy cleanup** to avoid ongoing charges. We will **NOT** enable soft delete or immutability features that make deletion difficult.

## Learning Objectives

By the end of this lab, you will be able to:
- Create and configure a Recovery Services Vault for lab use
- Enable and perform Azure VM backups
- Install and register the MARS Agent on Windows Server
- Configure file-level backup schedules
- Perform on-demand backups
- Monitor backup jobs in the Azure Portal
- Perform file-level recovery from backup
- Properly clean up all resources to avoid charges

## Prerequisites

- Active Azure subscription
- Basic understanding of Azure Portal navigation
- Ability to connect to Windows VMs via RDP

## Estimated Time to Complete

⏱️ **60-90 minutes** (including cleanup)

---

## Exercise 1: Environment Preparation

**Objective**: Set up the required infrastructure for backup and recovery operations.

**Duration**: ⏱️ 15 minutes

### Instructions

#### Step 1: Create a Windows Server VM

1. Navigate to [Azure Portal](https://portal.azure.com)
2. Click **"Create a resource"** → Search for **"Virtual Machine"**
3. Click **"Create"**
4. Fill in the required details:
   - **Subscription**: Select your subscription
   - **Resource Group**: Create new (e.g., `rg-backup-lab`)
   - **VM Name**: `win-vm` (or any name you prefer)
   - **Region**: Select your preferred region
   - **Image**: **Windows Server 2022 Datacenter** or **Windows Server 2024**
   - **Size**: **Standard_D2s_v3** (2 vCPUs, 8 GB RAM) - recommended minimum
   - **Username**: Create an admin username
   - **Password**: Create a strong password (save it securely!)
5. **Networking**:
   - Allow RDP (3389) from your IP address
6. Click **"Review + Create"** → **"Create"**
7. Wait for deployment (3-5 minutes)

> [!TIP]
> Use Windows Server 2022 or 2024 for best performance and compatibility with backup features.

#### Step 2: Create a Recovery Services Vault

1. Search for **"Recovery Services vaults"** in Azure Portal
2. Click **"+ Create"**
3. Fill in the required details:
   - **Subscription**: Same as your VM
   - **Resource Group**: **Same as your VM** (`rg-backup-lab`)
   - **Vault Name**: `lucky-vault` (or any unique name)
   - **Region**: **Same region as your VM** (critical!)

4. **Important Configuration for Lab**:
   - Click **"Review + Create"**
   - After creation, go to the vault.
   - In the left menu, under **Settings**, click **Properties**.
   - In the main panel on the right, find **Backup Configuration** and click **Update**.
   - **Storage Redundancy**: Select **LRS (Locally Redundant Storage)** - cheaper for lab
   - **DO NOT enable**:
     - ❌ Soft Delete
     - ❌ Immutability
     - ❌ Cross-region restore (not needed for lab)

5. Click **"Save"**

> [!WARNING]
> **For Lab Use Only**: We're skipping soft delete and immutability to make cleanup easier. In production, you should enable these features for data protection.

### Validation

✅ **Success Criteria**:
- Windows Server VM is running
- You can connect via RDP
- Recovery Services Vault is created in the same region and resource group as VM
- Vault is configured with LRS storage
- Soft delete and immutability are disabled

---

## Exercise 2: Configure Azure VM Backup

**Objective**: Enable full VM backup with automated scheduling.

**Duration**: ⏱️ 15 minutes

### Background

Azure VM Backup captures:
- Complete OS disk
- All data disks
- Applications and configurations
- System state

This enables full VM restoration or file-level recovery.

### Instructions

#### Step 1: Navigate to VM Backup Settings

1. Go to **Virtual Machines** in Azure Portal
2. Select your VM (`win-vm`)
3. In the left menu, click **"Backup"** (under Operations)

#### Step 2: Enable Backup

1. **Recovery Services Vault**: Select `lucky-vault`
2. **Backup Policy**:
   - Leave the default **"EnhancedPolicy"** selected if "Standard" is disabled.
   - *Note: Newer "Trusted Launch" VMs often require Enhanced Policy. This is fine for the lab.*
   - If available, you can choose **"StandardPolicy"** to save slightly on costs, but **Enhanced** is acceptable.
3. Click **"Enable backup"**
4. Wait for backup configuration to complete (1-2 minutes)

#### Step 3: Trigger On-Demand Backup

> [!IMPORTANT]
> Always trigger an on-demand backup immediately after enabling backup. Don't wait for the scheduled time!

1. After backup is enabled, click **"Backup now"**
2. **Retain Backup Till**: Select a date 7-30 days from now
3. Click **"OK"**

#### Step 4: Monitor Backup Job

1. Go to **Recovery Services Vault** → `lucky-vault`
2. Click **"Backup jobs"** (under Monitoring)
3. You should see a job with:
   - **Backup Item**: win-vm
   - **Operation**: Backup
   - **Status**: In Progress → Completed

**Backup process includes two phases:**
1. **Taking Snapshot** (5-15 minutes)
2. **Transfer data to vault** (15-45 minutes depending on VM size)

Both must complete for a successful backup.

### Validation

✅ **Success Criteria**:
- Backup is enabled on the VM
- On-demand backup job is triggered
- Backup job shows "Completed" status in Backup Jobs
- Recovery point is created (visible in Backup Items → Azure Virtual Machine)

**Expected Timeline**: 20-60 minutes for first backup to complete

---

## Exercise 3: Prepare for File-Level Backup

**Objective**: Create test data and prepare the Windows VM for MARS Agent installation.

**Duration**: ⏱️ 10 minutes

### Instructions

#### Step 1: Connect to Windows VM

1. Go to your VM in Azure Portal
2. Click **"Connect"** → **"Download RDP File"**
3. Open the RDP file and connect using your credentials

> [!TIP]
> If RDP connection fails, verify:
> - VM is running
> - Port 3389 is allowed in NSG
> - Your IP address is allowed
> - VM has at least 8 GB RAM

#### Step 2: Install Chrome Browser (Optional but Recommended)

1. Inside the VM, open **Microsoft Edge**
2. Navigate to `https://www.google.com/chrome`
3. Download and install Chrome
4. This makes downloading MARS Agent easier

#### Step 3: Create Test Folder and Files

1. Open **File Explorer**
2. Navigate to `C:\`
3. Create a new folder: `C:\BackupDemo`
4. Inside `C:\BackupDemo`, create:
   - A text file: `notes.txt` (add some content)
   - A subfolder: `C:\BackupDemo\config`
   - A file inside config: `settings.txt`
   - Optional: Add a ZIP file or any other test files

**Example structure:**
```
C:\BackupDemo\
├── notes.txt
├── data.zip
└── config\
    └── settings.txt
```

### Validation

✅ **Success Criteria**:
- Successfully connected to Windows VM via RDP
- Chrome browser installed (optional)
- `C:\BackupDemo` folder created with test files
- At least 2-3 files in the folder for testing

---

## Exercise 4: Install and Register MARS Agent

**Objective**: Set up the Microsoft Azure Recovery Services Agent for file-level backups.

**Duration**: ⏱️ 15 minutes

### Background

The MARS Agent enables:
- File and folder-level backups
- Backup from on-premise or non-Azure VMs to Azure
- Selective data protection
- Encrypted data transfer

### Instructions

#### Step 1: Download MARS Agent and Vault Credentials

**From Azure Portal (on your local machine):**

1. Go to **Recovery Services Vault** → `lucky-vault`
2. Click **"Backup"** (under Getting Started)
3. **Where is your workload running?**: Select **"On-premises"**
4. **What do you want to back up?**: Select **"Files and folders"**
5. Click **"Prepare Infrastructure"**

6. **Download two items:**
   - **Download Agent for Windows Server**
     - Copy the download link
   - **Download vault credentials**
     - Click "Download"
     - Save the `.VaultCredentials` file

**Transfer to Windows VM:**

1. You can copy the MARS Agent download link
2. Inside the Windows VM, open Chrome
3. Paste the link and download the MARS Agent installer
4. Also transfer the vault credentials file to the VM (drag and drop into RDP session, or download again from inside VM)

> [!WARNING]
> Vault credentials are valid for **10 days only**. If expired, download a fresh file.

#### Step 2: Install MARS Agent

**Inside the Windows VM:**

1. Run `MARSAgentInstaller.exe`
2. **Installation Folder**: Accept default (`C:\Program Files\Microsoft Azure Recovery Services Agent`)
3. **Cache Location**: Accept default (or choose a location with sufficient space)
   - Cache needs 2-3% of backup data size
4. **Proxy Configuration**: Skip (unless you use a proxy)
5. Click **"Install"**
6. Wait for installation to complete (1-2 minutes)
7. **Check "Proceed to Registration"** → Click **"Finish"**
   - *Note: If you missed this or the wizard didn't open: Open **Microsoft Azure Backup** from the Start menu. In the **Actions** pane (right side), click **Register Server**.*

#### Step 3: Register Server to Vault

The **Register Server Wizard** opens automatically:

1. **Vault Identification**:
   - Click **"Browse"**
   - Select the vault credentials file you downloaded
   - Click **"Next"**

2. **Encryption Setting**:
   - Click **"Generate Passphrase"**
   - **Passphrase Location**: Choose a location to save (e.g., `C:\BackupDemo\passphrase.txt`)
   - **CRITICAL**: Save this passphrase securely!
   - **Uncheck** "Save passphrase securely to Azure Key Vault" (unless you configured Key Vault)
   - Click **"Finish"**

3. Wait for registration to complete (30-60 seconds)

> [!CAUTION]
> **Save the encryption passphrase!** Without it, you cannot restore your backup data. Microsoft cannot recover lost passphrases.

#### Step 4: Verify Registration

1. Open **Start Menu** → Search for **"Microsoft Azure Backup"**
2. The application should open without errors
3. In Azure Portal:
   - Go to **Recovery Services Vault** → `lucky-vault`
   - Click **"Backup Infrastructure"** → **"Protected Servers"** → **"Azure Backup Agent"**
   - You should see your VM listed

### Validation

✅ **Success Criteria**:
- MARS Agent installed successfully
- Server registered to `lucky-vault`
- Encryption passphrase saved securely
- VM appears in vault's Protected Servers list

---

## Exercise 5: Configure File-Level Backup Schedule

**Objective**: Set up automated file-level backups for the test folder.

**Duration**: ⏱️ 10 minutes

### Instructions

#### Step 1: Open Schedule Backup Wizard

**Inside the Windows VM:**

1. Open **Microsoft Azure Backup** application
2. In the **Actions** pane (right side), click **"Schedule Backup"**
3. The Schedule Backup Wizard opens

#### Step 2: Select Items to Back Up

1. Click **"Add Items"**
2. Browse to `C:\BackupDemo`
3. **Check the box** next to `BackupDemo` folder
4. Click **"OK"**
5. Verify `C:\BackupDemo\` appears in the selected items list
6. Click **"Next"**

#### Step 3: Specify Backup Schedule

1. **Backup Frequency**: Select **"Day"** (daily backup)
2. **Select Times**: Choose any time (e.g., 11:00 PM)
   - For lab, any time works
   - In production, choose off-peak hours
3. Click **"Next"**

#### Step 4: Select Retention Policy

1. **Daily Backup**: Retain for **7 days** (minimum for lab)
   - For production, use longer retention based on requirements
2. Click **"Next"**

#### Step 5: Choose Initial Backup Type

1. Select **"Automatically over the network"**
2. Click **"Next"**

#### Step 6: Confirmation

1. Review the summary
2. Click **"Finish"**
3. The schedule is now configured

### Validation

✅ **Success Criteria**:
- Backup schedule created successfully
- `C:\BackupDemo` folder is selected for backup
- Daily schedule configured
- 7-day retention policy set

---

## Exercise 6: Perform On-Demand File-Level Backup

**Objective**: Trigger an immediate backup without waiting for the schedule.

**Duration**: ⏱️ 10 minutes

### Instructions

#### Step 1: Trigger Backup

**Inside the Windows VM:**

1. Open **Microsoft Azure Backup** application
2. In the **Actions** pane, click **"Back Up Now"**
3. **Retain Backup Till**: Select a date 7-30 days from now
4. Click **"Back Up"**

#### Step 2: Monitor Backup Progress

The backup process includes:
1. **Scanning data** (analyzing files)
2. **Compressing and encrypting** data
3. **Uploading to vault**

**Progress window shows:**
- Files processed
- Data transferred
- Estimated time remaining

**Expected duration**: 2-10 minutes (depending on data size)

#### Step 3: Verify Completion

**In the MARS Agent application:**
- You should see: **"Backup successfully completed"**
- Note the data transferred size

### Validation

✅ **Success Criteria**:
- Backup completes without errors
- Success message displayed
- Data transferred to vault

---

## Exercise 7: Verify Backup in Azure Portal

**Objective**: Confirm that file-level backup appears in the Recovery Services Vault.

**Duration**: ⏱️ 5 minutes

### Instructions

#### Step 1: Navigate to Backup Items

1. Go to **Recovery Services Vault** → `lucky-vault`
2. Click **"Backup items"** (under Protected Items)
3. Click **"Azure Backup Agent"**

#### Step 2: Verify Backup

You should see:
- **Computer Name**: win-vm (or your VM name)
- **Item Type**: File-Folders
- **Last Backup Status**: Completed
- **Last Backup Time**: Recent timestamp
- **Recovery Points**: 1 (or more if you ran multiple backups)

#### Step 3: View Backup Jobs

1. Go to **"Backup jobs"** (under Monitoring)
2. Filter by **"Azure Backup Agent"** if needed
3. You should see:
   - **Backup Item**: win-vm
   - **Operation**: Backup
   - **Status**: Completed
   - **Job Type**: File-Folders

### Validation

✅ **Success Criteria**:
- File-level backup appears in Backup Items
- Recovery point count is at least 1
- Backup job shows "Completed" status
- Last backup time matches your on-demand backup

---

## Exercise 8: Perform File-Level Recovery (Optional)

**Objective**: Practice restoring files from a backup recovery point.

**Duration**: ⏱️ 10 minutes

### Instructions

#### Step 1: Simulate Data Loss

**Inside the Windows VM:**

1. Navigate to `C:\BackupDemo`
2. Delete one of the files (e.g., `notes.txt`)
3. Or delete the entire `BackupDemo` folder to simulate complete data loss

#### Step 2: Initiate Recovery

1. Open **Microsoft Azure Backup** application
2. In the **Actions** pane, click **"Recover Data"**
3. **Recovery Wizard** opens

#### Step 3: Select Recovery Location

1. **Where is the data you want to recover?**: Select **"This server (win-vm)"**
2. Click **"Next"**

#### Step 4: Select Recovery Mode

1. **Select Recovery Mode**: Choose **"Individual files and folders"**
2. Click **"Next"**

#### Step 5: Select Volume and Date

1. **Select Volume**: Choose **C:\\**
2. **Select Date**: Choose the date of your backup
3. **Select Time**: Choose the time of your backup
4. Click **"Mount"**

**What happens:**
- Azure mounts the backup as a temporary drive (e.g., **F:** or **G:**)
- You can browse the backup contents like a normal drive

#### Step 6: Browse and Restore Files

1. Open **File Explorer**
2. Navigate to the mounted drive (e.g., **F:\**)
3. Browse to `F:\C\BackupDemo\`
4. Copy the files you want to restore
5. Paste them back to `C:\BackupDemo\` (or any location)

#### Step 7: Unmount the Backup

1. Return to the **Recovery Wizard**
2. Click **"Unmount"**
3. Confirm unmount

> [!TIP]
> The backup drive automatically unmounts after 12 hours if you forget to unmount it manually.

### Validation

✅ **Success Criteria**:
- Backup successfully mounted as a drive
- Files visible and accessible
- Files restored to original or new location
- Backup drive unmounted successfully

---

## Exercise 9: Lab Cleanup (CRITICAL)

**Objective**: Delete all resources to avoid ongoing charges.

**Duration**: ⏱️ 15 minutes

> [!WARNING]
> **Complete this exercise immediately after finishing the lab** to avoid charges for storage, VM runtime, and backup retention.

### Cleanup Order

Follow this exact order to avoid deletion errors:

#### Step 1: Stop VM Backup and Delete Backup Data

1. Go to **Virtual Machines** → `win-vm`
2. Click **"Backup"**
3. Click **"Stop Backup"**
4. Select **"Delete Backup Data"**
5. **Type the VM name** to confirm
6. Click **"Stop Backup"**
7. Wait for deletion to complete (2-5 minutes)

#### Step 2: Stop File-Level Backup and Delete Backup Data

1. Go to **Recovery Services Vault** → `lucky-vault`
2. Click **"Backup items"** → **"Azure Backup Agent"**
3. Click on your server (win-vm)
4. Click **"Delete"**
5. **Type the server name** to confirm
6. Click **"Delete"**
7. Wait for deletion to complete

#### Step 3: Delete Recovery Services Vault

1. Go to **Recovery Services Vault** → `lucky-vault`
2. Verify no backup items remain:
   - Backup Items → Azure Virtual Machine: 0 items
   - Backup Items → Azure Backup Agent: 0 items
3. Click **"Delete"**
4. **Type the vault name** to confirm
5. Click **"Delete"**

> [!NOTE]
> Because we disabled soft delete and immutability, the vault should delete easily. If it doesn't, wait 5-10 minutes and try again.

#### Step 4: Delete Virtual Machine

1. Go to **Virtual Machines** → `win-vm`
2. Click **"Delete"**
3. **Check all boxes**:
   - ☑ Delete with VM: Disks
   - ☑ Delete with VM: Network interfaces
   - ☑ Delete with VM: Public IP addresses
4. **Type "delete"** to confirm
5. Click **"Delete"**

#### Step 5: Delete Resource Group

1. Go to **Resource Groups** → `rg-backup-lab`
2. Click **"Delete resource group"**
3. **Type the resource group name** to confirm
4. Click **"Delete"**
5. Wait for deletion to complete (5-10 minutes)

### Validation

✅ **Success Criteria**:
- All backup data deleted
- Recovery Services Vault deleted
- Virtual Machine deleted
- All associated resources (disks, NICs, IPs) deleted
- Resource group deleted
- No resources remain in your subscription related to this lab

**Verify in Azure Portal:**
- Search for `lucky-vault` → Should not exist
- Search for `win-vm` → Should not exist
- Check Resource Groups → `rg-backup-lab` should not exist

---

## Lab Summary

### What You Accomplished

✅ Created a Windows Server VM
✅ Created and configured a Recovery Services Vault
✅ Enabled and performed Azure VM backup
✅ Installed and registered MARS Agent
✅ Configured file-level backup schedule
✅ Performed on-demand file-level backup
✅ Monitored backup jobs in Azure Portal
✅ Performed file-level recovery (optional)
✅ Cleaned up all resources to avoid charges

### Key Takeaways

1. **VM Backup vs. File-Level Backup**:
   - VM Backup: Full system (OS, apps, data, configs)
   - MARS Agent: File and folder level only

2. **Always Trigger On-Demand Backup**:
   - Don't wait for scheduled time
   - Ensures immediate protection

3. **Backup Jobs Appear Immediately**:
   - Visible in vault as soon as they start
   - Monitor progress in real-time

4. **Encryption Passphrase is Critical**:
   - Required for MARS Agent recovery
   - Cannot be recovered if lost
   - Save securely

5. **Cleanup is Important**:
   - Backups incur storage costs
   - Unused vaults continue charging
   - Always delete resources after lab

### Time Breakdown

| Exercise | Duration |
|----------|----------|
| Environment Preparation | 15 min |
| VM Backup Configuration | 15 min |
| File-Level Backup Prep | 10 min |
| MARS Agent Installation | 15 min |
| Backup Schedule Configuration | 10 min |
| On-Demand Backup | 10 min |
| Verify in Portal | 5 min |
| File Recovery (Optional) | 10 min |
| **Lab Cleanup** | **15 min** |
| **Total** | **90-105 min** |

---

## Troubleshooting Guide

### Common Issues and Solutions

**Problem**: Cannot connect to VM via RDP
- **Solution**: 
  - Verify VM is running
  - Check NSG allows port 3389
  - Verify VM has at least 8 GB RAM
  - Try resetting RDP from Azure Portal

**Problem**: Backup job fails with "VM agent not responding"
- **Solution**:
  - Restart the VM
  - Wait 5 minutes and try again
  - Verify VM agent is running (VM → Extensions + applications)

**Problem**: MARS Agent registration fails
- **Solution**:
  - Verify vault credentials file is not expired (< 10 days old)
  - Download fresh vault credentials
  - Ensure VM has internet connectivity

**Problem**: Cannot delete Recovery Services Vault
- **Solution**:
  - Verify all backup items are deleted
  - Wait 10-15 minutes after deleting backup data
  - Check for any replication items or policies
  - If still fails, contact Azure support
 
 **Problem**: `ResourceGroupDeletionBlocked` on `AzureBackupRG_...`
 - **Cause**: This resource group contains **Restore Point Collections** (instant recovery points) that are locked by the Vault.
 - **Solution**:
   1. Go to your Vault (`lucky-vault`) → **Backup Items**.
   2. Ensure all items are deleted.
   3. Check **Soft Delete**:
      - Go to **Properties** → **Security Settings** → **Update**.
      - If Soft Delete is **Enabled**, your deleted items are in a "Soft Deleted" state (retained for 14 days).
      - **To force delete**: Disable Soft Delete, then go to **Backup Items** → **Soft Deleted Items** → **Undelete** the item → **Delete** it again.
   4. Once the Vault is truly empty, the `AzureBackupRG` will either disappear automatically or can be manually deleted.

 **Problem**: "There are protected items in this vault" / Cannot Unregister Server
 - **Cause**: Data still exists in a "Soft Deleted" state, preventing unregistration.
 - **Solution (The specific sequence matters)**:
   1. In the **Left Menu**, under **Settings**, click on **Properties**.
   2. In the **Right Panel**, scroll down to the **Security Settings** heading.
   3. Look specifically for the subsection **Soft Delete Settings**.
   4. Click the blue **Update** link appearing directly under "Soft Delete Settings".
   5. A new pane opens. **Uncheck** "Soft Delete" and **Save**.
      - **Critical Troubleshooting**: If the checkbox is **MISSING** in the UI:
        1. Open **Cloud Shell** (icon `>_` at top right of Portal). Select **PowerShell**.
        2. Run these commands to force-disable it (updates module first to ensure command exists):
           ```powershell
           Update-Module -Name Az.RecoveryServices -Force
           $vault = Get-AzRecoveryServicesVault -ResourceGroupName "rg-backup-lab" -Name "lucky-vault"
           Set-AzRecoveryServicesVaultProperty -Vault $vault -SoftDeleteFeatureState Disable
           ```
           ```
        3. **Alternative (Bash/Azure CLI)**:
           If PowerShell fails or you see "Update-Module not found", switch Cloud Shell to **Bash** (top left dropdown) and run:
           ```bash
           az backup vault backup-properties set --name "lucky-vault" --resource-group "rg-backup-lab" --soft-delete-feature-state Disable
           ```
           az backup vault backup-properties set --name "lucky-vault" --resource-group "rg-backup-lab" --soft-delete-feature-state Disable
           ```
      - **Error `BMSUserErrorDisablingSoftDeleteStateNotAllowed`**:
        - This means **"Always-on Soft Delete"** is enabled for your subscription or vault.
        - **This is irreversible.** You cannot disable Soft Delete.
        - **Impact**: You CANNOT delete the Backup Vault or Resource Group immediately.
        - **Workaround**: 
          1. Delete everything else (VM, Disks, NICs) individually.
          2. Leave the Vault and Resource Group.
          3. Wait **14 days** (after the backup item was deleted).
          4. After 14 days, the soft-deleted item permanently expires, and you can delete the empty Vault.
          5. *Note: You are NOT charged for soft-deleted data retention.*
        - **Q: Can I manually delete the `Restore Point Collection`?**
          - **No.** The Vault places a lock on this resource. Any attempt to manually delete it (or the Resource Group it lives in) will fail with the `ResourceGroupDeletionBlocked` error until the Soft Delete period expires.
   6. Go to **Backup Items** → **Azure Backup Agent**.
   3. Even if empty, check if there is a filter or separate tab for **"Soft Deleted Items"**.
   4. If you see an item there:
      - Click it → **Undelete** (Restores it to active state).
      - Once active, click **Stop Backup** → **Delete Backup Data** again.
      - *Because Soft Delete is now OFF, this will permanently delete it.*
   5. NOW go to **Backup Infrastructure** → **Protected Servers** → **Unregister/Delete**.

**Problem**: File-level backup shows "Failed"
- **Solution**:
  - Check cache location has sufficient space (2-3% of data size)
  - Verify files are not locked by applications
  - Check VM has internet connectivity
  - Review error details in MARS Agent console

---

## Additional Resources

- [Azure Backup Documentation](https://docs.microsoft.com/azure/backup/)
- [MARS Agent Documentation](https://docs.microsoft.com/azure/backup/backup-azure-file-folder-backup-faq)
- [Recovery Services Vault Overview](https://docs.microsoft.com/azure/backup/backup-azure-recovery-services-vault-overview)
- [Backup Best Practices](https://docs.microsoft.com/azure/backup/backup-azure-best-practices)

---

**🎉 Congratulations on completing the Azure Backup and File-Level Recovery Lab!**

> [!IMPORTANT]
> **Don't forget to complete Exercise 9 (Lab Cleanup)** to avoid ongoing charges!
