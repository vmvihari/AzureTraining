# Assignment 2: Add Additional Disk to Existing Virtual Machine

## Overview

This guide explains how to add an additional data disk to an existing Azure Virtual Machine. This is a common task when you need more storage for applications, databases, or data files.

---

## Why Add Additional Disks?

### Common Scenarios

1. **Running Out of Space**
   - Application data growing beyond OS disk capacity
   - Database files requiring more storage
   - Log files consuming disk space

2. **Performance Optimization**
   - Separate OS and data disks for better performance
   - Dedicated disk for database files (high IOPS)
   - Isolate workloads to different disks

3. **Data Organization**
   - Separate disks for different applications
   - Dedicated disk for backups
   - Temporary data on separate disk

4. **Compliance Requirements**
   - Encrypted disks for sensitive data
   - Separate disks for audit logs
   - Data residency requirements

---

## Disk Types in Azure

### OS Disk
- Contains operating system
- Created automatically with VM
- Typically C: (Windows) or /dev/sda (Linux)
- Cannot be detached while VM is running

### Data Disk
- Additional storage for applications and data
- Can be attached/detached
- Up to 64 data disks per VM (depending on VM size)
- Can be different types (Standard HDD, Standard SSD, Premium SSD, Ultra Disk)

### Temporary Disk
- Ephemeral storage (data lost on VM stop/restart)
- D: drive on Windows, /dev/sdb on Linux
- Good for page files, temp data
- **Not suitable for important data**

---

## Disk Performance Tiers

| Disk Type | IOPS | Throughput | Use Case | Cost |
|-----------|------|------------|----------|------|
| **Standard HDD** | Up to 500 | Up to 60 MB/s | Backups, infrequent access | Lowest |
| **Standard SSD** | Up to 6,000 | Up to 750 MB/s | Web servers, dev/test | Low |
| **Premium SSD** | Up to 20,000 | Up to 900 MB/s | Production, databases | Medium |
| **Ultra Disk** | Up to 160,000 | Up to 4,000 MB/s | Mission-critical, SAP HANA | Highest |

---

## Adding a Disk: Azure Portal

### Step 1: Navigate to Virtual Machine

1. Open **Azure Portal** (portal.azure.com)
2. Navigate to **Virtual machines**
3. Select your VM (e.g., `myVM`)
4. Ensure VM is **running** or **stopped** (deallocated is fine)

---

### Step 2: Add Data Disk

1. In the VM blade, select **Disks** (under Settings)
2. Click **+ Create and attach a new disk**

**Configure the disk**:
- **Disk name**: `myVM-datadisk-01`
- **Source type**: **None (empty disk)**
- **Size**: Select size (e.g., 128 GB, 256 GB, 512 GB, 1 TB)
- **Disk SKU**: 
  - **Standard HDD** (cost-effective)
  - **Standard SSD** (balanced)
  - **Premium SSD** (high performance)
  - **Ultra Disk** (extreme performance)
- **Host caching**: 
  - **None** (for write-heavy workloads)
  - **Read-only** (for read-heavy workloads)
  - **Read/write** (for balanced workloads)
- **Encryption**: 
  - **Platform-managed key** (default)
  - **Customer-managed key** (for compliance)

3. Click **Save**

> [!NOTE]
> The disk will be attached to the VM, but it won't be usable until you initialize and format it inside the OS.

---

## Adding a Disk: Azure CLI

### Create and Attach New Disk

```bash
# Variables
RESOURCE_GROUP="myResourceGroup"
VM_NAME="myVM"
DISK_NAME="myVM-datadisk-01"
DISK_SIZE=128  # GB
DISK_SKU="Premium_LRS"  # Standard_LRS, StandardSSD_LRS, Premium_LRS, UltraSSD_LRS

# Create managed disk
az disk create \
    --resource-group $RESOURCE_GROUP \
    --name $DISK_NAME \
    --size-gb $DISK_SIZE \
    --sku $DISK_SKU

# Attach disk to VM
az vm disk attach \
    --resource-group $RESOURCE_GROUP \
    --vm-name $VM_NAME \
    --name $DISK_NAME

# Verify disk is attached
az vm show \
    --resource-group $RESOURCE_GROUP \
    --name $VM_NAME \
    --query "storageProfile.dataDisks" \
    --output table
```

---

### Attach Existing Disk

```bash
# If you have an existing disk to attach
az vm disk attach \
    --resource-group $RESOURCE_GROUP \
    --vm-name $VM_NAME \
    --name $EXISTING_DISK_NAME
```

---

## Adding a Disk: PowerShell

### Create and Attach New Disk

