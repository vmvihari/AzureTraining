# Lab 01: Azure Blob Storage - Storage Accounts and Container Access Levels

## Lab Overview

**Duration**: 45-60 minutes  
**Difficulty**: Beginner  
**Prerequisites**: Active Azure subscription with contributor access

### Learning Objectives

By the end of this lab, you will be able to:
- Create and configure Azure Storage Accounts
- Understand different blob container access levels
- Upload and manage blobs in containers
- Validate and test anonymous access behavior
- Apply security best practices for blob storage

---

## Lab Scenario

You are a cloud engineer tasked with setting up blob storage for a web application. The application needs to store:
- **Private user data** (requires authentication)
- **Public product images** (accessible via direct URL but not browsable)
- **Public documentation** (fully accessible and browsable)

You need to configure appropriate storage containers with different access levels to meet these requirements.

---

## Exercise 1: Create Resource Group and Storage Account

### Task 1.1: Create a Resource Group

#### Using Azure Portal

1. Sign in to the [Azure Portal](https://portal.azure.com)
2. Click **"Resource groups"** from the left navigation menu
3. Click **"+ Create"**
4. Configure the resource group:
   - **Subscription**: Select your subscription
   - **Resource group name**: `rg-blobstorage-lab`
   - **Region**: `East US` (or your preferred region)
5. Click **"Review + create"**
6. Click **"Create"**

#### Using Azure CLI

```bash
# Login to Azure
az login

# Create resource group
az group create \
  --name rg-blobstorage-lab \
  --location eastus
```

### Task 1.2: Create a Storage Account

#### Using Azure Portal

1. In the Azure Portal, search for **"Storage accounts"**
2. Click **"+ Create"**
3. On the **Basics** tab:
   - **Subscription**: Select your subscription
   - **Resource group**: `rg-blobstorage-lab`
   - **Storage account name**: `stbloblab<yourname><date>` (e.g., `stbloblabmoni20231118`)
     - Must be globally unique
     - 3-24 characters, lowercase letters and numbers only
   - **Region**: `East US` (same as resource group)
   - **Performance**: **Standard**
   - **Redundancy**: **Locally-redundant storage (LRS)**
4. Click **"Next: Advanced"**
5. On the **Advanced** tab:
   - Verify **Access tier** is set to **Hot**
   - Leave other settings as default
6. Click **"Review + create"**
7. Review settings and click **"Create"**
8. Wait for deployment (1-2 minutes)
9. Click **"Go to resource"**

#### Using Azure CLI

```bash
# Set variables (customize as needed)
STORAGE_ACCOUNT="stbloblab$(date +%Y%m%d%H%M)"
RESOURCE_GROUP="rg-blobstorage-lab"
LOCATION="eastus"

# Create storage account
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS \
  --access-tier Hot \
  --kind StorageV2

# Display storage account details
az storage account show \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --output table
```

### Task 1.3: Document Storage Account Details

Create a document with the following information:

```
Storage Account Configuration
==============================
Storage account name: _______________________
Resource group name: rg-blobstorage-lab
Location: East US
Performance: Standard
Redundancy type: LRS (Locally-redundant storage)
Access tier: Hot
```

> [!TIP]
> Keep this information handy as you'll need it throughout the lab.

---

## Exercise 2: Configure Blob Containers with Different Access Levels

### Task 2.1: Enable Anonymous Blob Access

Before creating containers with public access, you must enable anonymous access at the storage account level.

#### Using Azure Portal

1. In your storage account, navigate to **Settings** → **Configuration**
2. Find **"Allow Blob public access"**
3. Toggle to **Enabled**
4. Click **Save** at the top

#### Using Azure CLI

```bash
# Enable blob public access
az storage account update \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --allow-blob-public-access true
```

> [!IMPORTANT]
> This setting is disabled by default for security. In production, only enable it if you have a legitimate need for public blob access.

### Task 2.2: Create Three Containers with Different Access Levels

#### Using Azure Portal

1. In your storage account, go to **Data storage** → **Containers**
2. Click **"+ Container"**

**Container 1: Private Access**
- **Name**: `private-container`
- **Public access level**: **Private (no anonymous access)**
- Click **Create**

**Container 2: Blob-Level Access**
- Click **"+ Container"** again
- **Name**: `blob-container`
- **Public access level**: **Blob (anonymous read access for blobs only)**
- Click **Create**

**Container 3: Container-Level Access**
- Click **"+ Container"** again
- **Name**: `container-access`
- **Public access level**: **Container (anonymous read access for containers and blobs)**
- Click **Create**

#### Using Azure CLI

```bash
# Create private-container
az storage container create \
  --name private-container \
  --account-name $STORAGE_ACCOUNT \
  --public-access off \
  --auth-mode login

# Create blob-container
az storage container create \
  --name blob-container \
  --account-name $STORAGE_ACCOUNT \
  --public-access blob \
  --auth-mode login

# Create container-access
az storage container create \
  --name container-access \
  --account-name $STORAGE_ACCOUNT \
  --public-access container \
  --auth-mode login

# List all containers
az storage container list \
  --account-name $STORAGE_ACCOUNT \
  --auth-mode login \
  --output table
```

---

## Exercise 3: Upload Files and Test Access Behavior

### Task 3.1: Create Sample Test Files

Create two simple text files on your local machine:

**test1.txt**
```
This is test file 1 for Azure Blob Storage Lab.
Container: [container-name]
```

**test2.txt**
```
This is test file 2 for Azure Blob Storage Lab.
Container: [container-name]
```

> [!TIP]
> You can use Notepad, VS Code, or any text editor to create these files.

### Task 3.2: Upload Files to Each Container

#### Using Azure Portal

**For each container (private-container, blob-container, container-access):**

1. Click on the container name
2. Click **"Upload"** at the top
3. Click **"Browse for files"**
4. Select both `test1.txt` and `test2.txt`
5. Click **"Upload"**
6. Wait for upload confirmation

#### Using Azure CLI

```bash
# Create test files (Windows PowerShell)
"This is test file 1 for Azure Blob Storage Lab." | Out-File -FilePath test1.txt -Encoding utf8
"This is test file 2 for Azure Blob Storage Lab." | Out-File -FilePath test2.txt -Encoding utf8

# Upload to private-container
az storage blob upload --account-name $STORAGE_ACCOUNT --container-name private-container --name test1.txt --file test1.txt --auth-mode login
az storage blob upload --account-name $STORAGE_ACCOUNT --container-name private-container --name test2.txt --file test2.txt --auth-mode login

# Upload to blob-container
az storage blob upload --account-name $STORAGE_ACCOUNT --container-name blob-container --name test1.txt --file test1.txt --auth-mode login
az storage blob upload --account-name $STORAGE_ACCOUNT --container-name blob-container --name test2.txt --file test2.txt --auth-mode login

# Upload to container-access
az storage blob upload --account-name $STORAGE_ACCOUNT --container-name container-access --name test1.txt --file test1.txt --auth-mode login
az storage blob upload --account-name $STORAGE_ACCOUNT --container-name container-access --name test2.txt --file test2.txt --auth-mode login
```

### Task 3.3: Collect Blob URLs

#### Using Azure Portal

**For each container:**

1. Click on the container name
2. Click on `test1.txt`
3. In the blob properties, find and copy the **URL**
4. Document the URL in your notes

#### Using Azure CLI

```bash
# Get URLs for all test files
echo "=== Private Container URLs ==="
az storage blob url --account-name $STORAGE_ACCOUNT --container-name private-container --name test1.txt --auth-mode login
az storage blob url --account-name $STORAGE_ACCOUNT --container-name private-container --name test2.txt --auth-mode login

echo "=== Blob Container URLs ==="
az storage blob url --account-name $STORAGE_ACCOUNT --container-name blob-container --name test1.txt --auth-mode login
az storage blob url --account-name $STORAGE_ACCOUNT --container-name blob-container --name test2.txt --auth-mode login

echo "=== Container Access URLs ==="
az storage blob url --account-name $STORAGE_ACCOUNT --container-name container-access --name test1.txt --auth-mode login
az storage blob url --account-name $STORAGE_ACCOUNT --container-name container-access --name test2.txt --auth-mode login
```

### Task 3.4: Test Anonymous Access

1. **Open a new private/incognito browser window** (to ensure no cached credentials)
2. **Test each blob URL** by pasting it into the browser
3. **Document the results** using the table below

#### Access Test Results Table

| Container Name | Access Level | Blob URL (test1.txt) | Result | HTTP Status |
|----------------|--------------|----------------------|--------|-------------|
| private-container | Private | `https://...` | ❌ Denied | 404 |
| blob-container | Blob | `https://...` | ✅ Accessible | 200 |
| container-access | Container | `https://...` | ✅ Accessible | 200 |

### Task 3.5: Test Container Listing Access

Test whether you can list all blobs in each container anonymously.

**Container Listing URL Format:**
```
https://[storageaccount].blob.core.windows.net/[container]?restype=container&comp=list
```

**Example:**
```
https://stbloblab20231118.blob.core.windows.net/container-access?restype=container&comp=list
```

Test this URL for each container in an incognito browser window.

#### Container Listing Results Table

| Container Name | Access Level | Listing URL | Can List Blobs? | Result |
|----------------|--------------|-------------|-----------------|--------|
| private-container | Private | `https://...?restype=container&comp=list` | ❌ No | Access Denied |
| blob-container | Blob | `https://...?restype=container&comp=list` | ❌ No | Access Denied |
| container-access | Container | `https://...?restype=container&comp=list` | ✅ Yes | XML blob list |

---

## Exercise 4: Understanding Access Levels

### Task 4.1: Analyze Access Behavior

Based on your testing, answer the following questions:

**Question 1:** What happens when you try to access a blob in `private-container` without authentication?

**Answer:** _______________________________________________________________________

**Question 2:** Can you list all blobs in `blob-container` without knowing the exact blob names?

**Answer:** _______________________________________________________________________

**Question 3:** What is the key difference between `blob-container` and `container-access`?

**Answer:** _______________________________________________________________________

**Question 4:** Which access level provides "security through obscurity"?

**Answer:** _______________________________________________________________________

### Task 4.2: Document Your Findings

Write a brief explanation (3-5 sentences) for each access level:

#### Private (No anonymous access)
```
Explanation:
_______________________________________________________________________
_______________________________________________________________________
_______________________________________________________________________
```

#### Blob (Anonymous read access for blobs only)
```
Explanation:
_______________________________________________________________________
_______________________________________________________________________
_______________________________________________________________________
```

#### Container (Anonymous read access for containers and blobs)
```
Explanation:
_______________________________________________________________________
_______________________________________________________________________
_______________________________________________________________________
```

---

## Exercise 5: Real-World Application Scenario

### Scenario Analysis

A website frequently receives high-resolution product images from vendors. These images are stored in Azure Blob Storage and must be optimized (compressed) by a nightly script before being used by the website.

Answer the following questions:

### Question 1: Container Access Type for Processing Script

**Which container access type is most appropriate for allowing a script to read all files at once for processing, and why?**

```
Answer:
_______________________________________________________________________
_______________________________________________________________________
_______________________________________________________________________
```

### Question 2: Storage Location for Optimized Images

**Where should the optimized images be stored?**

```
Answer:
_______________________________________________________________________
_______________________________________________________________________
_______________________________________________________________________
```

### Question 3: Benefits of Using Storage Account URLs

**Why should the website use the storage account URL instead of storing images locally on the web server?**

```
Answer:
_______________________________________________________________________
_______________________________________________________________________
_______________________________________________________________________
```

### Question 4: Blob Versioning Advantage

**Provide one advantage of enabling blob versioning in this scenario.**

```
Answer:
_______________________________________________________________________
_______________________________________________________________________
_______________________________________________________________________
```

---

## Lab Cleanup

> [!CAUTION]
> Leaving resources running will incur costs. Make sure to clean up when you're done with the lab.

### Option 1: Delete Resource Group (Recommended)

This will delete the storage account and all containers/blobs.

#### Using Azure Portal
1. Go to **Resource groups**
2. Click on `rg-blobstorage-lab`
3. Click **"Delete resource group"**
4. Type the resource group name to confirm
5. Click **Delete**

#### Using Azure CLI
```bash
az group delete --name rg-blobstorage-lab --yes --no-wait
```

### Option 2: Delete Individual Resources

If you want to keep the resource group but delete the storage account:

```bash
az storage account delete \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --yes
```

---

## Knowledge Check

Test your understanding with these questions:

1. **What is the default public access setting for new storage accounts?**
   - [ ] Enabled
   - [ ] Disabled
   - [ ] Blob-level only

2. **Which access level allows anonymous users to list all blobs in a container?**
   - [ ] Private
   - [ ] Blob
   - [ ] Container

3. **What is the maximum length for a storage account name?**
   - [ ] 12 characters
   - [ ] 24 characters
   - [ ] 64 characters

4. **Which redundancy option provides the lowest cost?**
   - [ ] LRS
   - [ ] GRS
   - [ ] RA-GRS

5. **Can you change a container's access level after creation?**
   - [ ] Yes
   - [ ] No
   - [ ] Only from private to public

<details>
<summary>Click to reveal answers</summary>

1. **Disabled** - For security, anonymous blob access is disabled by default
2. **Container** - Only container-level access allows listing blobs
3. **24 characters** - Storage account names must be 3-24 characters
4. **LRS** - Locally-redundant storage is the most cost-effective option
5. **Yes** - You can change access levels at any time via portal or CLI
</details>

---

## Additional Resources

- [Azure Blob Storage Documentation](https://docs.microsoft.com/en-us/azure/storage/blobs/)
- [Configure anonymous public read access for containers and blobs](https://docs.microsoft.com/en-us/azure/storage/blobs/anonymous-read-access-configure)
- [Azure Storage redundancy](https://docs.microsoft.com/en-us/azure/storage/common/storage-redundancy)
- [Blob storage pricing](https://azure.microsoft.com/en-us/pricing/details/storage/blobs/)

---

## Lab Summary

Congratulations! You have completed the Azure Blob Storage lab. You have learned how to:

✅ Create and configure Azure Storage Accounts  
✅ Create blob containers with different access levels  
✅ Upload and manage blobs  
✅ Test and validate anonymous access behavior  
✅ Apply appropriate access levels for different use cases  
✅ Understand security implications of public blob access  

**Next Steps:** Explore advanced blob storage features like lifecycle management, blob versioning, and soft delete.
