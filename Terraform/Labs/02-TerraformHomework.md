# Lab 02: Terraform Basics Homework

**Topic**: Terraform Infrastructure as Code  
**Mode**: Individual  
**Objective**: Use Terraform to create and manage Azure infrastructure.

---

## Task 1: Terraform Installation Verification

1.  Verify Terraform installation:
    ```powershell
    terraform -version
    ```
2.  Verify Azure CLI login:
    ```powershell
    az login --use-device-code
    ```

> **Deliverables**:
> *   Screenshot of **Terraform version**.
> *   Screenshot confirming **Azure login success**.

---

## Task 2: Create Azure Resource Group Using Terraform

1.  Create a new directory named `terraform-rg`.
2.  Create a file named `main.tf`.
3.  Add the **Azure RM provider block** and a **Resource block** to create a Resource Group:
    *   **Location**: `East US` or `Central India`.
4.  Run the lifecycle commands:
    ```powershell
    terraform init
    terraform validate
    terraform plan
    terraform apply
    ```
    *(Type `yes` to confirm apply)*

> **Deliverables**:
> *   Screenshots of `terraform init`, `terraform plan`, and `terraform apply` output.
> *   **Azure Portal screenshot** showing the created Resource Group.

---

## Task 3: Modify and Observe Terraform Behavior

1.  **Modify** the resource group *name* in your `main.tf` code.
2.  Run Plan:
    ```powershell
    terraform plan
    ```
3.  **Observe**: Does it plan to update in-place or destroy and recreate?
4.  **Add Tags**: Add a tag block to your resource (e.g., `tags = { Environment = "Dev" }`).
5.  Run Apply:
    ```powershell
    terraform apply
    ```

> **Deliverables**:
> *   Screenshot of `terraform plan` showing **destroy/create** behavior (steps 1-3).
> *   Screenshot showing **in-place update** for tags (steps 4-5).
> *   **Azure Portal screenshot** with verify tags applied.

---

## Task 4: Terraform Cleanup

1.  Destroy all resources to avoid costs:
    ```powershell
    terraform destroy
    ```

> **Deliverables**:
> *   Screenshot confirming **successful destroy**.
> *   Confirmation that the resource group **no longer exists** in Azure.
