# Recovery Services Vault

## Overview

The Recovery Services Vault is the central component of Azure's backup and disaster recovery infrastructure. It serves as a secure, managed storage repository for all backup data and provides the foundation for implementing comprehensive data protection strategies.

## What is a Recovery Services Vault?

A Recovery Services Vault is a storage entity in Azure that:
- Stores backup data for Azure VMs, on-premise servers, and hybrid scenarios
- Manages backup policies and retention schedules
- Provides centralized monitoring and management of backup jobs
- Enables cross-region restore capabilities
- Supports disaster recovery through VM replication

**Key characteristics:**
- Highly durable and secure storage
- Geo-redundant by default (optional)
- Supports immutability features to prevent accidental or malicious deletion
- Integrates with Azure Monitor for alerting and reporting

## Creating a Recovery Services Vault

### Prerequisites
- Azure subscription
- Resource group (or create new)
- Region selection (choose based on your VM locations)

### Creation Steps

1. **Navigate to Azure Portal** → Search for "Recovery Services vaults"
2. **Click "+ Create"**
3. **Configure basic settings:**
   - **Subscription**: Select your subscription
   - **Resource Group**: Choose existing or create new
   - **Vault Name**: Unique name for the vault
   - **Region**: Select the region (should match or be close to your VMs)

4. **Configure advanced features** (recommended):
   - ✅ Enable **Cross-region restore**
   - ✅ Enable **Immutability** (soft delete protection)
   - Configure **Storage Redundancy** (GRS recommended)

### Storage Redundancy Options

| Option | Description | Use Case |
|--------|-------------|----------|
| **LRS** (Locally Redundant) | 3 copies in single datacenter | Cost-sensitive, non-critical workloads |
| **GRS** (Geo-Redundant) | 6 copies across two regions | Production workloads, DR scenarios |
| **ZRS** (Zone-Redundant) | 3 copies across availability zones | High availability within region |

> [!IMPORTANT]
> For production environments, **always enable Geo-Redundant Storage (GRS)** to protect against regional outages.

## Key Features

### 1. Cross-Region Restore

**What it does:**
Allows you to restore backups in a secondary Azure region, even if the primary region is unavailable.

**Why it's critical:**
- Protects against regional disasters
- Enables business continuity during Azure regional outages
- Provides geographic redundancy for compliance requirements

**How to enable:**
- Must be enabled during vault creation or in vault settings
- Requires GRS storage redundancy
- Secondary region is automatically paired by Azure (e.g., East US → West US)

**Example scenario:**
```
Primary Region: East US (experiencing outage)
Secondary Region: West US (automatically paired)
Action: Restore VM in West US from backup stored in vault
```

### 2. Immutability and Soft Delete

**Soft Delete:**
- Deleted backup data is retained for 14 days before permanent deletion
- Protects against accidental deletion
- Can be recovered during the retention period

**Immutability:**
- Prevents deletion of backup data even by administrators
- Protects against ransomware and malicious deletion
- Can be configured with time-based retention locks

> [!WARNING]
> Vaults with immutability enabled and active backups are **extremely difficult to delete**. This is by design to protect your data.

### 3. Vault Protection

Recovery Services Vaults are highly protected resources:
- Cannot be easily deleted if they contain backup data
- Require multi-step deletion process
- Protected against accidental or unauthorized deletion

**Why this matters:**
- Ensures backup data safety
- Prevents costly data loss
- Maintains compliance with retention policies

## Managing the Vault

### Backup Policies

Vaults contain backup policies that define:
- **Schedule**: When backups occur (daily, weekly, etc.)
- **Retention**: How long to keep backups
- **Backup window**: Time range for backup operations

### Monitoring

The vault dashboard provides:
- Active backup jobs
- Failed backup alerts
- Storage consumption
- Protected items count
- Replication status (for DR scenarios)

### Access Control

Use Azure RBAC to control vault access:
- **Backup Operator**: Can trigger backups and restores
- **Backup Contributor**: Can manage backup policies
- **Backup Reader**: View-only access

## Vault Deletion Process

> [!CAUTION]
> Deleting a Recovery Services Vault is **not straightforward** and requires multiple steps. Unused vaults can lead to unexpected costs.

### Why Deletion is Complex

The vault is designed to be difficult to delete to protect backup data from:
- Accidental deletion
- Unauthorized access
- Ransomware attacks
- Administrative errors

### Deletion Steps

Simply clicking "Delete" in the portal **will not work** if the vault contains:
- Active backups
- Backup data
- Protected items
- Replication configurations

**Required procedure:**

1. **Stop all backups:**
   ```
   For each protected item:
   - Navigate to Backup Items
   - Select the item
   - Click "Stop Backup"
   - Choose "Delete Backup Data"
   ```

2. **Delete all backup data:**
   - Confirm deletion of all recovery points
   - Wait for deletion to complete (can take time)

3. **Remove replication configurations:**
   - Disable replication for all replicated VMs
   - Delete recovery plans

4. **Download and run PowerShell script:**
   ```powershell
   # Azure provides a script to remove vault dependencies
   # Download from vault settings → Properties
   # Run the script with appropriate permissions
   ```

5. **Delete the vault:**
   - After all dependencies are removed
   - Vault can finally be deleted from portal

### Cost Implications

> [!WARNING]
> Unused vaults with retained backup data continue to incur storage charges. Always clean up unused vaults properly.

**Cost factors:**
- Backup storage consumed
- Retention duration
- Cross-region replication (if enabled)
- Protected instances count

## Automatic Resource Creation

When configuring disaster recovery replication, the vault automatically creates:
- **Target Resource Group**: In the secondary region
- **Virtual Networks**: Matching source network topology
- **Storage Accounts**: For replication data
- **Recovery Plans**: For orchestrated failover

This automation simplifies DR setup but requires understanding of what resources are created.

## Best Practices

1. **Enable cross-region restore** for all production vaults
2. **Use GRS storage redundancy** for critical workloads
3. **Enable soft delete and immutability** for ransomware protection
4. **Implement proper RBAC** to control vault access
5. **Monitor vault health** with Azure Monitor alerts
6. **Document vault configurations** for disaster recovery procedures
7. **Regularly review and clean up** unused vaults to avoid unnecessary costs
8. **Test cross-region restore** periodically to verify DR capabilities
9. **Tag vaults appropriately** for cost tracking and management
10. **Plan retention policies** carefully to balance protection and cost

## Vault Naming Conventions

Recommended naming pattern:
```
rsv-<environment>-<region>-<purpose>-<number>

Examples:
- rsv-prod-eastus-vm-01
- rsv-dev-westus-files-01
- rsv-dr-centralus-replication-01
```

## Next Steps

- Configure [VM Backup](./03-VMBackup.md) using the vault
- Set up [MARS Agent](./04-MARSAgent.md) for hybrid scenarios
- Define [Backup Policies](./05-BackupPolicies.md) for your workloads
- Plan [Disaster Recovery](./07-DisasterRecovery.md) with cross-region replication
