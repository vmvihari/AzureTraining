# Docker Architecture & Commands

This document covers the core concepts of Docker architecture, installation, and essential commands for managing images and containers, based on practical session learnings.

## 1. Docker Architecture

Docker uses a **Client-Server** architecture:

*   **Docker Client (CLI)**: The command-line tool (`docker`) that you use to issue commands. It sends requests to the Docker Daemon.
*   **Docker Daemon (`dockerd`)**: The background service running on the host machine. It listens for API requests and manages Docker objects (images, containers, networks, volumes).

### Permissions & Security
By default, the Docker daemon listens on a Unix socket owned by the `root` user and the `docker` group.
*   **Issue**: Regular users cannot access the socket and get a "permission denied" error.
*   **Fix**: Add the user to the `docker` group: `sudo usermod -aG docker $USER`.
*   **Effect**: Allows running `docker` commands without `sudo`.

---

## 2. Installation (Convenience Script)

While you can install Docker via standard repositories, the **convenience script** is a quick way to install the latest version on development environments.

```bash
# Download the script
curl -fsSL https://get.docker.com -o get-docker.sh

# Execute the script
sudo sh get-docker.sh
```

---

## 3. System Commands

These commands help you understand the state of your Docker environment.

*   `docker info`: Display system-wide information (kernel version, number of containers/images, storage driver).
*   `docker system df`: Show Docker disk usage (size of images, containers, and volumes).
*   `docker events`: Stream real-time events from the server (e.g., container create, start, die). Useful for monitoring.
*   `docker system prune`: **Destructive command**. Removes all unused data (stopped containers, unused networks, dangling images). Use with caution!

---

## 4. Image Categories & Operations

### Image Types
*   **Official Images**: Maintained by Docker or upstream software providers (e.g., `nginx`, `python`). Preferred for security.
*   **Custom Images**: Built by users or organizations.

### Key Commands
*   `docker search <term>`: Search Docker Hub for images.
*   `docker pull <image>:<tag>`: Download an image. If tag is omitted, `:latest` is used by default.
*   `docker images`: List locally available images.
*   `docker rmi <image_id>`: Remove an image.
*   `docker rmi $(docker images -q)`: Bulk remove all images (requires force `-f` if used by stopped containers).

---

## 5. Container Operations

A container runs only as long as its main process is running.

### Lifecycle
*   `docker run <image>`: Create and start a container.
*   `docker stop <container>`: Gracefully stop a running container.
*   `docker start <container>`: Start a stopped container.
*   `docker restart <container>`: Stop then start.
*   `docker rm <container>`: Remove a stopped container (use `-f` to force remove a running one).

### Modes
*   **Foreground (Default)**: Attaches your terminal to the container's output.
*   **Detached (`-d`)**: Runs in the background. Terminal remains free.

### Port Binding
Services inside containers are isolated. To access them, you must map a host port to the container port.
*   **Syntax**: `-p <HostPort>:<ContainerPort>`
*   **Example**: `docker run -d -p 8080:80 nginx` maps host port 8080 to container's web server (port 80).

### Logs
*   `docker logs <container>`: View output.
*   `docker logs -f <container>`: Follow log output in real-time.

---

## 6. Docker Hub Integration

To push images to your personal repository:
1.  **Tag**: `docker tag <local_image> <username>/<repo>:<tag>`
2.  **Login**: `docker login` (use a Personal Access Token for password).
3.  **Push**: `docker push <username>/<repo>:<tag>`
