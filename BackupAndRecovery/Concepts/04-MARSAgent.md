# MARS Agent (Microsoft Azure Recovery Services Agent)

## Overview

The Microsoft Azure Recovery Services (MARS) Agent enables file-level backups from on-premise servers, AWS VMs, and other non-Azure environments to Azure Recovery Services Vault. It's the key component for hybrid cloud backup scenarios where full Azure VM backup capabilities are not available.

## What is the MARS Agent?

The MARS Agent is a lightweight software component that:
- Installs on Windows servers (on-premise, AWS, or other clouds)
- Backs up files and folders to Azure Recovery Services Vault
- Enables hybrid cloud backup strategies
- Provides secure, encrypted data transfer to Azure
- Supports scheduled and on-demand backups

**Key distinction:**
- **MARS Agent**: File-level backups only
- **Azure VM Backup**: Full VM backups (OS, apps, data, config)

## Use Cases

### 1. On-Premise to Azure Backup

**Scenario:**
Protect on-premise file servers, application data, or critical folders by backing them up to Azure.

**Benefits:**
- Cloud-based backup storage (no local backup infrastructure)
- Geographic redundancy
- Reduced on-premise storage costs
- Disaster recovery capability

### 2. AWS to Azure Backup

**Scenario:**
Simulate "on-premise" environment using AWS VMs and back up to Azure.

**Why this approach:**
- Full Azure VM backup requires Azure-native components
- AWS VMs cannot use Azure VM backup extensions
- MARS Agent provides file-level protection for AWS workloads

**Example from session:**
```
AWS Windows VM → Contains software folders (Tomcat, Jenkins, etc.)
                → MARS Agent installed
                → Backs up to Azure Recovery Services Vault
                → Can restore to Azure Windows VM
```

### 3. Specific Application Data Backup

**Scenario:**
Back up specific application folders, databases, or configuration files without backing up entire VMs.

**Examples:**
- Database backup folders
- Application logs
- Configuration files
- User data directories
- Software installation packages

## Limitations

> [!IMPORTANT]
> The MARS Agent **cannot perform full VM backups** on non-Azure VMs. It only supports file and folder-level backups.

**What MARS Agent CANNOT do:**
- ❌ Full VM backup (OS, applications, system state)
- ❌ Application-consistent backups for databases
- ❌ Bare-metal recovery
- ❌ System state backup
- ❌ Automated VM restoration

**What MARS Agent CAN do:**
- ✅ File and folder backups
- ✅ Selective data protection
- ✅ Scheduled backups
- ✅ Incremental backups
- ✅ Encrypted data transfer
- ✅ Cross-platform restore (backup from AWS, restore to Azure)

## Installation and Configuration

### Prerequisites

1. **Windows Server** (2008 R2 or later, 2022/2024 recommended)
2. **Recovery Services Vault** in Azure
3. **Vault credentials file** (downloaded from Azure portal)
4. **Internet connectivity** to Azure endpoints
5. **.NET Framework 4.5** or later
6. **Sufficient local storage** for cache (2-3% of backup data size)

### Installation Steps

#### 1. Download MARS Agent

```
Azure Portal → Recovery Services Vault → Getting Started → Backup
→ Where is your workload running? Select "On-premises"
→ What do you want to backup? Select "Files and folders"
→ Download Agent for Windows Server
```

#### 2. Download Vault Credentials

**Critical step:** The vault credentials file is required to register the agent.

```
Same location as agent download
→ Download vault credentials
→ File is valid for 10 days
→ Save securely (contains sensitive information)
```

> [!WARNING]
> Vault credentials expire after 10 days. If expired, download a new file from the portal.

#### 3. Install MARS Agent

**On the target server (on-premise or AWS VM):**

1. Run the downloaded installer (`MARSAgentInstaller.exe`)
2. Choose installation folder (default: `C:\Program Files\Microsoft Azure Recovery Services Agent`)
3. Specify cache location (requires sufficient space)
4. Configure proxy settings if needed
5. Complete installation

#### 4. Register Agent with Vault

**After installation:**

1. Launch **Microsoft Azure Backup** console
2. Click **Register Server** in the Actions pane
3. Browse to the downloaded **vault credentials file**
4. Set **encryption passphrase**:
   - Minimum 16 characters
   - Store securely (required for restore)
   - Cannot be recovered if lost

> [!CAUTION]
> **Save the encryption passphrase securely!** Without it, you cannot restore your backup data. Microsoft cannot recover lost passphrases.

5. Click **Register**
6. Wait for registration to complete

**Verification:**
```
Azure Portal → Recovery Services Vault → Backup Infrastructure
→ Protected Servers → Azure Backup Agent
→ Your server should appear in the list
```

### Configuration Example (Session Scenario)

**AWS Windows VM setup:**

1. **Prepare data folder:**
   ```
   C:\Software\
   ├── Tomcat\
   ├── Jenkins\
   └── Other applications\
   ```

2. **Install MARS Agent** on AWS VM

3. **Register with Azure vault** using vault credentials

4. **Configure backup** for `C:\Software\` folder

5. **Set schedule** (e.g., daily at 11:00 PM)

6. **Trigger initial backup**

## Configuring Backup Schedule

### Using the MARS Agent Console

1. Open **Microsoft Azure Backup** console
2. Click **Schedule Backup** in Actions pane
3. **Select items to backup:**
   - Click **Add Items**
   - Browse to folders (e.g., `C:\Software\`)
   - Select folders/files to protect
   - Click **OK**

4. **Specify backup schedule:**
   - **Frequency**: Daily or Weekly
   - **Time**: Select backup time (e.g., 11:00 PM)
   - **Multiple backups per day**: Optional

5. **Select retention policy:**
   - Daily: 7-180 days
   - Weekly: 4-104 weeks
   - Monthly: 1-60 months
   - Yearly: 1-10 years

6. **Choose initial backup type:**
   - Over network (recommended for initial setup)
   - Offline backup (for very large datasets)

7. **Confirm and finish**

### Backup Schedule Example

```
Items to backup: C:\Software\
Schedule: Daily at 11:00 PM
Retention:
  - Daily: 30 days
  - Weekly: 12 weeks
  - Monthly: 6 months
