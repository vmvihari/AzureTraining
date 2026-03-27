# Git Repository Security & Production Strategy

This document covers essential security practices for Git repositories and the strategy of using tags for production deployments.

## Repository Security

### Visibility
*   **Public**: Visible to everyone.
*   **Private**: Restricted access. You can change a repository's visibility in GitHub under **Settings > Change Visibility**.

### SSH Key Authentication
For private repositories, SSH keys provide a secure way to authenticate without entering passwords.

1.  **Generate Keys**:
    Run the following command in your terminal (Git Bash or PowerShell):
    ```bash
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    ```
    *   This generates a public key (ending in `.pub`) and a private key.
    *   **Important**: The private key stays on your local machine. Never share it.

2.  **Configure GitHub**:
    *   Copy the contents of the public key file (`.pub`).
    *   Go to your GitHub Repository > **Settings** > **Deploy Keys**.
    *   Add the new key.

### Secrets & Webhooks
*   **GitHub Actions Secrets**: Store sensitive data (like Azure credentials) securely in **Settings > Secrets and variables**. These are used by CI/CD pipelines to connect to cloud providers.
*   **Webhooks**: Configure webhooks to automatically trigger actions (like starting a pipeline) whenever code is pushed to the repository.

---

## Tags vs. Branches for Production

A critical best practice for production deployments is to use **Tags** instead of Branches.

### The Problem with Branches
*   **Mutability**: Branches (even `production` or `main`) are mutable. Developers can potentially push changes directly to them, bypassing reviews or introducing last-minute unverified fixes.
*   **Risk**: Deploying from a branch means the code state could change between testing and deployment.

### The Solution: Immutable Tags
*   **Immutability**: Tags are specific points in history that cannot be changed. Once a tag `v1.0` is created, it always points to the exact same commit.
*   **Workflow**:
    1.  Development is done on feature branches.
    2.  Code is merged to the main branch after review.
    3.  A **Tag** is created from the main branch (e.g., via GitHub **Releases > Create new release**).
    4.  The production deployment pipeline is triggered from the **Tag**, ensuring the exact approved code is deployed.
*   **Policy**: Many organizations strictly enforce "Deploy from Tag" policies to ensure integrity.
