# Assignment 1: Azure File Shares

## Overview

Azure File Shares provide fully managed file shares in the cloud that are accessible via the industry-standard Server Message Block (SMB) protocol, Network File System (NFS) protocol, and Azure Files REST API. Azure file shares can be mounted concurrently by cloud or on-premises deployments.

---

## What are Azure File Shares?

**Definition**: Azure File Shares are cloud-based file shares that can be accessed from anywhere using standard protocols (SMB, NFS, or REST API).

**Key Characteristics**:
- Fully managed (no server maintenance required)
- Accessible from Windows, Linux, and macOS
- Can be mounted like a network drive
- Supports concurrent access from multiple clients
- Integrated with Azure Active Directory for authentication
- Snapshots for backup and recovery
- Soft delete protection

---

## When to Use Azure File Shares

### ✅ Use Azure File Shares When:

1. **Lift and Shift Applications**
   - Migrating on-premises applications that use file shares
   - No code changes required
   - Example: Legacy applications expecting a file share

2. **Shared Application Data**
   - Multiple VMs need access to the same files
   - Configuration files shared across servers
   - Log files centralized in one location

3. **Development and Testing**
   - Shared development environments
   - Test data accessible by multiple team members
   - CI/CD pipelines reading/writing files

4. **Cloud-Native Applications**
   - Containerized applications (Kubernetes, Docker)
   - Azure App Service content storage
   - Azure Functions shared data

5. **Hybrid Scenarios**
   - Azure File Sync for on-premises to cloud synchronization
   - Disaster recovery and backup
   - Cloud bursting for peak loads

---

## Azure File Shares vs Blob Storage

| Feature | Azure File Shares | Blob Storage |
|---------|------------------|--------------|
| **Protocol** | SMB, NFS, REST | REST only |
| **Access** | Mount as drive | URL-based access |
| **Hierarchy** | Directory structure | Flat namespace (virtual folders) |
| **Use Case** | Shared file systems | Object storage, media files |
| **Concurrent Access** | Yes (file locking) | Yes (no locking) |
| **Performance** | Standard, Premium | Standard, Premium |
| **Best For** | Traditional apps | Modern apps, big data |

---

## Creating Azure File Shares

### Method 1: Azure Portal

**Steps**:
1. Navigate to your **Storage Account**
2. In the left menu, select **File shares** (under Data storage)
3. Click **+ File share**
4. Configure:
   - **Name**: `myfileshare` (lowercase, 3-63 characters)
   - **Tier**: 
     - **Transaction optimized** (default, general purpose)
     - **Hot** (frequently accessed files)
     - **Cool** (infrequently accessed files)
   - **Quota**: Maximum size (e.g., 100 GB)
   - **Backup**: Enable/disable Azure Backup
5. Click **Create**

---

### Method 2: Azure CLI

```bash
# Create file share
az storage share create \
  --name myfileshare \
  --account-name mystorageacct \
  --quota 100

# List file shares
az storage share list \
  --account-name mystorageacct \
  --output table

# Show file share properties
az storage share show \
  --name myfileshare \
  --account-name mystorageacct
```

---

### Method 3: PowerShell

```powershell
# Get storage account context
$storageAccount = Get-AzStorageAccount `
    -ResourceGroupName "myResourceGroup" `
    -Name "mystorageacct"
$ctx = $storageAccount.Context

# Create file share
New-AzStorageShare `
    -Name "myfileshare" `
    -Context $ctx `
    -QuotaGiB 100

# List file shares
Get-AzStorageShare -Context $ctx
```

---

## Mounting Azure File Shares

### Windows VM

#### Option 1: PowerShell Script (Recommended)

**Get Mount Script from Azure Portal**:
1. Navigate to Storage Account → **File shares**
2. Select your file share
3. Click **Connect** button
4. Select **Windows** tab
5. Copy the PowerShell script

**Example Script**:
```powershell
# Variables
$storageAccountName = "mystorageacct"
$fileShareName = "myfileshare"
$storageAccountKey = "your-storage-key"

# Create credential
$securePassword = ConvertTo-SecureString -String $storageAccountKey -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential `
    -ArgumentList "AZURE\$storageAccountName", $securePassword

# Mount as Z: drive
New-PSDrive -Name Z -PSProvider FileSystem `
    -Root "\\$storageAccountName.file.core.windows.net\$fileShareName" `
    -Credential $credential -Persist

# Verify mount
Get-PSDrive Z
```

**Test Access**:
```powershell
# Create a test file
"Hello from Azure File Share" | Out-File Z:\test.txt

# List files
Get-ChildItem Z:\

# Read file
Get-Content Z:\test.txt
```

---

#### Option 2: Persistent Mount via Task Scheduler

**Create Mount Script** (`C:\Scripts\mount-fileshare.ps1`):
```powershell
$storageAccountName = "mystorageacct"
$fileShareName = "myfileshare"
$storageAccountKey = "your-storage-key"

$securePassword = ConvertTo-SecureString -String $storageAccountKey -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential `
    -ArgumentList "AZURE\$storageAccountName", $securePassword

