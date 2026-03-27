# Lab 01: Terraform Installation & Basics

**Objective**: Install Terraform, configure VS Code, and perform a basic deployment cycle (Init -> Plan -> Apply -> Destroy).

## 1. Prerequisites (Windows)

### Install Terraform
1.  Download the **Terraform Binary (AMD64)** for Windows from the official website.
2.  Extract the `terraform.exe` from the zip file.
3.  Move `terraform.exe` to a folder in your system **PATH**.
    *   *Tip*: If you have `Packer` installed (e.g., `Program Files\Packer`), you can drop it there since that folder is likely already in your PATH.
4.  Open a new CMD/PowerShell and verify:
    ```powershell
    terraform -version
    ```

### VS Code Extensions
1.  Open **VS Code**.
2.  Install the **HashiCorp Terraform** extension (for syntax highlighting and intellisense).
3.  Install the **Azure Terraform** extension (optional, for Azure-specific helpers).

### Authentication
You need to authenticate to Azure so Terraform can manage resources.
1.  Open the terminal in VS Code.
2.  Run:
    ```powershell
    az login --use-device-code
    ```
3.  Follow the browser prompt to sign in.

## 2. Creating Your First Infrastructure

1.  Create a new file `main.tf` in a new folder.
2.  **Define the Provider**:
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
3.  **Define a Resource Group**:
    ```hcl
    resource "azurerm_resource_group" "example" {
      name     = "rg-terraform-demo"
      location = "East US"
      
      tags = {
        environment = "dev"
      }
    }
    ```
    *   `azurerm_resource_group` is the **resource type**.
    *   `example` is the **Terraform ID** (internal name).
    *   `name = "rg-terraform-demo"` is the **Azure Name**.

## 3. The Lifecycle Walkthrough

Run the following commands in your terminal:

1.  **Initialize**:
    ```powershell
    terraform init
    ```
    *   *Observation*: Notice the `.terraform` folder is created.

2.  **Format & Validate**:
    ```powershell
    terraform fmt
    terraform validate
    ```

3.  **Plan**:
    ```powershell
    terraform plan
    ```
    *   *Observation*: Terraform shows it will "create" 1 resource.

4.  **Apply**:
    ```powershell
    terraform apply
    ```
    *   Type `yes` when prompted.
    *   *Verification*: Go to the Azure Portal and verify `rg-terraform-demo` exists.

5.  **Modify**:
    *   Change the `environment` tag in `main.tf` to `prod`.
    *   Run `terraform apply`.
    *   *Observation*: Terraform detects an **update** in-place (no destruction needed).

6.  **Destroy**:
    ```powershell
    terraform destroy
    ```
    *   Type `yes`.
    *   *Verification*: The resource group is removed from Azure.
