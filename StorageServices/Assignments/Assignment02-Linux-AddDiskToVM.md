# Assignment 2: Add Additional Disk to Existing Virtual Machine (Linux)

## Overview

This guide explains how to add an additional data disk to an existing Linux Virtual Machine in Azure. This is a common task when you need more storage for applications, databases, or data files.

---

## Disk Types in Azure

### OS Disk
- Contains operating system
- Created automatically with VM
- Typically `/dev/sda`
- Cannot be detached while VM is running

### Data Disk
- Additional storage for applications and data
- Can be attached/detached
- Up to 64 data disks per VM (depending on VM size)
- Can be different types (Standard HDD, Standard SSD, Premium SSD, Ultra Disk)

### Temporary Disk
- Ephemeral storage (data lost on VM stop/restart)
- Typically `/dev/sdb`
- Good for swap files, temp data
- **Not suitable for important data**

---

## Step 1: Add Disk in Azure Portal

1. **Navigate to Virtual Machine**:
   - Open Azure Portal → Virtual machines → Select your Linux VM.

2. **Add Data Disk**:
   - Select **Disks** (under Settings).
   - Click **+ Create and attach a new disk**.
   - Configure:
     - **Name**: `myVM-datadisk-01`
     - **Size**: Select size (e.g., 128 GB)
     - **Storage type**: Premium SSD (recommended for performance) or Standard HDD/SSD.
   - Click **Save**.

> [!NOTE]
> The disk is now attached, but the Linux OS doesn't know how to use it yet. You must initialize, partition, and format it.

---

## Step 2: Prepare the Disk in Linux

### 1. Connect to VM
```bash
ssh azureuser@<VM-Public-IP>
```

### 2. Identify the New Disk
Use `lsblk` to list all block devices.

```bash
lsblk
```

**Output Example**:
```
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0   30G  0 disk 
├─sda1   8:1    0 29.9G  0 part /
├─sda14  8:14   0    4M  0 part 
└─sda15  8:15   0  106M  0 part /boot/efi
sdb      8:16   0   14G  0 disk 
└─sdb1   8:17   0   14G  0 part /mnt
sdc      8:32   0  128G  0 disk    <-- New disk (no partitions)
```
*In this example, the new disk is `/dev/sdc`.*

### 3. Partition the Disk
You can use `fdisk` (for MBR) or `parted` (for GPT). We'll use `parted` as it handles large disks (>2TB) better.

```bash
# Create GPT partition table
sudo parted /dev/sdc mklabel gpt

# Create partition using all space
sudo parted -a opt /dev/sdc mkpart primary ext4 0% 100%

# Verify
sudo parted /dev/sdc print
```

### 4. Format the Partition
Format the new partition (`/dev/sdc1`) with the `ext4` filesystem.

```bash
sudo mkfs.ext4 /dev/sdc1
```
*Alternatively, use `mkfs.xfs` for XFS filesystem.*

### 5. Mount the Disk

```bash
# Create mount point
sudo mkdir -p /datadisk

# Mount the partition
sudo mount /dev/sdc1 /datadisk

# Verify mount
df -h | grep datadisk
```

---

## Step 3: Make Mount Persistent

To ensure the disk mounts automatically after a reboot, add it to `/etc/fstab`.

### 1. Get the UUID
Always use UUIDs instead of device names (like `/dev/sdc1`) because device names can change.

```bash
sudo blkid /dev/sdc1
```
**Output**: `/dev/sdc1: UUID="12345678-1234-1234-1234-123456789abc" TYPE="ext4" ...`

### 2. Update /etc/fstab

```bash
# Backup fstab
sudo cp /etc/fstab /etc/fstab.backup

# Add entry (Replace UUID with your actual UUID)
echo 'UUID=12345678-1234-1234-1234-123456789abc /datadisk ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab
```

### 3. Verify Fstab
Always verify `fstab` syntax before rebooting to avoid boot issues.

```bash
# Unmount first
sudo umount /datadisk

# Mount all from fstab
sudo mount -a

# Check if mounted
df -h | grep datadisk
```

---

## Troubleshooting

**Issue: Mount fails after reboot**
- **Cause**: Incorrect UUID or syntax in `/etc/fstab`.
- **Solution**:
  - Check `sudo blkid` again.
  - Edit `/etc/fstab` with `sudo nano /etc/fstab`.
  - Ensure the `nofail` option is used so the VM can still boot if the disk fails.

**Issue: Permission denied when writing**
- **Cause**: The mount point is owned by root.
- **Solution**: Change ownership to your user.
  ```bash
  sudo chown -R azureuser:azureuser /datadisk
  ```

---

## Summary

1. **Attach disk** in Azure Portal.
2. **Identify disk** with `lsblk`.
3. **Partition** with `parted`.
4. **Format** with `mkfs.ext4`.
5. **Mount** manually.
6. **Persist** via `/etc/fstab` using UUID.
