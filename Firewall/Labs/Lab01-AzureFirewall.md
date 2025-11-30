# Lab: Azure Firewall - Hub and Spoke Architecture

## Lab Overview

In this lab, you will build a secure Hub and Spoke network architecture in Azure. You will deploy Azure Firewall to control outbound traffic from a virtual machine located in a spoke network, verifying that traffic is correctly routed and filtered.

## Learning Objectives

By the end of this lab, you will be able to:
- Create a Hub and Spoke network topology with VNET peering
- Deploy and configure Azure Bastion for secure VM access
- Deploy Azure Firewall in a central hub network
- Configure User Defined Routes (UDR) to force traffic through the firewall
- Create Application Rules to filter outbound traffic
- Verify network security controls

## Prerequisites

- Active Azure subscription
- Basic understanding of Azure Networking (VNETs, Subnets)

## Estimated Time to Complete

⏱️ **60-90 minutes**

---

## Part 1: Create the Network Foundation

**Objective**: Establish the basic network structure with two separate Virtual Networks.

### Task 1: Create Resource Groups

1. Create a Resource Group for the Hub:
   - **Name**: `RG-Hub`
   - **Region**: Canada Central (or your preferred region)

2. Create a Resource Group for the Spoke:
   - **Name**: `RG-Spoke`
   - **Region**: Same as RG-Hub

### Task 2: Create Virtual Networks

#### 1. Hub VNET
- **Resource Group**: `RG-Hub`
- **Name**: `VNET-Hub`
- **Region**: Same as RG-Hub
- **Address Space**: `10.0.0.0/16`
- **Subnets**:
  - **AzureFirewallSubnet**: `10.0.1.0/24` (Must be named exactly this)
  - **AzureBastionSubnet**: `10.0.2.0/24` (Must be named exactly this, min /26)

#### 2. Spoke VNET
- **Resource Group**: `RG-Spoke`
- **Name**: `VNET-Spoke`
- **Region**: Same as RG-Spoke
- **Address Space**: `10.1.0.0/16`
- **Subnets**:
  - **Spoke-Subnet**: `10.1.1.0/24`

---

## Part 2: Deploy Required Azure Resources

**Objective**: Deploy the compute and connectivity resources.

### Task 3: Deploy Azure Bastion

1. Search for **"Bastions"** in the Azure Portal and click **Create**.
2. **Basics Tab**:
   - **Subscription**: Your subscription
   - **Resource Group**: `RG-Hub`
   - **Name**: `Bastion-Hub`
   - **Region**: Same as VNET-Hub
   - **Tier**: **Basic**
3. **Networking Tab**:
   - **Virtual Network**: Select `VNET-Hub`
   - **Subnet**: Should auto-select `AzureBastionSubnet`
   - **Public IP Address**: Click **Create new**
     - **Name**: `Bastion-Hub-PIP`
     - **SKU**: Standard
4. Click **Review + create** → **Create**.
   - *Note: Deployment takes 5-10 minutes.*

### Task 4: Create a Windows Virtual Machine

1. Create a Virtual Machine in the Spoke:
   - **Resource Group**: `RG-Spoke`
   - **Name**: `VM-Spoke`
   - **Region**: Same as VNET-Spoke
   - **Image**: Windows Server 2022 Datacenter
   - **Size**: Standard_B2s (or similar)
   - **Username/Password**: Create admin credentials
2. **Networking**:
   - **Virtual Network**: `VNET-Spoke`
   - **Subnet**: `Spoke-Subnet`
   - **Public IP**: **None** (We will use Bastion)
     - *Note: You can temporarily assign one for testing if you wish, but for the final lab verification, we will use Bastion.*
3. Click **Review + create** → **Create**.

---

## Part 3: Security and Routing Setup

**Objective**: Connect the networks and enforce traffic routing through the firewall.

### Task 5: Create VNET Peering

1. Go to `VNET-Hub` → **Peerings** → **+ Add**.
2. **This Virtual Network (Hub)**:
   - **Name**: `Hub-to-Spoke`
   - **Remote Virtual Network**: Select `VNET-Spoke`
   - **Allow forwarded traffic**: Check this box
