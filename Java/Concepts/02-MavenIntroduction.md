# Introduction to Apache Maven

**Apache Maven** is a build automation tool used primarily for Java projects. It addresses the challenges of managing large projects with hundreds of files and dependencies.

## 1. Why Maven?

| Without Maven | With Maven |
| :--- | :--- |
| Manually compile hundreds of files (`javac *.java`) | Single command (`mvn compile`) builds everything. |
| Manually download JARs and add to classpath. | Automatically downloads dependencies from repositories. |
| Manual folder structure creation. | Generates standard project structure. |
| Manual deployment steps. | Automates testing, packaging, and deployment. |

---

## 2. Maven Directory Structure

Maven enforces a standard directory structure (Convention over Configuration).

```text
my-app/
├── pom.xml              # Project Object Model (Configuration)
├── src/
│   ├── main/
│   │   ├── java/        # Source code
│   │   └── resources/   # Config files (properties, xml)
│   └── test/
│       ├── java/        # Unit tests
│       └── resources/   # Test config files
└── target/              # Compiled output (JARs/WARs go here)
```

---

## 3. The Build Lifecycle

Maven has a specific sequence of phases. Running a later phase executes all preceding phases.

1.  **`validate`**: Checks if the project is correct and all info is available.
2.  **`compile`**: Compiles the source code (`src/main/java`) into bytecode.
3.  **`test`**: Runs unit tests (`src/test/java`) using a framework like JUnit.
4.  **`package`**: Takes compiled code and packages it (e.g., `webapp.war`).
5.  **`verify`**: Runs integration tests.
6.  **`install`**: Installs the package into your **local repository** (`~/.m2`).
7.  **`deploy`**: Copies the final package to a **remote repository** (Nexus/JFrog) for sharing.

### Common Commands
```bash
mvn clean package  # Deletes target/ and rebuilds the package
mvn compile        # Only compiles
mvn test           # Compiles and runs tests
```

---

## 4. Transitive Dependencies

If your project depends on **Library A**, and Library A depends on **Library B**:
*   **Manual**: You must download both A and B.
*   **Maven**: You declare **A** in `pom.xml`. Maven automatically downloads **A** AND **B**.
