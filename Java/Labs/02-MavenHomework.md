# Lab 02: Maven Build and Deployment Homework (Session 48)

**Topic**: Java + Maven Build and Deployment using Tomcat

## Objective
By completing this homework, you will:
*   Understand Java compilation vs Maven build
*   Install and configure Maven (v3.9.12)
*   Build a specific Java web application (Spring Petclinic) using Maven
*   Deploy the resulting WAR file to Tomcat 9
*   Access the application from a browser

## Prerequisites
*   Linux VM (Ubuntu preferred)
*   Java JDK 17 or 21
*   Internet access
*   Git installed

---

## Task 1: Verify Java Installation

1.  Check Java version:
    ```bash
    java -version
    ```
2.  If Java is not installed, install JDK 21:
    ```bash
    sudo apt update
    sudo apt install openjdk-21-jdk -y
    ```
3.  Verify again:
    ```bash
    javac -version
    ```

---

## Task 2: Install Maven Manually

1.  Download Maven 3.9.12:
    ```bash
    wget https://dlcdn.apache.org/maven/maven-3/3.9.12/binaries/apache-maven-3.9.12-bin.tar.gz
    ```
2.  Extract the archive:
    ```bash
    tar -xvzf apache-maven-3.9.12-bin.tar.gz
    ```
3.  Rename the folder for simplicity:
    ```bash
    mv apache-maven-3.9.12 maven-3912
    ```
4.  Set Maven path (temporary):
    ```bash
    export PATH=$PATH:$HOME/maven-3912/bin
    ```
5.  Make the path permanent:
    ```bash
    # Append to .bashrc
    echo 'export PATH=$PATH:$HOME/maven-3912/bin' >> ~/.bashrc
    
    # Reload the file
    source ~/.bashrc
    ```
6.  Verify Maven installation:
    ```bash
    mvn -version
    ```

---

## Task 3: Clone a Sample Maven Java Web Project

1.  Clone the Spring Petclinic project:
    ```bash
    git clone https://github.com/spring-projects/spring-petclinic.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd spring-petclinic
    ```
3.  Confirm `pom.xml` exists:
    ```bash
    ls
    ```

---

## Task 4: Execute Maven Build Lifecycle

Run the following commands one by one and observe the output.

1.  **Validate** project structure:
    ```bash
    mvn validate
    ```
2.  **Compile** source code:
    ```bash
    mvn compile
    ```
3.  **Run tests**:
    ```bash
    mvn test
    ```
4.  **Package** the application (Creates JAR/WAR):
    ```bash
    mvn package
    ```
5.  **Verify** the Artifact:
    ```bash
    ls target
    # Look for the .jar or .war file confirmed in the output
    ```

---

## Task 5: Install and Configure Tomcat

1.  Download Tomcat 9:
    ```bash
    cd ~
    wget https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.96/bin/apache-tomcat-9.0.96.tar.gz
    ```
2.  Extract:
    ```bash
    tar -xvzf apache-tomcat-9.0.96.tar.gz
    ```
3.  Navigate to Tomcat bin directory:
    ```bash
    cd apache-tomcat-9.0.96/bin
    ```
4.  Start Tomcat:
    ```bash
    ./startup.sh
    ```
5.  **Azure NSG**: Ensure port **8080** is allowed in your Azure Network Security Group (Inbound rules).

---

## Task 6: Deploy to Tomcat

1.  Navigate to the webapps folder:
    ```bash
    cd ../webapps
    ```
2.  Copy the built artifact (Note: Petclinic usually builds a JAR, but if configured as WAR, copy it here):
    ```bash
    # Adjust path if needed
    cp ~/spring-petclinic/target/*.war . 
    # OR if it built a JAR and you want to run it directly: java -jar target/*.jar
    ```
    *> **Note**: Standard Tomcat deployment requires a WAR file. If the project built a JAR (common for Spring Boot), you might run it with `java -jar` instead of deploying to Tomcat. For this lab, ensure you are copying a valid WAR if using Tomcat.*

3.  Restart Tomcat (if deployed as WAR):
    ```bash
    cd ../bin
    ./shutdown.sh
    ./startup.sh
    ```

---

## Task 7: Access the Application

1.  Open your browser:
    ```text
    http://<VM-Public-IP>:8080/
    ```
    *(Note: If you deployed `petclinic.war`, the URL might be `http://<IP>:8080/petclinic`)*

2.  Confirm the application (Petclinic) loads successfully.

---

## Troubleshooting

### Error: "Web server failed to start. Port 8080 was already in use."
This happens if you try to run the application directly (e.g., `java -jar target/*.jar`) while the external Tomcat server (started in Task 5) is **already running**. Both use port 8080.

**Solution**:
1.  **Stop Tomcat** first:
    ```bash
    cd ~/apache-tomcat-9.0.96/bin
    ./shutdown.sh
    ```
2.  **OR** Run the app on a different port:
    ```bash
    java -jar target/*.jar --server.port=8081
    ```

3.  **Find and Kill** the process manually (if stuck):
    ```bash
    sudo lsof -i :8080
    # Note the PID (Process ID)
    kill -9 <PID>
    ```

---

## Submission Requirements

Please submit:
1.  Screenshot of `mvn package` success message.
2.  Screenshot of the WAR/Artifact file inside `webapps` or `target`.
3.  Screenshot of the application running in the browser.
4.  **Short explanation (3–4 lines)** answering:
    *   Why Maven is used instead of `javac`?
    *   What is the difference between GitHub and an Artifact Repository?