```powershell
# Variables
$resourceGroup = "myResourceGroup"
$vmName = "myVM"
$diskName = "myVM-datadisk-01"
$diskSize = 128  # GB
$diskSku = "Premium_LRS"  # Standard_LRS, StandardSSD_LRS, Premium_LRS, UltraSSD_LRS
$location = "eastus"

# Get VM
$vm = Get-AzVM -ResourceGroupName $resourceGroup -Name $vmName

# Create disk configuration
$diskConfig = New-AzDiskConfig `
    -Location $location `
    -CreateOption Empty `
    -DiskSizeGB $diskSize `
    -SkuName $diskSku

# Create managed disk
$disk = New-AzDisk `
    -ResourceGroupName $resourceGroup `
    -DiskName $diskName `
    -Disk $diskConfig

# Attach disk to VM
$vm = Add-AzVMDataDisk `
    -VM $vm `
    -Name $diskName `
    -CreateOption Attach `
    -ManagedDiskId $disk.Id `
    -Lun 0  # Logical Unit Number (0-63)

# Update VM
Update-AzVM -ResourceGroupName $resourceGroup -VM $vm

# Verify
Get-AzVM -ResourceGroupName $resourceGroup -Name $vmName | `
    Select-Object -ExpandProperty StorageProfile | `
    Select-Object -ExpandProperty DataDisks
```

---

## Initializing and Formatting the Disk

### Windows VM

#### Step 1: Connect to VM

```powershell
# RDP to the VM
mstsc /v:<VM-Public-IP>
```

#### Step 2: Initialize Disk

**Option 1: Disk Management GUI**

1. Right-click **Start** → **Disk Management**
2. You'll see a popup: "Initialize Disk"
3. Select **GPT** (GUID Partition Table) for disks > 2 TB, or **MBR** for smaller disks
4. Click **OK**

**Option 2: PowerShell**

```powershell
# List all disks
Get-Disk

# Initialize disk (replace 2 with your disk number)
Initialize-Disk -Number 2 -PartitionStyle GPT

# Verify
Get-Disk -Number 2
```

---

#### Step 3: Create Partition and Format

**Option 1: Disk Management GUI**

1. Right-click the **Unallocated** space
2. Select **New Simple Volume**
3. Follow the wizard:
   - Volume size: Use maximum
   - Drive letter: Select (e.g., F:)
   - File system: **NTFS**
   - Allocation unit size: **Default**
   - Volume label: `DataDisk`
   - Quick format: **Checked**
4. Click **Finish**

**Option 2: PowerShell**

```powershell
# Create partition using all available space
$partition = New-Partition -DiskNumber 2 -UseMaximumSize -AssignDriveLetter

# Format the partition
Format-Volume `
    -DriveLetter $partition.DriveLetter `
    -FileSystem NTFS `
    -NewFileSystemLabel "DataDisk" `
    -Confirm:$false

# Verify
Get-Volume -DriveLetter $partition.DriveLetter
```

---

#### Step 4: Verify and Test

```powershell
# Check disk
Get-Disk -Number 2

# Check volume
Get-Volume -DriveLetter F

# Create test file
"Hello from new disk" | Out-File F:\test.txt

# Read test file
Get-Content F:\test.txt

# Check disk space
Get-PSDrive F
```

---

### Linux VM

#### Step 1: Connect to VM

```bash
# SSH to the VM
ssh azureuser@<VM-Public-IP>
```

#### Step 2: Identify the New Disk

```bash
# List all disks
lsblk

# Output example:
# NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
# sda      8:0    0   30G  0 disk 
# ├─sda1   8:1    0 29.9G  0 part /
# ├─sda14  8:14   0    4M  0 part 
# └─sda15  8:15   0  106M  0 part /boot/efi
# sdb      8:16   0   14G  0 disk 
# └─sdb1   8:17   0   14G  0 part /mnt
# sdc      8:32   0  128G  0 disk    <-- New disk (no partitions)

# The new disk is typically /dev/sdc (or /dev/sdd, etc.)
```

---

#### Step 3: Partition the Disk

**Option 1: Using fdisk**

```bash
# Start fdisk
sudo fdisk /dev/sdc

# Commands to enter:
# n    - new partition
# p    - primary partition
# 1    - partition number
# Enter - default first sector
# Enter - default last sector (use all space)
# w    - write changes and exit

# Verify partition created
lsblk
# Output should show /dev/sdc1
```

**Option 2: Using parted (for GPT)**

```bash
# Create GPT partition table
sudo parted /dev/sdc mklabel gpt

# Create partition using all space
sudo parted -a opt /dev/sdc mkpart primary ext4 0% 100%

# Verify
sudo parted /dev/sdc print
```

---

#### Step 4: Format the Partition

```bash
# Format as ext4 (most common for Linux)
sudo mkfs.ext4 /dev/sdc1

# Alternative: Format as xfs
# sudo mkfs.xfs /dev/sdc1

# Verify
sudo blkid /dev/sdc1
# Output: /dev/sdc1: UUID="..." TYPE="ext4" ...
```

---

#### Step 5: Create Mount Point and Mount