3. **Remote Virtual Network (Spoke)**:
   - **Name**: `Spoke-to-Hub`
   - **Allow forwarded traffic**: Check this box
4. Click **Add**.

### Task 6: Deploy Azure Firewall

1. Search for **"Firewalls"** and click **Create**.
2. **Basics**:
   - **Resource Group**: `RG-Hub`
   - **Name**: `FW-Hub`
   - **Region**: Same as VNET-Hub
   - **Firewall SKU**: Standard
   - **Firewall Management**: Use a Firewall Policy (create new) or Classic (choose Classic for simple lab)
     - *Recommendation: Choose **Classic** for this specific lab if available, or create a new **Standard Policy**.*
3. **Networking**:
   - **Virtual Network**: Use existing `VNET-Hub`
   - **Subnet**: Auto-selected `AzureFirewallSubnet`
   - **Public IP Address**: Create new (`FW-PIP`)
4. Click **Review + create** → **Create**.
5. **IMPORTANT**: Once deployed, go to the Firewall resource and note its **Private IP address** (e.g., `10.0.1.4`).

### Task 7: Create and Assign a Route Table

1. Search for **"Route tables"** and click **Create**.
   - **Resource Group**: `RG-Spoke`
   - **Name**: `RT-Spoke`
   - **Region**: Same as VNET-Spoke
2. Go to the new Route Table resource.
3. **Routes** → **+ Add**:
   - **Route name**: `To-Firewall`
   - **Address prefix destination**: **IP Addresses**
   - **Destination IP addresses/CIDR ranges**: `0.0.0.0/0` (All traffic)
   - **Next hop type**: **Virtual appliance**
   - **Next hop address**: Enter the **Firewall Private IP** you noted earlier.
4. **Subnets** → **+ Associate**:
   - **Virtual network**: `VNET-Spoke`
   - **Subnet**: `Spoke-Subnet`
5. Click **OK**.

> [!NOTE]
> At this point, `VM-Spoke` loses internet access because all traffic is sent to the firewall, which blocks everything by default.

---

## Part 4: Firewall Rule Testing

**Objective**: Configure firewall rules to allow specific traffic and verify access.

### Task 8: Create an Application Rule

1. Go to your Azure Firewall (`FW-Hub`).
2. Select **Rules (Classic)** or **Firewall Policy** depending on what you chose.
   - *If using Classic Rules*: Click **Application rule collection** → **+ Add application rule collection**.
   - *If using Policy*: Go to the Policy → **Application Rules** → **+ Add Rule Collection**.
3. **Rule Collection**:
   - **Name**: `Allow-Google`
   - **Priority**: `100`
   - **Action**: **Allow**
4. **Rule**:
   - **Name**: `Allow-Google-Search`
   - **Source type**: **IP Address**
   - **Source**: `*` (or `10.1.0.0/16` for tighter security)
   - **Protocol**: `http, https`
   - **Target FQDNs**: `www.google.com`
5. Click **Add**.

### Task 9: Test Access

1. Go to `VM-Spoke` in the Azure Portal.
2. Click **Connect** → **Bastion**.
3. Enter your username and password.
4. Once logged in, open **Edge** or **Chrome**.
5. **Test 1**: Navigate to `www.google.com`.
   - **Result**: ✅ Should load successfully.
6. **Test 2**: Navigate to `www.microsoft.com`.
   - **Result**: ❌ Should be blocked (connection timed out or firewall error).
7. **Test 3**: Navigate to `www.instagram.com`.
   - **Result**: ❌ Should be blocked.

---

## Lab Cleanup

> [!IMPORTANT]
> Azure Firewall and Bastion are expensive resources. Delete them immediately after completing the lab to avoid high costs.

1. Delete **RG-Hub** (removes Firewall, Bastion, VNET-Hub).
2. Delete **RG-Spoke** (removes VM, VNET-Spoke).

## Troubleshooting

- **Bastion fails to deploy**: Ensure subnet is named exactly `AzureBastionSubnet` and is at least `/26`.
- **VM has internet access to everything**: Check if the Route Table is correctly associated with `Spoke-Subnet`.
- **VM has NO internet access to Google**: Check Firewall Rule priority and ensure Target FQDN is correct.
