# Azure Storage Services

This section covers Azure storage services and concepts based on hands-on training sessions.

## Table of Contents

- [Topics Covered](#topics-covered)
- [Concepts](#concepts)
- [Hands-On Labs](#hands-on-labs)
- [Getting Started](#getting-started)

## Topics Covered

Explore these comprehensive concept guides to understand Azure Storage Services:

### [Data Types Overview](Concepts/00-DataTypes.md)
Learn about structured, semi-structured, and unstructured data types, and how to choose the right Azure storage solution for each.

**Key Topics**:
- Structured vs Semi-Structured vs Unstructured Data
- RDBMS vs NoSQL comparison
- Decision matrix for choosing storage types

---

### [Azure Storage Accounts](Concepts/01-StorageAccounts.md)
Understand storage account fundamentals, performance tiers, redundancy options, and configuration best practices.

**Key Topics**:
- Creating and naming storage accounts
- Performance tiers (Standard vs Premium)
- Redundancy options (LRS, ZRS, GRS, RA-GRS, GZRS)
- Access tiers (Hot, Cool, Cold, Archive)
- Security and access control (Keys, SAS tokens)

---

### [Blob Containers and Access Levels](Concepts/02-BlobContainers.md)
Deep dive into blob containers, access levels, and data recovery features.

**Key Topics**:
- Container access levels (Private, Blob, Container)
- Anonymous access configuration
- Soft delete for containers and blobs
- Blob versioning and lifecycle management

---

### [Storage Services Overview](Concepts/03-StorageServices.md)
Comprehensive guide to all Azure Storage services: Blobs, Files, Queues, and Tables.

**Key Topics**:
- Blob Storage (Block, Append, Page blobs)
- File Shares (SMB/NFS, mounting on VMs)
- Queue Storage (messaging and decoupling)
- Table Storage (NoSQL key-value store)
- Service comparison and integration scenarios

---

### [Real-World Use Cases and Advanced Topics](Concepts/04-UseCases.md)
Practical scenarios and advanced integration patterns from production environments.

**Key Topics**:
- Automated image processing pipelines
- Kubernetes and container integration
- IoT data ingestion and processing
- Accessing private containers (Keys, SAS, Managed Identities)
- Mounting file shares on VMs
- Batch operations and programmatic access
- Working with Azure Tables using Python

## Concepts

Dive deeper into specific Azure Storage concepts with these detailed guides:

- **[00 - Data Types Overview](Concepts/00-DataTypes.md)** - Understanding structured, semi-structured, and unstructured data
- **[01 - Azure Storage Accounts](Concepts/01-StorageAccounts.md)** - Performance tiers, redundancy, and configuration
- **[02 - Blob Containers and Access Levels](Concepts/02-BlobContainers.md)** - Container management and security
- **[03 - Storage Services Overview](Concepts/03-StorageServices.md)** - Blobs, Files, Queues, and Tables
- **[04 - Real-World Use Cases](Concepts/04-UseCases.md)** - Practical scenarios and advanced integration patterns

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

## Getting Started

Explore the topics above to learn about Azure storage services and how to implement efficient, secure data storage solutions in Azure. Each topic includes practical examples and real-world scenarios from production environments.
