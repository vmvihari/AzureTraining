# Lab 05: The "9 Subnets" Challenge

**Objective**: Use mathematical functions (`floor`, `modulo`) to efficiently distribute child resources (Subnets) across parent resources (VNets) using a single loop.

## Scenario
*   **Resources**:
    *   **3 Resource Groups** (`testRG1`, `testRG2`, `testRG3`)
    *   **3 VNets** (`vnet1`, `vnet2`, `vnet3`), one in each RG.
    *   **9 Subnets**, distributed evenly (3 subnets per VNet).

## Instructions

### Step 1: Resource Groups & VNets
Create the foundation using standard `count` loops.

```hcl
resource "azurerm_resource_group" "rgs" {
  count    = 3
  name     = "testRG${count.index + 1}"
  location = "East US"
}

resource "azurerm_virtual_network" "vnets" {
  count               = 3
  name                = "vnet${count.index + 1}"
  location            = azurerm_resource_group.rgs[count.index].location
  resource_group_name = azurerm_resource_group.rgs[count.index].name
  address_space       = ["10.${count.index}.0.0/16"]
}
```

### Step 2: The 9 Subnets (The Hard Part)
We need to create 9 subnets.
*   `count = 9`
*   **Mapping Logic**:
    *   Subnet 0, 1, 2 -> VNet 0 (RG 0)
    *   Subnet 3, 4, 5 -> VNet 1 (RG 1)
    *   Subnet 6, 7, 8 -> VNet 2 (RG 2)

Add this block to your code:

```hcl
resource "azurerm_subnet" "subnets" {
  count = 9

  # Calculate Parent VNet Index: 0, 0, 0, 1, 1, 1, 2, 2, 2
  # floor(0/3) = 0, floor(3/3) = 1
  name                 = "subnet-${floor(count.index / 3) + 1}-${(count.index % 3) + 1}"
  
  # Reference the correct Parent VNet/RG using the math
  resource_group_name  = azurerm_resource_group.rgs[floor(count.index / 3)].name
  virtual_network_name = azurerm_virtual_network.vnets[floor(count.index / 3)].name

  # Distinct Address Prefixes
  # VNet 0: 10.0.1.0, 10.0.2.0, 10.0.3.0
  # VNet 1: 10.1.1.0...
  address_prefixes     = ["10.${floor(count.index / 3)}.${(count.index % 3) + 1}.0/24"]
}
```

### Step 3: Verify
1.  Run `terraform plan`.
2.  Inspect the output carefully.
    *   Check `subnet-1-1`: Should be in `vnet1`, Address `10.0.1.0/24`.
    *   Check `subnet-2-1`: Should be in `vnet2`, Address `10.1.1.0/24`.

## Why is this useful?
This pattern allows you to create massive, mathematically consistent infrastructures with very few lines of code, rather than copying and pasting blocks 100 times.
