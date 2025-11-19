# Azure Storage Services

This section covers Azure storage services and concepts based on hands-on training sessions.

## Table of Contents

- [Concepts](#concepts)
- [Hands-On Labs](#hands-on-labs)
- [Assignments](#assignments)

## Concepts

Dive deeper into specific Azure Storage concepts with these detailed guides:

- **[00 - Data Types Overview](Concepts/00-DataTypes.md)** - Understanding structured, semi-structured, and unstructured data
- **[01 - Azure Storage Accounts](Concepts/01-StorageAccounts.md)** - Performance tiers, redundancy, and configuration
- **[02 - Blob Containers and Access Levels](Concepts/02-BlobContainers.md)** - Container management, security, and SAS tokens
- **[03 - Storage Services Overview](Concepts/03-StorageServices.md)** - Blobs, Files, Queues, and Tables
- **[04 - Real-World Use Cases](Concepts/04-UseCases.md)** - Practical scenarios and advanced integration patterns
- **[05 - Azure Tables](Concepts/05-AzureTables.md)** - NoSQL key-value store for structured data
- **[06 - Static Website Hosting](Concepts/06-StaticWebsiteHosting.md)** - Host static websites directly from Azure Storage
- **[07 - Python SDK Guide](Concepts/07-PythonSDK.md)** - Programmatic access to Azure Storage with Python
- **[08 - .NET SDK Guide](Concepts/08-DotNetSDK.md)** - Programmatic access to Azure Storage with C# and .NET

## Hands-On Labs

Practice your Azure Storage skills with these comprehensive labs:

### [Lab 01: Azure Blob Storage - Storage Accounts and Container Access Levels](Labs/Lab01-BlobStorage.md)
**Duration**: 45-60 minutes | **Difficulty**: Beginner

Learn how to create and configure Azure Storage Accounts, work with blob containers, and understand different access levels through hands-on exercises.

**What you'll learn:**
- Create resource groups and storage accounts
- Configure blob containers with private, blob-level, and container-level access
- Upload and manage blobs
- Test and validate anonymous access behavior
- Apply real-world scenarios for image processing workflows

## Assignments

Practice essential Azure storage operations with these hands-on assignments:

### [Assignment 1: Azure File Shares](Assignments/Assignment01-AzureFileShares.md)
**Topics**: File share creation, mounting on Windows/Linux, performance tiers, security

Learn how to create and use Azure File Shares for shared storage across multiple VMs. Covers SMB/NFS protocols, persistent mounting, Azure AD authentication, and real-world use cases.

---

### [Assignment 2: Add Additional Disk to Existing VM](Assignments/Assignment02-AddDiskToVM.md)
**Topics**: Disk types, creation, attachment, initialization, formatting

Learn how to add additional data disks to Azure VMs. Covers disk performance tiers, initialization on Windows (Disk Management, PowerShell) and Linux (fdisk, parted), and making mounts persistent.

---

### [Assignment 3: Extend Storage of Attached Disk](Assignments/Assignment03-ExtendDiskStorage.md)
**Topics**: Disk expansion, snapshot creation, partition extension, filesystem resizing

Learn how to expand existing disks when running out of space. Covers snapshot creation, Azure disk expansion, partition extension on Windows and Linux, and troubleshooting common issues.

---