# Remove if already mounted
if (Test-Path Z:) {
    Remove-PSDrive -Name Z -Force
}

# Mount
New-PSDrive -Name Z -PSProvider FileSystem `
    -Root "\\$storageAccountName.file.core.windows.net\$fileShareName" `
    -Credential $credential -Persist
```

**Create Scheduled Task**:
```powershell
# Create scheduled task to run at startup
$action = New-ScheduledTaskAction -Execute 'PowerShell.exe' `
    -Argument '-ExecutionPolicy Bypass -File C:\Scripts\mount-fileshare.ps1'

$trigger = New-ScheduledTaskTrigger -AtStartup

$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount

Register-ScheduledTask -TaskName "MountAzureFileShare" `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Description "Mount Azure File Share at startup"
```

---

### Linux VM

#### Option 1: Temporary Mount

**Install CIFS utilities**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install cifs-utils

# RHEL/CentOS
sudo yum install cifs-utils
```

**Mount the file share**:
```bash
# Variables
STORAGE_ACCOUNT="mystorageacct"
FILE_SHARE="myfileshare"
STORAGE_KEY="your-storage-key"
MOUNT_POINT="/mnt/myfileshare"

# Create mount point
sudo mkdir -p $MOUNT_POINT

# Mount
sudo mount -t cifs \
    //$STORAGE_ACCOUNT.file.core.windows.net/$FILE_SHARE \
    $MOUNT_POINT \
    -o vers=3.0,username=$STORAGE_ACCOUNT,password=$STORAGE_KEY,serverino
```

**Test Access**:
```bash
# Create test file
echo "Hello from Azure File Share" | sudo tee $MOUNT_POINT/test.txt

# List files
ls -la $MOUNT_POINT

# Read file
cat $MOUNT_POINT/test.txt
```

---

#### Option 2: Persistent Mount via /etc/fstab

**Create credentials file**:
```bash
# Create credentials directory
sudo mkdir -p /etc/smbcredentials

# Create credentials file
sudo bash -c 'cat > /etc/smbcredentials/mystorageacct.cred << EOF
username=mystorageacct
password=your-storage-key
EOF'

# Secure the credentials file
sudo chmod 600 /etc/smbcredentials/mystorageacct.cred
```

**Add to /etc/fstab**:
```bash
# Create mount point
sudo mkdir -p /mnt/myfileshare

# Add entry to /etc/fstab
sudo bash -c 'cat >> /etc/fstab << EOF
//mystorageacct.file.core.windows.net/myfileshare /mnt/myfileshare cifs nofail,credentials=/etc/smbcredentials/mystorageacct.cred,dir_mode=0777,file_mode=0777,serverino
EOF'

# Mount all entries in fstab
sudo mount -a

# Verify mount
df -h | grep myfileshare
```

**Test Persistence**:
```bash
# Reboot the VM
sudo reboot

# After reboot, verify mount is still there
df -h | grep myfileshare
ls -la /mnt/myfileshare
```

---

## Performance Tiers

### Standard (Transaction Optimized, Hot, Cool)

**Storage Account Type**: General-purpose v2 (GPv2)

**Performance**:
- IOPS: Up to 1,000 per share (10,000 with large file shares)
- Throughput: Up to 60 MiB/s per share
- Latency: Higher than Premium

**Pricing**:
- Pay for storage used + transactions
- **Transaction Optimized**: Balanced for workloads with many transactions
- **Hot**: Optimized for frequently accessed files
- **Cool**: Optimized for infrequently accessed files (lower storage cost, higher transaction cost)

**Use Cases**:
- General-purpose file shares
- Development and testing
- Backup and archive (Cool tier)

---

### Premium (FileStorage)

**Storage Account Type**: FileStorage (Premium)

**Performance**:
- IOPS: Up to 100,000 per share
- Throughput: Up to 10 GiB/s per share
- Latency: Single-digit milliseconds
- SSD-backed storage

**Pricing**:
- Pay for provisioned capacity (not actual usage)
- No transaction charges
- Higher cost per GB

**Use Cases**:
- High-performance applications
- Databases (SQL Server, Oracle)
- IO-intensive workloads
- Production environments requiring low latency

---

## Security and Access Control

### Authentication Methods

#### 1. Storage Account Key
- Full access to all file shares
- Should be rotated regularly
- Store in Azure Key Vault

#### 2. Shared Access Signature (SAS)
- Time-limited, permission-scoped access
- Can be revoked by rotating keys
- Good for temporary access

#### 3. Azure Active Directory (Azure AD)
- Identity-based authentication
- Most secure option
- Supports RBAC (Role-Based Access Control)
- Only works with SMB protocol

**Enable Azure AD Authentication**:
```bash
# Enable Azure AD DS authentication
az storage account update \
    --name mystorageacct \
    --resource-group myResourceGroup \
    --enable-files-aadds true
```

---

### Network Security

#### Private Endpoints
- File share accessible only from specific VNet
- No public internet access
- Enhanced security for sensitive data

