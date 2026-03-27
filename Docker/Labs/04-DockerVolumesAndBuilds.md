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

---

## Task 7: Optimizing Layers with RUN

**Goal**: Reduce image size and layers by combining commands.

1.  **Create Bad Dockerfile (Multiple RUN commands)**:
    ```bash
    cat > Dockerfile.bad <<EOF
    FROM ubuntu:latest
    RUN apt-get update
    RUN apt-get install -y curl
    RUN apt-get install -y vim
    EOF
    ```
2.  **Build Bad Image**:
    ```bash
    docker build -f Dockerfile.bad -t bad-optimization:v1 .
    ```
3.  **Create Good Dockerfile (Chained commands)**:
    ```bash
    cat > Dockerfile.good <<EOF
    FROM ubuntu:latest
    RUN apt-get update && \
        apt-get install -y curl vim && \
        rm -rf /var/lib/apt/lists/*
    EOF
    ```
4.  **Build Good Image**:
    ```bash
    docker build -f Dockerfile.good -t good-optimization:v1 .
    ```
5.  **Compare History/Layers**:
    ```bash
    docker history bad-optimization:v1
    docker history good-optimization:v1
    ```
    *   *Observation*: The "good" image has fewer layers contributed by the `RUN` command.

---

## Task 8: WORKDIR Demonstration

**Goal**: Show how WORKDIR changes the context for all future commands.

1.  **Create Dockerfile**:
    ```bash
    cat > Dockerfile.workdir <<EOF
    FROM alpine:latest
    WORKDIR /app
    RUN echo "I am in /app" > info.txt
    WORKDIR /app/data
    RUN echo "I am in /app/data" > data.txt
    EOF
    ```
2.  **Build and Run**:
    ```bash
    docker build -f Dockerfile.workdir -t workdir-demo:v1 .
    docker run --rm workdir-demo:v1 sh -c 'ls -l /app && ls -l /app/data'
    ```
    *   *Expected*: `info.txt` is in `/app`, `data.txt` is in `/app/data`.

---

## Task 9: CMD vs ENTRYPOINT

**Goal**: Verify how `docker run` arguments override (or don't override) startup commands.

### Part A: CMD (Overridable)

1.  **Create Dockerfile**:
    ```bash
    cat > Dockerfile.cmd <<EOF
    FROM alpine:latest
    CMD ["echo", "Hello from CMD"]
    EOF
    ```
2.  **Build**:
    ```bash
    docker build -f Dockerfile.cmd -t cmd-demo:v1 .
    ```
3.  **Run with Default**:
    ```bash
    docker run --rm cmd-demo:v1
    # Output: Hello from CMD
    ```
4.  **Run with Override**:
    ```bash
    docker run --rm cmd-demo:v1 echo "Overridden!"
    # Output: Overridden!
    ```

### Part B: ENTRYPOINT (Persistent)

1.  **Create Dockerfile**:
    ```bash
    cat > Dockerfile.entry <<EOF
    FROM alpine:latest
    ENTRYPOINT ["echo", "Hello from ENTRYPOINT"]
    EOF
    ```
2.  **Build**:
    ```bash
    docker build -f Dockerfile.entry -t entry-demo:v1 .
    ```
3.  **Run with Default**:
    ```bash
    docker run --rm entry-demo:v1
    # Output: Hello from ENTRYPOINT
    ```
4.  **Run with Args**:
    ```bash
    docker run --rm entry-demo:v1 "Extra Args"
    # Output: Hello from ENTRYPOINT Extra Args
    ```
