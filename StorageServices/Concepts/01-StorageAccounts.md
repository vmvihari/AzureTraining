# Azure Storage Accounts

## Overview

An Azure Storage Account is a foundational resource that provides a unique namespace for storing and accessing Azure Storage data objects. It serves as the container for all Azure Storage services including blobs, files, queues, and tables.

## Creating a Storage Account

### Naming Requirements

**Rules**:
- Must be **globally unique** across all of Azure
- Length: 3-24 characters
- Only lowercase letters and numbers
- No special characters, spaces, or uppercase letters

**Examples**:
- ✅ `mystorageacct2024`
- ✅ `companydata01`
- ✅ `webappblobs123`
- ❌ `MyStorageAcct` (uppercase)
- ❌ `storage-account` (hyphen)
- ❌ `st` (too short)

> [!TIP]
> Use a naming convention that includes: company/project prefix + purpose + environment + number
> Example: `contosoweb01prod`

---

## Performance Tiers

Azure Storage offers two performance tiers to match different workload requirements.

### Standard Performance

**Characteristics**:
- Backed by magnetic hard disk drives (HDDs)
- Cost-effective for most scenarios
- Suitable for general-purpose workloads

**Use Cases**:
- Web applications
- Backup and disaster recovery
- Media storage and distribution
- Development and testing environments
- Data analytics and big data

**Supported Services**:
- Blob Storage (all types)
- File Shares
- Queue Storage
- Table Storage

**Pricing**: Lower cost per GB

---

### Premium Performance

**Characteristics**:
- Backed by solid-state drives (SSDs)
- Low latency and high throughput
- Consistent performance for I/O-intensive workloads

**Types of Premium Storage**:

#### Premium Block Blobs
- Optimized for high transaction rates
- Ideal for small objects and low-latency scenarios
- Use cases: IoT data, streaming, gaming

#### Premium File Shares
- Enterprise-grade file shares
- SMB and NFS protocol support
  - **Server Message Block (SMB)**: A network protocol enabling computers to share files, printers, and other resources over a network
    - **How it works**: Client computers request access to resources on a server, which responds to enable seamless access to files as if they were stored locally
    - **Usage**: Commonly used in Windows environments, with support across macOS, Linux, and Android
  - **Network File System (NFS)**: A client-server protocol that allows users on one computer to access files stored on another computer over a network
    - **How it works**: Clients make requests to an NFS server using Remote Procedure Calls (RPC) to read, write, or modify files. The server verifies file existence and client permissions before granting access
    - **Origins**: Originally developed by Sun Microsystems in 1984, now an open standard with various versions (NFSv4 being the most recent)
    - **Usage**: Popular in Unix-based systems including Linux, with support on other platforms like Windows Server for cross-platform interoperability
- Use cases: Lift-and-shift applications, databases

#### Premium Page Blobs
- Optimized for random read/write operations
- Use cases: Azure Virtual Machine disks (OS and data disks)

**Pricing**: Higher cost per GB, but better performance

---

### Performance Tier Comparison

| Feature | Standard | Premium |
|---------|----------|---------|
| **Storage Medium** | HDD | SSD |
| **Latency** | Higher | Lower (single-digit milliseconds) |
| **IOPS** | Up to 20,000 | Up to 100,000+ |
| **Throughput** | Up to 60 MB/s per blob | Up to 200 MB/s per blob |
| **Cost** | Lower | Higher |
| **Best For** | General workloads | Performance-critical apps |

---

## Redundancy Options

Redundancy ensures your data is protected against hardware failures, datacenter outages, and regional disasters.

