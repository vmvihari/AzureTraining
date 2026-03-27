# Java Development Basics

Understanding the fundamentals of Java development, artifacts, and deployment is essential for setting up CI/CD pipelines.

## 1. Java Compilation Process

Unlike interpreted languages (like Python or JavaScript), Java is a **compiled** language.

1.  **Source Code (`.java`)**: The developer writes human-readable code.
2.  **Compilation (`javac`)**: The `javac` compiler translates source code into **bytecode**.
3.  **Bytecode (`.class`)**: Platform-independent binary format.
4.  **Execution (`java`)**: The Java Virtual Machine (JVM) runs the bytecode.

### Example
```bash
# Compile
javac HelloWorld.java
# Output: HelloWorld.class

# Run (do not include .class extension)
java HelloWorld
```

---

## 2. Software Development Process

Modern software development involves more than just writing code.

*   **IDE (Integrated Development Environment)**: Tools like **Eclipse**, **IntelliJ IDEA**, or VS Code. They manage file structures, syntax highlighting, and debugging.
*   **Dependencies**: Most projects rely on external libraries (e.g., Spring Boot, Log4j). Tools are needed to download these automatically.
*   **Testing**: Automated unit tests and security scans run before deployment.

---

## 3. Deployment Artifacts

When a Java project is built for deployment, it is packaged into an **Artifact**. The type of artifact depends on the application type.

| Artifact Type | Full Name | Use Case |
| :--- | :--- | :--- |
| **JAR** | Java Archive | Standalone applications, libraries, microservices (Spring Boot). |
| **WAR** | Web Archive | Web applications deployed to a container like **Apache Tomcat**. |
| **EAR** | Enterprise Archive | Large enterprise apps running on servers like JBoss/WildFly (less common now). |

> **Note**: For other languages:
> *   **Python/.NET**: Typically produce `.zip` files.
> *   **Docker**: Produces a **Container Image**.

---

## 4. Artifact Storage

*   **Source Code Repositories** (e.g., **GitHub**, Azure Repos): Store the human-readable *source code* (`.java`).
*   **Artifact Repositories** (e.g., **JFrog Artifactory**, **Sonatype Nexus**): Store the compiled binaries (`.jar`, `.war`).

**Rule**: Never commit large binary artifacts (JARs/WARs) to git. Store them in an artifact repository.
