# Homework: Git Local Workflow Practice

## Objective
Practice the complete Git local workflow (init → add → commit → modify → stage → commit → history) and submit it in a clean dashboard format.

## Task 1: Install and Verify Git
1.  **Install Git**: Install Git with default settings.
2.  **Verify Installation**: Open Git Bash and run:
    ```bash
    git --version
    git config --global user.name "Your Name"
    git config --global user.email "your@email.com"
    ```
    > **Submission Proof**: Command outputs (copy-paste OR clear screenshot).

## Task 2: Create a Local Repository
1.  **Create Directory**:
    ```bash
    mkdir git-homework
    cd git-homework
    ```
2.  **Create Files**:
    ```bash
    touch notes.txt tasks.txt
    ```
3.  **Initialize Git**:
    ```bash
    git init
    ```
4.  **Check Status**:
    ```bash
    git status
    ```
    > **Submission Proof**: Output of `git status` showing untracked files.

## Task 3: Staging Area Practice
1.  **Stage One File**:
    ```bash
    git add notes.txt
    git status
    ```
2.  **Stage Remaining File**:
    ```bash
    git add tasks.txt
    git status
    ```
    > **Submission Proof**: Output showing files moved from untracked → staged.

## Task 4: First Commit
1.  **Commit**:
    ```bash
    git commit -m "Initial commit with notes and tasks"
    ```
2.  **Verify History**:
    ```bash
    git log --oneline
    ```
    > **Submission Proof**: `git log --oneline` output.

## Task 5: Modify, Track, and Commit Again
1.  **Modify Files**:
    ```bash
    echo "Git staging practice" >> notes.txt
    echo "Task 1: Learn git add/commit" >> tasks.txt
    ```
2.  **Check Changes**:
    ```bash
    git status
    git diff
    ```
3.  **Stage and Commit First File**:
    ```bash
    git add notes.txt
    git commit -m "Update notes"
    ```
4.  **Stage and Commit Second File**:
    ```bash
    git add tasks.txt
    git commit -m "Update tasks"
    ```
    > **Submission Proof**:
    > - `git diff` output (or screenshot)
    > - `git log --oneline` showing 3 commits total

## Task 6: Verify Tracking and Understanding
Run and capture outputs:
```bash
git status # Should show clean working tree
git log # Full log
```
> **Submission Proof**: Outputs of both commands.
