# Assignment 3: Extend Storage of Attached Disk That Has Become Full

## Overview

This guide explains how to extend the storage capacity of an existing disk attached to an Azure Virtual Machine when it has become full. This is a common scenario as applications grow and require more storage space.

---

## When to Extend Disk Storage

### Common Scenarios

1. **Disk Space Running Low**
   - Application data growing beyond current capacity
   - Database files consuming all available space
   - Log files filling up the disk
   - Warning: "Low disk space" alerts

2. **Planned Capacity Increase**
   - Anticipating future growth
   - Migrating large datasets
   - Expanding database capacity
   - Adding new features requiring more storage

3. **Performance Optimization**
   - Larger disks often have better IOPS and throughput
   - Premium SSD performance scales with size

---

## Important Concepts

### Disk Expansion Process

The process involves **two steps**:

1. **Expand the Azure disk** (increase disk size in Azure)
2. **Extend the partition/filesystem** (make the OS recognize the new space)

> [!IMPORTANT]
> Expanding the Azure disk does NOT automatically make the space available to the OS. You must also extend the partition and filesystem.

### Limitations and Considerations

- ✅ **Can expand**: Disks can be expanded (made larger)
- ❌ **Cannot shrink**: Disks cannot be made smaller
- ⚠️ **Downtime**: 
  - **OS disk**: Requires VM to be deallocated (stopped)
  - **Data disk**: Can be expanded while VM is running (no downtime)
- ⚠️ **Backup first**: Always take a snapshot before expanding

---

## Step 1: Check Current Disk Usage

### Windows

```powershell
# Check disk space
Get-PSDrive -PSProvider FileSystem

# Detailed disk information
Get-Volume

# Specific drive
Get-Volume -DriveLetter F

# Output example:
# DriveLetter FileSystemLabel FileSystem Size         SizeRemaining
# ----------- --------------- ---------- ----         -------------
# F           DataDisk        NTFS       128 GB       5 GB          <-- Almost full!
```

### Linux

```bash
# Check disk space
df -h

# Output example:
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sdc1       126G  120G  1.2G  99% /datadisk    <-- Almost full!

# Detailed disk information
lsblk

# Output example:
# NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
# sdc      8:32   0  128G  0 disk 
# └─sdc1   8:33   0  128G  0 part /datadisk
```

---

## Step 2: Create Snapshot (Backup)

> [!WARNING]
> Always create a snapshot before expanding a disk. This allows you to restore if something goes wrong.

### Azure Portal

1. Navigate to **Virtual machines** → Select your VM
2. Go to **Disks**
3. Click on the disk you want to expand
4. Click **Create snapshot**
5. Configure:
   - **Name**: `myVM-datadisk-snapshot-20240115`
   - **Snapshot type**: **Full**
   - **Storage type**: **Standard HDD** (cheaper for backups)
6. Click **Review + create** → **Create**

### Azure CLI

```bash
# Variables
RESOURCE_GROUP="myResourceGroup"
DISK_NAME="myVM-datadisk-01"
SNAPSHOT_NAME="myVM-datadisk-snapshot-$(date +%Y%m%d)"

# Create snapshot
az snapshot create \
    --resource-group $RESOURCE_GROUP \
    --name $SNAPSHOT_NAME \
    --source $DISK_NAME

# Verify
az snapshot show \
    --resource-group $RESOURCE_GROUP \
    --name $SNAPSHOT_NAME \
    --output table
```

### PowerShell

```powershell
# Variables
$resourceGroup = "myResourceGroup"
$diskName = "myVM-datadisk-01"
$snapshotName = "myVM-datadisk-snapshot-$(Get-Date -Format 'yyyyMMdd')"
$location = "eastus"

# Get disk
$disk = Get-AzDisk -ResourceGroupName $resourceGroup -DiskName $diskName

# Create snapshot configuration
$snapshotConfig = New-AzSnapshotConfig `
    -SourceUri $disk.Id `
    -Location $location `
    -CreateOption Copy

# Create snapshot
New-AzSnapshot `
    -ResourceGroupName $resourceGroup `
    -SnapshotName $snapshotName `
    -Snapshot $snapshotConfig
```

---

## Step 3: Expand the Azure Disk

