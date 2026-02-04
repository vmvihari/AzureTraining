# Lab 03: SonarQube Setup

**Objective**: Set up a SonarCloud account and generate the necessary tokens for integration.

## 1. Sign up for SonarCloud

1.  Navigate to [https://sonarcloud.io/](https://sonarcloud.io/).
2.  Click **Login / Sign up**.
3.  Choose **GitHub**.
4.  Authorize SonarCloud to access your public GitHub repositories (this is safe and standard).

## 2. Create an Organization and Project

1.  Once logged in, click the **+ (Plus)** icon in the top right -> **Analyze new project**.
2.  **Create an organization**:
    *   Import from GitHub (select your username).
    *   It will ask for a key/name. Accept the default or verify it.
    *   Choose the **Free Plan**.
3.  **Create a Project**:
    *   Select the repository you want to analyze (e.g., `maven-hello-world` or `spring-petclinic`).
    *   If you don't see it, ensure you've synced your GitHub projects.
    *   Click **Set Up**.

## 3. Generate Analysis Token

To allow your VM (Maven) to talk to SonarCloud, you need a token.

1.  Go to **My Account** (Avatar top right) -> **Security**.
2.  **Generate Token**:
    *   Name: `AzureTrainingVM`
    *   Type: **User Token** (or Analysis Token).
    *   Click **Generate**.
3.  **Copy this token immediately**. You will not see it again.
    *   *Save it in Notepad for the next lab.*

## 4. Maven & JDK Compatibility

Before running the scan, ensure your environment is set up correctly.

*   **JDK Version**: Different projects require different JDK versions (e.g., 17 vs 21). Ensure your local development environment matches the project's requirement in `pom.xml`.
*   **Maven Lifecycle**: Running a higher-level command implies lower levels.
    *   Running `mvn package` automatically runs `validate`, `compile`, and `test`.

## 5. Running the Scan

The scan is triggered using the `mvn verify` command with the SonarQube plugin parameters.

**Command Syntax**:
```bash
mvn verify sonar:sonar \
  -Dsonar.projectKey=<YOUR_PROJECT_KEY> \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=<YOUR_TOKEN> \
  -Dsonar.organization=<YOUR_ORG_KEY>
```

*   **sonar.projectKey**: The unique ID you defined when creating the project in SonarQube.
*   **sonar.organization**: Your organization key (often your GitHub username).
*   **sonar.login**: The secret token generated in Step 3.

> [!NOTE]
> In a professional setting, **DevOps Engineers** handle the pipeline configuration, while **Developers** are responsible for fixing the issues identified by the scan. Setup like project creation and token generation is typically a one-time activity.

