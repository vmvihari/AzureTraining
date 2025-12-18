# Hosted Parallelism Grant for Azure DevOps

## Issue: No Hosted Parallelism
A common error encountered is: "no hosted parallelism has been purchased or granted." This prevents pipelines from running on Microsoft-hosted agents.

## Resolution
To resolve this, you must request a free hosted parallelism grant.

### Steps:
1.  **Fill out the Microsoft Form**: Search for the official request form for Azure DevOps Parallelism Grant.
2.  **Form Details**:
    -   **Name/Email**: Use your correct name and email ID.
    -   **Organization URL**: Enter the correct Azure DevOps organization URL (e.g., `https://dev.azure.com/yourorg`).
    -   **Project Visibility**: Choose **Private** projects.
3.  **Submission**: Submit the form.

### Verification
-   **Activation Time**: It typically takes 2-3 business days, but sometimes happens sooner.
-   **Confirmation**: Watch for a confirmation email.
-   **Test**: Re-run the pipeline the next day to verify if the error is resolved.
-   **Quota**: This typically enables 1800 minutes of free hosted parallelism.
