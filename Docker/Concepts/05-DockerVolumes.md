# Docker Storage & Volumes

This document explains how to handle data persistence in Docker. By default, containers are **ephemeral**, meaning data is lost when they are removed. Docker Volumes solve this problem.

## 1. The Ephemeral Nature of Containers

When you write files inside a container's writable layer:
1.  The data is tightly coupled to that specific container.
2.  If the container is deleted (`docker rm`), the data is deleted with it.
3.  Sharing data between containers is difficult.

To persist data, we use **Volumes**.

---

## 2. Named Volumes

Named volumes are the preferred method for persisting data in **production** or when you simply want data to survive container restarts without caring where it is stored on the host. They are managed by Docker.

### Creating a Volume
```bash
docker volume create my-data-vol
```

### Mounting a Volume
Use the `-v` flag to mount the volume.

```bash
docker run -d \
  --name db-container \
  -v my-data-vol:/data \
  alpine
```
*   **Source**: `my-data-vol` (Managed by Docker, usually in `/var/lib/docker/volumes`).
*   **Destination**: `/data` (Inside the container).

### Verifying Persistence
1.  **Create data**: Enter the container and create a file in `/data`.
2.  **Delete container**: `docker rm -f db-container`.
3.  **New container**: Start a *new* container mounting the *same* volume.
4.  **Verify**: The file will still be there.

---

## 3. Bind Mounts

Bind mounts map a specific file or directory on the **host machine** to a file or directory inside the container. This is essential for **development**.

### How it Works
You provide the exact path on your host machine. Any change you make in that folder is immediately visible inside the container, and vice versa.

### Usage Example (Nginx)
Imagine you have an `index.html` file in your current directory on your laptop/VM (`$(pwd)`).

```bash
docker run -d \
  --name dev-web \
  -p 8080:80 \
  -v $(pwd):/usr/share/nginx/html \
  nginx
```

*   **Source**: `$(pwd)` (Current directory on Host).
*   **Destination**: `/usr/share/nginx/html` (Nginx default web root).

### Development Workflow
1.  Start the container with a bind mount.
2.  Edit `index.html` locally using VS Code or Notepad.
3.  Refresh the browser. You see changes **instantly**.
4.  No need to rebuild the image for every simple HTML/CSS change.

---

## 4. Managing Volumes

*   **List Volumes**:
    ```bash
    docker volume ls
    ```

*   **Inspect Volume** (Find physical location):
    ```bash
    docker volume inspect <volume_name>
    ```

*   **Remove Volume**:
    ```bash
    docker volume rm <volume_name>
    ```

*   **Prune Failure**:
    ```bash
    docker volume prune
    ```
    *Removes all unused local volumes.*

---

## Summary: Named vs. Bind

| Feature | Named Volume | Bind Mount |
| :--- | :--- | :--- |
| **Managed By** | Docker (`/var/lib/docker/volumes/...`) | You (Local Host Filesystem) |
| **Best For** | Database storage, Production persistence | Local Development, Live Code Reloading |
| **Dependence** | Independent of host folder structure | Dependent on host OS directory structure |
| **Performance** | High | Variable (depends on host OS) |
