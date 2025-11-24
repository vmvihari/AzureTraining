# .NET SDK for Azure Storage

## Overview

The Azure Storage .NET SDK provides a comprehensive set of libraries for interacting with Azure Storage services programmatically. This guide covers installation, configuration, and practical usage for Blob Storage and Table Storage operations using modern .NET and C#.

## Prerequisites

### Installing .NET SDK

**Windows**:
```powershell
# Option 1: Download from Microsoft
# Visit https://dotnet.microsoft.com/download

# Option 2: Using winget (Windows Package Manager)
winget install Microsoft.DotNet.SDK.8

# Option 3: Using Chocolatey
choco install dotnet-sdk
```

**Linux (Ubuntu/Debian)**:
```bash
# Add Microsoft package repository
wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

# Install .NET SDK
sudo apt-get update
sudo apt-get install -y dotnet-sdk-8.0
```

**macOS**:
```bash
# Using Homebrew
brew install --cask dotnet-sdk
```

**Verify Installation**:
```bash
dotnet --version
# Output: 8.0.x
```

---

### Understanding NuGet

**What is NuGet?**: .NET's package manager, similar to:
- `pip` for Python
- `npm` for Node.js
- `apt` for Ubuntu/Debian
- `Maven` for Java

**Verify NuGet**:
```bash
dotnet nuget --version
```

> [!NOTE]
> NuGet is automatically included with the .NET SDK.

**Basic NuGet Commands**:
```bash
# Add a package to project
dotnet add package PackageName

# Add specific version
dotnet add package PackageName --version 1.2.3

# Remove a package
dotnet remove package PackageName

# List installed packages
dotnet list package

# Restore packages
dotnet restore

# Update packages
dotnet add package PackageName --version <new-version>
```

---

## Installing Azure Storage Packages

### Azure.Data.Tables

**Installation**:
```bash
dotnet add package Azure.Data.Tables
```

**Verify Installation**:
```bash
dotnet list package | findstr Azure.Data.Tables
```

**What it provides**:
- `TableServiceClient` - Manage tables in a storage account
- `TableClient` - Perform CRUD operations on table entities
- Entity operations (create, read, update, delete)
- Query capabilities
- Batch operations

---

### Azure.Storage.Blobs

**Installation**:
```bash
dotnet add package Azure.Storage.Blobs
```

**Verify Installation**:
```bash
dotnet list package | findstr Azure.Storage.Blobs
```

**What it provides**:
- `BlobServiceClient` - Manage containers and blobs
- `BlobContainerClient` - Container-level operations
- `BlobClient` - Individual blob operations
- Upload/download capabilities
- Blob metadata and properties

---

### Azure.Identity (for Authentication)

**Installation**:
```bash
dotnet add package Azure.Identity
```

**What it provides**:
- `DefaultAzureCredential` - Automatic credential detection
- `ManagedIdentityCredential` - For Azure resources
- `ClientSecretCredential` - Service principal authentication
- `InteractiveBrowserCredential` - Interactive login

---

### Install All at Once

**Create a new console project**:
```bash
dotnet new console -n AzureStorageDemo
cd AzureStorageDemo
```

**Add all packages**:
```bash
dotnet add package Azure.Data.Tables
dotnet add package Azure.Storage.Blobs
dotnet add package Azure.Identity
```

**Or edit .csproj file**:
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Azure.Data.Tables" Version="12.8.3" />
    <PackageReference Include="Azure.Storage.Blobs" Version="12.19.1" />
    <PackageReference Include="Azure.Identity" Version="1.10.4" />
  </ItemGroup>
</Project>
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
```csharp
using Azure.Data.Tables;
using Azure.Storage.Blobs;

// For Tables
var tableServiceClient = new TableServiceClient(
    "DefaultEndpointsProtocol=https;AccountName=mystorageacct;AccountKey=..."
);

// For Blobs
var blobServiceClient = new BlobServiceClient(
    "DefaultEndpointsProtocol=https;AccountName=mystorageacct;AccountKey=..."
);
```

**Best Practice - Use Environment Variables**:
```csharp
using System;

// Read from environment variable
var connectionString = Environment.GetEnvironmentVariable("AZURE_STORAGE_CONNECTION_STRING");
var tableServiceClient = new TableServiceClient(connectionString);
```

