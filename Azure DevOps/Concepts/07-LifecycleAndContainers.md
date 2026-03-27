# DevOps Lifecycle and Containers

## The DevOps Lifecycle
The lifecycle involves several stages:
1.  **Planning**: Clarify requirements and technologies.
2.  **Pipeline**:
    -   **Build**: Compile code.
    -   **Test**: Run automated tests.
    -   **Scan**: Perform code quality and security scans.
    -   **Deploy**: Deploy artifacts.
3.  **Artifact Management**: Store outputs (zip, jar, war) in repositories like **Nexus** or **JFrog**.

## Containers vs. Virtual Machines
-   **Virtual Machines (VMs)**: Require a full Operating System (OS), making them heavier.
-   **Containers**: Lightweight; they only include the minimal OS libraries needed for the application.
    -   **Efficiency**: Faster to start and more efficient to run.
    -   **Deployment**: Packaged as images and deployed to platforms like **Kubernetes**.

## Curriculum Roadmap
The learning path covers:
1.  **Git**: Version Control.
2.  **Jenkins**: CI/CD.
3.  **Docker**: Containerization.
4.  **Kubernetes**: Container Orchestration.
5.  **Terraform**: Infrastructure as Code (creating 3-tier applications).
6.  **Azure DevOps**: Integrating all tools into pipelines.
