# Lab 03: VNets and Loops with Terraform

**Objective**: Create complex networking resources and learn to use loops to generate multiple resources efficiently.

## Part 1: Creating a Basic VNet

1.  Create a new folder `terraform-vnet`.
2.  Create `main.tf` and initialize the provider.
3.  **Define Resources**:
    ```hcl
    resource "azurerm_resource_group" "rg" {
      name     = "rg-vnet-lab"
      location = "Central India"
    }

    resource "azurerm_virtual_network" "vnet" {
      name                = "my-vnet-01"
      # Dynamic Reference: Use the location/rg from the resource above
      location            = azurerm_resource_group.rg.location
      resource_group_name = azurerm_resource_group.rg.name
      address_space       = ["10.0.0.0/16"]
    }

    resource "azurerm_subnet" "subnet" {
      name                 = "web-subnet"
      resource_group_name  = azurerm_resource_group.rg.name
      virtual_network_name = azurerm_virtual_network.vnet.name
      address_prefixes     = ["10.0.1.0/24"]
    }
    ```
4.  Run `terraform init`, `plan`, and `apply`.
    *   *Observe*: Terraform handles the dependencies. It knows it must create the RG *before* the VNet.

## Part 2: Observing State Synchronization

1.  **Comment out** the Subnet block in your code (lines 14-19).
    *   *Tip*: Use `Ctrl + /` in VS Code to toggle comments.
2.  Run `terraform plan`.
    *   *Observation*: You will see a **Destroy** action (minus symbol `-`).
    *   *Reason*: The resource exists in the *State*, but not in the *Code*. Terraform matches the state to the code.
3.  **Uncomment** the block to restore it.

## Part 3: Using Loops (`count`)

Instead of copying and pasting code to create 3 resource groups, use `count`.

1.  Create a new file `loops.tf` (or append to `main.tf`).
2.  Add this code:
    ```hcl
    resource "azurerm_resource_group" "multi_rg" {
      count    = 3
      name     = "testRG${count.index + 1}"  # Result: testRG1, testRG2, testRG3
      location = "East US"
    }
    ```
3.  Run `terraform plan`.
    *   *Observation*: Terraform plans to create 3 resources.
    *   `${count.index}` is the current iteration (0, 1, 2). We add `+1` to make it human-friendly (1, 2, 3).
4.  Run `terraform apply`.
    *   *Observation*: Terraform uses **Parallel Execution** (multiple threads) to create these simultaneously, as they don't depend on each other.

## Part 4: Cleanup
1.  Run `terraform destroy` to remove all resources.
