# Training Assignments - Summary

## Overview

This document provides a summary of the three assignments given at the end of the Azure Storage Services training meeting, due the following Monday.

---

## Assignment 1: Azure File Shares

**File**: [Assignment01-AzureFileShares.md](Assignment01-AzureFileShares.md)

### What You'll Learn

- What Azure File Shares are and when to use them
- Difference between File Shares and Blob Storage
- How to create file shares (Portal, CLI, PowerShell)
- Mounting file shares on Windows and Linux VMs
- Making mounts persistent (auto-mount on reboot)
- Performance tiers (Standard vs Premium)
- Security and access control (Azure AD, SAS tokens, private endpoints)
- Snapshots and backup strategies
- Real-world use cases

### Key Concepts

**Azure File Shares** = Fully managed cloud file shares accessible via SMB/NFS protocols

**Use Cases**:
- Lift and shift applications (no code changes)
- Shared configuration files across multiple VMs
- Centralized log collection
- Kubernetes persistent volumes
- Hybrid scenarios with Azure File Sync

**Mounting**:
- **Windows**: PowerShell script with credentials, mount as drive letter (e.g., Z:)
- **Linux**: CIFS mount, add to /etc/fstab for persistence

---

## Assignment 2: Add Additional Disk to Existing Virtual Machine

**File**: [Assignment02-AddDiskToVM.md](Assignment02-AddDiskToVM.md)

### What You'll Learn

- Why and when to add additional disks
- Disk types (OS disk, data disk, temporary disk)
- Performance tiers (Standard HDD, Standard SSD, Premium SSD, Ultra Disk)
- Creating and attaching disks (Portal, CLI, PowerShell)
- Initializing and formatting disks on Windows and Linux
- Making mounts persistent on Linux (/etc/fstab)
- Best practices for disk selection and caching
- Troubleshooting common issues

### Key Concepts

**Two-Step Process**:
1. **Attach disk in Azure** (via Portal, CLI, or PowerShell)
2. **Initialize and format in OS** (Disk Management/PowerShell for Windows, fdisk/parted for Linux)

**Windows**:
- Initialize disk (GPT or MBR)
- Create partition and format as NTFS
- Assign drive letter (e.g., F:)

**Linux**:
- Identify new disk (`lsblk`)
- Partition disk (`fdisk` or `parted`)
- Format partition (`mkfs.ext4` or `mkfs.xfs`)
- Mount partition (`mount`)
- Add to `/etc/fstab` for persistence (use UUID!)

**Performance Tiers**:
- **Standard HDD**: Backups, infrequent access (~$5/month for 128 GB)
- **Standard SSD**: Web servers, dev/test (~$10/month for 128 GB)
- **Premium SSD**: Production, databases (~$20/month for 128 GB)
- **Ultra Disk**: Mission-critical, SAP HANA (~$100+/month)

---

## Assignment 3: Extend Storage of Attached Disk That Has Become Full

**File**: [Assignment03-ExtendDiskStorage.md](Assignment03-ExtendDiskStorage.md)

### What You'll Learn

- When and why to extend disk storage
- Creating snapshots before expansion (critical!)
- Expanding Azure disks (Portal, CLI, PowerShell)
- Extending partitions and filesystems on Windows and Linux
- Differences between OS disk and data disk expansion
- Troubleshooting common issues
- Alternative solutions (add disk, clean up, file shares)

### Key Concepts

**Three-Step Process**:
1. **Create snapshot** (backup before changes!)
2. **Expand Azure disk** (increase size in Azure)
3. **Extend partition/filesystem** (make OS recognize new space)

**Important**:
- ✅ Can expand (make larger)
- ❌ Cannot shrink (make smaller)
- ⚠️ **Data disk**: No downtime (can expand while VM is running)
- ⚠️ **OS disk**: Requires VM stop (plan for downtime)

**Windows**:
- Disk Management GUI: Right-click partition → Extend Volume
- PowerShell: `Resize-Partition -DriveLetter F -Size $maxSize`

**Linux**:
1. Rescan disk: `echo 1 | sudo tee /sys/class/block/sdc/device/rescan`
2. Extend partition: `sudo parted /dev/sdc resizepart 1 100%`
3. Extend filesystem:
   - ext4: `sudo resize2fs /dev/sdc1`
   - xfs: `sudo xfs_growfs /datadisk`

---

## Quick Reference

### Assignment 1: File Shares - Key Commands

**Create File Share**:
```bash
az storage share create --name myfileshare --account-name mystorageacct --quota 100
```

**Mount on Windows**:
```powershell
New-PSDrive -Name Z -PSProvider FileSystem -Root "\\mystorageacct.file.core.windows.net\myfileshare" -Credential $credential -Persist
```

**Mount on Linux**:
```bash
sudo mount -t cifs //mystorageacct.file.core.windows.net/myfileshare /mnt/myfileshare -o credentials=/etc/smbcredentials/mystorageacct.cred
```

---

### Assignment 2: Add Disk - Key Commands

**Create and Attach Disk**:
```bash
az disk create --resource-group myRG --name myDisk --size-gb 128 --sku Premium_LRS
az vm disk attach --resource-group myRG --vm-name myVM --name myDisk
```

**Initialize on Windows**:
```powershell
Initialize-Disk -Number 2 -PartitionStyle GPT
New-Partition -DiskNumber 2 -UseMaximumSize -AssignDriveLetter
Format-Volume -DriveLetter F -FileSystem NTFS -NewFileSystemLabel "DataDisk"
```

