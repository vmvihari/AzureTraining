# Container Operations & Management

This document covers intermediate container operations, including interactive sessions, file management inside containers, and troubleshooting techniques.

## 1. Container Naming & Execution

By default, Docker assigns random names to containers. Naming them makes management easier.

### Naming Containers
Use the `--name` flag to assign a custom name:
```bash
docker run -d --name my-web-server -p 8080:80 nginx
```

### Interactive Modes
Understanding the difference between creating a container and entering an existing one:

| Command | Purpose |
| :--- | :--- |
| `docker run -it <image>` | **Creates** a new container and enters it immediately. Useful for temporary tasks. |
| `docker exec -it <container> bash` | **Enters** an *already running* container. Useful for debugging specific instances. |

> [!NOTE]
> If `bash` is not available (common in Alpine images), try `sh` instead: `docker exec -it <container> sh`.

---

## 2. File Operations Inside Containers

Minimal container images often lack text editors (`nano`, `vi`). You can use shell redirection or `docker cp` to manage files.

### modifying Files without Editors
Use `echo` or `cat` with redirection:

*   **Overwrite (`>`)**: Replaces the entire file content.
    ```bash
    # Replaces index.html with "Hello World"
    echo "<h1>Hello World</h1>" > /usr/share/nginx/html/index.html
    ```

*   **Append (`>>`)**: Adds content to the end of the file.
    ```bash
    echo "New log entry" >> /var/log/app.log
    ```

### Copying Files (`docker cp`)
You can copy files between your host machine and a container without entering it.

1.  **Host to Container**:
    ```bash
    # Create file locally
    echo "<h1>Custom Page</h1>" > index.html
    
    # Copy to container
    docker cp index.html <container_name>:/usr/share/nginx/html/index.html
    ```

2.  **Container to Host**:
    ```bash
    docker cp <container_name>:/etc/nginx/nginx.conf ./local_nginx.conf
    ```

---

## 3. Installing Tools

In full OS containers (like `ubuntu`), you can install utilities just like on a virtual machine.

**Example: Installing `figlet` in an Ubuntu container:**
1.  Run the container: `docker run -it ubuntu bash`
2.  Update package lists: `apt-get update`
3.  Install the tool: `apt-get install figlet`
4.  Run it: `figlet Hello`

> [!IMPORTANT]
> Changes made (like installed packages) inside a standard container are **lost** when the container is removed, unless you commit the container as a new image.

---

## 4. Troubleshooting & Logs

### Real-Time Logs
Standard `docker logs` shows past output and exits. To monitor an application in real-time (e.g., watching web requests):

```bash
docker logs -f <container_name>
```
*   Press `Ctrl+C` to exit the log stream (this does not stop the container).

### Inspecting Container Details
To find specific details like IP address, environment variables, or mounts:
```bash
docker inspect <container_name>
```
