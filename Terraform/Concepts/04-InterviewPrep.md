# Interview Preparation & Real-World Expectations

## 1. The Environment: "Notepad Coding"
In many technical interviews, you will **not** have access to your usual tools:
*   **No VS Code Extensions**: IntelliSense, Autocomplete, and Copilot are often disabled or unavailable.
*   **Plain Text**: You might be asked to write HCL code in Notepad, a whiteboard, or a simple browser editor.
*   **Why?**: Interviewers want to test your understanding of the *structure* and *core concepts*, not your ability to hit Tab.

## 2. What to Memorize vs. What to Reference
You do **not** need to memorize every single argument of every resource.

### MUST KNOW (Core Concepts)
*   **Syntax Structure**: `resource "type" "name" {Key = Value}`.
*   **Meta-Arguments**: How to use `count`, `for_each`, `lifecycle`.
*   **State commands**: `terraform init`, `plan`, `apply`, `destroy`, `fmt`.
*   **Data Types**: Strings, Lists, Maps, and how to access them (`var.list[0]`, `var.map["key"]`).

### OK TO REFERENCE (Documentation)
*   **Specific obscure arguments**: e.g., enabling specialized strict validation logic on a specific resource.
*   **List of all functions**: You are not expected to know every math or string function (like `sha256` or `pathexpand`), just the common ones.

## 3. AI Tools in the Workplace
*   **Security Restrictions**: Many large organizations block tools like GitHub Copilot to prevent proprietary code from leaking.
*   **Reliance Risk**: If you rely 100% on AI to write your code, you will fail when debugging complex state issues or circular dependencies. Use AI as an *accelerator*, not a crutch.
