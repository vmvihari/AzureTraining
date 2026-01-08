# Git Advanced Operations

This document covers advanced Git operations including managing commit history with `reset`, handling work-in-progress with `stash`, and selective merging with `cherry-pick`.

## 1. Git Reset
The `git reset` command allows you to "undo" commits. It moves the `HEAD` pointer backward in the commit history. There are two main modes: Soft and Hard.

### Soft Reset (Default/Recommended)
Moves the commit history back but **preserves** your file changes in the staging/working area.
- **Command**: `git reset HEAD^` (or `git reset --soft HEAD^`)
- **Use Case**: You committed code but realized you need to make one more small change to it. You want to keep the work you've done.
- **Effect**:
  - The commit is removed from history.
  - Files remain in your working directory with the changes.
  - No data is lost.

### Hard Reset (Destructive)
Moves the commit history back and **deletes** all changes associated with that commit.
- **Command**: `git reset --hard HEAD^`
- **Use Case**: You want to completely discard the last commit and all its changes (e.g., you went down the wrong path entirely).
- **Effect**:
  - The commit is removed from history.
  - **Files are reverted** to the state of the previous commit.
  - **Data is permanently lost**.
- **⚠️ Warning**: Use with extreme caution.

---

## 2. Git Stash
`git stash` is used to temporarily save changes that you are not ready to commit yet, allowing you to switch branches with a clean working directory.

### Scenario
You are working on a feature in the `test` branch (files created/modified). Your manager asks for an urgent fix in `master`. You cannot switch to `master` because your uncommitted changes in `test` would carry over or block the switch.

### Workflow
1. **Sage your changes**: `git add .` (Files must be staged to be stashed efficiently).
2. **Stash changes**: `git stash`
   - This moves your changes to a temporary storage stack.
   - Your working directory is now clean (matches the last commit).
3. **Switch Branch**: `git switch master`
   - Perform your hotfix, commit, and push.
4. **Return to work**: `git switch test`
5. **Retrieve changes**: `git stash pop`
   - Applies the saved changes back to your working directory and removes them from the stash list.

### Key Commands
- `git stash`: Save changes.
- `git stash list`: View all stashed entries.
- `git stash pop`: Apply the latest stash and remove it from the list.
- `git stash apply`: Apply the latest stash but **keep** it in the list (useful if applying to multiple branches).

---

## 3. Git Cherry-Pick
`git cherry-pick` allows you to pick specific commits from one branch and apply them to another.

### Scenario
You have 3 commits in the `test` branch:
1. `Commit A`: Created `login.py` (Good, needed in production).
2. `Commit B`: Added debug logs to `login.py` (Testing only, do not want in production).
3. `Commit C`: Created `test_data.csv` (Testing only).

You only want to merge `Commit A` into `master`. A standard `git merge test` would bring all three.

### Workflow
1. **Identify Commit ID**: Run `git log` in the `test` branch and copy the ID of Commit A (e.g., `a1b2c3d4`).
2. **Switch to Target**: `git switch master`.
3. **Cherry-Pick**:
   ```bash
   git cherry-pick a1b2c3d4
   ```
4. **Result**: Only the changes from Commit A are applied to `master` as a new commit.

### Notes
- **Commit ID**: Minimum 8 characters recommended.
- **Content**: It applies exactly what was in that commit (and nothing else).
