# Lab 04: SonarQube Practical Homework

**Topic**: Static Code Analysis with SonarQube  
**Mode**: Individual  
**Objective**: Perform static code analysis on a Java project using SonarQube Cloud and Maven.

---

## Task 1: SonarQube Project Setup

1.  Log in to [SonarQube Cloud](https://sonarcloud.io/).
2.  Create a new project manually.
3.  During creation:
    *   Select your **Organization name**.
    *   Generate a unique **Project Key** (e.g., `my-java-scan-project`).
4.  Generate a SonarQube Token for authentication:
    *   Go to **Account Security** -> **Generate Token**.
    *   Name it (e.g., `HomeworkScan`).
    2d6c3d8ec8219835f05cd6c4e416b04a2a23f75f

> **Deliverables**:
> *   Screenshot of the **Project created** in SonarQube Cloud.
> *   Screenshot of the **Generated token** (mask the sensitive value).

---

## Task 2: Java & Maven Validation

Verify your local environment meets project requirements.

1.  Verify Java installation:
    ```bash
    java -version
    ```
3.  **If Java or Maven is missing**:
    *   **Java**: Install OpenJDK 17 or 21 (e.g., `sudo apt install openjdk-21-jdk -y` on Linux).
    *   **Maven**: Install via package manager (`sudo apt install maven`) or [Download Manual](https://maven.apache.org/download.cgi).
    *   *Refer to [Lab 01](../Labs/01-MavenBuildAndDeploy.md) for detailed steps.*

4.  Verify Maven installation:
    ```bash
    mvn -version
    ```

> **Deliverables**:
> *   Screenshot of both command outputs.
> *   **Written**: Does the installed Java version align with the project's `pom.xml` requirement? (Yes/No)

---

## Task 3: SonarQube Code Scan Using Maven

1.  Clone a sample Java Maven project (e.g., Spring Petclinic) or use an existing one.
2.  Navigate to the project root (where `pom.xml` exists).
3.  Run the SonarQube scan (Replace generic placeholders with your actual values):
    ```bash
    mvn verify sonar:sonar \
      -Dsonar.projectKey=<your-project-key> \
      -Dsonar.host.url=https://sonarcloud.io \
      -Dsonar.login=<your-token> \
      -Dsonar.organization=<your-org-name>
    ```

> **Deliverables**:
> *   Screenshot of **Command execution**.
> *   Screenshot of **Successful build** / scan completion message.
> *   Screenshot of **SonarQube dashboard** showing code scan results.

---

## Task 4: SonarQube Analysis Review

Analyze the results on the SonarQube dashboard.

1.  Identify the number of Issues in the following categories:
    *   **Security**
    *   **Reliability**
    *   **Maintainability**
2.  Check the **Quality Gate** status (Passed / Failed).

> **Deliverables**:
> *   **Short written summary (5–6 lines)** answering:
>     *   What type of issues were found?
>     *   Would this code be allowed to proceed to packaging in a real pipeline? Why?
