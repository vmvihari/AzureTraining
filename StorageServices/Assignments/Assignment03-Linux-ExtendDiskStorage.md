# Assignment 3: Extend Storage of Attached Disk That Has Become Full (Linux)

## Overview

This guide explains how to extend the storage capacity of an existing disk attached to a Linux Virtual Machine when it has become full. The process involves expanding the disk in Azure and then resizing the filesystem in Linux.

---

## Important Concepts

- **Two-Step Process**: 
  1. Expand the Azure disk resource.
  2. Extend the partition and filesystem inside the Linux OS.
- **No Downtime for Data Disks**: You can expand data disks while the VM is running.
- **Downtime for OS Disks**: You must stop (deallocate) the VM to expand the OS disk.
- **Backup**: Always take a snapshot before modifying disks.

---

## Step 1: Check Current Disk Usage

```bash
# Check disk space
df -h

# Check block devices
lsblk
```

**Example Output**:
```
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sdc      8:32   0  128G  0 disk 
└─sdc1   8:33   0  128G  0 part /datadisk
```
*In this example, `/dev/sdc` is 128GB and fully allocated to `/dev/sdc1`.*

---

## Step 2: Create Snapshot (Backup)

Before making any changes, create a snapshot in the Azure Portal.

1. Navigate to **Disks**.
2. Select your disk.
3. Click **Create snapshot**.
4. Follow the prompts to create a full backup.

---

## Step 3: Expand the Azure Disk

1. **Navigate to Disk**:
   - Go to Azure Portal → Virtual machines → Select VM → Disks.
   - Click on the disk you want to expand (e.g., `myVM-datadisk-01`).

2. **Resize**:
   - Click **Size + performance**.
   - Select a larger size (e.g., change 128 GB to 256 GB).
   - Click **Resize**.

> [!NOTE]
> If expanding the OS disk, you must stop the VM first. For data disks, you can do this while the VM is running.

---

## Step 4: Extend Partition and Filesystem in Linux

After resizing in Azure, the Linux OS needs to recognize the new space.

### 1. Rescan the Disk
If the new size doesn't show up immediately in `lsblk`, rescan the SCSI bus.

```bash
# Rescan (replace sdc with your device name)
echo 1 | sudo tee /sys/class/block/sdc/device/rescan

# Verify new size
lsblk
```
**Expected Output**:
```
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sdc      8:32   0  256G  0 disk           <-- New size (256G)
└─sdc1   8:33   0  128G  0 part /datadisk <-- Old partition size (128G)
```

### 2. Extend the Partition
Use `parted` to resize the partition to fill the new space.

```bash
# Resize partition 1 to use 100% of the disk
sudo parted /dev/sdc resizepart 1 100%

# Verify
lsblk
```
*Now `sdc1` should show 256G.*

### 3. Extend the Filesystem
The command depends on your filesystem type (`ext4` or `xfs`).

**Check filesystem type**:
```bash
df -T /datadisk
```

**For ext4**:
```bash
# Resize ext4 filesystem
sudo resize2fs /dev/sdc1
```

**For xfs**:
```bash
# Resize xfs filesystem (must be mounted)
sudo xfs_growfs /datadisk
```

### 4. Verify Final Result

```bash
df -h | grep datadisk
```
**Output**:
```
/dev/sdc1       251G  120G  119G  51% /datadisk
```
*The available space should now reflect the expansion.*

---

## Troubleshooting

**Issue: Partition size didn't update**
- **Solution**: Try running `sudo partprobe` to notify the OS of partition table changes.

**Issue: resize2fs fails with "Bad magic number"**
- **Cause**: You are trying to use `resize2fs` on an XFS filesystem.
- **Solution**: Use `xfs_growfs` instead.

**Issue: Cannot expand OS disk**
- **Cause**: VM is running.
- **Solution**: Stop (deallocate) the VM, resize the disk, then start the VM.

---

## Summary

1. **Snapshot** the disk for safety.
2. **Expand** the disk in Azure Portal.
3. **Rescan** disk in Linux (`echo 1 > .../rescan`).
4. **Resize partition** (`parted ... resizepart`).
5. **Resize filesystem** (`resize2fs` or `xfs_growfs`).