| Redundancy Type | How It Works | Protection Level | Durability | Use Cases | Special Notes |
|-----------------|--------------|------------------|------------|-----------|---------------|
| **LRS**<br>(Local Redundancy Storage) | • Replicates data **3 times** within a single datacenter<br>• All copies stored in the same physical location | ✅ Protects against server rack and drive failures<br>❌ Does NOT protect against datacenter-level disasters | 99.999999999%<br>(11 nines) | • Non-critical data<br>• Data that can be easily reconstructed<br>• Cost-sensitive scenarios<br>• Development and testing | **Cost**: Lowest redundancy option |
| **ZRS**<br>(Zone-Redundant Storage) | • Replicates data across **3 availability zones** in the same region<br>• Each zone is a separate physical location with independent power, cooling, and networking | ✅ Protects against datacenter failures<br>❌ Does NOT protect against regional disasters | 99.9999999999%<br>(12 nines) | • High availability requirements<br>• Mission-critical applications<br>• Compliance requirements for data residency | **Availability**: Not available in all regions |
| **GRS**<br>(Geo-Redundant Storage) | • Combines LRS in primary region with LRS in a secondary region<br>• Data replicated to a paired region **hundreds of miles away**<br>• Secondary region data is **not accessible** for read unless failover occurs | ✅ Protects against regional disasters<br>✅ Highest level of durability | 99.99999999999999%<br>(16 nines) | • Business-critical data<br>• Disaster recovery requirements<br>• Long-term data retention<br>• Compliance and regulatory requirements | **Failover**: Manual or Microsoft-managed failover to secondary region |
| **RA-GRS**<br>(Read-Access Geo-Redundant Storage) | • Same as GRS, but with **read access** to the secondary region<br>• Applications can read from secondary region even without failover | • Same as GRS<br>• Additional benefit of read availability during primary region outage | 99.99999999999999%<br>(16 nines) | • Applications requiring high read availability<br>• Global content distribution<br>• Disaster recovery with minimal downtime | **Endpoints**:<br>• Primary: `https://mystorageacct.blob.core.windows.net`<br>• Secondary: `https://mystorageacct-secondary.blob.core.windows.net` |
| **GZRS**<br>(Geo-Zone-Redundant Storage) | • Combines ZRS in primary region with LRS in secondary region<br>• Best of both: zone redundancy + geo redundancy | ✅ Protects against zone failures<br>✅ Protects against regional disasters | 99.99999999999999%<br>(16 nines) | • Maximum availability and durability<br>• Critical workloads requiring both zone and geo protection | **Also Available**: RA-GZRS (with read access to secondary) |

### Quick Comparison

| Redundancy | Copies | Locations | Protects Against | Durability (9s) | Relative Cost |
|------------|--------|-----------|------------------|-----------------|---------------|
| **LRS** | 3 | 1 datacenter | Hardware failures | 11 | $ |
| **ZRS** | 3 | 3 zones (1 region) | Datacenter failures | 12 | $$ |
| **GRS** | 6 | 2 regions | Regional disasters | 16 | $$$ |
| **RA-GRS** | 6 | 2 regions | Regional disasters + read HA | 16 | $$$+ |
| **GZRS** | 6 | 3 zones + 2 regions | Zone + regional disasters | 16 | $$$$ |
| **RA-GZRS** | 6 | 3 zones + 2 regions | Zone + regional disasters + read HA | 16 | $$$$+ |

---

## Storage Account Configuration

### Access Tiers

Data access tiers optimize storage costs based on how frequently you access your data.

| Tier | Use Case | Characteristics | Examples | Ideal For | Storage Cost | Access Cost | Minimum Storage | Retrieval Time |
|------|----------|-----------------|----------|-----------|--------------|-------------|-----------------|----------------|
| **Hot** | Frequently accessed data | Higher storage cost, lower access cost | • Active website images<br>• Application data<br>• Streaming content | Data accessed multiple times per day | Highest | Lowest | None | Immediate |
| **Cool** | Infrequently accessed data | Lower storage cost, higher access cost | • Short-term backups<br>• Older media files | Data accessed a few times per month | Lower | Higher | 30 days | Immediate |
| **Cold** | Rarely accessed data | Even lower storage cost, higher access cost than Cool | • Long-term backups<br>• Compliance archives | Data accessed a few times per year | Even Lower | Even Higher | 90 days | Immediate |
| **Archive** | Long-term archival | Lowest storage cost, highest access cost<br>**Rehydration Required**: Must rehydrate to Hot/Cool before accessing | • Legal archives<br>• Historical records<br>• Compliance data | Data rarely or never accessed | Lowest | Highest | 180 days | Hours (rehydration) |

