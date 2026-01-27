# Lab 02: Docker Installation and Management Homework

## Objective
In this lab, you will create an Ubuntu Virtual Machine in Azure, install Docker using the convenience script, configure rootless access, and practice basic container management commands using Nginx.

## Prerequisites
- An active Azure Subscription.
- A terminal (PowerShell, Bash, or Azure Cloud Shell).

## Task 1: Create a Ubuntu VM in Azure

1.  **Log in to Azure Portal**: Go to [portal.azure.com](https://portal.azure.com).
2.  **Create a Resource**: Click "Create a resource" > "Ubuntu Server 20.04 LTS" (or 22.04 LTS).
3.  **Configure Basics**:
    - **Resource Group**: `DockerLab_RG` (create new).
    - **Virtual Machine Name**: `DockerVM`.
    - **Region**: East US (or your preferred region).
    - **Image**: Ubuntu Server 20.04 LTS - Gen2.
    - **Size**: Standard_B1s (sufficient for this lab).
    - **Authentication type**: SSH public key.
    - **Username**: `azureuser`.
    - **Inbound port rules**: Allow selected ports (SSH 22). **IMPORTANT**: Also add port **8080** later or now to access Nginx.
4.  **Review + Create**: Click "Review + create", pass validation, and hit "Create".
5.  **Connect**: Once deployed, click "Go to resource" and connect via SSH.
    ```bash
    ssh azureuser@<VM-Public-IP>
    ```

> **Note**: Don't forget to open port **8080** in the Networking settings of your VM if you want to access the web server from your browser later.

---

## Task 2: Login and Install Docker

We will use the official Docker convenience script for a quick installation on Linux.

1.  **Update package database**:
    ```bash
    sudo apt update -y
    ```

2.  **Download and run the Docker installation script**:
    ```bash
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    ```

### Setup Rootless Access
By default, running Docker requires `sudo`. Let's configure it so you can run it as a regular user.

1.  **Create the docker group** (if it doesn't exist):
    ```bash
    sudo groupadd -f docker
    ```

2.  **Add your user to the docker group**:
    ```bash
    sudo usermod -aG docker "$USER"
    ```

3.  **Apply group changes**:
    You can either log out and log back in, or run:
    ```bash
    newgrp docker
    ```

4.  **Verify Docker installation (without sudo)**:
    ```bash
    docker --version
    docker ps
    ```
    *Output should show the version and an empty list of containers without permission errors.*

---

## Task 3: Pull an Image from Docker Hub

1.  **Pull the Nginx image**:
    ```bash
    docker pull nginx
    ```

2.  **Verify the image was pulled**:
    ```bash
    docker images
    ```
    *Concept checked: Docker Hub, Images*

---

## Task 4: Run a Container

1.  **Run Nginx in detached mode** mapping host port 8080 to container port 80:
    ```bash
    docker run -d -p 8080:80 --name my-nginx nginx
    ```

2.  **Verify the container is running**:
    ```bash
    docker ps
    ```

3.  **Access in Browser**:
    Open your web browser and navigate to:
    `http://<VM-Public-IP>:8080`
    
    *You should see the "Welcome to nginx!" default page.*

    > **Troubleshooting**: If the page doesn't load, check your Azure VM Networking settings. Ensure an Inbound Security Rule exists for port **8080** (Protocol: TCP, Source: Any, Destination port ranges: 8080).

    *Concept checked: Containers, Port Mapping*

---

## Task 5: Container Management

Practice the following lifecycle commands:

1.  **Stop the container**:
    ```bash
    docker stop my-nginx
    ```

2.  **Start the container**:
    ```bash
    docker start my-nginx
    ```

3.  **Restart the container**:
    ```bash
    docker restart my-nginx
    ```

4.  **Remove the container** (forcefully, since it's running):
    ```bash
    docker rm -f my-nginx
    ```

5.  **Verify it is gone**:
    ```bash
    docker ps -a
    ```
