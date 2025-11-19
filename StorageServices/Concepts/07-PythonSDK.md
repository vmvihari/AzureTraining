# Python SDK for Azure Storage

## Overview

The Azure Storage Python SDK provides a comprehensive set of libraries for interacting with Azure Storage services programmatically. This guide covers installation, configuration, and practical usage for Blob Storage and Table Storage operations.

## Prerequisites

### Installing Python

**Windows**:
```powershell
# Option 1: Download from python.org
# Visit https://www.python.org/downloads/

# Option 2: Using winget (Windows Package Manager)
winget install Python.Python.3.12

# Option 3: Using Microsoft Store
# Search for "Python 3.12" in Microsoft Store
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**macOS**:
```bash
# Using Homebrew
brew install python3
```

**Verify Installation**:
```bash
python --version
# Output: Python 3.12.x

# Or on some systems:
python3 --version
```

---

### Understanding pip

**What is pip?**: Python's package manager, similar to:
- `apt` for Ubuntu/Debian
- `npm` for Node.js
- `NuGet` for .NET
- `Maven` for Java

**Verify pip Installation**:
```bash
pip --version
# Output: pip 24.x from ...

# Or on some systems:
pip3 --version
```

> [!NOTE]
> pip is automatically installed with Python 3.4 and later versions.

**Basic pip Commands**:
```bash
# Install a package
pip install package-name

# Install specific version
pip install package-name==1.2.3

# Upgrade a package
pip install --upgrade package-name

# Uninstall a package
pip uninstall package-name

# List installed packages
pip list

# Show package details
pip show package-name

# Save installed packages to file
pip freeze > requirements.txt

# Install from requirements file
pip install -r requirements.txt
```

---

## Installing Azure Storage Packages

### Azure Data Tables

**Installation**:
```bash
pip install azure-data-tables
```

**Verify Installation**:
```bash
pip show azure-data-tables
```

**What it provides**:
- `TableServiceClient` - Manage tables in a storage account
- `TableClient` - Perform CRUD operations on table entities
- Entity operations (create, read, update, delete)
- Query capabilities
- Batch operations

---

### Azure Storage Blob

**Installation**:
```bash
pip install azure-storage-blob
```

**Verify Installation**:
```bash
pip show azure-storage-blob
```

**What it provides**:
- `BlobServiceClient` - Manage containers and blobs
- `ContainerClient` - Container-level operations
- `BlobClient` - Individual blob operations
- Upload/download capabilities
- Blob metadata and properties

---

### Azure Identity (for Authentication)

**Installation**:
```bash
pip install azure-identity
```

**What it provides**:
- `DefaultAzureCredential` - Automatic credential detection
- `ManagedIdentityCredential` - For Azure resources
- `ClientSecretCredential` - Service principal authentication
- `InteractiveBrowserCredential` - Interactive login

---

### Install All at Once

**Create requirements.txt**:
```text
azure-data-tables>=12.4.0
azure-storage-blob>=12.19.0
azure-identity>=1.15.0
python-dotenv>=1.0.0
```

**Install**:
```bash
pip install -r requirements.txt
```

---

## Authentication Methods

### Method 1: Connection String

**Pros**:
- ✅ Simple to use
- ✅ Full access to storage account
- ✅ Works from anywhere

**Cons**:
- ⚠️ Requires secure storage
- ⚠️ Full access (cannot be scoped)
- ⚠️ Difficult to rotate

**Where to Find**:
1. Azure Portal → Storage Account
2. **Access keys** section
3. Copy **Connection string**

**Format**:
```
DefaultEndpointsProtocol=https;
AccountName=mystorageacct;
AccountKey=abc123...;
EndpointSuffix=core.windows.net
```

**Usage**:
```python
from azure.data.tables import TableServiceClient
from azure.storage.blob import BlobServiceClient

# For Tables
table_service = TableServiceClient.from_connection_string(
    conn_str="DefaultEndpointsProtocol=https;AccountName=..."
)