**Create Private Endpoint**:
```bash
az network private-endpoint create \
    --name myPrivateEndpoint \
    --resource-group myResourceGroup \
    --vnet-name myVNet \
    --subnet mySubnet \
    --private-connection-resource-id "/subscriptions/.../storageAccounts/mystorageacct" \
    --group-id file \
    --connection-name myConnection
```

#### Firewall Rules
- Restrict access to specific IP addresses or VNets
- Configure in Storage Account → Networking

---

## Snapshots and Backup

### File Share Snapshots

**What are Snapshots?**
- Point-in-time read-only copies
- Incremental (only changes are stored)
- Up to 200 snapshots per file share
- Retained even if file share is deleted

**Create Snapshot (Azure CLI)**:
```bash
az storage share snapshot \
    --name myfileshare \
    --account-name mystorageacct
```

**List Snapshots**:
```bash
az storage share list \
    --account-name mystorageacct \
    --include-snapshot \
    --query "[?name=='myfileshare']"
```

**Restore from Snapshot**:
1. Navigate to File share → **Snapshots**
2. Select snapshot
3. Browse to file/folder
4. Click **Restore**

---

### Azure Backup

**Benefits**:
- Automated backup scheduling
- Retention policies
- Centralized management
- Compliance and governance

**Enable Backup**:
1. Navigate to Storage Account → **File shares**
2. Select file share
3. Click **Backup**
4. Create or select Recovery Services vault
5. Configure backup policy
6. Click **Enable backup**

---

## Real-World Use Cases

### Use Case 1: Shared Configuration Files

**Scenario**: Multiple web servers need access to shared configuration files

**Solution**:
```bash
# Mount on all web servers
sudo mount -t cifs \
    //mystorageacct.file.core.windows.net/config \
    /etc/app/config \
    -o credentials=/etc/smbcredentials/mystorageacct.cred

# Application reads from /etc/app/config
# Updates to config files are immediately available to all servers
```

---

### Use Case 2: Centralized Log Collection

**Scenario**: Collect logs from multiple VMs in one location

**Solution**:
```powershell
# Mount on all VMs
New-PSDrive -Name L -PSProvider FileSystem `
    -Root "\\mystorageacct.file.core.windows.net\logs" `
    -Credential $credential -Persist

# Configure application to write logs to L:\
# All logs centralized for analysis
```

---

### Use Case 3: Kubernetes Persistent Volumes

**Scenario**: Containerized applications need persistent storage

**Solution**:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: azurefile-pv
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteMany
  azureFile:
    secretName: azure-storage-secret
    shareName: myfileshare
    readOnly: false
```

---

## Best Practices

### Performance
- ✅ Use Premium tier for production workloads
- ✅ Enable large file shares for better IOPS
- ✅ Use SMB 3.0 or higher for better performance
- ✅ Mount file shares close to compute resources (same region)

### Security
- ✅ Use Azure AD authentication when possible
- ✅ Enable encryption at rest and in transit
- ✅ Use private endpoints for sensitive data
- ✅ Rotate storage account keys regularly
- ✅ Enable soft delete for accidental deletion protection

### Cost Optimization
- ✅ Use Cool tier for infrequently accessed data
- ✅ Set appropriate quotas to prevent overage
- ✅ Delete unused snapshots
- ✅ Monitor usage and adjust tiers accordingly

### Reliability
- ✅ Enable snapshots for backup
- ✅ Use Azure Backup for automated protection
- ✅ Choose appropriate redundancy (LRS, ZRS, GRS)
- ✅ Test restore procedures regularly

---

## Troubleshooting

### Common Issues

**Issue 1: Cannot mount file share on Windows**
```
Error: The network path was not found
```
**Solution**:
- Verify port 445 is open (SMB protocol)
- Check storage account firewall rules
- Ensure correct storage account name and key

**Test Port 445**:
```powershell
Test-NetConnection -ComputerName mystorageacct.file.core.windows.net -Port 445
```

---

**Issue 2: Permission denied on Linux**
```
Error: mount error(13): Permission denied
```
**Solution**:
- Verify credentials are correct
- Check file/directory permissions (dir_mode, file_mode)
- Ensure CIFS utilities are installed

---

**Issue 3: Slow performance**
```
File operations are very slow
```
**Solution**:
- Check if you're hitting IOPS or throughput limits
- Consider upgrading to Premium tier
- Enable large file shares
- Verify network latency between VM and storage

---

## Summary

Azure File Shares provide a fully managed, cloud-based file sharing solution that:

1. **Supports standard protocols** (SMB, NFS) for easy integration
2. **Works across platforms** (Windows, Linux, macOS)
3. **Enables concurrent access** from multiple clients
4. **Offers multiple tiers** (Standard, Premium) for different performance needs
5. **Integrates with Azure AD** for secure authentication
6. **Provides snapshots and backup** for data protection

**When to Use**:
- ✅ Lift and shift applications requiring file shares
- ✅ Shared configuration or log files
- ✅ Development and testing environments
- ✅ Kubernetes persistent volumes
- ✅ Hybrid cloud scenarios with Azure File Sync

**Key Takeaway**: Azure File Shares eliminate the need to manage file servers while providing the same functionality with better scalability, availability, and security.
