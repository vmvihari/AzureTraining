# Lab 03: Docker Practical Homework

## Objective
To practice running containers, managing access, working inside containers, viewing logs, and understanding Docker volumes with hands-on commands.

## Prerequisites
*   Docker installed on your machine (or VM).
*   User added to `docker` group (Task 2 covers this).

---

## Task 1: Run NGINX Container with Custom Name and Port Mapping
**Description**: Run an NGINX container with a custom name, map a host port to container port 80, and verify browser access.

### Commands
```bash
docker pull nginx
docker run -d --name nginx-app -p 8081:80 nginx
docker ps
```

### Verification
Open in browser: `http://<VM-PUBLIC-IP>:8081`

---

## Task 2: Fix Docker Permission Issue (Docker Group)
**Description**: Allow Docker commands to run without using sudo.

### Commands
```bash
docker ps
# If you get permission denied:
sudo usermod -aG docker $USER
newgrp docker
docker ps
```

---

## Task 3: Check Container Logs (Normal and Real-Time)
**Description**: View NGINX container logs and observe real-time logs when accessing the application.

### Commands
```bash
docker logs nginx-app
docker logs -f nginx-app
```

### Verification
Refresh the browser multiple times and observe logs updating live in the terminal.

---

## Task 4: Enter Inside a Running Container
**Description**: Access the running container and confirm you are inside the container environment.

### Commands
```bash
docker exec -it nginx-app /bin/bash
hostname
exit
```

---

## Task 5: Locate NGINX Default HTML Page
**Description**: Identify where NGINX serves its default HTML file from.

### Commands
```bash
docker exec -it nginx-app /bin/bash
cd /usr/share/nginx/html
ls
cat index.html
exit
```

---

## Task 6: Modify HTML File Without Editors
**Description**: Overwrite the default NGINX page using shell redirection since editors are not available.

### Commands
```bash
docker exec -it nginx-app /bin/bash
echo "<h1>Welcome to Docker NGINX</h1>" > /usr/share/nginx/html/index.html
exit
```

### Verification
Refresh browser and confirm page change.

---

## Task 7: Understand > vs >> (Overwrite vs Append)
**Description**: Append additional content without removing existing data.

### Commands
```bash
docker exec -it nginx-app /bin/bash
echo "<p>Appended Content</p>" >> /usr/share/nginx/html/index.html
exit
```

### Verification
Refresh browser and observe appended text.

---

## Task 8: Copy File into Running Container
**Description**: Copy an HTML file from VM into a running container.

### Commands (On VM)
```bash
echo "<h1>Custom Page from Host</h1>" > index.html
docker cp index.html nginx-app:/usr/share/nginx/html/index.html
```

### Verification
Refresh browser.

---

## Task 9: docker run -it vs docker exec -it
**Description**: Understand the difference between creating a container and entering an existing one.

### Commands
```bash
# Create and enter a NEW container
docker run -it --name ubuntu-test ubuntu /bin/bash
exit
# Container stops after exit

# Start it back up
docker start ubuntu-test

# Enter the EXISTING running container
docker exec -it ubuntu-test /bin/bash
exit
```

---

## Task 10: Ubuntu Container Exit Behavior
**Description**: Observe how Ubuntu containers stop when no foreground process exists.

### Commands
```bash
docker run --name ubuntu-exit ubuntu
docker ps -a
```
*Observation*: Status is 'Exited'.

---

## Task 11: Install a Tool Inside Ubuntu Container
**Description**: Install a package inside an Ubuntu container.

### Commands
```bash
docker start ubuntu-test
docker exec -it ubuntu-test /bin/bash
apt update
apt install figlet -y
figlet Docker
exit
```

---

## Task 12: Demonstrate Container Ephemerality
**Description**: Show that data inside a container is lost after removal.

### Commands
```bash
# Create data in existing container
docker exec -it nginx-app /bin/bash
touch /tmp/testfile
exit

# Remove container
docker rm -f nginx-app

# Create NEW container
docker run -d --name nginx-new -p 8081:80 nginx

# Check for file
docker exec -it nginx-new ls /tmp
```
*Observation*: `testfile` is gone.

---

## Task 13: Create a Named Docker Volume
**Description**: Create and inspect a Docker named volume.

### Commands
```bash
docker volume create myvolume
docker volume ls
docker volume inspect myvolume
```

---

## Task 14: Mount Named Volume into Container
**Description**: Mount a Docker volume into a container and verify data sharing.

### Commands
```bash
docker run -it --name volume-test -v myvolume:/app ubuntu /bin/bash
cd /app
touch file1.txt
exit
```

---

## Task 15: Verify Data Persistence After Container Removal
**Description**: Remove container and reattach the same volume to a new container.

### Commands
```bash
docker rm volume-test
docker run -it --name volume-test2 -v myvolume:/app ubuntu /bin/bash
ls /app
exit
```
*Observation*: `file1.txt` is still there!

---

## Submission Requirement
1.  **Commands executed** (terminal output or list of commands).
2.  **Browser screenshots** (NGINX page).
3.  **Short explanation**:
    *   Why containers are ephemeral?
    *   Why volumes are required?
