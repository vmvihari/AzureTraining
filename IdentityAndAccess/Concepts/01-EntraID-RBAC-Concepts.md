# Identity and Access Concepts

## Authentication vs Authorization

One of the most fundamental concepts in security is the difference between **Authentication** and **Authorization**:

- **Authentication (AuthN)**: The process of verifying *who you are*. It confirms your identity (e.g., logging in with a username and password, MFA).
- **Authorization (AuthZ)**: The process of determining *what you can do*. It typically happens after authentication and decides which resources you can access and what actions you can perform on them.

## Microsoft Entra ID (formerly Azure AD)

Microsoft Entra ID is a cloud-based identity and access management service. It serves as the directory for your tenant and handles:
- **User & Group Management**: Creating and managing user identities and groups.
- **Authentication**: Verifying user identities (Sign-in).
- **Application Access**: Managing access to applications.

## Azure Role-Based Access Control (RBAC)

Azure RBAC is an authorization system built on Azure Resource Manager that provides fine-grained access management of Azure resources.

### Key Components of RBAC

1.  **Security Principal**: The "who" (User, Group, Service Principal, or Managed Identity).
2.  **Role Definition**: The "what" (A collection of permissions, e.g., Read, Write, Delete).
    - **Actions**: Operations allowed.
    - **NotActions**: Operations explicitly denied (subtracted from Actions).
3.  **Scope**: The "where" (The level at which the access applies).
    - Management Group
    - Subscription
    - Resource Group
    - Resource

### Least Privilege Principle

The principle of **Least Privilege** states that users should only be granted the minimum level of access necessary to perform their job functions. This reduces the risk of accidental or malicious damage.

For example, if a user needs to restart a VM, they should not be given the "Contributor" role (which allows creating/deleting resources). Instead, they should be given a custom role with only the `Microsoft.Compute/virtualMachines/restart/action` permission.