---

### Security and Access Control

#### Secure Transfer Requirement

**What it does**: Enforces HTTPS for all requests to the storage account

**Benefits**:
- Encrypts data in transit
- Protects against man-in-the-middle attacks
- Industry best practice

**Recommendation**: Always enable for production workloads

---

#### Access Keys

**Primary and Secondary Keys**:
- Full access to all storage account resources
- Should be treated like passwords
- Rotate regularly for security

**Best Practices**:
- Store keys in Azure Key Vault
- Use secondary key during rotation
- Never commit keys to source control
- Regenerate if compromised

---

#### Shared Access Signatures (SAS)

**What it is**: A URI that grants restricted access rights to storage resources

**Benefits**:
- Granular permissions (read, write, delete, list)
- Time-limited access
- IP address restrictions
- Protocol restrictions (HTTPS only)

**Types**:
- **Account SAS**: Access to multiple services
- **Service SAS**: Access to specific service (blob, file, queue, table)
- **User Delegation SAS**: Secured with Azure AD credentials (most secure)

**Use Cases**:
- Granting temporary access to clients
- Third-party integrations
- Mobile app access to storage

---

#### Anonymous Blob Access

**Setting**: Allow/Disallow public anonymous access to blobs

**Default**: Disabled (for security)

**When to Enable**:
- Public website assets (images, CSS, JavaScript)
- Public datasets or documentation
- Content delivery scenarios

**Security Note**: Only enable if you have a legitimate business need for public access

---

## Storage Account Types

### General-Purpose v2 (GPv2)

**Recommended**: Yes, for most scenarios

**Supports**:
- All storage services (blobs, files, queues, tables)
- All redundancy options
- All access tiers
- Latest features and capabilities

**Use Cases**: Default choice for new storage accounts

---

### General-Purpose v1 (GPv1)

**Recommended**: No, legacy option

**Limitations**:
- No access tier support
- Higher transaction costs
- Missing newer features

**Migration**: Upgrade to GPv2 (no downtime)

---

### Blob Storage

**Recommended**: No, use GPv2 instead

**Purpose**: Legacy account type for blob-only scenarios

**Note**: GPv2 provides all the same capabilities with more flexibility

---

### Premium Storage Types

- **BlockBlobStorage**: Premium block blobs
- **FileStorage**: Premium file shares
- **PageBlobStorage**: Premium page blobs (VM disks)

---

## Best Practices

### Naming and Organization
- Use consistent naming conventions
- Include environment indicators (dev, test, prod)
- Separate storage accounts by workload or application

### Performance
- Choose appropriate performance tier based on workload
- Use Premium for latency-sensitive applications
- Monitor IOPS and throughput metrics

### Cost Optimization
- Select the right redundancy level (don't over-provision)
- Use appropriate access tiers for data lifecycle
- Enable lifecycle management policies
- Delete unused storage accounts

### Security
- Enable secure transfer requirement
- Disable public blob access unless needed
- Use SAS tokens instead of account keys
- Enable Azure Defender for Storage
- Configure firewall and virtual network rules

### Monitoring
- Enable diagnostic logging
- Set up alerts for capacity and performance
- Use Azure Monitor for insights
- Track costs with Azure Cost Management

---

## Summary

Azure Storage Accounts are the foundation of Azure Storage services. Key decisions include:

1. **Performance Tier**: Standard for general use, Premium for high performance
2. **Redundancy**: LRS for cost, GRS/GZRS for disaster recovery
3. **Access Tier**: Hot for active data, Cool/Cold/Archive for infrequent access
4. **Security**: Enable secure transfer, use SAS tokens, protect access keys

**Next Steps**: Explore specific storage services like Blob Containers, File Shares, and Tables.

---

## Related Concepts

- [Data Types Overview](00-DataTypes.md)
- [Blob Containers and Access Levels](02-BlobContainers.md)
- [Storage Services Overview](03-StorageServices.md)
- [Real-World Use Cases](04-UseCases.md)