### Azure Portal

#### For Data Disk (No Downtime)

1. Navigate to **Virtual machines** → Select your VM
2. Go to **Disks**
3. Click on the **data disk** you want to expand
4. Click **Size + performance**
5. Select a larger size (e.g., 128 GB → 256 GB)
   - Note: You can only increase, not decrease
6. Click **Resize**
7. Wait for the operation to complete (usually 1-2 minutes)

#### For OS Disk (Requires Downtime)

1. **Stop (deallocate) the VM**:
   - Navigate to VM → Click **Stop**
   - Wait until status shows "Stopped (deallocated)"
2. Go to **Disks**
3. Click on the **OS disk**
4. Click **Size + performance**
5. Select a larger size
6. Click **Resize**
7. **Start the VM** after resize completes

---

### Azure CLI

#### For Data Disk

```bash
# Variables
RESOURCE_GROUP="myResourceGroup"
DISK_NAME="myVM-datadisk-01"
NEW_SIZE=256  # GB (must be larger than current size)

# Expand disk (no VM stop required for data disks)
az disk update \
    --resource-group $RESOURCE_GROUP \
    --name $DISK_NAME \
    --size-gb $NEW_SIZE

# Verify
az disk show \
    --resource-group $RESOURCE_GROUP \
    --name $DISK_NAME \
    --query "diskSizeGb" \
    --output tsv
```

#### For OS Disk

```bash
# Variables
RESOURCE_GROUP="myResourceGroup"
VM_NAME="myVM"
NEW_SIZE=128  # GB

# Stop (deallocate) VM
az vm deallocate \
    --resource-group $RESOURCE_GROUP \
    --name $VM_NAME

# Get OS disk name
OS_DISK_NAME=$(az vm show \
    --resource-group $RESOURCE_GROUP \
    --name $VM_NAME \
    --query "storageProfile.osDisk.name" \
    --output tsv)

# Expand OS disk
az disk update \
    --resource-group $RESOURCE_GROUP \
    --name $OS_DISK_NAME \
    --size-gb $NEW_SIZE

# Start VM
az vm start \
    --resource-group $RESOURCE_GROUP \
    --name $VM_NAME
```

---

### PowerShell

#### For Data Disk

```powershell
# Variables
$resourceGroup = "myResourceGroup"
$diskName = "myVM-datadisk-01"
$newSize = 256  # GB

# Get disk
$disk = Get-AzDisk -ResourceGroupName $resourceGroup -DiskName $diskName

# Update disk size
$disk.DiskSizeGB = $newSize

# Apply update
Update-AzDisk `
    -ResourceGroupName $resourceGroup `
    -DiskName $diskName `
    -Disk $disk

# Verify
Get-AzDisk -ResourceGroupName $resourceGroup -DiskName $diskName | `
    Select-Object Name, DiskSizeGB
```

#### For OS Disk

```powershell
# Variables
$resourceGroup = "myResourceGroup"
$vmName = "myVM"
$newSize = 128  # GB

# Stop VM
Stop-AzVM -ResourceGroupName $resourceGroup -Name $vmName -Force

# Get VM
$vm = Get-AzVM -ResourceGroupName $resourceGroup -Name $vmName

# Get OS disk
$osDiskName = $vm.StorageProfile.OsDisk.Name
$disk = Get-AzDisk -ResourceGroupName $resourceGroup -DiskName $osDiskName

# Update disk size
$disk.DiskSizeGB = $newSize
Update-AzDisk -ResourceGroupName $resourceGroup -DiskName $osDiskName -Disk $disk

# Start VM
Start-AzVM -ResourceGroupName $resourceGroup -Name $vmName
```

---

## Step 4: Extend Partition and Filesystem

After expanding the Azure disk, you must extend the partition and filesystem inside the OS.

### Windows

#### Option 1: Disk Management GUI

1. **RDP to the VM**
2. Right-click **Start** → **Disk Management**
3. You'll see **unallocated space** next to your partition
4. Right-click the partition (e.g., F:) → **Extend Volume**
5. Follow the wizard:
   - Click **Next**
   - Select amount of space (use maximum)
   - Click **Next** → **Finish**
6. The partition is now extended

#### Option 2: PowerShell (Recommended)

