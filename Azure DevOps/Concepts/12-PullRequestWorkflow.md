# Pull Request Workflow & Code Reviews

The Pull Request (PR) workflow is the standard method for merging code safely in a collaborative environment. It ensures code quality through mandatory reviews and checks.

## The PR Lifecycle

1.  **Feature Branch**:
    *   Developers never work directly on the `prod` or `main` branch.
    *   Create a feature branch (e.g., `dev` or `feature/login`) from the production branch.
    *   Make commits to this feature branch.

2.  **Create Pull Request**:
    *   On GitHub/Azure DevOps, navigate to **Pull Requests > New Pull Request**.
    *   **Source**: Your feature branch (`dev`).
    *   **Target**: The production branch (`prod`).
    *   Direction: `dev` -> `prod`.

3.  **Code Review**:
    *   **Add Reviewers**: Assign 3-5 team members to review the code.
    *   **Review Process**: Reviewers examine the changes (diffs), leave comments, request changes, or approve.

4.  **Branch Policies**:
    *   Organizations set policies that block merging until criteria are met.
    *   **Minimum Approvals**: E.g., at least 2 approvals required.
    *   **Build Checks**: CI pipelines must pass.
    *   **Resolution**: All comments must be resolved.

5.  **Merge**:
    *   Once all checks pass and approvals are granted, the "Merge" button becomes active.
    *   Click **Merge pull request** to integrate changes into the production branch.

## Azure DevOps Repos vs. GitHub

While the core Git concepts are identical, Azure DevOps adds enterprise focused integrations:

*   **Work Items**: Commits and PRs can be linked to Work Items (Issues/Tickets) for end-to-end traceability.
*   **Default Branch**: You can configure any branch (like `dev`) to be the default for new clones and PRs.
*   **Enterprise Management**: Both platforms offer robust user management and branch protection rules, but Azure Repos is tightly integrated with Azure Boards and Pipelines.

## Command Line Proficiency

While GUIs exist, proficiency with the Git command line is mandatory for DevOps Engineers.
*   **Automation**: CI/CD pipelines run git commands, not GUI clicks.
*   **Troubleshooting**: Complex issues often require command-line tools to resolve.
*   **Universality**: The command line works uniformly across all environments (Windows, Linux, macOS).
