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

### Local Redundancy Storage (LRS)

**How it works**:
- Replicates data **3 times** within a single datacenter
- All copies stored in the same physical location

**Protection Level**:
- ✅ Protects against server rack and drive failures
- ❌ Does NOT protect against datacenter-level disasters

**Durability**: 99.999999999% (11 nines) over a year

**Use Cases**:
- Non-critical data
- Data that can be easily reconstructed
- Cost-sensitive scenarios
- Development and testing

**Cost**: Lowest redundancy option

---

### Zone-Redundant Storage (ZRS)

**How it works**:
- Replicates data across **3 availability zones** in the same region
- Each zone is a separate physical location with independent power, cooling, and networking

**Protection Level**:
- ✅ Protects against datacenter failures
- ❌ Does NOT protect against regional disasters

**Durability**: 99.9999999999% (12 nines) over a year

**Use Cases**:
- High availability requirements
- Mission-critical applications
- Compliance requirements for data residency

**Availability**: Not available in all regions

---

### Geo-Redundant Storage (GRS)

**How it works**:
- Combines LRS in primary region with LRS in a secondary region
- Data replicated to a paired region **hundreds of miles away**
- Secondary region data is **not accessible** for read unless failover occurs

**Protection Level**:
- ✅ Protects against regional disasters
- ✅ Highest level of durability

**Durability**: 99.99999999999999% (16 nines) over a year

**Use Cases**:
- Business-critical data
- Disaster recovery requirements
- Long-term data retention
- Compliance and regulatory requirements

**Failover**: Manual or Microsoft-managed failover to secondary region

---

### Read-Access Geo-Redundant Storage (RA-GRS)

**How it works**:
- Same as GRS, but with **read access** to the secondary region
- Applications can read from secondary region even without failover

**Protection Level**:
- Same as GRS
- Additional benefit of read availability during primary region outage

**Use Cases**:
- Applications requiring high read availability
- Global content distribution
- Disaster recovery with minimal downtime

**Endpoints**:
- Primary: `https://mystorageacct.blob.core.windows.net`
- Secondary: `https://mystorageacct-secondary.blob.core.windows.net`

---

### Geo-Zone-Redundant Storage (GZRS)

**How it works**:
- Combines ZRS in primary region with LRS in secondary region
- Best of both: zone redundancy + geo redundancy

**Protection Level**:
- ✅ Protects against zone failures
- ✅ Protects against regional disasters

**Durability**: 99.99999999999999% (16 nines) over a year

**Use Cases**:
- Maximum availability and durability
- Critical workloads requiring both zone and geo protection

**Also Available**: RA-GZRS (with read access to secondary)

---

### Redundancy Comparison Table

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

#### Hot Tier
- **Use Case**: Frequently accessed data
- **Characteristics**: Higher storage cost, lower access cost
- **Examples**: Active website images, application data, streaming content
- **Ideal For**: Data accessed multiple times per day

#### Cool Tier
- **Use Case**: Infrequently accessed data (stored for at least 30 days)
- **Characteristics**: Lower storage cost, higher access cost
- **Examples**: Short-term backups, older media files
- **Ideal For**: Data accessed a few times per month

#### Cold Tier
- **Use Case**: Rarely accessed data (stored for at least 90 days)
- **Characteristics**: Even lower storage cost, higher access cost than Cool
- **Examples**: Long-term backups, compliance archives
- **Ideal For**: Data accessed a few times per year

#### Archive Tier
- **Use Case**: Long-term archival (stored for at least 180 days)
- **Characteristics**: Lowest storage cost, highest access cost
- **Rehydration Required**: Must rehydrate to Hot/Cool before accessing (hours)
- **Examples**: Legal archives, historical records, compliance data
- **Ideal For**: Data rarely or never accessed

**Access Tier Comparison**:

| Tier | Storage Cost | Access Cost | Minimum Storage | Retrieval Time |
|------|--------------|-------------|-----------------|----------------|
| Hot | Highest | Lowest | None | Immediate |
| Cool | Lower | Higher | 30 days | Immediate |
| Cold | Even Lower | Even Higher | 90 days | Immediate |
| Archive | Lowest | Highest | 180 days | Hours (rehydration) |

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
