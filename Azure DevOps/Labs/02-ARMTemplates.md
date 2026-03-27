# Practical Homework: ARM Templates (Process Only)

## Objective
This exercise focuses on the **process** of creating, exporting, and deploying ARM templates. You will not be writing code from scratch but will learn how to generate and reuse templates from existing resources.

## Task 1: Set up your Azure Workspace
1.  **Sign in**: Log in to the Azure Portal.
2.  **Resource Group**: Create or select a dedicated Resource Group for this homework.
3.  **Region**: Choose one Azure region and use it consistently.

## Task 2: Create a Baseline VM
Create a Linux VM in the portal to serve as your template source.
-   **Size**: Select a low-cost VM size.
-   **Auth**: SSH key or password.
-   **Networking**: Keep default settings (VNet, Subnet, NSG).
-   **Public IP**: Enabled (for testing).
-   **Tags**:
    -   `Environment = Dev`
    -   `Owner = YourName`
    -   `AutoShutdown = Yes`
    -   `Project = ARM-Practice`

## Task 3: Export the ARM Template
1.  Open the VM resource you just created.
2.  Select **Export template**.
3.  Download and save the files:
    -   `template.json`
    -   `parameters.json`
    > **Deliverable**: Save both files in a folder named `ARM-Homework`.

## Task 4: Review Template and Parameters
Open the downloaded files and analyze them.

### template.json
-   Identify resources (VM, NIC, NSG, Public IP, VNet/Subnet, disks).
-   Locate your tags.
-   Identify dependencies (e.g., VM depends on NIC).

### parameters.json
-   Identify parameterized values (VM name, admin username, size, etc.).

> **Deliverable**: Write 8–10 bullet points listing:
> - Resources created by the template.
> - Key parameters found.
> - Any hard-coded values noticed.

## Task 5: Plan for Reusability
Decide what should be flexible for future deployments (without editing code yet).
-   **VM Name**: To allow multiple VM deployments.
-   **VM Size**: For right-sizing.
-   **Admin Username**: For flexibility.
-   **Tags**: To enforce governance.
-   **Networking**: Optional, depending on reuse strategy.

> **Deliverable**: Create a short list with:
> - Field Name
> - Why it should be parameterized
> - Example values

## Task 6: Deploy the ARM Template
Use one of the following methods to deploy:
1.  **Azure Portal**: "Deploy a custom template".
2.  **Azure CLI**: Resource group deployment.

**Requirements**:
-   Change the **VM Name**.
-   Change or add a **Tag** (e.g., `CostCenter = Training`).

> **Deliverable**: Note the deployment status (Succeeded) and the final VM name.

## Task 7: Validate Creation
Verify the new resources in the Resource Group:
-   [ ] Virtual machine is created and running.
-   [ ] Network interface exists and is attached.
-   [ ] Network security group exists and rules are present.
-   [ ] Public IP exists (if enabled).
-   [ ] Virtual network and subnet exist (or were reused).
-   [ ] Tags are present on the VM.

> **Deliverable**: A checklist with each item marked as Pass/Fail.

## Task 8: Change Request Simulation
Assume a change request comes in (e.g., Increase OS disk size, Change VM SKU, or Remove Public IP).

**Task**:
1.  Identify where the change would be made (template vs parameters).
2.  Predict impact (update vs recreate).
3.  List risks (downtime, dependency conflicts).

> **Deliverable**: 6–10 lines describing:
> - The chosen change request.
> - Where you would apply the change.
> - Expected impact and risk.
