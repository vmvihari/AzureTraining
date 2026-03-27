# Lab 04: Git Repository Management & Workflow

## Objective
Master the Git remote workflow, including creating repositories, pushing code to GitHub, managing branches and Pull Requests, and using tags for releases.

## Tasks

### Task 1: Repository Creation (Method 1 - Empty)
1.  **GitHub**: Create a new **Public** repository named `git-lab-method1`. Do **not** initialize with README/license.
2.  **Local**:
    ```bash
    # Create directory and file
    mkdir git-lab-method1
    cd git-lab-method1
    echo "<h1>Method 1 Repo</h1>" > index.html
    
    # Git commands
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M prod
    
    # Link and Push (Replace URL with your repo URL)
    git remote add origin https://github.com/<YourUsername>/git-lab-method1.git
    git push -u origin prod
    ```

### Task 2: Repository Creation (Method 2 - Existing Files)
1.  **Local**:
    ```bash
    # Setup existing project simulation
    mkdir git-lab-method2
    cd git-lab-method2
    touch app.py requirements.txt notes.txt
    
    # Git commands
    git init
    git add .
    git commit -m "Initial commit of existing app"
    ```
2.  **GitHub**: Create a new repository named `git-lab-method2`.
3.  **Local**:
    ```bash
    git branch -M prod
    git remote add origin https://github.com/<YourUsername>/git-lab-method2.git
    git push -u origin prod
    ```

### Task 3: README & Markdown Documentation
1.  **Create README**:
    In the `git-lab-method2` folder, create a `README.md` with:
    *   One Main Heading (`#`)
    *   One Subheading (`##`)
    *   A code block (` ``` `)
    *   A short description.
    
    **Command Line Challenge**: Use `echo` for this.
    ```bash
    echo "# Project Alpha" > README.md
    echo "## Setup" >> README.md
    echo "\`\`\`bash" >> README.md
    echo "pip install -r requirements.txt" >> README.md
    echo "\`\`\`" >> README.md
    echo "This is a demo project." >> README.md
    ```
    *   *Note: `>` overwrites, `>>` appends.*

2.  **Commit and Push**:
    ```bash
    git add README.md
    git commit -m "Add documentation"
    git push
    ```

### Task 4: Branch & Pull Request
1.  **Create Dev Branch**:
    ```bash
    git checkout -b dev
    ```
2.  **Make a Change**:
    ```bash
    echo "New feature updates" >> notes.txt
    git add notes.txt
    git commit -m "Add feature notes"
    git push -u origin dev
    ```
3.  **Create Pull Request (GitHub UI)**:
    *   Go to your repository on GitHub.
    *   You should see a "Compare & pull request" button.
    *   Set **Base** to `prod` and **Compare** to `dev`.
    *   Add a reviewer (username) if available or assign yourself.
    *   Click **Create pull request**.

### Task 5: Tag Creation
1.  **Create a Tag (Locally)**:
    ```bash
    git checkout prod
    git tag release-1.0
    git push origin release-1.0
    ```
    *Alternatively, you can create a release in the GitHub UI under "Releases" -> "Draft a new release".*

## Submission
Provide the following:
1.  **Repository URLs**: Links to both method 1 and method 2 repos.
2.  **PR Screenshot**: Screenshot showing the active Pull Request.
3.  **Tag Screenshot**: Screenshot showing the `release-1.0` tag in GitHub.