**Initialize on Linux**:
```bash
sudo parted /dev/sdc mklabel gpt
sudo parted -a opt /dev/sdc mkpart primary ext4 0% 100%
sudo mkfs.ext4 /dev/sdc1
sudo mount /dev/sdc1 /datadisk
echo 'UUID=<uuid> /datadisk ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab
```

---

### Assignment 3: Extend Disk - Key Commands

**Create Snapshot**:
```bash
az snapshot create --resource-group myRG --name mySnapshot --source myDisk
```

**Expand Disk**:
```bash
az disk update --resource-group myRG --name myDisk --size-gb 256
```

**Extend on Windows**:
```powershell
$maxSize = (Get-PartitionSupportedSize -DriveLetter F).SizeMax
Resize-Partition -DriveLetter F -Size $maxSize
```

**Extend on Linux**:
```bash
echo 1 | sudo tee /sys/class/block/sdc/device/rescan
sudo parted /dev/sdc resizepart 1 100%
sudo resize2fs /dev/sdc1  # ext4
# or
sudo xfs_growfs /datadisk  # xfs
```

---

## Practical Scenarios

### Scenario 1: Web Application with Growing Data

**Problem**: Web application running out of disk space for user uploads

**Solution Path**:
1. Check current usage: `df -h` (Linux) or `Get-Volume` (Windows)
2. If < 80% full: Add new disk (Assignment 2)
3. If > 80% full: Extend existing disk (Assignment 3)
4. Alternative: Use Azure File Share for shared uploads (Assignment 1)

---

### Scenario 2: Multiple VMs Need Shared Configuration

**Problem**: 5 web servers need access to same configuration files

**Solution**: Azure File Share (Assignment 1)
- Create file share
- Mount on all 5 VMs
- Update config in one place, all VMs see changes immediately

---

### Scenario 3: Database Server Running Out of Space

**Problem**: SQL Server database files filling up disk

**Solution Path**:
1. **Immediate**: Extend existing disk (Assignment 3)
   - Create snapshot first!
   - Expand disk to 512 GB or 1 TB
   - Extend partition and filesystem
2. **Long-term**: Add dedicated disk for database files (Assignment 2)
   - Premium SSD for better performance
   - Separate data files and log files to different disks

---

## Best Practices Summary

### File Shares
- ✅ Use Premium tier for production workloads
- ✅ Enable Azure AD authentication for security
- ✅ Use private endpoints for sensitive data
- ✅ Enable snapshots for backup

### Adding Disks
- ✅ Choose appropriate disk type (Standard vs Premium)
- ✅ Use managed disks (easier management)
- ✅ Always use UUID in /etc/fstab (Linux)
- ✅ Enable encryption for sensitive data

### Extending Disks
- ✅ **Always create snapshot before expanding**
- ✅ Expand data disks online (no downtime)
- ✅ Plan OS disk expansion during maintenance window
- ✅ Monitor disk usage proactively (alert at 80%)

---

## Common Mistakes to Avoid

### File Shares
- ❌ Not securing credentials (store in Key Vault)
- ❌ Using storage account key instead of Azure AD
- ❌ Not testing mount persistence (reboot to verify)
- ❌ Forgetting to open port 445 (SMB)

### Adding Disks
- ❌ Not initializing disk after attaching
- ❌ Using device name instead of UUID in /etc/fstab (Linux)
- ❌ Wrong host caching for database workloads
- ❌ Not testing write access after mounting

### Extending Disks
- ❌ **Not creating snapshot before expansion** (biggest mistake!)
- ❌ Expanding Azure disk but not extending partition
- ❌ Trying to shrink disks (not supported)
- ❌ Not planning for downtime when expanding OS disk

---

## Troubleshooting Quick Guide

### File Share Won't Mount
1. Check port 445 is open: `Test-NetConnection -Port 445`
2. Verify storage account name and key
3. Check firewall rules on storage account
4. Ensure CIFS utilities installed (Linux)

### Disk Not Showing After Attach
1. Rescan disks: `Update-HostStorageCache` (Windows)
2. Rescan SCSI bus: `echo "- - -" | sudo tee /sys/class/scsi_host/host*/scan` (Linux)
3. Check Azure Portal to verify disk is attached

### Partition Won't Extend After Disk Expansion
1. Reboot VM or rescan partition table
2. Check for recovery partition in the way (Windows)
3. Verify disk was actually expanded in Azure
4. Use correct tool for filesystem type (resize2fs vs xfs_growfs)

---

## Summary

These three assignments cover essential Azure storage operations:

1. **File Shares**: Shared storage across multiple VMs
2. **Add Disk**: Increase storage capacity by adding new disks
3. **Extend Disk**: Expand existing disks when running out of space

**Key Takeaways**:
- Always backup/snapshot before making changes
- Understand the difference between Azure operations and OS operations
- Test persistence (reboot to verify mounts)
- Monitor disk usage proactively
- Choose appropriate storage type for your workload

**Practice Recommendation**:
1. Create a test VM
2. Complete all three assignments in order
3. Document your steps and any issues encountered
4. Practice troubleshooting scenarios

---

## Additional Resources

- [Assignment 1: Azure File Shares](Assignment01-AzureFileShares.md)
- [Assignment 2: Add Disk to VM](Assignment02-AddDiskToVM.md)
- [Assignment 3: Extend Disk Storage](Assignment03-ExtendDiskStorage.md)
- [Azure Storage Documentation](https://docs.microsoft.com/azure/storage/)
- [Azure VM Disk Documentation](https://docs.microsoft.com/azure/virtual-machines/disks-types)
