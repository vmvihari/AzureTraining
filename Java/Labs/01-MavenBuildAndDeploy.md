# Lab 01: Maven Build Lifecycle and Deployment

**Objective**: Manually install Maven, build a Java application from source, and deploy it to a hosted Tomcat server.

## Prerequisites
*   Ubuntu Virtual Machine (or WSL)
*   Sudo privileges

---

## Task 1: Install Java (JDK) and Maven

1.  **Update packages**:
    ```bash
    sudo apt update
    ```
2.  **Install JDK 21**:
    ```bash
    sudo apt install openjdk-21-jdk -y
    java -version
    ```
3.  **Download Maven**:
    ```bash
    cd /opt
    sudo wget https://dlcdn.apache.org/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.tar.gz
    ```
    *(Note: Check [maven.apache.org](https://maven.apache.org/download.cgi) for the latest version link)*
4.  **Extract and Configure**:
    ```bash
    sudo tar -xvzf apache-maven-*.tar.gz
    sudo mv apache-maven-3.9.6 maven
    ```
5.  **Set Environment Variables**:
    ```bash
    export PATH=$PATH:/opt/maven/bin
    # To make permanent: echo 'export PATH=$PATH:/opt/maven/bin' >> ~/.bashrc
    ```
6.  **Verify**:
    ```bash
    mvn -version
    ```

---

## Task 2: Build a Java Project

1.  **Clone the Repository**:
    ```bash
    cd ~
    git clone https://github.com/Azure-Samples/maven-hello-world.git
    cd maven-hello-world
    ```
2.  **Run Build Phases**:
    ```bash
    # Check structure
    mvn validate

    # Compile source code
    mvn compile

    # Package (Creates WAR file)
    mvn package
    ```
3.  **Verify Output**:
    ```bash
    ls target/
    # You should see a .war file (e.g., helloworld.war)
    ```

---

## Task 3: Deploy to Tomcat

1.  **Install Tomcat**:
    ```bash
    cd /opt
    # Download Tomcat 9 (Adjust version as needed)
    sudo wget https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.85/bin/apache-tomcat-9.0.85.tar.gz
    sudo tar -xvzf apache-tomcat-*.tar.gz
    sudo mv apache-tomcat-9.0.85 tomcat
    ```
2.  **Start Tomcat**:
    ```bash
    sudo sh /opt/tomcat/bin/startup.sh
    ```
3.  **Deploy Application**:
    Copy the WAR file generated in Task 2 to Tomcat's webapps folder.
    ```bash
    # Assuming you are in the project folder
    sudo cp target/*.war /opt/tomcat/webapps/app.war
    ```
4.  **Access Application**:
    *   Open Port 8080 in your VM's Security Group (Network SG).
    *   Browser: `http://<VM-Public-IP>:8080/app`