**Set Environment Variable**:

Windows (PowerShell):
```powershell
$env:AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=mystorageacct;AccountKey=..."
```

Linux/macOS:
```bash
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=mystorageacct;AccountKey=..."
```

**Using appsettings.json** (ASP.NET Core):
```json
{
  "AzureStorage": {
    "ConnectionString": "DefaultEndpointsProtocol=https;AccountName=mystorageacct;AccountKey=..."
  }
}
```

```csharp
using Microsoft.Extensions.Configuration;

var configuration = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json")
    .Build();

var connectionString = configuration["AzureStorage:ConnectionString"];
var tableServiceClient = new TableServiceClient(connectionString);
```

> [!WARNING]
> Never commit connection strings to source control. Always use environment variables, Azure Key Vault, or user secrets.

---

### Method 2: Account Key

**Usage**:
```csharp
using Azure.Data.Tables;
using Azure.Storage.Blobs;
using Azure.Storage;

var accountName = "mystorageacct";
var accountKey = "abc123...";

// Create credential
var credential = new StorageSharedKeyCredential(accountName, accountKey);

// For Tables
var tableServiceClient = new TableServiceClient(
    new Uri($"https://{accountName}.table.core.windows.net"),
    credential
);

// For Blobs
var blobServiceClient = new BlobServiceClient(
    new Uri($"https://{accountName}.blob.core.windows.net"),
    credential
);
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
```csharp
using Azure.Data.Tables;
using Azure.Storage.Blobs;
using Azure.Storage.Sas;

var accountName = "mystorageacct";
var sasToken = "sv=2021-06-08&ss=t&srt=sco&sp=rwdlacu&se=...";

// For Tables
var tableClient = new TableClient(
    new Uri($"https://{accountName}.table.core.windows.net/mytable?{sasToken}")
);

// For Blobs
var blobClient = new BlobClient(
    new Uri($"https://{accountName}.blob.core.windows.net/mycontainer/myblob.txt?{sasToken}")
);
```

**Generate SAS Token Programmatically**:
```csharp
using Azure.Storage.Blobs;
using Azure.Storage.Sas;

var blobClient = new BlobClient(
    new Uri("https://mystorageacct.blob.core.windows.net/mycontainer/myblob.txt"),
    new StorageSharedKeyCredential("mystorageacct", "account-key")
);

var sasBuilder = new BlobSasBuilder
{
    BlobContainerName = "mycontainer",
    BlobName = "myblob.txt",
    Resource = "b",
    StartsOn = DateTimeOffset.UtcNow,
    ExpiresOn = DateTimeOffset.UtcNow.AddHours(1)
};

sasBuilder.SetPermissions(BlobSasPermissions.Read | BlobSasPermissions.Write);

var sasUri = blobClient.GenerateSasUri(sasBuilder);
Console.WriteLine($"SAS URI: {sasUri}");
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
```csharp
using Azure.Identity;
using Azure.Data.Tables;
using Azure.Storage.Blobs;

// Automatically uses managed identity when running on Azure
var credential = new DefaultAzureCredential();

// For Tables
var tableServiceClient = new TableServiceClient(
    new Uri("https://mystorageacct.table.core.windows.net"),
    credential
);

// For Blobs
var blobServiceClient = new BlobServiceClient(
    new Uri("https://mystorageacct.blob.core.windows.net"),
    credential
);
```

**Required Azure RBAC Roles**:
- `Storage Blob Data Contributor` - For blob operations
- `Storage Table Data Contributor` - For table operations

---

## Working with Azure Tables

### TableServiceClient

**Purpose**: Manage tables in a storage account

**Common Operations**:
```csharp
using Azure.Data.Tables;

// Connect
var serviceClient = new TableServiceClient(connectionString);

// Create table
await serviceClient.CreateTableAsync("products");

// Create table if not exists
await serviceClient.CreateTableIfNotExistsAsync("products");

// List tables
await foreach (var table in serviceClient.QueryAsync())
{
    Console.WriteLine($"Table: {table.Name}");
}

// Delete table
await serviceClient.DeleteTableAsync("products");

// Get table client
var tableClient = serviceClient.GetTableClient("products");
```

