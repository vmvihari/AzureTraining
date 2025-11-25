# Project 3: Azure Python-Based Storage Management Web Application

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Step-by-Step Implementation](#step-by-step-implementation)
  - [Phase 1: Azure Infrastructure Setup](#phase-1-azure-infrastructure-setup)
  - [Phase 2: Deploy the Python Application to Azure App Service](#phase-2-deploy-the-python-application-to-azure-app-service)
  - [Phase 3: Application Development in Azure Cloud Shell](#phase-3-application-development-in-azure-cloud-shell)
  - [Phase 4: Deploy the Python Application](#phase-4-deploy-the-python-application)
  - [Phase 5: Verification](#phase-5-verification)
- [Appendix: Command History](#appendix-command-history)

---

## Project Overview

This project implements a serverless Python-based web application deployed on Azure App Service. The application enables users to upload files and metadata, which are then stored across multiple Azure Storage services:

- **Azure Blob Storage**: For file uploads
- **Azure Table Storage**: For metadata storage
- **Azure File Share**: For persistent structured file storage

The application is developed in Python (Flask), deployed through Azure Cloud Shell, and hosted using Azure App Service (Linux).

---

## Architecture Overview

| Component | Service | Purpose |
|-----------|---------|---------|
| **Web App** | Azure App Service (Linux) | Hosts the Python Flask application |
| **Object Storage** | Azure Blob Storage | Stores uploaded files (unstructured data) |
| **NoSQL Store** | Azure Table Storage | Stores metadata about uploads |
| **File Storage** | Azure File Share | Stores persistent structured files |
| **Deployment** | Azure Cloud Shell | Used for development and deployment |

---

## Prerequisites

- Active Azure Subscription
- Azure Cloud Shell access (Bash)
- Basic knowledge of Python and Flask

---

## Step-by-Step Implementation

### Phase 1: Azure Infrastructure Setup

#### Step 1: Create a Resource Group

1. Sign in to the **Azure Portal**.
2. Navigate to **Resource Groups** > **Create**.
3. Configure:
   - **Subscription**: Pay-As-You-Go
   - **Resource Group Name**: `lucky`
   - **Region**: `canada central`
4. Click **Review + Create** → **Create**.

#### Step 2: Create the Azure Storage Account

1. Go to **Storage Accounts** > **Create**.
2. **Basics** tab:
   - **Resource Group**: `lucky`
   - **Storage Account Name**: `statestorage23315`
   - **Region**: `East US`
   - **Performance**: Standard
   - **Redundancy**: Locally-redundant storage (LRS)
3. **Advanced** tab:
   - **Hierarchical namespace**: Disabled
   - **Large File Shares**: Enabled
   - **SFTP**: Disabled
   - **NFS v3**: Disabled
   - **Access Tier**: Hot
4. **Security** tab:
   - **Secure transfer**: Enabled
   - **Anonymous access**: Disabled
   - **Account key access**: Enabled
   - **TLS Minimum Version**: 1.2
5. **Data Protection** tab:
   - All delete/versioning options: Disabled
6. **Networking** tab:
   - **Public network access**: Enabled
   - **Routing preference**: Microsoft network routing
7. Click **Review + Create** → **Create**.

#### Step 3: Configure Storage Services

**3.1 Create Blob Container**
1. Navigate to **Storage Account** → **Containers** → **+ Container**
2. **Name**: `uploads` (Do not change this name as it is used in the script)
3. **Access Level**: Private

**3.2 Create Azure Table Storage**
1. Navigate to **Storage Account** → **Tables** → **+ Table**
2. **Name**: `luckytable` (Do not change this name)

**3.3 Create Azure File Share**
1. Navigate to **File Shares** → **+ File Share**
2. **Name**: `luckyshare` (Do not change this name)
3. **Backup**: Disable backups (Important to avoid extra billing)

**3.4 Generate SAS Token**
1. Go to your **Storage Account** → **Shared Access Signatures**.
2. **Allowed resource types**: Check **Service**, **Container**, **Object**.
3. **Allowed permissions**: Check **Read**, **Add**, **Update**, **Query**.
4. **Expiry**: Set to 12 or 24 hours.
5. Click **Generate SAS and connection string**.
6. **Copy the SAS token** and make a note of it.

---

### Phase 2: Deploy the Python Application to Azure App Service

#### Step 4: Create the Azure App Service

1. Navigate to **App Services** → **Create**.
2. Configure:
   - **Resource Group**: `lucky`
   - **Name**: `lucky-webapp-18454` (You can give any unique name)
   - **Runtime Stack**: Python 3.14
   - **Region**: `canada central`
   - **App Service Plan**: Basic B1 (or upgrade if deployment fails)
3. Click **Review + Create** → **Create**.

---

### Phase 3: Application Development in Azure Cloud Shell

#### Step 5: Create App Folder and Files

1. Open **Azure Cloud Shell** (Bash).
2. Run the following commands:
   ```bash
   mkdir lucky
   cd lucky
   touch app.py
   touch requirements.txt
   ```

3. Use `nano` to update the files:
   ```bash
   nano app.py
   nano requirements.txt
   ```
   *(Paste the application code and requirements here)*

4. Save using `CTRL + O` → `Enter`, then `CTRL + X` to exit.

**Optional: Local Test using Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```
*Expected Output*: `* Running on http://127.0.0.1:5000`

---

### Phase 4: Deploy the Python Application

#### Step 6: Authenticate Azure CLI

To verify login:
```bash
az account show
```

If no account is found:
```bash
az login --use-device-code
```

#### Step 7: Deploy Using `az webapp up`

Run the deployment command:
```bash
az webapp up \
  --name lucky-webapp-18454 \
  --resource-group lucky \
  --sku B1 \
  --runtime "PYTHON:3.14" \
  --os-type Linux \
  --location canadacentral
```

Once deployment completes, Azure displays your App Service URL. Open it in the browser to verify successful deployment.

---

### Phase 5: Verification

1. Navigate to the App Service URL.
2. Test file upload functionality.
3. Validate:
   - Files appear in `luckycontainer` (Blob Storage)
   - Metadata appears in `emp_table` (Table Storage)
   - Files appear in `lucky_fileshare` (File Share)

---

## Appendix: Command History

Cleaned & Ordered Command History:

```bash
1  ls
2  cd lucky
3  mkdir lucky
4  cd lucky
5  nano app.py
6  nano requirements.txt
7  python3 -m venv venv
8  source venv/bin/activate
9  pip install -r requirements.txt 
10 pip freeze > requirements.txt
11 python3 app.py
12 az login --use-device-code
13 az webapp up --name lucky-webapp-18454 --resource-group lucky --sku B1 --runtime "PYTHON:3.14" --os-type Linux --location canadacentral
14 history
```
