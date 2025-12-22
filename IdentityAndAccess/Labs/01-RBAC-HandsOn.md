# Practical Homework: Microsoft Entra ID + Azure RBAC (Hands-on)

## Objective
Create users, validate authentication vs authorization behavior, and implement least-privilege access to view and operate on a VM using custom role (JSON) at subscription or resource scope.

---

## Tasks

### Task 1: Create a Test User in Microsoft Entra ID
1. Go to **Azure Portal** -> **Microsoft Entra ID** -> **Users** -> **New user**.
2. Create a user (example):
   - **User name**: `ops-vm-operator`
   - **Name**: `Ops VM Operator`
3. Create a temporary password.
4. Save these details in your notes:
   - User Principal Name (UPN)
   - Temporary password
   - Tenant default domain (e.g., `yourtenant.onmicrosoft.com`)
   > **Submission proof**: Screenshot of the created user overview page (UPN visible).

### Task 2: Demonstrate Authentication vs Authorization
1. Open a new browser window (**Incognito/Private**).
2. Sign in to `portal.azure.com` using the new user credentials from Task 1.
3. Observe what the user can see/do initially (usually nothing useful, or prompts for trial).
4. Write 3 lines in your notes:
   - What authentication means (1 line)
   - What authorization means (1 line)
   - What happened after login with the new user (1 line)
   > **Submission proof**: Screenshot showing the user login succeeded but access is restricted (any "no access / no subscriptions / need permission" view).

### Task 3: Create a Resource Group + VM (Using Your Admin Account)
1. Using your main/admin account:
2. Create **Resource Group**: `rg-entra-rbac-lab`
3. Create **Linux VM**: `vm-rbac-lab` (basic size and settings are fine)
4. Confirm the VM is running.
   > **Submission proof**: Screenshot of VM Overview page (VM name + RG visible).

### Task 4: Assign ONLY "Reader" Role and Validate Visibility
1. Go to **Resource Group** -> **Access control (IAM)** -> **Add role assignment**.
2. Assign role:
   - **Role**: `Reader`
   - **Member**: `ops-vm-operator`
   - **Scope**: Resource Group (`rg-entra-rbac-lab`)
3. Log in again as the test user (or refresh) and verify:
   - VM is visible.
   - The user still cannot create/delete resources.
   > **Submission proof**: 
   > - Screenshot of Reader role assignment (role + user + scope visible)
   > - Screenshot from test user showing VM is visible

### Task 5: Create a Custom Role via JSON for VM Start/Stop/Restart (Least Privilege)
You will create a custom role in Azure RBAC (subscription or resource group scope).

#### 5A) Prepare Role Definition (JSON)
1. **Get your Subscription ID**:
   Run this command in Cloud Shell to see your ID:
   ```bash
   az account show --query id -o tsv
   ```
   *Copy this ID, you will need it in the next step.*

2. Create a file named `StartStopRestartVMRole.json`.
3. Use the template below, but **YOU MUST REPLACE** `<SUBSCRIPTION_ID>` with the actual ID you just copied.

```json
{
  "Name": "Start Stop Restart VM Operator",
  "IsCustom": true,
  "Description": "Can start, stop(deallocate) and restart virtual machines.",
  "Actions": [
    "Microsoft.Compute/virtualMachines/start/action",
    "Microsoft.Compute/virtualMachines/restart/action",
    "Microsoft.Compute/virtualMachines/deallocate/action",
    "Microsoft.Compute/virtualMachines/read"
  ],
  "NotActions": [],
  "DataActions": [],
  "NotDataActions": [],
  "AssignableScopes": [
    "/subscriptions/<PUT_YOUR_SUBSCRIPTION_ID_HERE>/resourceGroups/rg-entra-rbac-lab"
  ]
}
```

#### 5B) Create the Role
**Option 1 (Recommended): Azure Cloud Shell (Bash)**
Run:
```bash
az role definition create --role-definition StartStopRestartVMRole.json
```

**Option 2:** If Cloud Shell isn't available, use local Azure CLI (only if already configured).

> **Submission proof**: Screenshot of the command output OR Azure Portal showing the custom role exists.

### Task 6: Assign the Custom Role and Test VM Control
1. Go to **Resource Group** -> **Access control (IAM)**.
2. Add role assignment:
   - **Role**: `Start Stop Restart VM Operator` (your custom role)
   - **Member**: `ops-vm-operator`
   - **Scope**: `rg-entra-rbac-lab`
3. Login as test user and try from VM page:
   - Start
   - Restart
   - Stop (Deallocate)
4. Expected result:
   - User can perform start/stop/restart.
   - User cannot delete VM.
   - User cannot create new VM.
   > **Submission proof**: 
   > - Screenshot of role assignment
   > - Screenshot showing successful stop/deallocate OR restart action by the test user

### Task 7: Granular Scope Challenge (Optional but Recommended)
Repeat Task 6 but scope the permission to only one VM instead of the full RG.
**Hint**:
- Assign the custom role at VM resource level (VM -> IAM)
- Or update `AssignableScopes` to the VM resource ID (advanced)

> **Submission proof**: Screenshot of role assignment at VM scope.

### Task 8: Bulk User Creation (Template Exercise)
1. Go to **Entra ID** -> **Users** -> **Bulk operations** -> **Bulk create**.
2. Download the template.
3. Fill at least 3 users with valid formatting.
4. Validate the file (upload step) but do not create if you want to avoid clutter OR create and delete them if you prefer.
5. In your notes answer:
   - What kind of error happens if username format is wrong?
   - What kind of error happens if template version/format is incorrect?
   > **Submission proof**: 
   > - Screenshot of the filled template (hide passwords if present)
   > - Screenshot of upload/validation result
