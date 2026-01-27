# Lab 02: Docker Installation and Management Homework

## Objective
In this lab, you will perform a comprehensive hands-on practice with Docker on a Linux VM. You will go through installation, permission management, system exploration, image and container operations, and cleanup.

## Prerequisites
- An active Azure Subscription.
- A terminal (PowerShell, Bash, or Azure Cloud Shell).

---

## Task 1: Install Docker on Linux

1.  **Launch an Ubuntu Linux VM** in Azure (e.g., Standard_B1s, Ubuntu 20.04/22.04 LTS).
2.  **Log in to the VM** using SSH:
    ```bash
    ssh azureuser@<VM-Public-IP>
    ```
3.  **Update the system packages**:
    ```bash
    sudo apt update
    ```
4.  **Download the official Docker installation script**:
    ```bash
    curl -fsSL https://get.docker.com -o get-docker.sh
    ```
5.  **Execute the script to install Docker**:
    ```bash
    sudo sh get-docker.sh
    ```
6.  **Verify Docker installation**:
    ```bash
    sudo docker --version
    ```
7.  **Run the hello-world container**:
    ```bash
    sudo docker run hello-world
    ```

---

## Task 2: Fix Docker Permission Issue

1.  **Try running a command without sudo** and observe the "permission denied" error:
    ```bash
    docker ps
    ```
2.  **Add your Linux user to the docker group**:
    ```bash
    sudo usermod -aG docker $USER
    ```
3.  **Refresh the group session**:
    ```bash
    newgrp docker
    ```
4.  **Confirm access is fixed**:
    ```bash
    docker ps
    ```
    *(Should list containers without error)*

---

## Task 3: Explore Docker System Commands

1.  **Check Docker disk usage**:
    ```bash
    docker system df
    ```
2.  **View Docker system information**:
    ```bash
    docker info
    ```
3.  **Monitor Docker system events**:
    *   Open a new terminal tab, SSH into the VM, and run:
        ```bash
        docker events
        ```
    *   Keep this running.
4.  **Generate events**:
    *   In your original terminal:
        ```bash
        docker run --rm hello-world
        ```
5.  **Observe events**: Check the `docker events` tab to see the "create", "start", "die", etc. events.

---

## Task 4: Work with Docker Images

1.  **Search for the nginx image**:
    ```bash
    docker search nginx
    ```
2.  **Pull the nginx image** (defaults to `latest`):
    ```bash
    docker pull nginx
    ```
3.  **Pull the ubuntu image**:
    ```bash
    docker pull ubuntu
    ```
4.  **List all locally available images**:
    ```bash
    docker images
    ```
5.  **Note**: Observe under the "TAG" column that `latest` was downloaded because no specific tag was provided.

---

## Task 5: Run Containers and Observe Behavior

1.  **Run an ubuntu container normally**:
    ```bash
    docker run ubuntu
    ```
2.  **Check container status**:
    ```bash
    docker ps -a
    ```
    *Observation: It status is "Exited".*
3.  **Run an nginx container**:
    ```bash
    docker run -d nginx
    ```
4.  **Check running containers**:
    ```bash
    docker ps
    ```
    *Observation: Nginx stays "Up".*
5.  **Why?** Ubuntu container exited because it had no foreground process to keep it alive (it just started bash and exited). Nginx has a built-in foreground process (the web server) that keeps running.

---

## Task 6: Container Lifecycle Management

1.  **Stop the running nginx container**:
    ```bash
    docker stop <container_id_or_name>
    ```
2.  **Start the same container again**:
    ```bash
    docker start <container_id_or_name>
    ```
3.  **Check container logs**:
    ```bash
    docker logs <container_id_or_name>
    ```
4.  **View real-time logs**:
    ```bash
    docker logs -f <container_id_or_name>
    ```
    *(Press Ctrl+C to exit)*
5.  **Stop the container again**:
    ```bash
    docker stop <container_id_or_name>
    ```

---

## Task 7: Run Container in Detached Mode with Name

1.  **Run nginx in detached mode with a name**:
    ```bash
    docker run -d --name my-web-server nginx
    ```
2.  **Verify it is running**:
    ```bash
    docker ps
    ```
3.  **Confirm detached mode**: Your terminal prompt returned immediately, meaning it's running in the background.

---

## Task 8: Port Binding and Browser Access

1.  **Run nginx with port mapping (Host 8080 -> Container 80)**:
    ```bash
    docker run -d -p 8080:80 --name public-web nginx
    ```
2.  **Open VM's Security Rules**:
    *   Go to Azure Portal > Your VM > Networking.
    *   Add Inbound Port Rule: Destination Port `8080`, Protocol `TCP`, Action `Allow`.
3.  **Access functionality**:
    *   Open browser: `http://<VM-Public-IP>:8080`
    *   *Verify you see "Welcome to nginx!"*

---

## Task 9: Multiple Containers from Same Image

1.  **Run a second nginx container on port 8081**:
    ```bash
    docker run -d -p 8081:80 --name secondary-web nginx
    ```
    *(Remember to open port 8081 in Azure Networking if you want to test externally)*
2.  **Verify both are running**:
    ```bash
    docker ps
    ```
3.  **Access**: You now have two separate web servers running from the same image on different ports.

---

## Task 10: Image Tagging and Docker Hub Login

1.  **Retag the nginx image**:
    ```bash
    # Replace <your-dockerhub-username>
    docker tag nginx <your-dockerhub-username>/my-nginx-custom:v1
    ```
2.  **Create Access Token**:
    *   Go to [hub.docker.com](https://hub.docker.com) > Settings > Security > New Access Token.
3.  **Login to Docker Hub**:
    ```bash
    docker login -u <your-dockerhub-username>
    # Paste the token when prompted for password
    ```
4.  **Push the image**:
    ```bash
    docker push <your-dockerhub-username>/my-nginx-custom:v1
    ```
5.  **Verify**: Check your repository on Docker Hub to see the new image.

---

## Task 11: Cleanup Containers

1.  **List all containers (running and stopped)**:
    ```bash
    docker ps -a
    ```
2.  **Remove all containers at once**:
    *   **Warning**: This deletes everything!
    ```bash
    docker rm -f $(docker ps -aq)
    ```
    *   `-f`: Force removal (for running containers).
    *   `$(docker ps -aq)`: Sub-command that lists all container IDs.
3.  **Verify**:
    ```bash
    docker ps -a
    ```
    *(Should be empty)*

---

## Task 12: Cleanup Images

1.  **List all images**:
    ```bash
    docker images
    ```
2.  **Remove all images at once**:
    ```bash
    docker rmi -f $(docker images -q)
    ```
3.  **Confirm**:
    ```bash
    docker images
    ```
    *(Should be empty)*
