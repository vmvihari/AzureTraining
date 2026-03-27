# Git Workflow and Operations

## Distributed Version Control
Git follows a distributed model:
-   **Central Remote Repository**: Hosted on platforms like Azure DevOps Repos or GitHub.
-   **Local Repository**: A copy of the repository on each developer's machine.

### Typical Workflow
1.  **Pull**: Get the latest code from the remote repository.
2.  **Change**: Make changes locally.
3.  **Commit**: Save changes to the local history.
4.  **Push**: Send changes back to the remote repository.

> **Note**: A local repository is essentially a normal folder that has been initialized with Git tracking.

## Local Git Layers
The local workflow consists of three layers:
1.  **Working Directory**: Where you edit files.
2.  **Staging Area**: A temporary area where you select changes to be committed.
3.  **Local Repository**: The permanent local history where commits are stored.

### Sequence
`git add` moves changes from Working Directory -> Staging Area.
`git commit` moves changes from Staging Area -> Local Repository.

## Practical Demonstration

### Initialization
1.  Create a directory.
2.  Create some files (e.g., using `touch`).
3.  Run `git add .`. It will fail because the folder is not a Git repository.
4.  Run `git init` to initialize the repository.
5.  Run `git status`. It will show files as "untracked".

### Staging and Committing
1.  Run `git add .` to stage the files.
2.  Run `git status`. It will confirm files are staged.
3.  Run `git commit -m "message"` to permanently save changes.
    -   If `-m` is omitted, Git will open a text editor for the message.
4.  Run `git log` to view the commit history (author, date, message).

## Configuration
For first-time commits, you may need to set your identity:
```bash
git config user.name "Your Name"
git config user.email "your@email.com"
```
In professional environments, these should match your official organization details.

## Branching and Pushing
-   `git init` creates a default branch (often `master` or `main`).
-   Local commits are only visible to you until you **push** them to the remote repository.
-   Managers typically define branch strategies (dev, test, stage, prod) to manage the software lifecycle.
