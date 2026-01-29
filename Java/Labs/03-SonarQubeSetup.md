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