```bash
# Create mount point
sudo mkdir -p /datadisk

# Mount the partition
sudo mount /dev/sdc1 /datadisk

# Verify mount
df -h | grep datadisk
# Output: /dev/sdc1  126G   61M  120G   1% /datadisk

# Test write
echo "Hello from new disk" | sudo tee /datadisk/test.txt
cat /datadisk/test.txt
```

---

#### Step 6: Make Mount Persistent (Auto-mount on Reboot)

**Get UUID of the partition**:
```bash
sudo blkid /dev/sdc1
# Output: /dev/sdc1: UUID="12345678-1234-1234-1234-123456789abc" TYPE="ext4" ...

# Copy the UUID value
```

**Add to /etc/fstab**:
```bash
# Backup fstab first
sudo cp /etc/fstab /etc/fstab.backup

# Add entry to fstab (replace UUID with your actual UUID)
echo 'UUID=12345678-1234-1234-1234-123456789abc /datadisk ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab

# Verify fstab syntax
sudo mount -a

# If no errors, reboot to test
sudo reboot

# After reboot, verify mount
df -h | grep datadisk
```

> [!IMPORTANT]
> Always use UUID instead of device name (/dev/sdc1) in /etc/fstab because device names can change on reboot.

---

## Best Practices

### Disk Selection

- ✅ **Use Premium SSD** for production databases and high-performance applications
- ✅ **Use Standard SSD** for web servers and general applications
- ✅ **Use Standard HDD** for backups and infrequent access
- ✅ **Use Ultra Disk** only for mission-critical workloads (SAP HANA, SQL Server)

### Host Caching

- ✅ **None**: For write-heavy workloads (databases, transaction logs)
- ✅ **Read-only**: For read-heavy workloads (web servers, data warehouses)
- ✅ **Read/write**: For balanced workloads (general applications)

> [!WARNING]
> Never use Read/write caching for database data files or transaction logs. Use None or Read-only.

### Partitioning

- ✅ **Use GPT** for disks larger than 2 TB
- ✅ **Use MBR** for smaller disks (compatibility with older systems)
- ✅ **Single partition** for data disks (simplicity)

### File Systems

**Windows**:
- ✅ **NTFS**: Standard for Windows (supports large files, permissions, encryption)
- ❌ **FAT32**: Limited to 4 GB files (avoid for data disks)

**Linux**:
- ✅ **ext4**: Most common, reliable, good performance
- ✅ **xfs**: Better for large files, used by RHEL/CentOS by default
- ✅ **btrfs**: Advanced features (snapshots, compression) but less mature

### Security

- ✅ **Enable encryption** for sensitive data (Azure Disk Encryption)
- ✅ **Use managed disks** (easier management, better availability)
- ✅ **Regular snapshots** for backup and disaster recovery
- ✅ **RBAC permissions** to control who can attach/detach disks

---

## Troubleshooting

### Issue 1: Disk Not Showing in OS

**Windows**:
```powershell
# Rescan disks
Update-HostStorageCache

# Check Disk Management
diskmgmt.msc
```

**Linux**:
```bash
# Rescan SCSI bus
echo "- - -" | sudo tee /sys/class/scsi_host/host*/scan

# List disks again
lsblk
```

---

### Issue 2: Cannot Attach Disk

**Error**: "The disk is already attached to another VM"

**Solution**:
```bash
# Detach from other VM first
az vm disk detach \
    --resource-group $RESOURCE_GROUP \
    --vm-name $OTHER_VM_NAME \
    --name $DISK_NAME

# Then attach to target VM
az vm disk attach \
    --resource-group $RESOURCE_GROUP \
    --vm-name $VM_NAME \
    --name $DISK_NAME
```

---

### Issue 3: Mount Fails After Reboot (Linux)

**Error**: "mount: /datadisk: can't find UUID=..."

**Solution**:
```bash
# Check if UUID changed
sudo blkid /dev/sdc1

# Update /etc/fstab with correct UUID
sudo nano /etc/fstab

# Test mount
sudo mount -a
```

---

## Summary

Adding an additional disk to an Azure VM involves:

1. **Create and attach disk** via Azure Portal, CLI, or PowerShell
2. **Initialize disk** in the operating system
3. **Create partition** using Disk Management (Windows) or fdisk/parted (Linux)
4. **Format partition** with NTFS (Windows) or ext4/xfs (Linux)
5. **Mount partition** and make it persistent (Linux: /etc/fstab)

**Key Takeaways**:
- ✅ Choose appropriate disk type based on performance needs
- ✅ Use managed disks for easier management
- ✅ Always use UUID in /etc/fstab (Linux)
- ✅ Test mount persistence by rebooting
- ✅ Enable encryption for sensitive data
- ✅ Take snapshots for backup

**Next Steps**: See [Assignment 3: Extend Disk Storage](Assignment03-ExtendDiskStorage.md) to learn how to expand disk size when you run out of space.
