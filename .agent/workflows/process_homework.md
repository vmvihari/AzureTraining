---
description: Process a homework assignment to create a detailed lab document
---

1.  **Analyze the Homework Request**:
    *   Read the user-provided homework details/prompt carefully.
    *   Identify the main objective, specific tasks, constraints, and any specific commands mentioned.

2.  **Determine Lab Location**:
    *   Identify the subject area (e.g., Git, Azure, DevOps).
    *   Look for the corresponding `Labs` directory in the repository (e.g., `Azure DevOps/Labs`).
    *   *Heuristic*: It is usually in the same component directory as the most recent "Meeting Summary" work.
    *   Determine the next logical filename prefix (e.g., if `01-Git.md` exists, use `02-NewHomework.md`).

3.  **Draft Lab Documentation**:
    *   Create a new markdown file in the identified `Labs` folder.
    *   **Structure**:
        *   **Title**: Clear and descriptive.
        *   **Objective**: What the student will learn/accomplish.
        *   **Instructions**: Broken down into numbered, logical steps.
        *   **Commands**: Provide exact, copy-pasteable command blocks (e.g., ```bash). **Do not be vague.**
        *   **Verification**: Steps to verify the output is correct.
        *   **Troubleshooting**: (Optional) Common pitfalls.

4.  **Update Documentation**:
    *   Update the `README.md` in the parent directory to link to the new Lab file.

5.  **Review**:
    *   Notify the user and provide a link to the new lab file for review.
