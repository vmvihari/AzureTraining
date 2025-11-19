# Blob Containers and Access Levels

## Overview

Blob containers are logical groupings within Azure Storage Accounts that organize and manage blob (Binary Large Object) storage. They function similarly to folders or directories in a file system, providing a way to organize unstructured data like images, videos, documents, and backups.

## What is a Blob Container?

**Definition**: A container is a logical boundary that groups a set of blobs together within a storage account.

**Key Characteristics**:
- Each storage account can have unlimited containers
- Each container can hold unlimited blobs
- Container names must be unique within a storage account
- Containers provide a security boundary for access control

**Naming Rules**:
- 3-63 characters long
- Lowercase letters, numbers, and hyphens only
- Must start with a letter or number
- No consecutive hyphens

**Examples**:
- ✅ `product-images`
- ✅ `user-uploads`
- ✅ `backup2024`
- ❌ `Product-Images` (uppercase)
- ❌ `-backups` (starts with hyphen)
- ❌ `my--container` (consecutive hyphens)

---

## Container Access Levels

Azure Blob Storage provides three access levels that control anonymous (public) access to container data. This is critical for security and determines who can access your blobs without authentication.

> [!IMPORTANT]
> Before setting container-level public access, you must first enable "Allow Blob public access" at the storage account level. This is disabled by default for security.

---

### Private (No Anonymous Access)

**Access Level**: `Private`

**Behavior**:
- ❌ Anonymous users **cannot** access blobs
- ❌ Anonymous users **cannot** list blobs in the container
- ✅ Requires authentication (account key, SAS token, or Azure AD)

**Security**: Highest security level

**Use Cases**:
- User-uploaded content (personal files, documents)
- Sensitive business data
- Internal application data
- Customer information
- Financial records
- Healthcare data (HIPAA compliance)
- Any data requiring authentication

**Example Scenario**:
A healthcare application stores patient medical records. These files must only be accessible to authenticated users with proper permissions.

**Access Methods**:
- Storage account access keys
- Shared Access Signatures (SAS) with appropriate permissions
- Azure Active Directory authentication
- Managed identities for Azure resources

**Error When Accessing Anonymously**:
```
HTTP 404 (ResourceNotFound)
or
HTTP 403 (Public access is not permitted on this storage account)
```

---

### Blob (Anonymous Read Access for Blobs Only)

**Access Level**: `Blob`

**Behavior**:
- ✅ Anonymous users **can** access individual blobs if they know the exact URL
- ❌ Anonymous users **cannot** list blobs in the container
- ✅ Provides "security through obscurity"

**Security**: Medium security level

**Use Cases**:
- Public website assets (images, CSS, JavaScript files)
- Product images for e-commerce sites
- Public documentation files
- Shared media files where listing is not desired
- Content delivery for web applications

**Example Scenario**:
An e-commerce website stores product images. The website needs to display these images publicly, but you don't want users to browse all available images in the container.

**How It Works**:
```
Direct blob URL: ✅ Accessible
https://mystorageacct.blob.core.windows.net/product-images/item123.jpg

Container listing URL: ❌ Not accessible
https://mystorageacct.blob.core.windows.net/product-images?restype=container&comp=list
```

**Security Consideration**: 
While blobs are publicly accessible, users cannot discover blob names without the exact URL. However, if blob names are predictable (e.g., sequential numbers), this provides limited security.

---

### Container (Anonymous Read Access for Containers and Blobs)

**Access Level**: `Container`

**Behavior**:
- ✅ Anonymous users **can** access individual blobs
- ✅ Anonymous users **can** list all blobs in the container
- ✅ Full public read access

**Security**: Lowest security level (fully public)

**Use Cases**:
- Public datasets
- Open-source project assets
- Public documentation repositories
- Shared resources for community access
- Public APIs serving static content
- Research data meant for public consumption

**Example Scenario**:
A government agency publishes public datasets (census data, weather information) that anyone should be able to browse and download.

**How It Works**:
```
Direct blob URL: ✅ Accessible
https://mystorageacct.blob.core.windows.net/public-data/census2024.csv

Container listing URL: ✅ Accessible (returns XML list of all blobs)
https://mystorageacct.blob.core.windows.net/public-data?restype=container&comp=list
```

**Container Listing Response**:
```xml
<?xml version="1.0" encoding="utf-8"?>
<EnumerationResults>
  <Blobs>
    <Blob>
      <Name>census2024.csv</Name>
      <Url>https://...</Url>
      <Properties>...</Properties>
    </Blob>
    <Blob>
      <Name>weather-data.json</Name>
      <Url>https://...</Url>
      <Properties>...</Properties>
    </Blob>
  </Blobs>
</EnumerationResults>
```

---

## Access Level Comparison

| Feature | Private | Blob | Container |
|---------|---------|------|-----------|
| **Anonymous blob access** | ❌ No | ✅ Yes | ✅ Yes |
| **Anonymous container listing** | ❌ No | ❌ No | ✅ Yes |
| **Requires authentication** | ✅ Yes | ❌ No | ❌ No |
| **Blob discoverability** | None | Low (need exact URL) | High (can list all) |
| **Security level** | High | Medium | Low |
| **Best for** | Private data | Public assets | Public datasets |

---

## Enabling Public Access

### Step 1: Enable at Storage Account Level

Before containers can have public access, you must enable it on the storage account:

**Azure Portal**:
1. Navigate to Storage Account → **Configuration**
2. Find **"Allow Blob public access"**
3. Set to **Enabled**
4. Click **Save**

**Azure CLI**:
```bash
az storage account update \
  --name <storage-account-name> \
  --resource-group <resource-group> \
  --allow-blob-public-access true
```

