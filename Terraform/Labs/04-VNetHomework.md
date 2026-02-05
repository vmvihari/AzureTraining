# Lab 04: Terraform VNet & State Homework

**Topic**: Azure Virtual Network & Terraform State Behavior  
**Mode**: Individual  
**Objective**: Practice creating VNets, Subnets, and using the `count` parameter. Understand State synchronization and directory isolation.

---

## Task 1: Terraform Project Setup

1.  Create a new folder on your system named `terraform-vnet-practice`.
2.  Inside the folder, create a file named `main.tf`.

---

## Task 2: Provider Configuration

1.  Add the `terraform` block and `provider` block to `main.tf`.
    ```hcl
    terraform {
      required_providers {
        azurerm = {
          source  = "hashicorp/azurerm"
          version = "~> 3.0"
        }
      }
    }

    provider "azurerm" {
      features {}
    }
    ```
2.  Run initialization:
    ```powershell
    terraform init
    ```
    *   *Observation*: Verify `.terraform` folder is created.

---

## Task 3: Create Resource Groups Using `count`

Create 3 Resource Groups efficiently using a loop.

1.  Add the following resource block:
    ```hcl
    resource "azurerm_resource_group" "rgs" {
      count    = 3
      name     = "testRG${count.index + 1}"  # Creates testRG1, testRG2, testRG3
      location = "East US"
    }
    ```
2.  Apply the configuration:
    ```powershell
    terraform fmt
    terraform plan
    terraform apply
    ```

---

## Task 4: Create Virtual Network (VNet)

Create a VNet in the **first** Resource Group (`testRG1`).

1.  Add the VNet resource. note how we reference the **first** RG using `[0]`:
    ```hcl
    resource "azurerm_virtual_network" "vnet" {
      name                = "myVnet1"
      address_space       = ["10.0.0.0/16"]
      # referencing the first resource group created by the loop
      location            = azurerm_resource_group.rgs[0].location
      resource_group_name = azurerm_resource_group.rgs[0].name
    }
    ```
2.  Run `terraform plan` and `terraform apply`.

---

## Task 5: Create Subnet Inside the VNet

1.  Add the Subnet resource:
    ```hcl
    resource "azurerm_subnet" "sub" {
      name                 = "subnet1"
      resource_group_name  = azurerm_resource_group.rgs[0].name
      virtual_network_name = azurerm_virtual_network.vnet.name
      address_prefixes     = ["10.0.1.0/24"]
    }
    ```
2.  Apply changes and verify in the Azure Portal.

---

## Task 6: Terraform State Understanding

1.  Locate `terraform.tfstate` in your folder.
2.  **Question**: What is the purpose of this file?
    *   *Self-Answer*: It maps your code (resources like `myVnet1`) to the actual Azure Resource ID. It is the "source of truth" for Terraform.
3.  **Question**: Why does removing a block cause a destroy action?
    *   *Self-Answer*: Terraform compares Code vs State. If it's in State but not Code, Terraform assumes you want it deleted.

---

## Task 7: State Synchronization Test

1.  **Comment out** the entire `azurerm_subnet` block from Task 5.
2.  Run:
    ```powershell
    terraform plan
    ```
3.  **Observe and note**:
    *   **Which resource Terraform plans to destroy?**
        *   *Self-Answer*: `azurerm_subnet.sub`.
    *   **Why the destroy action appears?**
        *   *Self-Answer*: Because you removed it from the configuration (`main.tf`). Terraform sees it in the State file (so it exists in Azure), but since it's gone from your code, Terraform thinks you want to delete it. Code is the Desired State.
4.  **Re-enable** the block (uncomment) and run `terraform apply` to ensure it exists for the next task.

---

## Task 8: Resource Recreation Awareness

1.  Change the `address_prefixes` in the subnet block:
    *   From: `["10.0.1.0/24"]`
    *   To: `["10.0.2.0/24"]`
2.  Run `terraform plan`.
3.  **Observe**:
    *   Look for the `-/+` symbol.
    *   This means **Replace** (Destroy then Create). Most VNet changes force a replacement.

---

## Task 9: Directory Isolation Test

1.  Create a new folder `terraform-vnet-practice-2`.
2.  Copy your `main.tf` into this new folder.
3.  Open a terminal in this new folder and run `terraform init`.
4.  **Questions**:
    *   **Why is init required?** Because the `.terraform` (plugins) folder is specific to the directory/project.
    *   **Does it share state?** No. This is a completely separate project. If you apply this, it will try to create *new* resources (and fail if names collide with existing Azure resources).

---

## Task 10: Documentation Exploration

1.  Visit the [Terraform Registry (AzureRM)](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs).
2.  Search for `azurerm_virtual_network`.
3.  **Identify**:
    *   **azurerm_virtual_network**:
        *   *Mandatory*: `name`, `resource_group_name`, `location`, `address_space`.
        *   *Optional*: `dns_servers`, `subnet`, `tags`, `ddos_protection_plan`.
    *   **azurerm_subnet**:
        *   *Mandatory*: `name`, `resource_group_name`, `virtual_network_name`, `address_prefixes`.
        *   *Optional*: `delegation` (for linking services like Web Apps), `service_endpoints`, `private_endpoint_network_policies_enabled`.

4.  **Write 3 points on why documentation is important in Terraform**:
    *   **Updates & Deprecations**: Providers change frequently (e.g., AzureRM v3.0 to v4.0). Documentation warns you about deprecated fields or breaking changes.
    *   **Discovery**: You can't memorize every optional argument (like `delegation` or timeouts). The docs reveal powerful features you might not know exist.
    *   **Syntax Accuracy**: Copying the example usage block is the fastest way to get the correct syntax and required structure (blocks vs arguments).