---

### TableClient

**Purpose**: Perform CRUD operations on table entities

**Define Entity Class**:
```csharp
using Azure;
using Azure.Data.Tables;

public class ProductEntity : ITableEntity
{
    public string PartitionKey { get; set; } = default!;
    public string RowKey { get; set; } = default!;
    public DateTimeOffset? Timestamp { get; set; }
    public ETag ETag { get; set; }
    
    // Custom properties
    public string Name { get; set; } = default!;
    public double Price { get; set; }
    public bool InStock { get; set; }
}
```

**Create Entity**:
```csharp
using Azure.Data.Tables;

var tableClient = new TableClient(connectionString, "products");

// Create entity
var entity = new ProductEntity
{
    PartitionKey = "Electronics",
    RowKey = "PROD-001",
    Name = "Laptop",
    Price = 999.99,
    InStock = true
};

await tableClient.AddEntityAsync(entity);
Console.WriteLine("Entity created!");
```

**Read Entity**:
```csharp
// Get single entity
var entity = await tableClient.GetEntityAsync<ProductEntity>(
    partitionKey: "Electronics",
    rowKey: "PROD-001"
);

Console.WriteLine($"Product: {entity.Value.Name}");
Console.WriteLine($"Price: ${entity.Value.Price}");
```

**Query Entities**:
```csharp
// Query all entities in partition
var entities = tableClient.QueryAsync<ProductEntity>(
    filter: $"PartitionKey eq 'Electronics'"
);

await foreach (var entity in entities)
{
    Console.WriteLine($"{entity.Name}: ${entity.Price}");
}

// Query with multiple filters
var query = $"PartitionKey eq 'Electronics' and Price lt 1000";
var filteredEntities = tableClient.QueryAsync<ProductEntity>(filter: query);

// Select specific properties
var selectedEntities = tableClient.QueryAsync<ProductEntity>(
    filter: $"PartitionKey eq 'Electronics'",
    select: new[] { "Name", "Price" }
);
```

**Update Entity**:
```csharp
// Get entity
var response = await tableClient.GetEntityAsync<ProductEntity>("Electronics", "PROD-001");
var entity = response.Value;

// Modify
entity.Price = 899.99;

// Update (replace mode - overwrites all properties)
await tableClient.UpdateEntityAsync(entity, entity.ETag, TableUpdateMode.Replace);

// Update (merge mode - updates only specified properties)
await tableClient.UpdateEntityAsync(entity, entity.ETag, TableUpdateMode.Merge);
```

**Delete Entity**:
```csharp
await tableClient.DeleteEntityAsync(
    partitionKey: "Electronics",
    rowKey: "PROD-001"
);
```

---

### Complete Example: Product Catalog

```csharp
using Azure.Data.Tables;
using System;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        // Configuration
        var connectionString = Environment.GetEnvironmentVariable("AZURE_STORAGE_CONNECTION_STRING");
        var tableName = "products";

        // Connect and create table
        var serviceClient = new TableServiceClient(connectionString);
        await serviceClient.CreateTableIfNotExistsAsync(tableName);
        var tableClient = serviceClient.GetTableClient(tableName);

        // Insert products
        var products = new[]
        {
            new ProductEntity
            {
                PartitionKey = "Electronics",
                RowKey = "PROD-001",
                Name = "Laptop",
                Price = 999.99,
                InStock = true
            },
            new ProductEntity
            {
                PartitionKey = "Electronics",
                RowKey = "PROD-002",
                Name = "Mouse",
                Price = 29.99,
                InStock = true
            },
            new ProductEntity
            {
                PartitionKey = "Books",
                RowKey = "PROD-003",
                Name = "C# Programming",
                Price = 49.99,
                InStock = false
            }
        };

        foreach (var product in products)
        {
            await tableClient.AddEntityAsync(product);
            Console.WriteLine($"Added: {product.Name}");
        }

        // Query electronics
        Console.WriteLine("\nElectronics in stock:");
        var query = $"PartitionKey eq 'Electronics' and InStock eq true";
        var electronics = tableClient.QueryAsync<ProductEntity>(filter: query);

        await foreach (var item in electronics)
        {
            Console.WriteLine($"- {item.Name}: ${item.Price}");
        }
    }
}
```