```powershell
# List all partitions
Get-Partition

# Identify the partition to extend (e.g., DriveLetter F)
$driveLetter = "F"

# Get partition
$partition = Get-Partition -DriveLetter $driveLetter

# Get maximum supported size
$maxSize = (Get-PartitionSupportedSize -DriveLetter $driveLetter).SizeMax

# Extend partition to maximum size
Resize-Partition -DriveLetter $driveLetter -Size $maxSize

# Verify
Get-Partition -DriveLetter $driveLetter
Get-Volume -DriveLetter $driveLetter
```

#### Option 3: DiskPart (Command Line)

```cmd
# Open DiskPart
diskpart

# List volumes
list volume

# Select volume (replace 2 with your volume number)
select volume 2

# Extend volume
extend

# Exit
exit
```

---

### Linux

The process varies depending on the partition type and filesystem.

#### Step 1: Rescan Disk

```bash
# Rescan SCSI bus to detect new disk size
echo 1 | sudo tee /sys/class/block/sdc/device/rescan

# Verify new disk size
lsblk
# Output should show larger disk size for sdc, but partition sdc1 is still old size
# NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
# sdc      8:32   0  256G  0 disk           <-- New size
# └─sdc1   8:33   0  128G  0 part /datadisk <-- Old size
```

---

#### Step 2: Extend Partition

**For GPT partitions (parted)**:

```bash
# Install parted if not available
sudo apt-get install parted  # Ubuntu/Debian
# sudo yum install parted    # RHEL/CentOS

# Extend partition to use all available space
sudo parted /dev/sdc resizepart 1 100%

# Verify
sudo parted /dev/sdc print
lsblk
# Now sdc1 should show 256G
```

**For MBR partitions (fdisk)**:

```bash
# This is more complex - you need to delete and recreate the partition
# WARNING: This does NOT delete data, but be careful!

sudo fdisk /dev/sdc

# Commands:
# p    - print partition table (note start sector of partition 1)
# d    - delete partition 1
# n    - create new partition
# p    - primary
# 1    - partition number 1
# Enter - accept default start sector (MUST be same as before!)
# Enter - accept default end sector (uses all space)
# N    - do not remove signature
# w    - write changes

# Reboot or re-read partition table
sudo partprobe /dev/sdc
# or
sudo reboot
```

---

#### Step 3: Extend Filesystem

**For ext4 filesystem**:

```bash
# Check filesystem first
sudo e2fsck -f /dev/sdc1

# Resize filesystem
sudo resize2fs /dev/sdc1

# Verify
df -h | grep datadisk
# Output should show new size
```

**For xfs filesystem**:

```bash
# XFS must be mounted to resize
# If not mounted, mount it first
sudo mount /dev/sdc1 /datadisk

# Resize filesystem
sudo xfs_growfs /datadisk

# Verify
df -h | grep datadisk
```

**For btrfs filesystem**:

```bash
# Resize btrfs
sudo btrfs filesystem resize max /datadisk

# Verify
df -h | grep datadisk
```

---

#### Complete Linux Example (ext4)

```bash
# 1. Rescan disk
echo 1 | sudo tee /sys/class/block/sdc/device/rescan

# 2. Verify new disk size
lsblk

# 3. Extend partition (GPT)
sudo parted /dev/sdc resizepart 1 100%

# 4. Check filesystem
sudo e2fsck -f /dev/sdc1

# 5. Resize filesystem
sudo resize2fs /dev/sdc1

# 6. Verify
df -h | grep datadisk
lsblk

# Output should show:
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sdc1       251G  120G  119G  51% /datadisk  <-- New size!
```

---

## Verification

### Windows

```powershell
# Check volume
Get-Volume -DriveLetter F

# Check partition
Get-Partition -DriveLetter F

# Check disk
Get-Disk

# Create test file to verify write access
"Test after expansion" | Out-File F:\test-expansion.txt
Get-Content F:\test-expansion.txt
```

### Linux

```bash
# Check disk space
df -h | grep datadisk

# Check partition
lsblk

# Check filesystem
sudo dumpe2fs /dev/sdc1 | grep -i "block count"  # ext4
# or
sudo xfs_info /datadisk  # xfs

# Create test file
echo "Test after expansion" | sudo tee /datadisk/test-expansion.txt
cat /datadisk/test-expansion.txt
```

