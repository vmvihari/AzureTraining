# Assignment 1: Azure File Shares (Linux)

## Overview

Azure File Shares provide fully managed file shares in the cloud that are accessible via the industry-standard Server Message Block (SMB) protocol, Network File System (NFS) protocol, and Azure Files REST API. This assignment focuses on mounting and using Azure File Shares on Linux Virtual Machines.

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

---

## Creating Azure File Shares

### Method 1: Azure Portal

**Steps**:
1. Navigate to your **Storage Account**
2. In the left menu, select **File shares** (under Data storage)
3. Click **+ File share**
4. Configure:
   - **Name**: `myfileshare` (lowercase, 3-63 characters)
   - **Tier**: Transaction optimized (default), Hot, or Cool
   - **Quota**: Maximum size (e.g., 100 GB)
5. Click **Create**

### Method 2: Azure CLI

```bash
# Create file share
az storage share create \
  --name myfileshare \
  --account-name mystorageacct \
  --quota 100
```

---

## Mounting Azure File Shares on Linux

### Prerequisites

Ensure your Linux VM has the necessary utilities installed.

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install cifs-utils

# RHEL/CentOS
sudo yum install cifs-utils
```

### Option 1: Temporary Mount (Manual)

This method mounts the share for the current session. The mount will be lost after a reboot.

1. **Get Connection Details**:
   - Go to Azure Portal → Storage Account → File shares
   - Select your share → Click **Connect** → Select **Linux**
   - Copy the storage account key or the generated script

2. **Mount Command**:

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

3. **Test Access**:

```bash
# Create test file
echo "Hello from Azure File Share" | sudo tee $MOUNT_POINT/test.txt

# List files
ls -la $MOUNT_POINT

# Read file
cat $MOUNT_POINT/test.txt
```

### Option 2: Persistent Mount (via /etc/fstab)

This method ensures the share is automatically mounted when the VM boots.

1. **Create Credentials File**:
   Storing credentials in a separate file is more secure than putting them directly in `/etc/fstab`.

```bash
# Create credentials directory
sudo mkdir -p /etc/smbcredentials

# Create credentials file
sudo bash -c 'cat > /etc/smbcredentials/mystorageacct.cred << EOF
username=mystorageacct
password=your-storage-key
EOF'

# Secure the credentials file (read/write only for root)
sudo chmod 600 /etc/smbcredentials/mystorageacct.cred
```

2. **Add Entry to /etc/fstab**:

```bash
# Create mount point if it doesn't exist
sudo mkdir -p /mnt/myfileshare

# Backup fstab
sudo cp /etc/fstab /etc/fstab.backup

# Add entry to /etc/fstab
# Note: dir_mode and file_mode 0777 gives full permissions to all users. Adjust as needed.
sudo bash -c 'cat >> /etc/fstab << EOF
//mystorageacct.file.core.windows.net/myfileshare /mnt/myfileshare cifs nofail,credentials=/etc/smbcredentials/mystorageacct.cred,dir_mode=0777,file_mode=0777,serverino
EOF'
```

3. **Verify and Mount**:

```bash
# Mount all entries in fstab
sudo mount -a

# Verify mount
df -h | grep myfileshare
```

4. **Test Persistence**:
   - Reboot the VM: `sudo reboot`
   - After reconnecting, check if mounted: `df -h | grep myfileshare`

---

## Troubleshooting

### Common Issues

**Issue 1: Permission denied (mount error 13)**
- **Cause**: Incorrect username or password (storage key).
- **Solution**: Verify the storage account name and key in your credentials file.

**Issue 2: Network path not found (mount error 2)**
- **Cause**: DNS resolution failure or firewall blocking port 445.
- **Solution**:
  - Ensure port 445 (SMB) is open outbound on your VM.
  - Check if your ISP blocks port 445 (common for residential IPs).
  - Verify the storage account name is correct.

**Issue 3: Read-only file system**
- **Cause**: Incorrect permissions or mount options.
- **Solution**: Check `dir_mode` and `file_mode` in your mount command or fstab entry.

---

## Best Practices

- **Security**: Always use a credentials file for `/etc/fstab` mounts. Restrict access to this file (`chmod 600`).
- **Performance**: Use the Premium tier for IO-intensive workloads.
- **Backup**: Enable Azure Backup for your file shares to protect against accidental deletion.
- **Encryption**: Azure File Shares use encryption in transit (SMB 3.0+). Ensure your client supports it.

---

## Summary

In this assignment, you learned how to:
1. Create an Azure File Share.
2. Install necessary CIFS utilities on Linux.
3. Mount the share manually for temporary access.
4. Configure `/etc/fstab` for persistent mounting across reboots.
5. Securely store credentials.
