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

Named volumes are the preferred method for persisting data. They are managed by Docker and stored in a dedicated area of the host filesystem (usually `/var/lib/docker/volumes` on Linux/VMs).

### Creating a Volume
```bash
docker volume create my-data-vol
```

### Mounting a Volume
Use the `-v` flag to mount the volume to a specific directory inside the container.

```bash
docker run -d \
  --name db-container \
  -v my-data-vol:/data \
  alpine
```
*   **Source**: `my-data-vol` (Managed by Docker)
*   **Destination**: `/data` (Inside the container)

### Verifying Persistence
1.  **Create data**: Enter the container and create a file in `/data`.
2.  **Delete container**: `docker rm -f db-container`.
3.  **New container**: Start a *new* container mounting the *same* volume.
4.  **Verify**: The file created in step 1 will still be there.

---

## 3. Managing Volumes

*   **List Volumes**:
    ```bash
    docker volume ls
    ```

*   **Inspect Volume** (Find physical location on host):
    ```bash
    docker volume inspect <volume_name>
    ```

*   **Remove Volume**:
    ```bash
    docker volume rm <volume_name>
    ```
    > [!WARNING]
    > You cannot remove a volume that is in use by a container (even a stopped one). Remove the container first.

*   **Prune Failure**:
    ```bash
    docker volume prune
    ```
    Removes all unused local volumes.

---

## Summary

| Storage Type | Characteristics | Best For |
| :--- | :--- | :--- |
| **Container Layer** | Ephemeral, lost on deletion | Temporary files, scratch space |
| **Named Volume** | Persistent, managed by Docker | Database storage, sharing data between containers |
| **Bind Mount** | Maps exact host path to container | Development (live code reloading), config files |