---

## Troubleshooting

### Issue 1: Partition Not Showing New Size (Linux)

**Problem**: After expanding disk, partition still shows old size

**Solution**:
```bash
# Reboot the VM
sudo reboot

# Or re-read partition table
sudo partprobe /dev/sdc

# Or rescan SCSI bus
echo 1 | sudo tee /sys/class/block/sdc/device/rescan
```

---

### Issue 2: Cannot Extend Volume (Windows)

**Error**: "There is not enough space available on the disk(s) to complete this operation"

**Possible Causes**:
1. Recovery partition between OS partition and unallocated space
2. Disk is MBR and trying to extend beyond 2 TB

**Solution**:
```powershell
# Check partition layout
Get-Partition

# If recovery partition is in the way, you may need to:
# 1. Delete recovery partition (backup first!)
# 2. Extend main partition
# 3. Recreate recovery partition (optional)
```

---

### Issue 3: Filesystem Resize Fails (Linux)

**Error**: "resize2fs: Bad magic number in super-block"

**Solution**:
```bash
# Check filesystem type
sudo blkid /dev/sdc1

# Use correct resize command:
# ext4: resize2fs
# xfs: xfs_growfs
# btrfs: btrfs filesystem resize
```

---

## Best Practices

### Planning

- ✅ **Monitor disk usage** proactively (set alerts at 80% full)
- ✅ **Plan for growth** (expand before running out of space)
- ✅ **Size appropriately** (don't expand too frequently, plan ahead)
- ✅ **Consider performance** (larger Premium SSD = better IOPS)

### Safety

- ✅ **Always take snapshot** before expanding
- ✅ **Test in non-production** first
- ✅ **Backup critical data** before any disk operations
- ✅ **Document changes** (record old/new sizes, date, reason)

### Performance

- ✅ **Expand during maintenance window** (for OS disks)
- ✅ **Data disks can be expanded online** (no downtime)
- ✅ **Monitor performance** after expansion
- ✅ **Consider disk type upgrade** if performance is issue

### Cost Optimization

- ✅ **Don't over-provision** (pay for what you need)
- ✅ **Use appropriate tier** (Standard vs Premium)
- ✅ **Clean up old data** before expanding (may not need more space)
- ✅ **Consider archiving** old data to cheaper storage

---

## Alternative Solutions

### Instead of Expanding Disk

1. **Add Another Disk**
   - See [Assignment 2: Add Disk to VM](Assignment02-AddDiskToVM.md)
   - Good for separating workloads
   - No downtime for data disks

2. **Clean Up Existing Data**
   - Delete old logs, temporary files
   - Archive old data to Blob Storage (Cool/Archive tier)
   - Compress files

3. **Use Azure File Shares**
   - See [Assignment 1: Azure File Shares](Assignment01-AzureFileShares.md)
   - Good for shared data across VMs
   - Easier to expand (just increase quota)

4. **Implement Data Lifecycle Policies**
   - Automatically move old data to cheaper storage
   - Delete temporary data after retention period

---

## Summary

Extending disk storage involves:

1. **Create snapshot** (backup before changes)
2. **Expand Azure disk** via Portal, CLI, or PowerShell
   - Data disk: No downtime
   - OS disk: Requires VM stop
3. **Extend partition** in the OS
   - Windows: Disk Management or PowerShell
   - Linux: parted or fdisk
4. **Extend filesystem**
   - Windows: Automatic with partition extension
   - Linux: resize2fs (ext4), xfs_growfs (xfs), etc.
5. **Verify** new size is available

**Key Takeaways**:
- ✅ Always snapshot before expanding
- ✅ Expanding Azure disk ≠ Expanding OS partition (two separate steps)
- ✅ Data disks can be expanded online (no downtime)
- ✅ OS disks require VM stop (plan for downtime)
- ✅ Cannot shrink disks (only expand)
- ✅ Monitor disk usage proactively

**Related Assignments**:
- [Assignment 1: Azure File Shares](Assignment01-AzureFileShares.md)
- [Assignment 2: Add Disk to VM](Assignment02-AddDiskToVM.md)
