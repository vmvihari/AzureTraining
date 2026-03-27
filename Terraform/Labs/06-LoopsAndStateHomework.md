# Homework: Terraform Loops, Functions & State Understanding

**Session Reference**: Azure CloudOps C35 – Session 52  
**Objective**: Implement a scalable Azure network setup using Terraform loops, dynamic naming, `floor` & `modulo` functions, and validate understanding of Terraform state behavior.

---

## Part 1: Environment Preparation

1.  Current Terraform Version: Ensure you have the latest stable version installed.
2.  Azure Login:
    ```powershell
    az login
    ```
3.  Create a new empty folder named: `terraform-loops-practice`
4.  Create your `main.tf` file inside this folder.

---

## Part 2: Resource Group Creation (Using `count`)

**Task**: Create 3 Azure Resource Groups using a single resource block with `count`.

**Requirements**:
*   Names must be: `rg-1`, `rg-2`, `rg-3`
*   Location: Same region for all (e.g., "East US").
*   **Constraint**: Do not hardcode three separate blocks.

**Code Hint**:
```hcl
resource "azurerm_resource_group" "rg" {
  count    = 3
  name     = "rg-${count.index + 1}"
  location = "East US"
}
```

**Validation**:
*   Run `terraform plan`.
*   Confirm 3 RGs are created.
*   Check State Indexing: `azurerm_resource_group.rg[0]`, `[1]`, `[2]`.

---

## Part 3: Virtual Network Creation (Mapping RGs to VNets)

**Task**: Create 3 Virtual Networks using `count`.

**Requirements**:
*   **Names**: `vnet-1`, `vnet-2`, `vnet-3`
*   **Address Spaces**:
    *   `vnet-1` → `10.0.0.0/16`
    *   `vnet-2` → `10.1.0.0/16`
    *   `vnet-3` → `10.2.0.0/16`
*   **Dynamic Assignment**: Use `count.index` to assign the correct Resource Group and Address Space.

**Code Hint**:
```hcl
resource "azurerm_virtual_network" "vnet" {
  count               = 3
  name                = "vnet-${count.index + 1}"
  resource_group_name = azurerm_resource_group.rg[count.index].name
  location            = azurerm_resource_group.rg[count.index].location
  address_space       = ["10.${count.index}.0.0/16"]
}
```

**Validation**:
*   Confirm `vnet-1` is in `rg-1`, `vnet-2` in `rg-2`, etc.

---

## Part 4: Advanced Subnet Creation (`floor` & `modulo`)

**Task**: Create **9 subnets** total, distributed evenly across the 3 VNets (3 subnets per VNet).

**Distribution Pattern**:
*   VNet-1 → `subnet-1-1`, `subnet-1-2`, `subnet-1-3`
*   VNet-2 → `subnet-2-1`, `subnet-2-2`, `subnet-2-3`
*   VNet-3 → `subnet-3-1`, `subnet-3-2`, `subnet-3-3`

**Mandatory Logic**:
*   Use `floor()` to determine the VNet (Parent).
*   Use `%` (modulo) to determine the Subnet Number (Child).
*   **Naming Formula**: `subnet-${floor(count.index / 3) + 1}-${(count.index % 3) + 1}`

**IP Addressing Rules**:
*   Each subnet must have a `/24`.
*   Pattern: `10.x.y.0/24` (where x is VNet index, y is Subnet index).

**Code Hint**:
```hcl
resource "azurerm_subnet" "subnets" {
  count = 9

  # Determine Parent VNet Index (0, 0, 0, 1, 1, 1...)
  # floor(0/3)=0, floor(1/3)=0, floor(3/3)=1
  virtual_network_name = azurerm_virtual_network.vnet[floor(count.index / 3)].name
  resource_group_name  = azurerm_resource_group.rg[floor(count.index / 3)].name

  # Generate Name: subnet-1-1, subnet-1-2...
  name = "subnet-${floor(count.index / 3) + 1}-${(count.index % 3) + 1}"

  # specific address prefix logic
  address_prefixes = ["10.${floor(count.index / 3)}.${(count.index % 3) + 1}.0/24"]
}
```

---

## Part 5: Terraform State & Index Analysis

1.  Run `terraform apply`.
2.  Run `terraform state list`.

**Analysis Questions** (Write answers in a text file):
1.  Why does Terraform show `subnet[0]`, `subnet[1]` instead of the visible names like `subnet-1-1`?
    *   *Self-Answer*: `subnet[0]` is the internal **Resource Instance Address** in the state file. Terraform uses the index because the resource uses `count`. The "Name" (`subnet-1-1`) is just a property *attribute* sent to Azure API, not the Terraform identifier.
2.  What is the difference between Resource Index and Resource Name?
    *   *Self-Answer*:
        *   **Index**: How Terraform tracks the item in the `tfstate` / code (e.g., `azurerm_resource_group.rg[0]`).
        *   **Name**: The actual string label the resource gets in the Azure Cloud (e.g., `rg-1`).