# For Blobs
blob_service = BlobServiceClient.from_connection_string(
    conn_str="DefaultEndpointsProtocol=https;AccountName=..."
)
```

**Best Practice - Use Environment Variables**:
```python
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
table_service = TableServiceClient.from_connection_string(connection_string)
```

**.env file**:
```
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=mystorageacct;AccountKey=...
```

> [!WARNING]
> Never commit connection strings to source control. Always use environment variables or Azure Key Vault.

---

### Method 2: Account Key

**Usage**:
```python
from azure.data.tables import TableServiceClient
from azure.storage.blob import BlobServiceClient

account_name = "mystorageacct"
account_key = "abc123..."

# For Tables
table_service = TableServiceClient(
    endpoint=f"https://{account_name}.table.core.windows.net",
    credential=account_key
)

# For Blobs
blob_service = BlobServiceClient(
    account_url=f"https://{account_name}.blob.core.windows.net",
    credential=account_key
)
```

---

### Method 3: SAS Token

**Pros**:
- ✅ Granular permissions (read, write, delete, list)
- ✅ Time-limited access
- ✅ IP address restrictions
- ✅ Can be revoked
- ✅ Safer for client applications

**Cons**:
- ⚠️ Requires management and renewal
- ⚠️ More complex to generate

**Usage**:
```python
from azure.data.tables import TableClient
from azure.storage.blob import BlobClient

account_name = "mystorageacct"
sas_token = "sv=2021-06-08&ss=t&srt=sco&sp=rwdlacu&se=..."

# For Tables
table_client = TableClient(
    endpoint=f"https://{account_name}.table.core.windows.net",
    table_name="mytable",
    credential=sas_token
)

# For Blobs
blob_client = BlobClient(
    account_url=f"https://{account_name}.blob.core.windows.net",
    container_name="mycontainer",
    blob_name="myblob.txt",
    credential=sas_token
)
```

**Generate SAS Token Programmatically**:
```python
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

sas_token = generate_blob_sas(
    account_name="mystorageacct",
    container_name="mycontainer",
    blob_name="myblob.txt",
    account_key="abc123...",
    permission=BlobSasPermissions(read=True, write=True),
    expiry=datetime.utcnow() + timedelta(hours=1)
)

print(f"SAS Token: {sas_token}")
```

---

### Method 4: Managed Identity (Recommended for Azure Resources)

**Pros**:
- ✅ No credentials to manage
- ✅ Azure AD-based authentication
- ✅ Automatic credential rotation
- ✅ Most secure option

**Cons**:
- ⚠️ Only works for Azure resources (VMs, Functions, App Service, etc.)

**Usage**:
```python
from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient
from azure.storage.blob import BlobServiceClient

# Automatically uses managed identity when running on Azure
credential = DefaultAzureCredential()

# For Tables
table_service = TableServiceClient(
    endpoint="https://mystorageacct.table.core.windows.net",
    credential=credential
)

# For Blobs
blob_service = BlobServiceClient(
    account_url="https://mystorageacct.blob.core.windows.net",
    credential=credential
)
```

**Required Azure RBAC Roles**:
- `Storage Blob Data Contributor` - For blob operations
- `Storage Table Data Contributor` - For table operations

---

## Working with Azure Tables

### TableServiceClient

**Purpose**: Manage tables in a storage account

**Common Operations**:
```python
from azure.data.tables import TableServiceClient

# Connect
service_client = TableServiceClient.from_connection_string(conn_str)

# Create table
service_client.create_table("products")

# Create table if not exists
service_client.create_table_if_not_exists("products")

# List tables
tables = service_client.list_tables()
for table in tables:
    print(f"Table: {table.name}")

# Delete table
service_client.delete_table("products")

# Get table client
table_client = service_client.get_table_client("products")
```

---

### TableClient

**Purpose**: Perform CRUD operations on table entities

**Create Entity**:
```python
from azure.data.tables import TableClient

table_client = TableClient.from_connection_string(
    conn_str=connection_string,
    table_name="products"
)

# Create entity
entity = {
    "PartitionKey": "Electronics",
    "RowKey": "PROD-001",
    "Name": "Laptop",
    "Price": 999.99,
    "InStock": True
}

table_client.create_entity(entity=entity)
print("Entity created!")
```

**Read Entity**:
```python
# Get single entity
entity = table_client.get_entity(
    partition_key="Electronics",
    row_key="PROD-001"
)

