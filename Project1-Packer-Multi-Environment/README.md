# Project 1: Azure Multi-Environment Custom Image Deployment with Packer

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Step-by-Step Implementation](#step-by-step-implementation)
  - [Step 1: Create Service Principal](#step-1-create-service-principal-and-assign-roles)
  - [Step 2: Create Resource Groups](#step-2-create-resource-groups)
  - [Step 3: Create Users and Assign RBAC](#step-3-create-users-and-assign-rbac-roles)
  - [Step 4: Validate RBAC Permissions](#step-4-validate-rbac-by-logging-into-users)
  - [Step 5: Create Virtual Networks](#step-5-create-virtual-networks)
  - [Step 6: Create Packer Templates](#step-6-create-packer-templates)
  - [Step 7: Build Custom Images](#step-7-build-custom-images-using-packer)
  - [Step 8: Verify Images](#step-8-verify-images-in-azure-portal)
  - [Step 9: Deploy Virtual Machines](#step-9-deploy-virtual-machines-from-custom-images)
  - [Step 10: Enable Network Peering](#step-10-enable-peering-between-dev-and-test)
  - [Step 11: Final Validation](#step-11-final-validation)
- [Troubleshooting](#troubleshooting)

---

## Architecture Overview

This project builds **three isolated environments** (Dev, Test, Prod), each with:

| Component | Dev | Test | Prod |
|-----------|-----|------|------|
| **Resource Group** | `dev-rg` | `test-rg` | `prod-rg` |
| **Location** | East US | Canada Central | West US |
| **Virtual Network** | `dev-vnet` | `test-vnet` | `prod-vnet` |
| **Custom Image** | `devPackerImage` | `testPackerImage` | `prodPackerImage` |
| **Software Stack** | Java, Python, NodeJS | JMeter, Selenium | Nginx, Apache |
| **RBAC User** | `dev-user` (Contributor) | `test-user` (VM Contributor) | `prod-user` (Owner) |

**Network Peering**: Enabled only between Dev ↔ Test networks

---

## Prerequisites

Before starting, ensure you have:

- [ ] **Packer** installed locally ([Download Packer](https://www.packer.io/downloads))
- [ ] **Azure CLI** installed ([Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
- [ ] Active **Azure Subscription**
- [ ] Access to **Microsoft Entra ID** (formerly Azure AD)
- [ ] Basic understanding of Azure RBAC and networking

---

## Step-by-Step Implementation

### Step 1: Create Service Principal and Assign Roles

The service principal `lucky` will be used by Packer to authenticate and create custom images.

#### 1.1 Create App Registration

1. Navigate to **Azure Portal** → **Microsoft Entra ID** → **App registrations**
2. Click **+ New registration**
3. Enter the following details:
   - **Name**: `lucky`
   - **Supported account types**: Accounts in this organizational directory only
4. Click **Register**

#### 1.2 Generate Client Secret

1. In the `lucky` app registration, go to **Certificates & secrets**
2. Click **+ New client secret**
3. Enter a description (e.g., "Packer Secret")
4. Set expiration (recommended: 12 months)
5. Click **Add**
6. **⚠️ IMPORTANT**: Copy the secret **Value** immediately (you won't see it again)

#### 1.3 Collect Required IDs

Note down the following values:

```plaintext
client_id       = <Application (client) ID from Overview page>
client_secret   = <Secret value from step 1.2>
tenant_id       = <Directory (tenant) ID from Overview page>
subscription_id = <Your Azure Subscription ID>
```

#### 1.4 Assign Subscription-Level Role

1. Navigate to **Subscriptions** → Select your subscription
2. Click **Access control (IAM)** → **+ Add** → **Add role assignment**
3. Select **Contributor** role
4. Click **Next** → **+ Select members**
5. Search for `lucky` and select it
6. Click **Review + assign**

> **📺 Video Tutorial**: [Create a new user in Azure Active Directory](https://www.youtube.com/watch?v=xOkv1X8I5zE)

---

### Step 2: Create Resource Groups

Create three resource groups in different regions:

#### Using Azure Portal:

1. Navigate to **Resource groups** → **+ Create**
2. Create the following:

| Name | Region |
|------|--------|
| `dev-rg` | East US |
| `test-rg` | Canada Central |
| `prod-rg` | West US |

#### Using Azure CLI:

```bash
# Login to Azure
az login

# Create resource groups
az group create --name dev-rg --location eastus
az group create --name test-rg --location canadacentral
az group create --name prod-rg --location westus
```

---

### Step 3: Create Users and Assign RBAC Roles

#### 3.1 Create Users in Microsoft Entra ID

1. Navigate to **Microsoft Entra ID** → **Users** → **+ New user**
2. Create three users:

| User Principal Name | Display Name | Role Assignment |
|---------------------|--------------|-----------------|
| `dev-user@yourdomain.com` | Dev User | Contributor on `dev-rg` |
| `test-user@yourdomain.com` | Test User | Virtual Machine Contributor on `test-rg` |
| `prod-user@yourdomain.com` | Prod User | Owner on `prod-rg` |

3. Set initial passwords and note them down

#### 3.2 Assign RBAC Roles

**For dev-user (Contributor on dev-rg):**
1. Go to **Resource groups** → **dev-rg** → **Access control (IAM)**
2. Click **+ Add** → **Add role assignment**
3. Select **Contributor** → **Next**
4. Click **+ Select members** → Search for `dev-user` → **Select**
5. Click **Review + assign**

**For test-user (Virtual Machine Contributor on test-rg):**
1. Go to **Resource groups** → **test-rg** → **Access control (IAM)**
2. Select **Virtual Machine Contributor** role
3. Assign to `test-user`

**For prod-user (Owner on prod-rg):**
1. Go to **Resource groups** → **prod-rg** → **Access control (IAM)**
2. Select **Owner** role
3. Assign to `prod-user`

#### Using Azure CLI:

```bash
# Get user object IDs
DEV_USER_ID=$(az ad user show --id dev-user@yourdomain.com --query id -o tsv)
TEST_USER_ID=$(az ad user show --id test-user@yourdomain.com --query id -o tsv)
PROD_USER_ID=$(az ad user show --id prod-user@yourdomain.com --query id -o tsv)

# Assign roles
az role assignment create --assignee $DEV_USER_ID --role "Contributor" --resource-group dev-rg
az role assignment create --assignee $TEST_USER_ID --role "Virtual Machine Contributor" --resource-group test-rg
az role assignment create --assignee $PROD_USER_ID --role "Owner" --resource-group prod-rg
```

---

### Step 4: Validate RBAC by Logging Into Users

> **⚠️ CRITICAL**: This validation step ensures RBAC is correctly configured before proceeding.

#### 4.1 Validate dev-user

1. Open an **Incognito/Private browser window**
2. Navigate to [Azure Portal](https://portal.azure.com)
3. Sign in as `dev-user@yourdomain.com`
4. **Expected Behavior**:
   - ✅ Can view and access `dev-rg`
   - ✅ Can create/modify resources in `dev-rg`
   - ❌ Cannot view `test-rg` or `prod-rg`
   - ❌ Cannot access subscription-level settings

#### 4.2 Validate test-user

1. Open a new **Incognito/Private browser window**
2. Sign in as `test-user@yourdomain.com`
3. **Expected Behavior**:
   - ✅ Can view `test-rg`
   - ✅ Can manage VMs in `test-rg`
   - ❌ Cannot modify networking or images
   - ❌ Cannot view `dev-rg` or `prod-rg`
   - ❌ No subscription-level access

#### 4.3 Validate prod-user

1. Open a new **Incognito/Private browser window**
2. Sign in as `prod-user@yourdomain.com`
3. **Expected Behavior**:
   - ✅ Full control over `prod-rg`
   - ✅ Can create/delete all resources in `prod-rg`
   - ❌ Cannot view `dev-rg` or `test-rg`
   - ❌ No subscription-level access

> **✅ Checkpoint**: Only proceed if all validations pass.

---

### Step 5: Create Virtual Networks

Create isolated virtual networks for each environment with non-overlapping address spaces.

#### Using Azure Portal:

1. Navigate to **Virtual networks** → **+ Create**
2. Create the following VNets:

| VNet Name | Resource Group | Region | Address Space |
|-----------|----------------|--------|---------------|
| `dev-vnet` | `dev-rg` | East US | `10.1.0.0/16` |
| `test-vnet` | `test-rg` | Canada Central | `10.2.0.0/16` |
| `prod-vnet` | `prod-rg` | West US | `10.3.0.0/16` |

3. For each VNet, create a default subnet:
   - **dev-vnet**: Subnet `10.1.1.0/24`
   - **test-vnet**: Subnet `10.2.1.0/24`
   - **prod-vnet**: Subnet `10.3.1.0/24`

#### Using Azure CLI:

```bash
# Create dev-vnet
az network vnet create \
  --resource-group dev-rg \
  --name dev-vnet \
  --location eastus \
  --address-prefix 10.1.0.0/16 \
  --subnet-name default \
  --subnet-prefix 10.1.1.0/24

# Create test-vnet
az network vnet create \
  --resource-group test-rg \
  --name test-vnet \
  --location canadacentral \
  --address-prefix 10.2.0.0/16 \
  --subnet-name default \
  --subnet-prefix 10.2.1.0/24

# Create prod-vnet
az network vnet create \
  --resource-group prod-rg \
  --name prod-vnet \
  --location westus \
  --address-prefix 10.3.0.0/16 \
  --subnet-name default \
  --subnet-prefix 10.3.1.0/24
```

---

### Step 6: Create Packer Templates

Create three Packer template files, one for each environment.

#### 6.1 Create dev.pkr.hcl

Create a file named `dev.pkr.hcl` with the following content:

```hcl
packer {
  required_plugins {
    azure = {
      source  = "github.com/hashicorp/azure"
      version = ">= 2.0.0"
    }
  }
}

source "azure-arm" "dev" {
  client_id        = "YOUR_CLIENT_ID"
  client_secret    = "YOUR_CLIENT_SECRET"
  tenant_id        = "YOUR_TENANT_ID"
  subscription_id  = "YOUR_SUBSCRIPTION_ID"

  managed_image_resource_group_name = "dev-rg"
  managed_image_name                = "devPackerImage"

  os_type         = "Linux"
  image_publisher = "canonical"
  image_offer     = "0001-com-ubuntu-server-jammy"
  image_sku       = "22_04-lts"

  location = "eastus"
  vm_size  = "Standard_DS2_v2"

  azure_tags = {
    dept = "Engineering"
    task = "Image deployment"
    env  = "Dev"
  }
}

build {
  name    = "linux-dev-image"
  sources = ["source.azure-arm.dev"]

  provisioner "shell" {
    inline = [
      "sudo hostnamectl set-hostname dev-vm",
      "sudo apt-get update -y",
      "sudo apt-get upgrade -y",
      "sudo apt-get install -y openjdk-11-jdk",
      "sudo apt-get install -y python3 python3-pip",
      "sudo apt-get install -y nodejs npm"
    ]
  }
}
```

#### 6.2 Create test.pkr.hcl

Create a file named `test.pkr.hcl`:

```hcl
packer {
  required_plugins {
    azure = {
      source  = "github.com/hashicorp/azure"
      version = ">= 2.0.0"
    }
  }
}

source "azure-arm" "test" {
  client_id        = "YOUR_CLIENT_ID"
  client_secret    = "YOUR_CLIENT_SECRET"
  tenant_id        = "YOUR_TENANT_ID"
  subscription_id  = "YOUR_SUBSCRIPTION_ID"

  managed_image_resource_group_name = "test-rg"
  managed_image_name                = "testPackerImage"

  os_type         = "Linux"
  image_publisher = "canonical"
  image_offer     = "0001-com-ubuntu-server-jammy"
  image_sku       = "22_04-lts"

  location = "canadacentral"
  vm_size  = "Standard_DS2_v2"

  azure_tags = {
    dept = "Engineering"
    task = "Image deployment"
    env  = "Test"
  }
}

build {
  name    = "linux-test-image"
  sources = ["source.azure-arm.test"]

  provisioner "shell" {
    inline = [
      "sudo hostnamectl set-hostname test-vm",
      "sudo apt-get update -y",
      "sudo apt-get upgrade -y",
      "sudo apt-get install -y default-jre",
      "wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.5.tgz",
      "sudo tar -xzf apache-jmeter-5.5.tgz -C /opt/",
      "sudo apt-get install -y python3 python3-pip",
      "sudo pip3 install selenium"
    ]
  }
}
```

#### 6.3 Create prod.pkr.hcl

Create a file named `prod.pkr.hcl`:

```hcl
packer {
  required_plugins {
    azure = {
      source  = "github.com/hashicorp/azure"
      version = ">= 2.0.0"
    }
  }
}

source "azure-arm" "prod" {
  client_id        = "YOUR_CLIENT_ID"
  client_secret    = "YOUR_CLIENT_SECRET"
  tenant_id        = "YOUR_TENANT_ID"
  subscription_id  = "YOUR_SUBSCRIPTION_ID"

  managed_image_resource_group_name = "prod-rg"
  managed_image_name                = "prodPackerImage"

  os_type         = "Linux"
  image_publisher = "canonical"
  image_offer     = "0001-com-ubuntu-server-jammy"
  image_sku       = "22_04-lts"

  location = "westus"
  vm_size  = "Standard_DS2_v2"

  azure_tags = {
    dept = "Engineering"
    task = "Image deployment"
    env  = "Prod"
  }
}

build {
  name    = "linux-prod-image"
  sources = ["source.azure-arm.prod"]

  provisioner "shell" {
    inline = [
      "sudo hostnamectl set-hostname prod-vm",
      "sudo apt-get update -y",
      "sudo apt-get upgrade -y",
      "sudo apt-get install -y nginx",
      "sudo apt-get install -y apache2"
    ]
  }
}
```

> **⚠️ IMPORTANT**: Replace `YOUR_CLIENT_ID`, `YOUR_CLIENT_SECRET`, `YOUR_TENANT_ID`, and `YOUR_SUBSCRIPTION_ID` with the actual values from Step 1.

---

### Step 7: Build Custom Images Using Packer

Execute the following commands for each Packer template:

#### 7.1 Build Dev Image

```bash
# Initialize Packer (downloads required plugins)
packer init dev.pkr.hcl

# Validate the template
packer validate dev.pkr.hcl

# Build the image
packer build dev.pkr.hcl
```

**Expected Output**:
```
==> azure-arm.dev: Creating Azure Resource Manager (ARM) client...
==> azure-arm.dev: Creating resource group...
==> azure-arm.dev: Validating deployment template...
==> azure-arm.dev: Deploying deployment template...
==> azure-arm.dev: Provisioning with shell script...
==> azure-arm.dev: Querying the machine's properties...
==> azure-arm.dev: Capturing image...
Build 'azure-arm.dev' finished after X minutes.
```

#### 7.2 Build Test Image

```bash
packer init test.pkr.hcl
packer validate test.pkr.hcl
packer build test.pkr.hcl
```

#### 7.3 Build Prod Image

```bash
packer init prod.pkr.hcl
packer validate prod.pkr.hcl
packer build prod.pkr.hcl
```

> **⏱️ Note**: Each build takes approximately 10-15 minutes.

---

### Step 8: Verify Images in Azure Portal

After all builds complete, verify the images were created:

1. Navigate to **Azure Portal** → **Resource groups**
2. Open **dev-rg** → Click **Images** → Verify `devPackerImage` exists
3. Open **test-rg** → Click **Images** → Verify `testPackerImage` exists
4. Open **prod-rg** → Click **Images** → Verify `prodPackerImage` exists

#### Using Azure CLI:

```bash
# List images in each resource group
az image list --resource-group dev-rg --output table
az image list --resource-group test-rg --output table
az image list --resource-group prod-rg --output table
```

---

### Step 9: Deploy Virtual Machines from Custom Images

Deploy VMs using the custom images created by Packer.

#### 9.1 Deploy Dev VM

**Using Azure Portal**:
1. Navigate to **Virtual machines** → **+ Create**
2. **Basics**:
   - Resource group: `dev-rg`
   - VM name: `dev-vm`
   - Region: `East US`
   - Image: Click **See all images** → **My Images** → Select `devPackerImage`
   - Size: `Standard_DS2_v2`
   - Authentication: SSH public key or Password
3. **Networking**:
   - Virtual network: `dev-vnet`
   - Subnet: `default`
   - Public IP: Create new
4. Click **Review + create** → **Create**

**Using Azure CLI**:
```bash
az vm create \
  --resource-group dev-rg \
  --name dev-vm \
  --image devPackerImage \
  --vnet-name dev-vnet \
  --subnet default \
  --admin-username azureuser \
  --generate-ssh-keys
```

#### 9.2 Deploy Test VM

```bash
az vm create \
  --resource-group test-rg \
  --name test-vm \
  --image testPackerImage \
  --vnet-name test-vnet \
  --subnet default \
  --admin-username azureuser \
  --generate-ssh-keys
```

#### 9.3 Deploy Prod VM

```bash
az vm create \
  --resource-group prod-rg \
  --name prod-vm \
  --image prodPackerImage \
  --vnet-name prod-vnet \
  --subnet default \
  --admin-username azureuser \
  --generate-ssh-keys
```

---

### Step 10: Enable Peering Between Dev and Test

Enable bi-directional VNet peering between Dev and Test environments.

#### Using Azure Portal:

**Create Dev → Test Peering**:
1. Navigate to **Virtual networks** → **dev-vnet**
2. Click **Peerings** → **+ Add**
3. Configure:
   - **This virtual network**:
     - Peering link name: `dev-to-test`
     - Allow traffic to remote virtual network: ✅
   - **Remote virtual network**:
     - Peering link name: `test-to-dev`
     - Virtual network: Select `test-vnet`
     - Allow traffic from remote virtual network: ✅
4. Click **Add**

#### Using Azure CLI:

```bash
# Get VNet IDs
DEV_VNET_ID=$(az network vnet show --resource-group dev-rg --name dev-vnet --query id -o tsv)
TEST_VNET_ID=$(az network vnet show --resource-group test-rg --name test-vnet --query id -o tsv)

# Create peering from dev to test
az network vnet peering create \
  --name dev-to-test \
  --resource-group dev-rg \
  --vnet-name dev-vnet \
  --remote-vnet $TEST_VNET_ID \
  --allow-vnet-access

# Create peering from test to dev
az network vnet peering create \
  --name test-to-dev \
  --resource-group test-rg \
  --vnet-name test-vnet \
  --remote-vnet $DEV_VNET_ID \
  --allow-vnet-access
```

#### Verify Peering Status:

```bash
az network vnet peering list --resource-group dev-rg --vnet-name dev-vnet --output table
az network vnet peering list --resource-group test-rg --vnet-name test-vnet --output table
```

Both should show `PeeringState: Connected`

---

### Step 11: Final Validation

Perform comprehensive validation of all components.

#### 11.1 SSH into VMs

```bash
# Get public IPs
DEV_IP=$(az vm show -d --resource-group dev-rg --name dev-vm --query publicIps -o tsv)
TEST_IP=$(az vm show -d --resource-group test-rg --name test-vm --query publicIps -o tsv)
PROD_IP=$(az vm show -d --resource-group prod-rg --name prod-vm --query publicIps -o tsv)

# SSH into dev-vm
ssh azureuser@$DEV_IP
```

#### 11.2 Validate Network Connectivity

**From dev-vm, ping test-vm**:
```bash
# Get test-vm private IP
TEST_PRIVATE_IP=$(az vm show -d --resource-group test-rg --name test-vm --query privateIps -o tsv)

# SSH into dev-vm and ping test-vm
ssh azureuser@$DEV_IP
ping $TEST_PRIVATE_IP
```

**Expected**: Successful ping (peering is working)

**From dev-vm, try to ping prod-vm**:
```bash
# Get prod-vm private IP
PROD_PRIVATE_IP=$(az vm show -d --resource-group prod-rg --name prod-vm --query privateIps -o tsv)

# From dev-vm
ping $PROD_PRIVATE_IP
```

**Expected**: Failed ping (no peering between dev and prod)

#### 11.3 Validate Installed Software

**On dev-vm**:
```bash
ssh azureuser@$DEV_IP

# Check Java
java -version
# Expected: openjdk version "11.x.x"

# Check Python
python3 --version
# Expected: Python 3.x.x

# Check NodeJS
node --version
# Expected: v12.x.x or higher

npm --version
# Expected: 6.x.x or higher
```

**On test-vm**:
```bash
ssh azureuser@$TEST_IP

# Check JMeter
ls /opt/apache-jmeter-5.5
# Expected: bin  docs  lib  licenses  printable_docs  README.md

# Check Selenium
python3 -c "import selenium; print(selenium.__version__)"
# Expected: Selenium version number
```

**On prod-vm**:
```bash
ssh azureuser@$PROD_IP

# Check Nginx
nginx -v
# Expected: nginx version: nginx/1.x.x

# Check Apache
apache2 -v
# Expected: Server version: Apache/2.x.x
```

#### 11.4 Final Checklist

- [ ] All three resource groups created (dev-rg, test-rg, prod-rg)
- [ ] Service principal `lucky` has Contributor access
- [ ] Three users created with appropriate RBAC roles
- [ ] RBAC validation completed for all users
- [ ] Three VNets created with non-overlapping address spaces
- [ ] Three custom images built successfully with Packer
- [ ] Three VMs deployed from custom images
- [ ] VNet peering enabled between dev-vnet and test-vnet
- [ ] Connectivity verified: dev-vm ↔ test-vm (success), dev-vm ↔ prod-vm (fail)
- [ ] Software validated on all VMs

---

## Troubleshooting

### Packer Build Fails

**Error**: `Error: compute.VirtualMachinesClient#CreateOrUpdate: Failure sending request`

**Solution**: Verify the service principal has Contributor role at subscription level.

### RBAC Validation Fails

**Error**: User can see resources they shouldn't access

**Solution**: 
1. Wait 5-10 minutes for RBAC propagation
2. Clear browser cache and sign in again
3. Verify role assignments in IAM

### Peering Not Working

**Error**: Cannot ping between dev-vm and test-vm

**Solution**:
1. Verify peering status is "Connected" on both sides
2. Check NSG rules allow ICMP traffic
3. Ensure VMs are in the correct VNets

### SSH Connection Refused

**Error**: `Connection refused` when trying to SSH

**Solution**:
1. Verify NSG allows port 22
2. Check VM is running: `az vm get-instance-view --resource-group <rg> --name <vm-name>`
3. Verify public IP is correct

---

## Summary

You have successfully:
- ✅ Created a multi-environment Azure infrastructure
- ✅ Implemented RBAC with least-privilege access
- ✅ Built custom VM images using Packer
- ✅ Deployed VMs from custom images
- ✅ Configured network isolation and selective peering
- ✅ Validated all components end-to-end

**Next Steps**: Consider automating this deployment using Terraform or Azure Resource Manager templates.
