# Azure Storage Services Overview

## Introduction

Azure Storage provides a comprehensive suite of cloud storage services designed to handle different types of data and access patterns. Each service is optimized for specific scenarios, from storing massive amounts of unstructured data to providing high-performance file shares for enterprise applications.

## Storage Browser Components

When you navigate to a storage account in the Azure Portal, you'll find four main storage services under the "Data storage" section:

1. **Blob Containers** - Unstructured data storage
2. **File Shares** - Network file shares
3. **Queues** - Message queuing
4. **Tables** - NoSQL data storage

---

## Blob Storage

### Overview

**Purpose**: Store massive amounts of unstructured data

**Data Types**: 
- Images (JPG, PNG, GIF)
- Videos (MP4, AVI, MOV)
- Documents (PDF, Word, PowerPoint)
- Backups and archives
- Logs and telemetry data
- Static website content

### Blob Types

#### Block Blobs
- **Use Case**: General-purpose storage
- **Optimized For**: Text and binary files
- **Max Size**: ~190.7 TB (4.75 TB per block × 50,000 blocks)
- **Examples**: Images, videos, documents, backups

#### Append Blobs
- **Use Case**: Append operations (logging scenarios)
- **Optimized For**: Sequential write operations
- **Max Size**: ~195 GB
- **Examples**: Application logs, audit logs, streaming data

#### Page Blobs
- **Use Case**: Random read/write operations
- **Optimized For**: Virtual machine disks
- **Max Size**: 8 TB
- **Examples**: Azure VM OS disks, data disks

### Key Features

**Access Tiers**:
- Hot, Cool, Cold, Archive
- Optimize costs based on access frequency

**Access Levels**:
- Private, Blob, Container
- Control anonymous access

**Versioning and Soft Delete**:
- Maintain blob history
- Recover deleted data

**Lifecycle Management**:
- Automatically transition blobs to cooler tiers
- Delete old data based on rules

### Common Use Cases

- **Website Hosting**: Static website content (HTML, CSS, JavaScript, images)
- **Media Storage**: Videos, images for streaming applications
- **Backup and Disaster Recovery**: Long-term data retention
- **Data Lakes**: Big data analytics storage
- **Content Distribution**: Serve files globally via Azure CDN

---

## File Shares

### Overview

**Purpose**: Fully managed cloud file shares accessible via SMB and NFS protocols

**Key Characteristic**: Can be mounted like traditional network drives

**Capacity**: Up to 100 TB per file share

**Protocols**:
- **SMB (Server Message Block)**: Windows, Linux, macOS
- **NFS (Network File System)**: Linux and macOS

### How It Works

File shares provide a shared storage location that multiple virtual machines or on-premises systems can access simultaneously.

**Access Methods**:
1. **Mount on Windows**: Map as network drive (e.g., Z:\)
2. **Mount on Linux**: Mount via SMB or NFS
3. **REST API**: Programmatic access
4. **Azure Portal**: Web-based file management

### Performance Tiers

#### Standard File Shares
- **Storage**: HDD-backed
- **Performance**: Up to 60 MB/s per share
- **Use Cases**: General file sharing, dev/test environments

#### Premium File Shares
- **Storage**: SSD-backed
- **Performance**: Up to 100,000 IOPS per share
- **Use Cases**: High-performance applications, databases, enterprise workloads

### Key Features

**Snapshots**:
- Point-in-time read-only copies
- Protection against accidental deletion or modification
- Retention for backup purposes

**Azure File Sync**:
- Sync on-premises file servers with Azure
- Cloud tiering to optimize local storage
- Multi-site access to same data

**Active Directory Integration**:
- Identity-based authentication
- NTFS permissions support
- Seamless integration with Windows environments

### Common Use Cases

- **Lift and Shift**: Migrate applications that use file shares to Azure
- **Shared Application Data**: Multiple VMs accessing same configuration files
- **Development Tools**: Shared code repositories, build outputs
- **Containerized Applications**: Persistent storage for containers
- **Hybrid Cloud**: Extend on-premises file shares to cloud
- **Disaster Recovery**: Backup for on-premises file servers

### Mounting File Shares on VMs

**Windows Example**:
```powershell
# Map drive using storage account key
net use Z: \\mystorageacct.file.core.windows.net\myshare /u:AZURE\mystorageacct <storage-key>
```

**Linux Example**:
```bash
# Mount using SMB
sudo mount -t cifs //mystorageacct.file.core.windows.net/myshare /mnt/myshare \
  -o vers=3.0,username=mystorageacct,password=<storage-key>,dir_mode=0777,file_mode=0777
```

---

## Queue Storage

### Overview

**Purpose**: Reliable messaging between application components

**Key Characteristic**: Asynchronous communication and decoupling

**Message Size**: Up to 64 KB per message

**Queue Size**: Millions of messages (limited by storage account capacity)

### How It Works

Queues enable asynchronous processing by allowing applications to send and receive messages independently.

