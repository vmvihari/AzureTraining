# Advanced Loops & Mathematical Functions

## 1. The Challenge: Flattening Nested Structures
In Terraform, you often need to create resources in a hierarchical structure (e.g., VNets containing Subnets) using simple loops.
*   **Problem**: `count` is a simple iterative loop (0, 1, 2...).
*   **Scenario**: Creating **9 Subnets** distributed across **3 VNets** (3 subnets per VNet) using a single loop.

## 2. Mathematical Functions
To solve this, we map the single index `i` (0 to 8) to Parent (VNet) and Child (Subnet) indices.

### `floor()` - Finding the Parent
*   **Purpose**: Rounds down to the nearest integer. Used to determine which "Batch" or "Parent" the current item belongs to.
*   **Formula**: `floor(count.index / size_of_batch)`
*   **Example (Batch Size 3)**:
    *   Index 0: `floor(0 / 3)` = `0` -> VNet 1
    *   Index 1: `floor(1 / 3)` = `0` -> VNet 1
    *   Index 2: `floor(2 / 3)` = `0` -> VNet 1
    *   Index 3: `floor(3 / 3)` = `1` -> VNet 2

### `ceil()` - Rounding Up
*   **Purpose**: The opposite of floor. Rounds up to the nearest integer.
*   *Note*: Less commonly used for index mapping, but useful for capacity planning (e.g., calculating required nodes).

### `%` (Modulo) - Finding the Child Position
*   **Purpose**: Returns the *remainder* of division. Used to cycle through numbers (1, 2, 3, 1, 2, 3...).
*   **Formula**: `count.index % size_of_batch`
*   **Example (Batch Size 3)**:
    *   Index 0: `0 % 3` = `0` -> Subnet 1
    *   Index 1: `1 % 3` = `1` -> Subnet 2
    *   Index 2: `2 % 3` = `2` -> Subnet 3
    *   Index 3: `3 % 3` = `0` -> Subnet 1 (Cycle restarts)

## 3. Applying the Logic
By combining these, we can dynamically generate names and IP addresses:

```hcl
# VNet Index (0, 0, 0, 1, 1, 1...)
local.vnet_index = floor(count.index / 3)

# Subnet Index (0, 1, 2, 0, 1, 2...)
local.subnet_index = count.index % 3

# Name Example: subnet-vnet1-1, subnet-vnet1-2...
name = "subnet-vnet${local.vnet_index + 1}-${local.subnet_index + 1}"
```