print(f"Product: {entity['Name']}")
print(f"Price: ${entity['Price']}")
```

**Query Entities**:
```python
# Query all entities in partition
entities = table_client.query_entities(
    query_filter="PartitionKey eq 'Electronics'"
)

for entity in entities:
    print(f"{entity['Name']}: ${entity['Price']}")

# Query with multiple filters
query = "PartitionKey eq 'Electronics' and Price lt 1000"
entities = table_client.query_entities(query_filter=query)

# Select specific properties
entities = table_client.query_entities(
    query_filter="PartitionKey eq 'Electronics'",
    select=["Name", "Price"]
)
```

**Update Entity**:
```python
# Get entity
entity = table_client.get_entity("Electronics", "PROD-001")

# Modify
entity["Price"] = 899.99
entity["LastUpdated"] = "2024-01-15"

# Update (replace mode - overwrites all properties)
table_client.update_entity(entity=entity, mode="replace")

# Update (merge mode - updates only specified properties)
table_client.update_entity(entity=entity, mode="merge")
```

**Delete Entity**:
```python
table_client.delete_entity(
    partition_key="Electronics",
    row_key="PROD-001"
)
```

---

### Complete Example: Product Catalog

```python
from azure.data.tables import TableServiceClient
import os

# Configuration
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
table_name = "products"

# Connect and create table
service_client = TableServiceClient.from_connection_string(connection_string)
service_client.create_table_if_not_exists(table_name)
table_client = service_client.get_table_client(table_name)

# Insert products
products = [
    {
        "PartitionKey": "Electronics",
        "RowKey": "PROD-001",
        "Name": "Laptop",
        "Price": 999.99,
        "InStock": True
    },
    {
        "PartitionKey": "Electronics",
        "RowKey": "PROD-002",
        "Name": "Mouse",
        "Price": 29.99,
        "InStock": True
    },
    {
        "PartitionKey": "Books",
        "RowKey": "PROD-003",
        "Name": "Python Programming",
        "Price": 49.99,
        "InStock": False
    }
]

for product in products:
    table_client.create_entity(entity=product)
    print(f"Added: {product['Name']}")

# Query electronics
print("\nElectronics in stock:")
query = "PartitionKey eq 'Electronics' and InStock eq true"
electronics = table_client.query_entities(query_filter=query)

for item in electronics:
    print(f"- {item['Name']}: ${item['Price']}")
```

---

## Working with Blob Storage

### BlobServiceClient

**Purpose**: Manage containers and blobs in a storage account

**Common Operations**:
```python
from azure.storage.blob import BlobServiceClient

# Connect
blob_service = BlobServiceClient.from_connection_string(conn_str)

# Create container
blob_service.create_container("images")

# List containers
containers = blob_service.list_containers()
for container in containers:
    print(f"Container: {container.name}")

# Delete container
blob_service.delete_container("images")

# Get container client
container_client = blob_service.get_container_client("images")

# Get blob client
blob_client = blob_service.get_blob_client(
    container="images",
    blob="photo.jpg"
)
```

---

### ContainerClient

**Purpose**: Container-level operations

**Common Operations**:
```python
from azure.storage.blob import ContainerClient

# Connect to container
container_client = ContainerClient.from_connection_string(
    conn_str=connection_string,
    container_name="images"
)

# Upload blob
with open("photo.jpg", "rb") as data:
    container_client.upload_blob(
        name="photo.jpg",
        data=data,
        overwrite=True
    )

# List blobs
blobs = container_client.list_blobs()
for blob in blobs:
    print(f"Blob: {blob.name} ({blob.size} bytes)")

# Delete blob
container_client.delete_blob("photo.jpg")
```

---

### BlobClient

**Purpose**: Individual blob operations

**Upload Blob**:
```python
from azure.storage.blob import BlobClient

blob_client = BlobClient.from_connection_string(
    conn_str=connection_string,
    container_name="images",
    blob_name="photo.jpg"
)

