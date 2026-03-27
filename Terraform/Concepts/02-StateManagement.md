# Terraform State & Directory Management

## 1. Directory Structure = Project Scope
In Terraform, **each folder is an independent project**.
*   **Isolation**: Resources defined in `Folder A` are completely separate from `Folder B`.
*   **Initialization**: You must run `terraform init` in *every* new directory to download the provider plugins.
    *   *Note*: If you create a new folder `Class2A` and add a `main.tf`, it will not work until you initialize it, even if you ran init in a previous folder.
    *   The `.terraform` folder (hidden) stores the plugins (~800MB+). It is safe to delete this to save space, but you must run `terraform init` again before working.

## 2. The State File (`terraform.tfstate`)
This file is the **Brain** of Terraform.
*   **Creation**: Generated automatically after your first successful `terraform apply`.
*   **Purpose**: It maps your code configuration to real-world Azure Resource IDs.
*   **Synchronization**:
    *   Terraform compares: **Code (Desired)** vs **State (Known)** vs **Azure (Actual)**.
    *   **Drift**: If you delete a resource in the Portal manually, Terraform detects it is missing from the State/Cloud and will try to recreate it.
    *   **Orphaned Resources**: If you lose the state file, Terraform loses track of the resources, even if they still exist in Azure.

### The Backup File
`terraform.tfstate.backup` preserves the state *before* the last operation, allowing for rollback if the state file gets corrupted.

## 3. State Locking
When running `plan` or `apply`, Terraform creates a temporary file: `.terraform.tfstate.lock.info`.
*   **Purpose**: Prevents two people (or two processes) from modifying the infrastructure at the same time.
*   **Behavior**: It contains a hash and operation details. It is automatically deleted when the command finishes.

## 4. Resource Naming: Terraform vs Azure
*   **Terraform ID**: The name used *inside* the code to reference the resource (e.g., `azurerm_resource_group.my_rg`).
*   **Azure Name**: The actual name of the resource in the cloud (e.g., `rg-demo-01`).
*   **Constraint**: You cannot have two resources with the same *Terraform ID* in the same folder.