**Message Flow**:
1. **Producer**: Application adds messages to queue
2. **Queue**: Stores messages reliably
3. **Consumer**: Application retrieves and processes messages
4. **Delete**: Consumer deletes message after successful processing

### Key Features

**Message Visibility Timeout**:
- Message becomes invisible when retrieved
- Prevents multiple consumers from processing same message
- Configurable timeout (default: 30 seconds)

**Message TTL (Time-to-Live)**:
- Messages expire after specified duration
- Default: 7 days
- Maximum: 7 days

**Peek Messages**:
- View messages without removing from queue
- Useful for monitoring and debugging

**Poison Message Handling**:
- Track dequeue count
- Move messages that fail repeatedly to dead-letter queue

### Common Use Cases

- **Task Queuing**: Distribute work across multiple workers
- **Load Leveling**: Smooth out traffic spikes
- **Decoupling Components**: Separate front-end from back-end processing
- **Asynchronous Processing**: Image resizing, email sending, report generation
- **Workflow Orchestration**: Multi-step business processes

### Example Scenario

**E-commerce Order Processing**:
1. User places order → Message added to `orders` queue
2. Order processor retrieves message → Validates inventory
3. Payment processor retrieves from `payments` queue → Charges customer
4. Shipping processor retrieves from `shipping` queue → Creates shipping label
5. Notification service sends confirmation email

---

## Table Storage

### Overview

**Purpose**: NoSQL key-value store for semi-structured data

**Key Characteristic**: Schema-less, flexible data model

**Scale**: Billions of entities, terabytes of data

**Cost**: Very cost-effective for large datasets

### Data Model

**Tables**: Collection of entities (like a database table, but schema-less)

**Entities**: Individual records (like rows)
- Each entity has a **PartitionKey** and **RowKey** (together form primary key)
- Can have up to 252 properties
- Properties can vary between entities in same table

**Properties**: Key-value pairs (like columns)
- Supported types: String, Binary, Boolean, DateTime, Double, GUID, Int32, Int64

### Key Concepts

#### Partition Key
- **Purpose**: Distributes data across storage partitions
- **Performance**: Entities with same partition key are stored together
- **Querying**: Queries within single partition are fastest

#### Row Key
- **Purpose**: Unique identifier within a partition
- **Combination**: PartitionKey + RowKey = unique entity identifier

**Example**:
```
PartitionKey: "Customer_USA"
RowKey: "12345"
Properties: {Name: "John Doe", Email: "john@example.com", Age: 30}
```

### Key Features

**Schema Flexibility**:
- No predefined schema
- Each entity can have different properties
- Easy to evolve data model

**Scalability**:
- Automatic partitioning
- Horizontal scaling
- High throughput

**Querying**:
- Filter by PartitionKey and RowKey
- OData query syntax
- Limited query capabilities compared to SQL

### Common Use Cases

- **IoT Telemetry**: Store sensor data from millions of devices
- **User Profiles**: Flexible schema for user attributes
- **Logging and Diagnostics**: Application logs, audit trails
- **Product Catalogs**: E-commerce products with varying attributes
- **Session State**: Web application session data
- **Metadata Storage**: File metadata, indexing information

### Working with Tables

**Python Example**:
```python
from azure.data.tables import TableServiceClient

# Connect to table service
table_service = TableServiceClient.from_connection_string(conn_str)

# Get table client
table_client = table_service.get_table_client("customers")

# Insert entity
entity = {
    "PartitionKey": "USA",
    "RowKey": "12345",
    "Name": "John Doe",
    "Email": "john@example.com"
}
table_client.create_entity(entity)

# Query entities
entities = table_client.query_entities("PartitionKey eq 'USA'")
for entity in entities:
    print(entity)
```

**.NET Example**:
```csharp
using Azure.Data.Tables;

// Connect to table service
var tableServiceClient = new TableServiceClient(connectionString);

// Get table client
var tableClient = tableServiceClient.GetTableClient("customers");

// Define entity class
public class CustomerEntity : ITableEntity
{
    public string PartitionKey { get; set; } = "USA";
    public string RowKey { get; set; } = "12345";
    public DateTimeOffset? Timestamp { get; set; }
    public ETag ETag { get; set; }
    public string Name { get; set; } = "John Doe";
    public string Email { get; set; } = "john@example.com";
}

// Insert entity
var entity = new CustomerEntity();
await tableClient.AddEntityAsync(entity);

// Query entities
var entities = tableClient.QueryAsync<CustomerEntity>(
    filter: $"PartitionKey eq 'USA'"
);

await foreach (var customer in entities)
{
    Console.WriteLine($"{customer.Name}: {customer.Email}");
}
```

### Table Storage vs Cosmos DB

| Feature | Table Storage | Cosmos DB (Table API) |
|---------|---------------|----------------------|
| **Performance** | Good | Excellent (single-digit ms latency) |
| **Global Distribution** | No | Yes |
| **SLA** | 99.9% | 99.99% (multi-region) |
| **Indexing** | PartitionKey + RowKey only | All properties automatically |
| **Cost** | Lower | Higher |
| **Use Case** | Cost-sensitive, regional apps | Mission-critical, global apps |