# Upload from file
with open("photo.jpg", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

# Upload from string
text_data = "Hello, Azure Storage!"
blob_client.upload_blob(text_data, overwrite=True)
```

**Download Blob**:
```python
# Download to file
with open("downloaded_photo.jpg", "wb") as file:
    download_stream = blob_client.download_blob()
    file.write(download_stream.readall())

# Download to memory
download_stream = blob_client.download_blob()
content = download_stream.readall()
print(f"Downloaded {len(content)} bytes")
```

**Blob Properties and Metadata**:
```python
# Get properties
properties = blob_client.get_blob_properties()
print(f"Size: {properties.size} bytes")
print(f"Content Type: {properties.content_settings.content_type}")
print(f"Last Modified: {properties.last_modified}")

# Set metadata
metadata = {
    "uploaded_by": "admin",
    "category": "photos",
    "year": "2024"
}
blob_client.set_blob_metadata(metadata)

# Get metadata
properties = blob_client.get_blob_properties()
print(f"Metadata: {properties.metadata}")
```

---

### Complete Example: Image Upload and Processing

```python
from azure.storage.blob import BlobServiceClient
from PIL import Image
import io
import os

# Configuration
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service = BlobServiceClient.from_connection_string(connection_string)

# Create containers
blob_service.create_container("uploads")
blob_service.create_container("thumbnails")

# Upload original image
upload_container = blob_service.get_container_client("uploads")
with open("photo.jpg", "rb") as data:
    upload_container.upload_blob("photo.jpg", data, overwrite=True)
print("Original image uploaded")

# Download and create thumbnail
blob_client = blob_service.get_blob_client("uploads", "photo.jpg")
image_data = blob_client.download_blob().readall()

# Create thumbnail
image = Image.open(io.BytesIO(image_data))
image.thumbnail((200, 200))

# Save thumbnail
thumbnail_io = io.BytesIO()
image.save(thumbnail_io, format='JPEG')
thumbnail_io.seek(0)

# Upload thumbnail
thumbnail_container = blob_service.get_container_client("thumbnails")
thumbnail_container.upload_blob(
    "photo_thumb.jpg",
    thumbnail_io,
    overwrite=True
)
print("Thumbnail created and uploaded")
```

---

## Error Handling

### Common Exceptions

```python
from azure.core.exceptions import (
    ResourceExistsError,
    ResourceNotFoundError,
    HttpResponseError
)

try:
    # Create entity
    table_client.create_entity(entity)
except ResourceExistsError:
    print("Entity already exists")
except HttpResponseError as e:
    print(f"HTTP error: {e.status_code} - {e.message}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Best Practices

```python
import logging
from azure.core.exceptions import AzureError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_create_entity(table_client, entity):
    """Safely create entity with error handling"""
    try:
        table_client.create_entity(entity)
        logger.info(f"Created entity: {entity['RowKey']}")
        return True
    except ResourceExistsError:
        logger.warning(f"Entity already exists: {entity['RowKey']}")
        return False
    except AzureError as e:
        logger.error(f"Azure error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False
```

---

## Summary

The Azure Storage Python SDK provides powerful tools for programmatic access to Azure Storage services. Key takeaways:

1. **Installation**: Use `pip install azure-data-tables azure-storage-blob azure-identity`
2. **Authentication**: Connection strings for development, managed identities for production
3. **Tables**: Use `TableServiceClient` and `TableClient` for NoSQL operations
4. **Blobs**: Use `BlobServiceClient`, `ContainerClient`, and `BlobClient` for file storage
5. **Security**: Never commit credentials, use environment variables or Key Vault

**Best Practices**:
- ✅ Use managed identities when running on Azure
- ✅ Store credentials in environment variables or Key Vault
- ✅ Implement proper error handling
- ✅ Use SAS tokens for client applications
- ✅ Enable logging for debugging

---

## Related Concepts

- [Azure Storage Accounts](01-StorageAccounts.md)
- [Azure Tables](05-AzureTables.md)
- [Blob Containers and Access Levels](02-BlobContainers.md)
- [Static Website Hosting](06-StaticWebsiteHosting.md)
- [Real-World Use Cases](04-UseCases.md)

## Hands-On Practice

- [Assignment 1: Azure File Shares](../Assignments/Assignment01-AzureFileShares.md) - Learn to create and mount file shares
- [Assignment 2: Add Disk to VM](../Assignments/Assignment02-AddDiskToVM.md) - Add additional storage to VMs
- [Assignment 3: Extend Disk Storage](../Assignments/Assignment03-ExtendDiskStorage.md) - Expand existing disks
