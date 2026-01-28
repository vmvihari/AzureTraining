# Lab 04: Docker Volumes and Advanced Builds

## Objective
To master Docker data persistence using Named and Bind volumes, and to understand Dockerfile instructions including `COPY` vs `ADD`, `LABEL`, and build caching.

## Prerequisites
- An active Azure Subscription.
- A terminal (PowerShell, Bash, or Azure Cloud Shell).
- Docker installed on the VM.

---

## Task 1: Named Volume with NGINX (Persist Data)

**Goal**: Create a named volume, mount it to NGINX web root, and verify data persists even after container deletion.

1.  **Create a named volume**:
    ```bash
    docker volume create demo_vol
    docker volume ls
    ```
2.  **Create a temporary container** to write HTML into the named volume:
    ```bash
    docker run --rm -it -v demo_vol:/data alpine sh -c 'echo "<h1>Named Volume Page</h1>" > /data/index.html'
    ```
3.  **Run NGINX container** using the named volume:
    ```bash
    docker run -d --name web_named -p 8080:80 -v demo_vol:/usr/share/nginx/html nginx:latest
    docker ps
    ```
4.  **Verify in browser**:
    *   Open: `http://<VM-IP>:8080` or `http://localhost:8080`
5.  **Delete container and re-run** to confirm persistence:
    ```bash
    docker rm -f web_named
    docker run -d --name web_named2 -p 8080:80 -v demo_vol:/usr/share/nginx/html nginx:latest
    ```
6.  **Verify again in browser**:
    *   Visit `http://<VM-IP>:8080`
    *   *Expected*: Same "Named Volume Page" should still appear.

---

## Task 2: Bind Volume with NGINX (Live Sync from Host)

**Goal**: Mount a local folder into the container and verify changes reflect instantly.

1.  **Create a folder and index.html on host**:
    ```bash
    mkdir -p /tmp/html_bind
    cd /tmp/html_bind
    cat > index.html <<EOF
    <h1>Bind Volume Page - Version 1</h1>
    EOF
    ls -l
    ```
2.  **Run NGINX with bind mount**:
    ```bash
    docker run -d --name web_bind -p 8081:80 -v /tmp/html_bind:/usr/share/nginx/html nginx:latest
    docker ps
    ```
3.  **Verify in browser**:
    *   Visit `http://<VM-IP>:8081` or `http://localhost:8081`
4.  **Modify the file locally and refresh browser**:
    ```bash
    cat > /tmp/html_bind/index.html <<EOF
    <h1>Bind Volume Page - Version 2</h1>
    EOF
    ```
    *   *Expected*: Browser should show "Version 2" after refresh.
5.  **Cleanup**:
    ```bash
    docker rm -f web_bind
    ```

---

## Task 3: Create Dockerfile (FROM + LABEL) and Build Image

**Goal**: Create a basic Dockerfile using NGINX base image and labels.

1.  **Create working folder**:
    ```bash
    mkdir -p ~/docker_hw
    cd ~/docker_hw
    ```
2.  **Create Dockerfile**:
    ```bash
    cat > Dockerfile <<EOF
    FROM nginx:latest
    LABEL org="NCPL"
    LABEL version="v1"
    LABEL description="Custom NGINX image for Docker practice"
    EOF
    ```
3.  **Build image**:
    ```bash
    docker build -t demo-nginx:v1 .
    docker images | head
    ```
4.  **Run container**:
    ```bash
    docker run -d --name my_demo -p 8082:80 demo-nginx:v1
    ```
5.  **Verify**:
    *   Visit `http://<VM-IP>:8082`
6.  **Cleanup**:
    ```bash
    docker rm -f my_demo
    ```

---

## Task 4: COPY Instruction (Copy index.html into NGINX path)

**Goal**: Use COPY to place your custom index.html inside `/usr/share/nginx/html/`.

1.  **Inside `~/docker_hw`, create `index.html`**:
    ```bash
    cd ~/docker_hw
    cat > index.html <<EOF
    <h1>Copied via Dockerfile COPY</h1>
    EOF
    ```
2.  **Update Dockerfile**:
    ```bash
    cat > Dockerfile <<EOF
    FROM nginx:latest
    LABEL org="NCPL"
    LABEL version="v2"
    LABEL description="NGINX with custom index.html using COPY"
    COPY index.html /usr/share/nginx/html/index.html
    EOF
    ```
3.  **Build and run**:
    ```bash
    docker build -t demo-nginx:v2 .
    docker run -d --name copy_test -p 8083:80 demo-nginx:v2
    ```
4.  **Verify**:
    *   Visit `http://<VM-IP>:8083`
5.  **Login into container and verify file**:
    ```bash
    docker exec -it copy_test bash
    ls -l /usr/share/nginx/html/
    cat /usr/share/nginx/html/index.html
    exit
    ```
6.  **Cleanup**:
    ```bash
    docker rm -f copy_test
    ```

---

## Task 5: ADD vs COPY (Extraction Difference)

**Goal**: Prove that ADD extracts `.tar.gz` automatically but COPY does not.

### Part A: ADD Extracts tar.gz

1.  **Create a sample folder and tar.gz**:
    ```bash
    mkdir -p ~/docker_hw/add_test/files
    cd ~/docker_hw/add_test/files
    echo "Hello from file1" > file1.txt
    echo "Hello from file2" > file2.txt
    cd ..
    tar -czf sample.tar.gz -C files .
    ls -l
    ```
2.  **Create Dockerfile using ADD**:
    ```bash
    cat > Dockerfile <<EOF
    FROM alpine:latest
    ADD sample.tar.gz /opt/
    CMD ["sh", "-c", "ls -l /opt && sleep 300"]
    EOF
    ```
3.  **Build and run**:
    ```bash
    docker build -t add-demo:v1 .
    docker run -d --name add_container add-demo:v1
    ```
4.  **Check inside container**:
    ```bash
    docker exec -it add_container sh
    ls -l /opt
    cat /opt/file1.txt
    exit
    ```
    *Expected*: `/opt/file1.txt` and `/opt/file2.txt` exist (extracted).
5.  **Cleanup**:
    ```bash
    docker rm -f add_container
    ```

### Part B: COPY does NOT extract

1.  **Replace Dockerfile with COPY**:
    ```bash
    cat > Dockerfile <<EOF
    FROM alpine:latest
    COPY sample.tar.gz /opt/
    CMD ["sh", "-c", "ls -l /opt && sleep 300"]
    EOF
    ```
2.  **Build and run**:
    ```bash
    docker build -t copy-demo:v1 .
    docker run -d --name copy_container copy-demo:v1
    ```
3.  **Check inside container**:
    ```bash
    docker exec -it copy_container sh
    ls -l /opt
    exit
    ```
    *Expected*: Only `sample.tar.gz` exists, not extracted.
4.  **Cleanup**:
    ```bash
    docker rm -f copy_container
    ```

---

## Task 6: Docker Build Cache Test

**Goal**: Observe Docker cache speeding up builds.

1.  **Build once (note time)**:
    ```bash
    cd ~/docker_hw
    time docker build -t cache-test:v1 .
    ```
2.  **Build again without changes**:
    ```bash
    time docker build -t cache-test:v1 .
    ```
    *Expected*: Second build is faster ("Using cache" appears in output).
3.  **Change label and rebuild**:
    ```bash
    sed -i 's/version="v2"/version="v2.1"/' Dockerfile
    time docker build -t cache-test:v2.1 .
    ```
    *Expected*: Cache breaks for layers after the modified line.
