# Introduction to SonarQube

**SonarQube** is a code quality assurance tool that integrates into your DevOps pipeline to analyze source code for bugs, vulnerabilities, and code smells.

## 1. Code Quality vs. Compilation

It is important to distinguish between *compilation errors* and *code quality*.

*   **Compiler (Maven/Javac)**: Checks **syntax**. "Does the code follow the rules of the language?" If yes, it builds successfully.
*   **SonarQube**: Checks **quality and maintainability**. "Is the code written efficiently and securely?"

### The "Cost of Bad Code" Example
A poorly written application might work functionality-wise (it compiles), but it might be inefficient.
*   **Scenario**: An overly complex loop or memory leak executes thousands of unnecessary operations.
*   **Impact**:
    *   To run this inefficient app, you might need an **8GB RAM / 8 CPU** Virtual Machine (~$200/month).
    *   If the code were optimized, it could run on a **1GB RAM / 1 CPU** VM (~$10/month).
*   **Conclusion**: Poor code quality directly increases infrastructure costs.

## 2. Architecture

SonarQube has a few key components:

1.  **SonarQube Server**: The central server that processes reports and displays the dashboard. We will use **SonarCloud.io** (the cloud verison) for labs.
2.  **Database**: Managed by the server (YOU do not manage this in SonarCloud). Stores the history of code quality.
3.  **Scanner**: A small utility installed on your Build Server (Virtual Machine). It scans the code and sends the report to the Server.

## 3. Quality Gates

A **Quality Gate** is a set of conditions the code must meet to be considered "Pass".
*   *Example Rule*: "New code must not have any critical vulnerabilities."
*   *Example Rule*: "Code coverage (testing) must be at least 80%."

If the pipeline fails the Quality Gate, the software is rejected (deployment stops).