> [!WARNING]
> This setting is disabled by default for security. Only enable if you have a legitimate business need for public blob access.

### Step 2: Set Container Access Level

**Azure Portal**:
1. Navigate to Storage Account → **Containers**
2. Select a container
3. Click **Change access level**
4. Select: Private, Blob, or Container
5. Click **OK**

**Azure CLI**:
```bash
# Create container with specific access level
az storage container create \
  --name my-container \
  --account-name <storage-account-name> \
  --public-access blob  # or 'container' or 'off'
```

---

## Data Recovery Features

### Soft Delete for Containers

**What it does**: Retains deleted containers for a specified retention period

**Benefits**:
- Recover from accidental deletions
- Protection against malicious deletion
- Configurable retention period (1-365 days)

**How to Enable**:
1. Storage Account → **Data protection**
2. Enable **"Container soft delete"**
3. Set retention period (e.g., 7 days)

**Recovery**:
- Deleted containers appear with a "deleted" marker
- Can be restored within the retention period
- Original container name and contents are preserved

**Use Cases**:
- Protection against accidental deletion
- Compliance requirements for data retention
- Disaster recovery scenarios

---

### Soft Delete for Blobs

**What it does**: Retains deleted blobs and blob snapshots

**Benefits**:
- Recover individual files
- Protection against overwrites
- Snapshot preservation

**Configuration**:
- Retention period: 1-365 days
- Applies to all blobs in the storage account

**Recovery Process**:
1. Navigate to container
2. Enable **"Show deleted blobs"**
3. Select deleted blob
4. Click **Undelete**

---

### Blob Versioning

**What it does**: Automatically maintains previous versions of a blob

**How it works**:
- Each modification creates a new version
- Previous versions are preserved
- Each version has a unique version ID

**Benefits**:
- Complete history of blob changes
- Rollback to any previous version
- Protection against accidental overwrites
- Audit trail for compliance

**Use Cases**:
- Document management systems
- Configuration file management
- Image processing workflows (preserve originals)
- Compliance and regulatory requirements

**Example Scenario**:
A nightly script compresses product images. If the compression algorithm malfunctions, blob versioning allows you to immediately restore the original high-resolution images without needing separate backups.

**Version Management**:
```
Current version: image.jpg (version ID: 2024-01-15T10:30:00Z)
Previous version: image.jpg (version ID: 2024-01-14T09:15:00Z)
Original version: image.jpg (version ID: 2024-01-10T08:00:00Z)
```

**Cost Consideration**: Each version consumes storage space. Use lifecycle policies to automatically delete old versions.

---

## Best Practices

### Security
- **Default to Private**: Only make containers public when absolutely necessary
- **Use SAS Tokens**: For temporary access instead of making containers public
- **Regular Audits**: Review public containers periodically
- **Principle of Least Privilege**: Grant minimum necessary permissions

### Organization
- **Logical Grouping**: Organize blobs by purpose, environment, or data type
- **Naming Conventions**: Use consistent, descriptive container names
- **Separate Environments**: Use different containers for dev, test, and production

### Performance
- **Partition Strategy**: Distribute blobs across multiple containers for high-scale scenarios
- **Blob Naming**: Use random prefixes for high-throughput scenarios to avoid partition hotspots

### Cost Optimization
- **Lifecycle Policies**: Automatically move old data to cooler tiers
- **Delete Unused Containers**: Remove containers that are no longer needed
- **Monitor Access Patterns**: Adjust access tiers based on actual usage

### Data Protection
- **Enable Soft Delete**: Protect against accidental deletion
- **Use Versioning**: For critical data that changes frequently
- **Regular Backups**: Even with redundancy, maintain backups for critical data
- **Test Recovery**: Regularly test your ability to restore deleted data

---

## Common Scenarios

### Scenario 1: Public Website Assets

**Requirement**: Serve images, CSS, and JavaScript files for a public website

**Solution**:
- Container: `website-assets`
- Access Level: **Blob**
- Why: Files need to be publicly accessible, but listing all assets is not necessary

### Scenario 2: User File Uploads

**Requirement**: Store files uploaded by authenticated users

**Solution**:
- Container: `user-uploads`
- Access Level: **Private**
- Access Method: Generate SAS tokens for authenticated users
- Why: User data should never be publicly accessible

### Scenario 3: Public Dataset Distribution

**Requirement**: Share research data with the public

**Solution**:
- Container: `public-datasets`
- Access Level: **Container**
- Why: Users should be able to browse and discover available datasets

### Scenario 4: Image Processing Pipeline

**Requirement**: Vendors upload images, script processes them, website displays optimized versions

**Solution**:
- Container 1: `vendor-uploads` (Private) - Raw uploads
- Container 2: `optimized-images` (Blob) - Processed images for website
- Enable: Blob versioning on both containers
- Why: Separate raw and processed data, protect originals, allow public access to optimized images

---

## Summary

Blob containers are the fundamental organizational unit in Azure Blob Storage. Key takeaways:

1. **Choose the right access level**: Private for sensitive data, Blob for public assets, Container for public datasets
2. **Enable data protection**: Use soft delete and versioning for critical data
3. **Follow security best practices**: Default to private, use SAS tokens, audit public containers
4. **Organize logically**: Use clear naming conventions and separate containers by purpose

**Remember**: Storage account-level public access must be enabled before container-level public access works.

---

## Related Concepts

- [Data Types Overview](00-DataTypes.md)
- [Azure Storage Accounts](01-StorageAccounts.md)
- [Storage Services Overview](03-StorageServices.md)
- [Real-World Use Cases](04-UseCases.md)
