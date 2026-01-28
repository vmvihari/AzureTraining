# Lab 02: Docker Installation and Management Homework

## Objective
In this lab, you will perform a comprehensive hands-on practice with Docker on a Linux VM. You will cover installation, permission management, data persistence (Volumes), and custom image creation (Dockerfiles).

## Prerequisites
- An active Azure Subscription.
- A terminal (PowerShell, Bash, or Azure Cloud Shell).

---

## Task 1: Install Docker on Linux

1.  **Launch an Ubuntu Linux VM** in Azure.
2.  **Log in via SSH**: `ssh azureuser@<VM-Public-IP>`
3.  **Update and Install**:
    ```bash
    sudo apt update
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    ```
4.  **Verify**: `sudo docker --version`

---

## Task 2: Fix Docker Permission Issue

1.  **Grant Permissions**:
    ```bash
    sudo usermod -aG docker $USER
    newgrp docker
    ```
2.  **Verify**: `docker ps` (Should run without `sudo`).

---

## Task 3: Explore Docker System Commands

1.  **Disk Usage**: `docker system df`
2.  **System Info**: `docker info`
3.  **Events**: Open a second terminal, SSH in, and run `docker events`. Keep it open to watch the next steps.

---

## Task 4: Basic Container Operations

1.  **Run Nginx**:
    ```bash
    docker run -d --name basic-web nginx
    ```
2.  **View Logs**: `docker logs basic-web`
3.  **Stop and Start**:
    ```bash
    docker stop basic-web
    docker start basic-web
    ```

---

## Task 5: Port Binding and Azure Networking

1.  **Remove previous container**: `docker rm -f basic-web`
2.  **Run with Port Mapping**:
    ```bash
    docker run -d -p 8080:80 --name public-web nginx
    ```
3.  **Azure Configuration**:
    *   Go to **Azure Portal > VM > Networking**.
    *   Add Inbound Rule: Port **8080**, Allow.
4.  **Test**: Visit `http://<VM-Public-IP>:8080` in your browser.

---

## Task 6: Working with Named Volumes (Persistence)

1.  **Create Volume**:
    ```bash
    docker volume create my-data
    ```
2.  **Mount to Nginx**:
    ```bash
    docker run -d -p 8081:80 -v my-data:/usr/share/nginx/html --name vol-web nginx
    ```
    *(Remember to open port 8081 in Azure if testing externally)*
3.  **Concept**: Even if you delete `vol-web`, the data in `my-data` persists.

---

## Task 7: Working with Bind Volumes (Development)

1.  **Setup Local Directory**:
    ```bash
    mkdir ~/my-site
    echo "<h1>Hello from Bind Mount</h1>" > ~/my-site/index.html
    ```
2.  **Mount Local Folder**:
    ```bash
    docker run -d -p 8082:80 -v ~/my-site:/usr/share/nginx/html --name bind-web nginx
    ```
3.  **Live Update**:
    *   Edit `~/my-site/index.html` locally.
    *   Curl or refresh `localhost:8082`.
    *   Observation: Changes appear instantly without rebuilding.

---

## Task 8: Create a Dockerfile

1.  **Setup Build Folder**:
    ```bash
    mkdir ~/custom-image
    cd ~/custom-image
    ```
2.  **Create Dockerfile**:
    ```bash
    nano Dockerfile
    ```
    Content:
    ```dockerfile
    FROM nginx:latest
    LABEL version="1.0"
    LABEL maintainer="learning@example.com"
    ```

---

## Task 9: COPY vs ADD Instructions

1.  **Create Assets**:
    ```bash
    echo "<h1>Custom Image Page</h1>" > index.html
    mkdir assets
    touch assets/style.css
    tar -czvf assets.tar.gz assets/
    ```
2.  **Update Dockerfile**:
    ```dockerfile
    FROM nginx:latest
    LABEL version="1.0"
    
    # COPY: Best for local files
    COPY index.html /usr/share/nginx/html/index.html
    
    # ADD: Extracts tarballs automatically
    ADD assets.tar.gz /usr/share/nginx/html/
    ```

---

## Task 10: Build, Tag, and Caching

1.  **Build Image**:
    ```bash
    docker build -t my-app:v1 .
    ```
2.  **Test Cache**:
    *   Run the same command again.
    *   Observe "Using cache" (Build should be instant).

---

## Task 11: Docker Hub Integration

1.  **Tag for Hub**:
    ```bash
    # Replace <username> with your Docker Hub ID
    docker tag my-app:v1 <username>/my-app:v1
    ```
2.  **Login and Push**:
    ```bash
    docker login
    docker push <username>/my-app:v1
    ```

---

## Task 12: Advanced Cleanup

1.  **Remove All Containers**:
    ```bash
    docker rm -f $(docker ps -aq)
    ```
2.  **Remove All Images**:
    ```bash
    docker rmi -f $(docker images -q)
    ```
3.  **Prune Volumes**:
    ```bash
    docker volume prune -f
    ```
    *Warning: This deletes all unused volumes.*