Initial backup: Over network
```

## Running Backups

### Scheduled Backup

Runs automatically based on the configured schedule. No manual intervention required.

**Monitoring:**
- Check backup status in MARS Agent console
- View jobs in Recovery Services Vault → Backup Jobs
- Configure alerts for failures

### On-Demand Backup

**When to use:**
- Immediate backup before scheduled time
- Before major changes
- Ad-hoc data protection needs

**How to trigger:**

1. Open **Microsoft Azure Backup** console
2. Click **Back Up Now** in Actions pane
3. Select retention (can differ from policy)
4. Click **Back Up**
5. Monitor progress in the console

## Backup Job Monitoring

### In MARS Agent Console

```
Microsoft Azure Backup → Jobs
```

**Information displayed:**
- Job status
- Start and end time
- Data transferred
- Errors or warnings

### In Azure Portal

```
Recovery Services Vault → Backup Jobs
→ Filter by: Azure Backup Agent
```

**Shows:**
- All backup jobs from registered servers
- Job status and duration
- Protected item name
- Error details

> [!TIP]
> Backup jobs appear in the Recovery Services Vault **as soon as they start**, providing real-time visibility into backup operations.

## Data Transfer and Costs

### Data Transfer Charges

**Backup (Upload to Azure):**
- Data transfer **from on-premise/AWS to Azure** incurs charges
- Charged based on amount of data transferred
- Incremental backups transfer only changed data (lower costs)

**Recovery (Download from Azure):**
- Data transfer **from Azure to on-premise/AWS** also incurs charges
- Charged based on amount of data restored
- Consider costs when planning large restores

### Cost Optimization

1. **Use incremental backups** (automatic after initial backup)
2. **Compress data** before backup (MARS Agent does this automatically)
3. **Selective backup** of only critical data
4. **Optimize retention policies** to balance protection and cost
5. **Schedule backups during off-peak hours** if bandwidth is metered

### Pricing Factors

| Factor | Impact on Cost |
|--------|----------------|
| **Backup size** | More data = higher storage cost |
| **Retention duration** | Longer retention = higher cost |
| **Data transfer** | Upload and download charges |
| **Protected instances** | Per-server licensing cost |
| **Storage redundancy** | GRS costs more than LRS |

## Restore Process

### Restoring to Original Server

1. Open **Microsoft Azure Backup** console
2. Click **Recover Data** in Actions pane
3. Select **This server** (where backup was taken)
4. Choose recovery point (date/time)
5. Select files/folders to restore
6. Specify recovery location
7. Click **Recover**

### Restoring to Different Server

**Scenario from session:**
- Backup taken from AWS Windows VM
- Restore to Azure Windows VM

**Requirements:**
- MARS Agent installed on target server
- Same encryption passphrase
- Vault credentials for registration

**Steps:**
1. Install MARS Agent on target server (Azure VM)
2. Register with same Recovery Services Vault
3. Click **Recover Data** → **Another server**
4. Provide vault credentials
5. Enter encryption passphrase
6. Select source server
7. Choose recovery point
8. Select files/folders
9. Specify restore location
10. Complete recovery

## Best Practices

1. **Use latest Windows Server versions** (2022 or 2024) for better performance and security
2. **Store encryption passphrase securely** in a password manager or secure vault
3. **Test restore procedures** regularly to ensure data can be recovered
4. **Monitor backup jobs** and configure failure alerts
5. **Maintain sufficient cache space** (2-3% of backup data size)
6. **Keep MARS Agent updated** to latest version
7. **Document backup configurations** for disaster recovery procedures
8. **Use appropriate retention policies** based on business requirements
9. **Schedule backups during low-activity periods** to minimize impact
10. **Verify initial backup completion** before relying on scheduled backups

## Troubleshooting

### Common Issues

#### Registration Failed
- **Cause**: Expired vault credentials
- **Solution**: Download new vault credentials file

#### Backup Job Failed
- **Cause**: Insufficient cache space
- **Solution**: Free up disk space or change cache location

#### Cannot Connect to Azure
- **Cause**: Firewall or proxy blocking
- **Solution**: Configure proxy settings or allow Azure endpoints

#### Slow Backup Performance
- **Cause**: Network bandwidth limitations
- **Solution**: Schedule during off-peak hours, optimize data selection

## Comparison: MARS Agent vs. Azure VM Backup

| Feature | MARS Agent | Azure VM Backup |
|---------|------------|-----------------|
| **Scope** | Files and folders only | Full VM (OS, apps, data) |
| **Platform** | On-premise, AWS, other clouds | Azure VMs only |
| **Installation** | Manual agent install | Automatic extension |
| **Backup type** | File-level | VM-level |
| **Recovery** | File/folder restore | Full VM or file-level restore |
| **Use case** | Hybrid scenarios | Azure-native VMs |
| **Cost** | Lower (selective data) | Higher (full VM) |

## Next Steps

- Understand [Backup Policies](./05-BackupPolicies.md) for retention and scheduling
- Learn [Data Recovery](./06-DataRecovery.md) procedures
- Review [Best Practices](./10-BestPractices.md) for comprehensive guidance