---

## Working with Blob Storage

### BlobServiceClient

**Purpose**: Manage containers and blobs in a storage account

**Common Operations**:
```csharp
using Azure.Storage.Blobs;

// Connect
var blobServiceClient = new BlobServiceClient(connectionString);

// Create container
await blobServiceClient.CreateBlobContainerAsync("images");

// List containers
await foreach (var container in blobServiceClient.GetBlobContainersAsync())
{
    Console.WriteLine($"Container: {container.Name}");
}

// Delete container
await blobServiceClient.DeleteBlobContainerAsync("images");

// Get container client
var containerClient = blobServiceClient.GetBlobContainerClient("images");

// Get blob client
var blobClient = blobServiceClient.GetBlobClient(
    blobContainerName: "images",
    blobName: "photo.jpg"
);
```

---

### BlobContainerClient

**Purpose**: Container-level operations

**Common Operations**:
```csharp
using Azure.Storage.Blobs;

// Connect to container
var containerClient = new BlobContainerClient(connectionString, "images");

// Upload blob
using (var fileStream = File.OpenRead("photo.jpg"))
{
    await containerClient.UploadBlobAsync("photo.jpg", fileStream);
}

// List blobs
await foreach (var blob in containerClient.GetBlobsAsync())
{
    Console.WriteLine($"Blob: {blob.Name} ({blob.Properties.ContentLength} bytes)");
}

// Delete blob
await containerClient.DeleteBlobAsync("photo.jpg");
```

---

### BlobClient

**Purpose**: Individual blob operations

**Upload Blob**:
```csharp
using Azure.Storage.Blobs;

var blobClient = new BlobClient(connectionString, "images", "photo.jpg");

// Upload from file
using (var fileStream = File.OpenRead("photo.jpg"))
{
    await blobClient.UploadAsync(fileStream, overwrite: true);
}

// Upload from string
var textData = "Hello, Azure Storage!";
using (var stream = new MemoryStream(Encoding.UTF8.GetBytes(textData)))
{
    await blobClient.UploadAsync(stream, overwrite: true);
}
```

**Download Blob**:
```csharp
// Download to file
using (var fileStream = File.OpenWrite("downloaded_photo.jpg"))
{
    await blobClient.DownloadToAsync(fileStream);
}

// Download to memory
var downloadInfo = await blobClient.DownloadContentAsync();
var content = downloadInfo.Value.Content.ToArray();
Console.WriteLine($"Downloaded {content.Length} bytes");
```

**Blob Properties and Metadata**:
```csharp
// Get properties
var properties = await blobClient.GetPropertiesAsync();
Console.WriteLine($"Size: {properties.Value.ContentLength} bytes");
Console.WriteLine($"Content Type: {properties.Value.ContentType}");
Console.WriteLine($"Last Modified: {properties.Value.LastModified}");

// Set metadata
var metadata = new Dictionary<string, string>
{
    { "uploaded_by", "admin" },
    { "category", "photos" },
    { "year", "2024" }
};
await blobClient.SetMetadataAsync(metadata);

// Get metadata
properties = await blobClient.GetPropertiesAsync();
foreach (var kvp in properties.Value.Metadata)
{
    Console.WriteLine($"{kvp.Key}: {kvp.Value}");
}
```

---

### Complete Example: Image Upload and Processing

