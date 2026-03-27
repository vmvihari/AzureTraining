# Introduction to Terraform

## 1. What is Terraform?

Terraform is an **Infrastructure as Code (IaC)** tool that allows you to build, change, and version infrastructure safely and efficiently.
*   **Declarative**: You tell Terraform *what* you want (e.g., "I want a Resource Group named `rg-demo`"), and Terraform figures out *how* to create it.
*   **Platform Agnostic**: Supports Azure, AWS, Google Cloud, Kubernetes, and more via **Providers**.
*   **Language**: Uses **HCL (HashiCorp Configuration Language)**, designed to be easy for humans to read and write.

> [!NOTE]
> Terraform (HashiCorp) was recently acquired by **IBM**.

## 2. Core Concepts

### Provider
A plugin that enables Terraform to interact with an API.
*   **AzureRM Provider**: Used to manage resources in Microsoft Azure.
*   **Versioning**: Providers are updated frequently (every few days/weeks) to support new cloud features. A `.terraform.lock.hcl` file ensures appropriate versions are used.

### Resources
The fundamental building blocks.
*   A resource might be a virtual machine, a DNS record, or a resource group.
*   **Naming**: Every resource has a **Terraform ID** (used inside the code) and an **Azure Name** (actual name in the cloud).

### State File (`terraform.tfstate`)
*   This file is the **source of truth** for your environment.
*   It maps real-world resources to your configuration.
*   **Critical**: If creating this locally, losing this file means Terraform loses track of your infrastructure.

## 3. The Terraform Workflow

The standard cycle for managing infrastructure:

| Command | Purpose |
| :--- | :--- |
| `terraform init` | **Initialize**. Downloads the specified providers (e.g., AzureRM) into a hidden `.terraform` folder. |
| `terraform validate` | **Check Syntax**. Verifies that your configuration is syntactically valid. |
| `terraform fmt` | **Format**. Automatically rewrites Terraform config files to a canonical format and style. |
| `terraform plan` | **Preview**. Shows a "Dry Run" of what Terraform *will* do against the real infrastructure. |
| `terraform apply` | **Execute**. Applies the changes to reach the desired state of the configuration. Requires confirmation (`yes`). |
| `terraform destroy` | **Cleanup**. Destroys the Terraform-managed infrastructure. |

## 4. Resource Management Behavior

*   **Immutable Properties**: Changing certain fields (like a Resource Group's location) cannot be done "in-place". Terraform will **destroy** the old resource and **create** a new one to apply the change.
*   **In-Place Updates**: Changing mutable properties (like Tags) updates the existing resource without deletion.
*   **Parallelism**: Terraform builds a dependency graph and creates non-dependent resources in parallel (default up to 10 threads) for speed.