---

## Service Comparison Matrix

| Service | Data Type | Access Method | Max Size | Best For |
|---------|-----------|---------------|----------|----------|
| **Blob Storage** | Unstructured | HTTP/HTTPS, REST API | 190.7 TB per blob | Media, backups, data lakes |
| **File Shares** | Files | SMB, NFS, REST API | 100 TB per share | Shared file access, lift-and-shift |
| **Queue Storage** | Messages | REST API, SDKs | Unlimited (64 KB per msg) | Async processing, decoupling |
| **Table Storage** | Semi-structured | REST API, SDKs | Unlimited | NoSQL data, IoT, logs |

---

## Integration Scenarios

### Scenario 1: Web Application Architecture

**Components**:
- **Blob Storage**: Static website content (images, CSS, JavaScript)
- **File Shares**: Shared configuration files across web servers
- **Queue Storage**: Background job processing (email, reports)
- **Table Storage**: User session state, application logs

### Scenario 2: Data Processing Pipeline

**Flow**:
1. **Blob Storage**: Raw data ingestion
2. **Queue Storage**: Trigger processing jobs
3. **Azure Functions**: Process data
4. **Table Storage**: Store processed results
5. **Blob Storage**: Archive processed data

### Scenario 3: Enterprise File Server Migration

**Components**:
- **File Shares**: Replace on-premises file servers
- **Azure File Sync**: Sync with remaining on-premises servers
- **Blob Storage**: Long-term archive of old files
- **Backup**: Azure Backup for file share protection

---

## Advanced Integration Topics

### Virtual Machine Integration

**Blob Storage**:
- VM disk storage (page blobs)
- Boot diagnostics logs
- Custom script extensions

**File Shares**:
- Mounted as network drives
- Shared application data
- Configuration files

### Kubernetes and Container Integration

**Blob Storage**:
- Container image storage (Azure Container Registry)
- Persistent volume claims
- Application data

**File Shares**:
- Persistent volumes for stateful applications
- Shared configuration across pods

### Infrastructure as Code

**Terraform/ARM Templates**:
- Automated storage account creation
- Container and file share provisioning
- Access policy configuration

### Load Balancer Integration

**Standard Load Balancer**:
- Distribute traffic across VMs accessing shared storage
- High availability for storage-dependent applications

**Virtual Machine Scale Sets**:
- Auto-scaling VMs that access shared file shares
- Consistent storage access across instances

---

## Best Practices

### Choosing the Right Service

**Use Blob Storage when**:
- Storing unstructured data (images, videos, documents)
- Need access tiers for cost optimization
- Building data lakes or backup solutions

**Use File Shares when**:
- Need SMB/NFS protocol support
- Migrating applications that use file shares
- Require shared access from multiple VMs

**Use Queue Storage when**:
- Need asynchronous processing
- Decoupling application components
- Building reliable messaging systems

**Use Table Storage when**:
- Storing semi-structured NoSQL data
- Need cost-effective storage for large datasets
- Schema flexibility is important

### Performance Optimization

- **Blob Storage**: Use CDN for frequently accessed content
- **File Shares**: Choose Premium for high-performance needs
- **Queue Storage**: Use multiple queues for parallel processing
- **Table Storage**: Design partition keys for even distribution

### Cost Optimization

- **Blob Storage**: Use lifecycle policies to move to cooler tiers
- **File Shares**: Use standard tier unless performance is critical
- **Queue Storage**: Delete processed messages promptly
- **Table Storage**: Most cost-effective for large NoSQL datasets

### Security

- **All Services**: Use SAS tokens for granular access control
- **File Shares**: Enable Active Directory authentication
- **All Services**: Enable encryption at rest and in transit
- **All Services**: Use private endpoints for network isolation

---

## Summary

Azure Storage provides four complementary services:

1. **Blob Storage**: Unstructured data at massive scale
2. **File Shares**: Cloud-based network file shares
3. **Queue Storage**: Reliable messaging for decoupled architectures
4. **Table Storage**: Cost-effective NoSQL storage

**Key Takeaway**: Choose the service that matches your data type and access pattern. Often, solutions use multiple services together for comprehensive storage needs.

---

## Related Concepts

- [Data Types Overview](00-DataTypes.md)
- [Azure Storage Accounts](01-StorageAccounts.md)
- [Blob Containers and Access Levels](02-BlobContainers.md)
- [Real-World Use Cases](04-UseCases.md)
- [Azure Tables](05-AzureTables.md)
- [Python SDK Guide](07-PythonSDK.md)

## Hands-On Practice

- [Assignment 1: Azure File Shares](../Assignments/Assignment01-AzureFileShares.md) - Learn to create and mount file shares
- [Assignment 2: Add Disk to VM](../Assignments/Assignment02-AddDiskToVM.md) - Add additional storage to VMs
