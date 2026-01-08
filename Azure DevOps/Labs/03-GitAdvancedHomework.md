# Practical Git Homework – Commit Management, Reset, Stash, and Cherry-Pick

## Objective
This homework is designed to help trainees practice real-world Git operations covered in the session, including commit rollback, reset modes, branch switching, stashing, and selective commit transfer using cherry-pick.

---

## Prerequisites
- Git installed on the system
- Basic knowledge of terminal or Git Bash
- Any operating system (Windows, macOS, Linux)

---

## Task 1: Git Commit and Soft Reset (Safe Rollback)

### Steps
1. Create a new folder and initialize a Git repository.
2. Create a file named `file56.txt`.
3. Add the file to the staging area and commit it with a message.
4. Edit the file by adding some text.
5. Stage and commit the changes.
6. Verify the commit history using `git log`.
7. Roll back the latest commit using:
   ```bash
   git reset HEAD^
   ```
8. Check the file content and status.

### Expected Outcome
- The latest commit should be removed from the commit history.
- The file content should still exist locally.
- The file should appear as **modified** and **unstaged**.

---

## Task 2: Git Reset Hard (Understanding Risk)

### Steps
1. Stage and commit the modified file again.
2. Verify commit history.
3. Run the following command:
   ```bash
   git reset --hard HEAD^
   ```
4. Check the file system and commit history.

### Expected Outcome
- The commit should be removed from history.
- File changes may be **permanently deleted**.
- Trainee should understand why this command is dangerous.

---

## Task 3: Branch Switching and File Visibility

### Steps
1. Create and switch to a new branch called `test`.
2. Create a new file `file57.txt` but **do not commit it**.
3. Switch back to the `master` (or `main`) branch.
4. Observe the file visibility.

### Expected Outcome
- The uncommitted file remains visible across branches.
- Trainee understands why uncommitted files must be managed manually.

---

## Task 4: Git Stash (Real-World Scenario)

### Scenario
You are working on the `test` branch. Your manager asks for an urgent fix in the `master` branch.

### Steps
1. In the `test` branch, modify or create multiple files.
2. Stage all changes:
   ```bash
   git add .
   ```
3. Stash the changes:
   ```bash
   git stash
   ```
4. Switch to the `master` branch.
5. Create a file `hotfix.txt`, add content, commit it.
6. Switch back to the `test` branch.
7. Retrieve the stashed changes:
   ```bash
   git stash pop
   ```

### Expected Outcome
- `master` branch remains clean.
- Work-in-progress changes are safely restored in `test`.

---

## Task 5: Git Stash Management

### Steps
1. Create and stash changes multiple times.
2. List all stashes:
   ```bash
   git stash list
   ```
3. Apply the latest stash without deleting it:
   ```bash
   git stash apply
   ```
4. Drop a stash manually.

### Expected Outcome
- Trainee understands how to manage multiple stashes.

---

## Task 6: Git Cherry-Pick (Selective Commit Transfer)

### Steps
1. In the `test` branch:
   - **Commit 1**: Create `file58.txt` (empty).
   - **Commit 2**: Add content to `file58.txt`.
   - **Commit 3**: Create another file `file59.txt`.
2. View commit history and note commit IDs.
3. Switch to the `master` branch.
4. Cherry-pick only the commit that created `file58.txt`:
   ```bash
   git cherry-pick <commit-id>
   ```
5. Verify files in `master`.

### Expected Outcome
- Only the selected commit is merged.
- Subsequent edits and other files are excluded.

---

## Submission Instructions

Trainees must submit:

1. **Screenshot or copy of**:
   - `git log`
   - `git status`
2. **Commands used for**:
   - reset
   - stash
   - cherry-pick
3. **A short explanation** (2–3 lines) for:
   - Difference between `git reset` and `git reset --hard`
   - Why `git stash` is required before switching branches
   - Use case for `git cherry-pick`
