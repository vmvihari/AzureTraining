# Project 3: Azure Python-Based Storage Management Web Application

## Project Overview
This project implements a serverless Python-based web application deployed on **Azure App Service**. The application enables users to upload files and metadata, which are then stored across multiple Azure Storage services:
- **Azure Blob Storage** for file uploads
- **Azure Table Storage** for metadata storage
- **Azure File Share** for persistent structured file storage

The application is developed in Python (Flask), deployed through Azure Cloud Shell, and hosted using Azure App Service (Linux).

## Phase 1: Azure Infrastructure Setup

### Step 1: Create a Resource Group
1. Sign in to the Azure Portal.
2. Navigate to **Resource Groups** > **Create**.
3. Configure:
   - **Subscription**: Pay-As-You-Go
   - **Resource Group Name**: `lucky`
   - **Region**: `canada central`
4. Click **Review + Create** → **Create**.

### Step 2: Create the Azure Storage Account
1. Go to **Storage Accounts** > **Create**.
2. Configure the **Basics** tab:
   - **Resource Group**: `lucky`
   - **Storage Account Name**: `statestorage23315` (or unique name)
   - **Region**: `East US` (Note: Different from RG region per prompt, but generally okay)
   - **Performance**: `Standard`
   - **Redundancy**: `Locally-redundant storage (LRS)`
3. Under **Advanced**, ensure:
   - **Hierarchical namespace**: Disabled
   - **Large File Shares**: Enabled
   - **SFTP**: Disabled
   - **NFS v3**: Disabled
   - **Access Tier**: Hot
4. Under **Security**:
   - **Secure transfer**: Enabled
   - **Anonymous access**: Disabled
   - **Account key access**: Enabled
   - **TLS Minimum Version**: 1.2
5. Under **Data Protection**:
   - **All delete/versioning options**: Disabled
6. Under **Networking**:
   - **Public network access**: Enabled
   - **Routing preference**: Microsoft network routing
7. Click **Review + Create** → **Create**.

### Step 3: Configure Storage Services

#### 3.1 Create Blob Container
1. Navigate to: **Storage Account** → **Containers** → **+ Container**.
2. **Name**: `uploads` (Do not change, required by script).
3. **Access Level**: `Private`.

#### 3.2 Create Azure Table Storage
1. Navigate to: **Storage Account** → **Tables** → **+ Table**.
2. **Name**: `luckytable` (Do not change, required by script).

#### 3.3 Create Azure File Share
1. Navigate to: **File Shares** → **+ File Share**.
2. **Name**: `luckyshare` (Do not change, required by script).
3. **Disable backups** (Important to avoid extra billing).

#### 3.4 Generate SAS Token (Concept)
*Objective: Understand secure access to table data.*
1. Go to your **Storage Account** → **Shared Access Signatures**.
2. **Allowed resource types**: Check **Service**, **Container**, **Object**.
3. **Allowed permissions**: Check **Read**, **Add**, **Update**, **Query**.
4. Set expiry to 12 or 24 hours.
5. Click **Generate SAS and connection string**.
6. **Copy the Connection String**. You will need this for the application to connect.
   - *Note: In a real deployment, we set this as an App Service Environment Variable.*

---

## Phase 2: Deploy the Python Application to Azure App Service

### Step 4: Create the Azure App Service
1. Navigate to **App Services** → **Create**.
2. Configure:
   - **Resource Group**: `lucky`
   - **Name**: `lucky-webapp-18454` (or unique name)
   - **Runtime Stack**: `Python 3.12` (Note: Python 3.14 is likely not available yet, stick to LTS/stable).
   - **Region**: `canada central`
   - **App Service Plan**: `Basic B1` (Upgrade to higher SKU if deployment fails or quota exceeded).
3. Click **Review + Create** → **Create**.

---

## Phase 3: Application Development in Azure Cloud Shell

### Step 5: Create App Folder and Files
1. Open Azure Cloud Shell (Bash).
2. Create directory and files:
   ```bash
   mkdir lucky
   cd lucky
   touch app.py
   touch requirements.txt
   ```

3. Update `app.py`:
   - Use `nano app.py`.
   - Copy the content of the provided `app.py` (ensure connection string logic is handled).
   - `CTRL + O` → `Enter` to save, `CTRL + X` to exit.

4. Update `requirements.txt`:
   - Use `nano requirements.txt`.
   - Add:
     ```
     flask
     azure-storage-blob
     azure-data-tables
     azure-storage-file-share
     ```
   - Save and exit.

### Optional: Local Test using Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Set connection string env var
export AZURE_STORAGE_CONNECTION_STRING="<your-connection-string>"
python3 app.py
```
*Expected Output:* `* Running on http://127.0.0.1:5000`

---

## Phase 4: Deploy the Python Application to Azure App Service

### Step 6: Authenticate Azure CLI
```bash
az account show
# If needed:
az login --use-device-code
```

### Step 7: Deploy Using `az webapp up`
Run the deployment command from within the `lucky` directory:
```bash
az webapp up \
  --name lucky-webapp-18454 \
  --resource-group lucky \
  --plan ASP-lucky-883d \
  --sku B1 \
  --runtime "PYTHON:3.12" \
  --os-type Linux \
  --location canadacentral
```
*(Note: Remove `--plan` if you want it to create one automatically, or ensure the plan name matches yours)*.

Once deployment completes, visit the URL provided in the output.

### Important: Configure Connection String
For the app to work on Azure, you must set the Connection String in the App Settings.
1. Go to App Service -> **Settings** -> **Environment variables**.
2. Add a new setting:
   - **Name**: `AZURE_STORAGE_CONNECTION_STRING`
   - **Value**: Your Storage Account Connection String.
3. Save and Restart the App.

---

## Phase 5: Verification
1. Navigate to the App Service URL.
2. Upload a file using the web interface.
3. Validate resources in Azure Portal:
   - **Blob**: File appears in `uploads` container.
   - **Table**: Metadata entity appears in `luckytable`.
   - **File Share**: File appears in `luckyshare`.
