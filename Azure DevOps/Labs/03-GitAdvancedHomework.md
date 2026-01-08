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
   ```bash
   mkdir git-homework
   cd git-homework
   git init
   ```
2. Create a file named `file56.txt`.
   ```bash
   touch file56.txt
   ```
3. Add the file to the staging area and commit it with a message.
   ```bash
   git add file56.txt
   git commit -m "Initial commit of file56"
   ```
4. Edit the file by adding some text.
   ```bash
   echo "This is some new text" >> file56.txt
   ```
5. Stage and commit the changes.
   ```bash
   git add .
   git commit -m "Added text to file56"
   ```
6. Verify the commit history using `git log`.
   ```bash
   git log --oneline
   ```
7. Roll back the latest commit using:
   ```bash
   git reset HEAD^
   ```
8. Check the file content and status.
   ```bash
   cat file56.txt
   git status
   ```

### Expected Outcome
- The latest commit should be removed from the commit history.
- The file content should still exist locally.
- The file should appear as **modified** and **unstaged**.

---

## Task 2: Git Reset Hard (Understanding Risk)

### Steps
1. Stage and commit the modified file again.
   ```bash
   git add .
   git commit -m "Restoring changes"
   ```
2. Verify commit history.
   ```bash
   git log --oneline
   ```
3. Run the following command:
   ```bash
   git reset --hard HEAD^
   ```
4. Check the file system and commit history.
   ```bash
   ls
   git status
   git log --oneline
   ```

### Expected Outcome
- The commit should be removed from history.
- File changes may be **permanently deleted**.
- Trainee should understand why this command is dangerous.

---

## Task 3: Branch Switching and File Visibility

### Steps
1. Create and switch to a new branch called `test`.
   ```bash
   git branch test
   git switch test
   ```
2. Create a new file `file57.txt` but **do not commit it**.
   ```bash
   touch file57.txt
   ```
3. Switch back to the `master` (or `main`) branch.
   ```bash
   git switch master
   ```
4. Observe the file visibility.
   ```bash
   ls
   # You should see file57.txt even though you are in master
   ```

### Expected Outcome
- The uncommitted file remains visible across branches.
- Trainee understands why uncommitted files must be managed manually.

---

## Task 4: Git Stash (Real-World Scenario)

### Scenario
You are working on the `test` branch. Your manager asks for an urgent fix in the `master` branch.

### Steps
1. In the `test` branch, modify or create multiple files.
   ```bash
   git switch test
   echo "Work in progress" > wip.txt
   ```
2. Stage all changes:
   ```bash
   git add .
   ```
3. Stash the changes:
   ```bash
   git stash
   # Working directory should now be clean
   ```
4. Switch to the `master` branch.
   ```bash
   git switch master
   ```
5. Create a file `hotfix.txt`, add content, commit it.
   ```bash
   echo "Urgent fix" > hotfix.txt
   git add .
   git commit -m "Applied hotfix"
   ```
6. Switch back to the `test` branch.
   ```bash
   git switch test
   ```
7. Retrieve the stashed changes:
   ```bash
   git stash pop
   # wip.txt should reappear
   ```

### Expected Outcome
- `master` branch remains clean.
- Work-in-progress changes are safely restored in `test`.

---

## Task 5: Git Stash Management

### Steps
1. Create and stash changes multiple times.
   ```bash
   echo "Stash 1" > stash1.txt
   git add .
   git stash
   echo "Stash 2" > stash2.txt
   git add .
   git stash
   ```
2. List all stashes:
   ```bash
   git stash list
   ```
3. Apply the latest stash without deleting it:
   ```bash
   git stash apply
   # To apply specific stash: git stash apply stash@{1}
   ```
4. Drop a stash manually.
   ```bash
   git stash drop
   # To drop specific stash: git stash drop stash@{0}
   ```

### Expected Outcome
- Trainee understands how to manage multiple stashes.

---

## Task 6: Git Cherry-Pick (Selective Commit Transfer)

### Steps
1. In the `test` branch:
   - **Commit 1**: Create `file58.txt` (empty).
     ```bash
     git switch test
     touch file58.txt
     git add .
     git commit -m "Create file58"
     ```
   - **Commit 2**: Add content to `file58.txt`.
     ```bash
     echo "Update" > file58.txt
     git add .
     git commit -m "Update file58"
     ```
   - **Commit 3**: Create another file `file59.txt`.
     ```bash
     touch file59.txt
     git add .
     git commit -m "Create file59"
     ```
2. View commit history and note commit IDs.
   ```bash
   git log --oneline
   # Copy the ID for "Create file58" (e.g., a1b2c3d)
   ```
3. Switch to the `master` branch.
   ```bash
   git switch master
   ```
4. Cherry-pick only the commit that created `file58.txt`:
   ```bash
   git cherry-pick <commit-id>
   ```
5. Verify files in `master`.
   ```bash
   ls
   # Should see file58.txt but NOT file59.txt or the updates to file58.txt (unless you cherry-picked those too)
   ```

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
