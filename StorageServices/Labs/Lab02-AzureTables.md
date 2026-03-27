# Lab: Azure Table Storage - Hands-On Practice

## Lab Overview

In this lab, you will learn how to work with Azure Table Storage, a NoSQL key-value store for structured data. You'll create a storage account, manually insert data through the Azure Portal, generate secure access credentials, and programmatically interact with tables using Python.

## Learning Objectives

By the end of this lab, you will be able to:
- Create and configure an Azure Storage Account with Table service
- Understand the structure of Azure Table entities (PartitionKey, RowKey, properties)
- Manually insert data into Azure Tables using the Azure Portal
- Generate and use SAS tokens and connection strings for secure access
- Install and configure the Azure Data Tables SDK for Python
- Programmatically create and insert entities using Python

## Prerequisites

- Active Azure subscription
- Python 3.13.0 installed on Windows 11
- Basic understanding of Python programming
- Text editor or IDE (VS Code recommended)

### Python Installation

> [!IMPORTANT]
> Python installation will include pip automatically if you follow the video instructions exactly. If pip is not installed, you will need to install it manually.

**Video Tutorial**: [How to install Python 3.13.0 on Windows 11](https://www.youtube.com/watch?v=C3bOxcILGu4)

**Verify Installation**:
1. Open Command Prompt (cmd)
2. Check Python version:
   ```bash
   python --version
   ```
3. Check pip version:
   ```bash
   pip --version
   ```

**Expected Output**:
```
Python 3.13.0
pip 24.x.x from ...
```

## Estimated Time to Complete

⏱️ **45-60 minutes**

---


## Exercise 1: Create a Storage Account & Enable Table Service

**Objective**: Understand how Azure Tables fit inside a Storage Account.

**Duration**: ⏱️ 10 minutes

### Instructions

#### Step 1: Log in to the Azure Portal
- Navigate to [https://portal.azure.com](https://portal.azure.com)
- Sign in with your Azure credentials

#### Step 2: Create a new Storage Account
1. Click on **"Create a resource"** or search for **"Storage Account"**
2. Click **"Create"**
3. Fill in the required details:
   - **Subscription**: Select your subscription
   - **Resource Group**: Create new or select existing
   - **Storage Account Name**: Enter a unique name (lowercase, no spaces)
   - **Region**: Select your preferred region
   - **Performance**: Standard
   - **Redundancy**: LRS (Locally Redundant Storage)
4. Click **"Review + Create"** then **"Create"**
5. Wait for deployment to complete (1-2 minutes)

#### Step 3: Navigate to Tables
1. Go to your newly created Storage Account
2. In the left menu, under **"Data storage"**, find **"Tables"** (or use **Storage browser** → **Tables**)

#### Step 4: Create a new table
1. Click **"+ Table"**
2. Enter table name: `UserProfiles`
3. Click **"OK"** or **"Create"**

### Validation

✅ **Success Criteria**: 
- Storage Account is successfully deployed
- You can see the **UserProfiles** table in the Tables section

---

## Exercise 2: Insert Data into Azure Table Using Azure Portal

**Objective**: Learn the structure of Azure Table entities and manually insert data.

**Duration**: ⏱️ 10 minutes

### Background

Azure Table entities consist of:
- **PartitionKey**: Groups related entities together (e.g., by country, department)
- **RowKey**: Unique identifier within a partition
- **PartitionKey + RowKey**: Together form the unique primary key
- **Custom Properties**: Additional fields you define

### Instructions

#### Step 1: Navigate to your table
1. Open your Storage Account
2. Go to **Storage Browser** → **Tables** → **UserProfiles**

#### Step 2: Add the first entity
1. Click **"+ Add entity"**
2. Fill in the following fields:
   - **PartitionKey**: `India`
   - **RowKey**: `001`
3. Click **"Add property"** to add custom fields:
   - **FirstName** (String): `John`
   - **LastName** (String): `Doe`
   - **Email** (String): `john.doe@example.com`
4. Click **"Add"** or **"Insert"**

#### Step 3: Add the second entity
1. Click **"+ Add entity"** again
2. Fill in the following fields:
   - **PartitionKey**: `USA`
   - **RowKey**: `002`
3. Add custom properties:
   - **FirstName** (String): `Mary`
   - **LastName** (String): `Smith`
   - **Email** (String): `mary.smith@example.com`
4. Click **"Add"** or **"Insert"**

### Validation

✅ **Success Criteria**: 
- Two entities are visible in the UserProfiles table
- One entity has PartitionKey "India" with RowKey "001"
- One entity has PartitionKey "USA" with RowKey "002"
- All custom properties are correctly stored



---

## Exercise 3: Generate SAS Token and Connection String for Table Access

**Objective**: Understand secure access to table data using Shared Access Signatures.

**Duration**: ⏱️ 5 minutes

### Background

Shared Access Signatures (SAS) provide secure, delegated access to resources in your storage account without sharing your account keys. You can control:
- Which resources the client may access
- What permissions they have
- How long the SAS is valid

### Instructions

#### Step 1: Navigate to Shared Access Signature
1. Go to your Storage Account
2. In the left menu, find **"Security + networking"** → **"Shared access signature"**

#### Step 2: Configure SAS settings
1. **Allowed services**: Check **Table**
2. **Allowed resource types**: Check all three:
   - ☑ Service
   - ☑ Container
   - ☑ Object
3. **Allowed permissions**: Check the following:
   - ☑ Read
   - ☑ Add
   - ☑ Update
   - ☑ Query
4. **Start and expiry date/time**: 
   - Set expiry to 12 or 24 hours from now
5. **Allowed protocols**: HTTPS only (recommended)

#### Step 3: Generate SAS
1. Scroll down and click **"Generate SAS and connection string"**
2. Wait for the generation to complete

#### Step 4: Copy the Connection String
1. Locate **"Connection string"** in the results
2. Click the **copy icon** to copy it to clipboard
3. **Save this securely** in a text file - you'll need it for Exercise 5

### Validation

✅ **Success Criteria**: 
- You have successfully generated a SAS token
- Connection string is copied and saved securely
- Connection string format: `DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net`

> [!WARNING]
> Keep your connection string secure! It provides access to your storage account. Never commit it to version control or share it publicly.

---

## Exercise 4: Install Azure Data Tables Python Library

**Objective**: Prepare the Python development environment for programmatic table operations.

**Duration**: ⏱️ 5 minutes

### Instructions

#### Step 1: Verify Python Installation
1. Open Command Prompt or Terminal
2. Run:
   ```bash
   python --version
   ```
3. Confirm you see Python 3.13.0 or similar

#### Step 2: Install Azure Data Tables SDK
1. Run the following command:
   ```bash
   pip install azure-data-tables
   ```
2. Wait for installation to complete (30-60 seconds)

#### Step 3: Verify Installation
- You should see output indicating successful installation
- The package and its dependencies will be downloaded and installed

### Validation

✅ **Success Criteria**: 
```
Successfully installed azure-data-tables-12.x.x azure-core-1.x.x ...
```

- No error messages during installation
- Package is ready to import in Python scripts

---

## Exercise 5: Write a Python Script to Insert Data into the Table

**Objective**: Practice programmatic table operations using the Azure SDK for Python.

**Duration**: ⏱️ 15 minutes

### Instructions

#### Step 1: Create the Python script
1. Create a new file named `AzureTableHomework.py`
2. Use any text editor or IDE (VS Code, Notepad++, etc.)

#### Step 2: Add the following code

Copy and paste this code into your file:

```python
from azure.data.tables import TableServiceClient

# Replace with your connection string from Task 3
connection_string = "<your_connection_string_here>"

# Create table service client
table_service = TableServiceClient.from_connection_string(conn_str=connection_string)

# Get table client for UserProfiles table
table_client = table_service.get_table_client(table_name="UserProfiles")

# Create a new entity
entity = {
    "PartitionKey": "Training",
    "RowKey": "003",
    "FirstName": "TestUser",
    "LastName": "Student",
    "Progress": "Beginner"
}

# Insert the entity into the table
table_client.create_entity(entity=entity)

print("Entity created successfully!")
```

#### Step 3: Update the connection string
1. Replace `<your_connection_string_here>` with the actual connection string you copied in Exercise 3
2. Make sure to keep the quotes around it

#### Step 4: Save the file

#### Step 5: Run the script
1. Open Command Prompt or Terminal
2. Navigate to the directory where you saved the file:
   ```bash
   cd path\to\your\script
   ```
3. Run the script:
   ```bash
   python AzureTableHomework.py
   ```

### Expected Output

```bash
PS D:\pipelines\C35\python> python .\AzureTableHomework.py
Entity created successfully!
```

### Validation

✅ **Success Criteria**: 
- Script runs without errors
- "Entity created successfully!" message is displayed
- A new entity with RowKey 003 is added under the Training partition

---

## Lab Verification

**Objective**: Confirm that all exercises were completed successfully.

### Instructions

#### Step 1: Navigate to Azure Portal
1. Go to your Storage Account
2. Navigate to **Storage browser** → **Tables** → **UserProfiles**

#### Step 2: Check for all entities

You should now see **3 entities** in total:
- India/001 (John Doe)
- USA/002 (Mary Smith)
- Training/003 (TestUser Student) ← **Created by Python script**

#### Step 3: Verify the entity details
1. Click on the Training/003 entity
2. Confirm all properties are present:
   - PartitionKey: Training
   - RowKey: 003
   - FirstName: TestUser
   - LastName: Student
   - Progress: Beginner

### Final Validation

✅ **Lab Complete**: 
- All 3 entities are visible in the UserProfiles table
- Manual entries (India/001, USA/002) are correct
- Programmatic entry (Training/003) is correct with all properties

---

## Troubleshooting Guide

### Common Issues and Solutions

**Problem**: `ModuleNotFoundError: No module named 'azure'`
- **Solution**: Make sure you installed the package: `pip install azure-data-tables`

**Problem**: `Authentication failed` or `403 Forbidden`
- **Solution**: Verify your connection string is correct and the SAS token hasn't expired. Generate a new SAS token if needed.

**Problem**: `ResourceNotFoundError: The specified resource does not exist`
- **Solution**: Verify the table name is exactly `UserProfiles` (case-sensitive).

**Problem**: `EntityAlreadyExists`
- **Solution**: The entity with PartitionKey "Training" and RowKey "003" already exists. Either delete it from the portal or change the RowKey in your script (e.g., "004").

---

## Additional Challenges (Optional)

To extend your learning, try these additional exercises:

1. **Query Operations**: Modify the Python script to query and display all entities with PartitionKey "India"
2. **Update Operations**: Update the "Progress" field of the Training/003 entity to "Intermediate"
3. **Delete Operations**: Write a script to delete a specific entity
4. **Batch Operations**: Insert multiple entities in a single batch operation
5. **Error Handling**: Add try-except blocks to handle common errors gracefully

---

## Resources

- [Azure Table Storage Documentation](https://docs.microsoft.com/azure/storage/tables/)
- [Azure SDK for Python - Tables](https://docs.microsoft.com/python/api/overview/azure/data-tables-readme)
- [Table Storage Best Practices](https://docs.microsoft.com/azure/storage/tables/table-storage-design)

---

**🎉 Congratulations on completing the Azure Table Storage Lab!**