```csharp
using Azure.Storage.Blobs;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Processing;
using System;
using System.IO;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        // Configuration
        var connectionString = Environment.GetEnvironmentVariable("AZURE_STORAGE_CONNECTION_STRING");
        var blobServiceClient = new BlobServiceClient(connectionString);

        // Create containers
        await blobServiceClient.CreateBlobContainerAsync("uploads");
        await blobServiceClient.CreateBlobContainerAsync("thumbnails");

        // Upload original image
        var uploadContainer = blobServiceClient.GetBlobContainerClient("uploads");
        using (var fileStream = File.OpenRead("photo.jpg"))
        {
            await uploadContainer.UploadBlobAsync("photo.jpg", fileStream);
        }
        Console.WriteLine("Original image uploaded");

        // Download and create thumbnail
        var blobClient = blobServiceClient.GetBlobClient("uploads", "photo.jpg");
        var downloadInfo = await blobClient.DownloadContentAsync();
        var imageData = downloadInfo.Value.Content.ToArray();

        // Create thumbnail using ImageSharp
        using (var image = Image.Load(imageData))
        {
            image.Mutate(x => x.Resize(200, 200));

            using (var thumbnailStream = new MemoryStream())
            {
                await image.SaveAsJpegAsync(thumbnailStream);
                thumbnailStream.Position = 0;

                // Upload thumbnail
                var thumbnailContainer = blobServiceClient.GetBlobContainerClient("thumbnails");
                await thumbnailContainer.UploadBlobAsync("photo_thumb.jpg", thumbnailStream);
            }
        }
        Console.WriteLine("Thumbnail created and uploaded");
    }
}
```

> [!NOTE]
> The above example requires the `SixLabors.ImageSharp` NuGet package: `dotnet add package SixLabors.ImageSharp`

---

## Error Handling

### Common Exceptions

```csharp
using Azure;
using Azure.Data.Tables;

try
{
    // Create entity
    await tableClient.AddEntityAsync(entity);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Entity already exists");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Azure error: {ex.Status} - {ex.Message}");
}
catch (Exception ex)
{
    Console.WriteLine($"Unexpected error: {ex.Message}");
}
```

### Best Practices

```csharp
using Azure;
using Azure.Data.Tables;
using Microsoft.Extensions.Logging;

public class TableService
{
    private readonly TableClient _tableClient;
    private readonly ILogger<TableService> _logger;

    public TableService(TableClient tableClient, ILogger<TableService> logger)
    {
        _tableClient = tableClient;
        _logger = logger;
    }

    public async Task<bool> SafeCreateEntityAsync<T>(T entity) where T : class, ITableEntity
    {
        try
        {
            await _tableClient.AddEntityAsync(entity);
            _logger.LogInformation("Created entity: {RowKey}", entity.RowKey);
            return true;
        }
        catch (RequestFailedException ex) when (ex.Status == 409)
        {
            _logger.LogWarning("Entity already exists: {RowKey}", entity.RowKey);
            return false;
        }
        catch (RequestFailedException ex)
        {
            _logger.LogError(ex, "Azure error occurred");
            return false;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error occurred");
            return false;
        }
    }
}
```

---

## Summary

The Azure Storage .NET SDK provides powerful tools for programmatic access to Azure Storage services. Key takeaways:

1. **Installation**: Use `dotnet add package Azure.Data.Tables Azure.Storage.Blobs Azure.Identity`
2. **Authentication**: Connection strings for development, managed identities for production
3. **Tables**: Use `TableServiceClient` and `TableClient` for NoSQL operations
4. **Blobs**: Use `BlobServiceClient`, `BlobContainerClient`, and `BlobClient` for file storage
5. **Security**: Never commit credentials, use environment variables or Azure Key Vault

**Best Practices**:
- ✅ Use managed identities when running on Azure
- ✅ Store credentials in environment variables, appsettings.json, or Key Vault
- ✅ Implement proper error handling with try-catch blocks
- ✅ Use SAS tokens for client applications
- ✅ Enable logging for debugging
- ✅ Use async/await for all I/O operations
- ✅ Dispose of clients properly (use `using` statements or dependency injection)

---

## Related Concepts

- [Azure Storage Accounts](01-StorageAccounts.md)
- [Azure Tables](05-AzureTables.md)
- [Blob Containers and Access Levels](02-BlobContainers.md)
- [Static Website Hosting](06-StaticWebsiteHosting.md)
- [Python SDK Guide](07-PythonSDK.md)
- [Real-World Use Cases](04-UseCases.md)

## Hands-On Practice

- [Assignment 1: Azure File Shares](../Assignments/Assignment01-AzureFileShares.md) - Learn to create and mount file shares
- [Assignment 2: Add Disk to VM](../Assignments/Assignment02-AddDiskToVM.md) - Add additional storage to VMs
- [Assignment 3: Extend Disk Storage](../Assignments/Assignment03-ExtendDiskStorage.md) - Expand existing disks
